"""Install the Coder Nexus plugin projection from a source checkout (`coder-nexus install-plugin`)."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .plugin_build import (
    LEGACY_PLUGINS,
    PLUGIN_NAME,
    available_packs,
    build_variant,
    combo_key,
    load_pack,
    read_stack_file,
    write_stack_file,
)

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


def _variant_sources(plugins_dir: Path, packs: list[str]) -> list[Path]:
    sources = [plugins_dir / "core", plugins_dir / "shared_contracts"]
    for stack in packs:
        sources.append(plugins_dir / "packs" / stack)
        sources.extend(plugins_dir / "layers" / layer for layer in load_pack(plugins_dir, stack)["layers"])
    return sorted(set(sources))


def packs_for(target: str | None, framework: str | None) -> list[str]:
    """Map the legacy --plugin/--framework flags to a pack."""
    return ["backend"] if target == "be" else [framework or "flutter"]


def _install_plugin_projection(
    packs: list[str] | str,
    destination: Path,
    repo_root: Path,
    workspace_agents: bool = False,
    plugins_dir: Path | None = None,
) -> str:
    """Install core + `packs` built from source into the plugin folder `destination`.

    With `workspace_agents` the role agents go to <workspace>/.agents/agents.
    """
    plugins_dir = plugins_dir or repo_root / "plugins"
    packs = sorted(set(packs.split("+") if isinstance(packs, str) else packs))
    manifest = _read_json(plugins_dir / "core" / "bundle_manifest.json")
    shared_contracts = plugins_dir / "shared_contracts"
    if not (shared_contracts / "api_handshake_protocol.md").is_file():
        raise FileNotFoundError("Missing shared API handshake protocol")
    digest = hashlib.sha256()
    for source in _variant_sources(plugins_dir, packs):
        digest.update(_bundle_digest(source).encode())
    metadata = {
        "plugin_version": manifest.get("plugin_version", "UNKNOWN"),
        "hub_version": manifest.get("hub_version", "UNKNOWN"),
        "source_revision": _source_revision(repo_root),
        "source_path": str(repo_root),
        "bundle_digest": digest.hexdigest(),
        "hub_digest": _hub_digest(repo_root),
        "shared_contracts_digest": _bundle_digest(shared_contracts),
        "packs": packs,
        "agents_location": "workspace" if workspace_agents else "plugin",
    }
    existing = _read_json(destination / "installed_version.json") if destination.is_dir() else {}
    if existing == metadata:
        return "unchanged"

    with tempfile.TemporaryDirectory() as tmp:
        built = build_variant(packs, "workspace", Path(tmp), plugins_dir)
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
        agents_dir = destination.parent.parent / "agents" if workspace_agents else staging / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        for agent in (files / ".agents/agents").glob("*.md"):
            shutil.copy2(agent, agents_dir / agent.name)
        if not workspace_agents:  # agents live inside the plugin folder
            staged_manifest = _read_json(staging / "bundle_manifest.json")
            staged_manifest["required_resources"] = [
                res.removeprefix("../../") for res in staged_manifest.get("required_resources", [])
            ]
            (staging / "bundle_manifest.json").write_text(json.dumps(staged_manifest, indent=2) + "\n", encoding="utf-8")

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
    """Handle `coder-nexus install-plugin` (source checkout only).

    - --workspace <path>: installs <workspace>/.agents/plugins/coder-nexus, the composed role
      agents in .agents/agents and .agents/stack.json. A workspace holds one pack: when stack.json
      records a different one, nothing is touched unless --replace is given.
    - --global (or no --workspace): installs ~/.gemini/config/plugins/coder-nexus.
    The pack comes from --pack (exactly one) or the legacy --plugin fe|be / --framework flags.
    """
    repo_root = REPO_ROOT
    plugins_dir = repo_root / "plugins"
    requested = list(getattr(args, "pack", None) or []) or packs_for(
        getattr(args, "plugin", None), getattr(args, "framework", None)
    )
    unknown = sorted(set(requested) - set(available_packs(plugins_dir)))
    if unknown:
        print(f"❌ Unknown pack(s): {', '.join(unknown)} (available: {', '.join(available_packs(plugins_dir))})", file=sys.stderr)
        return 1
    if len(requested) != 1:
        print("❌ Install exactly one pack (flutter or backend); pass a single --pack", file=sys.stderr)
        return 1
    manifest = _read_json(plugins_dir / "core" / "bundle_manifest.json")
    if not manifest.get("plugin_version"):
        print("❌ Plugin bundle manifest is missing plugin_version", file=sys.stderr)
        return 1
    if args.workspace and not getattr(args, "replace", False):
        installed = sorted({
            pack.get("stack") for pack in read_stack_file(Path(args.workspace).resolve()).get("packs", [])
            if pack.get("stack") in available_packs(plugins_dir)
        } - set(requested))
        if installed:
            print(f"❌ workspace has {', '.join(installed)}; pass --replace to switch", file=sys.stderr)
            return 1

    installs: list[tuple[Path, list[str], Path | None]] = []
    if args.is_global or not args.workspace:
        global_plugins_dir = Path.home() / ".gemini" / "config" / "plugins"
        for legacy in ("aifactory-coder", *LEGACY_PLUGINS):
            legacy_path = global_plugins_dir / legacy
            if legacy_path.is_symlink() or legacy_path.exists():
                try:
                    _remove_path(legacy_path)
                    print(f"🧹 Removed legacy plugin: {legacy_path}")
                except OSError as exc:
                    print(f"❌ Failed to remove legacy plugin: {exc}", file=sys.stderr)
                    return 1
        installs.append((global_plugins_dir / PLUGIN_NAME, requested, None))

    if args.workspace:
        ws_path = Path(args.workspace).resolve()
        destination = ws_path / ".agents" / "plugins" / PLUGIN_NAME
        for legacy in LEGACY_PLUGINS:
            _remove_legacy_workspace_entry(ws_path, plugins_dir / legacy, ws_path / ".agents" / "plugins" / legacy)
            _remove_path(ws_path / ".agents" / "plugins" / legacy)
        installs.append((destination, requested, ws_path))

    try:
        for destination, packs, workspace in installs:
            action = _install_plugin_projection(packs, destination, repo_root, workspace_agents=workspace is not None)
            if workspace is not None:
                previous = {p.get("stack"): p.get("paths") for p in read_stack_file(workspace).get("packs", [])}
                spec = {
                    "plugin_version": manifest["plugin_version"],
                    "packs": [{k: load_pack(plugins_dir, s)[k] for k in ("stack", "title", "status")} for s in packs],
                }
                write_stack_file(workspace, spec, {s: previous.get(s) for s in packs})
            print(
                f"✅ Plugin {action}: {destination} packs={combo_key(packs)} "
                f"(version={manifest['plugin_version']}, source={_source_revision(repo_root)})"
            )
    except (OSError, ValueError) as exc:
        print(f"❌ Failed to install plugin: {exc}", file=sys.stderr)
        return 1
    return 0
