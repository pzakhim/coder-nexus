"""Full-context reads against a fake Huly that behaves like huly.imespro.ai (shapes from huly-debug dumps).

Server quirks reproduced here:
- find-all omits the queried attributes from each row (query by identifier -> no `identifier`);
- rich text (descriptions, document bodies) is served by GET /files/<ws>?file=<blob>;
- comments are chunter:class:ChatMessage with a ProseMirror JSON `message`.
"""

import asyncio
import json
from pathlib import Path

import httpx
import pytest

import coder_nexus.huly.client as mod
from coder_nexus.huly.client import HulyClient
from coder_nexus.huly.models import HulyCredentials

WS = "ws-1"
PARENT_DESC = {"type": "doc", "content": [
    {"type": "paragraph", "content": [{"type": "reference", "attrs": {"id": "doc-po", "objectclass": "document:class:Document", "label": "REQ-WMS-01: Inbound without PO"}}]},
    {"type": "paragraph", "content": [{"type": "image", "attrs": {"file-id": "blob-img", "alt": "architecture.jpg", "data-file-type": "image/jpeg"}}]},
]}
CHILD_DESC = {"type": "doc", "content": [{"type": "bulletList", "content": [
    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Show PO/Manual indicator."}]}]},
    {"type": "listItem", "content": [{"type": "paragraph", "content": [
        {"type": "text", "text": "Enter "}, {"type": "text", "text": "actual_received_qty", "marks": [{"type": "code"}]}]}]},
]}]}
PDF_URL = f"https://huly.example.com/files/{WS}/02_SCREEN_SPEC.pdf?file=blob-pdf&workspace={WS}"
COMMENT = {"type": "doc", "content": [{"type": "paragraph", "content": [
    {"type": "reference", "attrs": {"id": "p2", "objectclass": "contact:class:Person", "label": "Hung Le"}},
    {"type": "text", "text": " spec here "},
    {"type": "text", "text": PDF_URL, "marks": [{"type": "link", "attrs": {"href": PDF_URL}}]},
]}]}

ROWS = {
    "tracker:class:Issue": [
        {"_id": "i-parent", "identifier": "IMES-10", "number": 10, "title": "Inbound without PO", "status": "st-devdone",
         "assignee": "p1", "priority": 2, "attachedTo": "tracker:ids:NoParent", "parents": [], "subIssues": 2,
         "attachments": 1, "comments": 0, "description": "blob-parent", "dueDate": 1791115200000},
        {"_id": "i-c1", "identifier": "IMES-11", "number": 11, "title": "Count manual items", "status": "tracker:status:Backlog",
         "assignee": "p1", "priority": 0, "attachedTo": "i-parent", "subIssues": 0, "comments": 1, "description": "blob-child",
         "parents": [{"parentId": "i-parent", "identifier": "IMES-10", "parentTitle": "Inbound without PO"}]},
        {"_id": "i-c2", "identifier": "IMES-12", "number": 12, "title": "Link PO", "status": "st-cancel",
         "assignee": None, "priority": 3, "attachedTo": "i-parent", "subIssues": 0, "comments": 0, "description": None},
    ],
    "tracker:class:IssueStatus": [
        {"_id": "st-devdone", "name": "Dev Done", "category": "task:statusCategory:Active"},
        {"_id": "tracker:status:Backlog", "name": "Backlog", "category": "task:statusCategory:UnStarted"},
        {"_id": "st-cancel", "name": "CANCELED", "category": "task:statusCategory:Lost"},
    ],
    "contact:class:Person": [{"_id": "p1", "name": "Le Vu Tuan,Anh", "personUuid": "acc-1"},
                             {"_id": "p2", "name": "Le Quoc,Hung", "personUuid": "acc-2"}],
    "contact:class:SocialIdentity": [{"_id": "sid-1", "attachedTo": "p2"}],
    "chunter:class:ChatMessage": [{"_id": "m1", "attachedTo": "i-c1", "createdBy": "sid-1", "createdOn": 1789815700034,
                                    "attachments": 0, "message": json.dumps(COMMENT)}],
    "attachment:class:Attachment": [{"_id": "a1", "attachedTo": "i-parent", "file": "blob-img", "name": "architecture.jpg",
                                      "type": "image/jpeg", "size": 10}],
    "document:class:Document": [],  # PO document not visible to this account
}
BLOBS = {
    "blob-parent": json.dumps(PARENT_DESC).encode(),
    "blob-child": json.dumps(CHILD_DESC).encode(),
    "blob-img": b"\xff\xd8jpeg",
    "blob-pdf": b"%PDF-1.4 spec",
}


def handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path.startswith(f"/files/{WS}"):
        blob = request.url.params.get("file")
        return httpx.Response(200, content=BLOBS[blob]) if blob in BLOBS else httpx.Response(404)
    if "/find-all/" in path:
        q = dict(request.url.params)
        query = json.loads(q.get("query", "{}"))
        rows = [dict(r) for r in ROWS.get(q["class"], []) if all(r.get(k) == v for k, v in query.items())]
        for r in rows:  # server quirk: queried attributes are omitted
            for k in query:
                r.pop(k, None)
        return httpx.Response(200, json={"dataType": "TotalArray", "total": -1, "value": rows})
    return httpx.Response(404)


@pytest.fixture
def client(monkeypatch):
    transport = httpx.MockTransport(handler)
    real = httpx.AsyncClient

    class _Patched(real):
        def __init__(self, *a, **kw):
            kw["transport"] = transport
            super().__init__(*a, **kw)

    monkeypatch.setattr(mod.httpx, "AsyncClient", _Patched)
    return HulyClient(credentials=HulyCredentials(workspace_url="https://huly.example.com", session_token="t", workspace_id=WS))


def test_parent_full_context(client):
    d = asyncio.run(client.get_task_detail("IMES-10"))
    assert d.id == "IMES-10"
    assert d.status == "Dev Done" and d.status_category == "ACTIVE" and not d.is_closed
    assert d.assignee_name == "Anh Le Vu Tuan" and d.priority == "HIGH" and d.due_date
    assert "[REQ-WMS-01: Inbound without PO]" in d.description and "[image: architecture.jpg]" in d.description
    assert [c.id for c in d.sub_issues] == ["IMES-11", "IMES-12"]
    c1, c2 = d.sub_issues
    assert c1.status == "Backlog" and c1.status_category == "BACKLOG" and not c1.is_closed
    assert c2.is_closed and c2.status_category == "LOST" and c2.priority == "MEDIUM"
    kinds = {(s.kind, s.status) for s in d.sources}
    assert ("document", "UNREACHABLE") in kinds
    assert ("image", "AVAILABLE") in kinds
    assert len([s for s in d.sources if s.kind in ("image", "attachment")]) == 1  # same blob deduped


def test_child_comments_and_pdf_link_download(client, tmp_path):
    d = asyncio.run(client.get_task_detail("https://huly.example.com/workbench/w/tracker/imes-11", download_dir=str(tmp_path)))
    assert d.parent and d.parent.id == "IMES-10" and d.parent.status == "Dev Done"
    assert "- Show PO/Manual indicator." in d.description and "`actual_received_qty`" in d.description
    assert d.acceptance_criteria == [] and d.acceptance_criteria_source == "none"
    assert len(d.comments) == 1
    c = d.comments[0]
    assert c.author == "Hung Le Quoc" and c.created_at.startswith("2026-") and "@Hung Le" in c.text
    pdf = next(s for s in d.sources if s.kind == "file")
    assert pdf.title == "02_SCREEN_SPEC.pdf" and pdf.status == "DOWNLOADED"
    assert Path(pdf.local_path).read_bytes().startswith(b"%PDF")
    assert pdf.origin.startswith("comment ") and "Hung Le Quoc" in pdf.origin


def _jwt(claims: dict) -> str:
    import base64
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'HS256'})}.{enc(claims)}.sig"


def test_open_tasks_whole_workspace_use_status_category(client):
    tasks = asyncio.run(client.get_my_uncompleted_tasks(include_all=True))
    assert {t.id for t in tasks} == {"IMES-10", "IMES-11"}  # IMES-12 is in the LOST category
    assert {t.status for t in tasks} == {"Dev Done", "Backlog"}


def test_my_tasks_only_returns_the_logged_in_users_issues(client):
    ROWS["tracker:class:Issue"].append({"_id": "i-other", "identifier": "IMES-13", "number": 13, "title": "Someone else",
                                        "status": "tracker:status:Backlog", "assignee": "p2", "subIssues": 0})
    try:
        client.credentials.session_token = _jwt({"account": "acc-1", "workspace": WS})
        tasks = asyncio.run(client.get_my_uncompleted_tasks())
        assert {t.id for t in tasks} == {"IMES-10", "IMES-11"}
        assert all(t.assignee == "p1" for t in tasks)
    finally:
        ROWS["tracker:class:Issue"].pop()


def test_my_tasks_fails_clearly_without_account_claim(client):
    with pytest.raises(ValueError, match="Cannot tell who is logged in"):
        asyncio.run(client.get_my_uncompleted_tasks())


def test_sources_folder_is_git_ignored(tmp_path):
    from coder_nexus.server import default_sources_dir, ensure_sources_ignored
    d = default_sources_dir(str(tmp_path), "imes-1190")
    assert d == tmp_path / ".superpowers" / "sources" / "IMES-1190"
    ensure_sources_ignored(d)
    marker = tmp_path / ".superpowers" / "sources" / ".gitignore"
    assert marker.read_text().splitlines()[-1] == "*"
    assert not (tmp_path / ".gitignore").exists()  # project .gitignore untouched


def test_mention_followed_by_text_keeps_a_space():
    from coder_nexus.huly.markup import parse_markup
    doc = {"type": "doc", "content": [{"type": "paragraph", "content": [
        {"type": "reference", "attrs": {"id": "p", "objectclass": "contact:class:Person", "label": "Hưng Lê Quốc"}},
        {"type": "text", "text": "à đây "},
        {"type": "reference", "attrs": {"id": "q", "objectclass": "contact:class:Person", "label": "Van Ty"}},
        {"type": "text", "text": "xem nhé"},
        {"type": "text", "text": ", ok"},
    ]}]}
    assert parse_markup(doc).text == "@Hưng Lê Quốc à đây @Van Ty xem nhé, ok"
