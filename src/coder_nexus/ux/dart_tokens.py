"""Read design tokens straight from Flutter source (no Dart toolchain needed).

Extracts:
- color constants: `static const name = Color(0xAARRGGBB);` and aliases `static const x = primary;`
- seed colors: `ColorScheme.fromSeed(seedColor: Color(0x...))` / `colorSchemeSeed: Color(0x...)`
- fonts declared in pubspec.yaml (`flutter: fonts:` family + asset files)
- widget classes (`class X extends StatelessWidget|StatefulWidget`) for the component inventory
"""

import re
from pathlib import Path
from typing import Optional

_COLOR_CONST = re.compile(
    r"static\s+(?:const|final)\s+(?:Color\s+)?(\w+)\s*=\s*(?:const\s+)?Color\(\s*0x([0-9A-Fa-f]{8})\s*\)"
)
_ALIAS_CONST = re.compile(r"static\s+(?:const|final)\s+(?:Color\s+)?(\w+)\s*=\s*([A-Za-z_]\w*)\s*;")
_SEED = re.compile(r"(?:seedColor|colorSchemeSeed)\s*:\s*(?:const\s+)?Color\(\s*0x([0-9A-Fa-f]{8})\s*\)")
_PRIMARY_THEME = re.compile(r"\bprimary(?:Color)?\s*:\s*(?:const\s+)?Color\(\s*0x([0-9A-Fa-f]{8})\s*\)")
_WIDGET = re.compile(r"^class\s+(\w+)(?:<[^>]*>)?\s+extends\s+(StatelessWidget|StatefulWidget)", re.MULTILINE)
_FONT_FAMILY_IN_CODE = re.compile(r"fontFamily\s*:\s*['\"]([^'\"]+)['\"]")


def argb_to_css(argb: str) -> str:
    """'FF4B7ABD' -> '#4b7abd'; with alpha -> rgba()."""
    a, rgb = int(argb[:2], 16), argb[2:].lower()
    if a == 255:
        return f"#{rgb}"
    r, g, b = int(rgb[0:2], 16), int(rgb[2:4], 16), int(rgb[4:6], 16)
    return f"rgba({r}, {g}, {b}, {round(a / 255, 3)})"


def read_color_constants(dart_file: Path) -> dict[str, str]:
    """Color constants of one Dart file, aliases resolved (`info = primary`)."""
    text = dart_file.read_text(encoding="utf-8", errors="ignore")
    colors = {name: argb_to_css(val) for name, val in _COLOR_CONST.findall(text)}
    for _ in range(3):  # resolve alias chains
        for name, target in _ALIAS_CONST.findall(text):
            if name not in colors and target in colors:
                colors[name] = colors[target]
    return colors


def find_seed_color(files: list[Path]) -> Optional[str]:
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for rx in (_SEED, _PRIMARY_THEME):
            m = rx.search(text)
            if m:
                return argb_to_css(m.group(1))
    return None


def find_font_family_in_code(files: list[Path]) -> Optional[str]:
    for f in files:
        m = _FONT_FAMILY_IN_CODE.search(f.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1)
    return None


def widget_classes(lib_dir: Path) -> list[dict]:
    """Public widget classes under lib_dir: [{name, kind, path}]."""
    out = []
    for f in sorted(lib_dir.rglob("*.dart")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for name, kind in _WIDGET.findall(text):
            if not name.startswith("_"):
                out.append({"name": name, "kind": kind, "path": str(f)})
    return out


def pubspec_fonts(pubspec: Path) -> list[dict]:
    """`flutter: fonts:` entries -> [{family, files: [{asset, weight, style}]}] (no YAML dependency)."""
    if not pubspec.is_file():
        return []
    families: list[dict] = []
    in_flutter = in_fonts = False
    current: Optional[dict] = None
    file_entry: Optional[dict] = None
    for raw in pubspec.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0:
            in_flutter = stripped == "flutter:"
            in_fonts = False
            continue
        if in_flutter and indent <= 2 and stripped == "fonts:":
            in_fonts = True
            continue
        if in_flutter and indent <= 2 and stripped.endswith(":") and stripped != "fonts:":
            in_fonts = False
        if not in_fonts:
            continue
        m = re.match(r"-?\s*family:\s*(.+)", stripped)
        if m:
            current = {"family": m.group(1).strip().strip("'\""), "files": []}
            families.append(current)
            continue
        m = re.match(r"-?\s*asset:\s*(.+)", stripped)
        if m and current is not None:
            file_entry = {"asset": m.group(1).strip().strip("'\""), "weight": 400, "style": "normal"}
            current["files"].append(file_entry)
            continue
        m = re.match(r"weight:\s*(\d+)", stripped)
        if m and file_entry is not None:
            file_entry["weight"] = int(m.group(1))
            continue
        m = re.match(r"style:\s*(\w+)", stripped)
        if m and file_entry is not None:
            file_entry["style"] = m.group(1)
    return families
