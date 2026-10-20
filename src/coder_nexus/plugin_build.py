"""Build ready-to-copy plugin projections (`python -m coder_nexus.plugin_build`).

All projection logic (skill filtering, flattening, link and manifest rewriting) lives here.
The VS Code extension and `coder-nexus install-plugin` only copy a built projection with
`apply_projection`, so the two installers cannot drift apart.

Output layout (default `plugins/dist/`)::

    <layout>-<variant>/
        projection.json   {"plugin_version", "variant", "layout", "managed": [...], "remove": [...]}
        files/            tree relative to the destination root

`layout` is `workspace` (root = the workspace folder) or `global` (root = the host's
global plugins folder). Installers delete every `remove` and `managed` path under the root,
then copy each `managed` path from `files/`.

Standard library only: the extension tests and CI run this without project dependencies.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
DEFAULT_OUT = PLUGINS_DIR / "dist"

# variant -> (plugin name, framework or None)
VARIANTS: dict[str, tuple[str, str | None]] = {
    "fe-flutter": ("coder-nexus-fe", "flutter"),
    "fe-frappe": ("coder-nexus-fe", "frappe"),
    "be": ("coder-nexus-be", None),
}
LAYOUTS = ("workspace", "global")
FRAMEWORK_RULES = {"flutter": "clean_architecture_rules.md", "frappe": "frappe_specific_rules.md"}
SKILL_CATEGORIES = ("shared", "flutter", "frappe")


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _copy_entry(src: Path, dest: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def _remove(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _has_categories(plugin_dir: Path) -> bool:
    return any((plugin_dir / "skills" / category).is_dir() for category in ("flutter", "frappe"))


def project_plugin(plugin_dir: Path, out: Path, framework: str | None = "flutter", include_agents: bool = True) -> None:
    """Write the installed form of `plugin_dir` into `out` (which must not exist)."""
    shared_contracts = plugin_dir.parent / "shared_contracts"
    if not (shared_contracts / "api_handshake_protocol.md").is_file():
        raise FileNotFoundError("Missing shared API handshake protocol")
    out.mkdir(parents=True)
    categorized = _has_categories(plugin_dir)
    framework = framework or "flutter"

    for entry in sorted(plugin_dir.iterdir()):
        if entry.name == "agents" and not include_agents:
            continue
        if categorized and entry.name in ("skills", "rules"):
            continue
        _copy_entry(entry, out / entry.name)

    if categorized:
        rule = plugin_dir / "rules" / FRAMEWORK_RULES[framework]
        (out / "rules").mkdir(exist_ok=True)
        if rule.is_file():
            shutil.copy2(rule, out / "rules" / rule.name)
        skills_out = out / "skills"
        skills_out.mkdir(exist_ok=True)
        for category in ("shared", framework):
            category_dir = plugin_dir / "skills" / category
            if not category_dir.is_dir():
                continue
            for skill in sorted(category_dir.iterdir()):
                if skill.is_dir() and (skill / "SKILL.md").is_file():
                    shutil.copytree(skill, skills_out / skill.name, dirs_exist_ok=True)

    shutil.copytree(shared_contracts, out / "shared_contracts", dirs_exist_ok=True)

    if categorized:
        for document in out.rglob("*.md"):
            text = document.read_text(encoding="utf-8")
            rewritten = text.replace("(../../flutter/", "(../").replace("(../skills/flutter/", "(../skills/")
            if rewritten != text:
                document.write_text(rewritten, encoding="utf-8")

    manifest_path = out / "bundle_manifest.json"
    manifest = _read_json(manifest_path)
    resources = manifest.get("required_resources", [])
    if categorized:
        manifest["public_skills"] = sorted(
            p.name for p in (out / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
        )
        excluded = "frappe" if framework == "flutter" else "flutter"
        projected = []
        for res in resources:
            if res.startswith(f"skills/{excluded}/") or res == f"rules/{FRAMEWORK_RULES[excluded]}":
                continue
            for prefix in tuple(f"skills/{c}/" for c in SKILL_CATEGORIES):
                if res.startswith(prefix):
                    res = "skills/" + res[len(prefix):]
                    break
            projected.append(res)
        resources = projected
    projected_resources = []
    for res in resources:
        if res.startswith("../shared_contracts/"):
            res = res[len("../"):]
        elif res.startswith("agents/") and not include_agents:
            res = f"../../{res}"
        projected_resources.append(res)
    manifest["required_resources"] = projected_resources
    _write_json(manifest_path, manifest)
    _write_json(out / "installed_version.json", {
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "framework": framework if categorized else None,
    })


def build_variant(variant: str, layout: str, out: Path, plugins_dir: Path = PLUGINS_DIR) -> Path:
    plugin_name, framework = VARIANTS[variant]
    plugin_dir = plugins_dir / plugin_name
    target = out / f"{layout}-{variant}"
    _remove(target)
    files = target / "files"
    managed: list[str] = []
    remove: list[str] = []
    if layout == "workspace":
        plugin_rel = f".agents/plugins/{plugin_name}"
        project_plugin(plugin_dir, files / plugin_rel, framework, include_agents=False)
        managed.append(plugin_rel)
        for agent in sorted((plugin_dir / "agents").glob("*.md")):
            rel = f".agents/agents/{agent.name}"
            _copy_entry(agent, files / rel)
            managed.append(rel)
        remove.extend(f".agents/plugins/{name}" for name, _ in set(VARIANTS.values()) if name != plugin_name)
    else:
        project_plugin(plugin_dir, files / plugin_name, framework, include_agents=True)
        managed.append(plugin_name)
    manifest = _read_json(plugin_dir / "bundle_manifest.json")
    _write_json(target / "projection.json", {
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "variant": variant,
        "layout": layout,
        "plugin": plugin_name,
        "managed": managed,
        "remove": sorted(remove),
    })
    return target


def build(out: Path = DEFAULT_OUT, plugins_dir: Path = PLUGINS_DIR) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    return [build_variant(v, layout, out, plugins_dir) for v in VARIANTS for layout in LAYOUTS]


def apply_projection(projection_dir: Path, dest_root: Path) -> dict:
    """Copy a built projection into `dest_root`, replacing only the paths it manages."""
    spec = _read_json(projection_dir / "projection.json")
    if not spec.get("managed"):
        raise FileNotFoundError(f"Invalid projection: {projection_dir}")
    files = projection_dir / "files"
    for rel in [*spec.get("remove", []), *spec["managed"]]:
        _remove(dest_root / rel)
    for rel in spec["managed"]:
        _copy_entry(files / rel, dest_root / rel)
    return spec


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Coder Nexus plugin projections.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    for target in build(args.out):
        print(f"built {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
