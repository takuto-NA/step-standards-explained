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
    from cadquery import Assembly, Color

    d = out_dir()

    # 1) Minimal example: box → STEP
    cq.Workplane("XY").box(10, 20, 30).export(str(d / "cq_basics_box.step"))

    # 2) Sketch → extrude
    (
        cq.Workplane("XY")
        .rect(80, 60)
        .extrude(10)
        .export(str(d / "cq_basics_plate.step"))
    )

    # 3) Through hole on the top face
    (
        cq.Workplane("XY")
        .box(80, 60, 10)
        .faces(">Z")
        .workplane()
        .hole(6)
        .export(str(d / "cq_basics_hole.step"))
    )

    # 4) Multiple holes (bolt pattern)
    points = [(-30, -20), (30, -20), (30, 20), (-30, 20)]
    (
        cq.Workplane("XY")
        .box(80, 60, 10)
        .faces(">Z")
        .workplane()
        .pushPoints(points)
        .hole(5)
        .export(str(d / "cq_basics_bolt_pattern.step"))
    )

    # 5) Fillet
    (
        cq.Workplane("XY")
        .box(30, 30, 10)
        .edges("|Z")
        .fillet(2.0)
        .export(str(d / "cq_basics_fillet.step"))
    )

    # 6) Boolean cut
    base = cq.Workplane("XY").box(40, 30, 10)
    cut = cq.Workplane("XY").circle(6).extrude(20).translate((0, 0, -5))
    base.cut(cut).export(str(d / "cq_basics_boolean_cut.step"))

    # 7) Translate
    cq.Workplane("XY").box(10, 10, 10).translate((5, 0, 0)).export(
        str(d / "cq_basics_translated.step")
    )

    # 8) Assembly (names/colors) → STEP
    assy = Assembly()
    assy.add(
        cq.Workplane("XY").box(20, 10, 5),
        name="base",
        color=Color(1, 0, 0),
    )
    assy.add(
        cq.Workplane("XY").circle(2).extrude(10).translate((0, 0, 2.5)),
        name="pin",
        color=Color(0, 0.6, 1),
    )
    assy.export(str(d / "cq_basics_assembly.step"))

    print(f"CadQuery basics examples exported to: {d}")

    # Some OCCT-based environments crash during interpreter shutdown.
    # Force hard-exit after generating artifacts.
    os._exit(0)


if __name__ == "__main__":
    raise SystemExit(main())

