"""Offline checks for `coder-nexus setup tools` (no network, no SDK: every external command is faked)."""

import subprocess
from pathlib import Path

import pytest

from coder_nexus.setup import tools


@pytest.fixture
def all_on_path(monkeypatch):
    monkeypatch.setattr(tools.shutil, "which", lambda cmd: f"/usr/bin/{cmd}")


@pytest.fixture
def commands(monkeypatch):
    """Record external commands; `flutter pub add --dev` and `uv add --dev` update the manifest like the real tools."""
    seen: list[list[str]] = []

    def fake(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
        seen.append(cmd)
        if cmd[:4] == ["flutter", "pub", "add", "--dev"]:
            pubspec = cwd / "pubspec.yaml"
            text = pubspec.read_text(encoding="utf-8")
            if "dev_dependencies:" not in text:
                text += "\ndev_dependencies:\n"
            pubspec.write_text(text + "".join(f"  {name}: ^1.0.0\n" for name in cmd[4:]), encoding="utf-8")
        if cmd[:3] == ["uv", "add", "--dev"]:
            pyproject = cwd / "pyproject.toml"
            added = "".join(f'"{name}", ' for name in cmd[3:])
            pyproject.write_text(pyproject.read_text(encoding="utf-8").replace("dev = [", f"dev = [{added}", 1), encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(tools, "run", fake)
    return seen


def _flutter_project(tmp_path: Path, dev: str = "") -> Path:
    (tmp_path / "pubspec.yaml").write_text(
        "name: demo\n\ndependencies:\n  flutter:\n    sdk: flutter\n\ndev_dependencies:\n  flutter_test:\n    sdk: flutter\n" + dev,
        encoding="utf-8",
    )
    return tmp_path


def _backend_project(tmp_path: Path, extra: str = "") -> Path:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "svc"\nversion = "0.1.0"\n\n[dependency-groups]\ndev = ["pytest>=8"]\n' + extra,
        encoding="utf-8",
    )
    return tmp_path


def _snapshot(folder: Path) -> dict[str, str]:
    return {p.name: p.read_text(encoding="utf-8") for p in folder.iterdir() if p.is_file()}


def test_catalog_defaults_and_optional_tools():
    flutter_dev = {t.name for t in tools.CATALOG["flutter"] if t.kind == "dev" and t.default}
    assert flutter_dev == {"flutter_lints", "mocktail", "bloc_test", "very_good_analysis", "dart_code_linter"}
    assert all(t.default for t in tools.CATALOG["flutter"])
    backend_dev = {t.name for t in tools.CATALOG["backend"] if t.kind == "dev" and t.default}
    assert backend_dev == {"pytest", "pytest-asyncio", "ruff", "mypy", "pytest-cov", "import-linter", "pytest-alembic", "pytest-randomly"}
    assert all(t.default for t in tools.CATALOG["backend"])


def test_check_is_read_only_and_reports_missing(tmp_path, all_on_path, commands, capsys):
    project = _flutter_project(tmp_path, "  mocktail: ^1.0.0\n")
    before = _snapshot(project)
    assert tools.run_tools(project, "flutter", check_only=True) == 1
    out = capsys.readouterr().out
    assert "mocktail" in out and "PASS" in out
    assert "flutter_lints" in out and "MISSING" in out
    assert _snapshot(project) == before
    assert commands == []


def test_unknown_only_name_is_rejected_with_valid_names(tmp_path, capsys):
    project = _flutter_project(tmp_path)
    assert tools.run_tools(project, "flutter", only=["ruff"], check_only=True) == 2
    out = capsys.readouterr().out
    assert "ruff" in out and "mocktail" in out


def test_flutter_install_adds_missing_dev_deps_and_analysis_options(tmp_path, all_on_path, commands):
    project = _flutter_project(tmp_path, "  mocktail: ^1.0.0\n")
    assert tools.run_tools(project, "flutter", assume_yes=True) == 0
    assert ["flutter", "pub", "add", "--dev", "flutter_lints", "bloc_test", "very_good_analysis", "dart_code_linter"] in commands
    options = (project / "analysis_options.yaml").read_text(encoding="utf-8")
    assert "include: package:very_good_analysis/analysis_options.yaml" in options
    for rule in ("avoid_print", "prefer_const_constructors", "cancel_subscriptions", "close_sinks", "empty_catches"):
        assert rule in options
    after_first = _snapshot(project)
    commands.clear()
    assert tools.run_tools(project, "flutter", assume_yes=True) == 0
    assert not [c for c in commands if c[:2] == ["flutter", "pub"]]
    assert _snapshot(project) == after_first


def test_existing_analysis_options_are_kept_and_only_completed(tmp_path, all_on_path, commands):
    project = _flutter_project(tmp_path, "  flutter_lints: ^5.0.0\n  mocktail: ^1.0.0\n  bloc_test: ^9.0.0\n  very_good_analysis: ^6.0.0\n  dart_code_linter: ^1.0.0\n")
    (project / "analysis_options.yaml").write_text(
        "include: package:very_good_analysis/analysis_options.yaml\n\nlinter:\n  rules:\n    - avoid_print\n",
        encoding="utf-8",
    )
    assert tools.run_tools(project, "flutter", assume_yes=True) == 0
    options = (project / "analysis_options.yaml").read_text(encoding="utf-8")
    assert options.startswith("include: package:very_good_analysis/analysis_options.yaml\n")
    assert "flutter_lints/flutter.yaml" not in options
    assert options.count("avoid_print") == 1
    assert "    - close_sinks\n" in options


def test_rules_named_only_in_comments_are_added(tmp_path, all_on_path, commands):
    """The `flutter create` template lists rules as comments; those are not enabled."""
    project = _flutter_project(tmp_path, "  flutter_lints: ^5.0.0\n  mocktail: ^1.0.0\n  bloc_test: ^9.0.0\n  very_good_analysis: ^6.0.0\n  dart_code_linter: ^1.0.0\n")
    (project / "analysis_options.yaml").write_text(
        "include: package:flutter_lints/flutter.yaml\n\nlinter:\n  rules:\n"
        "    # avoid_print: false  # Uncomment to disable the `avoid_print` rule\n"
        "    # prefer_single_quotes: true  # Uncomment to enable the `prefer_single_quotes` rule\n",
        encoding="utf-8",
    )
    assert tools.run_tools(project, "flutter", assume_yes=True) == 0
    options = (project / "analysis_options.yaml").read_text(encoding="utf-8")
    assert "    - avoid_print\n" in options and "# avoid_print: false" in options
    assert "    - empty_catches\n" in options


def test_backend_install_adds_missing_dev_deps_and_tool_sections(tmp_path, all_on_path, commands):
    project = _backend_project(tmp_path, '\n[tool.mypy]\nstrict = true\n')
    assert tools.run_tools(project, "backend", assume_yes=True) == 0
    assert ["uv", "add", "--dev", "pytest-asyncio", "ruff", "mypy", "pytest-cov", "import-linter", "pytest-alembic", "pytest-randomly"] in commands
    pyproject = (project / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.ruff.lint]" in pyproject
    assert pyproject.count("[tool.mypy]") == 1 and "strict = true" in pyproject


def test_only_selects_optional_tools(tmp_path, all_on_path, commands):
    project = _backend_project(tmp_path)
    assert tools.run_tools(project, "backend", only=["pytest-cov"], assume_yes=True) == 0
    assert commands == [["uv", "add", "--dev", "pytest-cov"]]


def test_declined_confirmation_changes_nothing(tmp_path, all_on_path, commands):
    project = _flutter_project(tmp_path)
    before = _snapshot(project)
    assert tools.run_tools(project, "flutter", ask=lambda _: "n") == 1
    assert commands == []
    assert _snapshot(project) == before


def test_missing_system_tool_prints_install_hint_and_never_installs(tmp_path, monkeypatch, commands, capsys):
    monkeypatch.setattr(tools.shutil, "which", lambda cmd: None if cmd == "docker" else f"/usr/bin/{cmd}")
    project = _backend_project(tmp_path)
    assert tools.run_tools(project, "backend", only=["docker"], assume_yes=True) == 1
    assert "docker" in capsys.readouterr().out
    assert commands == []


def test_cli_parses_setup_tools(monkeypatch, tmp_path):
    from coder_nexus import cli

    received = {}

    def fake_run_tools(project, pack, only=None, check_only=False, assume_yes=False):
        received.update(project=project, pack=pack, only=only, check_only=check_only, assume_yes=assume_yes)
        return 0

    monkeypatch.setattr(tools, "run_tools", fake_run_tools)
    monkeypatch.setattr("sys.argv", ["coder-nexus", "setup", "tools", "--pack", "backend", "--only", "ruff,mypy", "--check", "--project", str(tmp_path)])
    assert cli.main() == 0
    assert received == {"project": tmp_path.resolve(), "pack": "backend", "only": ["ruff", "mypy"], "check_only": True, "assume_yes": False}


def test_ensure_mockoon_installs_via_npm_when_missing(monkeypatch):
    monkeypatch.setattr(tools.shutil, "which", lambda cmd: "/usr/bin/npm" if cmd == "npm" else None)
    called_args = []

    def fake_npm(args):
        called_args.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(tools, "npm", fake_npm)
    assert tools.ensure_mockoon() == "READY"
    assert called_args == [["install", "-g", "@mockoon/cli"]]


def test_ensure_ripgrep_installs_via_brew_when_missing(monkeypatch):
    monkeypatch.setattr(tools.shutil, "which", lambda cmd: "/opt/homebrew/bin/brew" if cmd == "brew" else None)
    called_args = []

    def fake_brew(args):
        called_args.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(tools, "brew", fake_brew)
    assert tools.ensure_ripgrep() == "READY"
    assert called_args == [["install", "ripgrep"]]
