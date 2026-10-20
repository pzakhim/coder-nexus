#!/usr/bin/env python3
"""Sync version across bundle_manifest.json and package.json."""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def sync_version(version_str: str) -> None:
    # Strip optional 'v' prefix
    version = version_str.lstrip("v").strip()
    if not re.match(r"^\d+\.\d+\.\d+", version):
        print(f"❌ Invalid semver version: '{version_str}'", file=sys.stderr)
        sys.exit(1)

    # 1. Update bundle manifests (Single Source of Truth)
    for plugin_name in ("core",):
        manifest_path = REPO_ROOT / "plugins" / plugin_name / "bundle_manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            old_v = manifest.get("plugin_version")
            manifest["plugin_version"] = version
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            print(f"✅ {plugin_name} bundle_manifest.json: {old_v} -> {version}")

    # 2. Update package.json (VS Code extension wrapper)
    pkg_path = REPO_ROOT / "package.json"
    if pkg_path.exists():
        pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
        old_v = pkg.get("version")
        pkg["version"] = version
        pkg_path.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
        print(f"✅ package.json: {old_v} -> {version}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sync_version.py <version>", file=sys.stderr)
        sys.exit(1)
    sync_version(sys.argv[1])
