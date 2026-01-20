from __future__ import annotations

import os
from pathlib import Path


def out_dir() -> Path:
    override = os.environ.get("STEP_EXPORT_OUTPUT_DIR")
    d = Path(override) if override else Path(__file__).resolve().parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def main() -> int:
    import cadquery as cq
    from cadquery.occ_impl.exporters.assembly import exportStepMeta

    d = out_dir()
    out = d / "cq_face_colored_top_red.step"

    cube = cq.Workplane("XY").box(10, 10, 10)
    top_face = cube.faces(">Z").val()

    # CadQuery route: attach face color as subshape metadata and export STEP with metadata.
    assy = cq.Assembly(name="colored_face_test")
    assy.add(cube, name="cube_body", color=cq.Color("lightgray"))
    assy.addSubshape(top_face, name="top_face", color=cq.Color("red"))

    exportStepMeta(assy, str(out), write_pcurves=True)

    print(f"Wrote: {out}")

    # Some OCCT-based environments crash during interpreter shutdown.
    os._exit(0)


if __name__ == "__main__":
    raise SystemExit(main())

