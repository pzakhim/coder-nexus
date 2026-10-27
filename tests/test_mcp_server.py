"""Tests for AIFactory MCP Server Hub tools (Read-Only & Zero Mock Data)."""

import pytest
from unittest.mock import AsyncMock, patch

from coder_nexus.server import app, huly_get_my_tasks, huly_get_task_detail
from coder_nexus.huly.models import HulyTaskSummary, HulyTaskDetail


@pytest.mark.anyio
async def test_mcp_server_tools_registered():
    """Verify that both read-only Huly tools are registered on the MCPServer."""
    tools = await app.list_tools()
    tool_names = [t.name for t in tools]
    assert "huly_get_my_tasks" in tool_names
    assert "huly_get_task_detail" in tool_names
    assert "get_project_structure" in tool_names
    assert "get_ux_error_patterns" in tool_names
    assert "validate_architecture_code" in tool_names
    assert "validate_proposal_spec" in tool_names
    assert "validate_plan_slices" in tool_names
    assert "validate_module_architecture" in tool_names
    assert "validate_ux_design" not in tool_names
    assert len(tool_names) == 8
    # Verify no write/mutation tools exist
    assert "huly_create_task" not in tool_names
    assert "huly_update_task" not in tool_names
    assert "huly_delete_task" not in tool_names


@pytest.mark.anyio
async def test_get_my_tasks_success():
    """Test huly_get_my_tasks returns structured task list on success."""
    fake_tasks = [
        HulyTaskSummary(
            id="GAME-1",
            title="Setup flutter project",
            status="TODO",
            priority="HIGH",
            assignee="jane.doe",
            due_date=None,
        ),
        HulyTaskSummary(
            id="GAME-2",
            title="Design system theme",
            status="IN_PROGRESS",
            priority="MEDIUM",
            assignee="jane.doe",
            due_date=None,
        ),
    ]

    with patch("coder_nexus.server.HulyClient.from_workspace") as mock_from_ws:
        mock_client = AsyncMock()
        mock_client.get_my_uncompleted_tasks.return_value = fake_tasks
        mock_from_ws.return_value = mock_client

        res = await huly_get_my_tasks(workspace_path="/fake/workspace")

        assert res["status"] == "success"
        assert res["total"] == 2
        assert len(res["tasks"]) == 2
        assert res["tasks"][0]["id"] == "GAME-1"
        assert res["tasks"][0]["title"] == "Setup flutter project"
        assert res["tasks"][1]["status"] == "IN_PROGRESS"


@pytest.mark.anyio
async def test_get_my_tasks_unauthenticated_fails_fast():
    """Test huly_get_my_tasks fails fast with clean error and hint when unauthenticated."""
    with patch("coder_nexus.server.HulyClient.from_workspace") as mock_from_ws:
        mock_client = AsyncMock()
        mock_client.get_my_uncompleted_tasks.side_effect = ValueError(
            "Not authenticated. Please run 'coder-nexus login' first."
        )
        mock_from_ws.return_value = mock_client

        res = await huly_get_my_tasks(workspace_path="/unauth/workspace")

        assert res["status"] == "error"
        assert "Not authenticated" in res["error"]
        assert "hint" in res
        assert ".env" in res["hint"]


@pytest.mark.anyio
async def test_get_task_detail_empty_id():
    """Test huly_get_task_detail validation when task_id is empty."""
    res = await huly_get_task_detail(task_id="   ")
    assert res["status"] == "error"
    assert "task_id is required" in res["error"]


@pytest.mark.anyio
async def test_get_task_detail_success():
    """Test huly_get_task_detail returns full description and acceptance criteria."""
    fake_detail = HulyTaskDetail(
        id="GAME-1",
        title="Setup flutter project",
        description="Project setup instructions with acceptance checklist:\n- [ ] Init git\n- [ ] Setup clean arch",
        status="TODO",
        priority="HIGH",
        assignee="jane.doe",
        acceptance_criteria=["Init git", "Setup clean arch"],
        figma_url="https://www.figma.com/design/sample-frame",
    )

    with patch("coder_nexus.server.HulyClient.from_workspace") as mock_from_ws:
        mock_client = AsyncMock()
        mock_client.get_task_detail.return_value = fake_detail
        mock_from_ws.return_value = mock_client

        res = await huly_get_task_detail(task_id="GAME-1", workspace_path="/fake/workspace")

        assert res["status"] == "success"
        task = res["task"]
        assert task["id"] == "GAME-1"
        assert task["title"] == "Setup flutter project"
        assert task["status"] == "TODO"
        assert len(task["acceptance_criteria"]) == 2
        assert "Init git" in task["acceptance_criteria"]
        assert task["figma_url"] == "https://www.figma.com/design/sample-frame"


@pytest.mark.anyio
async def test_get_task_detail_not_found():
    """Test huly_get_task_detail fails fast when task does not exist."""
    with patch("coder_nexus.server.HulyClient.from_workspace") as mock_from_ws:
        mock_client = AsyncMock()
        mock_client.get_task_detail.side_effect = ValueError("Task 'INVALID-999' not found in Huly workspace.")
        mock_from_ws.return_value = mock_client

        res = await huly_get_task_detail(task_id="INVALID-999")

        assert res["status"] == "error"
        assert "not found" in res["error"]
        assert "hint" in res


@pytest.mark.anyio
async def test_mcp_call_tool_dispatch():
    """Test invoking tools via MCPServer.call_tool interface directly."""
    fake_tasks = [
        HulyTaskSummary(
            id="HULY-1",
            title="Verify MCP server",
            status="TODO",
            priority="HIGH",
        )
    ]

    with patch("coder_nexus.server.HulyClient.from_workspace") as mock_from_ws:
        mock_client = AsyncMock()
        mock_client.get_my_uncompleted_tasks.return_value = fake_tasks
        mock_from_ws.return_value = mock_client

        call_result = await app.call_tool("huly_get_my_tasks", {"workspace_path": ""})
        assert call_result.is_error is False
        assert len(call_result.content) > 0
        content_text = call_result.content[0].text
        assert "HULY-1" in content_text
        assert "Verify MCP server" in content_text


@pytest.mark.anyio
async def test_mcp_get_project_structure_dispatch():
    """Test invoking get_project_structure via MCPServer.call_tool interface."""
    call_result = await app.call_tool("get_project_structure", {"scope": "module", "feature_name": "inventory"})
    assert call_result.is_error is False
    assert len(call_result.content) > 0
    content_text = call_result.content[0].text
    assert "Inventory" in content_text
    assert "inventory_entity.dart" in content_text




@pytest.mark.anyio
async def test_mcp_get_ux_error_patterns_dispatch():
    """Test invoking get_ux_error_patterns via MCPServer.call_tool interface."""
    call_result = await app.call_tool("get_ux_error_patterns", {"scenario": "auth_failure"})
    assert call_result.is_error is False
    assert len(call_result.content) > 0
    content_text = call_result.content[0].text
    assert "auth_failure" in content_text
    assert "errorText" in content_text


@pytest.mark.anyio
async def test_mcp_validate_architecture_code_dispatch():
    """Test invoking validate_architecture_code via MCPServer.call_tool interface."""
    dart_code = (
        "import 'package:flutter/material.dart';\n"
        "class MyEntity {}\n"
    )
    call_result = await app.call_tool(
        "validate_architecture_code",
        {"dart_code": dart_code, "layer": "domain"}
    )
    assert call_result.is_error is False
    assert len(call_result.content) > 0
    content_text = call_result.content[0].text
    assert "DOM-001" in content_text
    assert "Domain layer must not import or export Flutter framework" in content_text
    assert '"gate_status": "FAILED"' in content_text
    assert '"syntax_status": "NOT_CHECKED"' in content_text


@pytest.mark.anyio
async def test_mcp_validate_proposal_spec_dispatch():
    """Test invoking validate_proposal_spec via MCPServer.call_tool interface."""
    bad_proposal = "# Proposal\nTrạng thái: 🟢 APPROVED_BY_SPEC\n"
    call_result = await app.call_tool(
        "validate_proposal_spec",
        {"proposal_content": bad_proposal, "feature_name": "auth"}
    )
    assert call_result.is_error is False
    assert len(call_result.content) > 0
    content_text = call_result.content[0].text
    assert "SPEC-002" in content_text
    assert '"gate_status": "FAILED"' in content_text


@pytest.mark.anyio
async def test_mcp_validate_plan_slices_dispatch():
    """Test invoking validate_plan_slices via MCPServer.call_tool interface."""
    bare_tasks = "- [ ] Task 01: Do something\n"
    call_result = await app.call_tool(
        "validate_plan_slices",
        {"plan_content": "", "task_content": bare_tasks, "feature_name": "auth"}
    )
    assert call_result.is_error is False
    assert len(call_result.content) > 0
    content_text = call_result.content[0].text
    assert "PLAN-002" in content_text
    assert '"gate_status": "FAILED"' in content_text


@pytest.mark.anyio
async def test_mcp_validate_module_architecture_dispatch():
    """Test invoking validate_module_architecture via MCPServer.call_tool interface."""
    call_result = await app.call_tool(
        "validate_module_architecture",
        {"module_path": "/nonexistent/path", "feature_name": "auth"}
    )
    assert call_result.is_error is False
    assert len(call_result.content) > 0
    content_text = call_result.content[0].text
    assert '"status": "error"' in content_text
