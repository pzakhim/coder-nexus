"""Real HTTP and RPC client for Huly (ReadOnly: Query Tasks & Criteria)."""

import asyncio
import base64
import html
from html.parser import HTMLParser
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
import re
import urllib.parse
from typing import Any, Callable, Optional
import httpx

from .markup import Markup, blob_id_from_url, file_name_from_url, parse_markup
from .models import (
    HulyComment,
    HulyCredentials,
    HulyIssueRef,
    HulySource,
    HulySubIssue,
    HulyTaskDetail,
    HulyTaskSummary,
)
from .auth import load_client_credentials, save_client_credentials

logger = logging.getLogger(__name__)


def _extract_text_from_tiptap(node: Any) -> list[str]:
    """Recursively extract plain text paragraphs/items from TipTap/ProseMirror JSON doc."""
    lines: list[str] = []
    if isinstance(node, dict):
        node_type = node.get("type", "")
        if node_type == "text":
            text = node.get("text", "")
            if text:
                lines.append(text)
        elif node_type in ("doc", "bulletList", "orderedList", "taskList"):
            # Container nodes: collect lines from each block child
            for child in node.get("content", []):
                lines.extend(_extract_text_from_tiptap(child))
        elif "content" in node and isinstance(node["content"], list):
            sub_texts: list[str] = []
            for child in node["content"]:
                sub_texts.extend(_extract_text_from_tiptap(child))
            joined = " ".join(sub_texts).strip()
            if joined:
                if node_type == "taskItem":
                    checked = node.get("attrs", {}).get("checked", False)
                    lines.append(f"[{'x' if checked else ' '}] {joined}")
                elif node_type == "listItem":
                    lines.append(f"- {joined}")
                else:
                    lines.append(joined)
    elif isinstance(node, list):
        for item in node:
            lines.extend(_extract_text_from_tiptap(item))
    return lines


def _format_status(raw_status: str) -> str:
    """Normalize Huly status string (e.g. tracker:status:Backlog -> BACKLOG)."""
    if not raw_status:
        return "TODO"
    parts = raw_status.split(":")
    return parts[-1].upper()


def _format_priority(raw_priority: Any) -> str:
    """Huly IssuePriority: 0 NoPriority, 1 Urgent, 2 High, 3 Medium, 4 Low."""
    mapping = {0: "NO_PRIORITY", 1: "URGENT", 2: "HIGH", 3: "MEDIUM", 4: "LOW"}
    if isinstance(raw_priority, int):
        return mapping.get(raw_priority, "NO_PRIORITY")
    if isinstance(raw_priority, str):
        if raw_priority.isdigit():
            return mapping.get(int(raw_priority), "NO_PRIORITY")
        return raw_priority.upper()
    return "NO_PRIORITY"


NO_PARENT = "tracker:ids:NoParent"
CLOSED_STATUSES = {"DONE", "COMPLETED", "CANCELLED", "CANCELED", "CLOSED", "ARCHIVED"}
CLOSED_CATEGORIES = {"WON", "LOST"}
MAX_DOWNLOAD_BYTES = 150 * 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 120.0
DOC_TEXT_LIMIT = 20000
MAX_SUB_ISSUES = 100

_ISSUE_IDENT_RE = re.compile(r"\b([A-Za-z][A-Za-z0-9]{0,15}-\d+)\b")
_OBJECT_ID_RE = re.compile(r"^[0-9a-f]{24}$", re.IGNORECASE)


def parse_task_ref(raw: str) -> str:
    """Normalize what a user pastes into an issue reference.

    Accepts 'APP-123', 'app-123', '123', a Huly '_id', or a Huly link such as
    'https://huly.app/workbench/acme/tracker/APP-123' (query/fragment ignored).
    """
    ref = (raw or "").strip().strip("<>'\"")
    if "://" in ref or ref.startswith("/"):
        parsed = urllib.parse.urlparse(ref)
        path = urllib.parse.unquote(parsed.path)
        found = _ISSUE_IDENT_RE.findall(path)
        if found:
            return found[-1].upper()
        last = [seg for seg in path.split("/") if seg]
        if last and _OBJECT_ID_RE.match(last[-1]):
            return last[-1]
        # Some links carry the issue in the query string / fragment
        found = _ISSUE_IDENT_RE.findall(urllib.parse.unquote(parsed.query + " " + parsed.fragment))
        if found:
            return found[-1].upper()
        raise ValueError(f"Could not find an issue ID (like APP-123) in link: {raw}")
    m = _ISSUE_IDENT_RE.fullmatch(ref)
    return m.group(1).upper() if m else ref


def _person_display_name(person: dict) -> Optional[str]:
    """Huly stores Person.name as 'Last,First' -> 'First Last'."""
    name = str(person.get("name") or "").strip()
    if not name:
        return None
    if "," in name:
        last, first = name.split(",", 1)
        return f"{first.strip()} {last.strip()}".strip()
    return name


_AC_HEADING_RE = re.compile(r"^(#+\s*)?(acceptance\s+criteria|ac|ti[eê]u\s+ch[ií](\s+ch[aấ]p\s+nh[aậ]n)?)\s*:?\s*$", re.IGNORECASE)
_CHECKBOX_RE = re.compile(r"^(?:[-*+]\s*)?\[( |x|X)\]\s+(.*)$")
_NUMBERED_RE = re.compile(r"^\d+[.)]\s+(.*)$")
_BULLET_RE = re.compile(r"^[-*+•]\s+(.*)$")
# Numbered items that are not behavior: a goal / background paragraph, or a heading or label for a
# picture, link, design or file ("1. Mục tiêu: …", "1. Workflow detail", "4. MD file: tham khảo").
_NOT_AC_RE = re.compile(
    r"^(?:m[uụ]c\s*ti[eê]u|goals?|objectives?|purpose|background|context|hi[eệ]n\s*tr[aạ]ng|l[ýy]\s*do)\b\s*:"
    r"|^(?:workflow|user\s*flow|flow|links?|design|figma|mockup|md|files?|t[aà]i\s*li[eệ]u|attachments?|images?|h[iì]nh(?:\s*[aả]nh)?|"
    r"screenshots?|tham\s*kh[aả]o|references?|notes?|ghi\s*ch[uú])\b[^.!?]{0,40}$",
    re.IGNORECASE,
)


def _is_label_item(item: str) -> bool:
    """A numbered item that only names a goal, heading, link or file, not an observable behavior."""
    return bool(_NOT_AC_RE.search(item)) or (bool(re.search(r"https?://", item)) and len(item.split()) <= 8)


def extract_acceptance_criteria(description: str) -> tuple[list[str], str]:
    """Return (criteria, source). Never invents criteria from plain prose.

    source:
      'ac_section' - bullets/numbers/checkboxes under an 'Acceptance Criteria' / 'AC' / 'Tiêu chí' heading
      'checklist'  - checkbox items anywhere in the description
      'numbered'   - numbered list items anywhere in the description, minus goal paragraphs and
                     heading / link / file labels (they belong to goals or sources, not criteria)
      'none'       - nothing explicit; ask the user instead of guessing
    """
    lines = [l.strip() for l in (description or "").splitlines()]

    # 1. Explicit AC section
    section: list[str] = []
    in_section = False
    for line in lines:
        if not line:
            continue
        if _AC_HEADING_RE.match(line):
            in_section = True
            continue
        if in_section:
            item = None
            for rx in (_CHECKBOX_RE, _NUMBERED_RE, _BULLET_RE):
                m = rx.match(line)
                if m:
                    item = m.group(m.lastindex)
                    break
            if item is None:
                if section:
                    break  # first non-list line after the items ends the section
                continue  # intro text right under the heading
            section.append(item.strip())
    if section:
        return section, "ac_section"

    # 2. Checklist anywhere
    checks = [m.group(2).strip() for l in lines if (m := _CHECKBOX_RE.match(l))]
    if checks:
        return checks, "checklist"

    # 3. Numbered list anywhere, without goal paragraphs and heading / link / file labels
    numbered = [m.group(1).strip() for l in lines if (m := _NUMBERED_RE.match(l)) and not _is_label_item(m.group(1).strip())]
    if numbered:
        return numbered, "numbered"
    return [], "none"


class HulyOtpRequiredError(ValueError):
    """Raised when Keycloak/Huly requires a 2FA Authenticator OTP code and none was provided."""


class _KeycloakFormParser(HTMLParser):
    """Minimal HTML form parser for Keycloak login and OTP pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.forms: list[dict[str, Any]] = []
        self._current: Optional[dict[str, Any]] = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        t = tag.lower()
        attr_map = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if t == "form":
            self._current = {
                "id": attr_map.get("id", ""),
                "action": attr_map.get("action", ""),
                "inputs": [],
            }
            self.forms.append(self._current)
        elif t == "input" and self._current is not None:
            self._current["inputs"].append({
                "type": attr_map.get("type", "text").lower(),
                "name": attr_map.get("name", ""),
                "value": attr_map.get("value", ""),
                "checked": any(k.lower() == "checked" for k, _ in attrs),
            })

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "form":
            self._current = None


def _parse_keycloak_forms(html_text: str) -> list[dict[str, Any]]:
    parser = _KeycloakFormParser()
    parser.feed(html_text or "")
    return parser.forms


def _is_keycloak_totp_setup_page(html_text: str) -> bool:
    for form in _parse_keycloak_forms(html_text):
        if form["id"] == "kc-totp-settings-form":
            return True
        if any(inp["name"] == "totpSecret" for inp in form["inputs"]):
            return True
    return False


def _extract_keycloak_form_action(
    html_text: str, page_url: str, preferred_ids: tuple[str, ...] = ()
) -> Optional[str]:
    forms = _parse_keycloak_forms(html_text)
    if preferred_ids:
        for form in forms:
            if form["id"] in preferred_ids and form["action"]:
                return urllib.parse.urljoin(page_url, form["action"])
    for form in forms:
        if form["action"]:
            return urllib.parse.urljoin(page_url, form["action"])
    match = re.search(r'action="([^"]+)"', html_text or "")
    if match:
        return urllib.parse.urljoin(page_url, html.unescape(match.group(1)))
    return None


def _extract_keycloak_otp_form(html_text: str, page_url: str) -> Optional[tuple[str, dict[str, str], str]]:
    """Detect Keycloak's OTP verification form (`login-otp.ftl`).

    Returns (action_url, base_fields, otp_field_name) or None if the page is not an OTP prompt.
    """
    for form in _parse_keycloak_forms(html_text):
        if form["id"] == "kc-totp-settings-form" or any(inp["name"] == "totpSecret" for inp in form["inputs"]):
            continue
        otp_inputs = [
            inp["name"]
            for inp in form["inputs"]
            if inp["type"] != "hidden" and inp["name"] in ("otp", "totp")
        ]
        if form["id"] != "kc-otp-login-form" and not otp_inputs:
            continue
        if not form["action"]:
            continue
        action_url = urllib.parse.urljoin(page_url, form["action"])
        base_fields: dict[str, str] = {}
        selected_cred: Optional[str] = None
        first_cred: Optional[str] = None
        for inp in form["inputs"]:
            if inp["type"] == "hidden" and inp["name"]:
                base_fields[inp["name"]] = inp["value"]
            elif inp["type"] == "radio" and inp["name"] == "selectedCredentialId" and inp["value"]:
                if first_cred is None:
                    first_cred = inp["value"]
                if inp["checked"] and selected_cred is None:
                    selected_cred = inp["value"]
        if selected_cred or first_cred:
            base_fields["selectedCredentialId"] = selected_cred or first_cred  # type: ignore[assignment]
        otp_field = "otp" if "otp" in otp_inputs else (otp_inputs[0] if otp_inputs else "otp")
        return action_url, base_fields, otp_field
    return None


def _extract_keycloak_error(html_text: str) -> Optional[str]:
    """Extract a human-readable Keycloak error message across classic and PatternFly v5 themes."""
    patterns = (
        r'class="[^"]*\bkc-feedback-text\b[^"]*"[^>]*>(.*?)</span>',
        r'id="input-error-otp-code"[^>]*>(.*?)</(?:span|div|p)>',
        r'id="input-error"[^>]*>(.*?)</(?:span|div|p)>',
        r'class="[^"]*\bpf-v5-c-alert__title\b[^"]*"[^>]*>(.*?)</(?:span|div|h\d)>',
    )
    for pattern in patterns:
        match = re.search(pattern, html_text or "", re.IGNORECASE | re.DOTALL)
        if match:
            cleaned = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", match.group(1))).split())
            if cleaned:
                return cleaned
    return None


def _extract_token_from_url(url: str) -> Optional[str]:
    unquoted = urllib.parse.unquote(url or "")
    match = re.search(r"(?:[?&#]|^)token=([a-zA-Z0-9_\.\-]+)", unquoted)
    return match.group(1) if match else None


async def _follow_keycloak_redirects(
    http: httpx.AsyncClient, resp: httpx.Response, max_hops: int = 6
) -> tuple[Optional[str], httpx.Response]:
    """Follow Keycloak/Huly redirects until a Huly `token=` redirect is found or a non-redirect page arrives."""
    for _ in range(max_hops):
        if resp.status_code not in (301, 302, 303, 307, 308):
            break
        loc = resp.headers.get("location")
        if not loc:
            break
        token = _extract_token_from_url(loc)
        if token:
            return token, resp
        next_url = urllib.parse.urljoin(str(resp.url), loc)
        resp = await http.get(next_url)
    return _extract_token_from_url(str(resp.url)), resp


class HulyClient:
    """Read-Only client for interacting with Huly Platform Transactor API.
    
    Strictly READ-ONLY: Only queries tasks and acceptance criteria.
    Never creates, updates, or deletes tasks on Huly.
    """

    def __init__(self, credentials: Optional[HulyCredentials] = None, timeout: float = 10.0):
        self.credentials = credentials or HulyCredentials()
        self.timeout = timeout

    @classmethod
    def from_workspace(cls, workspace_path: Optional[str] = None, timeout: float = 10.0) -> "HulyClient":
        """Instantiate client automatically reading credentials from client workspace's .env."""
        creds = load_client_credentials(workspace_path)
        return cls(credentials=creds, timeout=timeout)

    async def _try_keycloak_login(
        self,
        base_url: str,
        username: str,
        password: str,
        *,
        otp: Optional[str] = None,
        otp_provider: Optional[Callable[[Optional[str]], str]] = None,
        max_otp_attempts: int = 3,
    ) -> Optional[tuple[str, Optional[str]]]:
        """Detect and authenticate via Keycloak OpenID flow for self-hosted Huly instances.

        Supports optional 2FA Authenticator (TOTP/OTP) verification when Keycloak returns
        `login-otp.ftl` after password submission.
        Returns (session_token, workspace_id) if successful, None if not Keycloak.
        """
        clean_url = base_url.rstrip("/")
        async with httpx.AsyncClient(follow_redirects=False, timeout=self.timeout) as http:
            # 1. Resolve accounts URL
            accounts_url = f"{clean_url}/_accounts"
            try:
                cfg_resp = await http.get(f"{clean_url}/config.json")
                if cfg_resp.status_code == 200:
                    accounts_url = cfg_resp.json().get("ACCOUNTS_URL", accounts_url)
            except Exception:
                pass

            # 2. Check if OpenID / Keycloak provider is active
            try:
                prov_resp = await http.get(f"{accounts_url}/providers")
                if prov_resp.status_code != 200 or "openid" not in prov_resp.text.lower():
                    return None
            except Exception:
                return None

            # 3. Hit openid initiation endpoint
            init_resp = await http.get(f"{accounts_url}/auth/openid")
            if init_resp.status_code not in (302, 303):
                return None
            kc_auth_url = init_resp.headers.get("location")
            if not kc_auth_url:
                return None
            kc_auth_url = urllib.parse.urljoin(str(init_resp.url), kc_auth_url)

            # 4. Fetch Keycloak login page
            kc_page = await http.get(kc_auth_url)
            action1 = _extract_keycloak_form_action(kc_page.text, str(kc_page.url), ("kc-form-login",))
            if not action1:
                return None

            # Detect 1-step vs 2-step Keycloak form
            if 'name="password"' in kc_page.text or "name='password'" in kc_page.text:
                post_resp = await http.post(action1, data={"username": username, "password": password})
            else:
                # 2-step flow: submit username first
                u_resp = await http.post(action1, data={"username": username})
                if u_resp.status_code != 200:
                    return None
                action2 = _extract_keycloak_form_action(u_resp.text, str(u_resp.url), ("kc-form-login",))
                if not action2:
                    return None
                post_resp = await http.post(action2, data={"password": password})

            # 5. Follow redirects toward Huly callback, or handle Keycloak 2FA OTP step
            account_token, resp = await _follow_keycloak_redirects(http, post_resp)

            if not account_token:
                if _is_keycloak_totp_setup_page(resp.text):
                    raise ValueError(
                        "Keycloak requires setting up an Authenticator app (2FA) first. "
                        "Log in once via your browser to finish 2FA setup, then retry."
                    )

                if _extract_keycloak_otp_form(resp.text, str(resp.url)) is not None:
                    pending_otp = otp
                    prev_error: Optional[str] = None
                    for _ in range(max_otp_attempts):
                        otp_form = _extract_keycloak_otp_form(resp.text, str(resp.url))
                        if otp_form is None:
                            raise ValueError(
                                f"Keycloak OTP authentication failed: {prev_error or 'OTP form is no longer available.'}"
                            )
                        otp_action, base_fields, otp_field = otp_form

                        if pending_otp is not None and pending_otp.strip():
                            code = pending_otp
                            pending_otp = None
                        elif otp_provider is not None:
                            code = otp_provider(prev_error)
                        else:
                            raise HulyOtpRequiredError(
                                "Keycloak requires a 6-digit Authenticator OTP code. "
                                "Pass --otp <6-digit-code> or run 'coder-nexus setup huly' in your terminal."
                            )

                        code = re.sub(r"\s+", "", code or "")
                        if not code:
                            if otp_provider is None:
                                raise HulyOtpRequiredError(
                                    "Keycloak requires a 6-digit Authenticator OTP code. "
                                    "Pass --otp <6-digit-code> or run 'coder-nexus setup huly' in your terminal."
                                )
                            prev_error = "Authenticator code cannot be empty."
                            continue

                        otp_resp = await http.post(otp_action, data={**base_fields, otp_field: code})
                        account_token, resp = await _follow_keycloak_redirects(http, otp_resp)
                        if account_token:
                            break

                        if _is_keycloak_totp_setup_page(resp.text):
                            raise ValueError(
                                "Keycloak requires setting up an Authenticator app (2FA) first. "
                                "Log in once via your browser to finish 2FA setup, then retry."
                            )
                        prev_error = _extract_keycloak_error(resp.text) or "Invalid authenticator code."
                        if _extract_keycloak_otp_form(resp.text, str(resp.url)) is None:
                            raise ValueError(f"Keycloak OTP authentication failed: {prev_error}")
                        if otp_provider is None:
                            raise ValueError(f"Keycloak OTP verification failed: {prev_error}")

                    if not account_token:
                        raise ValueError(
                            f"Keycloak OTP verification failed after {max_otp_attempts} attempts: "
                            f"{prev_error or 'Invalid authenticator code.'}"
                        )
                else:
                    if resp.status_code in (302, 303):
                        return None
                    err = _extract_keycloak_error(resp.text) or "Keycloak credentials rejected"
                    raise ValueError(f"Keycloak authentication failed: {err}")

            # 6. Call selectWorkspace to exchange for workspace session token and workspace ID
            workspace_id = None
            session_token = account_token
            try:
                rpc_headers = {"Authorization": f"Bearer {account_token}", "Content-Type": "application/json"}
                sel_resp = await http.post(f"{accounts_url}/", headers=rpc_headers, json={"method": "selectWorkspace", "params": {}})
                if sel_resp.status_code == 200:
                    ws_info = sel_resp.json().get("result", {})
                    session_token = ws_info.get("token") or account_token
                    workspace_id = ws_info.get("workspace")
            except Exception as e:
                logger.warning("selectWorkspace RPC error: %s", e)

            return session_token, workspace_id

    async def login(
        self,
        workspace_url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        workspace_path: Optional[str] = None,
        *,
        otp: Optional[str] = None,
        otp_provider: Optional[Callable[[Optional[str]], str]] = None,
    ) -> str:
        """Authenticate with Huly, obtain a session token, and persist to client workspace .env."""
        url = workspace_url or self.credentials.workspace_url or "https://huly.app"
        user_email = email or self.credentials.email
        user_pass = password or self.credentials.password

        if not user_email or not user_pass:
            raise ValueError("Email and password are required to login to Huly.")

        # 1. Try Keycloak / Self-hosted OpenID first if available
        kc_result = await self._try_keycloak_login(
            url, user_email, user_pass, otp=otp, otp_provider=otp_provider
        )
        if kc_result:
            token, ws_id = kc_result
            self.credentials.session_token = token
            self.credentials.workspace_url = url
            self.credentials.email = user_email
            self.credentials.password = user_pass
            self.credentials.workspace_id = ws_id
            if workspace_path:
                save_client_credentials(workspace_path, self.credentials)
            return token

        # 2. Fall back to standard Huly Cloud API login
        login_payload = {"email": user_email, "password": user_pass}
        login_url = f"{url.rstrip('/')}/api/auth/login"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(login_url, json=login_payload)
            if response.status_code == 200:
                data = response.json()
                token = data.get("token") or data.get("session_token") or data.get("access_token")
                if not token:
                    raise ValueError("No token returned by Huly auth service.")
                self.credentials.session_token = token
                self.credentials.workspace_url = url
                self.credentials.email = user_email
                self.credentials.password = user_pass
                if workspace_path:
                    save_client_credentials(workspace_path, self.credentials)
                return token
            else:
                raise RuntimeError(f"Huly login failed ({response.status_code}): {response.text}")

    async def _resolve_workspace_id(self) -> str:
        """Ensure workspace_id is present, fetching via selectWorkspace RPC if needed."""
        if self.credentials.workspace_id:
            return self.credentials.workspace_id

        accounts_url = f"{self.credentials.workspace_url.rstrip('/')}/_accounts"
        headers = {
            "Authorization": f"Bearer {self.credentials.session_token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.post(f"{accounts_url}/", headers=headers, json={"method": "selectWorkspace", "params": {}})
            if res.status_code == 200:
                ws_info = res.json().get("result", {})
                ws_id = ws_info.get("workspace")
                if ws_id:
                    self.credentials.workspace_id = ws_id
                    return ws_id
        raise RuntimeError("Could not resolve Huly workspace ID. Please re-run 'coder-nexus setup huly --reset'.")

    # ------------------------------------------------------------------ low-level reads

    async def _ensure_session(self, workspace_path: Optional[str] = None) -> str:
        """Load credentials, log in if only email/password are present, return workspace ID."""
        if workspace_path and not self.credentials.is_authenticated:
            self.credentials = load_client_credentials(workspace_path)
        if not self.credentials.session_token:
            if self.credentials.email and self.credentials.password:
                await self.login(workspace_path=workspace_path)
            else:
                raise ValueError("Not authenticated. Please run 'coder-nexus setup huly' first.")
        return await self._resolve_workspace_id()

    def _auth(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.credentials.session_token}"}

    @property
    def _base(self) -> str:
        return self.credentials.workspace_url.rstrip("/")

    async def _find_all(
        self,
        http: httpx.AsyncClient,
        workspace_id: str,
        cls: str,
        query: Optional[dict] = None,
        limit: Optional[int] = None,
    ) -> list[dict]:
        """GET /_transactor/api/v1/find-all with an optional server-side query (Huly REST API).

        The server omits the queried attributes from each returned row (e.g. a query on
        `identifier` returns rows without `identifier`), so they are put back here.
        """
        params: dict[str, str] = {"class": cls}
        if query:
            params["query"] = json.dumps(query)
        if limit:
            params["options"] = json.dumps({"limit": limit})
        res = await http.get(f"{self._base}/_transactor/api/v1/find-all/{workspace_id}", params=params,
                             headers={**self._auth(), "Content-Type": "application/json"})
        if res.status_code != 200:
            raise RuntimeError(f"Huly error querying {cls} ({res.status_code}): {res.text[:200]}")
        data = res.json()
        rows = data.get("value", []) if isinstance(data, dict) else list(data or [])
        for row in rows:
            for key, val in (query or {}).items():
                if isinstance(val, (str, int, float, bool)) and "." not in key:
                    row.setdefault(key, val)
        return rows

    async def _fetch_blob(self, http: httpx.AsyncClient, workspace_id: str, blob_id: str) -> httpx.Response:
        return await http.get(f"{self._base}/files/{workspace_id}", params={"file": blob_id, "workspace": workspace_id},
                              headers=self._auth())

    async def _fetch_markup(self, http: httpx.AsyncClient, workspace_id: str, blob_id: Any) -> Markup:
        """Rich text (description / document body) stored as a blob: GET /files/<ws>?file=<blob>.

        Note: the collaborator RPC is not used; on this server it returns unrelated sample content.
        """
        if not blob_id or not isinstance(blob_id, str):
            return Markup()
        try:
            res = await self._fetch_blob(http, workspace_id, blob_id)
            if res.status_code == 200:
                return parse_markup(res.text)
            logger.warning("Markup blob %s returned %s", blob_id, res.status_code)
        except httpx.HTTPError as exc:
            logger.warning("Markup blob %s failed: %s", blob_id, exc)
        return Markup()

    # ------------------------------------------------------------------ lookups (cached)

    async def _status_map(self, http: httpx.AsyncClient, workspace_id: str) -> dict[str, tuple[str, str]]:
        """status id -> (name, category: BACKLOG|TODO|ACTIVE|WON|LOST)."""
        if getattr(self, "_statuses", None) is None:
            self._statuses = {}
            try:
                for row in await self._find_all(http, workspace_id, "tracker:class:IssueStatus"):
                    cat = str(row.get("category") or "").split(":")[-1].upper()
                    cat = {"UNSTARTED": "BACKLOG"}.get(cat, cat)
                    if row.get("_id"):
                        self._statuses[row["_id"]] = (row.get("name") or _format_status(row["_id"]), cat)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not load issue statuses: %s", exc)
        return self._statuses

    async def _status(self, http: httpx.AsyncClient, workspace_id: str, status_id: Any) -> tuple[str, Optional[str]]:
        name, cat = (await self._status_map(http, workspace_id)).get(status_id, (None, None))
        if name is None:
            name = _format_status(str(status_id or ""))
            cat = "WON" if name.upper() in {"DONE", "COMPLETED"} else "LOST" if name.upper() in {"CANCELED", "CANCELLED"} else None
        return name, cat

    async def _resolve_person_name(self, http: httpx.AsyncClient, workspace_id: str, person_id: Any) -> Optional[str]:
        if not person_id:
            return None
        cache = self.__dict__.setdefault("_people", {})
        if person_id not in cache:
            cache[person_id] = None
            try:
                rows = await self._find_all(http, workspace_id, "contact:class:Person", {"_id": person_id}, limit=1)
                if rows:
                    cache[person_id] = _person_display_name(rows[0])
            except Exception as exc:  # noqa: BLE001 - name is a nice-to-have
                logger.warning("Could not resolve person %s: %s", person_id, exc)
        return cache[person_id]

    async def _resolve_account_name(self, http: httpx.AsyncClient, workspace_id: str, social_id: Any) -> Optional[str]:
        """`createdBy` is a social identity id; map it to the person's name when the server allows."""
        if not social_id:
            return None
        cache = self.__dict__.setdefault("_accounts", {})
        if social_id not in cache:
            cache[social_id] = None
            try:
                rows = await self._find_all(http, workspace_id, "contact:class:SocialIdentity", {"_id": social_id}, limit=1)
                if rows and rows[0].get("attachedTo"):
                    cache[social_id] = await self._resolve_person_name(http, workspace_id, rows[0]["attachedTo"])
            except Exception as exc:  # noqa: BLE001
                logger.debug("Could not resolve account %s: %s", social_id, exc)
        return cache[social_id]

    # ------------------------------------------------------------------ issues

    @staticmethod
    def _issue_matches(issue: dict, ref: str) -> bool:
        norm = ref.upper()
        ident = str(issue.get("identifier") or "").upper()
        num = str(issue.get("number") or "")
        raw_id = str(issue.get("_id") or "").upper()
        return norm in (ident, f"TASK-{num}", raw_id, num)

    async def _find_issue(self, http: httpx.AsyncClient, workspace_id: str, ref: str) -> dict:
        """Look up one issue by identifier / number / _id, filtering on the server first."""
        if ref.isdigit():
            query: dict = {"number": int(ref)}
        elif _OBJECT_ID_RE.match(ref):
            query = {"_id": ref}
        else:
            query = {"identifier": ref.upper()}

        matches: list[dict] = []
        try:
            matches = [i for i in await self._find_all(http, workspace_id, "tracker:class:Issue", query, limit=20)
                       if self._issue_matches(i, ref)]
        except RuntimeError as exc:
            logger.warning("Server-side issue filter failed, falling back to full scan: %s", exc)
        if not matches:
            matches = [i for i in await self._find_all(http, workspace_id, "tracker:class:Issue") if self._issue_matches(i, ref)]
        if not matches:
            raise ValueError(f"Task '{ref}' not found in Huly workspace '{workspace_id}'.")
        if ref.isdigit() and len(matches) > 1:
            ids = ", ".join(sorted(str(m.get("identifier")) for m in matches))
            raise ValueError(f"Number '{ref}' matches several issues ({ids}). Use the full ID, e.g. {matches[0].get('identifier')}.")
        return matches[0]

    def _token_account(self) -> Optional[str]:
        """Account UUID from the session JWT (`account` claim). Decoded locally, never logged."""
        parts = (self.credentials.session_token or "").split(".")
        if len(parts) != 3:
            return None
        try:
            payload = parts[1] + "=" * (-len(parts[1]) % 4)
            claims = json.loads(base64.urlsafe_b64decode(payload))
        except (ValueError, json.JSONDecodeError):
            return None
        account = claims.get("account") if isinstance(claims, dict) else None
        return account if isinstance(account, str) and account else None

    async def current_person(self, http: httpx.AsyncClient, workspace_id: str) -> tuple[str, Optional[str]]:
        """(person _id, display name) of the logged-in account: JWT `account` -> Person.personUuid."""
        cached = self.__dict__.get("_me")
        if cached:
            return cached
        account = self._token_account()
        if not account:
            raise ValueError("Cannot tell who is logged in (session token has no account). Re-run 'coder-nexus setup huly --reset'.")
        rows = await self._find_all(http, workspace_id, "contact:class:Person", {"personUuid": account}, limit=1)
        if not rows or not rows[0].get("_id"):
            raise ValueError("Logged-in account has no person in this Huly workspace.")
        me = (rows[0]["_id"], _person_display_name(rows[0]))
        self._me = me
        return me

    async def get_my_uncompleted_tasks(
        self, workspace_path: Optional[str] = None, include_all: bool = False
    ) -> list[HulyTaskSummary]:
        """Open issues (status category not WON/LOST) assigned to the logged-in user.

        `include_all=True` lists open issues of the whole workspace instead. Strictly READ-ONLY.
        """
        workspace_id = await self._ensure_session(workspace_path)
        async with httpx.AsyncClient(timeout=self.timeout) as http:
            if include_all:
                issues = await self._find_all(http, workspace_id, "tracker:class:Issue")
            else:
                person_id, _ = await self.current_person(http, workspace_id)
                issues = await self._find_all(http, workspace_id, "tracker:class:Issue", {"assignee": person_id})
            tasks: list[HulyTaskSummary] = []
            for issue in issues:
                name, cat = await self._status(http, workspace_id, issue.get("status"))
                if cat in CLOSED_CATEGORIES or (cat is None and name.upper() in CLOSED_STATUSES):
                    continue
                tasks.append(HulyTaskSummary(
                    id=issue.get("identifier") or f"TASK-{issue.get('number', issue.get('_id', ''))}",
                    title=issue.get("title", "Untitled Task"),
                    status=name,
                    priority=_format_priority(issue.get("priority")),
                    assignee=issue.get("assignee"),
                    due_date=_iso_date(issue.get("dueDate")),
                ))
            return tasks

    async def _resolve_parent(self, http: httpx.AsyncClient, workspace_id: str, issue: dict) -> Optional[HulyIssueRef]:
        parent_id = issue.get("attachedTo")
        if not parent_id or parent_id == NO_PARENT:
            return None
        info = (issue.get("parents") or [{}])[-1] or {}
        try:
            rows = await self._find_all(http, workspace_id, "tracker:class:Issue", {"_id": parent_id}, limit=1)
            if rows:
                name, _ = await self._status(http, workspace_id, rows[0].get("status"))
                return HulyIssueRef(id=rows[0].get("identifier") or info.get("identifier") or str(parent_id),
                                    title=rows[0].get("title", ""), status=name)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not fetch parent issue %s: %s", parent_id, exc)
        return HulyIssueRef(id=info.get("identifier") or str(parent_id), title=info.get("parentTitle", ""))

    async def _resolve_sub_issues(self, http: httpx.AsyncClient, workspace_id: str, issue: dict) -> list[HulySubIssue]:
        """Direct children (one level) with their own criteria, sorted by number."""
        if issue.get("subIssues") == 0:
            return []
        children = await self._find_all(http, workspace_id, "tracker:class:Issue",
                                         {"attachedTo": issue.get("_id")}, limit=MAX_SUB_ISSUES)
        children.sort(key=lambda c: (c.get("number") is None, c.get("number") or 0))
        sem = asyncio.Semaphore(5)

        async def build(child: dict) -> HulySubIssue:
            async with sem:
                markup = await self._fetch_markup(http, workspace_id, child.get("description"))
                name = await self._resolve_person_name(http, workspace_id, child.get("assignee"))
                status, cat = await self._status(http, workspace_id, child.get("status"))
            criteria, source = extract_acceptance_criteria(markup.text)
            return HulySubIssue(
                id=child.get("identifier") or f"TASK-{child.get('number', child.get('_id'))}",
                title=child.get("title", "Untitled Task"),
                status=status,
                status_category=cat,
                priority=_format_priority(child.get("priority")),
                assignee=child.get("assignee"),
                assignee_name=name,
                is_closed=cat in CLOSED_CATEGORIES,
                acceptance_criteria=criteria,
                acceptance_criteria_source=source,
                sub_issue_count=int(child.get("subIssues") or 0),
            )

        return list(await asyncio.gather(*(build(c) for c in children)))

    # ------------------------------------------------------------------ sources

    async def _comments(self, http: httpx.AsyncClient, workspace_id: str, issue: dict) -> list[tuple[HulyComment, Markup, dict]]:
        if not issue.get("comments"):
            return []
        rows = await self._find_all(http, workspace_id, "chunter:class:ChatMessage", {"attachedTo": issue.get("_id")}, limit=200)
        rows.sort(key=lambda r: r.get("createdOn") or 0)
        out = []
        for row in rows:
            markup = parse_markup(row.get("message", ""))
            author = await self._resolve_account_name(http, workspace_id, row.get("createdBy"))
            out.append((HulyComment(author=author, created_at=_iso_datetime(row.get("createdOn")), text=markup.text), markup, row))
        return out

    async def _document_source(self, http: httpx.AsyncClient, workspace_id: str, ref, origin: str) -> HulySource:
        """A mentioned Huly document (PO requirements). UNREACHABLE when this account cannot read it."""
        src = HulySource(kind="document", title=ref.label or ref.object_id, origin=origin, status="UNREACHABLE",
                         object_id=ref.object_id)
        try:
            rows = await self._find_all(http, workspace_id, ref.object_class or "document:class:Document", {"_id": ref.object_id}, limit=1)
        except Exception as exc:  # noqa: BLE001
            src.note = f"Query failed: {exc}"
            return src
        if not rows:
            src.note = ("This Huly account cannot see the document (no access to its teamspace, or it was deleted). "
                        "Ask the PO to share it, or attach/paste its content.")
            return src
        doc = rows[0]
        src.title = doc.get("title") or doc.get("name") or src.title
        body = doc.get("content") or doc.get("description")
        markup = await self._fetch_markup(http, workspace_id, body)
        if markup.text:
            src.status = "READ"
            src.text = markup.text[:DOC_TEXT_LIMIT] + ("\n…[truncated]" if len(markup.text) > DOC_TEXT_LIMIT else "")
        else:
            src.note = "Document found but its content could not be read."
        return src

    async def _collect_sources(self, http: httpx.AsyncClient, workspace_id: str, issue: dict, description: Markup,
                               comments: list[tuple[HulyComment, Markup, dict]]) -> list[HulySource]:
        sources: list[HulySource] = []
        seen: set[str] = set()

        def add(src: HulySource, key: str) -> None:
            if key and key not in seen:
                seen.add(key)
                sources.append(src)

        async def from_markup(markup: Markup, origin: str) -> None:
            for ref in markup.references:
                if ref.object_class and ref.object_class not in ("contact:class:Person", "tracker:class:Issue"):
                    if ref.object_id not in seen:
                        add(await self._document_source(http, workspace_id, ref, origin), ref.object_id)
            for img in markup.images:
                add(HulySource(kind="image", title=img.name, origin=origin, mime=img.mime, status="AVAILABLE", blob_id=img.blob_id), img.blob_id)
            for link in markup.links:
                href = link.href
                blob = blob_id_from_url(href) if "/files/" in href else None
                if blob and urllib.parse.urlparse(href).netloc in ("", urllib.parse.urlparse(self._base).netloc):
                    add(HulySource(kind="file", title=file_name_from_url(href), origin=origin, url=href, status="AVAILABLE", blob_id=blob), blob)
                else:
                    add(HulySource(kind="link", title=link.text or href, origin=origin, url=href, status="EXTERNAL"), href)

        await from_markup(description, "description")
        if issue.get("attachments"):
            try:
                for att in await self._find_all(http, workspace_id, "attachment:class:Attachment", {"attachedTo": issue.get("_id")}, limit=100):
                    raw_size = att.get("size")
                    size_bytes = raw_size if isinstance(raw_size, int) and raw_size > 0 else None
                    add(HulySource(kind="attachment", title=att.get("name") or att.get("file"), origin="attachments",
                                   mime=att.get("type"), status="AVAILABLE", blob_id=att.get("file"),
                                   size_bytes=size_bytes,
                                   note=f"{size_bytes} bytes" if size_bytes else None), att.get("file"))
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not list attachments: %s", exc)
        for comment, markup, row in comments:
            origin = f"comment {comment.created_at or ''} by {comment.author or 'unknown'}".strip()
            await from_markup(markup, origin)
            if row.get("attachments"):
                try:
                    for att in await self._find_all(http, workspace_id, "attachment:class:Attachment", {"attachedTo": row.get("_id")}, limit=50):
                        raw_size = att.get("size")
                        size_bytes = raw_size if isinstance(raw_size, int) and raw_size > 0 else None
                        add(HulySource(kind="attachment", title=att.get("name") or att.get("file"), origin=origin,
                                       mime=att.get("type"), status="AVAILABLE", blob_id=att.get("file"),
                                       size_bytes=size_bytes,
                                       note=f"{size_bytes} bytes" if size_bytes else None), att.get("file"))
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Could not list comment attachments: %s", exc)
        return sources

    async def _download_sources(self, http: httpx.AsyncClient, workspace_id: str, sources: list[HulySource], target: Path) -> None:
        """Save files/images/attachments and readable documents into `target` (read-only on Huly)."""
        target.mkdir(parents=True, exist_ok=True)
        used: set[str] = set()

        def safe_name(name: str) -> str:
            base = re.sub(r"[^\w.\-]+", "_", name, flags=re.UNICODE).strip("._") or "file"
            candidate, n = base, 1
            while candidate.lower() in used:
                stem, dot, ext = base.rpartition(".")
                candidate = f"{stem}-{n}.{ext}" if dot else f"{base}-{n}"
                n += 1
            used.add(candidate.lower())
            return candidate

        def is_html_source(title: str, mime: Optional[str]) -> bool:
            return Path(title).suffix.lower() in {".html", ".htm"} or "html" in (mime or "").lower()

        def manual_drop_hint(title: str, mime: Optional[str], expected_path: Path, prefix: str) -> str:
            if is_html_source(title, mime):
                sitemap_out = target / "sitemap"
                return (
                    f"{prefix} Ask the user to supply '{title}' manually or place it at '{expected_path}', "
                    f"then run: coder-nexus sitemap extract \"{expected_path}\" --out \"{sitemap_out}\""
                )
            return f"{prefix} Ask the user to supply '{title}' manually or place it at '{expected_path}'."

        for src in sources:
            if src.kind == "document" and src.status == "READ" and src.text:
                path = target / safe_name(f"{src.title}.md")
                path.write_text(f"# {src.title}\n\n> Source: Huly document ({src.origin})\n\n{src.text}\n", encoding="utf-8")
                src.local_path = str(path)
                continue
            if not src.blob_id or src.status != "AVAILABLE":
                continue
            if src.size_bytes and src.size_bytes > MAX_DOWNLOAD_BYTES:
                expected_path = target / safe_name(src.title)
                size_mb = src.size_bytes / (1024 * 1024)
                limit_mb = MAX_DOWNLOAD_BYTES / (1024 * 1024)
                src.status = "UNREACHABLE"
                src.note = manual_drop_hint(
                    src.title,
                    src.mime,
                    expected_path,
                    f"Skipped: {size_mb:.1f} MB ({src.size_bytes} bytes) exceeds the {limit_mb:.0f} MB auto-download limit.",
                )
                continue
            try:
                res = await self._fetch_blob(http, workspace_id, src.blob_id)
                if res.status_code != 200:
                    expected_path = target / safe_name(src.title)
                    src.status = "UNREACHABLE"
                    src.note = manual_drop_hint(
                        src.title, src.mime, expected_path, f"Download returned HTTP {res.status_code}."
                    )
                    continue
                if len(res.content) > MAX_DOWNLOAD_BYTES:
                    expected_path = target / safe_name(src.title)
                    size_mb = len(res.content) / (1024 * 1024)
                    limit_mb = MAX_DOWNLOAD_BYTES / (1024 * 1024)
                    src.status = "UNREACHABLE"
                    src.note = manual_drop_hint(
                        src.title,
                        src.mime or res.headers.get("content-type"),
                        expected_path,
                        f"Skipped: {size_mb:.1f} MB ({len(res.content)} bytes) exceeds the {limit_mb:.0f} MB auto-download limit.",
                    )
                    continue
                name = src.title
                if "." not in name and res.headers.get("content-type", "").startswith("image/"):
                    name += "." + res.headers["content-type"].split("/")[1].split(";")[0]
                path = target / safe_name(name)
                path.write_bytes(res.content)
                src.local_path, src.status = str(path), "DOWNLOADED"
                src.mime = src.mime or res.headers.get("content-type")
                if is_html_source(path.name, src.mime):
                    _maybe_extract_sitemap_source(path, src, target)
            except httpx.HTTPError as exc:
                expected_path = target / safe_name(src.title)
                src.status = "UNREACHABLE"
                src.note = manual_drop_hint(src.title, src.mime, expected_path, f"Download failed: {exc}.")

    # ------------------------------------------------------------------ public

    async def get_task_detail(
        self,
        task_id: str,
        workspace_path: Optional[str] = None,
        include_sub_issues: bool = True,
        download_dir: Optional[str] = None,
    ) -> HulyTaskDetail:
        """Full context for one Huly issue: description, status, people, parent, children,
        comments and every source it points to (documents, images, attachments, files, links).

        `task_id` may be 'APP-123', '123', a Huly _id or a Huly issue link. With `download_dir`,
        files and readable documents are saved there. Strictly READ-ONLY on Huly.
        """
        ref = parse_task_ref(task_id)
        workspace_id = await self._ensure_session(workspace_path)

        client_timeout = max(self.timeout, DOWNLOAD_TIMEOUT_SECONDS if download_dir else 20.0)
        async with httpx.AsyncClient(timeout=client_timeout, follow_redirects=True) as http:
            target = await self._find_issue(http, workspace_id, ref)
            description = await self._fetch_markup(http, workspace_id, target.get("description"))
            text = description.text

            figma_urls: list[str] = []
            for l in description.links:
                if "figma.com" in l.href and l.href not in figma_urls:
                    figma_urls.append(l.href)
            for m in re.finditer(r"(https://[^\s]*figma\.com[^\s\)\]]+)", text):
                if m.group(1) not in figma_urls:
                    figma_urls.append(m.group(1))
            figma_url = figma_urls[0] if figma_urls else None

            acceptance_criteria, ac_source = extract_acceptance_criteria(text)
            status, category = await self._status(http, workspace_id, target.get("status"))
            assignee_name = await self._resolve_person_name(http, workspace_id, target.get("assignee"))
            parent = await self._resolve_parent(http, workspace_id, target)
            sub_issues = await self._resolve_sub_issues(http, workspace_id, target) if include_sub_issues else []
            comments = await self._comments(http, workspace_id, target)
            sources = await self._collect_sources(http, workspace_id, target, description, comments)
            for s in sources:
                if s.url and "figma.com" in s.url and s.url not in figma_urls:
                    figma_urls.append(s.url)
            if not figma_url and figma_urls:
                figma_url = figma_urls[0]
            if download_dir:
                await self._download_sources(http, workspace_id, sources, Path(download_dir))
                for furl in figma_urls:
                    await _fetch_figma_source(sources, furl, Path(download_dir) / "figma", workspace_path)

            return HulyTaskDetail(
                id=target.get("identifier") or ref,
                title=target.get("title", "Untitled Task"),
                description=text,
                status=status,
                status_category=category,
                is_closed=category in CLOSED_CATEGORIES,
                priority=_format_priority(target.get("priority")),
                assignee=target.get("assignee"),
                assignee_name=assignee_name,
                due_date=_iso_date(target.get("dueDate")),
                acceptance_criteria=acceptance_criteria,
                acceptance_criteria_source=ac_source,
                figma_url=figma_url,
                attachments=[s.title for s in sources if s.kind == "attachment"],
                comments=[c for c, _, _ in comments],
                sources=sources,
                parent=parent,
                sub_issues=sub_issues,
            )


async def _fetch_figma_source(sources: list[HulySource], figma_url: str, target: Path, workspace_path: Optional[str]) -> None:
    """Fetch the ticket's Figma frame (read-only). READ, NOT_PROVIDED (no FIGMA_TOKEN) or UNREACHABLE; never guessed."""
    from ..figma import fetch_async, load_figma_token
    src = next((s for s in sources if s.url == figma_url), None)
    if src is None:
        src = HulySource(kind="figma", title="Figma frame", origin="description", url=figma_url, status="EXTERNAL")
        sources.append(src)
    result = await fetch_async(figma_url, target, load_figma_token(workspace_path))
    src.kind, src.status, src.note = "figma", result.status, result.note
    if result.name:
        src.title = f"Figma: {result.name}"
    if result.status == "READ":
        src.local_path = result.png_path or result.summary_path
        src.mime = "image/png" if result.png_path else "text/markdown"
        extra_imgs = [p for p in result.screen_images if p != result.png_path]
        all_paths = [p for p in (result.png_path, *extra_imgs, result.tokens_path, result.spec_path, result.json_path, result.summary_path) if p]
        saved = ", ".join(Path(p).name for p in all_paths)
        src.note = f"Saved to {target}: {saved}" + (f" ({result.note})" if result.note else "")
        text = Path(result.summary_path).read_text(encoding="utf-8")
        src.text = text[:DOC_TEXT_LIMIT] + ("\n…[truncated]" if len(text) > DOC_TEXT_LIMIT else "")


def _maybe_extract_sitemap_source(html_path: Path, src: HulySource, target: Path) -> None:
    """Auto-extract an interactive HTML sitemap attachment so agents read clean index/specs instead of raw multi-MB HTML."""
    from ..sitemap import AUTO_EXTRACT_ALL_MAX_SCREENS, extract_sitemap, inspect_sitemap, is_interactive_sitemap_html

    if not is_interactive_sitemap_html(html_path):
        return
    sitemap_dir = target / "sitemap"
    probe = inspect_sitemap(html_path)
    if probe.status != "READ":
        return
    index_only = probe.total_screens > AUTO_EXTRACT_ALL_MAX_SCREENS
    result = extract_sitemap(html_path, sitemap_dir, index_only=index_only)
    if result.status != "READ" or not result.index_md_path:
        return
    src.kind = "sitemap"
    src.status = "READ"
    src.local_path = result.index_md_path
    src.mime = "text/markdown"
    if index_only:
        src.note = (
            f"Interactive HTML sitemap ({result.total_stages} stages, {result.total_screens} screens). "
            f"Raw HTML saved at '{html_path}'; index written to '{result.index_md_path}'. "
            f"Do NOT read the raw HTML directly — unpack in-scope screens with: "
            f"coder-nexus sitemap extract \"{html_path}\" --out \"{sitemap_dir}\" --stage <STAGE_ID> | --screens <CODE1,CODE2> --include-neighbors"
        )
    else:
        src.note = (
            f"Interactive HTML sitemap ({result.total_stages} stages, {result.extracted_screens} screens extracted with PNGs & specs) "
            f"in '{sitemap_dir}' (raw HTML at '{html_path}')."
        )
    index_text = Path(result.index_md_path).read_text(encoding="utf-8")
    src.text = index_text[:DOC_TEXT_LIMIT] + ("\n…[truncated]" if len(index_text) > DOC_TEXT_LIMIT else "")


def _iso_datetime(ms: Any) -> Optional[str]:
    if not isinstance(ms, (int, float)) or ms <= 0:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat(timespec="minutes")


def _iso_date(ms: Any) -> Optional[str]:
    if not isinstance(ms, (int, float)) or ms <= 0:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date().isoformat()
