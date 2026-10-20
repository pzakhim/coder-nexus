"""Coder Nexus MCP Server Hub - Read-Only Huly Task Runner.

Exposes Model Context Protocol (MCP) tools over stdio transport.
Adheres strictly to Read-Only operations and Zero Mock Data.
"""

from pathlib import Path
import os
from typing import Any, Optional
from mcp.server.mcpserver import MCPServer
from .architecture.module_validator import module_architecture_validator
from .architecture.spec_validator import spec_validator
from .architecture.structure import get_project_structure_data
from .architecture.validator import architecture_validator
from .ux_patterns import get_ux_pattern
from .huly.client import HulyClient

app = MCPServer("coder-nexus")


@app.tool()
async def huly_get_my_tasks(workspace_path: str = "") -> dict[str, Any]:
    """Fetch uncompleted tasks (TODO, IN_PROGRESS, etc.) for the current user from Huly.

    Strictly READ-ONLY: Never modifies tasks on Huly.
    Zero Mock Data: Fails fast if credentials are not configured or network error occurs.

    Args:
        include_sub_issues: Also return direct child issues (one level) with their own criteria.
                            A parent issue is one feature: write one spec and use the children as
                            planning input. A child issue: scope the spec to it; parent is context only.
        workspace_path: Path to the Flutter developer workspace containing .env file.
                       Defaults to current working directory if empty.

    Returns:
        A dictionary containing task count and list of uncompleted tasks with ID, title, status, and priority.
    """
    path = workspace_path.strip() or None
    try:
        client = HulyClient.from_workspace(path)
        tasks = await client.get_my_uncompleted_tasks(path)
        return {
            "status": "success",
            "total": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "priority": t.priority,
                    "assignee": t.assignee,
                    "due_date": t.due_date,
                }
                for t in tasks
            ],
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "hint": (
                "Ensure your Flutter workspace has a valid .env file with HULY_WORKSPACE_URL, "
                "HULY_EMAIL, and HULY_PASSWORD, or run 'coder-nexus setup huly' in your workspace."
            ),
        }


def default_sources_dir(workspace_path: Optional[str], task_id: str) -> Path:
    """Where `download=True` saves ticket sources: <workspace>/.superpowers/sources/<ISSUE-ID>/."""
    from .huly.client import parse_task_ref
    base = Path(workspace_path).resolve() if workspace_path else Path.cwd()
    return base / ".superpowers" / "sources" / parse_task_ref(task_id).replace("/", "_")


SOURCES_GITIGNORE = "# Downloaded Huly sources (PDFs, images, PO docs): local only, never committed.\n*\n"


def ensure_sources_ignored(sources_dir: Path) -> None:
    """Keep `.superpowers/sources/` out of Git without touching the project's own .gitignore."""
    root = sources_dir.parent
    root.mkdir(parents=True, exist_ok=True)
    marker = root / ".gitignore"
    if not marker.exists():
        marker.write_text(SOURCES_GITIGNORE, encoding="utf-8")


@app.tool()
async def huly_get_task_detail(
    task_id: str,
    workspace_path: str = "",
    include_sub_issues: bool = True,
    download: bool = False,
) -> dict[str, Any]:
    """Read the FULL context of one Huly issue the user names (READ-ONLY on Huly).

    Returns: title, description text, status name + category, priority, assignee name, due date,
    explicit acceptance criteria (with source), parent, direct sub-issues (status, assignee, AC),
    comments (author, time, text) and `sources`: every PO document mention, image, attachment,
    file link (e.g. a PDF linked in a comment) and external link the ticket points to, each with
    a status: READ (document text included), DOWNLOADED (saved file path), AVAILABLE (call again
    with download=true), UNREACHABLE (this account cannot open it: ask the user) or EXTERNAL.

    Args:
        task_id: The issue the user named: an ID ('APP-123'), a number ('123', only if unique),
                 a Huly _id, or a Huly issue link pasted from the browser.
        workspace_path: Client workspace containing the .env with Huly credentials.
        include_sub_issues: Also return direct child issues (one level) with their own criteria.
                            A parent issue is one feature: write one spec and use the children as
                            planning input. A child issue: scope the spec to it; parent is context only.
        download: Save files, images, attachments and readable documents to
                  <workspace>/.superpowers/sources/<ISSUE-ID>/ so they can be opened and read
                  (PDF, images). Use it before writing requirements.
    """
    clean_task_id = task_id.strip()
    if not clean_task_id:
        return {"status": "error", "error": "task_id is required."}

    path = workspace_path.strip() or None
    try:
        client = HulyClient.from_workspace(path)
        target_dir = None
        if download:
            sources_dir = default_sources_dir(path, clean_task_id)
            ensure_sources_ignored(sources_dir)
            target_dir = str(sources_dir)
        detail = await client.get_task_detail(clean_task_id, path, include_sub_issues=include_sub_issues, download_dir=target_dir)
        task = detail.model_dump()
        task["sub_issue_summary"] = {
            "total": len(detail.sub_issues),
            "open": sum(1 for c in detail.sub_issues if not c.is_closed),
            "closed": sum(1 for c in detail.sub_issues if c.is_closed),
        }
        task["source_summary"] = {
            st: sum(1 for x in detail.sources if x.status == st)
            for st in ("READ", "DOWNLOADED", "AVAILABLE", "UNREACHABLE", "EXTERNAL")
        }
        result: dict[str, Any] = {"status": "success", "task": task}
        if target_dir:
            result["sources_dir"] = target_dir
        return result
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "hint": (
                f"Verify that task '{clean_task_id}' exists in your active Huly workspace and that "
                "your credentials in .env are valid."
            ),
        }


@app.tool()
async def get_project_structure(scope: str, feature_name: str = "") -> dict[str, Any]:
    """Retrieve Clean Architecture blueprint and guidelines for Flutter project root or feature module.

    Strictly READ-ONLY: Never generates code or touches files in the workspace.
    Zero Mock Data: Returns verified blueprints with traceable source references.

    Args:
        scope: Either 'root' (top-level layout & boot sequence) or 'module' (feature module).
        feature_name: Name of the feature module in lower_snake_case (required if scope='module').

    Returns:
        A dictionary containing blueprint tree, DI order, and source citations.
    """
    return get_project_structure_data(scope=scope, feature_name=feature_name)


@app.tool()
async def get_ux_error_patterns(scenario: str) -> dict[str, Any]:
    """Retrieve UX design patterns, UI behaviors, and BLoC state transitions for error/edge scenarios.

    Args:
        scenario: Error or edge scenario identifier (e.g., 'auth_failure', 'network_timeout', 'form_validation', 'empty_state').

    Returns:
        Dictionary containing UI behavior guidance, BLoC state pattern, and anti-patterns.
    """
    return get_ux_pattern(scenario=scenario)


@app.tool()
async def validate_architecture_code(
    dart_code: str, layer: str, architecture_profile: str = "imespro",
) -> dict[str, Any]:
    """Validate Dart source code against enterprise Clean Architecture rules for a specific layer.

    Strictly READ-ONLY: Performs static analysis on the provided code string without writing files.
    Zero Mock Data: Fails fast on invalid inputs or malformed layers, returning structured violations.

    Args:
        dart_code: Full Dart source code to analyze.
        layer: Architecture layer ('domain', 'data', 'presentation', 'core', 'module').
        architecture_profile: Approved mode: imespro, external-structured, or external-standard.
            Omitted values retain legacy iMESPro checks. External Client conventions need manual verification.

    Returns:
        Dictionary with status, valid flag, list of violations, checked rules, and unsupported checks.
    """
    return architecture_validator.validate(dart_code=dart_code, layer=layer, architecture_profile=architecture_profile)


@app.tool()
async def validate_proposal_spec(
    proposal_content: str = "",
    proposal_path: str = "",
    feature_name: str = "",
) -> dict[str, Any]:
    """Validate versioned requirements, codebase-notes, change impact, or design Markdown; legacy proposals remain readable.

    Strictly READ-ONLY: Never modifies files in the workspace.
    Zero Mock Data: Fails fast on invalid inputs or malformed schemas, returning structured violations.
    Anti-Self-Approval: Detects and rejects unauthorized autonomous approvals (APPROVED_BY_SPEC).

    Args:
        proposal_content: Raw Markdown content of a requirements, codebase-notes, impact, design, or legacy proposal document.
        proposal_path: Optional path in docs/features/<module>/<feature>/vN/ or docs/work-items/<slug>/vN/ (legacy paths also supported).
        feature_name: Name of the feature module (optional).

    Returns:
        Dictionary containing structural validation status, violations, and checked rules; never user approval.
    """
    return spec_validator.validate_proposal(
        proposal_content=proposal_content,
        proposal_path=proposal_path,
        feature_name=feature_name,
    )


@app.tool()
async def validate_plan_slices(
    plan_content: str = "",
    plan_path: str = "",
    task_content: str = "",
    task_path: str = "",
    feature_name: str = "",
) -> dict[str, Any]:
    """Validate a versioned implementation plan and its linked behavior phases, or a legacy plan/task pair.

    Strictly READ-ONLY: Never modifies files in the workspace.
    Zero Mock Data: Fails fast on invalid inputs or malformed schemas, returning structured violations.
    Versioned plans map ACs to linked phases in one version directory. A scoped UI-only phase is valid.

    Args:
        plan_content: Raw text of implementation-plan.md or a legacy plan.
        plan_path: Optional path to docs/features/<module>/<feature>/vN/implementation-plan.md.
        task_content: Legacy task.md content; unused for versioned plans.
        task_path: Legacy task.md path; unused for versioned plans.
        feature_name: Name of the feature module (optional).

    Returns:
        Dictionary containing validation status, gate_status (PASSED/FAILED), violations, and checked rules.
    """
    return spec_validator.validate_plan(
        plan_content=plan_content,
        plan_path=plan_path,
        task_content=task_content,
        task_path=task_path,
        feature_name=feature_name,
    )


@app.tool()
async def validate_module_architecture(
    module_path: str = "",
    feature_name: str = "",
    architecture_profile: str = "imespro",
) -> dict[str, Any]:
    """Validate module boundaries using the approved architecture profile.

    iMESPro also checks its layer, screen and DI conventions. External layout/DI needs Client inspection.

    Strictly READ-ONLY: Performs static inspection of the module directory without writing files.
    Zero Mock Data: Fails fast if module directory does not exist or has invalid structure.

    Args:
        module_path: Path to the feature module directory (e.g. lib/modules/<feature>).
        feature_name: Name of the feature module (optional, inferred from path if omitted).
        architecture_profile: Approved mode: imespro, external-structured, or external-standard.
            Omitted values retain legacy iMESPro checks. External layout/DI checks remain UNVERIFIED.

    Returns:
        Dictionary containing validation status, gate_status (PASSED/FAILED), violations, and checked rules.
    """
    return module_architecture_validator.validate_module(
        module_path=module_path,
        feature_name=feature_name,
        architecture_profile=architecture_profile,
    )


def run_server() -> None:
    """Run the MCP server listening on stdio transport."""
    app.run(transport="stdio")


if __name__ == "__main__":
    run_server()
