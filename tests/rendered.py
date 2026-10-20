"""Rendered (installed) Flutter projection for content assertions.

Agents and skills are composed at build time (core + frontend layer + Flutter pack), so
content checks read what a Flutter workspace actually receives.
"""

from functools import lru_cache
from pathlib import Path
import tempfile

from coder_nexus.plugin_build import build_variant

_TMP = tempfile.TemporaryDirectory()


@lru_cache(maxsize=None)
def flutter_workspace() -> Path:
    return build_variant("fe-flutter", "workspace", Path(_TMP.name)) / "files"


def rendered_agent(name: str) -> str:
    return (flutter_workspace() / ".agents/agents" / name).read_text(encoding="utf-8")
