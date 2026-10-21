"""Resolve where a Flutter Client's look comes from and build `design-system.json`.

Order (first match wins; the designer records the result as a D-NN with the user):
1. app-ui-kit  - the `app_ui_kit` package is used (company `imespro` profile)
2. client-theme - the Client has its own color/theme classes (`external-structured`)
3. material3   - plain Flutter: Material 3 baseline + seed/brand color if found (`external-standard`)
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .dart_tokens import (
    find_font_family_in_code,
    find_seed_color,
    pubspec_fonts,
    read_color_constants,
    widget_classes,
)

# Semantic roles used by kit.css, in the order they are documented.
ROLES = [
    "primary", "on-primary", "primary-light", "secondary", "background", "surface", "text", "text-2", "text-3",
    "border", "divider", "input-border", "disabled", "hint", "error", "error-bg", "success", "success-bg",
    "warning", "warning-bg", "info-bg", "shadow",
]

MATERIAL3_DEFAULTS = {
    "primary": "#6750a4", "on-primary": "#ffffff", "primary-light": "#eaddff", "secondary": "#625b71",
    "background": "#fef7ff", "surface": "#f7f2fa", "text": "#1d1b20", "text-2": "#49454f", "text-3": "#79747e",
    "border": "#cac4d0", "divider": "#e6e0e9", "input-border": "#79747e", "disabled": "#c4c0c8", "hint": "#79747e",
    "error": "#b3261e", "error-bg": "#f9dedc", "success": "#2e7d32", "success-bg": "#e6f4ea", "warning": "#ed6c02",
    "warning-bg": "#fff4e5", "info-bg": "#e8def8", "shadow": "rgba(0, 0, 0, 0.1)",
}

# Exact AppColor names in app-ui-kit.
APP_UI_KIT_ROLE_NAMES = {
    "primary": "primary", "on-primary": "textOnPrimary", "primary-light": "primaryLight", "secondary": "secondary",
    "background": "appBgColor", "surface": "surfaceColor", "text": "textPrimary", "text-2": "textSecondary",
    "text-3": "textTertiary", "border": "borderColor", "divider": "dividerColor", "input-border": "inputBorder",
    "disabled": "disabledColor", "hint": "hintColor", "error": "error", "error-bg": "errorLight", "success": "success",
    "success-bg": "successLight", "warning": "warning", "warning-bg": "warningLight", "info-bg": "infoLight",
    "shadow": "shadowColor",
}

# Name heuristics for a Client's own color classes (first matching pattern wins).
ROLE_PATTERNS = {
    "primary": [r"^primary$", r"^brand$", r"^primaryColor$", r"^main$"],
    "on-primary": [r"onPrimary", r"textOnPrimary", r"^white$"],
    "primary-light": [r"primaryLight", r"primary(50|100|Container)"],
    "secondary": [r"^secondary$", r"^accent$"],
    "background": [r"^background$", r"bg(Color)?$", r"scaffold"],
    "surface": [r"^surface", r"^card"],
    "text": [r"^text(Primary|Main|Dark)?$", r"^textColor$", r"^black$", r"^dark$"],
    "text-2": [r"textSecondary", r"^grey$", r"^gray$", r"subtitle", r"^medium$"],
    "text-3": [r"textTertiary", r"textHint", r"textLight"],
    "border": [r"^border", r"outline"],
    "divider": [r"divider", r"separator"],
    "input-border": [r"inputBorder", r"fieldBorder"],
    "disabled": [r"disabled", r"inactive"],
    "hint": [r"hint", r"placeholder"],
    "error": [r"^error$", r"^danger$", r"^red$"],
    "error-bg": [r"error(Light|Bg|Background)", r"danger(Light|Bg)"],
    "success": [r"^success$", r"^green$"],
    "success-bg": [r"success(Light|Bg|Background)"],
    "warning": [r"^warning$", r"^orange$", r"^amber$"],
    "warning-bg": [r"warning(Light|Bg|Background)"],
    "info-bg": [r"info(Light|Bg|Background)"],
    "shadow": [r"shadow"],
}

# Project widget -> kit class. Order matters (more specific first).
WIDGET_TO_KIT = [
    (r"Shimmer|Skeleton", "app-shimmer"), (r"BackButton", "app-appbar"),
    (r"Password", "app-formfield"), (r"Search", "app-search"), (r"Dropdown|Select", "app-dropdown"),
    (r"Date(Picker)?", "app-datepicker"), (r"Button", "app-button"), (r"FormField|TextField|Input", "app-formfield"),
    (r"Dialog|Alert", "app-dialog"), (r"BottomSheet", "app-bottomsheet"), (r"BottomNav|NavigationBar|TabBar", "app-bottomnav"),
    (r"App[Bb]ar|Header", "app-appbar"), (r"Badge|Tag", "app-badge"), (r"NoData|Empty", "app-nodata"),
    (r"Loading|Spinner|Progress", "app-loading"), (r"Card", "app-card"),
    (r"ListTile|ListItem", "app-list-item"), (r"Chip", "app-chip"),
]

MATERIAL_COMPONENTS = [
    ("app-appbar", "AppBar"), ("app-button", "FilledButton / ElevatedButton / OutlinedButton / TextButton"),
    ("app-formfield", "TextField / TextFormField"), ("app-search", "SearchBar"), ("app-dropdown", "DropdownMenu"),
    ("app-datepicker", "showDatePicker"), ("app-dialog", "AlertDialog"), ("app-bottomsheet", "showModalBottomSheet"),
    ("app-bottomnav", "NavigationBar"), ("app-badge", "Badge"), ("app-card", "Card"), ("app-list-item", "ListTile"),
    ("app-chip", "Chip"), ("app-loading", "CircularProgressIndicator"), ("app-shimmer", "(skeleton placeholder)"),
    ("app-nodata", "(empty state column)"), ("app-banner", "MaterialBanner / SnackBar"),
]

MATERIAL3_GEOMETRY = {
    "radius-button": "20px", "button-height": "40px", "button-font-size": "14px", "button-font-weight": "500",
    "radius-input": "4px", "input-padding": "16px", "input-font-size": "16px", "label-font-size": "12px",
    "label-font-weight": "400", "radius-card": "12px", "radius-dialog": "28px", "radius-sheet": "28px",
    "appbar-height": "64px", "body-font-size": "14px", "spacing": "16px",
}


def _rel(path: Path, project: Path) -> str:
    try:
        return str(path.resolve().relative_to(project.resolve()))
    except ValueError:
        return str(path)


def find_app_ui_kit(project: Path) -> Optional[Path]:
    """Root of the app_ui_kit package used by `project`, if any."""
    pubspec = project / "pubspec.yaml"
    text = pubspec.read_text(encoding="utf-8", errors="ignore") if pubspec.is_file() else ""
    if re.search(r"^name:\s*app_ui_kit\s*$", text, re.MULTILINE):
        return project
    uses_kit = re.search(r"^\s+app_ui_kit\s*:", text, re.MULTILINE) is not None
    config = project / ".dart_tool" / "package_config.json"
    if config.is_file():
        try:
            for pkg in json.loads(config.read_text(encoding="utf-8")).get("packages", []):
                if pkg.get("name") == "app_ui_kit":
                    uri = pkg.get("rootUri", "")
                    root = Path(uri[7:]) if uri.startswith("file://") else (config.parent / uri)
                    if (root / "lib").is_dir():
                        return root.resolve()
        except (ValueError, OSError):
            pass
    if uses_kit:
        m = re.search(r"^\s+app_ui_kit\s*:\s*\n\s+path:\s*(.+)$", text, re.MULTILINE)
        if m and (project / m.group(1).strip().strip("'\"")).is_dir():
            return (project / m.group(1).strip().strip("'\"")).resolve()
        for sibling in ("app-ui-kit", "app_ui_kit"):
            cand = project.parent / sibling
            if (cand / "lib" / "app_ui_kit").is_dir():
                return cand.resolve()
    return None


def _match_roles(colors: dict[str, str], prefix: str) -> dict[str, dict]:
    roles: dict[str, dict] = {}
    for role, patterns in ROLE_PATTERNS.items():
        for pat in patterns:
            name = next((n for n in colors if re.search(pat, n, re.IGNORECASE)), None)
            if name:
                roles[role] = {"value": colors[name], "from": f"{prefix}.{name}"}
                break
    return roles


def _fill_defaults(roles: dict[str, dict], seed: Optional[str] = None) -> dict[str, dict]:
    out = {}
    for role in ROLES:
        if role in roles:
            out[role] = roles[role]
        elif role == "primary" and seed:
            out[role] = {"value": seed, "from": "theme seed color"}
        else:
            out[role] = {"value": MATERIAL3_DEFAULTS[role], "from": "material3 default"}
    return out


def _kit_geometry(kit_root: Path) -> dict[str, str]:
    """Read the few numbers that shape AppButton / AppFormField; fall back to known values."""
    geo = dict(MATERIAL3_GEOMETRY)
    geo.update({"radius-button": "8px", "button-height": "48px", "button-font-size": "16px", "button-font-weight": "600",
                "radius-input": "8px", "input-padding": "12px 16px", "input-font-size": "16px", "label-font-size": "14px",
                "label-font-weight": "500", "radius-card": "12px", "radius-dialog": "16px", "radius-sheet": "16px",
                "appbar-height": "56px"})
    btn = kit_root / "lib" / "app_ui_kit" / "app_button.dart"
    if btn.is_file():
        t = btn.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"this\.height\s*=\s*(\d+)", t)
        if m:
            geo["button-height"] = f"{m.group(1)}px"
        m = re.search(r"borderRadius\s*\?\?\s*BorderRadius\.circular\((\d+)\)", t)
        if m:
            geo["radius-button"] = f"{m.group(1)}px"
    field = kit_root / "lib" / "app_ui_kit" / "app_formfield.dart"
    if field.is_file():
        t = field.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"BorderRadius\.circular\((\d+)\)", t)
        if m:
            geo["radius-input"] = f"{m.group(1)}px"
        m = re.search(r"contentPadding:\s*const\s+EdgeInsets\.symmetric\(horizontal:\s*(\d+),\s*vertical:\s*(\d+)\)", t)
        if m:
            geo["input-padding"] = f"{m.group(2)}px {m.group(1)}px"
    return geo


def _components_from_widgets(widgets: list[dict], project: Path, status: str) -> list[dict]:
    comps, seen = [], set()
    for w in widgets:
        kit_class = next((cls for pat, cls in WIDGET_TO_KIT if re.search(pat, w["name"])), None)
        comps.append({"kit_class": kit_class, "widget": w["name"], "status": status if kit_class else "code-only",
                      "path": _rel(Path(w["path"]), project)})
        if kit_class:
            seen.add(kit_class)
    # Generic layout pieces always available
    for cls, desc in (("app-card", "container"), ("app-list-item", "list row"), ("app-banner", "inline message")):
        if cls not in seen:
            comps.append({"kit_class": cls, "widget": desc, "status": "layout", "path": None})
    return comps


def _font(project: Path, families: list[dict], code_family: Optional[str], base: Path) -> dict:
    fam = None
    if families:
        fam = next((f for f in families if code_family and f["family"] == code_family), families[0])
    if fam:
        files = [{"path": str((base / f["asset"]).resolve()), "weight": f["weight"], "style": f["style"]}
                 for f in fam["files"] if (base / f["asset"]).is_file()]
        return {"family": fam["family"], "files": files, "from": f"pubspec fonts ({_rel(base / 'pubspec.yaml', project)})"}
    if code_family:
        return {"family": code_family, "files": [], "from": "fontFamily in code (font files not found)"}
    return {"family": "Roboto", "files": [], "from": "material3 default"}


def resolve_design_system(project: Path) -> dict:
    project = project.resolve()
    lib = project / "lib"
    dart_files = sorted(lib.rglob("*.dart")) if lib.is_dir() else []
    warnings: list[str] = []
    kit = find_app_ui_kit(project)

    if kit is not None:
        color_file = kit / "lib" / "app_ui_kit" / "app_color.dart"
        colors = read_color_constants(color_file) if color_file.is_file() else {}
        roles = {r: {"value": colors[n], "from": f"AppColor.{n}"} for r, n in APP_UI_KIT_ROLE_NAMES.items() if n in colors}
        missing = [r for r in ROLES if r not in roles]
        if missing:
            warnings.append(f"app-ui-kit has no color for roles {missing}; Material 3 defaults used.")
        widgets = widget_classes(kit / "lib" / "app_ui_kit")
        kit_dart = sorted((kit / "lib").rglob("*.dart"))
        source = {"kind": "app-ui-kit", "profile_hint": "imespro", "evidence": [_rel(color_file, project), _rel(kit, project)]}
        system = {
            "colors": colors, "roles": _fill_defaults(roles),
            "font": _font(project, pubspec_fonts(kit / "pubspec.yaml"), find_font_family_in_code(kit_dart), kit),
            "geometry": _kit_geometry(kit),
            "components": _components_from_widgets(widgets, project, "kit"),
        }
    else:
        theme_files = [f for f in dart_files if re.search(r"(color|colour|theme|palette|token|style)", f.name, re.IGNORECASE)]
        colors: dict[str, str] = {}
        evidence = []
        for f in theme_files:
            found = read_color_constants(f)
            if found:
                colors.update(found)
                evidence.append(_rel(f, project))
        seed = find_seed_color(dart_files)
        code_font = find_font_family_in_code(dart_files)
        if len(colors) >= 6:
            shared = [f for f in dart_files if re.search(r"/(shared|common|widgets|components|ui|core)/", str(f))]
            widgets = widget_classes(lib) if not shared else [w for d in {f.parent for f in shared} for w in widget_classes(d)]
            uniq = {w["name"]: w for w in widgets}
            source = {"kind": "client-theme", "profile_hint": "external-structured", "evidence": evidence}
            system = {
                "colors": colors, "roles": _fill_defaults(_match_roles(colors, "client"), seed),
                "font": _font(project, pubspec_fonts(project / "pubspec.yaml"), code_font, project),
                "geometry": dict(MATERIAL3_GEOMETRY),
                "components": _components_from_widgets(list(uniq.values()), project, "client"),
            }
            warnings.append("Geometry (radius, heights) uses Material 3 values; check against current-app screenshots.")
        else:
            source = {"kind": "material3", "profile_hint": "external-standard",
                      "evidence": [_rel(f, project) for f in dart_files if seed and seed[1:] in f.read_text(errors="ignore").lower()][:3]}
            system = {
                "colors": colors, "roles": _fill_defaults({}, seed),
                "font": _font(project, pubspec_fonts(project / "pubspec.yaml"), code_font, project),
                "geometry": dict(MATERIAL3_GEOMETRY),
                "components": [{"kit_class": c, "widget": w, "status": "framework", "path": None} for c, w in MATERIAL_COMPONENTS],
            }
            if not seed:
                warnings.append("No brand/seed color found; ask the user for the brand color, font and Material vs Cupertino.")

    source["decision"] = None  # D-NN once the user confirms the source
    return {
        "schema": 1,
        "generated_by": "coder-nexus ux extract",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "project": project.name,
        "source": source,
        **system,
        "warnings": warnings,
    }
