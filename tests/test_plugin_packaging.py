"""Tests for Antigravity plugin packaging, manifest, and installation."""

import argparse
import json
from pathlib import Path
import re
import shutil
import tempfile
import pytest

from coder_nexus.plugin_install import _install_plugin_projection, cmd_install_plugin

from .rendered import flutter_workspace, rendered_agent


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = REPO_ROOT / "plugins"


def test_plugin_json_structure():
    """Verify plugin.json exists, is valid JSON, and contains expected metadata."""
    manifest_file = PLUGIN_DIR / "core" / "plugin.json"
    assert manifest_file.exists(), f"Missing plugin.json at {manifest_file}"

    with open(manifest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("name") in {"coder-nexus-fe", "coder-nexus"}
    assert data.get("$schema") == "https://antigravity.google/schemas/v1/plugin.json"
    assert "description" in data
    assert set(data) == {"$schema", "name", "description"}


def test_extension_sync_requires_an_explicit_command():
    source = (REPO_ROOT / "extension.js").read_text(encoding="utf-8")
    activation = source.split("function activate(context) {", 1)[1].split("function deactivate()", 1)[0]
    assert "installAntigravityPlugin(context, null, true)" not in activation
    assert "registerCommand('coder-nexus.installWorkspace'" in activation
    assert "registerCommand('coder-nexus.installWorkspaceFlutter'" in activation
    assert "registerCommand('coder-nexus.installWorkspaceBE'" in activation
    assert "registerCommand('coder-nexus.installWorkspaceFE'" in activation
    assert "registerCommand('coder-nexus.installGlobal'" in activation
    assert "registerCommand('coder-nexus.showArchitecture'" in activation
    assert (REPO_ROOT / "media" / "architecture.html").exists()
    assert "frappe" not in source.lower(), "the Frappe pack was removed in 3.2.0"
    commands = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))["contributes"]["commands"]
    assert not [c for c in commands if "frappe" in json.dumps(c).lower()]


def test_bundle_manifest_inventory():
    manifest = json.loads((PLUGIN_DIR / "core" / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert bool(re.match(r"^\d+\.\d+\.\d+", manifest["plugin_version"]))
    if (REPO_ROOT / "package.json").exists():
        pkg = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
        assert manifest["plugin_version"] == pkg.get("version")
    assert manifest["hub_version"] == "0.1.0"
    assert manifest["resource_base"] == "plugins/"
    assert "flutter/verification" in manifest["public_skills"]
    assert len(manifest["mcp_tools"]) == 9
    packaged_skills = {f"core/{p.parent.name}" for p in (PLUGIN_DIR / "core" / "skills").glob("*/SKILL.md")}
    packaged_skills |= {f"{p.parent.parent.parent.name}/{p.parent.name}" for p in (PLUGIN_DIR / "packs").glob("*/skills/*/SKILL.md")}
    assert set(manifest["public_skills"]) == packaged_skills
    for resource in manifest["required_resources"]:
        assert (PLUGIN_DIR / resource).exists(), f"Missing bundle resource: {resource}"


def test_canonical_bundle_has_no_author_machine_path():
    offenders = []
    for path in (p for p in PLUGIN_DIR.rglob("*") if "dist" not in p.relative_to(PLUGIN_DIR).parts):
        if path.is_file() and path.suffix in {".json", ".md", ".tpl"}:
            content = path.read_text(encoding="utf-8")
            if "/Users/" in content:
                offenders.append(str(path.relative_to(PLUGIN_DIR)))
    assert offenders == []


def test_mcp_config_structure():
    """Verify the canonical config is portable and delegates to the installed CLI."""
    config_file = PLUGIN_DIR / "core" / "mcp_config.json"
    assert config_file.exists(), f"Missing mcp_config.json at {config_file}"

    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "mcpServers" in data
    assert "coder-nexus" in data["mcpServers"]
    server_cfg = data["mcpServers"]["coder-nexus"]
    assert server_cfg == {"command": "coder-nexus", "args": ["serve"]}
    assert "/Users/" not in config_file.read_text(encoding="utf-8")


def test_skill_markdown_structure():
    """Verify huly-task-intake SKILL.md has valid frontmatter and core instructions."""
    skill_file = PLUGIN_DIR / "core" / "skills" / "huly-task-intake" / "SKILL.md"
    assert skill_file.exists(), f"Missing SKILL.md at {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---")
    assert "name: huly-task-intake" in content
    assert "description:" in content
    # Verify core guidance references
    assert "huly_get_my_tasks" in content
    assert "huly_get_task_detail" in content
    assert "Read-Only" in content
    assert "Zero Mock Data" in content

def test_flutter_clean_architecture_skill_structure():
    """Verify flutter-clean-architecture SKILL.md, references, and manifest."""
    skill_dir = PLUGIN_DIR / "packs" / "flutter" / "skills" / "clean-architecture"
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists(), f"Missing SKILL.md at {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---")
    assert "name: clean-architecture" in content
    assert "description:" in content
    assert "get_project_structure" in content

    # Check references
    ref_dir = skill_dir / "references"
    assert (ref_dir / "manifest.json").exists()
    assert (ref_dir / "01_project_root.md").exists()
    assert (ref_dir / "02_core_subsystem.md").exists()
    assert (ref_dir / "03_feature_module.md").exists()
    assert (ref_dir / "04_cross_boundaries.md").exists()
    assert (ref_dir / "05_screen_contract.md").exists()


def test_client_workflow_skills_are_packaged_and_portable():
    """Verify public workflow skills ship in the plugin without author-machine links."""
    expected = {
        "requirements-elicitation",
        "grilling",
        "implementation-planning",
        "incremental-implementation",
        "clean-code",
        "code-simplification",
        "visual-quality",
        "verification",
        "code-review",
    }
    for name in expected:
        skill_file = next(iter([*(PLUGIN_DIR / "core" / "skills").glob(f"{name}/SKILL.md"), *(PLUGIN_DIR / "packs").glob(f"*/skills/{name}/SKILL.md")]), PLUGIN_DIR / "missing" / name)
        assert skill_file.exists(), f"Missing packaged skill: {name}"
        content = skill_file.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert f"name: {name}" in content
        assert "file:///Users/" not in content

    runtime_skill_files = [*(PLUGIN_DIR / "core").glob("**/*.md"), *(PLUGIN_DIR / "packs").glob("**/*.md")]
    author_paths = [
        str(path.relative_to(PLUGIN_DIR))
        for path in runtime_skill_files
        if "file:///Users/" in path.read_text(encoding="utf-8")
    ]
    assert author_paths == []


def test_clean_architecture_templates_exist_and_adhere_to_contracts():
    """Verify all 11 starter templates exist and strictly adhere to Senior contracts."""
    tpl_dir = PLUGIN_DIR / "packs" / "flutter" / "skills" / "clean-architecture" / "templates"
    expected_templates = [
        tpl_dir / "domain" / "entity.dart.tpl",
        tpl_dir / "domain" / "repository.dart.tpl",
        tpl_dir / "domain" / "usecase.dart.tpl",
        tpl_dir / "data" / "data_source.dart.tpl",
        tpl_dir / "data" / "model.dart.tpl",
        tpl_dir / "data" / "mapper.dart.tpl",
        tpl_dir / "data" / "repo_impl.dart.tpl",
        tpl_dir / "presentation" / "state.dart.tpl",
        tpl_dir / "presentation" / "cubit.dart.tpl",
        tpl_dir / "presentation" / "screen.dart.tpl",
        tpl_dir / "di" / "module_di.dart.tpl",
    ]
    for tpl in expected_templates:
        assert tpl.exists(), f"Missing template: {tpl}"

    # 1. Verify repo_impl wraps return with DataSuccess and avoids silent empty list fallback
    repo_impl_content = (tpl_dir / "data" / "repo_impl.dart.tpl").read_text(encoding="utf-8")
    assert "DataSuccess(" in repo_impl_content
    assert "DataFailure(" in repo_impl_content
    assert "return mapper.toEntities(" not in repo_impl_content
    assert "return <{{PascalCaseFeature}}Entity>[];" not in repo_impl_content

    # 2. Verify model does not use fake hardcoded fallbacks
    model_content = (tpl_dir / "data" / "model.dart.tpl").read_text(encoding="utf-8")
    assert "FormatException" in model_content
    assert "?? ''" not in model_content
    assert "?? 'UNKNOWN'" not in model_content
    assert "DateTime.now()" not in model_content

    # 3. Verify module_di uses relative imports within feature module
    di_content = (tpl_dir / "di" / "module_di.dart.tpl").read_text(encoding="utf-8")
    assert "../data/" not in di_content
    assert "../domain/" not in di_content
    assert "'data/data_sources/" in di_content

    # 4. Verify screen template requires the resolved Client base contract.
    screen_content = (tpl_dir / "presentation" / "screen.dart.tpl").read_text(encoding="utf-8")
    assert "extends BaseScreen" in screen_content
    assert "extends BaseScreenState<" in screen_content
    assert "{{verified_screen_metadata_override}}" in screen_content
    assert "{{verified_create_state_override}}" in screen_content
    assert "{{verified_base_screen_import}}" in screen_content
    assert "BLOCKED" in screen_content
    assert "extends StatelessWidget" not in screen_content

    # 5. Verify manifest.json has commit_hash and 11 templates mapped
    manifest_file = PLUGIN_DIR / "packs" / "flutter" / "skills" / "clean-architecture" / "references" / "manifest.json"
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    assert "commit_hash" in manifest_data
    assert "templates" in manifest_data
    assert len(manifest_data["templates"]) == 11


def test_clean_architecture_rules_structure():
    """Verify clean_architecture_rules.md exists in plugin rules directory."""
    rule_file = PLUGIN_DIR / "packs" / "flutter" / "rules" / "clean_architecture_rules.md"
    assert rule_file.exists(), f"Missing rule file at {rule_file}"
    content = rule_file.read_text(encoding="utf-8")
    assert "Domain Layer" in content
    assert "Presentation Layer" in content
    assert "Module DI Order" in content
    assert "BaseScreenState" in content


def test_cli_install_plugin_workspace():
    """Verify workspace install creates an idempotent official plugin projection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        args = argparse.Namespace(
            is_global=False,
            workspace=tmpdir,
        )
        exit_code = cmd_install_plugin(args)
        assert exit_code == 0

        installed = Path(tmpdir) / ".agents" / "plugins" / "coder-nexus"
        assert installed.is_dir()
        assert not (installed / "agents").exists()
        assert (Path(tmpdir) / ".agents" / "agents" / "code_writer.md").is_file()
        stack = json.loads((Path(tmpdir) / ".agents" / "stack.json").read_text(encoding="utf-8"))
        assert [pack["stack"] for pack in stack["packs"]] == ["flutter"]
        projected = json.loads((installed / "bundle_manifest.json").read_text(encoding="utf-8"))
        for resource in projected["required_resources"]:
            assert (installed / resource).is_file(), resource
        metadata = json.loads((installed / "installed_version.json").read_text(encoding="utf-8"))
        manifest = json.loads((PLUGIN_DIR / "core" / "bundle_manifest.json").read_text(encoding="utf-8"))
        assert metadata["plugin_version"] == manifest["plugin_version"]
        assert metadata["source_path"] == str(REPO_ROOT)
        runtime = json.loads((installed / "mcp_config.json").read_text(encoding="utf-8"))
        server = runtime["mcpServers"]["coder-nexus"]
        assert server["command"] == "uv"
        assert server["args"] == ["run", "--offline", "coder-nexus", "serve"]
        assert server["cwd"] == str(REPO_ROOT)

        exit_code2 = cmd_install_plugin(args)
        assert exit_code2 == 0
        metadata2 = json.loads((installed / "installed_version.json").read_text(encoding="utf-8"))
        assert metadata2 == metadata


def test_cli_install_plugin_migrates_legacy_workspace_entry():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Path(tmpdir) / ".agents" / "plugins.json"
        config.parent.mkdir(parents=True)
        config.write_text(
            json.dumps({"entries": [{"path": str((PLUGIN_DIR / "coder-nexus-fe").resolve())}, {"path": "/other/plugin"}]}),
            encoding="utf-8",
        )
        args = argparse.Namespace(is_global=False, workspace=tmpdir)
        assert cmd_install_plugin(args) == 0
        data = json.loads(config.read_text(encoding="utf-8"))
        assert data == {"entries": [{"path": "/other/plugin"}]}


def test_cli_install_plugin_global_replaces_legacy_symlink(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        home = Path(tmpdir)
        legacy = home / ".gemini" / "config" / "plugins" / "coder-nexus-fe"
        legacy.parent.mkdir(parents=True)
        legacy.symlink_to(PLUGIN_DIR, target_is_directory=True)
        monkeypatch.setattr(Path, "home", lambda: home)

        args = argparse.Namespace(is_global=True, workspace=None)
        assert cmd_install_plugin(args) == 0
        assert not legacy.exists() and not legacy.is_symlink()
        destination = home / ".gemini" / "config" / "plugins" / "coder-nexus"
        assert destination.is_dir()
        assert (destination / "agents" / "code_writer.md").is_file()
        metadata = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
        manifest = json.loads((PLUGIN_DIR / "core" / "bundle_manifest.json").read_text(encoding="utf-8"))
        assert metadata["plugin_version"] == manifest["plugin_version"]


def test_install_projection_update_and_rollback_change_digest(tmp_path):
    plugins = tmp_path / "plugins"
    shutil.copytree(REPO_ROOT / "plugins", plugins, ignore=shutil.ignore_patterns("dist"))
    destination = tmp_path / "installed" / "coder-nexus"

    assert _install_plugin_projection("flutter", destination, REPO_ROOT, plugins_dir=plugins) == "installed"
    original = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
    skill = plugins / "packs" / "flutter" / "skills" / "verification" / "SKILL.md"
    original_skill = skill.read_text(encoding="utf-8")
    skill.write_text(original_skill + "\n", encoding="utf-8")
    assert _install_plugin_projection("flutter", destination, REPO_ROOT, plugins_dir=plugins) == "updated"
    changed = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
    assert changed["bundle_digest"] != original["bundle_digest"]

    skill.write_text(original_skill, encoding="utf-8")
    assert _install_plugin_projection("flutter", destination, REPO_ROOT, plugins_dir=plugins) == "updated"
    rolled_back = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
    assert rolled_back["bundle_digest"] == original["bundle_digest"]


@pytest.mark.parametrize("variant", ["flutter", "backend"])
def test_installed_projection_includes_shared_contract_and_valid_resource_paths(tmp_path, variant):
    destination = tmp_path / "plugin"
    _install_plugin_projection(variant, destination, REPO_ROOT)
    assert (destination / "shared_contracts/api_handshake_protocol.md").read_bytes() == (
        REPO_ROOT / "plugins/shared_contracts/api_handshake_protocol.md"
    ).read_bytes()
    manifest = json.loads((destination / "bundle_manifest.json").read_text())
    assert "shared_contracts/api_handshake_protocol.md" in manifest["required_resources"]
    for resource in manifest["required_resources"]:
        assert (destination / resource).is_file(), resource
    if variant == "flutter":
        for relative in ("skills/work-item-contract/SKILL.md", "rules/clean_architecture_rules.md"):
            document = destination / relative
            for link in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                assert (document.parent / link).is_file(), (relative, link)


def test_shared_contract_edit_and_framework_switch_refresh_projection(tmp_path):
    plugins = tmp_path / "plugins"
    shutil.copytree(REPO_ROOT / "plugins", plugins, ignore=shutil.ignore_patterns("dist"))
    destination = tmp_path / "installed"
    assert _install_plugin_projection("flutter", destination, REPO_ROOT, plugins_dir=plugins) == "installed"
    assert _install_plugin_projection("flutter", destination, REPO_ROOT, plugins_dir=plugins) == "unchanged"
    protocol = plugins / "shared_contracts" / "api_handshake_protocol.md"
    protocol.write_text(protocol.read_text() + "\nProtocol revision changed.\n")
    assert _install_plugin_projection("flutter", destination, REPO_ROOT, plugins_dir=plugins) == "updated"
    assert (destination / "shared_contracts/api_handshake_protocol.md").read_bytes() == protocol.read_bytes()
    assert _install_plugin_projection("backend", destination, REPO_ROOT, plugins_dir=plugins) == "updated"
    assert not (destination / "skills/flutter-core-package-usage").exists()
    assert (destination / "skills/backend-api-contract-design/SKILL.md").is_file()


def test_flutter_code_review_skill_structure():
    """Verify flutter-code-review SKILL.md, manifest, references, and review template."""
    skill_dir = PLUGIN_DIR / "packs" / "flutter" / "skills" / "code-review"
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists(), f"Missing SKILL.md at {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---")
    assert "name: code-review" in content
    assert "description:" in content
    assert "Five-Axis" in content
    assert "Two-Gate Protocol" in content
    assert "validate_architecture_code" in content
    assert "gate_status" in content
    assert "BASE_REVISION" in content
    assert "git diff HEAD~1" not in content
    assert "verification" in content

    # Check references and manifest
    ref_dir = skill_dir / "references"
    manifest_file = ref_dir / "manifest.json"
    assert manifest_file.exists(), f"Missing manifest.json at {manifest_file}"

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest.get("version") == "1.2.0"
    assert manifest.get("skill_name") == "flutter-code-review"
    assert len(manifest.get("five_axes", [])) == 5
    assert len(manifest.get("references", [])) == 3
    assert len(manifest.get("templates", [])) == 1

    assert (ref_dir / "01_five_axis_rubric.md").exists()
    assert (ref_dir / "02_rule_source_matrix.md").exists()
    assert (ref_dir / "03_cross_branch_checklist.md").exists()

    # Check template
    tpl_dir = skill_dir / "templates"
    report_tpl = tpl_dir / "code_review_report.md.tpl"
    assert report_tpl.exists(), f"Missing template at {report_tpl}"
    tpl_content = report_tpl.read_text(encoding="utf-8")
    assert "Code Review Report" in tpl_content
    assert "Five-Axis Assessment" in tpl_content
    assert "Runtime Visual Review Gate" in tpl_content


def test_flutter_verification_skill_structure():
    skill_dir = PLUGIN_DIR / "packs" / "flutter" / "skills" / "verification"
    content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert "name: verification" in content
    assert "BASE_REVISION" in content
    assert "REVIEW_REVISION" in content
    assert "visual-quality" in content
    assert "incremental-implementation" in content
    assert "FAILED" in content and "BLOCKED" in content and "NOT_RUN" in content
    assert "file:///Users/" not in content

    contract = skill_dir / "references" / "01_client_check_contract.md"
    report = skill_dir / "templates" / "verification_report.md.tpl"
    assert contract.exists()
    assert report.exists()
    assert "Revision invalidation" in contract.read_text(encoding="utf-8")
    assert "Acceptance criteria traceability" in report.read_text(encoding="utf-8")


def test_plugin_agent_definitions_structure():
    """Verify five delivery agents, a docs writer and a UI/UX designer are packaged."""
    agents_dir = PLUGIN_DIR / "core" / "agents"
    assert agents_dir.is_dir(), f"Missing agents directory at {agents_dir}"

    agent_names = ["spec_writer", "planning", "code_writer", "code_reviewer", "test_runner", "docs_writer", "designer"]
    for name in agent_names:
        agent_file = agents_dir / f"{name}.md"
        assert agent_file.exists(), f"Missing agent definition file: {agent_file}"
        content = rendered_agent(f"{name}.md")
        assert content.startswith("---")
        assert f"name: {name}" in content
        assert "description:" in content
        assert "skills:" in content
        assert "tools:" in content

    # Check code_writer has ask_question for Grill-Me during implementation
    code_writer_content = rendered_agent("code_writer.md")
    assert "ask_question" in code_writer_content
    assert "clean-architecture" in code_writer_content
    assert "phase" in code_writer_content.lower()
    for tool in ("get_project_structure", "get_ux_error_patterns"):
        assert tool in code_writer_content
    assert "core-package-usage" in code_writer_content

    # Check spec_writer has ask_question for requirements Grill-Me
    spec_writer_content = rendered_agent("spec_writer.md")
    assert "ask_question" in spec_writer_content
    assert "Gate 1" in spec_writer_content and "Gate 2" in spec_writer_content
    assert "Do not write `lib/`, `test/`, `implementation-plan.md`" in spec_writer_content
    planning_content = rendered_agent("planning.md")
    assert "Gate 3" in planning_content and "SKIPPED" in planning_content
    assert "validate_plan_slices" in planning_content
    designer_content = rendered_agent("designer.md")
    assert "ui-ux-design" in designer_content and "ask_question" in designer_content
    assert "Do not write runtime code" in designer_content and "flutter-ui-kit-mapping" in designer_content
    docs_content = rendered_agent("docs_writer.md")
    assert "documentation" in docs_content and "Do not edit runtime code" in docs_content

    # Check test_runner is read-only for code
    test_runner_content = rendered_agent("test_runner.md")
    assert "read-only" in test_runner_content.lower()
    assert "verification" in test_runner_content

    # Check code_reviewer enforces Clean Architecture
    reviewer_content = rendered_agent("code_reviewer.md")
    assert "validate_architecture_code" in reviewer_content
    assert "Clean Architecture" in reviewer_content


def test_review_handoff_contract_is_packaged():
    agents = PLUGIN_DIR / "core" / "agents"
    spec = rendered_agent("spec_writer.md")
    writer = rendered_agent("code_writer.md")
    reviewer = rendered_agent("code_reviewer.md")
    runner = rendered_agent("test_runner.md")
    review_report = (PLUGIN_DIR / "packs/flutter/skills/code-review/templates/code_review_report.md.tpl").read_text(encoding="utf-8")
    verification_report = (PLUGIN_DIR / "packs/flutter/skills/verification/templates/verification_report.md.tpl").read_text(encoding="utf-8")

    assert "Gate 1" in spec and "Gate 2" in spec
    assert "Gate 3" in rendered_agent("planning.md")
    assert "READY_FOR_REVIEW" in writer
    assert "staged/unstaged/untracked scope" in writer
    assert "run_command" in reviewer and "visual-quality" in reviewer
    assert "APPROVED" in reviewer and "UNVERIFIED" in reviewer
    assert "same tree" in runner and "read-only" in runner.lower()
    for report in (review_report, verification_report):
        assert "{{APPROVED_DOCUMENT_REVISIONS}}" in report
        assert "{{ACTUAL_APPROVAL_REFERENCES}}" in report
        assert "{{PLANNED_CHECKS}}" in report
    assert "{{AC_ROWS}}" in review_report
    assert "{{UNCOMMITTED_SCOPE}}" in verification_report


def test_backend_pack_structure_and_installation(tmp_path):
    """Backend is a pack on the shared core agents (2.8.0), not a separate plugin."""
    from coder_nexus.plugin_build import load_pack

    assert not (PLUGIN_DIR / "coder-nexus-be").exists()
    pack = load_pack(PLUGIN_DIR, "backend")
    assert pack["status"] == "maintained"
    assert {"clean-architecture", "unit-testing", "code-review", "verification", "architecture-design"} <= set(pack["slots"])
    assert "api-contract-design" in pack["extra"]
    for agent in ("spec_writer.md", "planning.md", "code_writer.md", "code_reviewer.md", "test_runner.md", "docs_writer.md"):
        assert (PLUGIN_DIR / "packs" / "backend" / "agents" / agent).exists(), f"Missing Backend overlay: {agent}"

    args = argparse.Namespace(is_global=False, workspace=str(tmp_path), plugin="be")
    assert cmd_install_plugin(args) == 0
    installed = tmp_path / ".agents" / "plugins" / "coder-nexus"
    skills = {p.name for p in (installed / "skills").iterdir()}
    assert {"backend-clean-architecture", "backend-api-contract-design", "backend-clean-code", "backend-secure-coding-standards", "backend-code-simplification", "backend-root-cause-debugging", "backend-bug-hunt", "work-item-contract", "grilling"} <= skills
    assert not any(name.startswith("flutter-") for name in skills)
    stubs = json.loads((installed / "slot_stubs.json").read_text(encoding="utf-8"))
    assert stubs == {
        "backend-core-package-usage": "not_applicable",
        "backend-visual-quality": "not_applicable",
        "backend-ui-kit-mapping": "not_applicable",
    }
    writer = (tmp_path / ".agents" / "agents" / "code_writer.md").read_text(encoding="utf-8")
    assert "## Backend rules" in writer and "## Frontend rules" not in writer
    meta = json.loads((installed / "installed_version.json").read_text(encoding="utf-8"))
    assert meta["packs"] == ["backend"]


def test_cli_installs_one_pack_per_workspace(tmp_path, capsys):
    """3.2.0: packs are never combined; a different pack needs --replace and then replaces the installed one."""
    assert cmd_install_plugin(argparse.Namespace(is_global=False, workspace=str(tmp_path), pack=["flutter"])) == 0
    installed = tmp_path / ".agents/plugins/coder-nexus"
    before = sorted(str(p.relative_to(tmp_path)) for p in (tmp_path / ".agents").rglob("*"))
    meta_before = (installed / "installed_version.json").read_text(encoding="utf-8")
    assert cmd_install_plugin(argparse.Namespace(is_global=False, workspace=str(tmp_path), pack=["backend"])) == 1
    assert "workspace has flutter; pass --replace to switch" in capsys.readouterr().err
    assert sorted(str(p.relative_to(tmp_path)) for p in (tmp_path / ".agents").rglob("*")) == before, "nothing removed"
    assert (installed / "installed_version.json").read_text(encoding="utf-8") == meta_before
    stack = json.loads((tmp_path / ".agents" / "stack.json").read_text(encoding="utf-8"))
    assert [pack["stack"] for pack in stack["packs"]] == ["flutter"]
    assert (tmp_path / ".agents/plugins/coder-nexus/skills/flutter-core-package-usage").is_dir()
    assert cmd_install_plugin(argparse.Namespace(is_global=False, workspace=str(tmp_path), pack=["flutter", "backend"])) == 1
    assert cmd_install_plugin(argparse.Namespace(is_global=False, workspace=str(tmp_path), pack=["backend"], replace=True)) == 0
    stack = json.loads((tmp_path / ".agents" / "stack.json").read_text(encoding="utf-8"))
    assert [pack["stack"] for pack in stack["packs"]] == ["backend"]
    assert not (tmp_path / ".agents/plugins/coder-nexus/skills/flutter-core-package-usage").exists()
    assert (tmp_path / ".agents/plugins/coder-nexus/skills/backend-api-contract-design").is_dir()


@pytest.mark.parametrize("stack", ["flutter", "backend"])
def test_plan_change_and_acceptance_skills_install_in_every_projection(tmp_path, stack):
    """3.2.0: change-control and quality-acceptance are core skills, so both packs ship them."""
    from coder_nexus.plugin_build import build_variant

    target = build_variant(stack, "workspace", tmp_path)
    skills = target / "files/.agents/plugins/coder-nexus/skills"
    for name in ("change-control", "quality-acceptance"):
        assert f"name: {name}" in (skills / name / "SKILL.md").read_text(encoding="utf-8"), (stack, name)


def test_work_item_templates_carry_plan_change_constraints_and_expected():
    """3.2.0: plans record global constraints, review focus and changes; each task states Expected."""
    templates = PLUGIN_DIR / "core/skills/work-item-contract/templates"
    plan = (templates / "implementation-plan.md.tpl").read_text(encoding="utf-8")
    for heading in ("## Plan change log", "## Global constraints", "## Review focus"):
        assert re.search(rf"^{re.escape(heading)}\s*$", plan, re.M), heading
    phase = (templates / "phase.md.tpl").read_text(encoding="utf-8")
    assert "**Expected**" in phase


def test_shared_contracts_protocol_and_templates():
    """Verify shared_contracts contains handshake protocol and templates."""
    shared = REPO_ROOT / "plugins" / "shared_contracts"
    assert (shared / "api_handshake_protocol.md").exists()
    assert (shared / "templates" / "api_contract.json.tpl").exists()
    assert (shared / "templates" / "api_gap_report.md.tpl").exists()

    protocol = (shared / "api_handshake_protocol.md").read_text(encoding="utf-8")
    assert "Frontend pack" in protocol
    assert "Backend pack" in protocol
    assert ".agents/stack.json" in protocol
    assert "Contract-First" in protocol
    assert "DRAFT_BY_FE" in protocol
    assert "APPROVED_BY_BE" in protocol



def test_built_projections_apply_identically_for_every_variant(tmp_path):
    """Both installers copy the same built projection; workspace layouts keep one agent copy."""
    from coder_nexus.plugin_build import apply_projection, available_packs, build, build_variant

    out = tmp_path / "dist"
    build(out)
    assert available_packs() == ["backend", "flutter"]
    assert {p.name for p in out.iterdir() if p.is_dir()} == {
        f"{layout}-{stack}" for layout in ("workspace", "global") for stack in available_packs()
    }, "3.2.0 builds single-stack projections only"
    with pytest.raises(ValueError, match="exactly one pack"):
        build_variant(["backend", "flutter"], "workspace", tmp_path / "combo")
    for key in available_packs():
        workspace = tmp_path / f"ws-{key}"
        (workspace / ".agents/plugins/coder-nexus-fe").mkdir(parents=True)
        (workspace / ".agents/plugins/coder-nexus-be").mkdir(parents=True)
        spec = apply_projection(out / f"workspace-{key}", workspace)
        installed = workspace / spec["managed"][0]
        assert installed.name == "coder-nexus"
        assert not (installed / "agents").exists()
        assert len(list((workspace / ".agents/agents").glob("*.md"))) == 7
        assert not any((workspace / rel).exists() for rel in spec["remove"]), "pre-2.8 plugins must be removed"
        manifest = json.loads((installed / "bundle_manifest.json").read_text(encoding="utf-8"))
        assert manifest["packs"] == [key]
        for resource in manifest["required_resources"]:
            assert (installed / resource).is_file(), (key, resource)
        assert spec["problems"] == [], (key, spec["problems"])
    for stack in available_packs():
        home = tmp_path / f"home-{stack}"
        apply_projection(out / f"global-{stack}", home)
        assert (home / "coder-nexus" / "agents" / "code_writer.md").is_file()


def test_framework_skills_are_prefixed_and_agent_skills_resolve(tmp_path):
    """2.6.0: framework skills install as <stack>-<slot>; agents only declare installed skills."""
    from coder_nexus.plugin_build import build_variant

    target = build_variant("flutter", "workspace", tmp_path)
    spec = json.loads((target / "projection.json").read_text(encoding="utf-8"))
    assert spec["problems"] == []
    files = target / "files"
    skills = files / ".agents/plugins/coder-nexus/skills"
    names = {p.name for p in skills.iterdir()}
    assert {"flutter-core-package-usage", "flutter-clean-architecture", "work-item-contract", "delivery-workflow"} <= names
    assert "core-package-usage" not in names and "clean-architecture" not in names
    assert "name: flutter-core-package-usage" in (skills / "flutter-core-package-usage/SKILL.md").read_text(encoding="utf-8")
    for agent in (files / ".agents/agents").glob("*.md"):
        text = agent.read_text(encoding="utf-8")
        assert "{{slot:" not in text
        frontmatter = text.split("---", 2)[1]
        skill_block = frontmatter.split("skills:", 1)[1].split("tools:", 1)[0]
        for line in skill_block.splitlines():
            name = line.strip().removeprefix("- ").strip()
            if name:
                assert name in names, (agent.name, name)


def test_preview_pack_gaps_become_blocked_placeholders(tmp_path):
    """2.7.1: every slot a preview pack lacks resolves to a BLOCKED placeholder skill."""
    from coder_nexus.plugin_build import build_variant, load_pack

    plugins = tmp_path / "plugins"
    shutil.copytree(PLUGIN_DIR, plugins, ignore=shutil.ignore_patterns("dist"))
    pack_file = plugins / "packs" / "backend" / "pack.json"
    pack_data = json.loads(pack_file.read_text(encoding="utf-8"))
    pack_data["status"] = "preview"
    pack_file.write_text(json.dumps(pack_data), encoding="utf-8")
    assert load_pack(plugins, "backend")["status"] == "preview"
    slots_file = plugins / "core/slots.json"
    slots = json.loads(slots_file.read_text(encoding="utf-8"))
    slots["slots"]["probe-gap"] = "A slot no pack implements yet."
    slots_file.write_text(json.dumps(slots), encoding="utf-8")

    target = build_variant("backend", "workspace", tmp_path / "out", plugins)
    spec = json.loads((target / "projection.json").read_text(encoding="utf-8"))
    assert spec["status"] == "preview"
    assert spec["problems"] == []
    assert spec["stubs"]["backend-probe-gap"] == "blocked"
    skills = target / "files/.agents/plugins/coder-nexus/skills"
    stub = (skills / "backend-probe-gap/SKILL.md").read_text(encoding="utf-8")
    assert "name: backend-probe-gap" in stub and "BLOCKED" in stub
    assert (skills / "backend-clean-architecture/SKILL.md").is_file()


def test_maintained_pack_cannot_ship_a_missing_slot(tmp_path):
    from coder_nexus.plugin_build import build_variant

    plugins = tmp_path / "plugins"
    shutil.copytree(PLUGIN_DIR, plugins, ignore=shutil.ignore_patterns("dist"))
    pack_file = plugins / "packs/flutter/pack.json"
    pack = json.loads(pack_file.read_text(encoding="utf-8"))
    del pack["slots"]["visual-quality"]
    pack_file.write_text(json.dumps(pack), encoding="utf-8")
    with pytest.raises(ValueError, match="flutter-visual-quality"):
        build_variant("flutter", "workspace", tmp_path / "out", plugins)

    pack["not_applicable"] = [*pack.get("not_applicable", []), "visual-quality"]
    pack_file.write_text(json.dumps(pack), encoding="utf-8")
    target = build_variant("flutter", "workspace", tmp_path / "out", plugins)
    stub = target / "files/.agents/plugins/coder-nexus/skills/flutter-visual-quality/SKILL.md"
    assert "not applicable" in stub.read_text(encoding="utf-8")


def test_required_slot_cannot_be_missing_or_not_applicable(tmp_path):
    from coder_nexus.plugin_build import build_variant

    plugins = tmp_path / "plugins"
    shutil.copytree(PLUGIN_DIR, plugins, ignore=shutil.ignore_patterns("dist"))
    pack_file = plugins / "packs/flutter/pack.json"
    pack = json.loads(pack_file.read_text(encoding="utf-8"))

    # Missing from slots
    del pack["slots"]["clean-code"]
    pack_file.write_text(json.dumps(pack), encoding="utf-8")
    with pytest.raises(ValueError, match="packs/flutter: required slot clean-code missing or not_applicable"):
        build_variant("flutter", "workspace", tmp_path / "out", plugins)

    # In not_applicable
    pack["not_applicable"] = [*pack.get("not_applicable", []), "clean-code"]
    pack_file.write_text(json.dumps(pack), encoding="utf-8")
    with pytest.raises(ValueError, match="packs/flutter: required slot clean-code missing or not_applicable"):
        build_variant("flutter", "workspace", tmp_path / "out", plugins)


def test_core_and_frontend_layer_are_stack_neutral():
    """2.7.0: stack rules live in packs; core and shared layers carry no stack markers."""
    from coder_nexus.plugin_build import load_pack

    markers = []
    for pack_file in (PLUGIN_DIR / "packs").glob("*/pack.json"):
        markers += load_pack(PLUGIN_DIR, pack_file.parent.name)["markers"]
    pattern = re.compile(r"(?<![\w-])(" + "|".join(re.escape(m) for m in markers) + r")(?![\w-])")
    offenders = []
    for base in (PLUGIN_DIR / "core", PLUGIN_DIR / "layers"):
        for path in [*base.rglob("*.md"), *base.rglob("*.tpl")]:
            found = set(pattern.findall(path.read_text(encoding="utf-8")))
            if found:
                offenders.append(f"{path.relative_to(PLUGIN_DIR)}: {sorted(found)}")
    assert offenders == []


def test_flutter_agents_compose_core_frontend_and_pack_rules():
    code_writer = rendered_agent("code_writer.md")
    assert code_writer.index("## Frontend rules") < code_writer.index("## Flutter rules")
    assert "flutter-core-package-usage" in code_writer.split("---", 2)[1]


def test_backend_projection_receives_no_flutter_instructions(tmp_path):
    from coder_nexus.plugin_build import build_variant

    target = build_variant("backend", "workspace", tmp_path)
    problems = json.loads((target / "projection.json").read_text(encoding="utf-8"))["problems"]
    assert not [p for p in problems if "mentions another stack" in p or "another stack's skill" in p]


def test_designer_is_wired_into_the_delivery_flow():
    """UI-impact items: Designer between goal framing and Gate 1; Planning, Reviewer and visual checks use the approved design."""
    skills = flutter_workspace() / ".agents/plugins/coder-nexus/skills"
    route = (skills / "dev-team/SKILL.md").read_text(encoding="utf-8")
    contract = (skills / "work-item-contract/SKILL.md").read_text(encoding="utf-8")
    assert "**Designer** (UI/UX" in route and "READY_FOR_SPEC" in route and "| Designer |" in contract
    assert route.index("**Designer** (UI/UX") < route.index("**Planning** (Tech Lead)")
    assert "screen-catalog.md" in contract and "{{slot:" not in route + contract
    assert "flutter-ui-kit-mapping" in rendered_agent("designer.md")
    assert "workflows + UI/UX design" in (skills / "work-item-contract/references/type-sequences.md").read_text(encoding="utf-8")

    spec = rendered_agent("spec_writer.md")
    assert "Stage 1A-UX" in spec and "`designer`" in spec and "`## Workflows`" in spec and "validate_ux_design" in spec
    planning = rendered_agent("planning.md")
    assert "## UI/UX mapping" in planning and "DESIGN-008" in planning and "flutter-ui-kit-mapping" in planning
    assert "NEW COMPONENT" in planning
    assert "approved `uiux.md` revision" in rendered_agent("code_reviewer.md")
    assert "screen-catalog.md" in rendered_agent("docs_writer.md")

    assert "## Workflows" in (skills / "work-item-contract/templates/requirements.md.tpl").read_text(encoding="utf-8")
    assert not (skills / "delivery-workflow/templates/requirements.md.tpl").exists()
    design_tpl = (skills / "flutter-architecture-design/templates/design.md.tpl").read_text(encoding="utf-8")
    assert "## UI/UX mapping" in design_tpl and "`flutter-ui-kit-mapping` §3" in design_tpl
    visual = (skills / "flutter-visual-quality/SKILL.md").read_text(encoding="utf-8")
    assert "## Compare with the approved UI/UX design" in visual and ".superpowers/ux/current/" in visual


def test_ux_walkthrough_reference_is_packaged():
    """The designer learns to script walkthroughs; the reference ships in core and stays stack-neutral."""
    manifest = json.loads((PLUGIN_DIR / "core" / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert "core/skills/ui-ux-design/references/04_walkthrough.md" in manifest["required_resources"]
    skills = flutter_workspace() / ".agents/plugins/coder-nexus/skills"
    ref = (skills / "ui-ux-design/references/04_walkthrough.md").read_text(encoding="utf-8")
    for needle in ("## 8. Walkthrough", "data-ux-target", "Mô phỏng — MOCK", "Q-NN", "ux record", "not a test", "UX-011"):
        assert needle in ref, needle
    assert "references/04_walkthrough.md" in (skills / "ui-ux-design/SKILL.md").read_text(encoding="utf-8")
    assert "data-ux-target" in (skills / "ui-ux-design/references/02_screen_rules.md").read_text(encoding="utf-8")
    assert "▶ Play" in (skills / "ui-ux-design/references/03_revisions_and_approval.md").read_text(encoding="utf-8")
    assert "## 8. Walkthrough" in rendered_agent("designer.md")
    ux_kit = (skills / "flutter-ui-kit-mapping/SKILL.md").read_text(encoding="utf-8")
    assert "barcode scanners" in ux_kit and "Tablet landscape" in ux_kit


def test_ux_scenarios_orientation_and_fixed_shell_guidance_is_packaged():
    """Scenario workflows, labelled steps, orientation asked once, and the generated viewer shell reach the installed skill."""
    skills = flutter_workspace() / ".agents/plugins/coder-nexus/skills"
    interview = (skills / "ui-ux-design/references/01_workflow_interview.md").read_text(encoding="utf-8")
    for needle in ("One workflow per user-visible scenario", "Sai mật khẩu", "Quên mật khẩu", "Tài khoản bị khoá", "REQ-006",
                   "portrait · landscape · portrait + landscape", "--orientations", "once per project", "1 Chọn NG→S01, 2 Quét LPN→S01:scan"):
        assert needle in interview, needle
    skill = (skills / "ui-ux-design/SKILL.md").read_text(encoding="utf-8")
    assert "One `W-NN` per user-visible scenario" in skill and "UX-012" in skill and "never edit them" in skill
    designer = rendered_agent("designer.md")
    assert "portrait / landscape / both per platform" in designer and "Never edit `design-uiux/index.html`" in designer
    ux_kit = (skills / "flutter-ui-kit-mapping/SKILL.md").read_text(encoding="utf-8")
    assert "scanner stations" in ux_kit and "only when a source shows it" in ux_kit
    core = (PLUGIN_DIR / "core/skills/ui-ux-design/references/01_workflow_interview.md").read_text(encoding="utf-8")
    assert "Flutter" not in core and "flutter" not in core, "core stays stack-neutral"


def test_bug_hunt_skill_is_wired_into_review_and_writing():
    """Bug-hunt: concrete failure scenarios, adversarial verification, used by Reviewer and Code Writer."""
    for pack in ("flutter", "backend"):
        content = (PLUGIN_DIR / f"packs/{pack}/skills/bug-hunt/SKILL.md").read_text(encoding="utf-8")
        assert "name: bug-hunt" in content
        for term in ("CONFIRMED", "PLAUSIBLE", "BLOCKER"):
            assert term in content, term
    assert "bug-hunt" in rendered_agent("code_reviewer.md")
    assert "bug-hunt" in rendered_agent("code_writer.md")
    assert "bug-hunt" in (PLUGIN_DIR / "core/skills/incremental-implementation/SKILL.md").read_text(encoding="utf-8")
    for pack, ref in (("flutter", "05_bug_patterns.md"), ("backend", "bug_patterns.md")):
        review = PLUGIN_DIR / "packs" / pack / "skills/code-review"
        assert (review / "references" / ref).is_file()
        assert ref in (review / "SKILL.md").read_text(encoding="utf-8")
    report = (PLUGIN_DIR / "packs/flutter/skills/code-review/templates/code_review_report.md.tpl").read_text(encoding="utf-8")
    assert "{{BUG_HUNT_ROWS}}" in report and "Failure scenario" in report


def test_core_git_preflight_skill_is_wired():
    """Core git-preflight: spec first, branch after Gate 1 from the job type's base, never production."""
    content = (PLUGIN_DIR / "core/skills/git-preflight/SKILL.md").read_text(encoding="utf-8")
    assert "name: git-preflight" in content
    assert "after Gate 1" in content and "git switch -c" in content
    assert "Never put code on production" in content
    assert ".agents/skills/git-workflow/" in content
    for role in ("spec_writer.md", "planning.md", "code_writer.md", "code_reviewer.md"):
        assert "git-preflight" in rendered_agent(role), role
    assert "1E  Branch" in rendered_agent("spec_writer.md")


def test_all_skills_have_valid_yaml_frontmatter():
    """Every skill's SKILL.md frontmatter must parse cleanly without YAML syntax errors (e.g. unquoted colons)."""
    import yaml

    skill_files = list((PLUGIN_DIR / "core/skills").glob("*/SKILL.md")) + list((PLUGIN_DIR / "packs").glob("*/skills/*/SKILL.md"))
    assert len(skill_files) >= 15
    for skill_file in skill_files:
        content = skill_file.read_text(encoding="utf-8")
        assert content.startswith("---"), f"{skill_file} missing frontmatter delimiter"
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{skill_file} malformed frontmatter"
        data = yaml.safe_load(parts[1])
        assert isinstance(data, dict), f"{skill_file} frontmatter did not parse as a dict"
        assert "name" in data, f"{skill_file} missing 'name'"
        assert "description" in data, f"{skill_file} missing 'description'"


def test_pack_generated_from_matches_generator_versions():
    """generated_from in pack.json matches the actual VERSION files in skill-factory generators."""
    generators_dir = REPO_ROOT / "src/skill_factory/library/generators"
    required_slots = (
        "clean-code",
        "code-simplification",
        "secure-coding-standards",
        "unit-testing",
        "root-cause-debugging",
        "bug-hunt",
    )

    for pack_dir in sorted((PLUGIN_DIR / "packs").iterdir()):
        if not (pack_dir / "pack.json").is_file():
            continue
        pack = json.loads((pack_dir / "pack.json").read_text(encoding="utf-8"))
        generated = pack.get("generated_from", {})
        for slot in required_slots:
            assert slot in generated, f"pack {pack['stack']} missing generated_from for {slot}"
            gen_tag = generated[slot]
            gen_name, version = gen_tag.split("@", 1)
            version_file = generators_dir / gen_name / "VERSION"
            assert version_file.is_file(), f"missing VERSION file for {gen_name}"
            actual_version = version_file.read_text(encoding="utf-8").strip()
            assert version == actual_version, (
                f"pack {pack['stack']} cần sinh lại skill {slot}: expected {actual_version}, got {version}"
            )


def test_built_dist_does_not_contain_pack_json():
    """Task 6.4: pack.json is metadata for plugin_build and is never copied into the dist output."""
    dist = PLUGIN_DIR / "dist"
    if dist.is_dir():
        found = list(dist.glob("**/pack.json"))
        assert not found, f"Unexpected pack.json in dist: {found}"
