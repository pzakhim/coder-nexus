"""Copy generators into a workspace. The copies belong to the workspace afterwards."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from .catalog import CORE_DIR, Generator

GLOBAL_CORE_REF = "~/.claude/skill-factory/core/"
WORKSPACE_CORE_DIR = Path(".agents") / "skill-factory-core"
WORKSPACE_SKILLS_DIR = Path(".agents") / "skills"
CLAUDE_SKILLS_DIR = Path(".claude") / "skills"
TEXT_SUFFIXES = {".md", ".tmpl", ".json"}
IGNORED = shutil.ignore_patterns("__pycache__", ".DS_Store")


@dataclass
class GetResult:
    copied: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    linked: list[str] = field(default_factory=list)
    core: str = ""

    @property
    def ok(self) -> bool:
        return not self.skipped


def get(workspace: Path, generators: list[Generator], *, force: bool = False, claude_link: bool = True) -> GetResult:
    result = GetResult()
    skills_dir = workspace / WORKSPACE_SKILLS_DIR
    for generator in generators:
        dest = skills_dir / generator.name
        if dest.exists() and not force:
            result.skipped.append(f"{generator.name}: {dest} already exists (use --force to replace it)")
            continue
        _copy_tree(generator.path, dest)
        result.copied.append(f"{generator.name} {generator.version} → {dest.relative_to(workspace)}")
        if claude_link:
            link = _link_for_claude(workspace, generator.name, force)
            if link:
                result.linked.append(link)
    if result.copied:
        result.core = _copy_core(workspace, force)
    return result


def _copy_tree(source: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest, ignore=IGNORED)
    for path in dest.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8")
            if GLOBAL_CORE_REF in text:
                # Workspace copies read the core copied next to them, not the machine-wide one.
                path.write_text(text.replace(GLOBAL_CORE_REF, f"{WORKSPACE_CORE_DIR.as_posix()}/"), encoding="utf-8")


def _copy_core(workspace: Path, force: bool) -> str:
    dest = workspace / WORKSPACE_CORE_DIR
    if dest.exists() and not force:
        return f"kept existing {WORKSPACE_CORE_DIR.as_posix()} (use --force to refresh it)"
    _copy_tree(CORE_DIR, dest)
    return f"copied core → {WORKSPACE_CORE_DIR.as_posix()}"


def _link_for_claude(workspace: Path, name: str, force: bool) -> str:
    link = workspace / CLAUDE_SKILLS_DIR / name
    target = Path(os.path.relpath(workspace / WORKSPACE_SKILLS_DIR / name, link.parent))
    if link.is_symlink() and Path(os.readlink(link)) == target:
        return ""
    if link.exists() or link.is_symlink():
        if not force:
            return f"{link.relative_to(workspace)} exists and was left as is"
        if link.is_symlink() or link.is_file():
            link.unlink()
        else:
            shutil.rmtree(link)
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target)
    return f"{link.relative_to(workspace)} → {target.as_posix()}"
