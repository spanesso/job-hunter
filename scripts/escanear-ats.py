#!/usr/bin/env python3
"""Escanea listados abiertos de ATS públicos y filtra por palabras clave.

Uso:
    python3 escanear-ats.py empresas.txt --kw "ios|android|swift|kotlin"
    python3 escanear-ats.py empresas.txt --kw "data engineer" --excluir "intern|junior"

`empresas.txt`: una empresa por línea, formato `ats:slug` con ats en
{greenhouse, ashby, lever, recruitee}. Líneas vacías o con # se ignoran.

    greenhouse:wikimedia
    ashby:revenuecat
    lever:wisecode
    recruitee:guarana

Imprime: ATS | empresa | título | ubicación | URL. El filtro de
elegibilidad geográfica es manual (ver references/ats-formularios.md).
Solo usa endpoints públicos de listados; no envía nada ni requiere login.
"""
import argparse
import concurrent.futures as cf
import json
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (job-hunter skill)"}


def get_json(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except Exception:
        return None


def greenhouse(slug):
    d = get_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs") or {}
    return [(j["title"], j["location"]["name"], j["absolute_url"]) for j in d.get("jobs", [])]


def ashby(slug):
    d = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}") or {}
    return [(j["title"], j.get("location") or "", j.get("jobUrl") or "") for j in d.get("jobs", [])]


def lever(slug):
    d = get_json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    if not isinstance(d, list):
        return []
    return [(j["text"], j["categories"].get("location") or "", j["hostedUrl"]) for j in d]


def recruitee(slug):
    d = get_json(f"https://{slug}.recruitee.com/api/offers/") or {}
    return [(j["title"], j.get("location") or "", j.get("careers_url") or "") for j in d.get("offers", [])]


FETCHERS = {"greenhouse": greenhouse, "ashby": ashby, "lever": lever, "recruitee": recruitee}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("empresas", help="archivo con líneas ats:slug")
    ap.add_argument("--kw", required=True, help="regex (sin distinguir mayúsculas) a buscar en el título")
    ap.add_argument("--excluir", default="", help="regex de títulos a excluir")
    args = ap.parse_args()

    inc = re.compile(args.kw, re.I)
    exc = re.compile(args.excluir, re.I) if args.excluir else None

    tareas = []
    with open(args.empresas, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or ":" not in linea:
                continue
            ats, slug = linea.split(":", 1)
            if ats in FETCHERS:
                tareas.append((ats, slug.strip()))
            else:
                print(f"ATS no soportado, se ignora: {linea}", file=sys.stderr)

    def run(t):
        ats, slug = t
        out = []
        for titulo, ubic, url in FETCHERS[ats](slug):
            if inc.search(titulo) and not (exc and exc.search(titulo)):
                out.append((ats, slug, titulo, ubic, url))
        return out

    n = 0
    with cf.ThreadPoolExecutor(20) as ex:
        for res in ex.map(run, tareas):
            for fila in res:
                print(" | ".join(fila))
                n += 1
    print(f"{n} vacantes coinciden en {len(tareas)} empresas", file=sys.stderr)


if __name__ == "__main__":
    main()
