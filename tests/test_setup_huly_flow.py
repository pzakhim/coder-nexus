"""Tests for the guided `coder-nexus setup huly` flow (check -> URL ping -> login loop -> verify)."""

import argparse
import json
from pathlib import Path

import pytest

from coder_nexus.huly.auth import DEV_ENV_MARKER, load_client_credentials, parse_env_file
from coder_nexus.huly.client import HulyClient
from coder_nexus.huly.models import HulyTaskSummary
from coder_nexus.setup import huly as setup_huly
from coder_nexus.setup.huly import (
    EXIT_NEEDS_INPUT,
    EXIT_OK,
    EXIT_URL_UNREACHABLE,
    cmd_setup_huly,
    normalize_url,
    run_setup_huly,
)

GOOD_PASSWORD = "right-pass"
TASKS = [
    HulyTaskSummary(id="APP-7", title="Login screen", status="TODO", priority="high"),
    HulyTaskSummary(id="APP-9", title="Logout", status="IN_PROGRESS", priority="medium"),
]


@pytest.fixture
def fake_huly(monkeypatch):
    """Reachable server, login accepts only GOOD_PASSWORD, two open tasks."""
    calls = {"login": 0}
    monkeypatch.setattr(setup_huly, "ping_huly_url", lambda url, timeout=10.0: (True, "Huly server detected"))

    async def login(self, workspace_url=None, email=None, password=None, workspace_path=None):
        calls["login"] += 1
        if password != GOOD_PASSWORD:
            raise RuntimeError("Huly login failed (401): invalid credentials")
        self.credentials.session_token = "tok-1234567890abcdef"
        return self.credentials.session_token

    async def resolve(self):
        self.credentials.workspace_id = "ws-42"
        return "ws-42"

    async def tasks(self, workspace_path=None):
        return TASKS

    monkeypatch.setattr(HulyClient, "login", login)
    monkeypatch.setattr(HulyClient, "_resolve_workspace_id", resolve)
    monkeypatch.setattr(HulyClient, "get_my_uncompleted_tasks", tasks)
    return calls


def _scripted(answers):
    it = iter(answers)
    return lambda prompt="": next(it)


def test_normalize_url():
    assert normalize_url(" huly.cty.com/ ") == "https://huly.cty.com"
    assert normalize_url("http://10.0.0.5:8087/") == "http://10.0.0.5:8087"


def test_non_interactive_without_url_asks_for_url(tmp_path, capsys):
    code = run_setup_huly(str(tmp_path), as_json=True, interactive=False)
    assert code == EXIT_NEEDS_INPUT
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "needs_input" and out["needs"] == ["url"]
    assert not (tmp_path / ".env").exists()


def test_unreachable_url_stops_and_saves_nothing(tmp_path, capsys):
    code = run_setup_huly(str(tmp_path), url="http://127.0.0.1:59999", as_json=True, interactive=False)
    assert code == EXIT_URL_UNREACHABLE
    assert json.loads(capsys.readouterr().out)["status"] == "url_unreachable"
    assert not (tmp_path / ".env").exists()


def test_step1_saves_url_then_needs_account(tmp_path, fake_huly, capsys):
    code = run_setup_huly(str(tmp_path), url="huly.cty.com", as_json=True, interactive=False)
    assert code == EXIT_NEEDS_INPUT
    out = json.loads(capsys.readouterr().out)
    assert out["step"] == "account" and out["needs"] == ["email", "password"]
    env_text = (tmp_path / ".env").read_text()
    assert DEV_ENV_MARKER in env_text
    assert parse_env_file(tmp_path / ".env")["HULY_WORKSPACE_URL"] == "https://huly.cty.com"


def test_interactive_retries_until_login_succeeds(tmp_path, fake_huly, capsys):
    code = run_setup_huly(
        str(tmp_path),
        interactive=True,
        input_fn=_scripted(["https://huly.cty.com", "dev@cty.com", ""]),  # URL, email, email (keep default)
        getpass_fn=_scripted(["wrong", GOOD_PASSWORD]),
    )
    assert code == EXIT_OK
    assert fake_huly["login"] == 2
    creds = load_client_credentials(str(tmp_path))
    assert creds.workspace_url == "https://huly.cty.com"
    assert creds.email == "dev@cty.com" and creds.password == GOOD_PASSWORD
    assert creds.session_token == "tok-1234567890abcdef" and creds.workspace_id == "ws-42"
    printed = capsys.readouterr().out
    assert "[APP-7] Login screen" in printed
    assert "tok-1234567890abcdef" not in printed  # token is masked


def test_agent_json_flow_returns_first_open_task(tmp_path, fake_huly, capsys):
    code = run_setup_huly(str(tmp_path), url="https://huly.cty.com", email="dev@cty.com",
                          password=GOOD_PASSWORD, as_json=True, interactive=False)
    assert code == EXIT_OK
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "configured"
    assert out["first_task"]["id"] == "APP-7" and out["open_task_count"] == 2
    assert GOOD_PASSWORD not in json.dumps(out) and "tok-" not in json.dumps(out)


def test_wrong_password_non_interactive_fails_once(tmp_path, fake_huly, capsys):
    code = run_setup_huly(str(tmp_path), url="https://huly.cty.com", email="dev@cty.com",
                          password="wrong", as_json=True, interactive=False)
    assert code == setup_huly.EXIT_LOGIN_FAILED
    assert fake_huly["login"] == 1
    env = parse_env_file(tmp_path / ".env")
    assert env["HULY_WORKSPACE_URL"] == "https://huly.cty.com"  # step 1 kept
    assert not env.get("HULY_SESSION_TOKEN")


def test_already_configured_only_verifies(tmp_path, fake_huly, capsys):
    run_setup_huly(str(tmp_path), url="https://huly.cty.com", email="dev@cty.com",
                   password=GOOD_PASSWORD, interactive=False)
    capsys.readouterr()
    fake_huly["login"] = 0
    code = run_setup_huly(str(tmp_path), as_json=True, interactive=False)
    assert code == EXIT_OK
    assert json.loads(capsys.readouterr().out)["status"] == "already_configured"
    assert fake_huly["login"] == 0


def test_changing_url_drops_old_session(tmp_path, fake_huly):
    run_setup_huly(str(tmp_path), url="https://huly.cty.com", email="dev@cty.com",
                   password=GOOD_PASSWORD, interactive=False)
    run_setup_huly(str(tmp_path), url="https://other.cty.com", interactive=False, reset=True)
    env = parse_env_file(tmp_path / ".env")
    assert env["HULY_WORKSPACE_URL"] == "https://other.cty.com"
    assert not env.get("HULY_SESSION_TOKEN") and not env.get("HULY_WORKSPACE_ID")


def test_check_requires_all_five_values(tmp_path, fake_huly):
    args = argparse.Namespace(check=True, workspace_path=str(tmp_path))
    assert cmd_setup_huly(args) == 1
    run_setup_huly(str(tmp_path), url="https://huly.cty.com", interactive=False)
    assert cmd_setup_huly(args) == 1
    run_setup_huly(str(tmp_path), email="dev@cty.com", password=GOOD_PASSWORD, interactive=False)
    assert cmd_setup_huly(args) == 0
