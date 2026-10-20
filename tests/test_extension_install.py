"""Exercise real extension copy behavior with a small VS Code host stub."""

from pathlib import Path
import shutil
import subprocess

import pytest


def test_extension_projection():
    node = shutil.which("node")
    if not node:
        pytest.skip("Node is required for the extension installation checks")
    result = subprocess.run(
        [node, "--test", str(Path(__file__).with_name("extension_install.test.cjs"))],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
