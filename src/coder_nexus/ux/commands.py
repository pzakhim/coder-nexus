"""CLI handlers for `coder-nexus ux …`."""

import argparse
import json
from pathlib import Path

from .kitgen import ORIENTATIONS, VIEWPORT_PRESETS, extract, load_viewports, oriented_size, parse_size, save_viewports, ux_dir


def parse_orientations(text: str) -> dict[str, list[str]]:
    """'mobile=portrait,tablet=portrait+landscape' -> {'mobile': ['portrait'], 'tablet': ['portrait', 'landscape']}."""
    out: dict[str, list[str]] = {}
    for part in (p.strip() for p in text.split(",") if p.strip()):
        name, _, value = part.partition("=")
        values = [v.strip().lower() for v in value.split("+") if v.strip()]
        if not name.strip() or not values or any(v not in ORIENTATIONS for v in values):
            raise ValueError(f"Bad orientation '{part}': write platform=portrait, platform=landscape or platform=portrait+landscape")
        out[name.strip()] = list(dict.fromkeys(values))
    return out


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
    p_vp.add_argument("--orientations", help="Per platform: mobile=portrait,tablet=portrait+landscape,web=landscape (first = default)")
    p_vp.add_argument("--tablet-orientation", choices=["portrait", "landscape"], help="Alias of --orientations tablet=<value>")
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

    p_re = ux_sub.add_parser("record", help="Play walkthroughs headless and save videos to design-uiux/shots/ (needs Playwright, optional)")
    p_re.add_argument("--work-item", required=True, help=wi_help)
    p_re.add_argument("--workflow", help="Only this workflow, e.g. W-01 (default: every workflow with a walkthrough)")
    p_re.add_argument("--viewport", help="Only this platform from viewports.json, e.g. mobile (default: all)")
    p_re.add_argument("--orientation", choices=["portrait", "landscape"],
                      help="Only this orientation (default: every orientation each platform allows)")

    p_va = ux_sub.add_parser("validate", help="Check design-uiux/ against rules UX-001…UX-012 (read-only unless --write-hash)")
    p_va.add_argument("--work-item", required=True, help=wi_help)
    p_va.add_argument("--write-hash", action="store_true", help="Store the content hash in uiux.md first (when presenting or approving a revision)")
    p_va.add_argument("--json", action="store_true", help="Print the result as JSON")


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
            print(f"🔄 flows.js: {res['flows']} workflow(s), {res['screens']} screen(s), {res.get('walkthroughs', 0)} walkthrough(s)")
            for w in res["warnings"]:
                print(f"   ⚠ {w}")
        return 0
    except ScaffoldError as exc:
        print(f"❌ {exc}")
        return 1


def _cmd_validate(args: argparse.Namespace) -> int:
    from .scaffold import ScaffoldError
    from .validate import validate_design, write_content_hash
    if args.write_hash:
        try:
            print(f"🔒 Content hash written: {write_content_hash(args.work_item)}")
        except ScaffoldError as exc:
            print(f"❌ {exc}")
            return 1
    res = validate_design(args.work_item)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif res["status"] != "success":
        print(f"❌ {res['message']}")
    else:
        print(f"\n🧪 UI/UX {res['work_item']} {res['version']} {res['revision']} ({res['design_status']}): {res['gate_status']}"
              f" — {res['errors_count']} error(s), {res['warnings_count']} warning(s)")
        for v in res["violations"]:
            icon = "❌" if v["severity"] == "ERROR" else "⚠"
            where = f" (uiux.md:{v['line_number']})" if v["line_number"] else ""
            print(f"   {icon} {v['rule_id']}{where} {v['message']}\n      → {v['suggestion']}")
        print()
    return 0 if res["valid"] else 1


def _cmd_record(args: argparse.Namespace) -> int:
    from .record import record
    from .scaffold import ScaffoldError
    try:
        res = record(args.work_item, args.workflow, args.viewport, getattr(args, "orientation", None))
    except ScaffoldError as exc:
        print(f"❌ {exc}")
        return 1
    for path in res["videos"]:
        print(f"🎬 {path}")
    print("   MOCK simulation of the scripted walkthrough — not a test of app logic.")
    return 0


def cmd_ux(args: argparse.Namespace) -> int:
    if args.ux_command == "record":
        return _cmd_record(args)
    if args.ux_command == "validate":
        return _cmd_validate(args)
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
    try:
        orients = parse_orientations(getattr(args, "orientations", None) or "")
    except ValueError as exc:
        print(f"❌ {exc}")
        return 1
    if getattr(args, "tablet_orientation", None):
        orients.setdefault("tablet", [args.tablet_orientation])
    changes = orients or any(getattr(args, k, None) for k in ("platforms", "mobile", "tablet", "web"))
    if changes:
        from .kitgen import DEFAULT_VIEWPORTS
        platforms = {k: dict(v) for k, v in current["platforms"].items()}
        if args.platforms:
            keep = [p.strip() for p in args.platforms.split(",") if p.strip()]
            platforms = {k: platforms.get(k) or dict(DEFAULT_VIEWPORTS[k]) for k in keep if k in platforms or k in DEFAULT_VIEWPORTS}
        for name in ("mobile", "tablet", "web"):
            size = getattr(args, name, None)
            if size:
                w, h = parse_size(size)
                platforms.setdefault(name, dict(DEFAULT_VIEWPORTS.get(name, {"orientations": []})))
                platforms[name].update({"width": w, "height": h})
                if name not in orients and not platforms[name].get("orientations"):
                    platforms[name]["orientations"] = ["landscape" if w > h else "portrait"]
        unknown = sorted(set(orients) - set(platforms))
        if unknown:
            print(f"❌ --orientations names platform(s) not kept: {', '.join(unknown)} (platforms: {', '.join(platforms)})")
            return 1
        for name, values in orients.items():
            platforms[name]["orientations"] = values
        current = save_viewports(project, platforms, args.decision or current.get("decision"),
                                 orientations_confirmed=bool(orients) or bool(current.get("orientations_confirmed")))
    if args.json:
        print(json.dumps(current, ensure_ascii=False, indent=2))
        return 0
    state = "confirmed" + (f" ({current.get('decision')})" if current.get("decision") else "") if current.get("confirmed") else "NOT CONFIRMED (defaults) — ask the user once"
    print(f"\n📐 Viewports: {state}")
    for name, v in current["platforms"].items():
        sizes = " · ".join(f"{o} {'×'.join(map(str, oriented_size(v, o)))}" for o in v["orientations"])
        print(f"   {name:<7} {sizes}")
    if current.get("confirmed") and not current.get("orientations_confirmed"):
        print("   ⚠ Orientations not confirmed yet — ask the user (portrait / landscape / both per platform), then --orientations …")
    if not current.get("confirmed") or not current.get("orientations_confirmed"):
        print("\n   Common choices:")
        for name, opts in VIEWPORT_PRESETS.items():
            print(f"   {name:<7} " + " · ".join(opts))
        print("   Orientation per platform: portrait · landscape · portrait+landscape (first = default in the viewer)")
        print("   Set: coder-nexus ux viewports --platforms mobile,tablet --mobile 390x844 --tablet 820x1180 "
              "--orientations mobile=portrait,tablet=portrait+landscape --decision D-NN")
    print()
    return 0
