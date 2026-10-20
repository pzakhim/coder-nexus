"""Real HTTP and RPC client for Huly (ReadOnly: Query Tasks & Criteria)."""

import json
import logging
import re
import urllib.parse
from typing import Any, Optional
import httpx

from .models import HulyCredentials, HulyTaskSummary, HulyTaskDetail
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
    """Map Huly priority integer or string to readable level."""
    mapping = {0: "LOW", 1: "MEDIUM", 2: "HIGH", 3: "URGENT"}
    if isinstance(raw_priority, int):
        return mapping.get(raw_priority, "MEDIUM")
    if isinstance(raw_priority, str):
        if raw_priority.isdigit():
            return mapping.get(int(raw_priority), "MEDIUM")
        return raw_priority.upper()
    return "MEDIUM"


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

    async def _try_keycloak_login(self, base_url: str, username: str, password: str) -> Optional[tuple[str, Optional[str]]]:
        """Detect and authenticate via Keycloak OpenID flow for self-hosted Huly instances.
        
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

            # 4. Fetch Keycloak login page
            kc_page = await http.get(kc_auth_url)
            action_match = re.search(r'action="([^"]+)"', kc_page.text)
            if not action_match:
                return None
            action1 = action_match.group(1).replace("&amp;", "&")

            # Detect 1-step vs 2-step Keycloak form
            if 'name="password"' in kc_page.text:
                post_resp = await http.post(action1, data={"username": username, "password": password})
            else:
                # 2-step flow: submit username first
                u_resp = await http.post(action1, data={"username": username})
                if u_resp.status_code != 200:
                    return None
                p_match = re.search(r'action="([^"]+)"', u_resp.text)
                if not p_match:
                    return None
                action2 = p_match.group(1).replace("&amp;", "&")
                post_resp = await http.post(action2, data={"password": password})

            if post_resp.status_code not in (302, 303):
                err_match = re.search(r'class="kc-feedback-text"[^>]*>(.*?)</span>', post_resp.text)
                err = err_match.group(1).strip() if err_match else "Keycloak credentials rejected"
                raise ValueError(f"Keycloak authentication failed: {err}")

            cb_url = post_resp.headers.get("location")
            if not cb_url:
                return None

            # 5. Follow callback into Huly
            huly_cb_resp = await http.get(cb_url)
            login_auth_url = huly_cb_resp.headers.get("location", "")
            unquoted = urllib.parse.unquote(login_auth_url)
            match = re.search(r"token=([a-zA-Z0-9_\.\-]+)", unquoted)
            if not match:
                return None
            account_token = match.group(1)

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
    ) -> str:
        """Authenticate with Huly, obtain a session token, and persist to client workspace .env."""
        url = workspace_url or self.credentials.workspace_url or "https://huly.app"
        user_email = email or self.credentials.email
        user_pass = password or self.credentials.password

        if not user_email or not user_pass:
            raise ValueError("Email and password are required to login to Huly.")

        # 1. Try Keycloak / Self-hosted OpenID first if available
        kc_result = await self._try_keycloak_login(url, user_email, user_pass)
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
        raise RuntimeError("Could not resolve Huly workspace ID. Please re-run 'coder-nexus login'.")

    async def get_my_uncompleted_tasks(self, workspace_path: Optional[str] = None) -> list[HulyTaskSummary]:
        """Fetch real uncompleted tasks from Huly Transactor API.
        
        Strictly READ-ONLY: Never creates, updates, or mocks tasks.
        """
        if workspace_path and not self.credentials.is_authenticated:
            self.credentials = load_client_credentials(workspace_path)

        if not self.credentials.session_token:
            if self.credentials.email and self.credentials.password:
                await self.login(workspace_path=workspace_path)
            else:
                raise ValueError("Not authenticated. Please run 'coder-nexus login' first.")

        workspace_id = await self._resolve_workspace_id()
        base_url = self.credentials.workspace_url.rstrip("/")
        transactor_url = f"{base_url}/_transactor/api/v1/find-all/{workspace_id}?class=tracker:class:Issue"
        headers = {
            "Authorization": f"Bearer {self.credentials.session_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(transactor_url, headers=headers)
            if res.status_code != 200:
                raise RuntimeError(f"Failed to query Huly tasks ({res.status_code}): {res.text[:200]}")

            data = res.json()
            raw_issues = data.get("value", [])

            tasks: list[HulyTaskSummary] = []
            for issue in raw_issues:
                status_raw = issue.get("status", "")
                status_clean = _format_status(status_raw)
                # Filter uncompleted tasks
                if status_clean in ("DONE", "COMPLETED", "CANCELLED", "CLOSED", "ARCHIVED"):
                    continue

                task_id = issue.get("identifier") or f"TASK-{issue.get('number', issue.get('_id', ''))}"
                tasks.append(
                    HulyTaskSummary(
                        id=task_id,
                        title=issue.get("title", "Untitled Task"),
                        status=status_clean,
                        priority=_format_priority(issue.get("priority")),
                        assignee=issue.get("assignee"),
                        due_date=issue.get("dueDate"),
                    )
                )

            return tasks

    async def _fetch_markup_content(self, workspace_id: str, description_id: str) -> str:
        """Fetch rich-text document content from Huly Collaborator RPC."""
        base_url = self.credentials.workspace_url.rstrip("/")
        collab_url = f"{base_url}/_collaborator/rpc/{workspace_id}"
        headers = {
            "Authorization": f"Bearer {self.credentials.session_token}",
            "Content-Type": "application/json",
        }
        payload = {"method": "getContent", "payload": {"source": description_id}}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(collab_url, headers=headers, json=payload)
                if res.status_code == 200:
                    body = res.json()
                    content_str = body.get("content", {}).get("", "")
                    if content_str and isinstance(content_str, str):
                        try:
                            tiptap_doc = json.loads(content_str)
                            extracted = _extract_text_from_tiptap(tiptap_doc)
                            return "\n".join(extracted)
                        except json.JSONDecodeError:
                            return content_str
                    elif isinstance(content_str, dict):
                        return "\n".join(_extract_text_from_tiptap(content_str))
        except Exception as exc:
            logger.debug("Failed to fetch markup content: %s", exc)
        return ""

    async def get_task_detail(self, task_id: str, workspace_path: Optional[str] = None) -> HulyTaskDetail:
        """Fetch full details and acceptance criteria for a real task from Huly.
        
        Strictly READ-ONLY. Ném ngoại lệ Fail-Fast nếu không tìm thấy.
        """
        if workspace_path and not self.credentials.is_authenticated:
            self.credentials = load_client_credentials(workspace_path)

        if not self.credentials.session_token:
            if self.credentials.email and self.credentials.password:
                await self.login(workspace_path=workspace_path)
            else:
                raise ValueError("Not authenticated. Please run 'coder-nexus login' first.")

        workspace_id = await self._resolve_workspace_id()
        base_url = self.credentials.workspace_url.rstrip("/")
        transactor_url = f"{base_url}/_transactor/api/v1/find-all/{workspace_id}?class=tracker:class:Issue"
        headers = {
            "Authorization": f"Bearer {self.credentials.session_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(transactor_url, headers=headers)
            if res.status_code != 200:
                raise RuntimeError(f"Huly error fetching task list ({res.status_code}): {res.text[:200]}")

            data = res.json()
            raw_issues = data.get("value", [])

            target = None
            norm_id = task_id.strip().upper()
            for issue in raw_issues:
                ident = str(issue.get("identifier") or "").upper()
                num = str(issue.get("number") or "")
                raw_id = str(issue.get("_id") or "").upper()
                if norm_id in (ident, f"TASK-{num}", raw_id, num):
                    target = issue
                    break

            if not target:
                raise ValueError(f"Task '{task_id}' not found in Huly workspace '{workspace_id}'.")

            # Resolve description text
            desc_val = target.get("description", "")
            description_text = ""
            if desc_val:
                # If description is a reference ID, fetch markup
                if isinstance(desc_val, str) and "-" in desc_val and len(desc_val) > 20:
                    description_text = await self._fetch_markup_content(workspace_id, desc_val)
                if not description_text:
                    description_text = str(desc_val)

            # Extract acceptance criteria from description
            acceptance_criteria: list[str] = []
            figma_url = None
            for line in description_text.splitlines():
                stripped = line.strip()
                if "figma.com" in stripped and not figma_url:
                    fig_match = re.search(r"(https://[^\s]+figma\.com[^\s\)]+)", stripped)
                    if fig_match:
                        figma_url = fig_match.group(1)

                # Checklist or numbered bullet points
                if stripped.startswith(("- [ ]", "- [x]", "* [ ]", "* [x]")):
                    acceptance_criteria.append(stripped[5:].strip())
                elif re.match(r"^\d+\.\s+", stripped):
                    acceptance_criteria.append(re.sub(r"^\d+\.\s+", "", stripped))

            if not acceptance_criteria and description_text:
                # If no explicit checklist, use the description sentences as criteria
                acceptance_criteria = [p.strip() for p in description_text.splitlines() if p.strip()]

            return HulyTaskDetail(
                id=target.get("identifier") or f"TASK-{target.get('number', target.get('_id'))}",
                title=target.get("title", "Untitled Task"),
                description=description_text,
                status=_format_status(target.get("status", "")),
                priority=_format_priority(target.get("priority")),
                assignee=target.get("assignee"),
                acceptance_criteria=acceptance_criteria,
                figma_url=figma_url,
            )
