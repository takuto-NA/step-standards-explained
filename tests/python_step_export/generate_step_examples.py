from __future__ import annotations

import os
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Sequence


def artifacts_dir() -> Path:
    """
    Directory where examples are written for easy inspection.

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


def write_text_minimal_part21(out: Path) -> None:
    out.write_text(
        "\n".join(
            [
                "ISO-10303-21;",
                "HEADER;",
                "FILE_DESCRIPTION(('generated minimal'),'21;1');",
                "FILE_NAME('generated.step','2026-01-20T00:00:00',('generator'),(''), '','', '');",
                "FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));",
                "ENDSEC;",
                "DATA;",
                "#10 = APPLICATION_CONTEXT('managed model based 3d engineering');",
                "ENDSEC;",
                "END-ISO-10303-21;",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )


def try_export_cadquery(out: Path) -> bool:
    try:
        import cadquery as cq  # type: ignore
    except Exception as e:
        print(f"[cadquery] skip: {e}")
        return False

    part = cq.Workplane("XY").box(10, 20, 30)
    part.export(str(out))
    print(f"[cadquery] wrote: {out}")
    return True


def try_export_build123d(out: Path) -> bool:
    try:
        import build123d  # type: ignore
    except Exception as e:
        print(f"[build123d] skip: {e}")
        return False

    part = build123d.Box(10, 20, 30)
    build123d.export_step(part, str(out))
    print(f"[build123d] wrote: {out}")
    return True


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


def try_export_freecad(out: Path) -> bool:
    """
    Export STEP via FreeCAD's Python runtime (FreeCADCmd).

    This is not "pip-only", but it can be very reliable if FreeCAD is installed.
    """
    freecad_cmd = _find_freecad_cmd()
    if not freecad_cmd:
        print("[freecad] skip: set FREECAD_CMD=... (or put FreeCADCmd in PATH)")
        return False

    script = Path(__file__).resolve().parent / "generate_freecad_step.py"
    cp = subprocess.run([freecad_cmd, str(script), str(out)], text=True)
    if cp.returncode != 0:
        print(f"[freecad] failed: exit={cp.returncode}")
        return False

    print(f"[freecad] wrote: {out}")
    return True


def _run_isolated(args: Sequence[str]) -> int:
    """
    Run an exporter in a subprocess so that native cleanup crashes (rare on some
    OCCT builds) don't take down the main generator process.
    """
    cp = subprocess.run([sys.executable, __file__, *args], text=True)
    return cp.returncode


def main() -> int:
    out_dir = artifacts_dir()

    # Always generate a minimal Part 21 text file
    write_text_minimal_part21(out_dir / "minimal.step")
    print(f"[text] wrote: {out_dir / 'minimal.step'}")

    # If installed, also export “real geometry” STEP via each library.
    # Run each exporter in an isolated subprocess to avoid interpreter-exit crashes.
    _run_isolated(["--cadquery", str(out_dir / "box_cadquery.step")])
    _run_isolated(["--build123d", str(out_dir / "box_build123d.step")])
    try_export_freecad(out_dir / "box_freecad.step")

    print(f"Done. Output dir: {out_dir}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--cadquery":
        out = Path(sys.argv[2])
        ok = try_export_cadquery(out)
        # Some OCCT-based environments crash during interpreter shutdown.
        # Force a hard exit after writing artifacts to keep CI/local runs stable.
        os._exit(0 if ok else 0)

    if len(sys.argv) >= 3 and sys.argv[1] == "--build123d":
        out = Path(sys.argv[2])
        ok = try_export_build123d(out)
        os._exit(0 if ok else 0)

    raise SystemExit(main())

