from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

import pytest


def test_build123d_export_step_smoke(
    tmp_path: Path,
    copy_artifact: Callable[[Path, str], Path],
) -> None:
    if os.environ.get("STEP_EXPORT_INTEGRATION") != "1":
        pytest.skip("Set STEP_EXPORT_INTEGRATION=1 to run OCCT integration tests.")

    build123d = pytest.importorskip("build123d")

    part = build123d.Box(10, 20, 30)
    out = tmp_path / "box_build123d.step"
    build123d.export_step(part, str(out))

    text = out.read_text(encoding="utf-8", errors="replace")
    assert text.startswith("ISO-10303-21;")
    assert "HEADER;" in text
    assert "DATA;" in text
    assert "END-ISO-10303-21;" in text

    copy_artifact(out, "box_build123d.step")

