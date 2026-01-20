from __future__ import annotations

import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    """
    FreeCAD-side generator script.

    Run with FreeCADCmd (recommended):
      FreeCADCmd path/to/generate_freecad_step.py path/to/out.step
    """
    if len(argv) >= 2:
        out = Path(argv[1]).expanduser().resolve()
    else:
        out = Path(__file__).resolve().parent / "output" / "box_freecad.step"

    out.parent.mkdir(parents=True, exist_ok=True)

    # FreeCAD modules are provided by FreeCAD's bundled Python runtime.
    import FreeCAD as App  # type: ignore
    import Import  # type: ignore
    import Part  # type: ignore

    doc = App.newDocument("step_export")
    try:
        shape = Part.makeBox(10, 20, 30)
        obj = doc.addObject("Part::Feature", "Box")
        obj.Shape = shape
        doc.recompute()

        # Export format is inferred from the file extension.
        Import.export([obj], str(out))
        print(f"[freecad] wrote: {out}")
        return 0
    finally:
        # Ensure the document doesn't linger between runs.
        try:
            App.closeDocument(doc.Name)
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

