"""Prepara los pares de antes y después.

Pares reales (de Cova): _fuentes/antes-despues/<id>-antes.jpg y <id>-despues.jpg
  · Los recorta a la misma proporción (4:5, vertical), iguala el tamaño y
    ajusta un poco el contraste para que las dos fotos se vean parejas.
Ejemplos de demostración: fotos de Unsplash (licencia libre) en _fuentes/unsplash/.

Crea assets/img/antes-despues/<id>-antes.webp y <id>-despues.webp

    python scripts/prepare_antes_despues.py
"""
import sys
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from content import ANTES_DESPUES  # noqa: E402

SRC = ROOT / "_fuentes" / "antes-despues"
UNS = ROOT / "_fuentes" / "unsplash"
OUT = ROOT / "assets" / "img" / "antes-despues"
W, H = 1080, 1350


def guarda(im, nombre):
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / f"{nombre}.webp", "WEBP", quality=82, method=6)


def unsplash(foto_id):
    UNS.mkdir(parents=True, exist_ok=True)
    ruta = UNS / f"{foto_id}.jpg"
    if not ruta.exists():
        url = f"https://images.unsplash.com/photo-{foto_id}?w=3000&q=90&fm=jpg"
        ruta.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read())
    return Image.open(ruta).convert("RGB")


def reales():
    for par in ANTES_DESPUES:
        fotos = []
        for lado in ("antes", "despues"):
            ruta = next((p for p in SRC.glob(f"{par['id']}-{lado}.*")), None)
            if not ruta:
                print(f"  falta {par['id']}-{lado}.jpg en _fuentes/antes-despues/")
                break
            im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
            im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, 0.4))
            im = ImageOps.autocontrast(im, cutoff=0.3, preserve_tone=True)
            fotos.append(im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=3)))
        else:
            guarda(fotos[0], f"{par['id']}-antes")
            guarda(fotos[1], f"{par['id']}-despues")
            print("  par real:", par["id"])


def ejemplos():
    # 1) Alisado: par real de antes y después publicado en Unsplash (maqueta de revista)
    im = unsplash("1785323451868-edd1e693daa6")            # 3000×3000
    antes = im.crop((395, 375, 1370, 1425))                 # página izquierda
    despues = im.crop((1655, 375, 2630, 1425))              # página derecha
    for lado, foto in (("antes", antes), ("despues", despues)):
        guarda(ImageOps.fit(foto, (W, int(W * foto.height / foto.width)), Image.LANCZOS), f"ejemplo-alisado-{lado}")

    # 2) Mechas: dos melenas fotografiadas juntas (oscura → iluminada)
    im = unsplash("1785456283212-338f5bc44d50")            # 3000×3000
    despues = im.crop((80, 120, 1580, 2995))
    antes = ImageOps.mirror(im.crop((1420, 120, 2920, 2995)))
    for lado, foto in (("antes", antes), ("despues", despues)):
        guarda(ImageOps.fit(foto, (W, H), Image.LANCZOS, centering=(0.5, 0.3)), f"ejemplo-mechas-{lado}")

    # 3) Brillo y color: la misma melena, apagada (simulado) y con brillo
    im = ImageOps.fit(unsplash("1730740505665-511513481bce"), (W, H), Image.LANCZOS, centering=(0.5, 0.45))
    despues = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.12)).enhance(1.06)
    antes = ImageEnhance.Color(im).enhance(0.35)
    antes = ImageEnhance.Contrast(antes).enhance(0.72)
    antes = ImageEnhance.Brightness(antes).enhance(0.9).filter(ImageFilter.GaussianBlur(1.2))
    guarda(antes, "ejemplo-brillo-antes")
    guarda(despues, "ejemplo-brillo-despues")
    print("  ejemplos listos")


if __name__ == "__main__":
    reales()
    ejemplos()
