from __future__ import annotations

from pathlib import Path
from typing import Callable

from steputils import p21


def _generate_minimal_part21_text() -> str:
    # Minimal, schema-light Part 21 file intended for smoke testing.
    # NOTE: This is not a full B-rep geometry example; it only validates the
    # physical file structure and that parsers accept the syntax.
    return "\n".join(
        [
            "ISO-10303-21;",
            "HEADER;",
            "FILE_DESCRIPTION(('pytest minimal'),'21;1');",
            "FILE_NAME('pytest.step','2026-01-20T00:00:00',('pytest'),(''), '','', '');",
            "FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));",
            "ENDSEC;",
            "DATA;",
            "#10 = APPLICATION_CONTEXT('managed model based 3d engineering');",
            "ENDSEC;",
            "END-ISO-10303-21;",
            "",
        ]
    )


def test_generate_part21_text_and_parse(
    tmp_path: Path,
    copy_artifact: Callable[[Path, str], Path],
) -> None:
    out = tmp_path / "minimal.step"
    out.write_text(_generate_minimal_part21_text(), encoding="utf-8", newline="\n")

    text = out.read_text(encoding="utf-8")
    assert text.startswith("ISO-10303-21;")
    assert "\nHEADER;\n" in text
    assert "\nDATA;\n" in text
    assert text.rstrip().endswith("END-ISO-10303-21;")

    # steputils parse smoke test
    with out.open("r", encoding="utf-8") as fp:
        sf = p21.load(fp)
    assert sf is not None

    # Copy to a stable folder for manual inspection
    copy_artifact(out, "minimal.step")

