# build123d basics

This page is a **practical cheat-sheet** for build123d: how to create simple solids and export STEP.

## Install (pip-only)

build123d depends on native wheels (OpenCASCADE via OCP). For best wheel coverage, prefer **Python 3.10–3.12**.

```bash
python -m pip install --upgrade pip
python -m pip install build123d
```

## Mental model

build123d supports multiple styles. For beginners, start with:

- **Primitive solids** (e.g., `Box(...)`) and export
- then move to **builder APIs** (`BuildPart`, `BuildSketch`, …) as your models grow

## Minimal example: box → STEP

This matches the integration test style in this repo.

```python
from build123d import Box, export_step

part = Box(10, 20, 30)
export_step(part, "box_build123d.step")
```

## Verify the examples in this repo

This repository includes a small runner that exports the “basics” examples into:

- `tests/python_step_export/output/`

Run:

```bash
python tests/python_step_export/run_build123d_basics_examples.py
```

It should generate:

- `tests/python_step_export/output/b3d_basics_box.step`

## Subtractive feature (simple “hole” via boolean cut)

The exact boolean API can differ by version and style, so the most robust pattern is:

- create solids
- use the library’s boolean operations for subtraction

If you use the builder API, you can express subtraction with modes (version-dependent). Refer to the official docs for your version.

## Selecting geometry (faces / edges)

build123d has a strong selection/filter story. Common patterns include:

- sorting faces by axis direction (e.g., “top face” by +Z)
- filtering by geometry type (e.g., circular edges)

Because selectors are version-sensitive, this guide keeps examples minimal and points to the official selector tutorial.

## STEP export notes

- If your environment has both CadQuery and build123d installed, their STEP outputs may differ in schema defaults and entity ordering.
- Some versions may also **conflict on `cadquery-ocp` requirements**. If you hit that, use separate virtualenvs.
- For “generate and compare” in this repo, run:

```bash
python tests/python_step_export/generate_step_examples.py
```

Generated files go to:

- `tests/python_step_export/output/`

## See also

- **[Exporting STEP from Python (pip-only)](./python-step-export.md)**
- build123d docs: `https://build123d.readthedocs.io/`

