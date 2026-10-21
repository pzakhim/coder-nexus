"""`coder-nexus ux record`: play walkthroughs in a headless browser and save each as a video.

Playwright is optional (not a Hub dependency). Videos go to `design-uiux/shots/<W-NN>-<viewport>-<orientation>.webm`,
which is git-ignored. A recording shows the scripted MOCK simulation only; it is not a test.
"""

import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from .kitgen import normalize_platform, oriented_size
from .scaffold import ScaffoldError, flows_data, resolve_work_item

PLAYWRIGHT_MISSING = (
    "Playwright is not installed, so no video was recorded. It is optional and not a Coder Nexus dependency: "
    "install it into this environment yourself (`uv pip install playwright` then `uv run playwright install chromium`), "
    "or let the reviewer press ▶ Play in design-uiux/index.html instead."
)


def _viewports(superpowers: Path) -> dict:
    try:
        raw = json.loads((superpowers / "ux" / "viewports.json").read_text(encoding="utf-8")).get("platforms") or {}
    except (OSError, ValueError):
        return {}
    return {k: normalize_platform(k, v) for k, v in raw.items()}


def record_jobs(platforms: dict, viewport: Optional[str] = None, orientation: Optional[str] = None) -> list[dict]:
    """One job per (platform, orientation) to record: size and the index.html query (`platform`, `orientation`)."""
    if viewport and viewport not in platforms:
        raise ScaffoldError(f"Viewport '{viewport}' is not in .superpowers/ux/viewports.json ({', '.join(platforms)}).")
    jobs = []
    for name in ([viewport] if viewport else list(platforms)):
        for orient in platforms[name]["orientations"]:
            if orientation and orient != orientation:
                continue
            w, h = oriented_size(platforms[name], orient)
            jobs.append({"platform": name, "orientation": orient, "width": w, "height": h,
                         "query": f"platform={name}&orientation={orient}&speed=1&chrome=off"})
    if not jobs:
        raise ScaffoldError(f"No platform{' ' + viewport if viewport else ''} allows {orientation} in .superpowers/ux/viewports.json.")
    return jobs


def _estimate_ms(rows: list[dict]) -> int:
    total = 0
    for r in rows:
        total += (r.get("wait") or 1000) + 1500 + 120 * len(str(r.get("value") or ""))
        m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*(ms|s)?", str(r.get("value") or "").strip())
        if r.get("action") == "timer" and not r.get("wait") and m:
            total += int(float(m.group(1)) * (1 if m.group(2) == "ms" else 1000))
    return total


def record(work_item: str, workflow: Optional[str] = None, viewport: Optional[str] = None,
           orientation: Optional[str] = None) -> dict:
    vdir, superpowers, _, _ = resolve_work_item(work_item)
    d = vdir / "design-uiux"
    if not (d / "uiux.md").is_file():
        raise ScaffoldError(f"No design-uiux/uiux.md in {vdir}. Run `coder-nexus ux new` first.")
    data, _ = flows_data(d)
    flows = [f for f in data["flows"] if f.get("walkthrough") and (not workflow or f["id"].upper() == workflow.upper())]
    if not flows:
        raise ScaffoldError(f"No walkthrough{' for ' + workflow if workflow else ''} in uiux.md '## 8. Walkthrough'.")
    platforms = _viewports(superpowers) or {"mobile": normalize_platform("mobile", {"width": 390, "height": 844})}
    jobs = record_jobs(platforms, viewport, orientation)
    if not (d / "data" / "flows.js").is_file():
        raise ScaffoldError("data/flows.js is missing. Run `coder-nexus ux sync` first.")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise ScaffoldError(PLAYWRIGHT_MISSING) from exc

    shots = d / "shots"
    shots.mkdir(exist_ok=True)
    if not (shots / ".gitignore").exists():
        (shots / ".gitignore").write_text("# generated screenshots — not committed\n*\n", encoding="utf-8")
    index = (d / "index.html").resolve().as_uri()
    written = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for job in jobs:
                page_size = {"width": job["width"] + 80, "height": job["height"] + 80}
                for flow in flows:
                    with tempfile.TemporaryDirectory() as tmp:
                        ctx = browser.new_context(viewport=page_size, record_video_dir=tmp, record_video_size=page_size)
                        page = ctx.new_page()
                        page.goto(f"{index}?play={flow['id']}&{job['query']}")
                        page.wait_for_function("['done', 'missing'].includes(document.documentElement.dataset.uxPlay)",
                                               timeout=_estimate_ms(flow["walkthrough"]) + 30000)
                        page.wait_for_timeout(1200)
                        video = page.video
                        ctx.close()
                        target = shots / f"{flow['id']}-{job['platform']}-{job['orientation']}.webm"
                        shutil.move(video.path(), target)
                        written.append(str(target))
        finally:
            browser.close()
    return {"videos": written}
