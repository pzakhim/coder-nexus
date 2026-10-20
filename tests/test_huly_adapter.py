"""Unit and integration tests for real Huly Adapter and CLI (Zero Mock Data)."""

import argparse
import asyncio
from pathlib import Path
import pytest
import httpx

from coder_nexus.huly.auth import (
    load_client_credentials,
    save_client_credentials,
    parse_env_file,
)
from coder_nexus.huly.models import HulyCredentials, HulyTaskSummary, HulyTaskDetail
from coder_nexus.huly.client import (
    HulyClient,
    _extract_text_from_tiptap,
    _format_status,
    _format_priority,
)
from coder_nexus.setup.huly import cmd_login, cmd_status, cmd_my_tasks, cmd_task_detail


class TestAuthPersistence:
    """Tests for reading and writing client workspace .env files."""

    def test_save_and_load_new_env(self, tmp_path: Path):
        creds = HulyCredentials(
            workspace_url="https://huly.example.com/",
            email="developer@example.com",
            password="secretpassword",
            session_token="jwt-token-12345",
            workspace_id="ws-uuid-abc-123",
        )
        env_file = save_client_credentials(str(tmp_path), creds)
        assert env_file.exists()

        loaded = load_client_credentials(str(tmp_path))
        assert loaded.workspace_url == "https://huly.example.com/"
        assert loaded.email == "developer@example.com"
        assert loaded.password == "secretpassword"
        assert loaded.session_token == "jwt-token-12345"
        assert loaded.workspace_id == "ws-uuid-abc-123"
        assert loaded.is_authenticated is True

    def test_save_preserves_existing_keys_and_comments(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        initial_content = (
            "# Existing Flutter Config\n"
            "FLUTTER_API_BASE=https://api.factory.com\n"
            "SOME_CUSTOM_KEY=custom_value\n\n"
            "# Previous Huly\n"
            "HULY_EMAIL=old@example.com\n"
        )
        env_file.write_text(initial_content, encoding="utf-8")

        new_creds = HulyCredentials(
            workspace_url="https://huly.example.com/",
            email="jane.doe@example.com",
            password="new_password",
            session_token="new-token-999",
            workspace_id="new-ws-uuid",
        )
        save_client_credentials(str(tmp_path), new_creds)

        file_text = env_file.read_text(encoding="utf-8")
        assert "FLUTTER_API_BASE=https://api.factory.com" in file_text
        assert "SOME_CUSTOM_KEY=custom_value" in file_text
        assert "HULY_EMAIL=jane.doe@example.com" in file_text
        assert "HULY_WORKSPACE_ID=new-ws-uuid" in file_text
        assert "old@example.com" not in file_text

    def test_load_defaults_when_no_env_exists(self, tmp_path: Path):
        non_existent_dir = tmp_path / "empty_dir"
        loaded = load_client_credentials(str(non_existent_dir))
        assert loaded.workspace_url == "https://huly.app"
        assert loaded.email is None
        assert loaded.password is None
        assert loaded.session_token is None
        assert loaded.workspace_id is None
        assert loaded.is_authenticated is False


class TestHulyParsers:
    """Tests for normalizing status, priority, and rich text documents."""

    def test_format_status(self):
        assert _format_status("tracker:status:Backlog") == "BACKLOG"
        assert _format_status("tracker:status:Todo") == "TODO"
        assert _format_status("tracker:status:InProgress") == "INPROGRESS"
        assert _format_status("tracker:status:Done") == "DONE"
        assert _format_status("") == "TODO"

    def test_format_priority(self):
        # Huly IssuePriority enum
        assert _format_priority(0) == "NO_PRIORITY"
        assert _format_priority(1) == "URGENT"
        assert _format_priority(2) == "HIGH"
        assert _format_priority(3) == "MEDIUM"
        assert _format_priority(4) == "LOW"
        assert _format_priority("2") == "HIGH"

    def test_extract_tiptap_text_and_checklists(self):
        doc = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Feature Overview"}]
                },
                {
                    "type": "taskItem",
                    "attrs": {"checked": True},
                    "content": [{"type": "text", "text": "Handle HTTP 401 error"}]
                },
                {
                    "type": "taskItem",
                    "attrs": {"checked": False},
                    "content": [{"type": "text", "text": "Handle HTTP 500 error"}]
                }
            ]
        }
        lines = _extract_text_from_tiptap(doc)
        assert len(lines) == 3
        assert lines[0] == "Feature Overview"
        assert lines[1] == "[x] Handle HTTP 401 error"
        assert lines[2] == "[ ] Handle HTTP 500 error"


class TestHulyClientFailFast:
    """Tests to verify client fails fast with real exceptions without mocking."""

    def test_missing_credentials_raises_error(self):
        client = HulyClient()
        with pytest.raises(ValueError, match="Not authenticated"):
            asyncio.run(client.get_my_uncompleted_tasks())

    def test_missing_credentials_for_task_detail_raises_error(self):
        client = HulyClient()
        with pytest.raises(ValueError, match="Not authenticated"):
            asyncio.run(client.get_task_detail("GAME-1"))

    def test_login_requires_email_and_password(self):
        client = HulyClient()
        with pytest.raises(ValueError, match="Email and password are required"):
            asyncio.run(client.login(workspace_url="https://huly.app", email=None, password=None))

    def test_unreachable_server_raises_exception_without_fallback(self):
        client = HulyClient(timeout=0.5)
        # Attempting login to unreachable host must raise exception, never create fake mock token
        with pytest.raises(Exception):
            asyncio.run(client.login(
                workspace_url="http://127.0.0.1:59999",
                email="dev@example.com",
                password="testpassword",
            ))
        assert client.credentials.session_token is None

    def test_keycloak_login_detection_returns_none_for_standard_url(self):
        client = HulyClient(timeout=0.5)
        res = asyncio.run(client._try_keycloak_login("http://127.0.0.1:59999", "user", "pass"))
        assert res is None


class TestCLIReadOnlyCommands:
    """Tests for CLI read-only subcommands."""

    def test_cli_status(self, tmp_path: Path):
        args = argparse.Namespace(
            command="status",
            workspace_path=str(tmp_path),
        )
        assert cmd_status(args) == 0

    def test_cli_my_tasks_fails_fast_when_not_logged_in(self, tmp_path: Path):
        args = argparse.Namespace(
            command="my-tasks",
            workspace_path=str(tmp_path),
            json=False,
        )
        # Should return exit code 1 (fails fast, does not return fake tasks)
        assert cmd_my_tasks(args) == 1

    def test_cli_task_detail_fails_fast_when_not_logged_in(self, tmp_path: Path):
        args = argparse.Namespace(
            command="task-detail",
            task_id="GAME-1",
            workspace_path=str(tmp_path),
            json=False,
        )
        assert cmd_task_detail(args) == 1


class TestIssueReferenceAndCriteria:
    """User-named issues: links, IDs, assignee names and explicit acceptance criteria."""

    def test_parse_task_ref_variants(self):
        from coder_nexus.huly.client import parse_task_ref
        assert parse_task_ref("app-123") == "APP-123"
        assert parse_task_ref(" APP-7 ") == "APP-7"
        assert parse_task_ref("42") == "42"
        assert parse_task_ref("https://huly.imespro.ai/workbench/imes/tracker/MOB-15") == "MOB-15"
        assert parse_task_ref("https://huly.app/workbench/acme/tracker/APP-9?space=x#top") == "APP-9"
        assert parse_task_ref("https://huly.app/workbench/acme/tracker/65f0c1d2e3a4b5c6d7e8f901") == "65f0c1d2e3a4b5c6d7e8f901"
        with pytest.raises(ValueError):
            parse_task_ref("https://huly.app/workbench/acme/tracker/")

    def test_person_display_name(self):
        from coder_nexus.huly.client import _person_display_name
        assert _person_display_name({"name": "Pham,Khiem"}) == "Khiem Pham"
        assert _person_display_name({"name": "Jane"}) == "Jane"
        assert _person_display_name({}) is None

    def test_ac_section_wins(self):
        from coder_nexus.huly.client import extract_acceptance_criteria
        desc = "Context line\n- not an AC\n\nAcceptance Criteria:\nGiven the list below\n- Shows error on 401\n- Retries on 500\n\nNotes:\n- ignore me"
        assert extract_acceptance_criteria(desc) == (["Shows error on 401", "Retries on 500"], "ac_section")

    def test_tiptap_checklist_is_recognized(self):
        from coder_nexus.huly.client import extract_acceptance_criteria
        desc = "\n".join(_extract_text_from_tiptap({"type": "doc", "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "Overview"}]},
            {"type": "taskItem", "attrs": {"checked": False}, "content": [{"type": "text", "text": "Handle 401"}]},
        ]}))
        assert extract_acceptance_criteria(desc) == (["Handle 401"], "checklist")

    def test_prose_is_not_turned_into_criteria(self):
        from coder_nexus.huly.client import extract_acceptance_criteria
        assert extract_acceptance_criteria("Build the login screen.\nUse the design system.") == ([], "none")


