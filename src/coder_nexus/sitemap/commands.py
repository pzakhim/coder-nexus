"""CLI handlers for `coder-nexus sitemap ...` (read-only HTML sitemap extraction)."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re

from .extractor import extract_sitemap, inspect_sitemap

EXIT_CODES = {"READ": 0, "UNSUPPORTED": 2, "ERROR": 1}


def _safe_stem(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", path.stem).strip("._-") or "sitemap"


def add_sitemap_parser(subparsers) -> None:
    p_map = subparsers.add_parser(
        "sitemap",
        help="Extract stages, screen specs, element logic tables, and PNG renders from an interactive HTML sitemap",
    )
    map_sub = p_map.add_subparsers(dest="sitemap_command", required=True)

    p_inspect = map_sub.add_parser(
        "inspect",
        help="Read-only summary of stages and screen counts inside an interactive HTML sitemap (writes nothing)",
    )
    p_inspect.add_argument("html_path", help="Path to the interactive HTML sitemap file")
    p_inspect.add_argument("--json", action="store_true", help="Print the result as JSON")

    p_extract = map_sub.add_parser(
        "extract",
        help="Write lightweight index.json/index.md plus filtered per-screen .png, .spec.json, and .md files",
    )
    p_extract.add_argument("html_path", help="Path to the interactive HTML sitemap file")
    p_extract.add_argument("--workspace-path", help="Client workspace root (default: cwd)")
    p_extract.add_argument(
        "--out",
        help="Output folder (default: <workspace>/.superpowers/sources/sitemap/<html-stem>/)",
    )
    p_extract.add_argument(
        "--stage",
        action="append",
        help="Filter by stage ID, number, or label (comma-separated or repeated, e.g. --stage STAGE_2,STAGE_3)",
    )
    p_extract.add_argument(
        "--screens",
        action="append",
        help="Filter by screen code/group (comma-separated or repeated, e.g. --screens M-05,M-06,BS-03)",
    )
    p_extract.add_argument(
        "--ids",
        action="append",
        help="Filter by screen IDs or ranges (comma-separated or repeated, e.g. --ids H19-H25 or H01,H02)",
    )
    p_extract.add_argument(
        "--query",
        help="Case-insensitive substring search across title, screen code, and screen content",
    )
    p_extract.add_argument(
        "--include-neighbors",
        action="store_true",
        help="Also extract direct parent and child screens connected to matched screens",
    )
    p_extract.add_argument(
        "--index-only",
        action="store_true",
        help="Write only index.json and index.md without unpacking per-screen files or PNGs",
    )
    p_extract.add_argument(
        "--no-images",
        action="store_true",
        help="Write per-screen .spec.json and .md without decoding PNG images",
    )
    p_extract.add_argument("--json", action="store_true", help="Print the result as JSON")


def cmd_sitemap(args: argparse.Namespace) -> int:
    from ..server import ensure_sources_ignored

    if args.sitemap_command == "inspect":
        result = inspect_sitemap(args.html_path)
        if args.json:
            print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
        elif result.status == "READ":
            print(f"✅ READ {result.title} ({result.total_stages} stages, {result.total_screens} screens)")
            for st in result.stages_summary:
                print(
                    f"   - {st['id']} ({st.get('code', '')}): {st['screen_count']} screens "
                    f"[{st.get('module_code') or ''}] — {st.get('title') or ''}"
                )
        else:
            print(f"⛔ {result.status}: {result.note}")
        return EXIT_CODES.get(result.status, 1)

    workspace = Path(args.workspace_path).resolve() if args.workspace_path else Path(os.getcwd())
    src_path = Path(args.html_path).resolve()
    if args.out:
        out = Path(args.out).resolve()
    else:
        out = workspace / ".superpowers" / "sources" / "sitemap" / _safe_stem(src_path)
        ensure_sources_ignored(out.parent)

    result = extract_sitemap(
        src_path,
        out,
        stages_filter=getattr(args, "stage", None),
        screen_codes_filter=getattr(args, "screens", None),
        ids_filter=getattr(args, "ids", None),
        query=getattr(args, "query", None),
        include_neighbors=bool(getattr(args, "include_neighbors", False)),
        index_only=bool(getattr(args, "index_only", False)),
        extract_images=not bool(getattr(args, "no_images", False)),
    )

    if args.json:
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
    elif result.status == "READ":
        print(
            f"✅ READ {result.title} "
            f"({result.total_stages} stages, {result.total_screens} total, {result.extracted_screens} extracted)"
        )
        print(f"   Index MD  : {result.index_md_path}")
        print(f"   Index JSON: {result.index_json_path}")
        if result.screen_markdowns:
            print(f"   Screens   : {len(result.screen_markdowns)} specs + {len(result.screen_images)} images in {Path(result.out_dir or out) / 'screens'}")
        if result.note:
            print(f"   ℹ️  {result.note}")
    else:
        print(f"⛔ {result.status}: {result.note}")
    return EXIT_CODES.get(result.status, 1)
