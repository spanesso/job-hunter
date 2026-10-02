#!/usr/bin/env python3
"""Genera un PDF a partir de un CV o cover letter en Markdown + un template HTML.

Uso:
    python generar-pdf.py <entrada.md> <template.html> <salida.pdf> [--lang es] [--title "Nombre - Cargo"]

El template debe contener el placeholder {{content}} (diseños A y B, o
cover letter), o {{sidebar}} y {{main}} (diseño C). Requiere `markdown`
y `weasyprint` instalados (`pip install markdown weasyprint`).
"""
import argparse
import pathlib
import re
import sys

SIDEBAR_HEADINGS = {
    "habilidades técnicas", "skills", "technical skills",
    "contacto", "contact",
    "educación", "education",
    "certificaciones", "certifications",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def markdown_to_html(md_text: str) -> str:
    try:
        import markdown as md_lib
    except ImportError:
        fail("Falta la dependencia 'markdown'. Instala con: pip install markdown")
    return md_lib.markdown(md_text, extensions=["extra", "sane_lists"])


def split_sidebar_main(html: str) -> tuple[str, str]:
    """Divide el HTML renderizado en bloques de sidebar vs. main según el
    heading h2 que abre cada sección (convención de estructura-cv.md)."""
    sections = re.split(r"(?=<h2[ >])", html)
    sidebar_parts, main_parts = [], []
    for section in sections:
        if not section.strip():
            continue
        heading_match = re.search(r"<h2[^>]*>(.*?)</h2>", section, re.IGNORECASE | re.DOTALL)
        heading_text = re.sub(r"<[^>]+>", "", heading_match.group(1)).strip().lower() if heading_match else ""
        if heading_text in SIDEBAR_HEADINGS or not main_parts and not heading_match:
            sidebar_parts.append(section)
        else:
            main_parts.append(section)
    return "".join(sidebar_parts), "".join(main_parts)


def render_pdf(html: str, output_path: pathlib.Path) -> None:
    try:
        from weasyprint import HTML
    except ImportError:
        fail(
            "Falta la dependencia 'weasyprint'. Instala con: pip install weasyprint\n"
            "Alternativa: usa wkhtmltopdf manualmente sobre el HTML intermedio."
        )
    HTML(string=html).write_pdf(str(output_path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada_md")
    parser.add_argument("template_html")
    parser.add_argument("salida_pdf")
    parser.add_argument("--lang", default="es")
    parser.add_argument("--title", default="CV")
    args = parser.parse_args()

    md_path = pathlib.Path(args.entrada_md)
    template_path = pathlib.Path(args.template_html)
    output_path = pathlib.Path(args.salida_pdf)

    if not md_path.exists():
        fail(f"No existe el archivo markdown: {md_path}")
    if not template_path.exists():
        fail(f"No existe el template: {template_path}")

    md_text = md_path.read_text(encoding="utf-8")
    template_text = template_path.read_text(encoding="utf-8")
    content_html = markdown_to_html(md_text)

    rendered = template_text.replace("{{lang}}", args.lang).replace("{{title}}", args.title)

    if "{{sidebar}}" in rendered and "{{main}}" in rendered:
        sidebar_html, main_html = split_sidebar_main(content_html)
        rendered = rendered.replace("{{sidebar}}", sidebar_html).replace("{{main}}", main_html)
    else:
        rendered = rendered.replace("{{content}}", content_html)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    render_pdf(rendered, output_path)
    print(f"PDF generado: {output_path}")


if __name__ == "__main__":
    main()
