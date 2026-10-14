"""Comprueba enlaces internos, anclas e imágenes de todas las páginas.

    python scripts/check.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errores = 0
paginas = sorted(ROOT.glob("*.html"))
for p in paginas:
    html = p.read_text(encoding="utf-8")
    ids = set(re.findall(r'id="([^"]+)"', html))
    for ref in re.findall(r'(?:href|src|data-lb|data-img|srcset)="([^"]+)"', html):
        if ref.startswith(("http", "tel:", "mailto:", "data:")):
            continue
        ruta, _, ancla = ref.partition("#")
        ruta = ruta.split("?")[0]
        if ruta and not (ROOT / ruta).exists():
            print(f"{p.name}: falta {ruta}"); errores += 1
        if ancla and not ruta and ancla not in ids:
            print(f"{p.name}: ancla rota #{ancla}"); errores += 1
    for url in re.findall(r"url\('([^']+)'\)", html):
        if not (ROOT / url).exists():
            print(f"{p.name}: falta {url}"); errores += 1
print(f"{len(paginas)} páginas revisadas · {errores} errores")
