"""Huly CLI commands: `setup huly` (guided setup), `setup huly --check` (status) and read-only task queries.

`setup huly` flow (same for a developer in a terminal and for an agent using --json):

  0. Check the project .env: URL, email, password, session token and workspace ID.
     All present -> verify by reading one open task, done.
  1. Step 1 - URL: ask (or take --url), ping it. Unreachable -> stop. Reachable -> save
     HULY_WORKSPACE_URL to .env immediately.
  2. Step 2 - Account: ask email/password (or --email/--password/--password-stdin), log in.
     Interactive: repeat until login succeeds. Success -> save email, password, session
     token and workspace ID to .env.
  3. Verify: read the user's open tasks and show the first one.

All values live in the project's .env, which is DEVELOPMENT ONLY.
"""

import argparse
import asyncio
import getpass
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable, Optional

import httpx

from ..huly.auth import load_client_credentials, update_env_values
from ..huly.client import HulyClient
from ..huly.models import HulyCredentials

DEFAULT_HULY_URL = "https://huly.app"

# Exit codes of `setup huly` (stable: agents and scripts rely on them).
EXIT_OK = 0
EXIT_LOGIN_FAILED = 1
EXIT_URL_UNREACHABLE = 2
EXIT_NEEDS_INPUT = 3
EXIT_VERIFY_FAILED = 4
EXIT_ABORTED = 130


def cmd_login(args: argparse.Namespace) -> int:
    """`coder-nexus login`: alias of `setup huly`."""
    return cmd_setup_huly(args)


def cmd_my_tasks(args: argparse.Namespace) -> int:
    """Handle `coder_nexus my-tasks` command."""
    workspace_path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()
    client = HulyClient.from_workspace(workspace_path)

    async def _fetch():
        return await client.get_my_uncompleted_tasks(workspace_path=workspace_path, include_all=getattr(args, "include_all", False))

    try:
        tasks = asyncio.run(_fetch())
        if args.json:
            print(json.dumps([t.model_dump() for t in tasks], indent=2))
            return 0

        scope = "Open tasks in the workspace" if getattr(args, "include_all", False) else "My open tasks"
        print(f"\n📋 {scope} ({len(tasks)}):")
        print(f"{'ID':<12} | {'PRIORITY':<8} | {'STATUS':<12} | {'TITLE'}")
        print("-" * 75)
        for t in tasks:
            print(f"{t.id:<12} | {t.priority.upper():<8} | {t.status:<12} | {t.title}")
        print("-" * 75 + "\n")
        return 0
    except Exception as exc:
        print(f"❌ Failed to fetch tasks: {exc}", file=sys.stderr)
        return 1


def cmd_task_detail(args: argparse.Namespace) -> int:
    """Handle `coder_nexus task-detail <task_id>` command."""
    from ..server import default_sources_dir, ensure_sources_ignored
    workspace_path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()
    client = HulyClient.from_workspace(workspace_path)
    download_dir = None
    if getattr(args, "download", False):
        sources_dir = default_sources_dir(workspace_path, args.task_id)
        ensure_sources_ignored(sources_dir)
        download_dir = str(sources_dir)

    async def _fetch():
        return await client.get_task_detail(args.task_id, workspace_path=workspace_path, download_dir=download_dir)

    try:
        d = asyncio.run(_fetch())
    except Exception as exc:
        print(f"❌ Failed to fetch task detail: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(d.model_dump(), indent=2, ensure_ascii=False))
        return 0

    line = "=" * 64
    print(f"\n{line}\n📌 [{d.id}] {d.title}")
    print(f"   Status: {d.status} ({d.status_category or '?'}) | Priority: {d.priority} | "
          f"Assignee: {d.assignee_name or d.assignee or 'Unassigned'} | Due: {d.due_date or '-'}")
    if d.parent:
        print(f"   ⬆️  Parent: [{d.parent.id}] {d.parent.title} ({d.parent.status or '?'})")
    print(line)
    print(f"\n📝 Description:\n{d.description or '(empty)'}\n")
    print(f"🎯 Acceptance Criteria (source: {d.acceptance_criteria_source}):")
    if not d.acceptance_criteria:
        print("  (none written in the ticket - confirm them with the requester)")
    for idx, ac in enumerate(d.acceptance_criteria, 1):
        print(f"  [{idx}] {ac}")
    if d.sub_issues:
        open_n = sum(1 for c in d.sub_issues if not c.is_closed)
        print(f"\n🧩 Sub-issues: {len(d.sub_issues)} ({open_n} open)")
        for c in d.sub_issues:
            mark = "✔" if c.is_closed else "•"
            extra = f", {len(c.acceptance_criteria)} AC" if c.acceptance_criteria else ", no AC"
            deeper = f", +{c.sub_issue_count} nested" if c.sub_issue_count else ""
            who = f" — {c.assignee_name}" if c.assignee_name else ""
            print(f"  {mark} [{c.id}] {c.title}  ({c.status}{extra}{deeper}){who}")
    if d.comments:
        print(f"\n💬 Comments ({len(d.comments)}):")
        for c in d.comments:
            print(f"  - {c.created_at or ''} {c.author or 'unknown'}: {c.text}")
    if d.sources:
        print(f"\n📎 Sources ({len(d.sources)}):")
        icons = {"READ": "✅", "DOWNLOADED": "⬇️ ", "AVAILABLE": "•", "UNREACHABLE": "⛔", "EXTERNAL": "🌐", "NOT_PROVIDED": "∅"}
        for s in d.sources:
            where = s.local_path or s.url or ""
            note = f" — {s.note}" if s.note else ""
            print(f"  {icons.get(s.status, '•')} {s.status:<11} {s.kind:<10} {s.title}  [{s.origin}] {where}{note}")
        if not download_dir and (d.figma_url or any(s.status == "AVAILABLE" for s in d.sources)):
            print("  → Re-run with --download to save files into .superpowers/sources/" + d.id + "/")
    if d.figma_url:
        print(f"\n🎨 Figma URL: {d.figma_url}")
    print(line + "\n")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Check current authentication status in client workspace .env."""
    workspace_path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()
    creds = load_client_credentials(workspace_path)

    print(f"\n🔍 Huly Client Environment Status:")
    print(f"   Workspace Path : {workspace_path}")
    print(f"   Target .env    : {Path(workspace_path) / '.env'}")
    print(f"   Workspace URL  : {creds.workspace_url}")
    print(f"   Email          : {creds.email or '(not set)'}")
    print(f"   Workspace ID   : {creds.workspace_id or '(not resolved)'}")
    print(f"   Has Session    : {'Yes' if creds.session_token else 'No'}")
    print(f"   Authenticated  : {'Yes' if creds.is_authenticated else 'No'}\n")
    return 0


# --------------------------------------------------------------------------- setup huly

def normalize_url(raw: str) -> str:
    """'huly.cty.com/' -> 'https://huly.cty.com'."""
    url = (raw or "").strip().strip("'\"")
    if not url:
        return ""
    if "://" not in url:
        url = f"https://{url}"
    return url.rstrip("/")


def ping_huly_url(url: str, timeout: float = 10.0) -> tuple[bool, str]:
    """Step 1 check: is there a server at `url`, and does it look like Huly?

    Returns (reachable, human-readable detail). Huly front-ends serve /config.json,
    so a 200 JSON there is a strong signal; any other HTTP answer < 500 means the
    host exists but may not be Huly (accepted, with a warning).
    """
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as http:
            try:
                cfg = http.get(f"{url}/config.json")
                if cfg.status_code == 200:
                    data = cfg.json()
                    if isinstance(data, dict) and any(k in data for k in ("ACCOUNTS_URL", "COLLABORATOR_URL", "UPLOAD_URL")):
                        return True, "Huly server detected (config.json OK)"
            except (ValueError, httpx.HTTPError):
                pass
            res = http.get(url)
            if res.status_code < 500:
                return True, f"Host reachable (HTTP {res.status_code}), but /config.json does not look like Huly"
            return False, f"Server error HTTP {res.status_code}"
    except httpx.HTTPError as exc:
        return False, f"{type(exc).__name__}: {exc}"


class _Out:
    """Human output on stderr when --json is set, so stdout carries exactly one JSON object."""

    def __init__(self, as_json: bool):
        self.as_json = as_json

    def say(self, msg: str = "") -> None:
        print(msg, file=sys.stderr if self.as_json else sys.stdout)

    def result(self, code: int, status: str, **fields: Any) -> int:
        if self.as_json:
            print(json.dumps({"status": status, "exit_code": code, **fields}, ensure_ascii=False, indent=2))
        return code


def _env_state(creds: HulyCredentials, raw_url_set: bool) -> dict[str, bool]:
    return {
        "HULY_WORKSPACE_URL": raw_url_set,
        "HULY_EMAIL": bool(creds.email),
        "HULY_PASSWORD": bool(creds.password),
        "HULY_SESSION_TOKEN": bool(creds.session_token),
        "HULY_WORKSPACE_ID": bool(creds.workspace_id),
    }


def _url_is_set(workspace_path: str) -> bool:
    from ..huly.auth import parse_env_file, _resolve_env_file
    return bool(parse_env_file(_resolve_env_file(workspace_path)).get("HULY_WORKSPACE_URL") or os.getenv("HULY_WORKSPACE_URL"))


def _gitignore_warning(workspace_path: str) -> Optional[str]:
    root = Path(workspace_path)
    gi = root / ".gitignore"
    if not (root / ".git").exists() and not gi.exists():
        return None
    patterns = {l.strip() for l in gi.read_text(encoding="utf-8").splitlines()} if gi.exists() else set()
    if patterns & {".env", "/.env", "*.env", ".env*", ".env.*"}:
        return None
    return f"⚠️  `.env` is not in {gi}. Add it before committing: echo '.env' >> .gitignore"


def _verify_open_task(client: HulyClient, workspace_path: str) -> tuple[Optional[dict], int]:
    try:
        tasks = asyncio.run(client.get_my_uncompleted_tasks(workspace_path=workspace_path))
    except ValueError:
        # The token does not identify the user: still prove the connection with any open task.
        tasks = asyncio.run(client.get_my_uncompleted_tasks(workspace_path=workspace_path, include_all=True))
    return (tasks[0].model_dump() if tasks else None), len(tasks)


def run_setup_huly(
    workspace_path: str,
    *,
    url: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    reset: bool = False,
    as_json: bool = False,
    interactive: Optional[bool] = None,
    input_fn: Callable[[str], str] = input,
    getpass_fn: Callable[[str], str] = getpass.getpass,
) -> int:
    """Guided Huly setup. See module docstring for the flow and exit codes."""
    out = _Out(as_json)
    if interactive is None:
        interactive = sys.stdin.isatty() and not as_json
    env_file = str(Path(workspace_path) / ".env")
    creds = load_client_credentials(workspace_path)
    url_set = _url_is_set(workspace_path)
    state = _env_state(creds, url_set)

    out.say("\n🔧 Huly setup (development .env)")
    out.say(f"   Project : {workspace_path}")
    out.say(f"   .env    : {env_file}")
    for key, present in state.items():
        out.say(f"   {'✅' if present else '❌'} {key}")
    warn = _gitignore_warning(workspace_path)
    if warn:
        out.say(warn)

    common = {"env_file": env_file}
    if warn:
        common["warning"] = warn

    # ---- 0. Already configured? -> verify only
    explicit_input = any(v is not None for v in (url, email, password))
    if all(state.values()) and not reset and not explicit_input:
        out.say("\nℹ️  Huly is already configured in .env. Verifying with your open tasks...")
        client = HulyClient(credentials=creds)
        try:
            first, count = _verify_open_task(client, workspace_path)
        except Exception as exc:  # noqa: BLE001 - surface any auth/network error
            out.say(f"❌ Verification failed: {exc}")
            out.say("   The saved session may be expired. Re-run: coder-nexus setup huly --reset")
            return out.result(EXIT_VERIFY_FAILED, "verify_failed", step="verify", message=str(exc), **common)
        _print_first_task(out, first, count)
        return out.result(EXIT_OK, "already_configured", workspace_url=creds.workspace_url, email=creds.email,
                          workspace_id=creds.workspace_id, open_task_count=count, first_task=first, **common)

    # ---- 1. URL
    out.say("\n— Step 1/2: Huly URL —")
    if url is None and url_set and not reset:
        url = creds.workspace_url
        out.say(f"   Using URL from .env: {url}")
    if url is None:
        if not interactive:
            out.say("❌ Huly URL is required. Pass --url <https://your-huly-host>.")
            return out.result(EXIT_NEEDS_INPUT, "needs_input", step="url", needs=["url"], **common)
        try:
            url = input_fn(f"   Huly URL [{DEFAULT_HULY_URL}]: ").strip() or DEFAULT_HULY_URL
        except (KeyboardInterrupt, EOFError):
            out.say("\n   Aborted.")
            return out.result(EXIT_ABORTED, "aborted", step="url", **common)
    url = normalize_url(url)
    out.say(f"   Pinging {url} ...")
    ok, detail = ping_huly_url(url)
    if not ok:
        out.say(f"❌ Cannot reach {url}: {detail}")
        out.say("   Setup stopped. Check the URL / VPN / network and try again.")
        return out.result(EXIT_URL_UNREACHABLE, "url_unreachable", step="url", workspace_url=url, message=detail, **common)
    out.say(f"   ✅ {detail}")
    url_values = {"HULY_WORKSPACE_URL": url}
    if normalize_url(creds.workspace_url) != url or reset:
        # Session/workspace belong to the previous server: drop them.
        url_values.update({"HULY_SESSION_TOKEN": "", "HULY_WORKSPACE_ID": ""})
    update_env_values(workspace_path, url_values)
    out.say("   Saved HULY_WORKSPACE_URL to .env")

    # ---- 2. Account
    out.say("\n— Step 2/2: Huly account —")
    if email is None and not reset:
        email = creds.email
    if password is None and not reset and email == creds.email:
        password = creds.password
    attempts = 0
    while True:
        attempts += 1
        if not email or not password:
            if not interactive:
                needs = [n for n, v in (("email", email), ("password", password)) if not v]
                out.say(f"❌ Missing {', '.join(needs)}. Pass --email and --password-stdin (or --password).")
                return out.result(EXIT_NEEDS_INPUT, "needs_input", step="account", needs=needs,
                                  workspace_url=url, **common)
            try:
                default = f" [{email}]" if email else ""
                email = input_fn(f"   Email / username{default}: ").strip() or email
                password = getpass_fn("   Password: ").strip()
            except (KeyboardInterrupt, EOFError):
                out.say("\n   Aborted. The URL stays saved in .env; re-run to continue.")
                return out.result(EXIT_ABORTED, "aborted", step="account", workspace_url=url, **common)
            if not email or not password:
                out.say("   Email and password are both required.")
                continue

        out.say(f"   Logging in as {email} ...")
        client = HulyClient(credentials=HulyCredentials(workspace_url=url, email=email, password=password))
        try:
            asyncio.run(client.login(workspace_url=url, email=email, password=password))
            asyncio.run(client._resolve_workspace_id())
            break
        except Exception as exc:  # noqa: BLE001
            out.say(f"   ❌ Login failed: {exc}")
            if not interactive:
                return out.result(EXIT_LOGIN_FAILED, "login_failed", step="account", workspace_url=url,
                                  email=email, attempts=attempts, message=str(exc), **common)
            out.say("   Please try again (Ctrl+C to stop).")
            password = None

    c = client.credentials
    update_env_values(workspace_path, {
        "HULY_WORKSPACE_URL": url,
        "HULY_EMAIL": email,
        "HULY_PASSWORD": password,
        "HULY_SESSION_TOKEN": c.session_token or "",
        "HULY_WORKSPACE_ID": c.workspace_id or "",
    })
    token = c.session_token or ""
    out.say("   ✅ Logged in. Saved email, password, session token and workspace ID to .env")
    out.say(f"      Workspace ID  : {c.workspace_id}")
    out.say(f"      Session token : {token[:12]}..." if len(token) > 12 else "      Session token : (short)")

    # ---- 3. Verify
    out.say("\n— Verify: reading your open tasks —")
    try:
        first, count = _verify_open_task(client, workspace_path)
    except Exception as exc:  # noqa: BLE001
        out.say(f"❌ Logged in, but reading tasks failed: {exc}")
        return out.result(EXIT_VERIFY_FAILED, "verify_failed", step="verify", workspace_url=url, email=email,
                          workspace_id=c.workspace_id, message=str(exc), **common)
    _print_first_task(out, first, count)
    return out.result(EXIT_OK, "configured", workspace_url=url, email=email, workspace_id=c.workspace_id,
                      open_task_count=count, first_task=first, attempts=attempts, **common)


def _print_first_task(out: _Out, first: Optional[dict], count: int) -> None:
    if not first:
        out.say("✅ Connected. You have no open tasks right now.")
        return
    out.say(f"✅ Connected. Open tasks: {count}. First one:")
    out.say(f"   [{first['id']}] {first['title']}  ({first['status']}, {first['priority']})")


def cmd_setup_huly(args: argparse.Namespace) -> int:
    """`coder-nexus setup huly` (and `login`): guided setup, or with --check a read-only status."""
    path = str(Path(args.workspace_path).resolve()) if getattr(args, "workspace_path", None) else os.getcwd()
    if getattr(args, "check", False):
        cmd_status(argparse.Namespace(workspace_path=path))
        creds = load_client_credentials(path)
        complete = _url_is_set(path) and all((creds.email, creds.password, creds.session_token, creds.workspace_id))
        return 0 if complete else 1

    password = getattr(args, "password", None)
    if getattr(args, "password_stdin", False):
        password = sys.stdin.readline().rstrip("\r\n")
    return run_setup_huly(
        path,
        url=getattr(args, "url", None),
        email=getattr(args, "email", None),
        password=password,
        reset=getattr(args, "reset", False),
        as_json=getattr(args, "json", False),
        interactive=False if getattr(args, "password_stdin", False) else None,
    )
