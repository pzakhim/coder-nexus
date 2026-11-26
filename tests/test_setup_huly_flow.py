"""Tests for the guided `coder-nexus setup huly` flow (check -> URL ping -> login loop -> verify)."""

import argparse
import json
from pathlib import Path

import pytest

from coder_nexus.cli import build_parser
from coder_nexus.huly.auth import DEV_ENV_MARKER, INIT_ENV_KEYS, init_env_file, load_client_credentials, parse_env_file
from coder_nexus.huly.client import HulyClient, HulyOtpRequiredError
from coder_nexus.huly.models import HulyTaskSummary
from coder_nexus.setup import huly as setup_huly
from coder_nexus.setup.huly import (
    EXIT_NEEDS_INPUT,
    EXIT_OK,
    EXIT_URL_UNREACHABLE,
    cmd_init,
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

    async def login(self, workspace_url=None, email=None, password=None, workspace_path=None, *, otp=None, otp_provider=None):
        calls["login"] += 1
        if password != GOOD_PASSWORD:
            raise RuntimeError("Huly login failed (401): invalid credentials")
        self.credentials.session_token = "tok-1234567890abcdef"
        return self.credentials.session_token

    async def resolve(self):
        self.credentials.workspace_id = "ws-42"
        return "ws-42"

    async def tasks(self, workspace_path=None, include_all=False):
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


def test_interactive_prompts_for_url_even_when_url_already_in_env(tmp_path, fake_huly):
    """When .env already has HULY_WORKSPACE_URL (e.g. https://huly.app), interactive setup still prompts for URL."""
    (tmp_path / ".env").write_text("HULY_WORKSPACE_URL=https://huly.app\n", encoding="utf-8")
    prompts: list[str] = []
    answers = iter(["https://huly.cty.com", "dev@cty.com"])

    def capture_input(prompt: str = "") -> str:
        prompts.append(prompt)
        return next(answers)

    code = run_setup_huly(
        str(tmp_path),
        interactive=True,
        input_fn=capture_input,
        getpass_fn=_scripted([GOOD_PASSWORD]),
    )
    assert code == EXIT_OK
    assert any("Huly URL [https://huly.app]:" in p for p in prompts)
    env = parse_env_file(tmp_path / ".env")
    assert env["HULY_WORKSPACE_URL"] == "https://huly.cty.com"


def test_init_creates_env_and_does_not_skip_url_step(tmp_path, capsys):
    code = cmd_init(argparse.Namespace(workspace_path=str(tmp_path)))
    assert code == 0
    env_text = (tmp_path / ".env").read_text(encoding="utf-8")
    assert DEV_ENV_MARKER in env_text
    parsed = parse_env_file(tmp_path / ".env")
    assert set(INIT_ENV_KEYS) == set(parsed.keys())
    assert all(v == "" for v in parsed.values())

    capsys.readouterr()
    # Running setup huly after `init` must still ask for URL first because HULY_WORKSPACE_URL is empty
    step_code = run_setup_huly(str(tmp_path), as_json=True, interactive=False)
    assert step_code == EXIT_NEEDS_INPUT
    out = json.loads(capsys.readouterr().out)
    assert out["step"] == "url" and out["needs"] == ["url"]


def test_init_appends_missing_keys_to_end_of_existing_env(tmp_path):
    env_file = tmp_path / ".env"
    original = "# App config\nAPI_BASE_URL=https://api.cty.com\nHULY_WORKSPACE_URL=https://huly.cty.com\n"
    env_file.write_text(original, encoding="utf-8")

    path, added, created_new = init_env_file(str(tmp_path))
    assert path == env_file
    assert not created_new
    assert "HULY_WORKSPACE_URL" not in added
    assert set(added) == set(INIT_ENV_KEYS) - {"HULY_WORKSPACE_URL"}

    updated_text = env_file.read_text(encoding="utf-8")
    assert updated_text.startswith(original)
    parsed = parse_env_file(env_file)
    assert parsed["API_BASE_URL"] == "https://api.cty.com"
    assert parsed["HULY_WORKSPACE_URL"] == "https://huly.cty.com"
    assert parsed["FIGMA_TOKEN"] == ""

    # Second run is a no-op
    _, added_again, created_again = init_env_file(str(tmp_path))
    assert added_again == [] and not created_again
    assert env_file.read_text(encoding="utf-8") == updated_text


@pytest.fixture
def fake_huly_2fa(monkeypatch):
    """Reachable server requiring GOOD_PASSWORD and OTP '246810'."""
    calls = {"login": 0}
    monkeypatch.setattr(setup_huly, "ping_huly_url", lambda url, timeout=10.0: (True, "Huly server detected"))

    async def login(self, workspace_url=None, email=None, password=None, workspace_path=None, *, otp=None, otp_provider=None):
        calls["login"] += 1
        if password != GOOD_PASSWORD:
            raise ValueError("Keycloak authentication failed: Invalid username or password.")
        code = otp
        err = None
        for _ in range(3):
            if not code:
                if otp_provider is None:
                    raise HulyOtpRequiredError("Keycloak requires a 6-digit Authenticator OTP code.")
                code = otp_provider(err)
            if code == "246810":
                self.credentials.session_token = "tok-2fa-session-999999"
                return self.credentials.session_token
            err = "Invalid authenticator code."
            if otp_provider is None:
                raise ValueError(f"Keycloak OTP verification failed: {err}")
            code = None
        raise ValueError("Keycloak OTP verification failed after 3 attempts.")

    async def resolve(self):
        self.credentials.workspace_id = "ws-2fa"
        return "ws-2fa"

    async def tasks(self, workspace_path=None, include_all=False):
        return TASKS

    monkeypatch.setattr(HulyClient, "login", login)
    monkeypatch.setattr(HulyClient, "_resolve_workspace_id", resolve)
    monkeypatch.setattr(HulyClient, "get_my_uncompleted_tasks", tasks)
    return calls


def test_non_interactive_2fa_requests_otp_step(tmp_path, fake_huly_2fa, capsys):
    code = run_setup_huly(
        str(tmp_path),
        url="https://huly.cty.com",
        email="dev@cty.com",
        password=GOOD_PASSWORD,
        as_json=True,
        interactive=False,
    )
    assert code == EXIT_NEEDS_INPUT
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "needs_input"
    assert out["step"] == "otp"
    assert out["needs"] == ["otp"]


def test_non_interactive_2fa_succeeds_with_otp_and_masks_secret(tmp_path, fake_huly_2fa, capsys):
    args = build_parser().parse_args([
        "setup", "huly",
        "--project", str(tmp_path),
        "--url", "https://huly.cty.com",
        "--email", "dev@cty.com",
        "--password", GOOD_PASSWORD,
        "--otp", "246810",
        "--json",
    ])
    code = cmd_setup_huly(args)
    assert code == EXIT_OK
    raw_out = capsys.readouterr().out
    out = json.loads(raw_out)
    assert out["status"] == "configured"
    assert out["workspace_id"] == "ws-2fa"
    assert "246810" not in raw_out
    assert "tok-2fa" not in raw_out


def test_interactive_2fa_prompts_for_otp_and_retries_without_reasking_password(tmp_path, fake_huly_2fa, capsys):
    code = run_setup_huly(
        str(tmp_path),
        interactive=True,
        input_fn=_scripted(["https://huly.cty.com", "dev@cty.com", "000000", "246810"]),
        getpass_fn=_scripted([GOOD_PASSWORD]),
    )
    assert code == EXIT_OK
    assert fake_huly_2fa["login"] == 1  # OTP retried inside same login session
    creds = load_client_credentials(str(tmp_path))
    assert creds.session_token == "tok-2fa-session-999999"
    assert creds.workspace_id == "ws-2fa"
    printed = capsys.readouterr().out
    assert "Two-factor authentication" in printed
    assert "Invalid authenticator code." in printed
    assert "246810" not in printed


def test_env_prefilled_with_otp_runs_one_shot_and_clears_otp(tmp_path, fake_huly_2fa, capsys):
    (tmp_path / ".env").write_text(
        f"HULY_WORKSPACE_URL=https://huly.cty.com\n"
        f"HULY_EMAIL=dev@cty.com\n"
        f"HULY_PASSWORD={GOOD_PASSWORD}\n"
        f"HULY_OTP=246810\n",
        encoding="utf-8",
    )

    def fail_if_prompted(prompt: str = "") -> str:
        raise AssertionError(f"Should not prompt when .env has URL, email, password, and OTP; got: {prompt}")

    code = run_setup_huly(
        str(tmp_path),
        interactive=True,
        input_fn=fail_if_prompted,
        getpass_fn=fail_if_prompted,
    )
    assert code == EXIT_OK
    env = parse_env_file(tmp_path / ".env")
    assert env["HULY_SESSION_TOKEN"] == "tok-2fa-session-999999"
    assert env["HULY_WORKSPACE_ID"] == "ws-2fa"
    assert env["HULY_OTP"] == ""  # auto-cleared after login
    printed = capsys.readouterr().out
    assert "246810" not in printed
    # `--check` succeeds even though HULY_OTP is empty
    assert cmd_setup_huly(argparse.Namespace(check=True, workspace_path=str(tmp_path))) == 0


def test_env_prefilled_with_otp_json_mode_clears_otp(tmp_path, fake_huly_2fa, capsys):
    (tmp_path / ".env").write_text(
        f"HULY_WORKSPACE_URL=https://huly.cty.com\n"
        f"HULY_EMAIL=dev@cty.com\n"
        f"HULY_PASSWORD={GOOD_PASSWORD}\n"
        f"HULY_OTP=246810\n",
        encoding="utf-8",
    )
    code = run_setup_huly(str(tmp_path), as_json=True, interactive=False)
    assert code == EXIT_OK
    raw_out = capsys.readouterr().out
    out = json.loads(raw_out)
    assert out["status"] == "configured"
    assert out["workspace_id"] == "ws-2fa"
    assert "246810" not in raw_out
    assert parse_env_file(tmp_path / ".env")["HULY_OTP"] == ""


def test_env_prefilled_expired_otp_interactive_falls_back_to_prompt_and_clears_otp(tmp_path, fake_huly_2fa, capsys):
    (tmp_path / ".env").write_text(
        f"HULY_WORKSPACE_URL=https://huly.cty.com\n"
        f"HULY_EMAIL=dev@cty.com\n"
        f"HULY_PASSWORD={GOOD_PASSWORD}\n"
        f"HULY_OTP=000000\n",
        encoding="utf-8",
    )
    code = run_setup_huly(
        str(tmp_path),
        interactive=True,
        input_fn=_scripted(["246810"]),
        getpass_fn=lambda prompt="": (_ for _ in ()).throw(AssertionError("Password should not be re-prompted")),
    )
    assert code == EXIT_OK
    env = parse_env_file(tmp_path / ".env")
    assert env["HULY_SESSION_TOKEN"] == "tok-2fa-session-999999"
    assert env["HULY_OTP"] == ""


def test_env_prefilled_expired_otp_non_interactive_fails_and_clears_otp(tmp_path, fake_huly_2fa, capsys):
    (tmp_path / ".env").write_text(
        f"HULY_WORKSPACE_URL=https://huly.cty.com\n"
        f"HULY_EMAIL=dev@cty.com\n"
        f"HULY_PASSWORD={GOOD_PASSWORD}\n"
        f"HULY_OTP=000000\n",
        encoding="utf-8",
    )
    code = run_setup_huly(str(tmp_path), as_json=True, interactive=False)
    assert code == setup_huly.EXIT_LOGIN_FAILED
    assert parse_env_file(tmp_path / ".env")["HULY_OTP"] == ""
