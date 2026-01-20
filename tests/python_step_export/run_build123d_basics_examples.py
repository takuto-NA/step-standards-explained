from __future__ import annotations

import os
from pathlib import Path


def out_dir() -> Path:
    override = os.environ.get("STEP_EXPORT_OUTPUT_DIR")
    d = Path(override) if override else Path(__file__).resolve().parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def main() -> int:
    try:
        from build123d import Box, export_step  # type: ignore
    except Exception as e:
        print(f"[build123d] not installed or failed to import: {e}")
        print("[build123d] skip generating examples.")
        return 0

    d = out_dir()

    # Minimal example: box → STEP (matches implementation/build123d-basics.md)
    part = Box(10, 20, 30)
    export_step(part, str(d / "b3d_basics_box.step"))

    print(f"build123d basics examples exported to: {d}")

    # Some OCCT-based environments crash during interpreter shutdown.
    os._exit(0)


if __name__ == "__main__":
    raise SystemExit(main())

