"""CLI handlers for `coder-nexus ux …`."""

import argparse
import json
from pathlib import Path

from .kitgen import VIEWPORT_PRESETS, extract, load_viewports, parse_size, save_viewports, ux_dir


def add_ux_parser(subparsers) -> None:
    p_ux = subparsers.add_parser("ux", help="UI/UX design support: design source, HTML kit, viewports")
    ux_sub = p_ux.add_subparsers(dest="ux_command", required=True)

    p_ex = ux_sub.add_parser("extract", help="Detect the design source (app-ui-kit / client theme / Material 3) and generate .superpowers/ux/kit/")
    p_ex.add_argument("--project", default=".", help="Client project path (default: cwd)")
    p_ex.add_argument("--brand", help="Override primary color, e.g. '#0055AA' (when the project has none)")
    p_ex.add_argument("--font", help="Override font family")
    p_ex.add_argument("--json", action="store_true", help="Print the design system as JSON")

    p_vp = ux_sub.add_parser("viewports", help="Show or set the project's mockup sizes (asked once per project)")
    p_vp.add_argument("--project", default=".", help="Client project path (default: cwd)")
    p_vp.add_argument("--platforms", help="Comma list of platforms to keep: mobile,tablet,web")
    p_vp.add_argument("--mobile", help="WIDTHxHEIGHT, e.g. 390x844")
    p_vp.add_argument("--tablet", help="WIDTHxHEIGHT, e.g. 820x1180")
    p_vp.add_argument("--web", help="WIDTHxHEIGHT, e.g. 1440x900")
    p_vp.add_argument("--tablet-orientation", choices=["portrait", "landscape"], help="Tablet orientation")
    p_vp.add_argument("--decision", help="D-NN that records the user's answer")
    p_vp.add_argument("--json", action="store_true", help="Print JSON")

    wi_help = "Work-item version folder: .superpowers/work-items/<slug>/vN"
    p_new = ux_sub.add_parser("new", help="Create design-uiux/ for a work item (uiux.md, index.html, CHANGELOG, mock data)")
    p_new.add_argument("--work-item", required=True, help=wi_help)
    p_new.add_argument("--title", required=True, help="Feature title shown in uiux.md and index.html")
    p_new.add_argument("--lang", help="HTML lang of the screens (default: vi)")

    p_sc = ux_sub.add_parser("screen", help="Add a screen (file + row in uiux.md)")
    p_sc.add_argument("--work-item", required=True, help=wi_help)
    p_sc.add_argument("--id", required=True, help="S01, S02, …")
    p_sc.add_argument("--slug", required=True, help="file slug, e.g. receive-qty")
    p_sc.add_argument("--title", required=True)
    p_sc.add_argument("--steps", default="", help="Workflow steps it serves, e.g. 'W-01#2' or 'W-01#1, W-02#1'")
    p_sc.add_argument("--kind", default="NEW", choices=["NEW", "CHANGED", "EXISTING", "new", "changed", "existing"])
    p_sc.add_argument("--catalog", default="", help="Stable screen slug in screen-catalog.md, e.g. wms.is-items.receive")
    p_sc.add_argument("--states", default="default,loading,empty,error", help="Comma list of states")
    p_sc.add_argument("--lang")

    p_co = ux_sub.add_parser("component", help="Add a NEW component drawing (file + row in uiux.md)")
    p_co.add_argument("--work-item", required=True, help=wi_help)
    p_co.add_argument("--id", required=True, help="C01, C02, …")
    p_co.add_argument("--slug", required=True)
    p_co.add_argument("--title", required=True)
    p_co.add_argument("--used-in", default="", help="Screens using it, e.g. 'S01, S02'")
    p_co.add_argument("--lang")

    p_sy = ux_sub.add_parser("sync", help="Rebuild data/flows.js (read by index.html) from uiux.md")
    p_sy.add_argument("--work-item", required=True, help=wi_help)


def _cmd_design(args: argparse.Namespace) -> int:
    from .scaffold import ScaffoldError, add_component, add_screen, new_design, sync
    try:
        if args.ux_command == "new":
            res = new_design(args.work_item, args.title, args.lang)
            print(f"✅ design-uiux ready: {res['design_dir']}")
            for f in res["created"]:
                print(f"   + {f}")
            print("   Next: confirm workflows, then `coder-nexus ux screen …` per step.")
        elif args.ux_command == "screen":
            res = add_screen(args.work_item, args.id, args.slug, args.title, args.steps, args.kind, args.catalog, args.states, args.lang)
            print(("✅ Created " if res["created"] else "ℹ️  Exists  ") + res["file"])
        elif args.ux_command == "component":
            res = add_component(args.work_item, args.id, args.slug, args.title, args.used_in, args.lang)
            print(("✅ Created " if res["created"] else "ℹ️  Exists  ") + res["file"])
        if args.ux_command in ("sync", "screen", "new"):
            res = sync(args.work_item)
            print(f"🔄 flows.js: {res['flows']} workflow(s), {res['screens']} screen(s)")
            for w in res["warnings"]:
                print(f"   ⚠ {w}")
        return 0
    except ScaffoldError as exc:
        print(f"❌ {exc}")
        return 1


def cmd_ux(args: argparse.Namespace) -> int:
    if args.ux_command in ("new", "screen", "component", "sync"):
        return _cmd_design(args)
    project = Path(args.project).resolve()
    if args.ux_command == "extract":
        system = extract(project, brand=args.brand, font=args.font)
        if args.json:
            print(json.dumps(system, ensure_ascii=False, indent=2))
            return 0
        src = system["source"]
        usable = sorted({c["kit_class"] for c in system["components"] if c.get("kit_class")})
        code_only = [c["widget"] for c in system["components"] if not c.get("kit_class")]
        print(f"\n🎨 Design source: {src['kind']} (profile hint: {src['profile_hint']})")
        for ev in src.get("evidence", []):
            print(f"   evidence: {ev}")
        print(f"   font: {system['font']['family']} ({system['font']['from']})")
        print(f"   primary: {system['roles']['primary']['value']} ({system['roles']['primary']['from']})")
        print(f"   kit classes: {', '.join(usable)}")
        if code_only:
            print(f"   widgets without HTML equivalent: {', '.join(code_only)}")
        for w in system.get("warnings", []):
            print(f"   ⚠ {w}")
        print(f"   decision: {src.get('decision') or 'NOT CONFIRMED — confirm the source with the user and record a D-NN'}")
        print(f"\n✅ Wrote {ux_dir(project) / 'design-system.json'}")
        print(f"✅ Wrote {ux_dir(project) / 'kit'}/ (kit.css, kit.js, viewports.js, components.html)")
        print(f"   Preview: open {ux_dir(project) / 'kit' / 'components.html'}\n")
        return 0

    # viewports
    current = load_viewports(project)
    changes = any(getattr(args, k) for k in ("platforms", "mobile", "tablet", "web", "tablet_orientation"))
    if changes:
        platforms = {k: dict(v) for k, v in current["platforms"].items()}
        for name in ("mobile", "tablet", "web"):
            size = getattr(args, name)
            if size:
                w, h = parse_size(size)
                platforms.setdefault(name, {})
                platforms[name].update({"width": w, "height": h})
                platforms[name].setdefault("orientation", "landscape" if w > h else "portrait")
        if args.tablet_orientation and "tablet" in platforms:
            t = platforms["tablet"]
            w, h = sorted((t["width"], t["height"]))
            t["width"], t["height"] = (h, w) if args.tablet_orientation == "landscape" else (w, h)
            t["orientation"] = args.tablet_orientation
        if args.platforms:
            keep = [p.strip() for p in args.platforms.split(",") if p.strip()]
            platforms = {k: v for k, v in platforms.items() if k in keep}
            for k in keep:
                if k not in platforms:
                    from .kitgen import DEFAULT_VIEWPORTS
                    platforms[k] = dict(DEFAULT_VIEWPORTS[k])
        current = save_viewports(project, platforms, args.decision)
    if args.json:
        print(json.dumps(current, ensure_ascii=False, indent=2))
        return 0
    state = "confirmed" + (f" ({current.get('decision')})" if current.get("decision") else "") if current.get("confirmed") else "NOT CONFIRMED (defaults) — ask the user once"
    print(f"\n📐 Viewports: {state}")
    for name, v in current["platforms"].items():
        print(f"   {name:<7} {v['width']}×{v['height']} {v.get('orientation', '')}")
    if not current.get("confirmed"):
        print("\n   Common choices:")
        for name, opts in VIEWPORT_PRESETS.items():
            print(f"   {name:<7} " + " · ".join(opts))
        print("   Set: coder-nexus ux viewports --platforms mobile,tablet --mobile 390x844 --tablet 820x1180 --decision D-NN")
    print()
    return 0
