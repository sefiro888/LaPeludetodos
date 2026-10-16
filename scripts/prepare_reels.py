"""Descarga la portada de cada reel de REELS (scripts/content.py).

Crea assets/img/reels/<código>.webp (vertical). Si además tienes el vídeo,
guárdalo como assets/video/<código>.mp4 y la web lo reproducirá en bucle.

    python scripts/prepare_reels.py
"""
import io
import sys
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from content import REELS  # noqa: E402

OUT = ROOT / "assets" / "img" / "reels"
OUT.mkdir(parents=True, exist_ok=True)
for codigo, titulo, _ in REELS:
    url = f"https://www.instagram.com/p/{codigo}/media/?size=l"
    datos = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    im = ImageOps.fit(im, (720, 1280), Image.LANCZOS, centering=(0.5, 0.45))
    im.save(OUT / f"{codigo}.webp", "WEBP", quality=80, method=6)
    print(codigo, titulo)
