# STEP export tests (Python, pip-only)

This repo is primarily a documentation site, but we keep a few **Python smoke tests** here to verify that:

- we can generate a **valid Part 21 STEP** file via pure-Python text output, and
- (optionally) we can export STEP via **CadQuery/build123d (OpenCASCADE/OCP)** if installed.

## Quick start (pure-Python test only)

```bash
python -m pip install -r tests/python_step_export/requirements.txt
python -m pytest -q tests/python_step_export
```

## Optional: real geometry export tests (CadQuery / build123d)

These require native wheels and may be environment-dependent. They are **disabled by default**
because OCCT-based packages can crash the interpreter on some setups.

```bash
python -m pip install -r tests/python_step_export/requirements-occt.txt
STEP_EXPORT_INTEGRATION=1 python -m pytest -q tests/python_step_export
```

## What the tests check

- **Text generation test**:
  - output file starts with `ISO-10303-21;`
  - has `HEADER;` and `DATA;` sections
  - ends with `END-ISO-10303-21;`
  - is parseable as a Part 21 physical file
  - copied to `tests/python_step_export/output/minimal.step`

- **CadQuery/build123d integration tests** (if installed):
  - exporting a simple box produces a `.step` file
  - output contains the Part 21 wrapper and basic structure
  - copied to `tests/python_step_export/output/box_cadquery.step` and/or `box_build123d.step`

## Where to find generated files

After running tests, look under:

- `tests/python_step_export/output/`

You can override the output folder:

```bash
STEP_EXPORT_OUTPUT_DIR=/some/path python -m pytest -q tests/python_step_export
```

## Generate both CadQuery and build123d outputs (recommended)

If you want **multiple exporters** to run and leave artifacts you can inspect, use the generator script:

```bash
python tests/python_step_export/generate_step_examples.py
```

It writes (depending on what is installed):

- `tests/python_step_export/output/minimal.step`
- `tests/python_step_export/output/box_cadquery.step`
- `tests/python_step_export/output/box_build123d.step`
- `tests/python_step_export/output/box_freecad.step` (if FreeCAD is installed)

## Optional: export via FreeCAD (external install)

If you have FreeCAD installed, you can export STEP using its Python API via `FreeCADCmd`.

### One-off generation

Run the FreeCAD generator script directly:

```bash
FreeCADCmd tests/python_step_export/generate_freecad_step.py tests/python_step_export/output/box_freecad.step
```

Or run the repo generator and let it pick FreeCAD up (recommended if you also want CadQuery/build123d artifacts):

```bash
python tests/python_step_export/generate_step_examples.py
```

If `FreeCADCmd` is not on your PATH, set it explicitly:

- Windows PowerShell:

```powershell
$env:FREECAD_CMD="C:\Program Files\FreeCAD 1.0\bin\FreeCADCmd.exe"; python tests/python_step_export/generate_step_examples.py
```

- bash:

```bash
FREECAD_CMD="/path/to/FreeCADCmd" python tests/python_step_export/generate_step_examples.py
```

### pytest integration test

FreeCAD export is also covered by an opt-in test:

```bash
STEP_EXPORT_INTEGRATION=1 FREECAD_CMD=/path/to/FreeCADCmd python -m pytest -q tests/python_step_export -k freecad
```

## Generate a face-colored STEP (CadQuery)

This repo includes a script that exports a box where only the **top face is red**:

```bash
python tests/python_step_export/generate_cadquery_face_colored_step.py
```

Output:

- `tests/python_step_export/output/cq_face_colored_top_red.step`

> [!NOTE]
> If your environment has conflicting OCCT stacks (CadQuery/build123d), run CadQuery in a separate venv.

## Notes / Lessons learned

- **Artifacts location**: pytest itself writes to a temp dir, so we copy `.step` files into `tests/python_step_export/output/` for easy inspection.
- **OCCT shutdown crashes**: some environments may crash on interpreter shutdown when importing OCCT-based packages. The generator uses isolated subprocesses to keep outputs reliable.
- **Integration tests are opt-in**: set `STEP_EXPORT_INTEGRATION=1` to run CadQuery/build123d export tests (otherwise they are skipped).

