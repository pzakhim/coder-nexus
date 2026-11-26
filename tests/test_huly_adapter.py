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
    HulyOtpRequiredError,
    _extract_keycloak_error,
    _extract_keycloak_otp_form,
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

    def test_numbered_goal_and_source_labels_are_not_criteria(self):
        from coder_nexus.huly.client import extract_acceptance_criteria
        # Same shape as a real ticket: behavior list, then restarted numbering for goal / image / design / file.
        desc = (
            "Hiện trạng: công nhân chọn OK/NG mỗi lần quét.\n"
            "1. Mặc định là quét OK, tự ghi nhận số lượng.\n"
            "2. Khi chọn NG, trong 15s quét LPN mới vẫn là NG.\n"
            "3. Bật thùng lẻ thì phải nhập số lượng.\n"
            "4. Bấm giữ một LPN để chuyển OK/NG.\n"
            "1. Mục tiêu: giảm thao tác khi phần lớn hàng đạt.\n"
            "  - Tối ưu tốc độ\n"
            "1. Workflow detail\n"
            "[image: flow.png]3. Link design: https://www.figma.com/design/abc/X?node-id=1-2\n"
            "4. MD file: tham khảo\n"
            "5. Design: https://example.com/spec\n"
        )
        criteria, source = extract_acceptance_criteria(desc)
        assert source == "numbered"
        assert criteria == [
            "Mặc định là quét OK, tự ghi nhận số lượng.",
            "Khi chọn NG, trong 15s quét LPN mới vẫn là NG.",
            "Bật thùng lẻ thì phải nhập số lượng.",
            "Bấm giữ một LPN để chuyển OK/NG.",
        ]

    def test_numbered_behavior_mentioning_design_words_is_kept(self):
        from coder_nexus.huly.client import extract_acceptance_criteria
        desc = "1. Design tab shows the saved layouts and lets the user rename one.\n2. File upload rejects files over 10 MB."
        assert extract_acceptance_criteria(desc)[0] == [
            "Design tab shows the saved layouts and lets the user rename one.",
            "File upload rejects files over 10 MB.",
        ]

    def test_prose_is_not_turned_into_criteria(self):
        from coder_nexus.huly.client import extract_acceptance_criteria
        assert extract_acceptance_criteria("Build the login screen.\nUse the design system.") == ([], "none")


class TestKeycloakOtpLogin:
    """Tests for Keycloak 2FA Authenticator (TOTP/OTP) login flow."""

    @staticmethod
    def _mock_keycloak_server(
        *,
        valid_otp: str = "654321",
        redirect_to_otp: bool = False,
        require_totp_setup: bool = False,
        multiple_creds: bool = False,
    ):
        state = {"otp_posts": []}

        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == "https://huly.example.com/config.json":
                return httpx.Response(200, json={"ACCOUNTS_URL": "https://huly.example.com/_accounts"})
            if url == "https://huly.example.com/_accounts/providers":
                return httpx.Response(200, json=["openid"])
            if url == "https://huly.example.com/_accounts/auth/openid":
                return httpx.Response(
                    302,
                    headers={"location": "https://sso.example.com/realms/acme/protocol/openid-connect/auth?state=s1"},
                )
            if url.startswith("https://sso.example.com/realms/acme/protocol/openid-connect/auth"):
                return httpx.Response(
                    200,
                    text=(
                        '<form id="kc-form-login" action="https://sso.example.com/realms/acme/login-actions/authenticate?step=pw&amp;tab=1" method="post">'
                        '<input name="username" type="text"/><input name="password" type="password"/>'
                        "</form>"
                    ),
                )
            if "step=pw" in url and request.method == "POST":
                body = request.content.decode()
                if "password=good-pass" not in body:
                    return httpx.Response(
                        200,
                        text='<span class="kc-feedback-text">Invalid username or password.</span>',
                    )
                if require_totp_setup:
                    return httpx.Response(
                        200,
                        text='<form id="kc-totp-settings-form" action="/setup"><input type="hidden" name="totpSecret" value="ABC"/></form>',
                    )
                if redirect_to_otp:
                    return httpx.Response(
                        302,
                        headers={"location": "/realms/acme/login-actions/authenticate?step=otp&tab=1"},
                    )
                return self_otp_page(multiple_creds=multiple_creds)
            if "step=otp" in url and request.method == "GET":
                return self_otp_page(multiple_creds=multiple_creds)
            if "step=otp" in url and request.method == "POST":
                form = dict(item.split("=", 1) for item in request.content.decode().split("&") if "=" in item)
                state["otp_posts"].append(form)
                if form.get("otp") == valid_otp:
                    return httpx.Response(
                        302,
                        headers={"location": "https://huly.example.com/_accounts/auth/openid/callback?code=c1&state=s1"},
                    )
                return self_otp_page(
                    multiple_creds=multiple_creds,
                    error_html='<span id="input-error-otp-code">Invalid authenticator code.</span>',
                    step_suffix="2",
                )
            if url.startswith("https://huly.example.com/_accounts/auth/openid/callback"):
                return httpx.Response(
                    302,
                    headers={"location": "https://huly.example.com/login/auth?token=acct.jwt.token"},
                )
            if url == "https://huly.example.com/_accounts/" and request.method == "POST":
                assert request.headers.get("authorization") == "Bearer acct.jwt.token"
                return httpx.Response(
                    200,
                    json={"result": {"token": "ws.jwt.session", "workspace": "ws-uuid-99"}},
                )
            return httpx.Response(404, text=f"Unhandled {request.method} {url}")

        def self_otp_page(*, multiple_creds: bool = False, error_html: str = "", step_suffix: str = "1") -> httpx.Response:
            radios = ""
            if multiple_creds:
                radios = (
                    '<input type="radio" name="selectedCredentialId" value="cred-old"/>'
                    '<input type="radio" name="selectedCredentialId" value="cred-phone" checked="checked"/>'
                )
            html_body = (
                f'<form id="kc-otp-login-form" action="/realms/acme/login-actions/authenticate?step=otp&amp;try={step_suffix}" method="post">'
                '<input type="hidden" name="session_code" value="sc-1"/>'
                f"{radios}"
                '<input id="otp" name="otp" autocomplete="one-time-code" type="text"/>'
                f"{error_html}"
                "</form>"
            )
            return httpx.Response(200, text=html_body)

        return httpx.MockTransport(handler), state

    def test_extract_otp_form_preserves_hidden_and_checked_credential(self):
        html_doc = (
            '<form id="kc-otp-login-form" action="/login-actions/authenticate?code=1&amp;tab=2" method="post">'
            '<input type="hidden" name="csrf" value="tok"/>'
            '<input type="radio" name="selectedCredentialId" value="cred-1"/>'
            '<input type="radio" name="selectedCredentialId" value="cred-2" checked/>'
            '<input id="otp" name="otp" type="text"/>'
            "</form>"
        )
        parsed = _extract_keycloak_otp_form(html_doc, "https://sso.example.com/realms/r/auth")
        assert parsed is not None
        action, fields, field_name = parsed
        assert action == "https://sso.example.com/login-actions/authenticate?code=1&tab=2"
        assert fields == {"csrf": "tok", "selectedCredentialId": "cred-2"}
        assert field_name == "otp"

    def test_extract_keycloak_error_supports_patternfly_v5(self):
        assert _extract_keycloak_error('<span id="input-error-otp-code">Invalid authenticator code.</span>') == (
            "Invalid authenticator code."
        )

    def test_keycloak_otp_direct_code_with_spaces_and_selected_credential(self, monkeypatch):
        transport, state = self._mock_keycloak_server(multiple_creds=True)
        real_client = httpx.AsyncClient
        monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **kw: real_client(*a, transport=transport, **kw))

        client = HulyClient()
        token = asyncio.run(
            client.login(
                workspace_url="https://huly.example.com",
                email="dev@example.com",
                password="good-pass",
                otp="654 321",
            )
        )
        assert token == "ws.jwt.session"
        assert client.credentials.workspace_id == "ws-uuid-99"
        assert state["otp_posts"] == [
            {"session_code": "sc-1", "selectedCredentialId": "cred-phone", "otp": "654321"}
        ]

    def test_keycloak_otp_after_redirect_and_interactive_retry(self, monkeypatch):
        transport, state = self._mock_keycloak_server(redirect_to_otp=True)
        real_client = httpx.AsyncClient
        monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **kw: real_client(*a, transport=transport, **kw))

        seen_errors: list[object] = []
        codes = iter(["000000", "654321"])

        def provider(err):
            seen_errors.append(err)
            return next(codes)

        client = HulyClient()
        token = asyncio.run(
            client.login(
                workspace_url="https://huly.example.com",
                email="dev@example.com",
                password="good-pass",
                otp_provider=provider,
            )
        )
        assert token == "ws.jwt.session"
        assert seen_errors == [None, "Invalid authenticator code."]
        assert [p["otp"] for p in state["otp_posts"]] == ["000000", "654321"]

    def test_keycloak_otp_missing_raises_typed_error(self, monkeypatch):
        transport, _ = self._mock_keycloak_server()
        real_client = httpx.AsyncClient
        monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **kw: real_client(*a, transport=transport, **kw))

        client = HulyClient()
        with pytest.raises(HulyOtpRequiredError, match="Authenticator OTP"):
            asyncio.run(
                client.login(
                    workspace_url="https://huly.example.com",
                    email="dev@example.com",
                    password="good-pass",
                )
            )

    def test_keycloak_otp_wrong_non_interactive_fails_fast(self, monkeypatch):
        transport, _ = self._mock_keycloak_server()
        real_client = httpx.AsyncClient
        monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **kw: real_client(*a, transport=transport, **kw))

        client = HulyClient()
        with pytest.raises(ValueError, match="Invalid authenticator code"):
            asyncio.run(
                client.login(
                    workspace_url="https://huly.example.com",
                    email="dev@example.com",
                    password="good-pass",
                    otp="111111",
                )
            )

    def test_keycloak_totp_setup_required_surfaces_clear_message(self, monkeypatch):
        transport, _ = self._mock_keycloak_server(require_totp_setup=True)
        real_client = httpx.AsyncClient
        monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **kw: real_client(*a, transport=transport, **kw))

        client = HulyClient()
        with pytest.raises(ValueError, match="setting up an Authenticator app"):
            asyncio.run(
                client.login(
                    workspace_url="https://huly.example.com",
                    email="dev@example.com",
                    password="good-pass",
                )
            )


