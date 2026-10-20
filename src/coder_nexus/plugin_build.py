"""Build ready-to-copy plugin projections (`python -m coder_nexus.plugin_build`).

All projection logic lives here. The VS Code extension and `coder-nexus install-plugin`
only copy a built projection with `apply_projection`, so the two installers cannot drift.

Source layout::

    plugins/core/            agents/ (process-only roles), skills/ (stack-neutral), plugin files
    plugins/layers/<layer>/  agents/<role>.md overlays shared by several packs (e.g. frontend)
    plugins/packs/<stack>/   pack.json, skills/<slot>/, rules/, agents/<role>.md overlays
    plugins/shared_contracts/

A pack skill installs as `<stack>-<slot>`; `{{slot:x}}` in any document renders to that name.
Role agents are the core agent plus, in order, each layer overlay and the pack overlay.

Output layout (default `plugins/dist/`)::

    <layout>-<variant>/
        projection.json   {"plugin_version", "variant", "layout", "managed", "remove", "problems"}
        files/            tree relative to the destination root

`layout` is `workspace` (root = the workspace folder) or `global` (root = the host's global
plugins folder). Installers delete every `remove` and `managed` path, then copy `managed`.

Standard library only: extension tests and CI run this without project dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
DEFAULT_OUT = PLUGINS_DIR / "dist"

# variant -> plugin name and packs (a pack-less variant projects a legacy plugin folder)
VARIANTS: dict[str, dict] = {
    "fe-flutter": {"plugin": "coder-nexus-fe", "packs": ["flutter"]},
    "fe-frappe": {"plugin": "coder-nexus-fe", "packs": ["frappe"]},
    "be": {"plugin": "coder-nexus-be", "packs": [], "legacy_dir": "coder-nexus-be"},
}
LAYOUTS = ("workspace", "global")

SLOT_RE = re.compile(r"\{\{slot:([a-z0-9-]+)\}\}")
LINK_RE = re.compile(r"\]\(([^)#\s]+)(#[^)]*)?\)")
NAME_RE = re.compile(r"^name:[^\n]*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
SKILLS_BLOCK_RE = re.compile(r"^skills:\n((?:[ \t]+-[ \t]+.*\n?)+)", re.MULTILINE)
PREFIXED_REF_RE = re.compile(r"`([a-z]+)-([a-z0-9-]+)`")


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


def _skill_dirs(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return [p for p in sorted(directory.iterdir()) if p.is_dir() and (p / "SKILL.md").is_file()]


def load_pack(plugins_dir: Path, stack: str) -> dict:
    pack = _read_json(plugins_dir / "packs" / stack / "pack.json")
    pack.setdefault("stack", stack)
    pack.setdefault("status", "maintained")
    pack.setdefault("slots", {})
    pack.setdefault("extra", [])
    pack.setdefault("layers", [])
    pack.setdefault("markers", [])
    return pack


def _mapped(target: Path, path_map: dict[Path, Path]) -> Path | None:
    for src, dest in path_map.items():
        if target == src or src in target.parents:
            return dest / target.relative_to(src)
    return None


def _rewrite_links(text: str, source_doc: Path, dest_doc: Path, path_map: dict[Path, Path]) -> str:
    """Point relative links at the installed location of their (source) target."""

    def sub(match: re.Match) -> str:
        link = match.group(1)
        if "://" in link or link.startswith(("/", "mailto:")):
            return match.group(0)
        target = _mapped((source_doc.parent / link).resolve(), path_map)
        if target is None:
            return match.group(0)
        return f"]({os.path.relpath(target, dest_doc.parent)}{match.group(2) or ''})"

    return LINK_RE.sub(sub, text)


def _split_frontmatter(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    return (match.group(1), text[match.end():]) if match else ("", text)


def _frontmatter_skills(frontmatter: str) -> list[str]:
    block = SKILLS_BLOCK_RE.search(frontmatter + "\n")
    if not block:
        return []
    names = []
    for line in block.group(1).splitlines():
        name = line.strip().removeprefix("-").split("#", 1)[0].strip()
        if name:
            names.append(name)
    return names


def compose_agent(core_agent: Path, overlays: list[Path]) -> str:
    """Core role agent + overlays. Overlay frontmatter `skills:` entries are appended."""
    frontmatter, body = _split_frontmatter(core_agent.read_text(encoding="utf-8"))
    skills = _frontmatter_skills(frontmatter)
    sections = [body.rstrip("\n")]
    for overlay in overlays:
        overlay_front, overlay_body = _split_frontmatter(overlay.read_text(encoding="utf-8"))
        for name in _frontmatter_skills(overlay_front):
            if name not in skills:
                skills.append(name)
        sections.append(overlay_body.strip("\n"))
    if skills:
        listing = "skills:\n" + "".join(f"  - {name}\n" for name in skills)
        if SKILLS_BLOCK_RE.search(frontmatter + "\n"):
            frontmatter = SKILLS_BLOCK_RE.sub(lambda _m: listing, frontmatter + "\n", count=1).rstrip("\n")
        else:
            frontmatter = f"{frontmatter}\n{listing.rstrip()}"
    return f"---\n{frontmatter}\n---\n" + "\n\n".join(sections) + "\n"


def _render_documents(path_map: dict[Path, Path], skills_out: Path, stack: str | None) -> None:
    for src, dest in path_map.items():
        documents = [dest] if dest.is_file() else [*dest.rglob("*.md"), *dest.rglob("*.tpl")]
        for document in documents:
            if document.suffix not in (".md", ".tpl"):
                continue
            source_doc = src if src.is_file() else src / document.relative_to(dest)
            text = document.read_text(encoding="utf-8")
            rewritten = _rewrite_links(text, source_doc, document, path_map)
            if stack:
                rewritten = SLOT_RE.sub(lambda m: f"{stack}-{m.group(1)}", rewritten)
            if document.name == "SKILL.md" and document.parent.parent == skills_out:
                rewritten = NAME_RE.sub(f"name: {document.parent.name}", rewritten, count=1)
            if rewritten != text:
                document.write_text(rewritten, encoding="utf-8")


def _finish_manifest(out: Path, plugins_dir: Path, path_map: dict[Path, Path], manifest_src: Path,
                     framework: str | None, plugin_name: str | None = None) -> None:
    manifest = _read_json(manifest_src)
    base = plugins_dir if manifest.get("resource_base") == "plugins/" else manifest_src.parent
    manifest.pop("resource_base", None)
    skills_out = out / "skills"
    if skills_out.is_dir():
        manifest["public_skills"] = sorted(p.name for p in _skill_dirs(skills_out))
    resources = []
    for res in manifest.get("required_resources", []):
        mapped = _mapped((base / res).resolve(), path_map)
        if mapped is not None:
            resources.append(os.path.relpath(mapped, out))
    manifest["required_resources"] = resources
    _write_json(out / "bundle_manifest.json", manifest)
    stamp = {"plugin_version": manifest.get("plugin_version", "UNKNOWN"), "framework": framework}
    _write_json(out / "installed_version.json", stamp)
    if plugin_name:
        plugin_json = _read_json(out / "plugin.json")
        if plugin_json:
            plugin_json["name"] = plugin_name
            _write_json(out / "plugin.json", plugin_json)


def project_bundle(
    plugins_dir: Path,
    packs: list[str],
    out: Path,
    agents_out: Path | None = None,
    plugin_name: str | None = None,
) -> list[str]:
    """Install core + `packs` into the plugin folder `out` (must not exist).

    Agents are written to `out/agents` unless `agents_out` is given. Returns check problems.
    """
    plugins_dir = plugins_dir.resolve()
    core = plugins_dir / "core"
    shared_contracts = plugins_dir / "shared_contracts"
    if not (shared_contracts / "api_handshake_protocol.md").is_file():
        raise FileNotFoundError("Missing shared API handshake protocol")
    if len(packs) != 1:
        raise ValueError("this release projects exactly one pack per plugin")
    out.mkdir(parents=True)
    agents_dest = agents_out or out / "agents"
    loaded = [load_pack(plugins_dir, stack) for stack in packs]

    path_map: dict[Path, Path] = {}
    for entry in sorted(core.iterdir()):
        if entry.name in ("agents", "skills", "bundle_manifest.json"):
            continue
        path_map[entry] = out / entry.name
    path_map[shared_contracts] = out / "shared_contracts"
    for skill in _skill_dirs(core / "skills"):
        path_map[skill] = out / "skills" / skill.name
    for pack in loaded:
        pack_dir = plugins_dir / "packs" / pack["stack"]
        units = {**pack["slots"], **{name: name for name in pack["extra"]}}
        for installed_as, source_name in units.items():
            path_map[pack_dir / "skills" / source_name] = out / "skills" / f"{pack['stack']}-{installed_as}"
        for rule in sorted((pack_dir / "rules").glob("*.md")):
            path_map[rule] = out / "rules" / rule.name
    (out / "skills").mkdir(exist_ok=True)
    (out / "rules").mkdir(exist_ok=True)
    for src, dest in path_map.items():
        _copy_entry(src, dest)

    # role agents: core + layer overlays + pack overlay, composed then rendered like any document
    agents_dest.mkdir(parents=True, exist_ok=True)
    for core_agent in sorted((core / "agents").glob("*.md")):
        overlays = []
        for pack in loaded:
            for layer in pack["layers"]:
                overlays.append(plugins_dir / "layers" / layer / "agents" / core_agent.name)
            overlays.append(plugins_dir / "packs" / pack["stack"] / "agents" / core_agent.name)
        composed = compose_agent(core_agent, [o for o in overlays if o.is_file()])
        (agents_dest / core_agent.name).write_text(composed, encoding="utf-8")
        path_map[core_agent] = agents_dest / core_agent.name

    stack = loaded[0]["stack"]
    _render_documents(path_map, out / "skills", stack)
    _finish_manifest(out, plugins_dir, path_map, core / "bundle_manifest.json", stack, plugin_name)

    known: set[str] = set()
    foreign_markers: list[str] = []
    foreign_stacks: set[str] = set()
    for pack_file in sorted((plugins_dir / "packs").glob("*/pack.json")):
        other = load_pack(plugins_dir, pack_file.parent.name)
        known |= set(other["slots"]) | set(other["extra"])
        if other["stack"] not in packs:
            foreign_markers.extend(other["markers"])
            foreign_stacks.add(other["stack"])
    return check_projection(out, agents_dest, known, {p["stack"] for p in loaded}, foreign_markers, foreign_stacks)


def project_plugin(plugin_dir: Path, out: Path, include_agents: bool = True, agents_out: Path | None = None) -> list[str]:
    """Project a legacy, self-contained plugin folder (Backend until it becomes a pack)."""
    plugin_dir = plugin_dir.resolve()
    shared_contracts = plugin_dir.parent / "shared_contracts"
    if not (shared_contracts / "api_handshake_protocol.md").is_file():
        raise FileNotFoundError("Missing shared API handshake protocol")
    out.mkdir(parents=True)
    agents_dest = out / "agents" if include_agents else agents_out
    path_map: dict[Path, Path] = {}
    for entry in sorted(plugin_dir.iterdir()):
        if entry.name == "agents":
            if agents_dest is not None:
                path_map[entry] = agents_dest
            continue
        path_map[entry] = out / entry.name
    path_map[shared_contracts.resolve()] = out / "shared_contracts"
    for src, dest in path_map.items():
        _copy_entry(src, dest)
    _render_documents(path_map, out / "skills", None)
    _finish_manifest(out, plugin_dir.parent, path_map, plugin_dir / "bundle_manifest.json", None)
    return check_projection(out, agents_dest)


def check_projection(plugin_out: Path, agents_dir: Path | None, known: set[str] | None = None,
                     stacks: set[str] | None = None, foreign_markers: list[str] | None = None,
                     foreign_stacks: set[str] | None = None) -> list[str]:
    """Report unresolved slots, agent skills that are not installed, broken links and
    instructions that belong to a stack that is not part of this projection."""
    problems: list[str] = []
    installed = {p.name for p in _skill_dirs(plugin_out / "skills")}
    documents = list(plugin_out.rglob("*.md")) + list(plugin_out.rglob("*.tpl"))
    if agents_dir is not None and agents_dir.is_dir():
        documents += sorted(agents_dir.glob("*.md"))
    marker_re = (
        re.compile(r"(?<![\w-])(" + "|".join(re.escape(m) for m in foreign_markers) + r")(?![\w-])")
        if foreign_markers else None
    )
    for document in documents:
        text = document.read_text(encoding="utf-8")
        is_agent = agents_dir is not None and document.parent == agents_dir
        label = f"agents/{document.name}" if is_agent else str(document.relative_to(plugin_out))
        for slot in SLOT_RE.findall(text):
            problems.append(f"{label}: unresolved slot {slot}")
        if is_agent:
            for name in _frontmatter_skills(_split_frontmatter(text)[0]):
                if name not in installed:
                    problems.append(f"{label}: declares missing skill {name}")
        if known and stacks:
            for prefix, suffix in PREFIXED_REF_RE.findall(text):
                ref = f"{prefix}-{suffix}"
                if prefix in stacks and suffix in known and ref not in installed:
                    problems.append(f"{label}: references missing skill {ref}")
                elif foreign_stacks and prefix in foreign_stacks and suffix in known:
                    problems.append(f"{label}: references another stack's skill {ref}")
        if marker_re is not None:
            found = sorted(set(marker_re.findall(text)))
            if found:
                problems.append(f"{label}: mentions another stack ({', '.join(found)})")
        if document.suffix == ".md":
            for target, _anchor in LINK_RE.findall(text):
                if "://" in target or target.startswith(("/", "mailto:")):
                    continue
                if not (document.parent / target).exists():
                    problems.append(f"{label}: broken link {target}")
    return sorted(set(problems))


def _variant_status(plugins_dir: Path, variant: str) -> str:
    statuses = [load_pack(plugins_dir, stack)["status"] for stack in VARIANTS[variant]["packs"]]
    return "preview" if "preview" in statuses else "maintained"


def build_variant(variant: str, layout: str, out: Path, plugins_dir: Path = PLUGINS_DIR) -> Path:
    spec = VARIANTS[variant]
    plugin_name = spec["plugin"]
    target = out / f"{layout}-{variant}"
    _remove(target)
    files = target / "files"
    managed: list[str] = []
    remove: list[str] = []
    if layout == "workspace":
        plugin_rel = f".agents/plugins/{plugin_name}"
        agents_out = files / ".agents/agents"
        if spec["packs"]:
            problems = project_bundle(plugins_dir, spec["packs"], files / plugin_rel, agents_out, plugin_name)
        else:
            problems = project_plugin(plugins_dir / spec["legacy_dir"], files / plugin_rel, False, agents_out)
        managed.append(plugin_rel)
        managed.extend(f".agents/agents/{agent.name}" for agent in sorted(agents_out.glob("*.md")))
        remove.extend(sorted({f".agents/plugins/{v['plugin']}" for v in VARIANTS.values()} - {plugin_rel}))
    else:
        if spec["packs"]:
            problems = project_bundle(plugins_dir, spec["packs"], files / plugin_name, None, plugin_name)
        else:
            problems = project_plugin(plugins_dir / spec["legacy_dir"], files / plugin_name, True)
        managed.append(plugin_name)
    if problems and _variant_status(plugins_dir, variant) == "maintained":
        raise ValueError(f"{layout}-{variant} projection is incomplete:\n  " + "\n  ".join(problems))
    manifest = _read_json(files / managed[0] / "bundle_manifest.json")
    _write_json(target / "projection.json", {
        "problems": problems,
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "variant": variant,
        "layout": layout,
        "plugin": plugin_name,
        "managed": managed,
        "remove": remove,
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
        problems = _read_json(target / "projection.json").get("problems", [])
        print(f"built {target}" + (f" ({len(problems)} known gaps, preview pack)" if problems else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
