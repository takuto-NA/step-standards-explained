from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture(scope="session")
def artifacts_dir() -> Path:
    """
    Directory where tests copy generated files for easy inspection.

    - Default: tests/python_step_export/output
    - Override: STEP_EXPORT_OUTPUT_DIR=/path/to/dir
    """
    override = os.environ.get("STEP_EXPORT_OUTPUT_DIR")
    if override:
        d = Path(override)
    else:
        d = Path(__file__).resolve().parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture()
def copy_artifact(artifacts_dir: Path) -> Callable[[Path, str], Path]:
    def _copy(src: Path, name: str) -> Path:
        dst = artifacts_dir / name
        dst.write_bytes(src.read_bytes())
        return dst

    return _copy

