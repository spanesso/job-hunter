#!/usr/bin/env python3
"""Test de parseo ATS de 2 minutos, automatizado.

Extrae el texto plano de un PDF de CV (como lo haría un ATS) y reporta
señales de un parseo roto: orden de secciones, bloques mezclados,
caracteres rotos. No sustituye la revisión humana, pero detecta los
casos obvios antes de enviar el CV a un portal.

Uso:
    python test-parseo.py <cv.pdf>
"""
import re
import sys

EXPECTED_SECTION_ORDER = [
    ("resumen profesional", "professional summary"),
    ("habilidades técnicas", "technical skills"),
    ("experiencia profesional", "professional experience"),
    ("proyectos destacados", "projects"),
    ("educación", "education"),
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def extract_text(pdf_path: str) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        fail("Falta la dependencia 'pypdf'. Instala con: pip install pypdf")
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def check_order(text_lower: str) -> list[str]:
    warnings = []
    positions = []
    for es_name, en_name in EXPECTED_SECTION_ORDER:
        pos = text_lower.find(es_name)
        if pos == -1:
            pos = text_lower.find(en_name)
        positions.append(pos)

    found = [(i, p) for i, p in enumerate(positions) if p != -1]
    for (i1, p1), (i2, p2) in zip(found, found[1:]):
        if p1 > p2:
            warnings.append(
                f"Orden sospechoso: la sección #{i1} aparece después de la #{i2} en el texto extraído."
            )
    missing = [EXPECTED_SECTION_ORDER[i][0] for i, p in enumerate(positions) if p == -1]
    if missing:
        warnings.append(f"No se encontraron estas secciones esperadas: {', '.join(missing)}")
    return warnings


def check_garbage(text: str) -> list[str]:
    warnings = []
    broken_char_ratio = len(re.findall(r"[^\x00-\x7FÀ-ſ\s]", text)) / max(len(text), 1)
    if broken_char_ratio > 0.02:
        warnings.append(
            f"Alto ratio de caracteres no estándar ({broken_char_ratio:.1%}) — "
            "posible fuente mal embebida o PDF escaneado."
        )
    if len(text.strip()) < 200:
        warnings.append(
            "Muy poco texto extraído (<200 caracteres) — el PDF puede ser una imagen escaneada "
            "en vez de texto seleccionable."
        )
    return warnings


def main() -> None:
    if len(sys.argv) != 2:
        fail("Uso: python test-parseo.py <cv.pdf>")
    pdf_path = sys.argv[1]
    text = extract_text(pdf_path)
    text_lower = text.lower()

    warnings = check_order(text_lower) + check_garbage(text)

    print(f"== Test de parseo ATS: {pdf_path} ==")
    if not warnings:
        print("[OK] No se detectaron problemas obvios de parseo.")
    else:
        for w in warnings:
            print(f"[AVISO] {w}")
        print(
            "\nRevisa el template/markdown antes de enviar este CV a un portal. "
            "Ver references/ats-2026.md para los 6 breakers comunes."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
