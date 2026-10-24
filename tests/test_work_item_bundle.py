"""Client work-item routing and packaging contracts."""

import argparse
from pathlib import Path

from coder_nexus.plugin_install import cmd_install_plugin


PLUGIN = Path(__file__).resolve().parent.parent / "plugins"
SKILL = PLUGIN / "core" / "skills" / "work-item-contract"
ITEM = ".superpowers/work-items/<slug>/vN/"


def test_new_router_covers_types_and_optional_plan():
    router = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    contract = (SKILL / "references/work-item-contract.md").read_text(encoding="utf-8")
    sequences = (SKILL / "references/type-sequences.md").read_text(encoding="utf-8")
    planning = (PLUGIN / "core/agents/planning.md").read_text(encoding="utf-8")
    assert ITEM in router
    for kind in ("feature", "bugfix", "refactor", "optimization", "migration", "maintenance", "investigation", "documentation"):
        assert f"`{kind}`" in contract
        assert f"`{kind}`" in sequences
    assert "Gate 1" in router and "Gate 2" in router and "Gate 3" in router
    assert "`design.md` - required for `feature`" in router
    assert "`implementation-plan.md` and **all linked** `phases/*.md` - required for `feature`" in router
    assert "codebase-notes.md" in router and "grilling" in contract
    assert "codebase-notes.md" in contract and "Question Queue" in contract
    assert "SKIPPED" in planning and "brief.md" in planning
    assert "baseline" in sequences and "regression" in sequences
    assert "Docs Writer" in router


def test_tool_reference_respects_public_validator_boundary():
    guide = (SKILL / "references/tool-usage.md").read_text(encoding="utf-8")
    for tool in ("huly_get_task_detail", "get_project_structure", "get_ux_error_patterns", "validate_proposal_spec", "validate_plan_slices", "validate_architecture_code", "validate_module_architecture"):
        assert f"`{tool}`" in guide
    assert "generic `brief.md`" in guide
    assert "cannot validate a brief-only item" in guide


def test_workspace_install_copies_all_eight_profiles(tmp_path):
    assert cmd_install_plugin(argparse.Namespace(is_global=False, workspace=str(tmp_path))) == 0
    client_agents = tmp_path / ".agents/agents"
    bundled = {path.name for path in (PLUGIN / "core" / "agents").glob("*.md")}
    assert bundled == {"spec_writer.md", "planning.md", "code_writer.md", "code_reviewer.md", "test_runner.md", "docs_writer.md", "designer.md", "bug_fixer.md"}
    assert {path.name for path in client_agents.glob("*.md")} == bundled
    assert (tmp_path / ".agents/plugins/coder-nexus/skills/work-item-contract/references/tool-usage.md").is_file()
