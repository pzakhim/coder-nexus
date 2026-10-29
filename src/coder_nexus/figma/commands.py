"""CLI handlers for `coder-nexus figma …` (read-only)."""

import argparse
import json
import os
from pathlib import Path

from .client import fetch, load_figma_token

EXIT_CODES = {"READ": 0, "UNREACHABLE": 1, "NOT_PROVIDED": 2}


def add_figma_parser(subparsers) -> None:
    p_fig = subparsers.add_parser("figma", help="Read-only Figma extraction (needs FIGMA_TOKEN in the Client .env)")
    fig_sub = p_fig.add_subparsers(dest="figma_command", required=True)
    p_fetch = fig_sub.add_parser(
        "fetch",
        help="Save frame/section as <node>.png/.jpg, per-screen images, <node>.json, <node>.spec.json and <node>.summary.md",
    )
    p_fetch.add_argument("url", help="Figma frame/section link (figma.com/design/<key>/…?node-id=1150-10051)")
    p_fetch.add_argument("--workspace-path", help="Path to client project workspace containing .env")
    p_fetch.add_argument("--out", help="Output folder (default: <workspace>/.superpowers/sources/figma/)")
    p_fetch.add_argument("--format", dest="image_format", choices=["png", "jpg"], default="png", help="Rendered image format (default: png)")
    p_fetch.add_argument("--export-icons", action="store_true", help="Also export detected pure-vector icon nodes as .svg files under <out>/icons/")
    p_fetch.add_argument("--json", action="store_true", help="Print the result as JSON")


def cmd_figma(args: argparse.Namespace) -> int:
    from ..server import ensure_sources_ignored
    workspace = Path(args.workspace_path).resolve() if args.workspace_path else Path(os.getcwd())
    if args.out:
        out = Path(args.out).resolve()
    else:
        out = workspace / ".superpowers" / "sources" / "figma"
        ensure_sources_ignored(out)
    result = fetch(
        args.url,
        out,
        load_figma_token(str(workspace)),
        image_format=getattr(args, "image_format", "png"),
        export_icons=getattr(args, "export_icons", False),
    )
    if args.json:
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
    elif result.status == "READ":
        print(f"✅ READ {result.name or result.node_id}")
        for path in (
            result.png_path,
            *[p for p in result.screen_images if p != result.png_path],
            *result.icon_svg_paths,
            result.tokens_path,
            result.spec_path,
            result.json_path,
            result.summary_path,
        ):
            if path:
                print(f"   {path}")
        if result.note:
            print(f"   ⚠️  {result.note}")
    else:
        print(f"⛔ {result.status}: {result.note}")
    return EXIT_CODES.get(result.status, 1)
