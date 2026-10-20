"""Tests for Antigravity plugin packaging, manifest, and installation."""

import argparse
import json
from pathlib import Path
import re
import shutil
import tempfile
import pytest

from coder_nexus.plugin_install import _install_plugin_projection, cmd_install_plugin


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = REPO_ROOT / "plugins" / "coder-nexus-fe"


def test_plugin_json_structure():
    """Verify plugin.json exists, is valid JSON, and contains expected metadata."""
    manifest_file = PLUGIN_DIR / "plugin.json"
    assert manifest_file.exists(), f"Missing plugin.json at {manifest_file}"

    with open(manifest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("name") == "coder-nexus-fe"
    assert data.get("$schema") == "https://antigravity.google/schemas/v1/plugin.json"
    assert "description" in data
    assert set(data) == {"$schema", "name", "description"}


def test_extension_sync_requires_an_explicit_command():
    source = (REPO_ROOT / "extension.js").read_text(encoding="utf-8")
    activation = source.split("function activate(context) {", 1)[1].split("function deactivate()", 1)[0]
    assert "installAntigravityPlugin(context, null, true)" not in activation
    assert "registerCommand('coder-nexus.installWorkspace'" in activation
    assert "registerCommand('coder-nexus.installWorkspaceFlutter'" in activation
    assert "registerCommand('coder-nexus.installWorkspaceFrappe'" in activation
    assert "registerCommand('coder-nexus.installWorkspaceBE'" in activation
    assert "registerCommand('coder-nexus.installWorkspaceFE'" in activation
    assert "registerCommand('coder-nexus.installGlobal'" in activation
    assert "registerCommand('coder-nexus.showArchitecture'" in activation
    assert (REPO_ROOT / "media" / "architecture.html").exists()


def test_bundle_manifest_inventory():
    manifest = json.loads((PLUGIN_DIR / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert bool(re.match(r"^\d+\.\d+\.\d+", manifest["plugin_version"]))
    if (REPO_ROOT / "package.json").exists():
        pkg = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
        assert manifest["plugin_version"] == pkg.get("version")
    assert manifest["hub_version"] == "0.1.0"
    assert "flutter/verification" in manifest["public_skills"]
    assert len(manifest["mcp_tools"]) == 8
    packaged_skills = {f"{path.parent.parent.name}/{path.parent.name}" for path in (PLUGIN_DIR / "skills").glob("*/*/SKILL.md")}
    assert set(manifest["public_skills"]) == packaged_skills
    for resource in manifest["required_resources"]:
        assert (PLUGIN_DIR / resource).exists(), f"Missing bundle resource: {resource}"


def test_canonical_bundle_has_no_author_machine_path():
    offenders = []
    for path in PLUGIN_DIR.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".md", ".tpl"}:
            content = path.read_text(encoding="utf-8")
            if "/Users/" in content:
                offenders.append(str(path.relative_to(PLUGIN_DIR)))
    assert offenders == []


def test_mcp_config_structure():
    """Verify the canonical config is portable and delegates to the installed CLI."""
    config_file = PLUGIN_DIR / "mcp_config.json"
    assert config_file.exists(), f"Missing mcp_config.json at {config_file}"

    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "mcpServers" in data
    assert "coder-nexus" in data["mcpServers"]
    server_cfg = data["mcpServers"]["coder-nexus"]
    assert server_cfg == {"command": "coder-nexus", "args": ["serve"]}
    assert "/Users/" not in config_file.read_text(encoding="utf-8")


def test_skill_markdown_structure():
    """Verify huly-task-runner SKILL.md has valid frontmatter and core instructions."""
    skill_file = PLUGIN_DIR / "skills" / "shared" / "huly-task-runner" / "SKILL.md"
    assert skill_file.exists(), f"Missing SKILL.md at {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---")
    assert "name: huly-task-runner" in content
    assert "description:" in content
    # Verify core guidance references
    assert "huly_get_my_tasks" in content
    assert "huly_get_task_detail" in content
    assert "Read-Only" in content
    assert "Zero Mock Data" in content

def test_flutter_clean_architecture_skill_structure():
    """Verify flutter-clean-architecture SKILL.md, references, and manifest."""
    skill_dir = PLUGIN_DIR / "skills" / "flutter" / "clean-architecture"
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


def test_flutter_core_usage_skill_structure():
    """Verify flutter core-usage SKILL.md and its guidance."""
    skill_dir = PLUGIN_DIR / "skills" / "flutter" / "core-usage"
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists(), f"Missing SKILL.md at {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---")
    assert "name: core-usage" in content
    assert "app_core" in content
    assert "app_ui_kit" in content


def test_flutter_feature_planner_skill_structure():
    """Verify flutter-feature-planner SKILL.md, manifest, and references packaging."""
    skill_dir = PLUGIN_DIR / "skills" / "shared" / "feature-planner"
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists(), f"Missing SKILL.md at {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---")
    assert "name: feature-planner" in content
    assert "description:" in content
    assert "Gate 1" in content and "Gate 2" in content and "Gate 3" in content
    assert "docs/features/<module>/<feature>/vN/" in content

    # Check references and manifest
    ref_dir = skill_dir / "references"
    manifest_file = ref_dir / "manifest.json"
    assert manifest_file.exists(), f"Missing manifest.json at {manifest_file}"

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest.get("version") == "1.3.0"
    assert manifest.get("skill_name") == "flutter-feature-planner"
    assert len(manifest.get("references", [])) == 4
    assert len(manifest.get("templates", [])) == 7
    assert len(manifest.get("legacy_templates", [])) == 3

    # Check templates
    tpl_dir = skill_dir / "templates"
    assert (tpl_dir / "feature_proposal.md.tpl").exists()
    assert (tpl_dir / "implementation_plan.md.tpl").exists()
    assert (tpl_dir / "task.md.tpl").exists()


def test_client_workflow_skills_are_packaged_and_portable():
    """Verify public workflow skills ship in the plugin without author-machine links."""
    expected = {
        "brainstorming",
        "planning-and-task-breakdown",
        "incremental-implementation",
        "clean-code",
        "code-simplification",
        "visual-verification",
        "verification",
        "code-review",
    }
    for name in expected:
        skill_file = next((PLUGIN_DIR / "skills").glob(f"*/{name}/SKILL.md"), PLUGIN_DIR / "skills" / "flutter" / name / "SKILL.md")
        assert skill_file.exists(), f"Missing packaged skill: {name}"
        content = skill_file.read_text(encoding="utf-8")
        assert f"name: {name}" in content
        assert "file:///Users/" not in content

    runtime_skill_files = list((PLUGIN_DIR / "skills").glob("**/*.md"))
    author_paths = [
        str(path.relative_to(PLUGIN_DIR))
        for path in runtime_skill_files
        if "file:///Users/" in path.read_text(encoding="utf-8")
    ]
    assert author_paths == []


def test_clean_architecture_templates_exist_and_adhere_to_contracts():
    """Verify all 11 starter templates exist and strictly adhere to Senior contracts."""
    tpl_dir = PLUGIN_DIR / "skills" / "flutter" / "clean-architecture" / "templates"
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
    manifest_file = PLUGIN_DIR / "skills" / "flutter" / "clean-architecture" / "references" / "manifest.json"
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    assert "commit_hash" in manifest_data
    assert "templates" in manifest_data
    assert len(manifest_data["templates"]) == 11


def test_clean_architecture_rules_structure():
    """Verify clean_architecture_rules.md exists in plugin rules directory."""
    rule_file = PLUGIN_DIR / "rules" / "clean_architecture_rules.md"
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

        installed = Path(tmpdir) / ".agents" / "plugins" / "coder-nexus-fe"
        assert installed.is_dir()
        assert not (installed / "agents").exists()
        assert (Path(tmpdir) / ".agents" / "agents" / "code_writer.md").is_file()
        projected = json.loads((installed / "bundle_manifest.json").read_text(encoding="utf-8"))
        for resource in projected["required_resources"]:
            assert (installed / resource).is_file(), resource
        metadata = json.loads((installed / "installed_version.json").read_text(encoding="utf-8"))
        manifest = json.loads((PLUGIN_DIR / "bundle_manifest.json").read_text(encoding="utf-8"))
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
            json.dumps({"entries": [{"path": str(PLUGIN_DIR.resolve())}, {"path": "/other/plugin"}]}),
            encoding="utf-8",
        )
        args = argparse.Namespace(is_global=False, workspace=tmpdir)
        assert cmd_install_plugin(args) == 0
        data = json.loads(config.read_text(encoding="utf-8"))
        assert data == {"entries": [{"path": "/other/plugin"}]}


def test_cli_install_plugin_global_replaces_legacy_symlink(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        home = Path(tmpdir)
        destination = home / ".gemini" / "config" / "plugins" / "coder-nexus-fe"
        destination.parent.mkdir(parents=True)
        destination.symlink_to(PLUGIN_DIR, target_is_directory=True)
        monkeypatch.setattr(Path, "home", lambda: home)

        args = argparse.Namespace(is_global=True, workspace=None)
        assert cmd_install_plugin(args) == 0
        assert destination.is_dir()
        assert not destination.is_symlink()
        metadata = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
        manifest = json.loads((PLUGIN_DIR / "bundle_manifest.json").read_text(encoding="utf-8"))
        assert metadata["plugin_version"] == manifest["plugin_version"]


def test_install_projection_update_and_rollback_change_digest():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        source = root / "source-plugin"
        destination = root / "installed" / "coder-nexus-fe"
        shutil.copytree(PLUGIN_DIR, source)
        shutil.copytree(REPO_ROOT / "plugins/shared_contracts", source.parent / "shared_contracts")

        assert _install_plugin_projection(source, destination, REPO_ROOT) == "installed"
        original = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
        skill = source / "skills" / "flutter" / "verification" / "SKILL.md"
        original_skill = skill.read_text(encoding="utf-8")
        skill.write_text(original_skill + "\n", encoding="utf-8")
        assert _install_plugin_projection(source, destination, REPO_ROOT) == "updated"
        changed = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
        assert changed["bundle_digest"] != original["bundle_digest"]

        skill.write_text(original_skill, encoding="utf-8")
        assert _install_plugin_projection(source, destination, REPO_ROOT) == "updated"
        rolled_back = json.loads((destination / "installed_version.json").read_text(encoding="utf-8"))
        assert rolled_back["bundle_digest"] == original["bundle_digest"]


@pytest.mark.parametrize("plugin,framework", [("fe", "flutter"), ("fe", "frappe"), ("be", "flutter")])
def test_installed_projection_includes_shared_contract_and_valid_resource_paths(tmp_path, plugin, framework):
    source = REPO_ROOT / "plugins" / f"coder-nexus-{plugin}"
    destination = tmp_path / source.name
    _install_plugin_projection(source, destination, REPO_ROOT, framework)
    assert (destination / "shared_contracts/api_handshake_protocol.md").read_bytes() == (
        REPO_ROOT / "plugins/shared_contracts/api_handshake_protocol.md"
    ).read_bytes()
    manifest = json.loads((destination / "bundle_manifest.json").read_text())
    assert "shared_contracts/api_handshake_protocol.md" in manifest["required_resources"]
    for resource in manifest["required_resources"]:
        assert (destination / resource).is_file(), resource
    if plugin == "fe" and framework == "flutter":
        for relative in ("skills/work-items/SKILL.md", "rules/clean_architecture_rules.md"):
            document = destination / relative
            for link in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                assert (document.parent / link).is_file(), (relative, link)


def test_shared_contract_edit_and_framework_switch_refresh_projection(tmp_path):
    source = tmp_path / "source" / "coder-nexus-fe"
    shutil.copytree(PLUGIN_DIR, source)
    shared = source.parent / "shared_contracts"
    shutil.copytree(REPO_ROOT / "plugins/shared_contracts", shared)
    destination = tmp_path / "installed"
    assert _install_plugin_projection(source, destination, REPO_ROOT) == "installed"
    assert _install_plugin_projection(source, destination, REPO_ROOT) == "unchanged"
    protocol = shared / "api_handshake_protocol.md"
    protocol.write_text(protocol.read_text() + "\nProtocol revision changed.\n")
    assert _install_plugin_projection(source, destination, REPO_ROOT) == "updated"
    assert (destination / "shared_contracts/api_handshake_protocol.md").read_bytes() == protocol.read_bytes()
    assert _install_plugin_projection(source, destination, REPO_ROOT, "frappe") == "updated"
    assert not (destination / "skills/flutter-core-usage").exists()
    assert (destination / "skills/frappe-ui-catalog/SKILL.md").is_file()


def test_flutter_code_review_skill_structure():
    """Verify flutter-code-review SKILL.md, manifest, references, and review template."""
    skill_dir = PLUGIN_DIR / "skills" / "flutter" / "code-review"
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
    skill_dir = PLUGIN_DIR / "skills" / "flutter" / "verification"
    content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert "name: verification" in content
    assert "BASE_REVISION" in content
    assert "REVIEW_REVISION" in content
    assert "visual-verification" in content
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
    """Verify five delivery agents and a docs writer are packaged."""
    agents_dir = PLUGIN_DIR / "agents"
    assert agents_dir.is_dir(), f"Missing agents directory at {agents_dir}"

    agent_names = ["spec_writer", "planning", "code_writer", "code_reviewer", "test_runner", "docs_writer"]
    for name in agent_names:
        agent_file = agents_dir / f"{name}.md"
        assert agent_file.exists(), f"Missing agent definition file: {agent_file}"
        content = agent_file.read_text(encoding="utf-8")
        assert content.startswith("---")
        assert f"name: {name}" in content
        assert "description:" in content
        assert "skills:" in content
        assert "tools:" in content

    # Check code_writer has ask_question for Grill-Me during implementation
    code_writer_content = (agents_dir / "code_writer.md").read_text(encoding="utf-8")
    assert "ask_question" in code_writer_content
    assert "clean-architecture" in code_writer_content
    assert "phase" in code_writer_content.lower()
    for tool in ("get_project_structure", "get_ux_error_patterns"):
        assert tool in code_writer_content
    assert "core-usage" in code_writer_content

    # Check spec_writer has ask_question for requirements Grill-Me
    spec_writer_content = (agents_dir / "spec_writer.md").read_text(encoding="utf-8")
    assert "ask_question" in spec_writer_content
    assert "Gate 1" in spec_writer_content and "Gate 2" in spec_writer_content
    assert "Do not write `lib/`, `test/`, `implement-plan.md`" in spec_writer_content
    planning_content = (agents_dir / "planning.md").read_text(encoding="utf-8")
    assert "Gate 3" in planning_content and "SKIPPED" in planning_content
    assert "validate_plan_slices" in planning_content
    docs_content = (agents_dir / "docs_writer.md").read_text(encoding="utf-8")
    assert "documentation" in docs_content and "Do not edit runtime code" in docs_content

    # Check test_runner is read-only for code
    test_runner_content = (agents_dir / "test_runner.md").read_text(encoding="utf-8")
    assert "read-only" in test_runner_content.lower()
    assert "verification" in test_runner_content

    # Check code_reviewer enforces Clean Architecture
    reviewer_content = (agents_dir / "code_reviewer.md").read_text(encoding="utf-8")
    assert "validate_architecture_code" in reviewer_content
    assert "Clean Architecture" in reviewer_content


def test_review_handoff_contract_is_packaged():
    agents = PLUGIN_DIR / "agents"
    spec = (agents / "spec_writer.md").read_text(encoding="utf-8")
    writer = (agents / "code_writer.md").read_text(encoding="utf-8")
    reviewer = (agents / "code_reviewer.md").read_text(encoding="utf-8")
    runner = (agents / "test_runner.md").read_text(encoding="utf-8")
    review_report = (PLUGIN_DIR / "skills/flutter/code-review/templates/code_review_report.md.tpl").read_text(encoding="utf-8")
    verification_report = (PLUGIN_DIR / "skills/flutter/verification/templates/verification_report.md.tpl").read_text(encoding="utf-8")

    assert "Gate 1" in spec and "Gate 2" in spec
    assert "Gate 3" in (agents / "planning.md").read_text(encoding="utf-8")
    assert "READY_FOR_REVIEW" in writer
    assert "staged/unstaged/untracked scope" in writer
    assert "run_command" in reviewer and "visual-verification" in reviewer
    assert "APPROVED" in reviewer and "UNVERIFIED" in reviewer
    assert "same tree" in runner and "read-only" in runner.lower()
    for report in (review_report, verification_report):
        assert "{{APPROVED_DOCUMENT_REVISIONS}}" in report
        assert "{{ACTUAL_APPROVAL_REFERENCES}}" in report
        assert "{{PLANNED_CHECKS}}" in report
    assert "{{AC_ROWS}}" in review_report
    assert "{{UNCOMMITTED_SCOPE}}" in verification_report


def test_backend_plugin_structure_and_installation():
    """Verify coder-nexus-be scaffold, agents, manifest, and CLI installation."""
    be_dir = REPO_ROOT / "plugins" / "coder-nexus-be"
    assert be_dir.is_dir()

    manifest_file = be_dir / "plugin.json"
    assert manifest_file.exists()
    data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert data.get("name") == "coder-nexus-be"

    bundle = json.loads((be_dir / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert "be-work-items" in bundle["public_skills"]
    assert "be-clean-architecture" in bundle["public_skills"]
    assert "be-api-contracts" in bundle["public_skills"]
    assert "grill-me" in bundle["public_skills"]

    # Verify all 6 backend agents exist
    agents_dir = be_dir / "agents"
    for agent in ("spec_writer.md", "planning.md", "code_writer.md", "code_reviewer.md", "test_runner.md", "docs_writer.md"):
        assert (agents_dir / agent).exists(), f"Missing BE agent: {agent}"

    # Verify installation of BE plugin
    with tempfile.TemporaryDirectory() as tmpdir:
        args = argparse.Namespace(is_global=False, workspace=tmpdir, plugin="be")
        assert cmd_install_plugin(args) == 0
        installed = Path(tmpdir) / ".agents" / "plugins" / "coder-nexus-be"
        assert installed.is_dir()
        meta = json.loads((installed / "installed_version.json").read_text(encoding="utf-8"))
        assert meta["plugin_version"] == bundle["plugin_version"]


def test_shared_contracts_protocol_and_templates():
    """Verify shared_contracts contains handshake protocol and templates."""
    shared = REPO_ROOT / "plugins" / "shared_contracts"
    assert (shared / "api_handshake_protocol.md").exists()
    assert (shared / "templates" / "api_contract.json.tpl").exists()
    assert (shared / "templates" / "api_gap_report.md.tpl").exists()

    protocol = (shared / "api_handshake_protocol.md").read_text(encoding="utf-8")
    assert "coder-nexus-fe" in protocol
    assert "coder-nexus-be" in protocol
    assert "Contract-First" in protocol
    assert "DRAFT_BY_FE" in protocol
    assert "APPROVED_BY_BE" in protocol



def test_built_projections_apply_identically_for_every_variant(tmp_path):
    """Both installers copy the same built projection; workspace layouts keep one agent copy."""
    from coder_nexus.plugin_build import VARIANTS, apply_projection, build

    out = tmp_path / "dist"
    build(out)
    for variant, (plugin_name, _framework) in VARIANTS.items():
        workspace = tmp_path / f"ws-{variant}"
        (workspace / ".agents/plugins/coder-nexus-fe" if plugin_name == "coder-nexus-be" else workspace / ".agents/plugins/coder-nexus-be").mkdir(parents=True)
        spec = apply_projection(out / f"workspace-{variant}", workspace)
        installed = workspace / spec["managed"][0]
        assert not (installed / "agents").exists()
        assert len(list((workspace / ".agents/agents").glob("*.md"))) == 6
        assert not any((workspace / rel).exists() for rel in spec["remove"]), "the other plugin must be removed"
        manifest = json.loads((installed / "bundle_manifest.json").read_text(encoding="utf-8"))
        for resource in manifest["required_resources"]:
            assert (installed / resource).is_file(), (variant, resource)

        home = tmp_path / f"home-{variant}"
        spec = apply_projection(out / f"global-{variant}", home)
        assert (home / plugin_name / "agents" / "code_writer.md").is_file()


def test_framework_skills_are_prefixed_and_agent_skills_resolve(tmp_path):
    """2.6.0: framework skills install as <stack>-<slot>; agents only declare installed skills."""
    from coder_nexus.plugin_build import build_variant

    target = build_variant("fe-flutter", "workspace", tmp_path)
    spec = json.loads((target / "projection.json").read_text(encoding="utf-8"))
    assert spec["problems"] == []
    files = target / "files"
    skills = files / ".agents/plugins/coder-nexus-fe/skills"
    names = {p.name for p in skills.iterdir()}
    assert {"flutter-core-usage", "flutter-clean-architecture", "work-items", "feature-planner"} <= names
    assert "core-usage" not in names and "clean-architecture" not in names
    assert "name: flutter-core-usage" in (skills / "flutter-core-usage/SKILL.md").read_text(encoding="utf-8")
    for agent in (files / ".agents/agents").glob("*.md"):
        text = agent.read_text(encoding="utf-8")
        assert "{{slot:" not in text
        frontmatter = text.split("---", 2)[1]
        skill_block = frontmatter.split("skills:", 1)[1].split("tools:", 1)[0]
        for line in skill_block.splitlines():
            name = line.strip().removeprefix("- ").strip()
            if name:
                assert name in names, (agent.name, name)


def test_preview_pack_gaps_are_reported_not_hidden(tmp_path):
    from coder_nexus.plugin_build import build_variant

    target = build_variant("fe-frappe", "workspace", tmp_path)
    problems = json.loads((target / "projection.json").read_text(encoding="utf-8"))["problems"]
    assert any("declares missing skill frappe-core-usage" in p for p in problems)
    assert (target / "files/.agents/plugins/coder-nexus-fe/skills/frappe-ui-catalog/SKILL.md").is_file()
