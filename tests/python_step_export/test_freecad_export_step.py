from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable

import pytest


def _find_freecad_cmd() -> str | None:
    """
    Prefer explicit configuration, otherwise try PATH.
    """
    env = os.environ.get("FREECAD_CMD")
    if env:
        return env
    for name in ("FreeCADCmd", "FreeCADCmd.exe"):
        p = shutil.which(name)
        if p:
            return p
    return None


def test_freecad_export_step_smoke(
    tmp_path: Path,
    copy_artifact: Callable[[Path, str], Path],
) -> None:
    if os.environ.get("STEP_EXPORT_INTEGRATION") != "1":
        pytest.skip("Set STEP_EXPORT_INTEGRATION=1 to run integration tests.")

    freecad_cmd = _find_freecad_cmd()
    if not freecad_cmd:
        pytest.skip("Set FREECAD_CMD=... (or put FreeCADCmd in PATH) to run FreeCAD export.")

    script = Path(__file__).resolve().parent / "generate_freecad_step.py"
    out = tmp_path / "box_freecad.step"

    cp = subprocess.run(
        [freecad_cmd, str(script), str(out)],
        text=True,
        capture_output=True,
    )
    assert cp.returncode == 0, f"FreeCADCmd failed.\nstdout:\n{cp.stdout}\nstderr:\n{cp.stderr}"

    text = out.read_text(encoding="utf-8", errors="replace")
    assert text.startswith("ISO-10303-21;")
    assert "HEADER;" in text
    assert "DATA;" in text
    assert "END-ISO-10303-21;" in text

    copy_artifact(out, "box_freecad.step")

