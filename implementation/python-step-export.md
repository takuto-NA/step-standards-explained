# Exporting STEP from Python (pip-only)

This page summarizes **reliable ways to generate STEP files from Python** when you cannot use conda (pip-only environments), and gives a practical, testable recommendation.

---

## Recommendation (Most Reliable)

**Difficulty**: ★★☆ (Intermediate)  
**Frequency**: ★★★ (Very Common)  
**Impact**: 🔴 High (Enables automated exports, CI, batch generation)

If you need **valid B-rep solids/surfaces** (not just a toy example), the most reliable approach in a pip-only environment is:

- **CadQuery (recommended) or build123d** as the modeling API
- backed by **OpenCASCADE via OCP wheels** (binary distributions)
- then export to **STEP (Part 21)** using the library’s exporter

This avoids writing AP schemas and B-rep topology by hand.

---

## Why “hand-writing STEP text” is rarely the right answer

STEP is a text format (Part 21), but **the hard part is not the syntax**—it’s correctly encoding:

- topology (shells/faces/edges/vertices and their orientation)
- geometry (analytic + NURBS surfaces/curves, trimming, p-curves)
- units, contexts, representation structure
- interoperability constraints (CAx-IF recommended practices)

If you want to learn the structure, see:
- **[Minimal Export Template](./minimal-export.md)** (start here)

For production export, use a CAD kernel (OpenCASCADE) via Python bindings.

---

## Option Matrix (pip-only)

| Option | What you get | pip-only reliability | Best for |
|---|---|---:|---|
| **CadQuery + OCP** | High-level CAD scripting + solid STEP export | ✅ Usually good (if wheels exist for your Python/OS) | Most users, parametric parts, basic assemblies |
| **build123d + OCP** | Modern Pythonic CAD scripting + STEP export | ✅ Usually good (same wheel constraints) | Clean code, newer API preference |
| **OCP direct** | Low-level OpenCASCADE API access | ⚠️ Medium (harder API, same wheel constraints) | When you need a feature not exposed by higher-level libs |
| **Text / Part 21 by hand** | Full control, no native deps | ✅ Installs anywhere | Educational, fixed tiny templates only |
| pythonOCC-core | Another OCCT binding | ⚠️ Often problematic with pip-only | Only if your environment already supports it |

---

## Prerequisites (best practice)

### Pin Python versions that have wheels

In pip-only setups, success is mostly determined by whether **binary wheels** are available for:

- your **OS** (Windows / macOS / Linux)
- your **Python version**
- your **architecture** (x64 vs ARM)

Practical guideline:

- Use **Python 3.10–3.12** for the best wheel coverage today.
- Always install inside a clean **venv**.

---

## Path A (Recommended): CadQuery → STEP

### Install (pip-only)

```bash
python -m venv .venv
./.venv/Scripts/python -m pip install --upgrade pip
./.venv/Scripts/pip install cadquery
```

> [!NOTE]
> On some platforms you may need `cadquery-ocp` / `cadquery-ocp-novtk` explicitly depending on your environment.

### Minimal export example

```python
import cadquery as cq

part = cq.Workplane("XY").box(10, 20, 30)
part.export("box.step")
```

If you are new to CadQuery, see:

- **[CadQuery basics](./cadquery-basics.md)**

### Assembly export (names/colors)

```python
import cadquery as cq
from cadquery import Assembly, Color

assy = Assembly()
assy.add(cq.Workplane("XY").box(10, 10, 10), name="base", color=Color(1, 0, 0))
assy.add(cq.Workplane("XY").circle(3).extrude(10).translate((0, 0, 5)), name="pin", color=Color(0, 0.6, 1))

assy.export("assy.step")
```

---

## Path B: build123d → STEP

### Install (pip-only)

```bash
python -m venv .venv
./.venv/Scripts/python -m pip install --upgrade pip
./.venv/Scripts/pip install build123d
```

### Minimal export example

```python
from build123d import Box, export_step

part = Box(10, 20, 30)
export_step(part, "box.step")
```

If you are new to build123d, see:

- **[build123d basics](./build123d-basics.md)**

---

## Validation (how to “test” the exported STEP)

### 1) Open in a reference CAD

Recommended quick checks:

- **FreeCAD**: open `.step` and confirm the solid displays correctly.
- Any target CAD system you actually need interoperability with.

### 2) Interoperability sanity checklist

- [ ] Units are correct (mm vs m)
- [ ] Solid is closed (no missing faces)
- [ ] Face orientations are consistent (no inverted normals)
- [ ] Colors / assembly structure are preserved (if required)

See also:
- **[Common Pitfalls](./common-pitfalls.md)** (units, orientations, colors, assemblies)
- **[Validation and CAx-IF](./validation-and-caxif.md)** (recommended practices and validation mindset)

### 3) Automated smoke tests (in this repo)

This repository includes small Python tests under `tests/python_step_export/`:

- a **pure-Python Part 21 generation** smoke test (always runnable with pip)
- optional **CadQuery / build123d** export tests (run only if those packages are installed)

Run them:

```bash
python -m pip install -r tests/python_step_export/requirements.txt
python -m pytest -q tests/python_step_export
```

Generated `.step` files are copied to:

- `tests/python_step_export/output/`

You can override the output folder:

```bash
STEP_EXPORT_OUTPUT_DIR=/some/path python -m pytest -q tests/python_step_export
```

If you want to generate **both CadQuery and build123d outputs** (and compare them), run:

```bash
python tests/python_step_export/generate_step_examples.py
```

For optional integration tests:

```bash
python -m pip install -r tests/python_step_export/requirements-occt.txt
STEP_EXPORT_INTEGRATION=1 python -m pytest -q tests/python_step_export
```

---

## Troubleshooting (pip-only)

### “No matching distribution found …”

Likely causes:

- Your Python version is not supported by available wheels (try **3.10–3.12**).
- Your architecture is unsupported (x64 vs ARM).

### Import errors / missing native libraries

Actions:

- Use a clean virtual environment.
- Prefer the “no VTK” variant if your environment has graphics/VTK conflicts.

### Lessons learned (from this repo)

#### 1) “My generated STEP is nowhere”

By default, pytest uses a temporary directory (`tmp_path`). In this repo we copy artifacts to a stable folder:

- `tests/python_step_export/output/`

If you need a different location:

```bash
STEP_EXPORT_OUTPUT_DIR=/some/path python -m pytest -q tests/python_step_export
```

#### 2) OCCT-based exporters can crash at interpreter shutdown

On some Windows setups, OCCT-based Python packages (e.g., CadQuery/OCP) may **segfault during interpreter exit**.
To keep artifact generation reliable, this repo’s generator script runs exporters in **isolated subprocesses**:

- `tests/python_step_export/generate_step_examples.py`

#### 2.1) CadQuery vs build123d dependency conflicts (`cadquery-ocp`)

CadQuery and build123d can require **different `cadquery-ocp` version ranges**. If you install both into the same Python environment, you may break one of them.

**Recommended practice**:

- Use **separate virtualenvs** for CadQuery and build123d when you need both.

#### 3) Windows path resolution can break VitePress builds

On Windows, drive-letter casing / realpath resolution can cause VitePress to miss page chunks and fail during render.
This repo sets:

- `.vitepress/config.mts`: `vite.resolve.preserveSymlinks = true`

#### 4) CadQuery face-level colors: use `exportStepMeta` + separate venv

Face-level colors require writing STEP with metadata (see **CadQuery basics**). In this repo we generate:

- `tests/python_step_export/output/cq_face_colored_top_red.step`

If your main Python environment is “dirty” (mixed CAD kernels), run CadQuery in an isolated venv.

---

## When you *should* generate Part 21 text yourself

Only consider text generation when:

- the geometry is extremely simple and fixed
- you are generating a small template file (educational / test vectors)
- you can validate the output across multiple importers

Start from:
- **[Minimal Export Template](./minimal-export.md)**

