"""Traducción de la web a euskera.

Funciona sobre el HTML ya generado en castellano: cada texto visible, cada
atributo legible (alt, aria-label, placeholder, title, descripciones) y cada
mensaje de WhatsApp se busca en i18n/eu.json y se sustituye por su traducción.
Lo que no esté traducido se queda en castellano y se lista en
i18n/pendientes-eu.txt para completarlo.

    python build.py                      # genera también /eu/
    python scripts/i18n.py --extraer     # lista todos los textos (i18n/cadenas.json)
"""
import html as H
import json
import re
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "i18n"
ATRIBUTOS = ("alt", "aria-label", "placeholder", "title", "content", "value")
META_TRADUCIBLE = re.compile(r'<meta (?:name="description"|property="og:(?:title|description|site_name)")')
_texto = re.compile(r">([^<]+)<")
_bloques_omitidos = re.compile(r"(<script\b.*?</script>|<style\b.*?</style>)", re.S)


def _es_traducible(t):
    t = t.strip()
    return bool(t) and bool(re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{2,}", t))


def _norm(t):
    return re.sub(r"\s+", " ", H.unescape(t)).strip()


def cadenas(html):
    """Devuelve el conjunto de textos traducibles de una página."""
    out = set()
    partes = _bloques_omitidos.split(html)
    for parte in partes:
        if parte.startswith("<script") or parte.startswith("<style"):
            continue
        for m in _texto.finditer(parte):
            if _es_traducible(m.group(1)):
                out.add(_norm(m.group(1)))
        for etiqueta in re.finditer(r"<[a-zA-Z][^>]*>", parte):
            tag = etiqueta.group(0)
            for at in ATRIBUTOS:
                for v in re.findall(rf'\s{at}="([^"]*)"', tag):
                    if at == "content" and not META_TRADUCIBLE.match(tag):
                        continue
                    if at == "value" and not tag.startswith("<option"):
                        continue
                    if _es_traducible(v):
                        out.add(_norm(v))
            for msg in re.findall(r"wa\.me/\d+\?text=([^\"&]+)", tag):
                out.add(_norm(unquote(msg)))
    return out


class Traductor:
    def __init__(self, lang="eu"):
        ruta = DIR / f"{lang}.json"
        self.dic = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
        self.faltan = set()

    def t(self, texto):
        clave = _norm(texto)
        if clave in self.dic:
            return self.dic[clave]
        if _es_traducible(clave):
            self.faltan.add(clave)
        return None

    def _sub_texto(self, m):
        crudo = m.group(1)
        if not _es_traducible(crudo):
            return m.group(0)
        tr = self.t(crudo)
        if tr is None:
            return m.group(0)
        ini = re.match(r"\s*", crudo).group(0)
        fin = re.search(r"\s*$", crudo).group(0)
        return ">" + ini + H.escape(tr, quote=False) + fin + "<"

    def _sub_etiqueta(self, m):
        tag = m.group(0)

        def at_sub(ma):
            at, v = ma.group(1), ma.group(2)
            if at == "content" and not META_TRADUCIBLE.match(tag):
                return ma.group(0)
            if at == "value" and not tag.startswith("<option"):
                return ma.group(0)
            if not _es_traducible(v):
                return ma.group(0)
            tr = self.t(v)
            return ma.group(0) if tr is None else f' {at}="{H.escape(tr)}"'
        tag = re.sub(r'\s(alt|aria-label|placeholder|title|content|value)="([^"]*)"', at_sub, tag)

        def wa_sub(mw):
            tr = self.t(unquote(mw.group(1)))
            return mw.group(0) if tr is None else mw.group(0).replace(mw.group(1), quote(tr))
        return re.sub(r"wa\.me/\d+\?text=([^\"&]+)", wa_sub, tag)

    def traduce(self, html):
        partes = _bloques_omitidos.split(html)
        res = []
        for parte in partes:
            if parte.startswith("<script") or parte.startswith("<style"):
                res.append(parte)
                continue
            parte = re.sub(r"<[a-zA-Z][^>]*>", self._sub_etiqueta, parte)
            parte = _texto.sub(self._sub_texto, parte)
            res.append(parte)
        return "".join(res)

    def guarda_pendientes(self, lang="eu"):
        ruta = DIR / f"pendientes-{lang}.txt"
        ruta.write_text("\n".join(sorted(self.faltan)), encoding="utf-8")
        return len(self.faltan)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    if "--extraer" in sys.argv:
        import build
        build.genera()
        todas = set()
        for _, h in build.PAGINAS:
            todas |= cadenas(h)
        DIR.mkdir(exist_ok=True)
        (DIR / "cadenas.json").write_text(json.dumps(sorted(todas), ensure_ascii=False, indent=1), encoding="utf-8")
        print(len(todas), "cadenas")
