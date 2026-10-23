"""The core-package-usage skill ships in the FE bundle and the Flutter agents route through it."""

import json
from pathlib import Path

from .rendered import rendered_agent

PLUGIN = Path(__file__).resolve().parent.parent / "plugins"


def test_core_usage_skill_is_bundled_and_wired():
    skill = PLUGIN / "packs" / "flutter" / "skills" / "core-package-usage" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    assert text.startswith("---\nname: core-package-usage\n")
    assert "coder-nexus setup flutter --check" in text
    assert "guidance/GUIDE.md" in text
    assert "app_core" in text and "app_ui_kit" in text

    manifest = json.loads((PLUGIN / "core" / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert "flutter/core-package-usage" in manifest["public_skills"]
    assert "packs/flutter/skills/core-package-usage/SKILL.md" in manifest["required_resources"]

    for agent in ("planning.md", "code_writer.md", "code_reviewer.md"):
        body = rendered_agent(agent)
        assert "core-package-usage" in body, agent
        assert "BaseBlocState" not in body, agent
        assert "app-core/references" not in body, agent  # old layout, removed


def test_profile_handoff_and_review_boundaries_are_consistent():
    """Guard the instruction paths that previously reintroduced company gates or mutating review."""
    skill = (PLUGIN / "packs/flutter/skills/core-package-usage/SKILL.md").read_text()
    assert "their existence never selects this profile" in skill
    assert "empty `core/`, `shared/` or `common/` directory alone is not evidence" in skill
    for template in ("architecture-design", "delivery-workflow"):
        design = next(iter([*(PLUGIN / "core" / "skills").glob(f"{template}/templates/design.md.tpl"), *(PLUGIN / "packs").glob(f"*/skills/{template}/templates/design.md.tpl")])).read_text()
        assert "architecture_profile:" in design
        assert "evidence:" in design
    reviewer = rendered_agent("code_reviewer.md")
    frontmatter = reviewer.split("---", 2)[1]
    assert "replace_file_content" not in frontmatter
    assert "Reviewer does not ask to start or trigger the next phase" in reviewer
    assert "explicit `architecture_profile`" in (PLUGIN / "packs/flutter/skills/code-review/SKILL.md").read_text()
    coordinator = (PLUGIN / "core/skills/dev-team/SKILL.md").read_text()
    assert "sole owner of phase continuation" in coordinator
    assert "shared_contracts/api_handshake_protocol.md" in coordinator
    for path in ("core/agents/test_runner.md", "packs/flutter/skills/visual-quality/SKILL.md"):
        text = rendered_agent(path.removeprefix("core/agents/")) if path.startswith("core/agents/") else (PLUGIN / path).read_text()
        assert "shared_contracts/api_handshake_protocol.md" in text
        assert "UI/contract" in text and "live" in text
