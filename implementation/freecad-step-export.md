# Export STEP from Python using FreeCAD 1.0 (Python API)

FreeCAD can be used as a **reliable STEP exporter** because it sits directly on OpenCascade and provides a practical Python API.

This approach is **not pip-only** (it requires a FreeCAD installation), but if you can install FreeCAD it can be simpler than managing OCCT wheels in Python.

---

## When FreeCAD is a good choice

**Difficulty**: ★★☆ (Intermediate)  
**Frequency**: ★★☆ (Common)  
**Impact**: 🔴 High (Robust STEP export without Python wheel juggling)

- You can install desktop software (FreeCAD) on the machine
- You want a stable STEP exporter for batch jobs
- You want to avoid `cadquery-ocp` / OCCT wheel compatibility issues

---

## Recommended execution model: `FreeCADCmd`

Use FreeCAD’s headless command:

- Windows: `FreeCADCmd.exe`
- Linux/macOS: `FreeCADCmd`

In this repo, we provide a generator script:

- `tests/python_step_export/generate_freecad_step.py`

### Run it directly

```bash
FreeCADCmd tests/python_step_export/generate_freecad_step.py tests/python_step_export/output/box_freecad.step
```

### Or run via the repo’s generator (multi-export)

The repo generator will also try FreeCAD if it can find `FreeCADCmd`:

```bash
python tests/python_step_export/generate_step_examples.py
```

Configure the command explicitly (recommended on Windows):

```bash
FREECAD_CMD="C:\Program Files\FreeCAD 1.0\bin\FreeCADCmd.exe" python tests/python_step_export/generate_step_examples.py
```

---

## Smoke test (optional)

This repo includes an opt-in pytest integration test:

```bash
STEP_EXPORT_INTEGRATION=1 FREECAD_CMD=/path/to/FreeCADCmd python -m pytest -q tests/python_step_export -k freecad
```

Artifacts are copied to:

- `tests/python_step_export/output/box_freecad.step`

---

## Notes / pitfalls

- **Environment**: FreeCAD’s Python modules are normally available only inside FreeCAD’s bundled runtime, so prefer `FreeCADCmd` over trying to `import FreeCAD` from a normal venv.
- **CI**: Installing FreeCAD in CI is heavier than pip-only solutions; keep this path optional.

---

## See also

- **[Exporting STEP from Python (pip-only)](./python-step-export.md)** (CadQuery/build123d/OCP approach)
- **[Common Pitfalls](./common-pitfalls.md)**

