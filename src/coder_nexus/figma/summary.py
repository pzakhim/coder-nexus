"""Framelink-style normalized `<node>.spec.json` tree (referencing DTCG tokens by name) and Markdown summary."""

from collections import Counter
from typing import Any, Iterator, Optional

from .tokens import TokenRegistry, _bound_var_ids, paint_to_hex

FRAME_TYPES = {"FRAME", "SECTION", "COMPONENT", "COMPONENT_SET"}
SCREEN_CONTAINER_TYPES = {"SECTION", "CANVAS", "GROUP"}
SCREEN_NODE_TYPES = {"FRAME", "COMPONENT", "COMPONENT_SET"}
VECTOR_LEAF_TYPES = {"VECTOR", "BOOLEAN_OPERATION", "STAR", "LINE", "ELLIPSE", "REGULAR_POLYGON"}
MAX_FRAMES, MAX_TEXTS, MAX_ROWS = 80, 300, 40
MAX_ICONS = 30

PRIMARY_ALIGN_MAP = {
    "MIN": "flex-start",
    "CENTER": "center",
    "MAX": "flex-end",
    "SPACE_BETWEEN": "space-between",
}
COUNTER_ALIGN_MAP = {
    "MIN": "flex-start",
    "CENTER": "center",
    "MAX": "flex-end",
    "BASELINE": "baseline",
}
SIZING_MAP = {
    "FIXED": "fixed",
    "HUG": "hug",
    "FILL": "fill",
}


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


def _is_screen_sized(node: dict) -> bool:
    b = _box(node)
    if not b:
        return False
    return b.get("width", 0) >= 240 and b.get("height", 0) >= 320


def extract_screen_nodes(root: dict) -> list[dict]:
    """Identify the ordered screen frames (`S01`, `S02`...) inside `root`."""
    kind = root.get("type")
    candidates: list[dict] = []

    if kind in SCREEN_CONTAINER_TYPES:
        for child in root.get("children") or []:
            if child.get("visible") is False:
                continue
            ctype = child.get("type")
            if ctype in SCREEN_NODE_TYPES:
                candidates.append(child)
            elif ctype in SCREEN_CONTAINER_TYPES:
                for sub in child.get("children") or []:
                    if sub.get("visible") is not False and sub.get("type") in SCREEN_NODE_TYPES:
                        candidates.append(sub)
    elif kind == "FRAME":
        visible_children = [c for c in (root.get("children") or []) if c.get("visible") is not False]
        frame_children = [c for c in visible_children if c.get("type") in SCREEN_NODE_TYPES and _is_screen_sized(c)]
        non_frame_children = [c for c in visible_children if c.get("type") not in SCREEN_NODE_TYPES]
        if len(frame_children) >= 2 and not non_frame_children:
            candidates = frame_children

    if not candidates:
        return [root]

    def sort_key(n: dict) -> tuple[int, int]:
        b = _box(n) or {"x": 0, "y": 0}
        return (round(b.get("y", 0) / 100), round(b.get("x", 0)))

    candidates.sort(key=sort_key)
    return candidates


def _node_destinations(node: dict) -> list[str]:
    dests: list[str] = []
    if node.get("transitionNodeID"):
        dests.append(str(node["transitionNodeID"]))
    for entry in (node.get("interactions") or []) + (node.get("reactions") or []):
        if not isinstance(entry, dict):
            continue
        action = entry.get("action") or entry
        if isinstance(action, dict):
            dest = action.get("destinationId") or action.get("transitionNodeID")
            if dest:
                dests.append(str(dest))
        for act in entry.get("actions") or []:
            if isinstance(act, dict):
                dest = act.get("destinationId") or act.get("transitionNodeID")
                if dest:
                    dests.append(str(dest))
    return dests


def _extract_interactions(screen_node: dict) -> list[dict[str, Any]]:
    """Extract prototype navigation links (`transitionNodeID` or `interactions`/`reactions`) inside a screen."""
    items: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for node, _ in _walk(screen_node):
        nid = str(node.get("id") or "")
        nname = str(node.get("name") or "?")
        for dest in _node_destinations(node):
            if (nid, dest) not in seen:
                seen.add((nid, dest))
                items.append({
                    "trigger_node_id": nid,
                    "trigger_name": nname,
                    "destination_node_id": dest,
                })
    return items


def _is_pure_vector_group(node: dict) -> bool:
    """True when all visible descendants are vector primitives (collapse as a single ICON/VECTOR leaf)."""
    children = [c for c in (node.get("children") or []) if c.get("visible") is not False]
    if not children:
        return False
    return all(
        c.get("type") in VECTOR_LEAF_TYPES or _is_pure_vector_group(c)
        for c in children
    )


def _match_pattern_text(text: str) -> Optional[str]:
    if not text:
        return None
    if any(k in text for k in ("appbar", "app_bar", "app-bar", "topbar", "top_bar", "top-bar", "header")) or (
        "navbar" in text and "bottom" not in text
    ):
        return "appbar"
    if any(k in text for k in ("bottomnav", "bottom_nav", "bottom-nav", "navigationbar", "tabbar", "bottom bar")) or (
        "navbar" in text and "bottom" in text
    ):
        return "bottomnav"
    if any(k in text for k in ("bottomsheet", "bottom_sheet", "bottom-sheet", "actionsheet", "action_sheet")):
        return "bottomsheet"
    if any(k in text for k in ("dialog", "modal", "alert", "popup")):
        return "dialog"
    if any(k in text for k in ("datepicker", "date_picker", "date-picker", "daterange", "calendar")):
        return "datepicker"
    if "search" in text:
        return "search"
    if any(k in text for k in ("dropdown", "select", "combobox", "picker")):
        return "dropdown"
    if any(k in text for k in ("textfield", "text_field", "text-field", "formfield", "input", "password", "textarea")):
        return "formfield"
    if any(k in text for k in ("button", "btn", "cta", "fab", "iconbutton")):
        return "button"
    if any(k in text for k in ("chip", "filterchip")):
        return "chip"
    if any(k in text for k in ("badge", "statuspill", "status_pill", "pill", "tag")):
        return "badge"
    if any(k in text for k in ("nodata", "no_data", "no-data", "emptystate", "empty_state", "empty-state")):
        return "nodata"
    if any(k in text for k in ("loading", "spinner", "shimmer", "skeleton", "progress")):
        return "loading"
    if any(k in text for k in ("banner", "toast", "snackbar", "callout", "notice")):
        return "banner"
    if any(k in text for k in ("card", "tile", "panel")):
        return "card"
    if any(k in text for k in ("list", "listitem", "list_item", "list-item", "rowitem", "table")):
        return "list"
    return None


def infer_canonical_pattern(node_name: str, component_name: str = "", component_set_name: str = "") -> str:
    """Deterministically classify a Figma component/instance into a canonical AIF UI pattern name."""
    comp_text = f"{component_set_name or ''} {component_name or ''}".lower().strip()
    matched = _match_pattern_text(comp_text)
    if matched:
        return matched
    full_text = f"{comp_text} {node_name or ''}".lower().strip()
    return _match_pattern_text(full_text) or "custom"


def extract_icon_nodes(root: dict) -> list[dict[str, str]]:
    """Walk visible nodes in `root` to find icon nodes suitable for SVG export."""
    icons: list[dict[str, str]] = []
    seen_ids: set[str] = set()

    def _visit(node: dict, depth: int) -> None:
        if len(icons) >= MAX_ICONS or node.get("visible") is False:
            return
        ntype = node.get("type")
        is_candidate = (
            ntype in ("FRAME", "GROUP", "COMPONENT", "INSTANCE") and _is_pure_vector_group(node)
        ) or (ntype in VECTOR_LEAF_TYPES and depth == 1)
        if is_candidate:
            b = _box(node)
            size_ok = True
            if b is not None:
                w = b.get("width", 0) or 0
                h = b.get("height", 0) or 0
                size_ok = (0 < w <= 128) and (0 < h <= 128)
            if size_ok:
                nid = node.get("id")
                if nid is not None:
                    sid = str(nid)
                    if sid not in seen_ids:
                        seen_ids.add(sid)
                        icons.append({"id": sid, "name": str(node.get("name") or "icon")})
                return
        for child in node.get("children") or []:
            if len(icons) >= MAX_ICONS:
                break
            _visit(child, depth + 1)

    _visit(root, 0)
    return icons


def _child_signature(c: dict[str, Any]) -> Optional[tuple[Any, ...]]:
    ctype = c.get("type")
    if ctype not in ("INSTANCE", "COMPONENT", "FRAME", "GROUP"):
        return None
    if c.get("component"):
        return ("COMP", c["component"].get("id") or c["component"].get("name"))
    if ctype in ("FRAME", "GROUP") and c.get("children"):
        return (
            "CONTAINER",
            ctype,
            tuple(sub.get("type") for sub in c["children"]),
            tuple((sub.get("component") or {}).get("name") for sub in c["children"]),
        )
    return None


def _collect_normalized_texts(node: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    txt = node.get("text")
    if isinstance(txt, str) and txt.strip():
        texts.append(txt.strip())
    for child in node.get("children") or []:
        texts.extend(_collect_normalized_texts(child))
    return texts


def _deduplicate_repeating_children(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse contiguous runs of >= 3 structurally identical sibling items into a representative with `repeatCount`."""
    if len(children) < 3:
        return children

    result: list[dict[str, Any]] = []
    i = 0
    n = len(children)
    while i < n:
        sig = _child_signature(children[i])
        if sig is None:
            result.append(children[i])
            i += 1
            continue
        j = i + 1
        while j < n and _child_signature(children[j]) == sig:
            j += 1
        run = children[i:j]
        if len(run) >= 3:
            rep = dict(run[0])
            rep["repeatCount"] = len(run)
            samples: list[str] = []
            for sib in run[1:6]:
                joined = " | ".join(_collect_normalized_texts(sib))
                if joined:
                    samples.append(joined)
            if samples:
                rep["repeatedSamples"] = samples
            result.append(rep)
        else:
            result.extend(run)
        i = j
    return result


def _normalize_node_tree(
    node: dict,
    registry: TokenRegistry,
    components_map: dict[str, Any],
    component_sets_map: dict[str, Any],
    *,
    is_screen_root: bool = False,
) -> dict[str, Any]:
    """Framelink-inspired recursive node normalizer referencing DTCG tokens in `registry` by `{token.path}`."""
    kind = node.get("type", "FRAME")
    node_styles = node.get("styles") or {}
    b = _box(node)

    out: dict[str, Any] = {
        "id": node.get("id"),
        "name": node.get("name", "?"),
        "type": "ICON" if (kind in ("FRAME", "GROUP") and _is_pure_vector_group(node)) else kind,
    }
    if b:
        out["bounds"] = {
            "x": round(b.get("x", 0)),
            "y": round(b.get("y", 0)),
            "width": round(b.get("width", 0)),
            "height": round(b.get("height", 0)),
        }

    tokens_ref: dict[str, Any] = {}

    # Fills / background / text color
    role_hint = "text" if kind == "TEXT" else ("background" if is_screen_root else "fill")
    fill_style_id = node_styles.get("fill") or node_styles.get("fills")
    fill_var_ids = _bound_var_ids(node, "fills")
    for paint in node.get("fills") or []:
        hex_c = paint_to_hex(paint)
        if hex_c:
            tpath = registry.register_color(
                hex_c,
                style_id=fill_style_id,
                var_ids=fill_var_ids,
                role_hint=role_hint,
            )
            tokens_ref["textColor" if kind == "TEXT" else "fill"] = f"{{{tpath}}}"
            break

    # Strokes
    stroke_style_id = node_styles.get("stroke") or node_styles.get("strokes")
    stroke_var_ids = _bound_var_ids(node, "strokes")
    for stroke in node.get("strokes") or []:
        s_hex = paint_to_hex(stroke)
        if s_hex:
            spath = registry.register_color(
                s_hex,
                style_id=stroke_style_id,
                var_ids=stroke_var_ids,
                role_hint="stroke",
            )
            tokens_ref["stroke"] = f"{{{spath}}}"
            sw = node.get("strokeWeight")
            if isinstance(sw, (int, float)) and sw > 0:
                out["strokeWeight"] = round(sw, 2)
            break

    # Corner radius
    cr = node.get("cornerRadius")
    if isinstance(cr, (int, float)) and cr > 0:
        rpath = registry.register_radius(cr, var_ids=_bound_var_ids(node, "cornerRadius"))
        tokens_ref["radius"] = f"{{{rpath}}}"
    elif isinstance(node.get("rectangleCornerRadii"), list) and any(r > 0 for r in node["rectangleCornerRadii"] if isinstance(r, (int, float))):
        radii_list = [round(r) if isinstance(r, (int, float)) else 0 for r in node["rectangleCornerRadii"][:4]]
        out["cornerRadii"] = radii_list
        for r in radii_list:
            if r > 0:
                registry.register_radius(r)

    # Effects / shadows
    effect_style_id = node_styles.get("effect") or node_styles.get("effects")
    for eff in node.get("effects") or []:
        sh_path = registry.register_shadow(eff, style_id=effect_style_id)
        if sh_path:
            tokens_ref["shadow"] = f"{{{sh_path}}}"
            break

    # Text content, typography token & text overflow/alignment metadata
    if kind == "TEXT":
        chars = (node.get("characters") or "").strip()
        out["text"] = chars
        tstyle = node.get("style") or {}
        text_style_id = node_styles.get("text")
        typo_path = registry.register_typography(tstyle, style_id=text_style_id)
        if typo_path:
            tokens_ref["textStyle"] = f"{{{typo_path}}}"
        text_meta: dict[str, Any] = {}
        max_lines = node.get("maxLines") or tstyle.get("maxLines")
        if isinstance(max_lines, int) and not isinstance(max_lines, bool) and max_lines > 0:
            text_meta["maxLines"] = max_lines
        if tstyle.get("textTruncation") == "ENDING" or node.get("textTruncation") == "ENDING":
            text_meta["truncation"] = "ellipsis"
        if tstyle.get("textAutoResize") in ("WIDTH_AND_HEIGHT", "HEIGHT", "NONE", "TRUNCATE"):
            text_meta["autoResize"] = str(tstyle["textAutoResize"]).lower()
        if tstyle.get("textAlignHorizontal") in ("CENTER", "RIGHT", "JUSTIFIED"):
            text_meta["align"] = str(tstyle["textAlignHorizontal"]).lower()
        if text_meta:
            out["textMeta"] = text_meta

    # Auto-layout & advanced layout semantics (Framelink flex vocabulary)
    raw_mode = node.get("layoutMode")
    sizing_h = SIZING_MAP.get(str(node.get("layoutSizingHorizontal") or ""), None)
    sizing_v = SIZING_MAP.get(str(node.get("layoutSizingVertical") or ""), None)
    is_abs = node.get("layoutPositioning") == "ABSOLUTE"
    overflow_dir = node.get("overflowDirection")
    has_scroll_dir = overflow_dir in (
        "HORIZONTAL_SCROLLING",
        "VERTICAL_SCROLLING",
        "HORIZONTAL_AND_VERTICAL_SCROLLING",
    )
    scroll_beh = node.get("scrollBehavior")
    has_scroll_beh = scroll_beh in ("FIXED_WHEN_SCROLLING", "STICKY_SCROLLING")
    min_max = {
        k: round(node[k])
        for k in ("minWidth", "maxWidth", "minHeight", "maxHeight")
        if isinstance(node.get(k), (int, float)) and not isinstance(node.get(k), bool) and node[k] > 0
    }

    if (
        raw_mode in ("HORIZONTAL", "VERTICAL")
        or is_screen_root
        or sizing_h
        or sizing_v
        or is_abs
        or has_scroll_dir
        or has_scroll_beh
        or min_max
    ):
        mode = "row" if raw_mode == "HORIZONTAL" else ("column" if raw_mode == "VERTICAL" else "none")
        layout_info: dict[str, Any] = {"mode": mode}
        if raw_mode in ("HORIZONTAL", "VERTICAL"):
            jc = PRIMARY_ALIGN_MAP.get(str(node.get("primaryAxisAlignItems") or ""), None)
            ai = COUNTER_ALIGN_MAP.get(str(node.get("counterAxisAlignItems") or ""), None)
            if jc:
                layout_info["justifyContent"] = jc
            if ai:
                layout_info["alignItems"] = ai
            gap = round(node.get("itemSpacing", 0) or 0)
            if gap > 0:
                gpath = registry.register_spacing(gap, var_ids=_bound_var_ids(node, "itemSpacing"))
                layout_info["gap"] = gap
                tokens_ref["gap"] = f"{{{gpath}}}"
            pt = round(node.get("paddingTop", 0) or 0)
            pr = round(node.get("paddingRight", 0) or 0)
            pb = round(node.get("paddingBottom", 0) or 0)
            pl = round(node.get("paddingLeft", 0) or 0)
            if any((pt, pr, pb, pl)):
                layout_info["padding"] = [pt, pr, pb, pl]
                for pval in (pt, pr, pb, pl):
                    if pval > 0:
                        registry.register_spacing(pval)
            if node.get("layoutWrap") == "WRAP":
                layout_info["wrap"] = True
        if sizing_h or sizing_v:
            layout_info["sizing"] = {
                "horizontal": sizing_h or "fixed",
                "vertical": sizing_v or "fixed",
            }
        if node.get("clipsContent") is True:
            layout_info["clipsContent"] = True
        if is_abs:
            layout_info["positioning"] = "absolute"
            constraints = node.get("constraints")
            if isinstance(constraints, dict) and ("horizontal" in constraints or "vertical" in constraints):
                layout_info["constraints"] = {
                    "horizontal": str(constraints.get("horizontal", "MIN")).lower(),
                    "vertical": str(constraints.get("vertical", "MIN")).lower(),
                }
        if has_scroll_dir:
            layout_info["scrollDirection"] = {
                "HORIZONTAL_SCROLLING": "horizontal",
                "VERTICAL_SCROLLING": "vertical",
                "HORIZONTAL_AND_VERTICAL_SCROLLING": "both",
            }[overflow_dir]
        if has_scroll_beh:
            layout_info["scrollBehavior"] = "fixed" if scroll_beh == "FIXED_WHEN_SCROLLING" else "sticky"
        if min_max:
            layout_info["minMax"] = min_max
        out["layout"] = layout_info

    # Component / Instance metadata
    if kind in ("INSTANCE", "COMPONENT"):
        comp_id = str(node.get("componentId") or node.get("id") or "")
        comp_meta = components_map.get(comp_id, {})
        comp_name = comp_meta.get("name") or node.get("name", "?")
        set_id = comp_meta.get("componentSetId")
        set_meta = component_sets_map.get(str(set_id or ""), {})
        raw_props = node.get("componentProperties") or {}
        props = {
            k: (v.get("value") if isinstance(v, dict) else v)
            for k, v in raw_props.items()
        }
        comp_info: dict[str, Any] = {
            "id": comp_id or None,
            "name": comp_name,
        }
        if set_meta.get("name"):
            comp_info["componentSet"] = set_meta["name"]
        if props:
            comp_info["properties"] = props
        comp_info["patternHint"] = infer_canonical_pattern(
            node.get("name", ""),
            comp_name,
            set_meta.get("name", ""),
        )
        out["component"] = comp_info

    if tokens_ref:
        out["tokens"] = tokens_ref

    dests = _node_destinations(node)
    if dests:
        out["navigateTo"] = dests[0] if len(dests) == 1 else dests

    # Children recursion (skip internal vector paths inside an ICON/VECTOR)
    if out["type"] not in ("ICON", *VECTOR_LEAF_TYPES):
        vis_children = [c for c in (node.get("children") or []) if c.get("visible") is not False]
        if vis_children:
            normalized_children = [
                _normalize_node_tree(c, registry, components_map, component_sets_map, is_screen_root=False)
                for c in vis_children
            ]
            out["children"] = _deduplicate_repeating_children(normalized_children)

    return out


def _extract_screen_spec(
    screen_node: dict,
    index: int,
    registry: TokenRegistry,
    components_map: dict[str, Any],
    component_sets_map: dict[str, Any],
    image_path: Optional[str] = None,
) -> dict[str, Any]:
    """Build the structured specification dictionary for one screen (`S01`, `S02`...)."""
    b = _box(screen_node) or {"x": 0, "y": 0, "width": 0, "height": 0}
    bg_color = next((h for h in map(_hex, screen_node.get("fills") or []) if h), None)
    if not bg_color and isinstance(screen_node.get("backgroundColor"), dict):
        bg_color = _hex({"type": "SOLID", "color": screen_node["backgroundColor"]})

    padding = [
        round(screen_node.get("paddingTop", 0) or 0),
        round(screen_node.get("paddingRight", 0) or 0),
        round(screen_node.get("paddingBottom", 0) or 0),
        round(screen_node.get("paddingLeft", 0) or 0),
    ]
    layout = {
        "mode": screen_node.get("layoutMode") or "NONE",
        "item_spacing": round(screen_node.get("itemSpacing", 0) or 0),
        "padding": padding,
        "corner_radius": round(screen_node.get("cornerRadius", 0) or 0),
        "background": bg_color,
    }

    sections: list[dict[str, Any]] = []
    for child in screen_node.get("children") or []:
        if child.get("visible") is False:
            continue
        if child.get("type") in {"FRAME", "SECTION", "GROUP"}:
            sections.append({
                "id": child.get("id"),
                "name": child.get("name", "?"),
                "type": child.get("type"),
                "size": _size(child),
                "layout_mode": child.get("layoutMode") or "NONE",
            })

    comp_items: list[dict[str, Any]] = []
    texts: list[tuple[int, int, str, Optional[str], Optional[str]]] = []

    for node, _ in _walk(screen_node):
        kind = node.get("type")
        if kind == "INSTANCE":
            comp_id = str(node.get("componentId") or "")
            comp_meta = components_map.get(comp_id, {})
            comp_name = comp_meta.get("name") or node.get("name", "?")
            set_id = comp_meta.get("componentSetId")
            set_meta = component_sets_map.get(str(set_id or ""), {})
            raw_props = node.get("componentProperties") or {}
            variant_props = {
                k: (v.get("value") if isinstance(v, dict) else v)
                for k, v in raw_props.items()
            }
            inner_texts = [
                (sub.get("characters") or "").strip()
                for sub, _ in _walk(node)
                if sub.get("type") == "TEXT" and (sub.get("characters") or "").strip()
            ]
            comp_items.append({
                "node_id": node.get("id"),
                "layer_name": node.get("name", "?"),
                "component_id": comp_id or None,
                "component_name": comp_name,
                "pattern_hint": infer_canonical_pattern(
                    node.get("name", ""),
                    comp_name,
                    set_meta.get("name", ""),
                ),
                "size": _size(node),
                "variant_properties": variant_props,
                "texts": inner_texts,
            })
        elif kind == "TEXT":
            style = node.get("style") or {}
            font = _font(style)
            chars = (node.get("characters") or "").strip()
            if chars:
                tb = _box(node) or {"x": 0, "y": 0}
                color = next((h for h in map(_hex, node.get("fills") or []) if h), None)
                texts.append((round(tb.get("y", 0)), round(tb.get("x", 0)), chars, font, color))

    texts.sort(key=lambda t: (t[0], t[1]))
    texts_reading_order = [
        {
            "text": " / ".join(chars.splitlines()),
            "font": font,
            "color": color,
            "x": x,
            "y": y,
        }
        for y, x, chars, font, color in texts
    ]

    normalized_tree = _normalize_node_tree(
        screen_node,
        registry,
        components_map,
        component_sets_map,
        is_screen_root=True,
    )

    return {
        "screen_index": index,
        "suggested_id": f"S{index:02d}",
        "node_id": screen_node.get("id"),
        "name": screen_node.get("name", f"Screen {index}"),
        "type": screen_node.get("type", "FRAME"),
        "image_path": image_path,
        "bounds": {
            "x": round(b.get("x", 0)),
            "y": round(b.get("y", 0)),
            "width": round(b.get("width", 0)),
            "height": round(b.get("height", 0)),
        },
        "layout": layout,
        "sections": sections,
        "components": comp_items,
        "texts_reading_order": texts_reading_order,
        "interactions": _extract_interactions(screen_node),
        "tree": normalized_tree,
    }


def build_spec_and_tokens(
    payload: dict[str, Any],
    node_id: str,
    url: str,
    *,
    file_key: Optional[str] = None,
    root_image_path: Optional[str] = None,
    screen_image_paths: Optional[dict[str, str]] = None,
    tokens_filename: str = "tokens.json",
) -> tuple[dict[str, Any], TokenRegistry]:
    """Build both the Framelink-style `<stem>.spec.json` and the file-level DTCG `TokenRegistry`."""
    entry = payload["nodes"][node_id]
    root = entry["document"]
    components_map = entry.get("components") or {}
    component_sets_map = entry.get("componentSets") or {}
    styles_map = entry.get("styles") or {}
    screen_image_paths = screen_image_paths or {}

    registry = TokenRegistry(
        file_key=file_key,
        file_name=payload.get("name", "?"),
        last_modified=payload.get("lastModified"),
        styles_meta=styles_map,
        components_meta=components_map,
        component_sets_meta=component_sets_map,
    )

    color_roles: Counter[tuple[str, str]] = Counter()
    typography_counter: Counter[tuple[str, Any, Any, Any]] = Counter()
    radii_set: set[int] = set()
    spacing_counter: Counter[tuple[str, int, int, int, int, int]] = Counter()
    comp_catalog_counter: Counter[tuple[str, str]] = Counter()

    for node, depth in _walk(root):
        kind = node.get("type")
        is_text = kind == "TEXT"
        role_default = "text" if is_text else ("background" if depth == 0 else "fill")
        for paint in node.get("fills") or []:
            c = _hex(paint)
            if c:
                color_roles[(c, role_default)] += 1
        for stroke in node.get("strokes") or []:
            sc = _hex(stroke)
            if sc:
                color_roles[(sc, "stroke")] += 1

        if is_text:
            style = node.get("style") or {}
            if style.get("fontFamily"):
                lh = style.get("lineHeightPx")
                typography_counter[(
                    style["fontFamily"],
                    style.get("fontWeight"),
                    style.get("fontSize"),
                    round(lh) if isinstance(lh, (int, float)) else None,
                )] += 1

        cr = node.get("cornerRadius")
        if isinstance(cr, (int, float)) and cr > 0:
            radii_set.add(round(cr))
        for r in node.get("rectangleCornerRadii") or []:
            if isinstance(r, (int, float)) and r > 0:
                radii_set.add(round(r))

        lmode = node.get("layoutMode")
        if lmode in ("HORIZONTAL", "VERTICAL"):
            isp = round(node.get("itemSpacing", 0) or 0)
            pt = round(node.get("paddingTop", 0) or 0)
            pr = round(node.get("paddingRight", 0) or 0)
            pb = round(node.get("paddingBottom", 0) or 0)
            pl = round(node.get("paddingLeft", 0) or 0)
            spacing_counter[(lmode, isp, pt, pr, pb, pl)] += 1

        if kind == "INSTANCE":
            cid = str(node.get("componentId") or "")
            cmeta = components_map.get(cid, {})
            cname = cmeta.get("name") or node.get("name", "?")
            comp_catalog_counter[(cid, cname)] += 1

    screen_nodes = extract_screen_nodes(root)
    screens_spec: list[dict[str, Any]] = []
    for idx, snode in enumerate(screen_nodes, start=1):
        sid = str(snode.get("id") or "")
        img = screen_image_paths.get(sid)
        if not img and len(screen_nodes) == 1 and sid == str(root.get("id") or node_id):
            img = root_image_path
        screens_spec.append(
            _extract_screen_spec(snode, idx, registry, components_map, component_sets_map, image_path=img)
        )

    spec_dict = {
        "file_key": file_key,
        "file_name": payload.get("name", "?"),
        "last_modified": payload.get("lastModified"),
        "source_url": url,
        "tokens_file": tokens_filename,
        "root_node_id": node_id,
        "root_name": root.get("name", node_id),
        "root_type": root.get("type", "?"),
        "root_image_path": root_image_path,
        "design_tokens": {
            "colors": [
                {"hex": hex_val, "role_hint": role, "uses": count}
                for (hex_val, role), count in color_roles.most_common()
            ],
            "typography": [
                {"family": fam, "weight": weight, "size": size, "line_height": lh, "uses": count}
                for (fam, weight, size, lh), count in typography_counter.most_common()
            ],
            "corner_radii": sorted(radii_set),
            "spacings": [
                {
                    "layout_mode": lmode,
                    "item_spacing": isp,
                    "padding": [pt, pr, pb, pl],
                    "uses": count,
                }
                for (lmode, isp, pt, pr, pb, pl), count in spacing_counter.most_common()
            ],
            "component_catalog": [
                {
                    "component_id": cid or None,
                    "component_name": cname,
                    "pattern_hint": infer_canonical_pattern(
                        cname,
                        cname,
                        component_sets_map.get(
                            str(components_map.get(cid, {}).get("componentSetId") or ""),
                            {},
                        ).get("name", ""),
                    ),
                    "instances_count": count,
                }
                for (cid, cname), count in comp_catalog_counter.most_common()
            ],
        },
        "screens": screens_spec,
    }
    return spec_dict, registry


def build_spec_dict(
    payload: dict[str, Any],
    node_id: str,
    url: str,
    *,
    file_key: Optional[str] = None,
    root_image_path: Optional[str] = None,
    screen_image_paths: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    """Build the structured Figma spec JSON (`<stem>.spec.json`)."""
    spec_dict, _ = build_spec_and_tokens(
        payload,
        node_id,
        url,
        file_key=file_key,
        root_image_path=root_image_path,
        screen_image_paths=screen_image_paths,
    )
    return spec_dict


def render_summary(
    payload: dict[str, Any],
    node_id: str,
    url: str,
    png_name: Optional[str] = None,
    screen_png_names: Optional[dict[str, str]] = None,
) -> str:
    entry = payload["nodes"][node_id]
    root = entry["document"]
    components = entry.get("components") or {}
    screen_png_names = screen_png_names or {}
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

    screen_nodes = extract_screen_nodes(root)
    if len(screen_nodes) > 1 or screen_png_names:
        lines += ["", f"## Screens ({len(screen_nodes)})", "", "| ID | Name | Node ID | Size | Image |", "|---|---|---|---|---|"]
        for idx, snode in enumerate(screen_nodes, start=1):
            sid = f"S{idx:02d}"
            snid = str(snode.get("id") or "")
            spng = screen_png_names.get(snid) or (png_name if len(screen_nodes) == 1 else None)
            img_cell = f"![{sid}]({spng})" if spng else "(none)"
            lines.append(f"| {sid} | {_cell(snode.get('name', '?'))} | `{snid}` | {_size(snode)} | {img_cell} |")

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
