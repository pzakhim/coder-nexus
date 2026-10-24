"""Authentication and .env persistence manager for Huly credentials."""

import os
from pathlib import Path
from typing import Optional

from .models import HulyCredentials

HULY_ENV_KEYS = {
    "HULY_WORKSPACE_URL": "workspace_url",
    "HULY_EMAIL": "email",
    "HULY_PASSWORD": "password",
    "HULY_SESSION_TOKEN": "session_token",
    "HULY_WORKSPACE_ID": "workspace_id",
}

INIT_ENV_KEYS: tuple[str, ...] = (
    "HULY_WORKSPACE_URL",
    "HULY_EMAIL",
    "HULY_PASSWORD",
    "HULY_SESSION_TOKEN",
    "HULY_WORKSPACE_ID",
    "FIGMA_TOKEN",
)

# Marker written at the top of every .env that `coder-nexus setup huly` touches.
DEV_ENV_MARKER = "# [coder-nexus] DEVELOPMENT ONLY"
DEV_ENV_HEADER = (
    f"{DEV_ENV_MARKER} - local developer environment variables.\n"
    "# HULY_* values are personal dev credentials (plain text). Do not commit this file,\n"
    "# do not reuse it for staging/production, and keep `.env` in .gitignore.\n"
)


def _resolve_env_file(workspace_path: Optional[str] = None) -> Path:
    """Resolve the path to the client's .env file."""
    base_dir = Path(workspace_path).resolve() if workspace_path else Path.cwd().resolve()
    return base_dir / ".env"


def parse_env_file(env_path: Path) -> dict[str, str]:
    """Parse a .env file into a dictionary of key-value pairs without modifying other lines."""
    if not env_path.exists() or not env_path.is_file():
        return {}

    env_vars: dict[str, str] = {}
    try:
        content = env_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" in stripped:
                key, val = stripped.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                env_vars[key] = val
    except Exception:
        pass
    return env_vars


def load_client_credentials(workspace_path: Optional[str] = None) -> HulyCredentials:
    """Load Huly credentials from the client workspace's .env file, falling back to os.environ."""
    env_file = _resolve_env_file(workspace_path)
    file_vars = parse_env_file(env_file)

    def get_var(key: str, default: Optional[str] = None) -> Optional[str]:
        # Priority: .env file > os.environ > default
        val = file_vars.get(key)
        if val is not None and val != "":
            return val
        env_val = os.getenv(key)
        if env_val is not None and env_val != "":
            return env_val
        return default

    return HulyCredentials(
        workspace_url=get_var("HULY_WORKSPACE_URL", "https://huly.app") or "https://huly.app",
        email=get_var("HULY_EMAIL"),
        password=get_var("HULY_PASSWORD"),
        session_token=get_var("HULY_SESSION_TOKEN"),
        workspace_id=get_var("HULY_WORKSPACE_ID"),
    )


def update_env_values(workspace_path: str, values: dict[str, str]) -> Path:
    """Upsert KEY=VALUE pairs in the client workspace's .env.

    Preserves every other line and comment, appends missing keys, and makes sure the
    DEVELOPMENT ONLY header is present at the top of the file.
    """
    env_path = _resolve_env_file(workspace_path)
    env_path.parent.mkdir(parents=True, exist_ok=True)

    lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    updated_lines: list[str] = []
    found_keys: set[str] = set()
    for line in lines:
        stripped = line.strip()
        if "=" in stripped and not stripped.startswith("#"):
            key = stripped.split("=", 1)[0].strip()
            if key in values:
                updated_lines.append(f"{key}={values[key]}")
                found_keys.add(key)
                continue
        updated_lines.append(line)

    for key, val in values.items():
        if key not in found_keys:
            updated_lines.append(f"{key}={val}")

    if not any(l.strip().startswith(DEV_ENV_MARKER) for l in updated_lines):
        updated_lines = DEV_ENV_HEADER.rstrip("\n").split("\n") + [""] + updated_lines

    env_path.write_text("\n".join(updated_lines).rstrip("\n") + "\n", encoding="utf-8")
    return env_path


def save_client_credentials(workspace_path: str, credentials: HulyCredentials) -> Path:
    """Save or update all Huly credentials in the client workspace's .env file.

    Preserves any existing non-Huly environment variables and comments in the file.
    """
    return update_env_values(
        workspace_path,
        {
            "HULY_WORKSPACE_URL": credentials.workspace_url,
            "HULY_EMAIL": credentials.email or "",
            "HULY_PASSWORD": credentials.password or "",
            "HULY_SESSION_TOKEN": credentials.session_token or "",
            "HULY_WORKSPACE_ID": credentials.workspace_id or "",
        },
    )


def init_env_file(workspace_path: Optional[str] = None) -> tuple[Path, list[str], bool]:
    """Create `.env` from template, or append missing Coder Nexus keys to the end of an existing `.env`.

    Returns (env_path, added_keys, created_new). Never overwrites existing keys or lines.
    """
    env_path = _resolve_env_file(workspace_path)
    env_path.parent.mkdir(parents=True, exist_ok=True)

    existing_text = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
    existing_lines = existing_text.splitlines()
    created_new = not env_path.exists() or not existing_text.strip()

    existing_keys = set(parse_env_file(env_path).keys())
    missing_keys = [k for k in INIT_ENV_KEYS if k not in existing_keys]
    if not missing_keys and not created_new:
        return env_path, [], False

    block_lines: list[str] = []
    if not any(l.strip().startswith(DEV_ENV_MARKER) for l in existing_lines):
        block_lines.extend(DEV_ENV_HEADER.rstrip("\n").split("\n"))
    block_lines.append("# Fill Huly credentials with `coder-nexus setup huly` or edit below (e.g. https://huly.app)")
    for key in missing_keys:
        if key == "FIGMA_TOKEN" and any(k.startswith("HULY_") for k in missing_keys):
            block_lines.append("")
            block_lines.append("# Optional: Figma Personal Access Token for read-only frame extraction")
        block_lines.append(f"{key}=")

    if created_new:
        out_lines = block_lines
    else:
        out_lines = list(existing_lines)
        if out_lines and out_lines[-1].strip() != "":
            out_lines.append("")
        out_lines.extend(block_lines)

    env_path.write_text("\n".join(out_lines).rstrip("\n") + "\n", encoding="utf-8")
    return env_path, missing_keys, created_new
