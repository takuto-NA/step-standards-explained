from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    marker = Path(__file__).resolve().parent / "output" / "freecad_cmd_debug.txt"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("ran\nargv=" + repr(sys.argv) + "\n", encoding="utf-8")
    print("[debug] FreeCADCmd executed Python script")
    print(f"[debug] wrote: {marker}")
    return 0


raise SystemExit(main())

