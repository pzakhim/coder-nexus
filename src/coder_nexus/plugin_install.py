"""Install the Coder Nexus plugin projection from a source checkout (`coder-nexus install-plugin`)."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .plugin_build import VARIANTS, build_variant, load_pack

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _source_revision(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short=12", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    revision = result.stdout.strip() if result.returncode == 0 else "UNKNOWN"
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return f"{revision}-dirty" if dirty.stdout.strip() else revision


def _bundle_digest(plugin_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in plugin_dir.rglob("*") if item.is_file()):
        digest.update(str(path.relative_to(plugin_dir)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _hub_digest(repo_root: Path) -> str:
    files = [repo_root / "pyproject.toml", repo_root / "uv.lock"]
    files.extend(sorted((repo_root / "src").rglob("*.py")))
    digest = hashlib.sha256()
    for path in files:
        if path.is_file():
            digest.update(str(path.relative_to(repo_root)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _variant_sources(plugins_dir: Path, variant: str) -> list[Path]:
    spec = VARIANTS[variant]
    if not spec["packs"]:
        return [plugins_dir / spec["legacy_dir"]]
    sources = [plugins_dir / "core"]
    for stack in spec["packs"]:
        sources.append(plugins_dir / "packs" / stack)
        sources.extend(plugins_dir / "layers" / layer for layer in load_pack(plugins_dir, stack)["layers"])
    return sources


def _variant_manifest(plugins_dir: Path, variant: str) -> dict:
    spec = VARIANTS[variant]
    source = plugins_dir / (spec["legacy_dir"] if not spec["packs"] else "core")
    return _read_json(source / "bundle_manifest.json")


def variant_for(target: str, framework: str | None) -> str:
    return "be" if target == "be" else f"fe-{framework or 'flutter'}"


def _install_plugin_projection(
    variant: str,
    destination: Path,
    repo_root: Path,
    workspace_agents: bool = False,
    plugins_dir: Path | None = None,
) -> str:
    """Install one built variant from source; agents go to <workspace>/.agents/agents when workspace_agents."""
    plugins_dir = plugins_dir or repo_root / "plugins"
    manifest = _variant_manifest(plugins_dir, variant)
    shared_contracts = plugins_dir / "shared_contracts"
    if not (shared_contracts / "api_handshake_protocol.md").is_file():
        raise FileNotFoundError("Missing shared API handshake protocol")
    digest = hashlib.sha256()
    for source in _variant_sources(plugins_dir, variant):
        digest.update(_bundle_digest(source).encode())
    metadata = {
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "hub_version": manifest.get("hub_version", "UNKNOWN"),
        "source_revision": _source_revision(repo_root),
        "source_path": str(repo_root),
        "bundle_digest": digest.hexdigest(),
        "hub_digest": _hub_digest(repo_root),
        "shared_contracts_digest": _bundle_digest(shared_contracts),
        "variant": variant,
        "framework": (VARIANTS[variant]["packs"] or [None])[0],
        "agents_location": "workspace" if workspace_agents else "plugin",
    }
    existing = _read_json(destination / "installed_version.json") if destination.is_dir() else {}
    if existing == metadata:
        return "unchanged"

    with tempfile.TemporaryDirectory() as tmp:
        layout = "workspace" if workspace_agents else "global"
        built = build_variant(variant, layout, Path(tmp), plugins_dir)
        files = built / "files"
        plugin_rel = _read_json(built / "projection.json")["managed"][0]
        staged_plugin = files / plugin_rel
        runtime_config = {
            "mcpServers": {
                "coder-nexus": {
                    "command": "uv",
                    "args": ["run", "--offline", "coder-nexus", "serve"],
                    "cwd": str(repo_root),
                }
            }
        }
        (staged_plugin / "mcp_config.json").write_text(json.dumps(runtime_config, indent=2) + "\n", encoding="utf-8")
        (staged_plugin / "installed_version.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = destination.parent / f".{destination.name}.installing"
        backup = destination.parent / f".{destination.name}.backup"
        _remove_path(staging)
        _remove_path(backup)
        shutil.copytree(staged_plugin, staging)
        if workspace_agents:
            agents_dir = destination.parent.parent / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            for agent in (files / ".agents/agents").glob("*.md"):
                shutil.copy2(agent, agents_dir / agent.name)

    existed = destination.is_symlink() or destination.exists()
    if existed:
        destination.rename(backup)
    try:
        staging.rename(destination)
    except OSError:
        if existed:
            backup.rename(destination)
        raise
    _remove_path(backup)
    return "updated" if existed else "installed"


def _remove_legacy_workspace_entry(workspace: Path, source_plugin: Path, installed_plugin: Path) -> None:
    config_path = workspace / ".agents" / "plugins.json"
    data = _read_json(config_path)
    entries = data.get("entries")
    if not isinstance(entries, list):
        return
    owned_paths = {str(source_plugin.resolve()), str(installed_plugin.resolve())}
    retained = [
        entry
        for entry in entries
        if not isinstance(entry, dict) or entry.get("path") not in owned_paths
    ]
    if retained == entries:
        return
    if retained:
        config_path.write_text(json.dumps({**data, "entries": retained}, indent=2) + "\n", encoding="utf-8")
    else:
        config_path.unlink()


def cmd_install_plugin(args: argparse.Namespace) -> int:
    """Handle `coder_nexus install-plugin` command.

    Installs a self-contained Coder Nexus plugin projection for Antigravity IDE:
    - --global: Installs to ~/.gemini/config/plugins/coder-nexus-<target>
    - --workspace <path>: Installs to <workspace>/.agents/plugins/coder-nexus-<target>
    - Default: Installs globally (target: fe)
    """
    repo_root = REPO_ROOT
    target = getattr(args, "plugin", None) or "fe"
    plugin_name = f"coder-nexus-{target}" if target in {"fe", "be"} else "coder-nexus-fe"
    variant = variant_for(target, getattr(args, "framework", "flutter"))
    manifest = _variant_manifest(repo_root / "plugins", variant)
    if not manifest.get("plugin_version"):
        print("❌ Plugin bundle manifest is missing plugin_version", file=sys.stderr)
        return 1
    plugin_dir = repo_root / "plugins" / plugin_name

    destinations: list[Path] = []

    if args.is_global or not args.workspace:
        global_plugins_dir = Path.home() / ".gemini" / "config" / "plugins"
        legacy_symlink = global_plugins_dir / "aifactory-coder"
        if legacy_symlink.is_symlink() or legacy_symlink.exists():
            try:
                _remove_path(legacy_symlink)
                print(f"🧹 Removed legacy plugin: {legacy_symlink}")
            except OSError as exc:
                print(f"❌ Failed to remove legacy plugin: {exc}", file=sys.stderr)
                return 1
        legacy_unsplit = global_plugins_dir / "coder-nexus"
        if legacy_unsplit.is_symlink() or (legacy_unsplit.exists() and legacy_unsplit != (global_plugins_dir / plugin_name)):
            try:
                _remove_path(legacy_unsplit)
                print(f"🧹 Removed legacy unsplit plugin: {legacy_unsplit}")
            except OSError as exc:
                print(f"❌ Failed to remove legacy unsplit plugin: {exc}", file=sys.stderr)
                return 1
        destinations.append(global_plugins_dir / plugin_name)

    if args.workspace:
        ws_path = Path(args.workspace).resolve()
        destination = ws_path / ".agents" / "plugins" / plugin_name
        _remove_legacy_workspace_entry(ws_path, plugin_dir, destination)
        destinations.append(destination)

    try:
        for destination in destinations:
            action = _install_plugin_projection(
                variant,
                destination,
                repo_root,
                workspace_agents=destination.parent.parent.name == ".agents",
            )
            print(
                f"✅ Plugin {action}: {destination} "
                f"(version={manifest['plugin_version']}, source={_source_revision(repo_root)})"
            )
    except OSError as exc:
        print(f"❌ Failed to install plugin: {exc}", file=sys.stderr)
        return 1
    return 0 if destinations else 1
