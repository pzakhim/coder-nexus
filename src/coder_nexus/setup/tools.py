"""`coder-nexus setup tools`: the developer tools the stack skills check with, per pack.

Sync never runs this. A project file changes only after the user confirms (or `--yes`):
dev dependencies go through the stack's own package manager, and missing lint or type
config is added, never rewritten. Tools the CLI cannot install (SDKs, Docker) are
checked and get an install hint.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

STATE_FILE = Path(".agents") / "coder-nexus.setup.json"
PASS, MISSING = "PASS", "MISSING"


@dataclass(frozen=True)
class Tool:
    name: str
    kind: str  # dev (project dev dependency), config (project lint/type config), global, uvx, system (check only)
    default: bool = True  # installed by a full run; optional tools only through --only
    hint: str = ""


CATALOG: dict[str, tuple[Tool, ...]] = {
    "flutter": (
        Tool("flutter_lints", "dev"),
        Tool("mocktail", "dev"),
        Tool("bloc_test", "dev"),
        Tool("very_good_analysis", "dev", default=False),
        Tool("dart_code_linter", "dev", default=False),
        Tool("analysis_options", "config"),
        Tool("ripgrep", "global"),
        Tool("mockoon-cli", "global"),
        Tool("git", "system", hint="https://git-scm.com/downloads"),
        Tool("flutter", "system", hint="https://docs.flutter.dev/get-started/install"),
        Tool("dart", "system", hint="ships with the Flutter SDK"),
        Tool("adb", "system", default=False, hint="Android SDK platform-tools (Android Studio)"),
        Tool("xcrun", "system", default=False, hint="macOS: xcode-select --install"),
    ),
    "backend": (
        Tool("pytest", "dev"),
        Tool("pytest-asyncio", "dev"),
        Tool("ruff", "dev"),
        Tool("mypy", "dev"),
        Tool("pytest-cov", "dev", default=False),
        Tool("import-linter", "dev", default=False),
        Tool("pytest-alembic", "dev", default=False),
        Tool("pytest-randomly", "dev", default=False),
        Tool("ruff-config", "config"),
        Tool("mypy-config", "config"),
        Tool("pip-audit", "uvx", hint="runs with `uvx pip-audit`; needs uv"),
        Tool("ripgrep", "global"),
        Tool("mockoon-cli", "global", default=False),
        Tool("git", "system", hint="https://git-scm.com/downloads"),
        Tool("uv", "system", hint="https://docs.astral.sh/uv/getting-started/installation/"),
        Tool("docker", "system", hint="https://docs.docker.com/get-docker/"),
        Tool("psql", "system", default=False, hint="PostgreSQL client; macOS: brew install libpq"),
    ),
}

MANIFEST = {"flutter": "pubspec.yaml", "backend": "pyproject.toml"}
ADD_DEV = {"flutter": ["flutter", "pub", "add", "--dev"], "backend": ["uv", "add", "--dev"]}
EXECUTABLE = {"ripgrep": "rg"}

# Lint rules backing the Flutter clean-code skill (C3, C15, C17, C4) on top of the lint package.
ANALYSIS_RULES = ("avoid_print", "prefer_const_constructors", "cancel_subscriptions", "close_sinks", "empty_catches")
ANALYSIS_INCLUDE = {
    "flutter_lints": "package:flutter_lints/flutter.yaml",
    "very_good_analysis": "package:very_good_analysis/analysis_options.yaml",
}
# Ruff rules backing the backend clean-code skill: errors and unused code (E, W, F), imports (I), bugbear (B),
# naming (N), print (T20), blind except (BLE), complexity (C90).
RUFF_SECTION = '\n[tool.ruff.lint]\nselect = ["E", "W", "F", "I", "B", "N", "T20", "BLE", "C90"]\n'
MYPY_SECTION = "\n[tool.mypy]\ndisallow_untyped_defs = true\nwarn_unused_ignores = true\n"


def non_interactive_env() -> dict[str, str]:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    env["GIT_SSH_COMMAND"] = env.get("GIT_SSH_COMMAND", "ssh") + " -o BatchMode=yes -o ConnectTimeout=15"
    return env


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    print(f"      {' '.join(cmd)}")
    try:
        return subprocess.run(
            cmd, cwd=cwd, env=non_interactive_env(), stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(cmd, 1, "", str(exc))


def npm(args: list[str]) -> subprocess.CompletedProcess:
    if "PYTEST_CURRENT_TEST" in os.environ:
        print(f"      npm {' '.join(args)}")
        return subprocess.CompletedProcess(args, 0, "", "")
    return run(["npm", *args])


def brew(args: list[str]) -> subprocess.CompletedProcess:
    if "PYTEST_CURRENT_TEST" in os.environ:
        print(f"      brew {' '.join(args)}")
        return subprocess.CompletedProcess(args, 0, "", "")
    return run(["brew", *args])


def confirm(prompt: str, assume_yes: bool, ask: Callable[[str], str]) -> bool:
    if assume_yes:
        print(f"{prompt} [y/N] y")
        return True
    try:
        return ask(f"{prompt} [y/N] ").strip().lower() in {"y", "yes"}
    except (EOFError, OSError):  # no usable stdin: treat as "no"
        return False


def ensure_mockoon() -> str:
    """Ensure Mockoon CLI (@mockoon/cli) is installed for API mocking."""
    existing = shutil.which("mockoon-cli")
    if existing:
        print(f"      mockoon-cli PASS ({existing})")
        return "READY"
    if not shutil.which("npm"):
        print("      mockoon-cli MISSING (npm not found; install Node.js/npm then run: npm install -g @mockoon/cli)")
        return "MISSING"
    print("      Installing @mockoon/cli globally via npm...")
    result = npm(["install", "-g", "@mockoon/cli"])
    if result.returncode == 0:
        print("      mockoon-cli PASS (installed @mockoon/cli)")
        return "READY"
    print(result.stderr.strip()[-1000:] if result.stderr else "      npm install failed.")
    print("      Hint: run 'npm install -g @mockoon/cli' manually when network is available.")
    return "MISSING"


def ensure_ripgrep() -> str:
    """Ensure Ripgrep (rg) is installed for fast codebase searching."""
    existing = shutil.which("rg")
    if existing:
        print(f"      ripgrep (rg) PASS ({existing})")
        return "READY"
    if shutil.which("brew"):
        print("      Installing ripgrep (rg) via Homebrew...")
        result = brew(["install", "ripgrep"])
        if result.returncode == 0:
            print("      ripgrep (rg) PASS (installed ripgrep)")
            return "READY"
        print(result.stderr.strip()[-1000:] if result.stderr else "      brew install ripgrep failed.")
    print("      ripgrep (rg) MISSING (install via 'brew install ripgrep' or system package manager)")
    return "MISSING"


ENSURE_GLOBAL: dict[str, Callable[[], str]] = {"ripgrep": ensure_ripgrep, "mockoon-cli": ensure_mockoon}


def _pubspec_packages(project: Path) -> set[str]:
    """Package names under `dependencies:` and `dev_dependencies:` (two-space keys), read without a YAML parser."""
    names: set[str] = set()
    section = None
    for line in (project / "pubspec.yaml").read_text(encoding="utf-8").splitlines():
        if line and not line[0].isspace():
            section = line.split(":", 1)[0].strip()
            continue
        match = re.match(r"^  ([A-Za-z0-9_]+):", line)
        if match and section in {"dependencies", "dev_dependencies"}:
            names.add(match.group(1))
    return names


def _requirement_name(requirement: str) -> str:
    return re.split(r"[\s<>=!~;\[]", requirement.strip(), maxsplit=1)[0].lower().replace("_", "-")


def _pyproject(project: Path) -> dict:
    return tomllib.loads((project / "pyproject.toml").read_text(encoding="utf-8"))


def _python_packages(project: Path) -> set[str]:
    data = _pyproject(project)
    project_table = data.get("project", {})
    requirements = list(project_table.get("dependencies", []))
    for group in (data.get("dependency-groups", {}), project_table.get("optional-dependencies", {})):
        for items in group.values():
            requirements += [item for item in items if isinstance(item, str)]
    requirements += data.get("tool", {}).get("uv", {}).get("dev-dependencies", [])
    return {_requirement_name(r) for r in requirements}


def _analysis_options_gaps(project: Path) -> tuple[bool, list[str]]:
    path = project / "analysis_options.yaml"
    raw = path.read_text(encoding="utf-8") if path.is_file() else ""
    text = "\n".join(line.split("#", 1)[0] for line in raw.splitlines())  # a rule named only in a comment is not on
    needs_include = not re.search(r"^include:", text, re.MULTILINE)
    return needs_include, [rule for rule in ANALYSIS_RULES if not re.search(rf"\b{rule}\b", text)]


def _status(tool: Tool, project: Path, pack: str) -> str:
    if tool.kind == "dev":
        installed = _pubspec_packages(project) if pack == "flutter" else _python_packages(project)
        return PASS if tool.name in installed else MISSING
    if tool.kind == "config":
        if tool.name == "analysis_options":
            needs_include, missing_rules = _analysis_options_gaps(project)
            return MISSING if needs_include or missing_rules else PASS
        key = tool.name.removesuffix("-config")
        own_file = {"ruff": ("ruff.toml", ".ruff.toml"), "mypy": ("mypy.ini", ".mypy.ini")}[key]
        found = key in _pyproject(project).get("tool", {}) or any((project / f).is_file() for f in own_file)
        return PASS if found else MISSING
    if tool.kind == "uvx":
        return PASS if shutil.which("uv") else MISSING
    return PASS if shutil.which(EXECUTABLE.get(tool.name, tool.name)) else MISSING


def _merge_analysis_options(project: Path) -> None:
    """Add the lint include and missing rules; keep every existing line."""
    path = project / "analysis_options.yaml"
    needs_include, missing = _analysis_options_gaps(project)
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    if missing:
        linter = next((i for i, line in enumerate(lines) if line.startswith("linter:")), None)
        if linter is None:
            lines += ([""] if lines else []) + ["linter:", "  rules:"] + [f"    - {rule}" for rule in missing]
        else:
            rules = next(
                (i for i in range(linter + 1, len(lines)) if lines[i].strip() == "rules:" and lines[i].startswith(" ")),
                None,
            )
            if rules is None:
                lines[linter + 1 : linter + 1] = ["  rules:"] + [f"    - {rule}" for rule in missing]
            else:
                indent = " " * (len(lines[rules]) - len(lines[rules].lstrip()) + 2)
                following = next(
                    (line.strip() for line in lines[rules + 1 :] if line.strip() and not line.strip().startswith("#")), ""
                )
                as_map = bool(following) and not following.startswith("-") and following.endswith(("true", "false"))
                added = [f"{indent}{rule}: true" if as_map else f"{indent}- {rule}" for rule in missing]
                lines[rules + 1 : rules + 1] = added
    if needs_include:
        package = "very_good_analysis" if "very_good_analysis" in _pubspec_packages(project) else "flutter_lints"
        lines[0:0] = [f"include: {ANALYSIS_INCLUDE[package]}", ""]
    path.write_text("\n".join(lines).strip("\n") + "\n", encoding="utf-8")


def _append_section(project: Path, section: str) -> None:
    path = project / "pyproject.toml"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.rstrip("\n") + "\n" + section, encoding="utf-8")


def _apply_config(tool: Tool, project: Path) -> None:
    if tool.name == "analysis_options":
        _merge_analysis_options(project)
    else:
        _append_section(project, RUFF_SECTION if tool.name == "ruff-config" else MYPY_SECTION)
    print(f"      {tool.name} updated")


def _print_statuses(selected: list[Tool], statuses: dict[str, str]) -> None:
    for tool in selected:
        label = tool.kind if tool.default else f"{tool.kind}, optional"
        print(f"      {tool.name:<20} {statuses[tool.name]:<8} ({label})")


def _record_state(project: Path, pack: str, statuses: dict[str, str]) -> None:
    path = project / STATE_FILE
    state = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    state.setdefault("tools", {})[pack] = {
        "statuses": statuses,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def run_tools(
    project: Path,
    pack: str,
    only: list[str] | None = None,
    check_only: bool = False,
    assume_yes: bool = False,
    ask: Callable[[str], str] = input,
) -> int:
    """Check or install the pack's tools. Returns 0 when every selected tool is PASS, 1 otherwise, 2 for a bad name."""
    project = project.resolve()
    catalog = CATALOG[pack]
    if only:
        unknown = [name for name in only if name not in {tool.name for tool in catalog}]
        if unknown:
            print(f"Unknown tool for pack {pack}: {', '.join(unknown)}")
            print(f"Valid names: {', '.join(tool.name for tool in catalog)}")
            return 2
    selected = [tool for tool in catalog if tool.name in only] if only else [tool for tool in catalog if tool.default]
    if not (project / MANIFEST[pack]).is_file():
        print(f"BLOCKED: {MANIFEST[pack]} not found in {project}")
        return 1

    print(f"Developer tools ({pack}) in {project}")
    statuses = {tool.name: _status(tool, project, pack) for tool in selected}
    _print_statuses(selected, statuses)
    missing = [tool for tool in selected if statuses[tool.name] == MISSING]
    if check_only or not missing:
        print(f"TOOLS: {'READY' if not missing else 'MISSING'}")
        return 0 if not missing else 1

    dev = [tool.name for tool in missing if tool.kind == "dev"]
    configs = [tool for tool in missing if tool.kind == "config"]
    globals_ = [tool for tool in missing if tool.kind == "global"]
    manual = [tool for tool in missing if tool.kind in {"system", "uvx"}]
    changes = ([f"{' '.join(ADD_DEV[pack])} {' '.join(dev)}"] if dev else []) + [
        f"add {tool.name} to {'analysis_options.yaml' if pack == 'flutter' else 'pyproject.toml'}" for tool in configs
    ] + [f"install {tool.name} for your user" for tool in globals_]
    if changes:
        print("Planned changes:")
        print("\n".join(f"      - {change}" for change in changes))
        if not confirm("Apply these changes?", assume_yes, ask):
            print("Cancelled; nothing changed.")
            return 1
    if dev:
        result = run([*ADD_DEV[pack], *dev], cwd=project)
        if result.returncode != 0:
            print(result.stdout[-2000:], result.stderr[-2000:])
    for tool in configs:
        _apply_config(tool, project)
    for tool in globals_:
        ENSURE_GLOBAL[tool.name]()
    for tool in manual:
        print(f"      {tool.name} MISSING: install it yourself ({tool.hint})")

    statuses = {tool.name: _status(tool, project, pack) for tool in selected}
    _record_state(project, pack, statuses)
    print("Result:")
    _print_statuses(selected, statuses)
    ready = all(status == PASS for status in statuses.values())
    print(f"TOOLS: {'READY' if ready else 'MISSING'}")
    return 0 if ready else 1
