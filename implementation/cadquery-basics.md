# CadQuery basics

This page is a **practical cheat-sheet** for CadQuery: how to model simple parts and export STEP.

## Install (pip-only)

CadQuery depends on native wheels (OCP / OpenCASCADE). For best wheel coverage, prefer **Python 3.10–3.12**.

```bash
python -m pip install --upgrade pip
python -m pip install cadquery
```

## Mental model

- **`Workplane("XY")`**: choose a reference plane.
- **Method chaining**: build up operations step-by-step.
- **Selectors** (`faces(...)`, `edges(...)`, `vertices(...)`): pick subsets to operate on.

## Minimal example: box → STEP

```python
import cadquery as cq

part = cq.Workplane("XY").box(10, 20, 30)
part.export("box_cadquery.step")
```

## Sketch → extrude (typical workflow)

```python
import cadquery as cq

plate = (
    cq.Workplane("XY")
    .rect(80, 60)
    .extrude(10)
)

plate.export("plate.step")
```

## Holes and pockets

### Through hole on the top face

```python
import cadquery as cq

part = (
    cq.Workplane("XY")
    .box(80, 60, 10)
    .faces(">Z").workplane()
    .hole(6)  # diameter
)

part.export("hole.step")
```

### Multiple holes (bolt pattern)

```python
import cadquery as cq

points = [(-30, -20), (30, -20), (30, 20), (-30, 20)]

part = (
    cq.Workplane("XY")
    .box(80, 60, 10)
    .faces(">Z").workplane()
    .pushPoints(points)
    .hole(5)
)

part.export("bolt_pattern.step")
```

## Fillet / chamfer

```python
import cadquery as cq

part = (
    cq.Workplane("XY")
    .box(30, 30, 10)
    .edges("|Z")       # edges parallel to Z axis
    .fillet(2.0)
)

part.export("fillet.step")
```

## Booleans

```python
import cadquery as cq

base = cq.Workplane("XY").box(40, 30, 10)
cut = cq.Workplane("XY").circle(6).extrude(20).translate((0, 0, -5))

result = base.cut(cut)
result.export("boolean_cut.step")
```

## Transforms (translate / rotate)

```python
import cadquery as cq

part = cq.Workplane("XY").box(10, 10, 10).translate((5, 0, 0))
part.export("translated.step")
```

## Assemblies (names/colors) → STEP

```python
import cadquery as cq
from cadquery import Assembly, Color

assy = Assembly()
assy.add(cq.Workplane("XY").box(20, 10, 5), name="base", color=Color(1, 0, 0))
assy.add(cq.Workplane("XY").circle(2).extrude(10).translate((0, 0, 2.5)), name="pin", color=Color(0, 0.6, 1))
assy.export("assembly.step")
```

## Face-level colors in STEP (color only specific faces)

CadQuery’s plain `shape.export("x.step")` is great for geometry, but **face-level colors** are typically handled via **Assembly metadata**.

If you want to color a specific face (e.g. the `+Z` face) and export that metadata into STEP, use:

- `Assembly.addSubshape(...)` to attach a color to a face/edge/etc.
- `exportStepMeta(...)` to write STEP including that metadata

```python
import cadquery as cq
from cadquery.occ_impl.exporters.assembly import exportStepMeta

cube = cq.Workplane("XY").box(10, 10, 10)

assy = cq.Assembly(name="colored_face_test")
assy.add(cube, name="cube_body", color=cq.Color("lightgray"))

top_face = cube.faces(">Z").val()
assy.addSubshape(top_face, name="top_face", color=cq.Color("red"))

exportStepMeta(assy, "colored_face.step", write_pcurves=True)
```

> [!NOTE]
> - Not all CAD viewers/importers display **per-face colors** consistently.
> - `exportStepMeta` may flatten some assembly structure depending on how you use it.
> - **CadQuery version matters**: `exportStepMeta` is available in newer CadQuery (e.g. 2.6.x). Older versions may not expose it.
> - **Environment matters**: mixing CadQuery/build123d in one environment can cause `cadquery-ocp` conflicts; prefer separate venvs.

### Verified in this repo (and the lessons learned)

This repo includes a script that generates a face-colored STEP artifact:

- `tests/python_step_export/generate_cadquery_face_colored_step.py`
- output: `tests/python_step_export/output/cq_face_colored_top_red.step`

**Lessons learned / pitfalls**:

- **Don’t mix OCCT stacks**: build123d and cadquery may require different `cadquery-ocp` versions → create separate virtualenvs.
- **VTK can silently be “half installed”**: if you see `ModuleNotFoundError: vtkmodules.vtkCommonDataModel`, reinstall `vtk` cleanly (remove stale `vtkmodules/` first) inside the venv.

## Notes (pip-only stability)

- If `pip install cadquery` fails, it is usually a **wheel availability** issue (Python version / OS / architecture).
- On some Windows environments, OCCT-based packages may **crash at interpreter shutdown**. In this repo we generate artifacts via an isolated-subprocess script:
  - `tests/python_step_export/generate_step_examples.py`

## See also

- **[Exporting STEP from Python (pip-only)](./python-step-export.md)**
- **[Exporting STEP from Python (FreeCAD)](./freecad-step-export.md)**
- CadQuery docs: `https://cadquery.readthedocs.io/`

