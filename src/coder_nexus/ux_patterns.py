"""Read-only UX error/edge-case patterns for `get_ux_error_patterns`."""

import json
from pathlib import Path
from typing import Any

PATTERNS_PATH = Path(__file__).with_name("ux_patterns.json")


def get_ux_pattern(scenario: str) -> dict[str, Any]:
    """Return the UX pattern for a scenario, or a structured error."""
    try:
        patterns = json.loads(PATTERNS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {"status": "error", "error": f"UX patterns failed to load: {exc}"}

    clean = (scenario or "").strip().lower()
    if not clean:
        return {"status": "error", "error": "scenario is required."}

    for pattern in patterns:
        if pattern["scenario"].lower() == clean:
            return {"status": "success", "pattern": pattern}

    available = [p["scenario"] for p in patterns]
    return {"status": "error", "error": f"Scenario '{scenario}' not found. Available scenarios: {available}"}
