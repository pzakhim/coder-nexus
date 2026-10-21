"""Read-only diagnostics for a Huly issue: dumps raw server responses (no tokens) to a JSON file.

Used to align the client with a real Huly server (field names, status/person classes,
collaborator API). Every probe is independent and records status code + a truncated body.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Optional

import httpx

from .client import HulyClient, parse_task_ref

MAX_BODY = 3000


def _trim(text: str) -> str:
    return text if len(text) <= MAX_BODY else text[:MAX_BODY] + f"... [+{len(text) - MAX_BODY} chars]"


async def run_debug(task_ref: str, workspace_path: Optional[str]) -> dict[str, Any]:
    client = HulyClient.from_workspace(workspace_path)
    ws = await client._ensure_session(workspace_path)
    base = client.credentials.workspace_url.rstrip("/")
    auth = {"Authorization": f"Bearer {client.credentials.session_token}"}
    report: dict[str, Any] = {"ref": task_ref, "workspace_url": base, "workspace_id": ws, "probes": {}}

    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as http:

        async def probe(name: str, method: str, url: str, **kw) -> Optional[httpx.Response]:
            try:
                res = await http.request(method, url, headers={**auth, **kw.pop("headers", {})}, **kw)
                report["probes"][name] = {"url": url.replace(base, ""), "params": kw.get("params"),
                                          "json": kw.get("json"), "status": res.status_code, "body": _trim(res.text)}
                return res
            except Exception as exc:  # noqa: BLE001
                report["probes"][name] = {"url": url.replace(base, ""), "error": f"{type(exc).__name__}: {exc}"}
                return None

        def find(cls: str, query: Optional[dict] = None, limit: int = 20) -> dict:
            p = {"class": cls, "options": json.dumps({"limit": limit})}
            if query is not None:
                p["query"] = json.dumps(query)
            return p

        fa = f"{base}/_transactor/api/v1/find-all/{ws}"
        cfg = await probe("config", "GET", f"{base}/config.json")
        config = cfg.json() if cfg is not None and cfg.status_code == 200 else {}
        report["config_urls"] = {k: v for k, v in config.items() if k.endswith("_URL")}

        account = client._token_account()
        report["token_has_account_claim"] = bool(account)
        if account:
            await probe("whoami_person", "GET", fa, params=find("contact:class:Person", {"personUuid": account}, 1))

        ref = parse_task_ref(task_ref)
        res = await probe("issue", "GET", fa, params=find("tracker:class:Issue", {"identifier": ref}, 5))
        issue = {}
        try:
            issue = (res.json().get("value") or [{}])[0] if res is not None else {}
        except Exception:  # noqa: BLE001
            pass
        report["issue_keys"] = sorted(issue.keys())
        if not issue:
            return report
        iid, desc, cls = issue.get("_id"), issue.get("description"), issue.get("_class", "tracker:class:Issue")

        # Status / assignee
        await probe("status_IssueStatus", "GET", fa, params=find("tracker:class:IssueStatus", {"_id": issue.get("status")}))
        await probe("status_core", "GET", fa, params=find("core:class:Status", {"_id": issue.get("status")}))
        await probe("person_Person", "GET", fa, params=find("contact:class:Person", {"_id": issue.get("assignee")}))
        await probe("person_Employee", "GET", fa, params=find("contact:mixin:Employee", {"_id": issue.get("assignee")}))

        # Children / attachments / comments
        await probe("children_attachedTo", "GET", fa, params=find("tracker:class:Issue", {"attachedTo": iid}))
        await probe("children_parents", "GET", fa, params=find("tracker:class:Issue", {"parents.parentId": iid}))
        await probe("attachments", "GET", fa, params=find("attachment:class:Attachment", {"attachedTo": iid}))
        await probe("comments", "GET", fa, params=find("chunter:class:ChatMessage", {"attachedTo": iid}))

        # Description blob (the collaborator RPC returns unrelated sample content on this server)
        refs: list[dict] = []
        if desc:
            res_d = await probe("desc_files_blob", "GET", f"{base}/files/{ws}", params={"file": desc, "workspace": ws})
            try:
                from .markup import parse_markup
                m = parse_markup(res_d.text) if res_d is not None else None
                refs = [r.__dict__ for r in (m.references if m else []) if r.object_class != "contact:class:Person"]
            except Exception:  # noqa: BLE001
                pass

        # Comment authors: createdBy is a social identity id
        try:
            cm = json.loads(report["probes"]["comments"]["body"]).get("value", [])
        except Exception:  # noqa: BLE001
            cm = []
        for i, c in enumerate(cm[:2]):
            await probe(f"comment{i}_author_SocialIdentity", "GET", fa,
                        params=find("contact:class:SocialIdentity", {"_id": c.get("createdBy")}, 1))

        # Mentioned documents (PO requirements)
        for i, r in enumerate(refs[:3]):
            res_doc = await probe(f"doc{i}_{r['object_class']}", "GET", fa, params=find(r["object_class"], {"_id": r["object_id"]}, 1))
            try:
                row = (res_doc.json().get("value") or [None])[0] if res_doc is not None else None
            except Exception:  # noqa: BLE001
                row = None
            if row:
                report[f"doc{i}_keys"] = sorted(row.keys())
                body = row.get("content") or row.get("description")
                if isinstance(body, str) and body:
                    await probe(f"doc{i}_content_blob", "GET", f"{base}/files/{ws}", params={"file": body, "workspace": ws})

    # Values that matter for mapping (non-secret)
    report["issue_fields"] = {k: issue.get(k) for k in (
        "_id", "_class", "space", "identifier", "number", "title", "status", "assignee", "priority",
        "attachedTo", "attachedToClass", "parents", "subIssues", "attachments", "comments",
        "description", "dueDate", "kind", "component", "milestone", "labels") if k in issue}
    return report


def write_debug(task_ref: str, workspace_path: Optional[str], out: Optional[str]) -> Path:
    report = asyncio.run(run_debug(task_ref, workspace_path))
    path = Path(out or f"huly-debug-{parse_task_ref(task_ref)}.json").resolve()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
