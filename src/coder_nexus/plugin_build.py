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
import os
import re
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


SLOT_RE = re.compile(r"\{\{slot:([a-z0-9-]+)\}\}")
LINK_RE = re.compile(r"\]\(([^)#\s]+)(#[^)]*)?\)")
NAME_RE = re.compile(r"^name:[^\n]*$", re.MULTILINE)


def _rewrite_links(text: str, source_doc: Path, dest_doc: Path, path_map: dict[Path, Path]) -> str:
    """Point relative links at the installed location of their (source) target."""

    def installed(target: Path) -> Path | None:
        for src, dest in path_map.items():
            if target == src or src in target.parents:
                return dest / target.relative_to(src)
        return None

    def sub(match: re.Match) -> str:
        link = match.group(1)
        if "://" in link or link.startswith(("/", "mailto:")):
            return match.group(0)
        target = installed((source_doc.parent / link).resolve())
        if target is None:
            return match.group(0)
        return f"]({os.path.relpath(target, dest_doc.parent)}{match.group(2) or ''})"

    return LINK_RE.sub(sub, text)


def project_plugin(
    plugin_dir: Path,
    out: Path,
    framework: str | None = "flutter",
    include_agents: bool = True,
    agents_out: Path | None = None,
) -> list[str]:
    """Write the installed form of `plugin_dir` into `out` (which must not exist).

    Agents go to `out/agents` when `include_agents`, otherwise to `agents_out` (if given).
    Framework skills are installed as `<stack>-<slot>`; `{{slot:x}}` renders to that name.
    Returns the problems found by `check_projection`.
    """
    plugin_dir = plugin_dir.resolve()
    shared_contracts = plugin_dir.parent / "shared_contracts"
    if not (shared_contracts / "api_handshake_protocol.md").is_file():
        raise FileNotFoundError("Missing shared API handshake protocol")
    out.mkdir(parents=True)
    categorized = _has_categories(plugin_dir)
    framework = framework or "flutter"
    agents_dest = out / "agents" if include_agents else agents_out

    # source path -> installed path, for every unit we copy
    path_map: dict[Path, Path] = {}
    for entry in sorted(plugin_dir.iterdir()):
        if entry.name == "agents":
            if agents_dest is not None:
                path_map[entry] = agents_dest
            continue
        if categorized and entry.name in ("skills", "rules"):
            continue
        path_map[entry] = out / entry.name
    path_map[shared_contracts.resolve()] = out / "shared_contracts"

    stack = None
    if categorized:
        rule = plugin_dir / "rules" / FRAMEWORK_RULES[framework]
        if rule.is_file():
            path_map[rule] = out / "rules" / rule.name
        (out / "rules").mkdir(exist_ok=True)
        shared_dir = plugin_dir / "skills" / "shared"
        for skill in sorted(shared_dir.iterdir()) if shared_dir.is_dir() else []:
            if skill.is_dir() and (skill / "SKILL.md").is_file():
                path_map[skill] = out / "skills" / skill.name
        pack = _read_json(plugin_dir / "skills" / framework / "pack.json")
        stack = pack.get("stack", framework)
        units = {**pack.get("slots", {}), **{name: name for name in pack.get("extra", [])}}
        for installed_as, source_name in units.items():
            path_map[plugin_dir / "skills" / framework / source_name] = out / "skills" / f"{stack}-{installed_as}"
        (out / "skills").mkdir(exist_ok=True)

    for src, dest in path_map.items():
        _copy_entry(src, dest)

    # render slots, links and skill names in every copied markdown file
    for src, dest in path_map.items():
        documents = [dest] if dest.is_file() else list(dest.rglob("*.md"))
        for document in documents:
            if document.suffix != ".md":
                continue
            source_doc = src if src.is_file() else src / document.relative_to(dest)
            text = document.read_text(encoding="utf-8")
            rewritten = _rewrite_links(text, source_doc, document, path_map)
            if stack:
                rewritten = SLOT_RE.sub(lambda m: f"{stack}-{m.group(1)}", rewritten)
            if document.name == "SKILL.md" and document.parent.parent == out / "skills":
                rewritten = NAME_RE.sub(f"name: {document.parent.name}", rewritten, count=1)
            if rewritten != text:
                document.write_text(rewritten, encoding="utf-8")

    manifest_path = out / "bundle_manifest.json"
    manifest = _read_json(manifest_path)
    if categorized:
        manifest["public_skills"] = sorted(
            p.name for p in (out / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
        )
    resources = []
    for res in manifest.get("required_resources", []):
        target = (plugin_dir / res).resolve()
        mapped = None
        for src, dest in path_map.items():
            if target == src or src in target.parents:
                mapped = dest / target.relative_to(src)
                break
        if mapped is not None:
            resources.append(os.path.relpath(mapped, out))
    manifest["required_resources"] = resources
    _write_json(manifest_path, manifest)
    _write_json(out / "installed_version.json", {
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "framework": framework if categorized else None,
    })
    known = set()
    for pack_file in (plugin_dir / "skills").glob("*/pack.json"):
        pack_data = _read_json(pack_file)
        known |= set(pack_data.get("slots", {})) | set(pack_data.get("extra", []))
    return check_projection(out, agents_dest, known or None)


FRONTMATTER_SKILLS_RE = re.compile(r"^skills:\n((?:\s+-\s+.*\n)+)", re.MULTILINE)
PREFIXED_REF_RE = re.compile(r"`((?:flutter|frappe)-[a-z0-9-]+)`")


def check_projection(plugin_out: Path, agents_dir: Path | None, known: set[str] | None = None) -> list[str]:
    """Report unresolved slots, agent skills that are not installed, and broken links.

    `known` limits prefixed-reference checks to real slot/skill suffixes (so `frappe-ui`,
    the npm package, is not mistaken for a skill).
    """
    problems: list[str] = []
    skills_dir = plugin_out / "skills"
    installed = {p.name for p in skills_dir.iterdir()} if skills_dir.is_dir() else set()
    stacks = {name.split("-", 1)[0] for name in installed if name.startswith(("flutter-", "frappe-"))}
    documents = list(plugin_out.rglob("*.md"))
    if agents_dir is not None and agents_dir.is_dir():
        documents += sorted(agents_dir.glob("*.md"))
    for document in documents:
        text = document.read_text(encoding="utf-8")
        label = document.name if document.parent == agents_dir else str(document.relative_to(plugin_out))
        for slot in SLOT_RE.findall(text):
            problems.append(f"{label}: unresolved slot {slot}")
        if document.parent == agents_dir:
            block = FRONTMATTER_SKILLS_RE.search(text)
            for line in block.group(1).splitlines() if block else []:
                name = line.strip().lstrip("-").split("#", 1)[0].strip()
                if name and name not in installed:
                    problems.append(f"{label}: declares missing skill {name}")
        for ref in PREFIXED_REF_RE.findall(text):
            stack_name, _, suffix = ref.partition("-")
            if stack_name in stacks and ref not in installed and (known is None or suffix in known):
                problems.append(f"{label}: references missing skill {ref}")
        for link in LINK_RE.findall(text):
            target = link[0]
            if "://" in target or target.startswith(("/", "mailto:")):
                continue
            if not (document.parent / target).exists():
                problems.append(f"{label}: broken link {target}")
    return sorted(set(problems))


def _pack_status(plugin_dir: Path, framework: str | None) -> str:
    if not _has_categories(plugin_dir):
        return "maintained"
    return _read_json(plugin_dir / "skills" / (framework or "flutter") / "pack.json").get("status", "maintained")


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
        problems = project_plugin(plugin_dir, files / plugin_rel, framework, include_agents=False,
                                  agents_out=files / ".agents/agents")
        managed.append(plugin_rel)
        managed.extend(f".agents/agents/{agent.name}" for agent in sorted((files / ".agents/agents").glob("*.md")))
        remove.extend(f".agents/plugins/{name}" for name, _ in set(VARIANTS.values()) if name != plugin_name)
    else:
        problems = project_plugin(plugin_dir, files / plugin_name, framework, include_agents=True)
        managed.append(plugin_name)
    if problems and _pack_status(plugin_dir, framework) == "maintained":
        raise ValueError(f"{layout}-{variant} projection is incomplete:\n  " + "\n  ".join(problems))
    manifest = _read_json(plugin_dir / "bundle_manifest.json")
    _write_json(target / "projection.json", {
        "problems": problems,
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
        problems = _read_json(target / "projection.json").get("problems", [])
        print(f"built {target}" + (f" ({len(problems)} known gaps, preview pack)" if problems else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
