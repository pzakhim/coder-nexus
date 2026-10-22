"""`skill-factory list | get`: copy skill generators into a workspace that then owns them."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .catalog import CatalogError, Generator, list_generators, resolve
from .installer import get

EXIT_OK, EXIT_SKIPPED, EXIT_USAGE = 0, 1, 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill-factory",
        description="Copy create-*-skill generators into a workspace; the workspace owns and edits the copies.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List skill generators")
    p_list.add_argument("-p", "--package", help="Only generators of this package (e.g. coder)")
    p_list.add_argument("--json", action="store_true", help="Print the list as JSON")

    p_get = sub.add_parser(
        "get",
        help="Copy generators into <workspace>/.agents/skills/",
        description="Default mode is --skills: `get clean-code` = `get -s clean-code`. `get .` copies every generator.",
    )
    p_get.add_argument("names", nargs="*", help="Generator names (full or short), or `.` for all")
    p_get.add_argument("-s", "--skills", nargs="+", default=[], help="Generator names (full or short)")
    p_get.add_argument("-p", "--package", help="Every generator of this package (e.g. coder)")
    p_get.add_argument("--workspace", help="Target workspace (default: current directory)")
    p_get.add_argument("--force", action="store_true", help="Replace generators (and the copied core) that already exist")
    p_get.add_argument("--no-claude-link", action="store_true", help="Do not add .claude/skills/<name> symlinks")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return _cmd_list(args) if args.command == "list" else _cmd_get(args)
    except CatalogError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return EXIT_USAGE


def _cmd_list(args: argparse.Namespace) -> int:
    generators = list_generators(args.package)
    if args.json:
        rows = [{"name": g.name, "version": g.version, "packages": list(g.packages), "description": g.description} for g in generators]
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return EXIT_OK
    width = max(len(g.name) for g in generators)
    for g in generators:
        packages = ",".join(g.packages) or "-"
        print(f"{g.name:<{width}}  {g.version:<7} {packages:<8} {_first_sentence(g.description)}")
    return EXIT_OK


def _cmd_get(args: argparse.Namespace) -> int:
    generators = _selection(args)
    workspace = Path(args.workspace).resolve() if args.workspace else Path(os.getcwd())
    result = get(workspace, generators, force=args.force, claude_link=not args.no_claude_link)
    for line in result.copied:
        print(f"✅ {line}")
    for line in result.linked:
        print(f"   🔗 {line}")
    if result.core:
        print(f"   {result.core}")
    for line in result.skipped:
        print(f"⚠️  {line}", file=sys.stderr)
    if result.copied:
        print(f"Next: run a generator in this workspace, e.g. /{generators[0].name}")
    return EXIT_OK if result.ok else EXIT_SKIPPED


def _selection(args: argparse.Namespace) -> list[Generator]:
    names = list(args.names) + list(args.skills)
    if "." in names:
        if len(names) > 1 or args.package:
            raise CatalogError("`.` means every generator; do not combine it with names or --package.")
        return list_generators()
    if args.package and names:
        raise CatalogError("Use either skill names (-s) or --package, not both.")
    if args.package:
        return list_generators(args.package)
    if not names:
        raise CatalogError("Nothing to get: give skill names, -p <package>, or `.` for all.")
    return resolve(names)


def _first_sentence(text: str) -> str:
    # Descriptions read "Write a workspace's own X skill ... - <what it covers> - for any stack ...":
    # the second segment is the informative one.
    parts = text.split(" - ")
    head = (parts[1] if len(parts) > 1 else parts[0]).split(". ")[0]
    return head if len(head) <= 90 else head[:87] + "..."


if __name__ == "__main__":
    sys.exit(main())
