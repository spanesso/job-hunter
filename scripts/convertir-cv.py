#!/usr/bin/env python3
"""Convierte el CV original del usuario (PDF) a Markdown con MarkItDown.

El skill NUNCA abre el PDF directamente: primero lo transforma a Markdown
con https://github.com/microsoft/markitdown y trabaja solo sobre ese .md.

Uso:
    python convertir-cv.py <cv.pdf> <salida.md>

Requiere `markitdown` con soporte PDF (`pip install 'markitdown[pdf,docx]'`).
"""
import pathlib
import sys

MIN_TEXT_CHARS = 200


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 3:
        fail("Uso: python convertir-cv.py <cv.pdf> <salida.md>")

    input_path = pathlib.Path(sys.argv[1]).expanduser()
    output_path = pathlib.Path(sys.argv[2]).expanduser()

    if not input_path.exists():
        fail(f"No existe el archivo: {input_path}")
    if input_path.suffix.lower() != ".pdf":
        fail(f"Se esperaba un PDF y se recibió '{input_path.suffix}'. Pide al usuario el CV en PDF.")

    try:
        from markitdown import MarkItDown
    except ImportError:
        fail("Falta la dependencia 'markitdown'. Instala con: pip install 'markitdown[pdf,docx]'")

    result = MarkItDown(enable_plugins=False).convert(str(input_path))
    text = (result.text_content or "").strip()

    if len(text) < MIN_TEXT_CHARS:
        fail(
            f"MarkItDown extrajo muy poco texto ({len(text)} caracteres). "
            "El PDF probablemente es una imagen escaneada: un ATS tampoco podrá leerlo. "
            "Pide al usuario un PDF exportado desde Word/Google Docs (texto seleccionable)."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text + "\n", encoding="utf-8")
    print(f"Markdown generado: {output_path} ({len(text)} caracteres)")


if __name__ == "__main__":
    main()
