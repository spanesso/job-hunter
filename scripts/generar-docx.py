#!/usr/bin/env python3
"""Genera el CV en Word (.docx) a partir del Markdown fuente de verdad.

El skill entrega el CV mejorado en Word; el usuario lo revisa, lo ajusta si
quiere y lo exporta él mismo a PDF (Archivo → Guardar como → PDF).

Uso:
    python generar-docx.py <cv.md> <salida.docx> [--design a|b|c] [--lang es]

Diseños (ver SKILL.md › "Los 3 diseños de CV"):
    a  ATS-First: una columna, negro, sin decoración.
    b  Balanced: una columna, títulos con color de acento.
    c  Portfolio: dos columnas (tabla) — nunca para portales ATS.

Markdown soportado: # h1, ## h2, ### h3, párrafos, viñetas (- / * / •),
**negrita**, *cursiva* y [texto](url). Requiere `python-docx`.
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

DESIGNS = {
    "a": {"font": "Arial", "size": 11, "accent": (0x00, 0x00, 0x00), "h1": 16},
    "b": {"font": "Calibri", "size": 11, "accent": (0x1F, 0x4E, 0x79), "h1": 20},
    "c": {"font": "Calibri", "size": 10.5, "accent": (0x1F, 0x4E, 0x79), "h1": 22},
}

INLINE_PATTERN = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\([^)]+\))")
BULLET_PATTERN = re.compile(r"^\s*([-*•])\s+(.*)$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def load_docx():
    try:
        import docx
    except ImportError:
        fail("Falta la dependencia 'python-docx'. Instala con: pip install python-docx")
    return docx


def parse_blocks(md_text: str) -> list[tuple[str, str]]:
    """Convierte el markdown en una lista plana de (tipo, texto)."""
    blocks, paragraph = [], []

    def flush() -> None:
        if paragraph:
            blocks.append(("p", " ".join(paragraph)))
            paragraph.clear()

    for raw in md_text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip() in {"---", "***"}:
            flush()
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        bullet = BULLET_PATTERN.match(line)
        if heading:
            flush()
            blocks.append((f"h{len(heading.group(1))}", heading.group(2).strip()))
        elif bullet:
            flush()
            blocks.append(("li", bullet.group(2).strip()))
        else:
            paragraph.append(line.strip())
    flush()
    return blocks


def add_hyperlink(paragraph, text: str, url: str, style: dict) -> None:
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    rel_id = paragraph.part.relate_to(
        url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), rel_id)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "%02X%02X%02X" % style["accent"])
    props.append(color)
    run.append(props)
    text_el = OxmlElement("w:t")
    text_el.text = text
    text_el.set(qn("xml:space"), "preserve")
    run.append(text_el)
    link.append(run)
    paragraph._p.append(link)


def add_inline(paragraph, text: str, style: dict) -> None:
    for part in INLINE_PATTERN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith("[") and "](" in part:
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part).groups()
            add_hyperlink(paragraph, label, url, style)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            paragraph.add_run(part[1:-1]).italic = True
        else:
            paragraph.add_run(part)


def write_blocks(container, blocks: list[tuple[str, str]], style: dict, docx) -> None:
    from docx.shared import Pt, RGBColor

    accent = RGBColor(*style["accent"])
    for kind, text in blocks:
        if kind == "h1":
            p = container.add_paragraph(style="Heading 1")
            run = p.add_run(re.sub(r"\*+", "", text))
            run.bold = True
            run.font.size = Pt(style["h1"])
            run.font.color.rgb = accent
        elif kind == "h2":
            p = container.add_paragraph(style="Heading 2")
            p.paragraph_format.space_before = Pt(12)
            run = p.add_run(re.sub(r"\*+", "", text).upper())
            run.bold = True
            run.font.size = Pt(style["size"] + 1)
            run.font.color.rgb = accent
            add_bottom_border(p, style)
        elif kind == "h3":
            p = container.add_paragraph(style="Heading 3")
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(re.sub(r"\*+", "", text))
            run.bold = True
        elif kind == "li":
            p = container.add_paragraph(style="List Bullet")
            add_inline(p, text, style)
        else:
            p = container.add_paragraph()
            add_inline(p, text, style)
        p.paragraph_format.space_after = Pt(3)


def add_bottom_border(paragraph, style: dict) -> None:
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "%02X%02X%02X" % style["accent"])
    borders.append(bottom)
    p_pr.append(borders)


def split_sidebar_main(blocks):
    """Separa las secciones h2 de sidebar (skills, educación…) del resto."""
    header, sidebar, main = [], [], []
    current = header
    for kind, text in blocks:
        if kind == "h2":
            current = sidebar if text.strip().lower() in SIDEBAR_HEADINGS else main
        current.append((kind, text))
    return header, sidebar, main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("entrada_md")
    parser.add_argument("salida_docx")
    parser.add_argument("--design", choices=sorted(DESIGNS), default="a")
    parser.add_argument("--lang", default="es")
    args = parser.parse_args()

    md_path = pathlib.Path(args.entrada_md)
    output_path = pathlib.Path(args.salida_docx)
    if not md_path.exists():
        fail(f"No existe el archivo markdown: {md_path}")
    if output_path.suffix.lower() != ".docx":
        fail("La salida debe terminar en .docx")

    docx = load_docx()
    from docx.shared import Mm, Pt, RGBColor

    style = DESIGNS[args.design]
    document = docx.Document()
    for section in document.sections:
        section.page_height, section.page_width = Mm(297), Mm(210)
        section.top_margin = section.bottom_margin = Mm(18)
        section.left_margin = section.right_margin = Mm(20)

    normal = document.styles["Normal"]
    normal.font.name = style["font"]
    normal.font.size = Pt(style["size"])
    for level in (1, 2, 3):
        heading = document.styles[f"Heading {level}"]
        heading.font.name = style["font"]
        heading.font.color.rgb = RGBColor(*style["accent"]) if level < 3 else RGBColor(0, 0, 0)
        heading.font.italic = False
        heading.font.size = Pt(style["size"] + (1 if level == 2 else 0))
    lang_tag = {"es": "es-CO", "en": "en-US"}.get(args.lang, args.lang)
    from docx.oxml.ns import qn
    r_pr = normal.element.get_or_add_rPr()
    lang_el = r_pr.find(qn("w:lang"))
    if lang_el is None:
        from docx.oxml import OxmlElement
        lang_el = OxmlElement("w:lang")
        r_pr.append(lang_el)
    lang_el.set(qn("w:val"), lang_tag)

    blocks = parse_blocks(md_path.read_text(encoding="utf-8"))
    if not blocks:
        fail("El markdown está vacío.")

    if args.design == "c":
        header, sidebar, main_blocks = split_sidebar_main(blocks)
        write_blocks(document, header, style, docx)
        table = document.add_table(rows=1, cols=2)
        table.autofit = False
        left, right = table.rows[0].cells
        left.width, right.width = Mm(58), Mm(112)
        left.paragraphs[0].text = ""
        right.paragraphs[0].text = ""
        write_blocks(left, sidebar, style, docx)
        write_blocks(right, main_blocks, style, docx)
    else:
        write_blocks(document, blocks, style, docx)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output_path))
    print(f"Word generado: {output_path}")


if __name__ == "__main__":
    main()
