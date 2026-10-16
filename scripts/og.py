"""Imagen para compartir (WhatsApp, Facebook, X…): 1200×630 con el logo.

Crea assets/img/brand/og.jpg (castellano) y og-eu.jpg (euskera).
El logo va centrado para que también se vea bien en la miniatura cuadrada
que usa WhatsApp.

    python scripts/og.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "img" / "brand"
FONTS = Path("C:/Windows/Fonts")
INK, PAPER, BRASS = (22, 20, 18), (247, 242, 234), (214, 178, 120)
PRIDE = [(224, 72, 72), (239, 138, 60), (239, 199, 74), (90, 168, 96), (63, 127, 200), (122, 85, 179)]


def fuente(nombre, tam):
    try:
        return ImageFont.truetype(str(FONTS / nombre), tam)
    except OSError:
        return ImageFont.load_default()


def centra(d, y, texto, f, color, w=1200, espaciado=0):
    if espaciado:
        ancho = sum(d.textlength(c, font=f) for c in texto) + espaciado * (len(texto) - 1)
        x = (w - ancho) / 2
        for c in texto:
            d.text((x, y), c, font=f, fill=color)
            x += d.textlength(c, font=f) + espaciado
    else:
        d.text(((w - d.textlength(texto, font=f)) / 2, y), texto, font=f, fill=color)


def genera(lineas, salida):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), INK)
    # fondo: foto de cabecera muy oscurecida y desenfocada, como textura
    fondo = Image.open(ROOT / "assets" / "img" / "hero" / "home-1920.webp").convert("RGB")
    fondo = ImageOps.fit(fondo, (W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6))
    im = Image.blend(im, fondo, 0.22)
    # viñeta para centrar la mirada
    vin = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vin).ellipse((-200, -260, W + 200, H + 260), fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(120))
    im = Image.composite(im, Image.new("RGB", (W, H), (12, 11, 10)), vin)
    d = ImageDraw.Draw(im)
    # línea arcoíris arriba y abajo (Tod@s)
    franja = W // len(PRIDE)
    for i, c in enumerate(PRIDE):
        d.rectangle((i * franja, 0, (i + 1) * franja + 1, 6), fill=c)
        d.rectangle((i * franja, H - 6, (i + 1) * franja + 1, H), fill=c)
    # logo centrado
    logo = Image.open(BRAND / "logo-claro.png").convert("RGBA")
    logo.thumbnail((400, 300), Image.LANCZOS)
    top = (H - (logo.height + 30 + 95)) // 2
    im.paste(logo, ((W - logo.width) // 2, top), logo)
    d = ImageDraw.Draw(im)
    y = top + logo.height + 30
    centra(d, y, lineas[0], fuente("georgiai.ttf", 40), PAPER)
    centra(d, y + 60, lineas[1], fuente("seguisb.ttf", 21), BRASS, espaciado=3)
    im.save(salida, quality=88, optimize=True)


if __name__ == "__main__":
    genera(["Tu espacio de belleza y bienestar en Bilbao",
            "CORTE · COLOR · COLORACIÓN VEGETAL · ERREKALDE"], BRAND / "og.jpg")
    genera(["Zure edertasun- eta ongizate-gunea Bilbon",
            "ILE-MOZKETA · KOLOREA · LANDARE-KOLOREA · ERREKALDE"], BRAND / "og-eu.jpg")
    print("og.jpg y og-eu.jpg listas")
