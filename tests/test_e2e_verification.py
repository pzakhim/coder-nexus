"""End-to-End verification test suite for AIFactory Coder (Sprint 01)."""

import json
from pathlib import Path
import subprocess
import pytest

from coder_nexus.server import app


REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_ENV_FILE = REPO_ROOT / "scratch" / "test_flutter_app" / ".env"


def test_e2e_stdio_handshake():
    """Verify that launching `coder-nexus serve` via stdio responds to JSON-RPC 2.0 handshake."""
    proc = subprocess.Popen(
        ["uv", "run", "--offline", "coder-nexus", "serve"],
        cwd=str(REPO_ROOT),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # 1. initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"},
            },
        }
        proc.stdin.write(json.dumps(init_req) + "\n")
        proc.stdin.flush()

        init_resp = json.loads(proc.stdout.readline())
        assert init_resp.get("jsonrpc") == "2.0"
        assert init_resp.get("id") == 1
        assert "serverInfo" in init_resp.get("result", {})
        assert init_resp["result"]["serverInfo"]["name"] == "coder-nexus"

        # 2. initialized notification
        proc.stdin.write(
            json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n"
        )
        proc.stdin.flush()

        # 3. tools/list
        proc.stdin.write(
            json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n"
        )
        proc.stdin.flush()

        tools_resp = json.loads(proc.stdout.readline())
        assert tools_resp.get("jsonrpc") == "2.0"
        assert tools_resp.get("id") == 2
        tool_names = [t["name"] for t in tools_resp["result"]["tools"]]
        assert "huly_get_my_tasks" in tool_names
        assert "huly_get_task_detail" in tool_names
        assert "get_project_structure" in tool_names
        assert "get_ux_error_patterns" in tool_names
        assert "validate_architecture_code" in tool_names
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_e2e_stdio_catalog_tool_calls():
    """Verify that MCP tools execute correctly over stdio JSON-RPC 2.0 transport."""
    proc = subprocess.Popen(
        ["uv", "run", "coder-nexus", "serve"],
        cwd=str(REPO_ROOT),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # 1. initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"},
            },
        }
        proc.stdin.write(json.dumps(init_req) + "\n")
        proc.stdin.flush()
        _ = json.loads(proc.stdout.readline())

        # 2. initialized notification
        proc.stdin.write(
            json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n"
        )
        proc.stdin.flush()

        # 3. Call get_project_structure over stdio
        struct_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_project_structure",
                "arguments": {"scope": "module", "feature_name": "inventory"},
            },
        }
        proc.stdin.write(json.dumps(struct_req) + "\n")
        proc.stdin.flush()
        struct_resp = json.loads(proc.stdout.readline())
        assert struct_resp.get("id") == 3
        struct_content = json.loads(struct_resp["result"]["content"][0]["text"])
        assert struct_content["status"] == "success"
        assert struct_content["feature_name"] == "inventory"

        # 6. Call get_ux_error_patterns over stdio
        ux_req = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "get_ux_error_patterns",
                "arguments": {"scenario": "auth_failure"},
            },
        }
        proc.stdin.write(json.dumps(ux_req) + "\n")
        proc.stdin.flush()
        ux_resp = json.loads(proc.stdout.readline())
        assert ux_resp.get("id") == 6
        ux_content = json.loads(ux_resp["result"]["content"][0]["text"])
        assert ux_content["status"] == "success"
        assert "Cubit state convention" in ux_content["pattern"]["bloc_state_pattern"]

        # 7. Call validate_architecture_code over stdio
        val_req = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "validate_architecture_code",
                "arguments": {
                    "dart_code": "import 'package:flutter/widgets.dart';\nclass E {}",
                    "layer": "domain",
                },
            },
        }
        proc.stdin.write(json.dumps(val_req) + "\n")
        proc.stdin.flush()
        val_resp = json.loads(proc.stdout.readline())
        assert val_resp.get("id") == 7
        val_content = json.loads(val_resp["result"]["content"][0]["text"])
        assert val_content["status"] == "success"
        assert val_content["valid"] is False
        assert val_content["gate_status"] == "FAILED"
        assert val_content["syntax_status"] == "NOT_CHECKED"
        assert any(v["rule_id"] == "DOM-001" for v in val_content["violations"])
    finally:
        proc.terminate()
        proc.wait(timeout=5)


@pytest.mark.anyio
async def test_e2e_fail_fast_missing_env():
    """Verify Fail-Fast behavior when querying without credentials."""
    res = await app.call_tool("huly_get_my_tasks", {"workspace_path": "/tmp/non_existent_workspace_dir"})
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["status"] == "error"
    assert "Not authenticated" in data["error"]
    assert "hint" in data


@pytest.mark.anyio
async def test_e2e_fail_fast_invalid_task():
    """Verify Fail-Fast behavior when requesting a task that does not exist."""
    res = await app.call_tool("huly_get_task_detail", {"task_id": "INVALID-99999", "workspace_path": "/tmp"})
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["status"] == "error"
    assert "hint" in data


@pytest.mark.anyio
async def test_e2e_live_query_with_scratch_env():
    """Verify live task query and detail extraction against real Huly instance if .env is present."""
    if not TEST_ENV_FILE.exists():
        pytest.skip("No live test .env found in scratch/test_flutter_app")

    workspace_dir = str(TEST_ENV_FILE.parent)

    # 1. Fetch open tasks of the workspace (the test account may have none assigned)
    tasks_res = await app.call_tool("huly_get_my_tasks", {"workspace_path": workspace_dir, "include_all": True})
    assert tasks_res.is_error is False
    tasks_data = json.loads(tasks_res.content[0].text)
    assert tasks_data["status"] == "success"
    assert tasks_data["total"] > 0
    first_task = tasks_data["tasks"][0]
    task_id = first_task["id"]
    assert task_id

    # 2. Fetch detail of first task
    detail_res = await app.call_tool("huly_get_task_detail", {"task_id": task_id, "workspace_path": workspace_dir})
    assert detail_res.is_error is False
    detail_data = json.loads(detail_res.content[0].text)
    assert detail_data["status"] == "success"
    task_info = detail_data["task"]
    assert task_info["id"] == task_id
    assert task_info["title"]
    assert isinstance(task_info["acceptance_criteria"], list)
