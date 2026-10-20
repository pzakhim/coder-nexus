"""Parse Huly rich text (ProseMirror JSON) into text plus the sources it points to.

Huly descriptions and comments are ProseMirror documents. Besides text they carry:
- `reference` nodes: mentions of people (`contact:class:Person`) or objects such as PO
  documents (`document:class:Document`) or other issues;
- `image` nodes: pasted images, stored as blobs (`file-id`);
- `link` marks: URLs, often to files on the same Huly host (`/files/<ws>/<name>?file=<blobId>`).
"""

import json
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class MarkupRef:
    object_id: str
    object_class: str
    label: str


@dataclass
class MarkupImage:
    blob_id: str
    name: str
    mime: Optional[str] = None


@dataclass
class MarkupLink:
    href: str
    text: str


@dataclass
class Markup:
    text: str = ""
    references: list[MarkupRef] = field(default_factory=list)
    images: list[MarkupImage] = field(default_factory=list)
    links: list[MarkupLink] = field(default_factory=list)


def _inline(nodes: list[dict], out: Markup) -> str:
    parts: list[str] = []
    after_ref = False
    for n in nodes or []:
        t = n.get("type")
        if t == "text":
            text = n.get("text", "")
            if after_ref and text and text[0].isalnum():
                text = " " + text  # Huly stores "@Name" + "next words" without a space
            for mark in n.get("marks") or []:
                if mark.get("type") == "link":
                    href = (mark.get("attrs") or {}).get("href", "")
                    if href:
                        out.links.append(MarkupLink(href=href, text=text))
                        if text != href:
                            text = f"{text} ({href})"
                elif mark.get("type") == "code":
                    text = f"`{text}`"
            parts.append(text)
            after_ref = False
        elif t == "reference":
            a = n.get("attrs") or {}
            ref = MarkupRef(object_id=str(a.get("id", "")), object_class=str(a.get("objectclass", "")), label=str(a.get("label", "")))
            out.references.append(ref)
            if after_ref:
                parts.append(" ")
            parts.append(f"@{ref.label}" if ref.object_class == "contact:class:Person" else f"[{ref.label}]")
            after_ref = True
            continue
        elif t == "image":
            _image(n, out)
            a = n.get("attrs") or {}
            parts.append(f"[image: {a.get('alt') or a.get('title') or a.get('file-id')}]")
        elif t == "hardBreak":
            parts.append("\n")
        elif n.get("content"):
            parts.append(_inline(n["content"], out))
    return "".join(parts)


def _image(n: dict, out: Markup) -> None:
    a = n.get("attrs") or {}
    blob = a.get("file-id") or blob_id_from_url(a.get("src", "") or "")
    if blob:
        out.images.append(MarkupImage(blob_id=blob, name=a.get("alt") or a.get("title") or blob, mime=a.get("data-file-type")))


def _blocks(nodes: list[dict], out: Markup, lines: list[str], indent: str = "") -> None:
    for n in nodes or []:
        t = n.get("type")
        if t in ("bulletList", "orderedList", "taskList", "todoList"):
            for i, item in enumerate(n.get("content") or [], 1):
                if t == "orderedList":
                    prefix = f"{i}. "
                elif t in ("taskList", "todoList") or item.get("type") in ("taskItem", "todoItem"):
                    prefix = f"- [{'x' if (item.get('attrs') or {}).get('checked') else ' '}] "
                else:
                    prefix = "- "
                sub: list[str] = []
                _blocks(item.get("content") or [], out, sub, indent + "  ")
                if sub:
                    lines.append(f"{indent}{prefix}{sub[0].strip()}")
                    lines.extend(sub[1:])
        elif t == "heading":
            level = int((n.get("attrs") or {}).get("level", 2))
            lines.append(f"{indent}{'#' * level} {_inline(n.get('content') or [], out)}")
        elif t in ("paragraph",):
            text = _inline(n.get("content") or [], out)
            if text.strip():
                lines.append(f"{indent}{text}")
        elif t == "image":
            _image(n, out)
            a = n.get("attrs") or {}
            lines.append(f"{indent}[image: {a.get('alt') or a.get('title') or a.get('file-id')}]")
        elif t in ("taskItem", "todoItem"):
            checked = (n.get("attrs") or {}).get("checked")
            sub: list[str] = []
            _blocks(n.get("content") or [], out, sub, indent)
            lines.append(f"{indent}- [{'x' if checked else ' '}] {' '.join(s.strip() for s in sub)}")
        elif t == "codeBlock":
            lines.append(f"{indent}```\n{_inline(n.get('content') or [], out)}\n```")
        elif t == "table":
            for row in n.get("content") or []:
                cells = []
                for cell in row.get("content") or []:
                    sub: list[str] = []
                    _blocks(cell.get("content") or [], out, sub)
                    cells.append(" ".join(s.strip() for s in sub))
                lines.append(f"{indent}| " + " | ".join(cells) + " |")
        elif n.get("content"):
            _blocks(n["content"], out, lines, indent)
        elif t == "text":
            lines.append(f"{indent}{_inline([n], out)}")


def parse_markup(raw: Any) -> Markup:
    """Accepts a ProseMirror dict or its JSON string; anything else is returned as plain text."""
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return Markup(text=raw)
    if not isinstance(raw, dict):
        return Markup(text=str(raw or ""))
    out = Markup()
    lines: list[str] = []
    _blocks(raw.get("content") or [], out, lines)
    out.text = "\n".join(lines).strip()
    return out


def blob_id_from_url(url: str) -> Optional[str]:
    """Huly file URL (`/files/<ws>/<name>?file=<blobId>&workspace=<ws>`) -> blobId."""
    try:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    except ValueError:
        return None
    return (q.get("file") or [None])[0]


def file_name_from_url(url: str) -> str:
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    segs = [s for s in path.split("/") if s]
    # /files/<ws>/<name>  -> name ; /files/<ws> -> fall back to blob id
    if len(segs) >= 3 and segs[0] == "files":
        return segs[-1]
    return blob_id_from_url(url) or "file"
