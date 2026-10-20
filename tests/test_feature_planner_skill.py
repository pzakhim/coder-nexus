"""Contract checks for the packaged versioned feature planning workflow."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "coder-nexus-fe"
SKILLS = PLUGIN / "skills"
PLANNER = SKILLS / "shared" / "feature-planner"
FEATURE_PATH = "docs/features/<module>/<feature>/vN/"


def read(relative: str) -> str:
    return (PLUGIN / relative).read_text(encoding="utf-8")


def test_three_gates_and_versioned_handoff():
    router = read("skills/shared/feature-planner/SKILL.md")
    spec = read("agents/spec_writer.md")
    brainstorm = read("skills/shared/brainstorming/SKILL.md")
    planning = read("skills/shared/planning-and-task-breakdown/SKILL.md")
    rubric = read("skills/shared/feature-planner/references/02_interview_rubric_and_gates.md")
    for content in (router, brainstorm, planning, rubric):
        assert FEATURE_PATH in content
        assert "Gate 1" in content
        assert "Gate 2" in content
        assert "Gate 3" in content or content is brainstorm
        assert "APPROVED_BY_SPEC" in content or "actual user approval" in content or "user approval" in content
    assert "all linked phase files" in router
    assert "ask_question" in spec
    assert "Gate 1" in spec and "Gate 2" in spec
    assert "Planning owns task breakdown" in spec
    assert "Docs Writer records phase as-built evidence" in spec
    assert "coordinator owns status and approval references" in spec
    for stage in ("1A", "1B", "1C", "Mockoon", "grill-me", "codebase-notes.md"):
        assert stage in spec
        assert stage in brainstorm
        assert stage in read("skills/shared/dev-team/SKILL.md")
        assert stage in read("skills/shared/work-items/SKILL.md")
    planning_agent = read("agents/planning.md")
    coder_agent = read("agents/code_writer.md")
    arch_design = read("skills/flutter/architecture-design/SKILL.md")
    incremental = read("skills/shared/incremental-implementation/SKILL.md")
    phase_rules = read("skills/shared/planning-and-task-breakdown/references/01_phase_slicing_rules.md")
    phase_tpl = read("skills/shared/feature-planner/templates/phase.md.tpl")
    work_phase_tpl = read("skills/shared/work-items/templates/phase.md.tpl")
    assert "Pre-Design Counter-Review" in planning_agent
    assert "Pre-Design Counter-Review" in arch_design
    reviewer_agent = read("agents/code_reviewer.md")
    runner_agent = read("agents/test_runner.md")
    api_mocking_ref = read("skills/flutter/architecture-design/references/05_api_mocking_strategy.md")
    arch_design_tpl = read("skills/flutter/architecture-design/templates/design.md.tpl")
    for target in (planning_agent, coder_agent, reviewer_agent, api_mocking_ref, arch_design_tpl):
        assert "Mockoon Trigger & Test Data Table" in target
    for target in (planning_agent, planning, phase_rules, coder_agent, reviewer_agent, runner_agent):
        assert "PHASE-00" in target
        assert "phase-00-prepare.md" in target
    for target in (planning_agent, planning, phase_rules, coder_agent, reviewer_agent):
        assert "[EXECUTE]" in target
        assert "[x] PREPARED / COMPLETED" in target
    assert "does NOT use Mockoon payloads to run unit-level logic tests" in runner_agent
    for target in (planning_agent, coder_agent, planning, incremental, phase_rules, phase_tpl, work_phase_tpl):
        assert "[PARALLEL:" not in target
        assert "Join <Group>" not in target


def test_versioned_manifest_files_exist_and_legacy_is_explicit():
    manifest = json.loads((PLANNER / "references/manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "1.3.0"
    assert len(manifest["three_gate_approvals"]) == 3
    assert set(manifest["templates"]) == {
        "templates/requirements.md.tpl",
        "templates/change_impact.md.tpl",
        "templates/design.md.tpl",
        "templates/versioned_implementation_plan.md.tpl",
        "templates/phase.md.tpl",
        "templates/as_built.md.tpl",
        "templates/feature_readme.md.tpl",
    }
    for relative in manifest["templates"] + manifest["legacy_templates"] + manifest["references"]:
        assert (PLANNER / relative).is_file()
    for relative in manifest["legacy_templates"]:
        assert "LEGACY" in (PLANNER / relative).read_text(encoding="utf-8")


def test_templates_cover_version_impact_ac_and_real_evidence():
    tpl = PLANNER / "templates"
    requirements = (tpl / "requirements.md.tpl").read_text(encoding="utf-8")
    impact = (tpl / "change_impact.md.tpl").read_text(encoding="utf-8")
    plan = (tpl / "versioned_implementation_plan.md.tpl").read_text(encoding="utf-8")
    phase = (tpl / "phase.md.tpl").read_text(encoding="utf-8")
    built = (tpl / "as_built.md.tpl").read_text(encoding="utf-8")
    assert "Scope out" in requirements and "Acceptance criteria" in requirements
    assert "Baseline code revision" in impact and "Design versus actual code differences" in impact
    assert "AC coverage" in plan and "phases/" in plan
    assert "READY when" in phase and "Visual target/states" in phase
    assert "NOT_RUN" in built and "Code revision" in built or "code revision" in built
    for text in (requirements, impact, plan, phase, built):
        assert "PENDING_REVIEW" in text or "NOT_RUN" in text


def test_downstream_agents_read_same_version_and_write_actual_evidence():
    for relative in (
        "agents/code_writer.md",
        "agents/test_runner.md",
        "agents/code_reviewer.md",
        "skills/shared/incremental-implementation/SKILL.md",
        "skills/flutter/code-review/SKILL.md",
        "skills/flutter/verification/SKILL.md",
    ):
        content = read(relative)
        assert "vN/" in content or "version" in content.lower()
        assert "phase" in content.lower()
        assert "as-built.md" in content or "revision" in content.lower()
    runner = read("agents/test_runner.md")
    assert "read-only" in runner.lower()
    assert "NOT_RUN" in runner and "BLOCKED" in runner
    reviewer = read("agents/code_reviewer.md")
    assert "validate_architecture_code" in reviewer


def test_pre_release_visual_cases_keep_real_data_and_reviewed_goldens():
    runner = read("agents/test_runner.md")
    verification = read("skills/flutter/verification/SKILL.md")
    visual = read("skills/flutter/visual-verification/SKILL.md")
    report = read("skills/flutter/verification/templates/verification_report.md.tpl")
    phase = read("skills/shared/feature-planner/templates/phase.md.tpl")
    assert "Code Review report" in runner
    assert "test-case matrix" in runner
    assert "Remain read-only toward `lib/` and `test/`" in runner
    assert "present the actual images" in runner
    assert "`--update-goldens`" in verification
    assert "human-reviewed baseline" in verification
    assert "live-data screenshot" in visual
    assert "{{CASE_ROWS}}" in report
    assert "{{GOLDEN_BASELINE_AND_RESULT_OR_NA}}" in report
    assert "Test cases/data provenance" in phase


def test_visual_intake_and_reuse_stay_bound_to_real_sources():
    router = read("skills/shared/feature-planner/SKILL.md")
    brainstorm = read("skills/shared/brainstorming/SKILL.md")
    matrix = read("skills/shared/feature-planner/references/03_ui_ux_intake_and_discovery_matrix.md")
    for content in (router, brainstorm, matrix):
        assert "Visual Intake Gate" in content
        assert "VISUAL_INPUT_MISSING" in content
        assert "core-usage" in content or "app_ui_kit" in content
    assert "48x48 dp" in matrix
    assert "4.5:1" in matrix


def test_public_workflow_skills_are_portable():
    for name in (
        "brainstorming",
        "planning-and-task-breakdown",
        "incremental-implementation",
    ):
        content = (SKILLS / "shared" / name / "SKILL.md").read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert f"name: {name}" in content
        assert "file:///Users/" not in content
