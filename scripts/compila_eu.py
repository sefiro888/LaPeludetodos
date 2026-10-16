"""Une las traducciones al euskera en i18n/eu.json.

- i18n/eu/b*.txt: número de texto (según i18n/cadenas-bloques.json, lista fija) + traducción.
- i18n/eu/extra.tsv: textos añadidos después, como «texto en castellano<TAB>traducción».
«=» significa que el texto se queda igual (nombres propios, marcas, reseñas).

    python scripts/compila_eu.py
"""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "i18n"
cadenas = json.loads((DIR / "cadenas-bloques.json").read_text(encoding="utf-8"))
dic, vistos = {}, set()
for f in sorted((DIR / "eu").glob("b*.txt")):
    for n, linea in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip():
            continue
        num, _, tr = linea.partition("\t")
        i = int(num)
        assert i not in vistos, f"{f.name}:{n} número repetido {i}"
        vistos.add(i)
        dic[cadenas[i]] = cadenas[i] if tr.strip() == "=" else tr.strip()
faltan = [i for i in range(len(cadenas)) if i not in vistos]
extra = DIR / "eu" / "extra.tsv"
if extra.exists():
    for linea in extra.read_text(encoding="utf-8").splitlines():
        if "	" in linea and not linea.startswith("#"):
            es, eu = linea.split("	", 1)
            dic[es.strip()] = es.strip() if eu.strip() == "=" else eu.strip()
(DIR / "eu.json").write_text(json.dumps(dic, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
print(f"{len(dic)} traducciones · {len(faltan)} sin traducir {faltan[:20]}")
