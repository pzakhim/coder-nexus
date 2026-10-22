"""Read the generator library shipped with the package: generators, versions and packages."""

from __future__ import annotations

import difflib
import json
import re
from dataclasses import dataclass
from pathlib import Path

LIBRARY_DIR = Path(__file__).resolve().parent / "library"
GENERATORS_DIR = LIBRARY_DIR / "generators"
CORE_DIR = LIBRARY_DIR / "core"
PACKAGES_FILE = LIBRARY_DIR / "packages.json"

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_FIELD_RE = re.compile(r"^(name|description):\s*(.*)$", re.MULTILINE)


class CatalogError(ValueError):
    """An unknown generator or package was requested."""


@dataclass(frozen=True, slots=True)
class Generator:
    name: str
    version: str
    description: str
    path: Path
    packages: tuple[str, ...]


def load_packages() -> dict[str, list[str]]:
    return json.loads(PACKAGES_FILE.read_text(encoding="utf-8"))


def _read_generator(path: Path, packages: dict[str, list[str]]) -> Generator:
    skill = (path / "SKILL.md").read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(skill)
    fields = dict(_FIELD_RE.findall(match.group(1))) if match else {}
    return Generator(
        name=fields.get("name", path.name),
        version=(path / "VERSION").read_text(encoding="utf-8").strip(),
        description=fields.get("description", ""),
        path=path,
        packages=tuple(sorted(p for p, members in packages.items() if path.name in members)),
    )


def list_generators(package: str | None = None) -> list[Generator]:
    packages = load_packages()
    if package is not None and package not in packages:
        raise CatalogError(_unknown("package", package, list(packages)))
    names = packages[package] if package else sorted(p.name for p in GENERATORS_DIR.iterdir() if (p / "SKILL.md").is_file())
    return [_read_generator(GENERATORS_DIR / name, packages) for name in names]


def resolve(names: list[str]) -> list[Generator]:
    """Map full (`create-clean-code-skill`) or short (`clean-code`) names to generators."""
    available = {g.name: g for g in list_generators()}
    resolved: list[Generator] = []
    for raw in names:
        full = raw if raw in available else f"create-{raw}-skill"
        if full not in available:
            raise CatalogError(_unknown("skill", raw, list(available)))
        if available[full] not in resolved:
            resolved.append(available[full])
    return resolved


def _unknown(kind: str, value: str, choices: list[str]) -> str:
    short = [c.removeprefix("create-").removesuffix("-skill") for c in choices]
    close = difflib.get_close_matches(value, choices + short, n=3)
    hint = f" Did you mean: {', '.join(close)}?" if close else f" Available: {', '.join(sorted(choices))}."
    return f"Unknown {kind} '{value}'.{hint}"
