"""Offline checks for `coder-nexus setup flutter` (no network, no Flutter SDK)."""

import json
import subprocess
from pathlib import Path

import pytest

from coder_nexus.setup import flutter as sf


def _git(*args, cwd=None):
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *args], cwd=cwd, check=True, capture_output=True)


def _package(folder: Path, name: str) -> Path:
    folder.mkdir(parents=True)
    (folder / "pubspec.yaml").write_text(f"name: {name}\n", encoding="utf-8")
    return folder


def _bare_repo(tmp: Path, name: str) -> str:
    work = _package(tmp / "remotes" / f"{name}-work", name)
    _git("init", "-q", cwd=work)
    _git("add", ".", cwd=work)
    _git("commit", "-qm", "init", cwd=work)
    bare = tmp / "remotes" / f"{name}.git"
    _git("clone", "-q", "--bare", str(work), str(bare))
    return bare.as_uri()


def _fake_pub(project_root: Path):
    """Stand-in for `flutter pub add`: records path deps in package_config like pub does."""

    def fake(args, cwd):
        assert args[:2] == ["pub", "add"]
        packages = []
        for desc in args[2:]:
            if desc.startswith("override:"):
                continue
            name, rel = desc.split("@{path: ")
            packages.append({"name": name, "rootUri": "../" + rel.rstrip("}")})
        (cwd / "pubspec.yaml").write_text((cwd / "pubspec.yaml").read_text() + "\n".join(args[2:]) + "\n")
        (cwd / ".dart_tool").mkdir(exist_ok=True)
        (cwd / ".dart_tool" / "package_config.json").write_text(json.dumps({"packages": packages}))
        return subprocess.CompletedProcess(args, 0, "", "")

    return fake


def _no_flutter(args, cwd):
    raise AssertionError(f"flutter must not run: {args}")


@pytest.fixture
def project(tmp_path):
    return _package(tmp_path / "codebase" / "project_banking", "project_banking")


def _tree(root: Path):
    return sorted((str(p), p.read_bytes() if p.is_file() else b"") for p in root.rglob("*"))


@pytest.mark.parametrize(
    "stderr,kind",
    [
        ("git@git.example.com: Permission denied (publickey).", "publickey"),
        ("Please make sure you have the correct access rights", "publickey"),
        ("Host key verification failed.", "host_key"),
        ("fatal: could not read Username for 'https://git.example.com': terminal prompts disabled", "auth"),
        ("The requested URL returned error: 403", "auth"),
        ("ssh: Could not resolve hostname git.example.com", "network"),
        ("something else", "unknown"),
    ],
)
def test_classify_git_error(stderr, kind):
    assert sf.classify_git_error(stderr) == kind


def test_scan_matches_pubspec_name_not_folder(project):
    _package(project.parent / "core", "app_core")
    _package(project.parent / "app-util", "not_company")
    assert sf.scan_siblings(project) == {"app_core": project.parent / "core"}


def test_missing_app_core_declined_blocks_without_writes(project, monkeypatch):
    monkeypatch.setattr(sf, "flutter", _no_flutter)
    before = _tree(project.parent)
    assert sf.run_setup(project, ask=lambda _: "n") == 1
    assert _tree(project.parent) == before


def test_clone_then_ready_and_check_is_read_only(project, tmp_path, monkeypatch):
    for name, (folder, _, _) in list(sf.REPOS.items()):
        url = _bare_repo(tmp_path, name)
        monkeypatch.setitem(sf.REPOS, name, (folder, url, url))
    monkeypatch.setattr(sf, "flutter", _fake_pub(project))

    assert sf.run_setup(project, assume_yes=True) == 0
    state = json.loads((project / sf.STATE_FILE).read_text())
    assert state["status"] == "READY"
    assert set(state["packages"]) == {"app_core", "app_util", "app_ui_kit"}
    assert "override:app_core@{path: ../app-core}" in (project / "pubspec.yaml").read_text()

    monkeypatch.setattr(sf, "flutter", _no_flutter)
    before = _tree(project.parent)
    assert sf.run_setup(project, check_only=True) == 0
    assert _tree(project.parent) == before


def test_check_blocks_when_pub_not_resolved_to_sibling(project):
    _package(project.parent / "app-core", "app_core")
    assert sf.check(project)[0] == "BLOCKED"


def test_clone_failure_prints_guide_and_blocks(project, tmp_path, monkeypatch, capsys):
    missing = (tmp_path / "nope.git").as_uri()
    monkeypatch.setitem(sf.REPOS, "app_core", ("app-core", missing, missing))
    monkeypatch.setattr(sf, "flutter", _no_flutter)
    assert sf.run_setup(project, assume_yes=True) == 1
    assert "BLOCKED: missing required package 'app_core'" in capsys.readouterr().out
    assert not (project.parent / "app-core").exists()


@pytest.mark.parametrize(
    "folder_name,expected_pkg_name",
    [
        ("banking-app-demo", "banking_app_demo"),
        ("banking_app_demo", "banking_app_demo"),
        ("My-Banking-App", "my_banking_app"),
        ("123banking", "app_123banking"),
        ("class", "app_class"),
        ("default", "app_default"),
        ("app-core-test-1", "app_core_test_1"),
        ("---", "app"),
        ("", "app"),
    ],
)
def test_dart_package_name_sanitization(folder_name, expected_pkg_name):
    assert sf.dart_package_name(folder_name) == expected_pkg_name


def test_normalize_profile():
    assert sf.normalize_profile("1") == "imespro"
    assert sf.normalize_profile("imespro") == "imespro"
    assert sf.normalize_profile("2") == "external-structured"
    assert sf.normalize_profile("external-structured") == "external-structured"
    assert sf.normalize_profile("3") == "external-standard"
    assert sf.normalize_profile("external-standard") == "external-standard"
    assert sf.normalize_profile("invalid") is None
    assert sf.normalize_profile(None) is None


def test_prompt_profile():
    assert sf.prompt_profile(lambda _: "1") == "imespro"
    assert sf.prompt_profile(lambda _: "2") == "external-structured"
    assert sf.prompt_profile(lambda _: "3") == "external-standard"
    assert sf.prompt_profile(lambda _: "external-structured") == "external-structured"
    assert sf.prompt_profile(lambda _: "unknown") == "imespro"


def test_setup_external_structured_profile(project, monkeypatch):
    (project / "lib" / "core").mkdir(parents=True)

    def fake_flutter(args, cwd):
        assert args == ["pub", "get"]
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(sf, "flutter", fake_flutter)
    assert sf.run_setup(project, profile="external-structured") == 0
    state = json.loads((project / sf.STATE_FILE).read_text())
    assert state["status"] == "READY"
    assert state["profile"] == "external-structured"
    assert state["packages"] == {}
    status, lines = sf.check(project, profile="external-structured")
    assert status == "READY"
    assert any("client foundations" in l and "PASS" in l for l in lines)


def test_setup_external_standard_profile(project, monkeypatch):
    def fake_flutter(args, cwd):
        assert args == ["pub", "get"]
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(sf, "flutter", fake_flutter)
    assert sf.run_setup(project, profile="external-standard") == 0
    state = json.loads((project / sf.STATE_FILE).read_text())
    assert state["status"] == "READY"
    assert state["profile"] == "external-standard"
    assert state["packages"] == {}
    status, lines = sf.check(project, profile="external-standard")
    assert status == "READY"
    assert any("standard flutter structure | PASS" in l for l in lines)


def test_setup_interactive_profile_prompt(project, monkeypatch):
    (project / "lib" / "core").mkdir(parents=True)

    def fake_flutter(args, cwd):
        assert args == ["pub", "get"]
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(sf, "flutter", fake_flutter)
    assert sf.run_setup(project, ask=lambda _: "2") == 0
    state = json.loads((project / sf.STATE_FILE).read_text())
    assert state["profile"] == "external-structured"


def test_create_project_sanitizes_hyphenated_folder_name(tmp_path, monkeypatch):
    project = tmp_path / "banking-app-demo"
    project.mkdir()

    captured_args = []

    def mock_flutter(args, cwd):
        captured_args.append(args)
        # Create minimal pubspec so create_project creates lib dirs
        (cwd / project.name / "lib").mkdir(parents=True, exist_ok=True)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(sf, "flutter", mock_flutter)

    assert sf.create_project(project) is True
    assert any("--project-name" in a and "banking_app_demo" in a for a in captured_args)
    for sub in sf.LIB_DIRS:
        assert (project / "lib" / sub).is_dir()
        assert (project / "lib" / sub / ".gitkeep").is_file()


def test_full_setup_flow_with_kebab_case_folder(tmp_path, monkeypatch):
    root = tmp_path / "workspace"
    project = root / "examples" / "banking-app-demo"
    project.mkdir(parents=True)

    for name, (folder, _, _) in list(sf.REPOS.items()):
        url = _bare_repo(tmp_path, name)
        monkeypatch.setitem(sf.REPOS, name, (folder, url, url))

    def fake_flutter(args, cwd):
        if args[0] == "create":
            # Emulate flutter create
            (cwd / "banking-app-demo" / "pubspec.yaml").write_text("name: banking_app_demo\n", encoding="utf-8")
            (cwd / "banking-app-demo" / "lib").mkdir(parents=True, exist_ok=True)
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[:2] == ["pub", "add"]:
            packages = []
            for desc in args[2:]:
                if desc.startswith("override:"):
                    continue
                name, rel = desc.split("@{path: ")
                packages.append({"name": name, "rootUri": "file://" + str((cwd / rel.rstrip("}")).resolve())})
            (cwd / "pubspec.yaml").write_text((cwd / "pubspec.yaml").read_text() + "\n".join(args[2:]) + "\n")
            (cwd / ".dart_tool").mkdir(exist_ok=True)
            (cwd / ".dart_tool" / "package_config.json").write_text(json.dumps({"packages": packages}))
            return subprocess.CompletedProcess(args, 0, "", "")
        raise AssertionError(f"Unexpected flutter invocation: {args}")

    monkeypatch.setattr(sf, "flutter", fake_flutter)

    # Run full setup flow answering yes
    ret = sf.run_setup(project, assume_yes=True)
    assert ret == 0

    # Verify pubspec has relative path dependencies pointing to sibling packages
    pubspec = (project / "pubspec.yaml").read_text(encoding="utf-8")
    assert "override:app_core@{path: ../app-core}" in pubspec
    assert "override:app_util@{path: ../app-util}" in pubspec
    assert "override:app_ui_kit@{path: ../app-ui-kit}" in pubspec

    # Verify state file
    state_file = project / sf.STATE_FILE
    assert state_file.is_file()
    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["status"] == "READY"
    assert state["profile"] == "imespro"
    assert state["packages"]["app_core"]["path"] == "../app-core"

    # Verify read-only check
    status, lines = sf.check(project)
    assert status == "READY"
    assert any("app_core" in l and "pub PASS" in l for l in lines)


def test_ensure_mockoon_installs_via_npm_when_missing(monkeypatch):
    monkeypatch.setattr(sf.shutil, "which", lambda cmd: "/usr/bin/npm" if cmd == "npm" else None)
    called_args = []

    def fake_npm(args):
        called_args.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(sf, "npm", fake_npm)
    assert sf.ensure_mockoon() == "READY"
    assert called_args == [["install", "-g", "@mockoon/cli"]]


def test_ensure_ripgrep_installs_via_brew_when_missing(monkeypatch):
    monkeypatch.setattr(sf.shutil, "which", lambda cmd: "/opt/homebrew/bin/brew" if cmd == "brew" else None)
    called_args = []

    def fake_brew(args):
        called_args.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(sf, "brew", fake_brew)
    assert sf.ensure_ripgrep() == "READY"
    assert called_args == [["install", "ripgrep"]]


@pytest.mark.parametrize(
    "base",
    ["ssh://git@git.example.com/group", "git@git.example.com:group", "https://git.example.com/group/"],
)
def test_core_urls_from_env(monkeypatch, base):
    monkeypatch.setenv(sf.CORE_GIT_ENV, base)
    assert sf._core_urls("app-core") == (
        "ssh://git@git.example.com/group/app-core.git",
        "https://git.example.com/group/app-core.git",
    )


def test_clone_without_core_git_env_blocks(project, monkeypatch, capsys):
    monkeypatch.setitem(sf.REPOS, "app_core", ("app-core", "", ""))
    assert sf.clone("app_core", project, "ssh") is False
    assert sf.CORE_GIT_ENV in capsys.readouterr().out
