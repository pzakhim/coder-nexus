"""Command Line Interface for AIFactory Coder (coder_nexus): argument parsing and dispatch only."""

import argparse
import sys
from pathlib import Path

from .plugin_install import (
    REPO_ROOT,
    cmd_install_plugin,
)
from .setup.huly import cmd_login, cmd_my_tasks, cmd_setup_huly, cmd_status, cmd_task_detail


def _add_huly_login_args(parser: argparse.ArgumentParser, path_flag: str) -> None:
    parser.add_argument("--url", default=None, help="Huly instance URL (asked if missing; suggested: https://huly.app)")
    parser.add_argument("--email", help="Huly user email or username")
    pw = parser.add_mutually_exclusive_group()
    pw.add_argument("--password", help="Huly user password (prefer --password-stdin: argv is visible in ps/history)")
    pw.add_argument("--password-stdin", action="store_true", help="Read the password from the first line of stdin (non-interactive)")
    parser.add_argument("--reset", action="store_true", help="Ignore saved .env values and ask for URL and account again")
    parser.add_argument("--json", action="store_true", help="Print one JSON result on stdout (for agents); progress goes to stderr")
    parser.add_argument(path_flag, dest="workspace_path", help="Path to client project workspace containing .env")


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="coder_nexus",
        description="AIFactory Coder CLI - Hub client & Huly task manager",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # setup flutter | setup huly
    p_setup = subparsers.add_parser("setup", help="Workspace setup gates (flutter, huly)")
    setup_sub = p_setup.add_subparsers(dest="stack", required=True)

    p_flutter = setup_sub.add_parser("flutter", help="iMESPro/external Flutter project setup gate")
    p_flutter.add_argument("--check", action="store_true", help="Read-only check; exit 0 only when READY")
    p_flutter.add_argument("--protocol", choices=["ssh", "https"], default="ssh", help="Clone protocol (default: ssh)")
    p_flutter.add_argument("--yes", "-y", action="store_true", help="Answer yes to create/clone prompts")
    p_flutter.add_argument("--project", default=".", help="Client project path (default: cwd)")
    p_flutter.add_argument("--project-name", help="Dart/Flutter package name (default: sanitized folder name)")
    p_flutter.add_argument(
        "--profile",
        choices=["imespro", "external-structured", "external-standard"],
        help="Architecture profile (imespro, external-structured, external-standard)",
    )

    p_huly = setup_sub.add_parser("huly", help="Guided Huly setup: check .env, ping URL, log in, save to the project .env (dev only)")
    p_huly.add_argument("--check", action="store_true", help="Read-only: exit 0 only when URL, email, password, session and workspace ID are all in .env")
    _add_huly_login_args(p_huly, "--project")

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Read-only check of Huly login and Flutter setup")
    p_doctor.add_argument("--project", default=".", help="Client project path (default: cwd)")

    # login / status (aliases of `setup huly` / `setup huly --check`)
    p_login = subparsers.add_parser("login", help="Alias of `setup huly`")
    _add_huly_login_args(p_login, "--workspace-path")
    p_status = subparsers.add_parser("status", help="Alias of `setup huly --check` (always exits 0)")
    p_status.add_argument("--workspace-path", help="Path to client project workspace containing .env")

    # my-tasks
    p_tasks = subparsers.add_parser("my-tasks", help="List uncompleted tasks assigned to user")
    p_tasks.add_argument("--workspace-path", help="Path to client project workspace containing .env")
    p_tasks.add_argument("--json", action="store_true", help="Output in raw JSON format")
    p_tasks.add_argument("--all", dest="include_all", action="store_true", help="Open tasks of the whole workspace, not only yours")

    # task-detail
    p_detail = subparsers.add_parser("task-detail", help="Get full details and acceptance criteria for a task")
    p_detail.add_argument("task_id", help="Issue ID (AUTH-101), unique number, Huly _id, or a Huly issue link")
    p_detail.add_argument("--workspace-path", help="Path to client project workspace containing .env")
    p_detail.add_argument("--json", action="store_true", help="Output in raw JSON format")
    p_detail.add_argument("--download", action="store_true", help="Save files/images/attachments/readable docs (and the Figma frame, with FIGMA_TOKEN) to .superpowers/sources/<ID>/")

    # huly-debug (read-only diagnostics)
    p_dbg = subparsers.add_parser("huly-debug", help="Read-only: dump raw Huly responses for one issue to a JSON file (no tokens)")
    p_dbg.add_argument("task_id", help="Issue ID or Huly issue link")
    p_dbg.add_argument("--workspace-path", help="Path to client project workspace containing .env")
    p_dbg.add_argument("--out", help="Output file (default: ./huly-debug-<ID>.json)")

    # ux (design source, HTML kit, viewports)
    from .ux.commands import add_ux_parser
    add_ux_parser(subparsers)

    # figma (read-only frame extraction)
    from .figma.commands import add_figma_parser
    add_figma_parser(subparsers)

    # serve
    subparsers.add_parser("serve", help="Start the AIFactory MCP Server listening on stdio")

    # install-plugin
    p_install = subparsers.add_parser("install-plugin", help="Install coder-nexus plugin into Antigravity IDE (source checkout only)")
    p_install.add_argument(
        "--plugin",
        default="fe",
        choices=["fe", "be"],
        help="Legacy shortcut: fe (pack from --framework) or be (backend pack), default: fe",
    )
    p_install.add_argument(
        "--framework",
        default="flutter",
        choices=["flutter", "frappe"],
        help="Target frontend framework: flutter or frappe (only used when plugin=fe), default: flutter",
    )
    p_install.add_argument(
        "--pack",
        action="append",
        help="Stack pack to install (repeatable): flutter, frappe, backend. Overrides --plugin/--framework.",
    )
    p_install.add_argument(
        "--replace",
        action="store_true",
        help="Install exactly the given packs instead of adding them to the packs in .agents/stack.json",
    )
    p_install.add_argument(
        "--global",
        dest="is_global",
        action="store_true",
        help="Install into global ~/.gemini/config/plugins/ directory",
    )
    p_install.add_argument(
        "--workspace",
        help="Workspace to install into (.agents/plugins/coder-nexus, .agents/agents, .agents/stack.json)",
    )

    return parser


def cmd_setup_flutter(args: argparse.Namespace) -> int:
    """Handle `coder_nexus setup flutter` command."""
    from .setup.flutter import run_setup
    project_path = Path(args.project).resolve()
    code = run_setup(
        project_path,
        protocol=args.protocol,
        check_only=args.check,
        assume_yes=args.yes,
        project_name=getattr(args, "project_name", None),
        profile=getattr(args, "profile", None),
    )
    if code == 0 and not args.check and (REPO_ROOT / "plugins" / "core").exists():
        cmd_install_plugin(argparse.Namespace(workspace=str(project_path), pack=["flutter"], is_global=False, replace=False))
    return code


def cmd_setup(args: argparse.Namespace) -> int:
    return cmd_setup_huly(args) if args.stack == "huly" else cmd_setup_flutter(args)


def cmd_doctor(args: argparse.Namespace) -> int:
    """Read-only: Huly status (informational, Huly is optional) and Flutter setup gate."""
    from .setup.flutter import run_setup
    cmd_status(argparse.Namespace(workspace_path=args.project))
    return run_setup(Path(args.project).resolve(), check_only=True)


def cmd_huly_debug(args: argparse.Namespace) -> int:
    from .huly.debug import write_debug
    try:
        path = write_debug(args.task_id, args.workspace_path, args.out)
    except Exception as exc:  # noqa: BLE001
        print(f"❌ huly-debug failed: {exc}", file=sys.stderr)
        return 1
    print(f"✅ Wrote {path} (no tokens or passwords inside). Share this file to align the client with your server.")
    return 0


def _cmd_ux(args: argparse.Namespace) -> int:
    from .ux.commands import cmd_ux
    return cmd_ux(args)


def _cmd_figma(args: argparse.Namespace) -> int:
    from .figma.commands import cmd_figma
    return cmd_figma(args)


def cmd_serve(args: argparse.Namespace) -> int:
    """Handle `coder_nexus serve` command to start MCP server over stdio."""
    from .server import run_server
    run_server()
    return 0


def main() -> int:
    """Entry point for CLI execution."""
    import logging
    for noisy in ("httpx", "httpcore"):  # per-request INFO lines drown the CLI output
        logging.getLogger(noisy).setLevel(logging.WARNING)
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    command_handlers = {
        "setup": cmd_setup,
        "doctor": cmd_doctor,
        "login": cmd_login,
        "status": cmd_status,
        "my-tasks": cmd_my_tasks,
        "task-detail": cmd_task_detail,
        "serve": cmd_serve,
        "huly-debug": cmd_huly_debug,
        "ux": _cmd_ux,
        "figma": _cmd_figma,
        "install-plugin": cmd_install_plugin,
    }

    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
