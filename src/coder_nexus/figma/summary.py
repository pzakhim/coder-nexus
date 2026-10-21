"""Compact Markdown summary of one Figma node tree (only what the JSON says; nothing inferred)."""

from collections import Counter
from typing import Any, Iterator, Optional

FRAME_TYPES = {"FRAME", "SECTION", "COMPONENT", "COMPONENT_SET"}
MAX_FRAMES, MAX_TEXTS, MAX_ROWS = 80, 300, 40


def _walk(node: dict, depth: int = 0) -> Iterator[tuple[dict, int]]:
    """Visible nodes only (a hidden parent hides its children)."""
    if node.get("visible") is False:
        return
    yield node, depth
    for child in node.get("children") or []:
        yield from _walk(child, depth + 1)


def _box(node: dict) -> Optional[dict]:
    return node.get("absoluteBoundingBox") or node.get("absoluteRenderBounds")


def _size(node: dict) -> str:
    b = _box(node)
    return f"{round(b['width'])}×{round(b['height'])}" if b else "?"


def _hex(paint: dict) -> Optional[str]:
    if paint.get("type") != "SOLID" or paint.get("visible") is False or not paint.get("color"):
        return None
    c = paint["color"]
    rgb = "#" + "".join(f"{round(c.get(k, 0) * 255):02X}" for k in ("r", "g", "b"))
    alpha = c.get("a", 1) * paint.get("opacity", 1)
    return rgb if alpha >= 0.999 else f"{rgb} @{alpha:.2f}"


def _font(style: dict) -> Optional[str]:
    if not style.get("fontFamily"):
        return None
    return f"{style['fontFamily']} {style.get('fontWeight', '?')} {style.get('fontSize', '?')}px"


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|")


def render_summary(payload: dict[str, Any], node_id: str, url: str, png_name: Optional[str] = None) -> str:
    entry = payload["nodes"][node_id]
    root = entry["document"]
    components = entry.get("components") or {}
    frames, texts = [], []
    fills, fonts, instances = Counter(), Counter(), Counter()

    for node, depth in _walk(root):
        kind = node.get("type")
        if kind in FRAME_TYPES:
            frames.append((depth, node))
        if kind == "INSTANCE":
            comp = components.get(node.get("componentId") or "", {})
            name = comp.get("name") or node.get("name", "?")
            instances[name if name == node.get("name") else f"{name} (layer: {node.get('name')})"] += 1
        for paint in node.get("fills") or []:
            color = _hex(paint)
            if color:
                fills[color] += 1
        if kind == "TEXT":
            font = _font(node.get("style") or {})
            if font:
                fonts[font] += 1
            chars = (node.get("characters") or "").strip()
            if chars:
                b = _box(node) or {"x": 0, "y": 0}
                color = next((h for h in map(_hex, node.get("fills") or []) if h), None)
                texts.append((round(b["y"]), round(b["x"]), chars, font, color))

    texts.sort(key=lambda t: (t[0], t[1]))
    lines = [
        f"# Figma frame: {root.get('name', node_id)}",
        "",
        f"> Source: {url}",
        f"> File: {payload.get('name', '?')} · node `{node_id}` · {root.get('type', '?')} {_size(root)}"
        + (f" · last modified {payload['lastModified']}" if payload.get("lastModified") else ""),
        "> Extracted read-only from the Figma REST API. Values are as stored in Figma; nothing is inferred.",
    ]
    if png_name:
        lines += ["", f"![{root.get('name', node_id)}]({png_name})"]

    lines += ["", f"## Frames ({len(frames)})", ""]
    lines += [f"{'  ' * d}- {n.get('name', '?')} — {n.get('type')} {_size(n)}" for d, n in frames[:MAX_FRAMES]]
    if len(frames) > MAX_FRAMES:
        lines.append(f"- … {len(frames) - MAX_FRAMES} more")

    lines += ["", f"## Visible text, reading order ({len(texts)})", ""]
    for _, _, chars, font, color in texts[:MAX_TEXTS]:
        meta = ", ".join(x for x in (font, color) if x)
        lines.append(f"- {' / '.join(chars.splitlines())}" + (f"  _({meta})_" if meta else ""))
    if len(texts) > MAX_TEXTS:
        lines.append(f"- … {len(texts) - MAX_TEXTS} more")

    def table(title: str, head: str, counter: Counter) -> None:
        lines.extend(["", f"## {title} ({len(counter)})", ""])
        if not counter:
            lines.append("(none)")
            return
        lines.extend([f"| {head} | Uses |", "|---|---|"])
        lines.extend(f"| {_cell(k)} | {v} |" for k, v in counter.most_common(MAX_ROWS))

    table("Fill colors", "Color", fills)
    table("Fonts", "Family weight size", fonts)
    table("Component instances", "Component", instances)
    return "\n".join(lines) + "\n"
