"""Descarga y prepara las cabeceras de banco de imágenes (Unsplash) para los
servicios de peluquería y estilismo.

Las fotos de Unsplash tienen licencia Unsplash: uso comercial gratuito,
sin necesidad de pedir permiso ni de citar al autor (aunque se agradece).
https://unsplash.com/license

Crea assets/img/stock/<clave>.webp, <clave>-1920.webp y <clave>-m.webp.
Qué cabeceras usa la web se elige en scripts/content.py → CABECERAS_PELU.

    python scripts/prepare_stock.py
"""
import io
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "stock"
FUENTE = ROOT / "_fuentes" / "unsplash"

# clave de cabecera -> (id de la foto en Unsplash, centro del recorte móvil 0-1, descripción)
STOCK = {
    "asesoria": ("1562322140-8baeececf3df", 0.62, "Estilista peinando a una clienta en el salón"),
    "cortes": ("1593702275687-f8b402bf1fb5", 0.55, "Peluquero haciendo un degradado con máquina"),
    "coloracion": ("1707979577466-2d6109c68a45", 0.55, "Dos coloristas aplicando tinte con guantes"),
    "mechas": ("1712213396688-c6f2d536671f", 0.5, "Mechas con papel de aluminio y pincel"),
    "fantasia": ("1634033505111-152bb89cce19", 0.5, "Melena en morado y violeta"),
    "vegetal": ("1603122612817-2fe0e0631a93", 0.5, "Polvo de henna en un cuenco"),
    "alisados": ("1780504542350-5078d4080081", 0.6, "Alisado con plancha sobre melena oscura"),
    "rizos": ("1579119159780-51419861f69f", 0.5, "Melena de rizos definidos"),
    "peinados": ("1672788725446-c303ec2b318e", 0.55, "Recogido de novia con tocado"),
    "tratamientos": ("1717160675643-53a7a2ebaa9f", 0.6, "Tratamiento en el lavacabezas"),
}


def descarga(foto_id):
    FUENTE.mkdir(parents=True, exist_ok=True)
    ruta = FUENTE / f"{foto_id}.jpg"
    if not ruta.exists():
        url = f"https://images.unsplash.com/photo-{foto_id}?w=3000&q=88&fm=jpg"
        datos = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
        ruta.write_bytes(datos)
    return Image.open(ruta).convert("RGB")


def guarda(im, ruta, q=80):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    im.save(ruta, "WEBP", quality=q, method=6)


if __name__ == "__main__":
    for clave, (foto_id, cx, _) in STOCK.items():
        im = descarga(foto_id)
        # tono algo más cálido y sobrio para casar con la paleta de la web
        im = ImageEnhance.Color(im).enhance(0.92)
        pan = ImageOps.fit(im, (2400, min(1350, int(im.height * 2400 / im.width))), Image.LANCZOS, centering=(0.5, 0.45))
        guarda(pan, OUT / f"{clave}.webp")
        p19 = pan.copy(); p19.thumbnail((1920, 1920), Image.LANCZOS)
        guarda(p19, OUT / f"{clave}-1920.webp")
        movil = ImageOps.fit(im, (1080, 1440), Image.LANCZOS, centering=(cx, 0.45))
        guarda(movil, OUT / f"{clave}-m.webp")
        print(clave, im.size)
