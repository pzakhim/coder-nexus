"""Tests for the Skill Factory: library integrity and `skill-factory list | get`."""

import json
import os
from pathlib import Path
import re

import pytest

from skill_factory import cli
from skill_factory.catalog import CORE_DIR, GENERATORS_DIR, LIBRARY_DIR, CatalogError, list_generators, load_packages, resolve
from skill_factory.installer import GLOBAL_CORE_REF, WORKSPACE_CORE_DIR

from .rendered import rendered_agent

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
LINK_RE = re.compile(r"\]\(([^)#\s{]+)\)")
CORE_REF_RE = re.compile(re.escape(GLOBAL_CORE_REF) + r"([A-Za-z0-9_./-]+[A-Za-z])")
CODER = [
    "create-clean-architecture-skill",
    "create-incremental-implementation-skill",
    "create-clean-code-skill",
    "create-unit-testing-skill",
    "create-code-simplification-skill",
    "create-bug-hunt-skill",
    "create-root-cause-debugging-skill",
    "create-secure-coding-standards-skill",
    "create-database-migrations-skill",
]
NON_CODER = ["create-code-review-skill", "create-security-review-skill"]
ALL = CODER + NON_CODER


def run(capsys, *argv: str) -> tuple[int, str, str]:
    code = cli.main(list(argv))
    out, err = capsys.readouterr()
    return code, out, err


# --- library integrity -------------------------------------------------------


def test_every_generator_is_well_formed():
    generators = list_generators()
    assert [g.name for g in generators] == sorted(ALL)
    for g in generators:
        assert g.name == g.path.name, f"{g.path}: frontmatter name differs from the folder"
        assert SEMVER_RE.match(g.version), f"{g.name}: VERSION {g.version!r} is not semver"
        assert g.description, f"{g.name}: missing description"
        changelog = (g.path / "CHANGELOG.md").read_text(encoding="utf-8")
        assert f"## {g.version} " in changelog, f"{g.name}: CHANGELOG has no entry for {g.version}"
        assert (g.path / "checklist.md").is_file()


def test_packages_reference_existing_generators():
    packages = load_packages()
    assert packages["coder"] == CODER
    assert set(packages["reviewer"]) >= {"create-code-review-skill", "create-bug-hunt-skill"}
    assert set(packages["security"]) == {"create-secure-coding-standards-skill", "create-security-review-skill"}
    for members in packages.values():
        for name in members:
            assert (GENERATORS_DIR / name / "SKILL.md").is_file(), f"package member {name} does not exist"


def test_library_links_and_core_references_resolve():
    for doc in LIBRARY_DIR.rglob("*"):
        if doc.suffix not in {".md", ".tmpl"}:
            continue
        text = doc.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if "://" not in target:
                assert (doc.parent / target).resolve().exists(), f"{doc}: broken link {target}"
        for ref in CORE_REF_RE.findall(text):
            assert (CORE_DIR / ref).exists(), f"{doc}: {GLOBAL_CORE_REF}{ref} does not exist in core/"


def test_frontmatter_is_valid_plain_yaml():
    """Unquoted `: ` or ` #` inside a frontmatter value breaks strict YAML parsers (the v2.9.2 bug)."""
    for doc in [*GENERATORS_DIR.rglob("SKILL.md"), *GENERATORS_DIR.rglob("SKILL*.tmpl")]:
        frontmatter = doc.read_text(encoding="utf-8").split("---", 2)[1]
        for line in frontmatter.strip().splitlines():
            key, _, value = line.partition(": ")
            if value and value[0] not in "\"'":
                assert ": " not in value and " #" not in value, f"{doc}: unquoted ': ' or ' #' in {key}"


def test_every_template_states_why_it_exists():
    for template in GENERATORS_DIR.rglob("*.tmpl"):
        assert "<!-- GEN: Why:" in template.read_text(encoding="utf-8"), f"{template}: missing Why note"


def test_skill_factory_does_not_depend_on_coder_nexus():
    for module in (LIBRARY_DIR.parent).glob("*.py"):
        assert "coder_nexus" not in module.read_text(encoding="utf-8"), f"{module} imports coder_nexus"


def test_roles_let_workspace_skills_override_fixed_skills():
    for role in ("code_writer.md", "code_reviewer.md"):
        content = rendered_agent(role)
        assert "## Workspace skills override" in content
        assert ".agents/skills/" in content and "skill-factory get" in content


# --- list --------------------------------------------------------------------


def test_list_shows_all_generators(capsys):
    code, out, _ = run(capsys, "list")
    assert code == 0
    for name in CODER:
        assert name in out


def test_list_package_as_json(capsys):
    code, out, _ = run(capsys, "list", "-p", "coder", "--json")
    rows = json.loads(out)
    assert code == 0
    assert [r["name"] for r in rows] == CODER
    assert all("coder" in r["packages"] and SEMVER_RE.match(r["version"]) for r in rows)


def test_list_unknown_package_is_a_usage_error(capsys):
    code, _, err = run(capsys, "list", "-p", "codr")
    assert code == 2
    assert "Unknown package 'codr'" in err and "coder" in err


# --- get ---------------------------------------------------------------------


def test_get_short_name_copies_generator_core_and_link(tmp_path, capsys):
    code, out, _ = run(capsys, "get", "clean-code", "--workspace", str(tmp_path))
    dest = tmp_path / ".agents" / "skills" / "create-clean-code-skill"
    assert code == 0
    assert (dest / "SKILL.md").is_file() and (dest / "VERSION").is_file()
    assert (tmp_path / WORKSPACE_CORE_DIR / "workflow.md").is_file()
    copied = "".join(p.read_text(encoding="utf-8") for p in dest.rglob("*") if p.suffix in {".md", ".tmpl"})
    assert GLOBAL_CORE_REF not in copied
    assert f"{WORKSPACE_CORE_DIR.as_posix()}/workflow.md" in copied
    link = tmp_path / ".claude" / "skills" / "create-clean-code-skill"
    assert link.is_symlink() and not os.path.isabs(os.readlink(link))
    assert (link / "SKILL.md").is_file()
    assert "Next: run a generator" in out


def test_get_several_skills_with_flag(tmp_path, capsys):
    code, _, _ = run(capsys, "get", "-s", "clean-code", "create-bug-hunt-skill", "--workspace", str(tmp_path), "--no-claude-link")
    skills = tmp_path / ".agents" / "skills"
    assert code == 0
    assert sorted(p.name for p in skills.iterdir()) == ["create-bug-hunt-skill", "create-clean-code-skill"]
    assert not (tmp_path / ".claude").exists()


def test_get_package_and_get_all(tmp_path, capsys):
    package_ws, all_ws = tmp_path / "pkg", tmp_path / "all"
    assert run(capsys, "get", "-p", "coder", "--workspace", str(package_ws))[0] == 0
    assert run(capsys, "get", ".", "--workspace", str(all_ws))[0] == 0
    assert sorted(p.name for p in (package_ws / ".agents" / "skills").iterdir()) == sorted(CODER)
    assert sorted(p.name for p in (all_ws / ".agents" / "skills").iterdir()) == sorted(ALL)


def test_get_existing_copy_is_kept_unless_forced(tmp_path, capsys):
    run(capsys, "get", "clean-code", "--workspace", str(tmp_path))
    skill = tmp_path / ".agents" / "skills" / "create-clean-code-skill" / "SKILL.md"
    core = tmp_path / WORKSPACE_CORE_DIR / "workflow.md"
    skill.write_text("my edit", encoding="utf-8")
    core.write_text("my core edit", encoding="utf-8")

    code, _, err = run(capsys, "get", "clean-code", "--workspace", str(tmp_path))
    assert code == 1 and "already exists" in err
    assert skill.read_text(encoding="utf-8") == "my edit"

    run(capsys, "get", "unit-testing", "--workspace", str(tmp_path))
    assert core.read_text(encoding="utf-8") == "my core edit", "core is copied once, not refreshed"

    code, _, _ = run(capsys, "get", "clean-code", "--workspace", str(tmp_path), "--force")
    assert code == 0
    assert skill.read_text(encoding="utf-8") != "my edit"
    assert core.read_text(encoding="utf-8") != "my core edit"


@pytest.mark.parametrize(
    "argv, message",
    [
        (["get"], "Nothing to get"),
        (["get", ".", "clean-code"], "`.` means every generator"),
        (["get", ".", "-p", "coder"], "`.` means every generator"),
        (["get", "-s", "clean-code", "-p", "coder"], "not both"),
        (["get", "clen-code"], "Did you mean: clean-code"),
    ],
)
def test_get_usage_errors(tmp_path, capsys, argv, message):
    code, _, err = run(capsys, *argv, "--workspace", str(tmp_path))
    assert code == 2
    assert message in err
    assert not (tmp_path / ".agents").exists()


def test_resolve_accepts_full_and_short_names_once():
    assert [g.name for g in resolve(["clean-code", "create-clean-code-skill"])] == ["create-clean-code-skill"]
    with pytest.raises(CatalogError):
        resolve(["nope"])
