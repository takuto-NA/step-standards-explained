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

## Notes (pip-only stability)

- If `pip install cadquery` fails, it is usually a **wheel availability** issue (Python version / OS / architecture).
- On some Windows environments, OCCT-based packages may **crash at interpreter shutdown**. In this repo we generate artifacts via an isolated-subprocess script:
  - `tests/python_step_export/generate_step_examples.py`

## See also

- **[Exporting STEP from Python (pip-only)](./python-step-export.md)**
- CadQuery docs: `https://cadquery.readthedocs.io/`

