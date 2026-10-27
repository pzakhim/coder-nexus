"""Build ready-to-copy plugin projections (`python -m coder_nexus.plugin_build`).

All projection logic lives here. The VS Code extension and `coder-nexus install-plugin`
only copy a built projection with `apply_projection` and record the chosen packs in
`.agents/stack.json`, so the two installers cannot drift.

Source layout::

    plugins/core/             agents/ (stack-neutral roles), skills/, slots.json, plugin files
    plugins/layers/<layer>/   layer.json (markers), agents/<role>.md overlays shared by packs
    plugins/packs/<stack>/    pack.json, skills/<slot>/, rules/, agents/<role>.md overlays
    plugins/shared_contracts/

A pack skill installs as `<stack>-<name>`. `{{slot:x}}` renders to the installed name: in a
pack file to that pack's skill, in core/layer files to the skill of every installed pack that
the file serves. A projection holds exactly one pack (3.2.0: a workspace has one stack); role
agents are the core agent followed by the pack's layer overlays and the pack overlay.

Output layout (default `plugins/dist/`)::

    packs.json                  installable packs and their status
    <layout>-<stack>/
        projection.json         {"packs", "status", "stubs", "problems", "managed", "remove", ...}
        files/                  tree relative to the destination root

`layout` is `workspace` (root = the workspace folder) or `global` (root = the host's global
plugins folder); both are built once per pack. Installers delete every `remove` and `managed`
path, then copy `managed`, so installing another pack replaces the previous one.

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
PLUGIN_NAME = "coder-nexus"
LEGACY_PLUGINS = ("coder-nexus-fe", "coder-nexus-be")
LAYOUTS = ("workspace", "global")

SLOT_RE = re.compile(r"\{\{slot:([a-z0-9-]+)\}\}")
TICKED_SLOT_RE = re.compile(r"`\{\{slot:([a-z0-9-]+)\}\}`")
LINK_RE = re.compile(r"\]\(([^)#\s]+)(#[^)]*)?\)")
NAME_RE = re.compile(r"^name:[^\n]*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
SKILLS_BLOCK_RE = re.compile(r"^skills:\n((?:[ \t]+-[ \t]+.*\n?)+)", re.MULTILINE)
PREFIXED_REF_RE = re.compile(r"`([a-z]+)-([a-z0-9-]+)`")
PROFILE_MARKER_RE = re.compile(
    r"<!-- \{\{profile_references\}\} -->|"
    r"<!-- \{\{profile_references:start\}\} -->.*?<!-- \{\{profile_references:end\}\} -->",
    re.DOTALL,
)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
TOPIC_RE = re.compile(r"^>\s*Topic:\s*(.+)$", re.MULTILINE)

STACK_ROUTING = (
    "## Stack rules\n\n"
    "The sections below hold the rules of each installed stack. `.agents/stack.json` lists the installed "
    "packs and the workspace paths each one owns; apply only the rules of the pack that owns the files "
    "you are working on, and treat a path no pack owns as a question for the user."
)


# --------------------------------------------------------------------------- helpers

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


# --------------------------------------------------------------------------- packs and slots

def available_packs(plugins_dir: Path = PLUGINS_DIR) -> list[str]:
    return sorted(p.parent.name for p in (plugins_dir / "packs").glob("*/pack.json"))


def load_pack(plugins_dir: Path, stack: str) -> dict:
    pack = _read_json(plugins_dir / "packs" / stack / "pack.json")
    pack.setdefault("stack", stack)
    pack.setdefault("title", stack)
    pack.setdefault("status", "maintained")
    pack.setdefault("slots", {})
    pack.setdefault("extra", [])
    pack.setdefault("layers", [])
    pack.setdefault("markers", [])
    pack.setdefault("not_applicable", [])
    return pack


def load_slots(plugins_dir: Path) -> dict[str, str]:
    return _read_json(plugins_dir / "core" / "slots.json").get("slots", {})


def load_required_slots(plugins_dir: Path) -> list[str]:
    return _read_json(plugins_dir / "core" / "slots.json").get("required", [])


def combo_key(packs: list[str]) -> str:
    return "+".join(sorted(set(packs)))


STUB_TEMPLATES = {
    "not_applicable": (
        "{title} does not use this step.",
        "This slot is not applicable to {title}. When a process step asks for `{name}`, skip it, "
        "record `N/A ({title})` with a one-line reason in the work item, and continue. "
        "Never invent stack rules to fill the gap.",
    ),
    "blocked": (
        "Not available yet for {title} (preview pack) — stop and report BLOCKED.",
        "{title} is a preview pack and does not provide `{name}` yet ({purpose}). When a process step needs it, "
        "stop that step and report `BLOCKED: {name} is not available for {title}` to the coordinator, naming the "
        "decision or rule the user must supply. Do not borrow another stack's rules and never mark the step PASS.",
    ),
}


def _write_stub(skill_dir: Path, name: str, kind: str, title: str, purpose: str) -> None:
    description, body = STUB_TEMPLATES[kind]
    fields = {"name": name, "title": title, "purpose": purpose.rstrip(".").lower()}
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description.format(**fields)}\n---\n\n"
        f"# {name}\n\n{body.format(**fields)}\n",
        encoding="utf-8",
    )


def _slot_gaps(plugins_dir: Path, pack: dict) -> dict[str, str]:
    """slot -> stub kind for every registered slot the pack does not implement."""
    gaps = {}
    for slot in load_slots(plugins_dir):
        if slot in pack["slots"]:
            continue
        if slot in pack["not_applicable"]:
            gaps[slot] = "not_applicable"
        elif pack["status"] == "preview":
            gaps[slot] = "blocked"
        else:
            gaps[slot] = "missing"
    return gaps


# --------------------------------------------------------------------------- rendering

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


def render_slots(text: str, stacks: list[str]) -> str:
    """`{{slot:x}}` -> `<stack>-x` for each stack the text serves."""
    if not stacks:
        return text
    text = TICKED_SLOT_RE.sub(lambda m: " / ".join(f"`{s}-{m.group(1)}`" for s in stacks), text)
    return SLOT_RE.sub(lambda m: " / ".join(f"{s}-{m.group(1)}" for s in stacks), text)


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


def _expand_skill(name: str, stacks: list[str]) -> list[str]:
    match = SLOT_RE.fullmatch(name)
    return [f"{s}-{match.group(1)}" for s in stacks] if match else [name]


def compose_agent(parts: list[tuple[Path, list[str]]], dest: Path, path_map: dict[Path, Path]) -> str:
    """Compose a role agent from (source file, stacks it serves) parts: the core agent first,
    then overlays. Slots, links and the frontmatter `skills:` list are rendered per part."""
    core_path, core_stacks = parts[0]
    frontmatter, body = _split_frontmatter(core_path.read_text(encoding="utf-8"))
    skills: list[str] = []
    for name in _frontmatter_skills(frontmatter):
        skills.extend(n for n in _expand_skill(name, core_stacks) if n not in skills)
    sections = [_rewrite_links(render_slots(body, core_stacks), core_path, dest, path_map).rstrip("\n")]
    if len(parts) > 1:
        sections.append(STACK_ROUTING)
    for overlay, stacks in parts[1:]:
        overlay_front, overlay_body = _split_frontmatter(overlay.read_text(encoding="utf-8"))
        for name in _frontmatter_skills(overlay_front):
            skills.extend(n for n in _expand_skill(name, stacks) if n not in skills)
        sections.append(_rewrite_links(render_slots(overlay_body, stacks), overlay, dest, path_map).strip("\n"))
    frontmatter = render_slots(frontmatter, core_stacks)
    if skills:
        listing = "skills:\n" + "".join(f"  - {name}\n" for name in skills)
        if SKILLS_BLOCK_RE.search(frontmatter + "\n"):
            frontmatter = SKILLS_BLOCK_RE.sub(lambda _m: listing, frontmatter + "\n", count=1).rstrip("\n")
        else:
            frontmatter = f"{frontmatter}\n{listing.rstrip()}"
    return f"---\n{frontmatter}\n---\n" + "\n\n".join(sections) + "\n"


def _render_documents(path_map: dict[Path, Path], owners: dict[Path, list[str]], skills_out: Path) -> None:
    for src, dest in path_map.items():
        if src not in owners:
            continue
        documents = [dest] if dest.is_file() else [*dest.rglob("*.md"), *dest.rglob("*.tpl")]
        for document in documents:
            if document.suffix not in (".md", ".tpl"):
                continue
            source_doc = src if src.is_file() else src / document.relative_to(dest)
            text = document.read_text(encoding="utf-8")
            rewritten = render_slots(_rewrite_links(text, source_doc, document, path_map), owners[src])
            if document.name == "SKILL.md" and document.parent.parent == skills_out:
                rewritten = NAME_RE.sub(f"name: {document.parent.name}", rewritten, count=1)
            if rewritten != text:
                document.write_text(rewritten, encoding="utf-8")


# --------------------------------------------------------------------------- projection

def project_bundle(plugins_dir: Path, packs: list[str], out: Path, agents_out: Path | None = None) -> dict:
    """Install core + `packs` into the plugin folder `out` (must not exist).

    Agents are written to `out/agents` unless `agents_out` is given.
    Returns {"problems": [...], "stubs": {...}}.
    """
    plugins_dir = plugins_dir.resolve()
    core = plugins_dir / "core"
    shared_contracts = plugins_dir / "shared_contracts"
    if not (shared_contracts / "api_handshake_protocol.md").is_file():
        raise FileNotFoundError("Missing shared API handshake protocol")
    packs = sorted(set(packs))
    unknown_packs = sorted(set(packs) - set(available_packs(plugins_dir)))
    if not packs or unknown_packs:
        raise ValueError(f"unknown or empty pack selection: {unknown_packs or packs}")
    loaded = [load_pack(plugins_dir, stack) for stack in packs]
    required_slots = load_required_slots(plugins_dir)
    for pack in loaded:
        for req in required_slots:
            if req not in pack.get("slots", {}) or req in pack.get("not_applicable", []):
                raise ValueError(f"packs/{pack['stack']}: required slot {req} missing or not_applicable")
    out.mkdir(parents=True)
    agents_dest = agents_out or out / "agents"
    layer_users: dict[str, list[str]] = {}
    for pack in loaded:
        for layer in pack["layers"]:
            layer_users.setdefault(layer, []).append(pack["stack"])

    path_map: dict[Path, Path] = {}
    owners: dict[Path, list[str]] = {}
    problems: list[str] = []

    def place(src: Path, dest: Path, stacks: list[str]) -> None:
        path_map[src] = dest
        owners[src] = stacks

    for entry in sorted(core.iterdir()):
        if entry.name not in ("agents", "skills", "bundle_manifest.json", "slots.json"):
            place(entry, out / entry.name, packs)
    place(shared_contracts, out / "shared_contracts", packs)
    for skill in _skill_dirs(core / "skills"):
        place(skill, out / "skills" / skill.name, packs)
    for pack in loaded:
        pack_dir = plugins_dir / "packs" / pack["stack"]
        units = {**pack["slots"], **{name: name for name in pack["extra"]}}
        for installed_as, source_name in units.items():
            place(pack_dir / "skills" / source_name, out / "skills" / f"{pack['stack']}-{installed_as}", [pack["stack"]])
        for rule in sorted((pack_dir / "rules").glob("*.md")):
            if out / "rules" / rule.name in path_map.values():
                problems.append(f"packs/{pack['stack']}/rules/{rule.name}: rule file name clashes with another pack")
            place(rule, out / "rules" / rule.name, [pack["stack"]])
        guideline = pack_dir / "GUIDELINE.md"  # a guide for people, next to the plugin's json files
        if guideline.is_file():
            place(guideline, out / guideline.name, [pack["stack"]])
    (out / "skills").mkdir(exist_ok=True)
    (out / "rules").mkdir(exist_ok=True)
    for src, dest in path_map.items():
        _copy_entry(src, dest)

    slots = load_slots(plugins_dir)
    stubs: dict[str, str] = {}
    for pack in loaded:
        problems += [f"packs/{pack['stack']}/pack.json: unknown slot {slot}" for slot in pack["slots"] if slot not in slots]
        for slot, kind in _slot_gaps(plugins_dir, pack).items():
            name = f"{pack['stack']}-{slot}"
            if kind != "missing":  # a missing maintained slot is reported by check_projection
                _write_stub(out / "skills" / name, name, kind, pack["title"], slots[slot])
                stubs[name] = kind
    if stubs:
        _write_json(out / "slot_stubs.json", stubs)

    # links into agents resolve to the installed agents folder
    path_map[core / "agents"] = agents_dest
    for layer in layer_users:
        path_map[plugins_dir / "layers" / layer / "agents"] = agents_dest
    for pack in loaded:
        path_map[plugins_dir / "packs" / pack["stack"] / "agents"] = agents_dest
    _render_documents(path_map, owners, out / "skills")

    agents_dest.mkdir(parents=True, exist_ok=True)
    for core_agent in sorted((core / "agents").glob("*.md")):
        parts = [(core_agent, packs)]
        emitted_layers: set[str] = set()
        for pack in loaded:  # each pack's layers (first use only), then the pack overlay
            for layer in pack["layers"]:
                if layer not in emitted_layers:
                    emitted_layers.add(layer)
                    parts.append((plugins_dir / "layers" / layer / "agents" / core_agent.name, layer_users[layer]))
            parts.append((plugins_dir / "packs" / pack["stack"] / "agents" / core_agent.name, [pack["stack"]]))
        parts = [parts[0]] + [(path, stacks) for path, stacks in parts[1:] if path.is_file()]
        dest = agents_dest / core_agent.name
        dest.write_text(compose_agent(parts, dest, path_map), encoding="utf-8")

    _finish_manifest(out, plugins_dir, path_map, core / "bundle_manifest.json", loaded)

    known: set[str] = set()
    foreign_markers: list[str] = []
    foreign_stacks: set[str] = set()
    for stack in available_packs(plugins_dir):
        other = load_pack(plugins_dir, stack)
        known |= set(other["slots"]) | set(other["extra"]) | set(slots)
        if stack not in packs:
            foreign_markers.extend(other["markers"])
            foreign_stacks.add(stack)
    for layer_file in sorted((plugins_dir / "layers").glob("*/layer.json")):
        if layer_file.parent.name not in layer_users:
            foreign_markers.extend(_read_json(layer_file).get("markers", []))
    problems += check_projection(out, agents_dest, known, set(packs), foreign_markers, foreign_stacks)
    return {"problems": sorted(set(problems)), "stubs": stubs}


def _finish_manifest(out: Path, plugins_dir: Path, path_map: dict[Path, Path], manifest_src: Path,
                     loaded: list[dict]) -> None:
    manifest = _read_json(manifest_src)
    manifest.pop("resource_base", None)
    manifest["public_skills"] = sorted(p.name for p in _skill_dirs(out / "skills"))
    resources = []
    for res in manifest.get("required_resources", []):
        mapped = _mapped((plugins_dir / res).resolve(), path_map)
        if mapped is not None:
            resources.append(os.path.relpath(mapped, out))
    manifest["required_resources"] = resources
    manifest["packs"] = [pack["stack"] for pack in loaded]
    _write_json(out / "bundle_manifest.json", manifest)
    _write_json(out / "installed_version.json", {
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "packs": [pack["stack"] for pack in loaded],
    })


def check_projection(plugin_out: Path, agents_dir: Path | None, known: set[str] | None = None,
                     stacks: set[str] | None = None, foreign_markers: list[str] | None = None,
                     foreign_stacks: set[str] | None = None) -> list[str]:
    """Report unresolved slots, agent skills that are not installed, broken links and
    instructions that belong to a stack (or layer) that is not part of this projection."""
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
    for skill_dir in _skill_dirs(plugin_out / "skills"):
        profiles_dir = skill_dir / "profiles"
        if not profiles_dir.is_dir():
            continue
        skill_label = str(skill_dir.relative_to(plugin_out))
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        if not PROFILE_MARKER_RE.search(skill_text):
            problems.append(f"{skill_label}/SKILL.md: missing <!-- {{{{profile_references}}}} --> marker for profiles/")
        base_refs = {p.name for p in (skill_dir / "references").glob("*.md")} if (skill_dir / "references").is_dir() else set()
        for profile_md in sorted(profiles_dir.glob("*/*.md")):
            md_label = str(profile_md.relative_to(plugin_out))
            if profile_md.name in base_refs:
                problems.append(f"{md_label}: filename collides with base references/{profile_md.name}")
            if not H1_RE.search(profile_md.read_text(encoding="utf-8")):
                problems.append(f"{md_label}: missing top-level '# <Title>' heading")
    return sorted(set(problems))


def read_workspace_profile(workspace: Path) -> str | None:
    """Return the active architecture profile recorded in `<workspace>/.superpowers/setup.json`, if any."""
    profile = _read_json(workspace / ".superpowers" / "setup.json").get("profile")
    return profile.strip() if isinstance(profile, str) and profile.strip() else None


def _extract_profile_doc_meta(md_path: Path) -> tuple[str, str]:
    text = md_path.read_text(encoding="utf-8")
    h1 = H1_RE.search(text)
    title = h1.group(1).strip() if h1 else md_path.stem.replace("-", " ").title()
    topic_match = TOPIC_RE.search(text)
    topic = topic_match.group(1).strip() if topic_match else title
    return title, topic


def _source_profiles_dir(skill_name: str, plugins_dir: Path) -> Path | None:
    core_profiles = plugins_dir / "core" / "skills" / skill_name / "profiles"
    if core_profiles.is_dir():
        return core_profiles
    for stack in available_packs(plugins_dir):
        prefix = f"{stack}-"
        if not skill_name.startswith(prefix):
            continue
        slot_or_extra = skill_name.removeprefix(prefix)
        pack = load_pack(plugins_dir, stack)
        source_name = pack.get("slots", {}).get(slot_or_extra, slot_or_extra)
        candidate = plugins_dir / "packs" / stack / "skills" / source_name / "profiles"
        if candidate.is_dir():
            return candidate
    return None


def apply_workspace_profile(
    plugin_dir: Path,
    profile: str | None,
    plugins_dir: Path = PLUGINS_DIR,
) -> list[str]:
    """Activate `profiles/<profile>/*.md` across installed skills in `plugin_dir`.

    For each skill with a `profiles/` directory (either in `skill_dir/profiles` or in source `plugins_dir`):
    - Removes any previously copied profile `.md` files from `references/`.
    - Copies all `*.md` files from `profiles/<profile>/` into `references/`.
    - Injects one table row per `.md` file at `<!-- {{profile_references}} -->` in `SKILL.md`.
    - Deletes `skill_dir/profiles` when `profile` is specified so only active references remain.
    Returns the list of relative reference paths activated.
    """
    activated: list[str] = []
    for skill_dir in _skill_dirs(plugin_dir / "skills"):
        local_profiles = skill_dir / "profiles"
        source_profiles = local_profiles if local_profiles.is_dir() else _source_profiles_dir(skill_dir.name, plugins_dir)
        if source_profiles is None or not source_profiles.is_dir():
            continue
        refs_dir = skill_dir / "references"
        all_profile_filenames = {p.name for p in source_profiles.glob("*/*.md")}
        if refs_dir.is_dir():
            for stale_name in all_profile_filenames:
                _remove(refs_dir / stale_name)
        rows: list[str] = []
        if profile:
            profile_dir = source_profiles / profile
            if profile_dir.is_dir():
                refs_dir.mkdir(parents=True, exist_ok=True)
                for md_file in sorted(profile_dir.glob("*.md")):
                    dest_ref = refs_dir / md_file.name
                    shutil.copy2(md_file, dest_ref)
                    title, topic = _extract_profile_doc_meta(md_file)
                    rows.append(f"| **[Profile: `{profile}`]** {topic} | [{title}](references/{md_file.name}) |")
                    activated.append(f"{skill_dir.name}/references/{md_file.name}")
            skill_md = skill_dir / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            replacement = (
                "<!-- {{profile_references:start}} -->\n"
                + "\n".join(rows)
                + "\n<!-- {{profile_references:end}} -->"
                if rows
                else "<!-- {{profile_references}} -->"
            )
            updated = PROFILE_MARKER_RE.sub(lambda _m: replacement, text, count=1)
            if updated != text:
                skill_md.write_text(updated, encoding="utf-8")
            _remove(local_profiles)
    return activated


def _status(loaded: list[dict]) -> str:
    return "preview" if any(pack["status"] == "preview" for pack in loaded) else "maintained"


def build_variant(packs: list[str] | str, layout: str, out: Path, plugins_dir: Path = PLUGINS_DIR) -> Path:
    """Build the projection of one pack (`packs` is the stack name or a one-item list)."""
    packs = sorted(set(packs.split("+") if isinstance(packs, str) else packs))
    if len(packs) != 1:
        raise ValueError(
            f"a projection holds exactly one pack, got {combo_key(packs) or 'none'}; "
            "replace the installed pack instead of combining packs"
        )
    key = combo_key(packs)
    target = out / f"{layout}-{key}"
    _remove(target)
    files = target / "files"
    if layout == "workspace":
        plugin_rel = f".agents/plugins/{PLUGIN_NAME}"
        agents_out = files / ".agents/agents"
        result = project_bundle(plugins_dir, packs, files / plugin_rel, agents_out)
        managed = [plugin_rel, *(f".agents/agents/{a.name}" for a in sorted(agents_out.glob("*.md")))]
        remove = [f".agents/plugins/{name}" for name in LEGACY_PLUGINS]
    else:
        plugin_rel = PLUGIN_NAME
        result = project_bundle(plugins_dir, packs, files / plugin_rel)
        managed = [plugin_rel]
        remove = list(LEGACY_PLUGINS)
    loaded = [load_pack(plugins_dir, stack) for stack in packs]
    status = _status(loaded)
    if result["problems"] and status == "maintained":
        raise ValueError(f"{layout}-{key} projection is incomplete:\n  " + "\n  ".join(result["problems"]))
    manifest = _read_json(files / plugin_rel / "bundle_manifest.json")
    _write_json(target / "projection.json", {
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "packs": [{"stack": p["stack"], "title": p["title"], "status": p["status"]} for p in loaded],
        "layout": layout,
        "status": status,
        "stubs": result["stubs"],
        "problems": result["problems"],
        "managed": managed,
        "remove": remove,
    })
    return target


def build(out: Path = DEFAULT_OUT, plugins_dir: Path = PLUGINS_DIR) -> list[Path]:
    _remove(out)
    out.mkdir(parents=True)
    targets = [build_variant([stack], layout, out, plugins_dir)
               for layout in LAYOUTS for stack in available_packs(plugins_dir)]
    _write_json(out / "packs.json", {"packs": [
        {key: load_pack(plugins_dir, stack)[key] for key in ("stack", "title", "status")}
        for stack in available_packs(plugins_dir)
    ]})
    return targets


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
    if spec.get("layout") == "workspace":
        profile = read_workspace_profile(dest_root)
        if profile:
            apply_workspace_profile(dest_root / spec["managed"][0], profile)
    return spec


def write_stack_file(workspace: Path, spec: dict, paths: dict[str, list[str]] | None = None) -> dict:
    """Record the installed packs (and the workspace paths each owns) in `.agents/stack.json`."""
    paths = paths or {}
    data = {
        "plugin_version": spec.get("plugin_version", "UNKNOWN"),
        "packs": [
            {**pack, "paths": paths.get(pack["stack"]) or ["."]}
            for pack in spec.get("packs", [])
        ],
    }
    _write_json(workspace / ".agents" / "stack.json", data)
    return data


def read_stack_file(workspace: Path) -> dict:
    return _read_json(workspace / ".agents" / "stack.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Coder Nexus plugin projections.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    for target in build(args.out):
        spec = _read_json(target / "projection.json")
        notes = []
        if spec.get("stubs"):
            notes.append(f"{len(spec['stubs'])} placeholder/N-A slots")
        if spec.get("problems"):
            notes.append(f"{len(spec['problems'])} known gaps")
        print(f"built {target.name}" + (f" ({spec.get('status')}: {', '.join(notes)})" if notes else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
