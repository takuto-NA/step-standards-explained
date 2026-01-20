from __future__ import annotations

import os
from pathlib import Path


def out_dir() -> Path:
    override = os.environ.get("STEP_EXPORT_OUTPUT_DIR")
    d = Path(override) if override else Path(__file__).resolve().parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def main() -> int:
    # OCP-only: generate a box, color only the top face, write STEP-CAF.
    from OCP.BRepBndLib import BRepBndLib
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCP.Bnd import Bnd_Box
    from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
    from OCP.STEPCAFControl import STEPCAFControl_Writer
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.TDocStd import TDocStd_Document
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TDF import TDF_LabelSequence
    from OCP.TopoDS import TopoDS
    from OCP.XCAFDoc import XCAFDoc_ColorType, XCAFDoc_DocumentTool

    d = out_dir()
    out = d / "ocp_face_colored_top_red.step"

    solid = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()

    # Pick "top" face by max Z of its bounding box.
    top_face = None
    top_z = None
    exp = TopExp_Explorer(solid, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        bb = Bnd_Box()
        BRepBndLib.Add_s(face, bb)
        xmin, ymin, zmin, xmax, ymax, zmax = bb.Get()
        if top_z is None or zmax > top_z:
            top_z = zmax
            top_face = face
        exp.Next()

    if top_face is None:
        raise RuntimeError("Failed to find a face to color")

    # XDE document
    doc = TDocStd_Document(TCollection_ExtendedString("ocp-xde"))
    shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())

    main_label = shape_tool.AddShape(solid, False)
    # Base color (light gray) on the whole shape
    color_tool.SetColor(
        main_label,
        Quantity_Color(0.8, 0.8, 0.8, Quantity_TOC_RGB),
        XCAFDoc_ColorType.XCAFDoc_ColorSurf,
    )

    # Add sub-shapes (faces) under the main label.
    # On some bindings, AddSubShape can be picky; we use ComputeShapes + lookup by comparing shapes.
    shape_tool.ComputeShapes(main_label)
    labels = TDF_LabelSequence()
    ok = shape_tool.GetSubShapes_s(main_label, labels)
    if not ok:
        raise RuntimeError("Failed to enumerate sub-shapes for main label.")

    face_label = None
    for i in range(1, labels.Length() + 1):
        lbl = labels.Value(i)
        sh = shape_tool.GetShape_s(lbl)
        try:
            if sh.IsSame(top_face):
                face_label = lbl
                break
        except Exception:
            pass

    if face_label is None or face_label.IsNull():
        raise RuntimeError("Failed to resolve label for top face (cannot assign per-face color).")

    # Top face color (red)
    color_tool.SetColor(
        face_label,
        Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB),
        XCAFDoc_ColorType.XCAFDoc_ColorSurf,
    )

    writer = STEPCAFControl_Writer()
    writer.SetColorMode(True)
    writer.SetNameMode(True)
    writer.Transfer(doc)
    writer.Write(str(out))

    print(f"Wrote: {out}")

    # Some OCCT-based environments crash during interpreter shutdown.
    os._exit(0)


if __name__ == "__main__":
    raise SystemExit(main())

