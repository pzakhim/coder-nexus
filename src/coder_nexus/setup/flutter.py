"""`coder-nexus setup flutter`: iMESPro Flutter project setup gate.

Requires the company external libraries to sit next to the Client project:

    Codebase/
    ├── <client_project>/  (Client, cwd)
    ├── app-core/          (package app_core, required)
    ├── app-util/          (package app_util)
    └── app-ui-kit/        (package app_ui_kit)

The CLI never accepts or stores git credentials; auth is delegated to SSH keys
or the OS git credential helper.
"""

from __future__ import annotations

import difflib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .tools import STATE_FILE, confirm, non_interactive_env, run_tools

CORE_GIT_ENV = "CODER_NEXUS_CORE_GIT"


def _core_urls(folder: str) -> tuple[str, str]:
    """SSH/HTTPS clone URLs from $CODER_NEXUS_CORE_GIT (e.g. ssh://git@git.example.com/group); empty when unset."""
    base = os.environ.get(CORE_GIT_ENV, "").strip().rstrip("/")
    if not base:
        return "", ""
    host_path = re.sub(r"^(ssh://|https?://)", "", base)
    if host_path.startswith("git@"):
        host_path = host_path[4:]
        if not base.startswith("ssh://"):
            host_path = host_path.replace(":", "/", 1)  # scp-style git@host:group
    return f"ssh://git@{host_path}/{folder}.git", f"https://{host_path}/{folder}.git"


# package name -> (sibling folder, ssh url, https url); company Git host comes from $CODER_NEXUS_CORE_GIT
REPOS: dict[str, tuple[str, str, str]] = {
    name: (folder, *_core_urls(folder))
    for name, folder in (("app_core", "app-core"), ("app_util", "app-util"), ("app_ui_kit", "app-ui-kit"))
}
REQUIRED = "app_core"
ORG = "com.imespro"
PLATFORMS = "android,ios"
LIB_DIRS = ("app", "config", "commons", "di", "router", "constants", "modules")

PROFILES: tuple[str, ...] = ("imespro", "external-structured", "external-standard")
PROFILE_MAP: dict[str, str] = {
    "1": "imespro",
    "imespro": "imespro",
    "2": "external-structured",
    "external-structured": "external-structured",
    "3": "external-standard",
    "external-standard": "external-standard",
}


def normalize_profile(choice: str | None) -> str | None:
    if not choice:
        return None
    val = choice.strip().lower()
    return PROFILE_MAP.get(val)


def prompt_profile(ask: Callable[[str], str], default: str = "imespro") -> str:
    print("      Please select the architecture profile for this project:")
    print("        1. imespro             (Internal company core: app_core, app_util, app_ui_kit)")
    print("        2. external-structured (Client project with existing core/shared foundation)")
    print("        3. external-standard   (Vanilla Flutter project / Minimalist Clean Architecture)")
    try:
        user_input = ask("      Enter choice [1-3 or profile name, default: 1]: ").strip()
    except EOFError:
        return default
    resolved = normalize_profile(user_input)
    return resolved or default


GUIDES = {
    "publickey": (
        "SSH public key is not authorized for {url}:\n"
        "  1. Generate key: ssh-keygen -t ed25519 -C \"<your work email>\"\n"
        "  2. Add ~/.ssh/id_ed25519.pub to your Git host -> User Settings -> SSH Keys\n"
        "  3. Verify: git ls-remote {url}\n"
        "  Or use HTTPS: coder-nexus setup flutter --protocol https"
    ),
    "host_key": "Host key verification failed. Connect once over SSH to the host in {url} and confirm its fingerprint.",
    "auth": (
        "HTTPS requires credentials:\n"
        "  1. Log in to your Git host -> User Settings -> Access Tokens\n"
        "  2. Create Personal Access Token with 'read_repository' scope\n"
        "  3. Configure helper: git config --global credential.helper osxkeychain   (macOS)\n"
        "  4. Test clone once: git clone {url}  (username + token as password)\n"
        "  Then retry: coder-nexus setup flutter --protocol https"
    ),
    "network": "Cannot connect to {url}. Please check company network or VPN.",
    "unknown": "git returned an unknown error, see stderr above.",
}


DART_RESERVED_WORDS = {
    "assert", "async", "await", "break", "case", "catch", "class", "const",
    "continue", "covariant", "default", "deferred", "do", "dynamic", "else",
    "enum", "export", "extends", "extension", "external", "factory", "false",
    "final", "finally", "for", "function", "get", "hide", "if", "implements",
    "import", "in", "interface", "is", "late", "library", "mixin", "native",
    "new", "null", "of", "on", "operator", "part", "patch", "required",
    "rethrow", "return", "set", "show", "static", "super", "switch", "sync",
    "this", "throw", "true", "try", "typedef", "var", "void", "while", "with",
    "yield",
}


def dart_package_name(name: str) -> str:
    """Sanitize any folder/project name into a valid Dart package identifier.

    Dart package name rules:
    - Lowercase words separated by underscores: [a-z0-9_]
    - Must be a valid Dart identifier (not start with a digit, not reserved word)
    """
    clean = re.sub(r"[^a-zA-Z0-9_]", "_", name).lower()
    clean = re.sub(r"_+", "_", clean).strip("_")
    if not clean or clean[0].isdigit() or clean in DART_RESERVED_WORDS:
        clean = f"app_{clean}" if clean else "app"
    return clean


def package_name(folder: Path) -> str | None:
    try:
        text = (folder / "pubspec.yaml").read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(r"^name:\s*['\"]?([A-Za-z0-9_]+)", text, re.MULTILINE)
    return match.group(1) if match else None


def scan_siblings(project: Path) -> dict[str, Path]:
    """Find company packages next to the project by pubspec `name:`, not folder name.

    Searches strictly within project.parent (sibling directories).
    """
    found: dict[str, Path] = {}
    try:
        entries = sorted(project.parent.iterdir())
    except OSError:
        return found
    for folder in entries:
        if folder.is_dir() and folder.resolve() != project.resolve():
            name = package_name(folder)
            if name in REPOS and name not in found:
                found[name] = folder
    return found


def classify_git_error(stderr: str) -> str:
    text = stderr.lower()
    if "permission denied (publickey" in text or "correct access rights" in text:
        return "publickey"
    if "host key verification failed" in text:
        return "host_key"
    if "could not read username" in text or "authentication failed" in text or re.search(r"\b40[13]\b", text):
        return "auth"
    if "could not resolve host" in text or "timed out" in text or "connection refused" in text:
        return "network"
    return "unknown"


def _git(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", *args], cwd=cwd, env=non_interactive_env(), capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 1, "", "timed out")


def revision(folder: Path) -> str:
    result = _git(["rev-parse", "--short", "HEAD"], cwd=folder)
    return result.stdout.strip() if result.returncode == 0 else "UNKNOWN"


def clone(name: str, project: Path, protocol: str) -> bool:
    folder, ssh_url, https_url = REPOS[name]
    url = ssh_url if protocol == "ssh" else https_url
    if not url:
        print(f"      {CORE_GIT_ENV} is not set; cannot clone {name}.")
        print(f"      Set it to your company Git group, e.g. export {CORE_GIT_ENV}=ssh://git@git.example.com/group")
        return False
    dest = project.parent / folder
    print(f"      git ls-remote {url}")
    result = _git(["ls-remote", url, "HEAD"])
    if result.returncode == 0:
        print(f"      git clone {url} {dest}")
        result = _git(["clone", url, str(dest)])
    if result.returncode != 0:
        print(result.stderr.strip())
        guide = GUIDES[classify_git_error(result.stderr)]
        print(guide.format(url=url))
        return False
    return True


def resolved_packages(project: Path) -> dict[str, Path]:
    """Package roots as actually resolved by pub (.dart_tool/package_config.json)."""
    config = project / ".dart_tool" / "package_config.json"
    try:
        data = json.loads(config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    roots: dict[str, Path] = {}
    for pkg in data.get("packages", []):
        if pkg.get("name") not in REPOS:
            continue
        uri = pkg.get("rootUri", "")
        root = Path(uri.removeprefix("file://")) if uri.startswith("file://") else config.parent / uri
        roots[pkg["name"]] = root.resolve()
    return roots


def check(project: Path, profile: str | None = None) -> tuple[str, list[str]]:
    """Read-only gate. Returns (status, report lines). Writes nothing."""
    lines: list[str] = []
    if not (project / "pubspec.yaml").is_file():
        return "BLOCKED", ["pubspec.yaml ...... MISSING (run: coder-nexus setup flutter)"]

    active_profile = profile
    state_file = project / STATE_FILE
    state_data: dict = {}
    if state_file.is_file():
        try:
            state_data = json.loads(state_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    active_profile = active_profile or state_data.get("profile") or "imespro"
    setup_recorded = state_data.get("stack") == "flutter"  # `setup tools` alone writes only the "tools" key

    lines.append(f"profile: {active_profile}")
    status = "READY"

    if active_profile == "imespro":
        siblings = scan_siblings(project)
        resolved = resolved_packages(project)
        for name in REPOS:
            sibling = siblings.get(name)
            if not sibling:
                lines.append(f"{name:<11} sibling MISSING")
                if name == REQUIRED:
                    status = "BLOCKED"
                continue
            if resolved.get(name) != sibling.resolve():
                lines.append(f"{name:<11} {sibling.name} rev {revision(sibling)} | pub NOT RESOLVED to sibling")
                status = "BLOCKED"
            else:
                lines.append(f"{name:<11} {sibling.name} rev {revision(sibling)} | pub PASS")
    elif active_profile == "external-structured":
        foundations = [d for d in ("core", "shared", "common") if (project / "lib" / d).is_dir()]
        if foundations:
            lines.append(f"client foundations: {', '.join('lib/' + f for f in foundations)} | PASS")
        else:
            lines.append("client foundations: no lib/core, lib/shared, or lib/common found yet | OK")
    else:  # external-standard
        lines.append("standard flutter structure | PASS")

    if status == "READY" and not setup_recorded:
        lines.append(f"{STATE_FILE} MISSING")
        status = "BLOCKED"

    return status, lines


def flutter(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    print(f"      flutter {' '.join(args)}")
    return subprocess.run(
        ["flutter", *args], cwd=cwd, env=non_interactive_env(), stdin=subprocess.DEVNULL, capture_output=True, text=True
    )


def create_project(project: Path, project_name: str | None = None) -> bool:
    pkg_name = dart_package_name(project_name or project.name)
    result = flutter(
        ["create", "--org", ORG, "--platforms", PLATFORMS, "--project-name", pkg_name, str(project)],
        cwd=project.parent,
    )
    if result.returncode != 0:
        print(result.stdout[-2000:], result.stderr[-2000:])
        return False
    for sub in LIB_DIRS:
        (project / "lib" / sub).mkdir(parents=True, exist_ok=True)
        (project / "lib" / sub / ".gitkeep").touch()
    return True


def run_setup(
    project: Path,
    protocol: str = "ssh",
    check_only: bool = False,
    assume_yes: bool = False,
    ask: Callable[[str], str] = input,
    project_name: str | None = None,
    profile: str | None = None,
) -> int:
    project = project.resolve()
    if check_only:
        status, lines = check(project, profile=profile)
        print("\n".join(lines))
        if (project / "pubspec.yaml").is_file():
            print("Developer tools (informational; STATUS below is the setup gate only)")
            if run_tools(project, "flutter", check_only=True) != 0:
                print("      Install them with: coder-nexus setup tools --pack flutter")
        print(f"STATUS: {status}")
        return 0 if status == "READY" else 1

    # [1/6] Architecture Profile Selection
    print("[1/6] Architecture profile")
    selected_profile = normalize_profile(profile)
    if not selected_profile:
        if assume_yes:
            selected_profile = "imespro"
            print(f"      Profile: {selected_profile} (default)")
        else:
            selected_profile = prompt_profile(ask)
            print(f"      -> Selected profile: {selected_profile}")
    else:
        print(f"      Profile: {selected_profile}")

    # [2/6] Flutter Project
    print(f"[2/6] Flutter project {project}")
    if not (project / "pubspec.yaml").is_file():
        pkg_name = dart_package_name(project_name or project.name)
        if not confirm(
            f"      pubspec.yaml not found. Create Flutter app '{pkg_name}' ({ORG}, {PLATFORMS})?",
            assume_yes,
            ask,
        ):
            print("BLOCKED: Flutter project missing.")
            return 1
        if not create_project(project, project_name=pkg_name):
            print("BLOCKED: flutter create failed.")
            return 1
    print("      PASS")

    # [3/6] Dependencies & Foundations
    print(f"[3/6] Dependencies & foundations ({selected_profile})")
    siblings: dict[str, Path] = {}
    if selected_profile == "imespro":
        print(f"      Checking sibling packages in {project.parent}")
        siblings = scan_siblings(project)
        for name, (folder, _, _) in REPOS.items():
            if name in siblings:
                print(f"      {name:<11} PASS ({siblings[name].name}, rev {revision(siblings[name])})")
                continue
            label = "required" if name == REQUIRED else "optional"
            print(f"      {name:<11} MISSING ({label})")
            if (project.parent / folder).exists():
                print(f"      ../{folder} already exists but is not package {name}; skipping clone.")
            elif confirm(f"      Clone {name} into ../{folder} via {protocol.upper()}?", assume_yes, ask):
                if clone(name, project, protocol):
                    siblings[name] = project.parent / folder
            if name == REQUIRED and name not in siblings:
                print(f"BLOCKED: missing required package '{REQUIRED}'. Setup cannot proceed.")
                return 1

        print("      Updating pubspec.yaml with sibling path dependencies and overrides...")
        pubspec = project / "pubspec.yaml"
        before = pubspec.read_text(encoding="utf-8")
        descriptors: list[str] = []
        for name, folder in siblings.items():
            rel = os.path.relpath(folder, project)
            descriptors += [f"{name}@{{path: {rel}}}", f"override:{name}@{{path: {rel}}}"]
        result = flutter(["pub", "add", *descriptors], cwd=project)
        after = pubspec.read_text(encoding="utf-8")
        diff = "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), "pubspec.yaml", "pubspec.yaml"))
        print(diff or "      (pubspec.yaml unchanged)")
        if result.returncode != 0:
            print(result.stdout[-3000:], result.stderr[-3000:])
            missing = [n for n in REPOS if n not in siblings]
            if missing:
                print(f"Hint: missing sibling package {', '.join(missing)}. Clone all needed packages and re-run.")
            print("BLOCKED: flutter pub add / pub get failed.")
            return 1
    elif selected_profile == "external-structured":
        print("      External structured profile: reusing client foundations without company packages.")
        foundations = [d for d in ("core", "shared", "common") if (project / "lib" / d).is_dir()]
        if foundations:
            print(f"      Detected client directories: {', '.join('lib/' + f for f in foundations)}")
        else:
            print("      No existing lib/core, lib/shared, or lib/common found yet.")
        result = flutter(["pub", "get"], cwd=project)
        if result.returncode != 0:
            print(result.stdout[-2000:], result.stderr[-2000:])
            print("BLOCKED: flutter pub get failed.")
            return 1
        print("      PASS")
    else:  # external-standard
        print("      External standard profile: standard Flutter dependencies (Ponytail minimalist).")
        result = flutter(["pub", "get"], cwd=project)
        if result.returncode != 0:
            print(result.stdout[-2000:], result.stderr[-2000:])
            print("BLOCKED: flutter pub get failed.")
            return 1
        print("      PASS")

    # [4/6] Developer tools: reported and installed on confirmation, never part of the gate
    print("[4/6] Developer tools")
    run_tools(project, "flutter", assume_yes=assume_yes, ask=ask)

    # [5/6] Record Setup State
    print("[5/6] Record setup state")
    state = {
        "status": "READY",
        "stack": "flutter",
        "profile": selected_profile,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "packages": {
            name: {"path": os.path.relpath(folder, project), "revision": revision(folder)}
            for name, folder in siblings.items()
        } if selected_profile == "imespro" else {},
    }
    state_path = project / STATE_FILE
    if state_path.is_file():
        previous = json.loads(state_path.read_text(encoding="utf-8"))
        if "tools" in previous:  # written by step [4/6]
            state["tools"] = previous["tools"]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"      {STATE_FILE}")

    # [6/6] Verification Check
    print("[6/6] Verification check (--check)")
    status, lines = check(project, profile=selected_profile)
    print("\n".join(f"      {line}" for line in lines))
    print(f"STATUS: {status}")
    return 0 if status == "READY" else 1
