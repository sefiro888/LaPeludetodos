"""Prepara logo, fotos y cabeceras a partir del material original.

Lee:  _fuentes/instagram/<codigo>.jpg  (fotos publicadas en @lapeludet2)
      Logo de peluquería con fondo transparente.png
Crea: assets/img/brand/*, assets/img/fotos/*.webp, assets/img/hero/*.webp

Retoque: recorte de la marca «Galaxy Z Fold4» (franja inferior), contraste y
color suaves, enfoque (unsharp mask) y escalado Lanczos cuando hace falta.

    python scripts/prepare_assets.py
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_fuentes" / "instagram"
OUT = ROOT / "assets" / "img"

# nombre -> (código de Instagram, recortar franja inferior con marca de agua)
FOTOS = {
    # trabajos de color
    "color-cobre-melena": ("DJSK0a7qSaF", True),
    "color-cobre-largo": ("DHqnxzTBrYo", True),
    "color-cobre-espalda": ("DIBJ9oAgMGE", False),
    "color-burdeos-liso": ("DPx82o4jAvI", False),
    "color-violeta-liso": ("DKcPODcs1BX", False),
    "color-negro-liso": ("DJZZZcuh2B2", False),
    "color-dorado": ("DJbPRPFo38B", False),
    "color-castano-claro": ("DJd1FfKtBk_", False),
    "color-rojo-mechas": ("DRSr4DUgcAu", False),
    "color-antes-despues": ("DRCYhNYiedl", False),
    "color-cobre-salon": ("DRkv-mYjZl8", True),
    "color-castano-oscuro": ("DOdXVaYALK6", False),
    # mechas y balayage
    "mechas-balayage-ondas": ("DPwpMXGgC64", False),
    "mechas-balayage-logo": ("DJXWso-PF-U", True),
    "mechas-degradado-logo": ("DIQ8IujIn59", True),
    "mechas-ombre-cobre": ("DQ6espWgSDw", False),
    "mechas-ombre-cobre-2": ("DQU6g3Yj5kC", False),
    "mechas-rubias": ("DQm-Bcpkp2M", False),
    "mechas-capas": ("DKB50fCuhNu", False),
    "mechas-clienta": ("DKPIdJXoBwQ", False),
    "mechas-reflejos": ("DOd8kawCRHu", False),
    "mechas-largo-logo": ("DJkRpUTtCTK", True),
    # fantasía
    "fantasia-azul": ("DH-kXO8v5Hs", True),
    "fantasia-rosa-lila": ("DKjwTMbhOZz", False),
    "fantasia-rojo-negro": ("DP6PhSiAoBq", True),
    "fantasia-rosa-ondas": ("DQq2eeOD85d", False),
    "fantasia-trenza-azul": ("DKZAvcypGcw", False),
    # vegetal
    "vegetal-rizo-cobre": ("DKIILzxMKOP", False),
    "vegetal-largo": ("DP4R-4LjzC4", True),
    "vegetal-castano": ("DIKAN-wpP0u", False),
    "vegetal-bob": ("DQbyy1-DxrB", False),
    "vegetal-productos": ("DJ9YKjAPRqd", False),
    "vegetal-cosmetica": ("DQ88RNGjxgx", False),
    "vegetal-antes": ("DRmVsnIlY0l", False),
    # cortes
    "corte-bob-rubio": ("DQ_rIqLj7CG", False),
    "corte-bob-cobre": ("DOYQfs1jG5N", False),
    "corte-bob-cobre-2": ("DRPZjTjDNsN", False),
    "corte-bob-castano": ("DSFzgtxjlM4", False),
    "corte-corto-negro": ("DKiCAP2tqi4", False),
    "corte-pixie-cobre": ("DSIDDN5CFlA", False),
    "corte-chico-cova": ("DRNd8mQlYz-", False),
    "corte-capas-mechas": ("DKMrqcVvVXp", False),
    "corte-ninos": ("DQoxnqVjdAO", False),
    "corte-media-melena": ("DRVTT7bCgQz", False),
    # liso, rizo, peinados
    "liso-largo": ("DJ_s1QaxCP_", False),
    "liso-espejo": ("DP02Mzaj3rf", False),
    "rizo-definido": ("DKR0kitOfYR", False),
    "rizo-corto": ("DRK3pyVCayc", False),
    "rizo-mechas": ("DH5YfPypo1x", True),
    "rizo-lavado": ("DHx_2JWsRwU", False),
    "recogido-rizos": ("DKfdTUTMZ4X", False),
    "trenza-boho": ("DSNYZZwkb3X", False),
    # salud capilar
    "raiz-cana": ("DKsaxTfAd8g", False),
    "raiz-cana-2": ("DMHkDPbIy80", False),
    "diagnostico-microcamara": ("DRiES-AE0jr", False),
    # cova y salón
    "cova-clienta": ("DQFKJnpEXGi", False),
    "cova-amiga": ("DRF7kNTiYc4", True),
    "cova-grupo": ("DSLX6UgCDIa", True),
    "cova-trabajando": ("DQcd9w_kW7Y", False),
    # estética
    "solarium-cabina": ("DMaSBAYMcKs", False),
    "presoterapia-piernas": ("DHf6gO_Pi9f", False),
    "presoterapia-botas": ("DKmVq8KMUMO", False),
}

# Recortes manuales (izq, arriba, der, abajo) en proporción 0-1
RECORTES = {
    "presoterapia-piernas": (0.0, 0.0, 0.78, 1.0),   # fuera sello del logo
    "presoterapia-botas": (0.30, 0.0, 0.86, 1.0),    # fuera texto y sello
    "cova-grupo": (0.0, 0.0, 1.0, 0.94),
    "cova-amiga": (0.0, 0.0, 1.0, 0.94),
}

# Cabeceras panorámicas: tríptico de fotos reales (3 × 1080 = 3240 px)
HEROES = {
    "home": ["mechas-degradado-logo", "mechas-balayage-ondas", "color-cobre-melena"],
    "servicios": ["color-burdeos-liso", "rizo-corto", "mechas-balayage-logo"],
    "asesoria": ["corte-bob-castano", "mechas-capas", "corte-pixie-cobre"],
    "cortes": ["corte-bob-rubio", "corte-chico-cova", "corte-bob-cobre"],
    "coloracion": ["color-cobre-salon", "color-violeta-liso", "color-dorado"],
    "mechas": ["mechas-balayage-ondas", "mechas-largo-logo", "mechas-rubias"],
    "fantasia": ["fantasia-rosa-lila", "fantasia-rojo-negro", "fantasia-rosa-ondas"],
    "vegetal": ["vegetal-productos", "vegetal-rizo-cobre", "vegetal-castano"],
    "alisados": ["liso-largo", "color-negro-liso", "mechas-ombre-cobre-2"],
    "rizos": ["rizo-definido", "rizo-lavado", "rizo-corto"],
    "peinados": ["recogido-rizos", "trenza-boho", "fantasia-trenza-azul"],
    "tratamientos": ["vegetal-cosmetica", "color-castano-claro", "color-negro-liso"],
    "diagnostico": ["vegetal-productos", "raiz-cana-2", "raiz-cana"],
    "laser-capilar": ["raiz-cana", "liso-espejo", "raiz-cana-2"],
    "sobre-cova": ["cova-clienta", "corte-chico-cova", "cova-amiga"],
    "espacio": ["cova-grupo", "fantasia-azul", "corte-chico-cova"],
    "galeria": ["fantasia-rosa-ondas", "mechas-ombre-cobre", "vegetal-largo"],
    "opiniones": ["cova-clienta", "mechas-clienta", "corte-pixie-cobre"],
    "ubicacion": ["mechas-degradado-logo", "vegetal-productos", "mechas-largo-logo"],
    "contacto": ["color-cobre-melena", "mechas-balayage-logo", "color-burdeos-liso"],
}
# Cabeceras de una sola imagen apaisada (se amplía y se enfoca)
HEROES_SIMPLES = {
    "presoterapia": "presoterapia-piernas",
    "solarium": "solarium-cabina",
    "depilacion": "presoterapia-piernas",
}


def retoca(im: Image.Image) -> Image.Image:
    im = ImageOps.autocontrast(im, cutoff=0.4, preserve_tone=True)
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=3))


def carga(nombre: str) -> Image.Image:
    codigo, marca = FOTOS[nombre]
    im = ImageOps.exif_transpose(Image.open(SRC / f"{codigo}.jpg")).convert("RGB")
    w, h = im.size
    if nombre in RECORTES:
        l, t, r, b = RECORTES[nombre]
        im = im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
    elif marca:
        im = im.crop((0, 0, w, int(h * 0.93)))
    return im


def guarda(im, ruta, q=82):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    im.save(ruta, "WEBP", quality=q, method=6)


def fotos():
    for nombre in FOTOS:
        im = retoca(carga(nombre))
        w, h = im.size
        if w < 1080:  # ampliación suave de las más pequeñas
            f = 1080 / w
            im = im.resize((1080, int(h * f)), Image.LANCZOS).filter(
                ImageFilter.UnsharpMask(radius=2, percent=40, threshold=2))
        guarda(im, OUT / "fotos" / f"{nombre}.webp")
        sm = im.copy(); sm.thumbnail((640, 900), Image.LANCZOS)
        guarda(sm, OUT / "fotos" / "sm" / f"{nombre}.webp", 78)


def ajusta(im, w, h):
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.42))


def heroes():
    W, H = 1080, 1350
    for nombre, piezas in HEROES.items():
        lienzo = Image.new("RGB", (W * 3, H), (20, 18, 16))
        for i, p in enumerate(piezas):
            lienzo.paste(ajusta(retoca(carga(p)), W, H), (i * W, 0))
        # banda panorámica 2.35:1 para escritorio
        pan =ImageOps.fit(lienzo, (3240, 1380), Image.LANCZOS, centering=(0.5, 0.4))
        guarda(pan, OUT / "hero" / f"{nombre}.webp", 80)
        pan_m = pan.copy(); pan_m.thumbnail((1920, 1920), Image.LANCZOS)
        guarda(pan_m, OUT / "hero" / f"{nombre}-1920.webp", 80)
        # versión móvil: la foto central en vertical
        movil = ajusta(retoca(carga(piezas[1])), 1080, 1440)
        guarda(movil, OUT / "hero" / f"{nombre}-m.webp", 80)
    for nombre, foto in HEROES_SIMPLES.items():
        im = retoca(carga(foto))
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(
            ImageFilter.UnsharpMask(radius=2.4, percent=60, threshold=2))
        pan = ImageOps.fit(im, (2400, 1022), Image.LANCZOS, centering=(0.5, 0.5))
        guarda(pan, OUT / "hero" / f"{nombre}.webp", 80)
        pan_m = pan.copy(); pan_m.thumbnail((1920, 1920), Image.LANCZOS)
        guarda(pan_m, OUT / "hero" / f"{nombre}-1920.webp", 80)
        movil = ImageOps.fit(im, (1080, 1440), Image.LANCZOS, centering=(0.45, 0.5))
        guarda(movil, OUT / "hero" / f"{nombre}-m.webp", 80)


def marca():
    src = ROOT / "Logo de peluquería con fondo transparente.png"
    logo = Image.open(src).convert("RGBA")
    bbox = logo.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    logo = logo.crop(bbox)
    d = OUT / "brand"; d.mkdir(parents=True, exist_ok=True)
    negro = logo.copy(); negro.thumbnail((900, 900), Image.LANCZOS)
    negro.save(d / "logo-negro.png", optimize=True)
    # versión clara: invierte solo el color, conserva el alfa
    r, g, b, a = negro.split()
    inv = ImageChops.invert(Image.merge("RGB", (r, g, b)))
    claro = Image.merge("RGBA", (*inv.split(), a))
    # tono hueso, no blanco puro
    tinte = Image.new("RGBA", claro.size, (246, 240, 230, 255))
    claro = Image.composite(tinte, claro, ImageChops.multiply(inv.convert("L"), a).point(lambda v: 255 if v > 128 else 0))
    claro.putalpha(ImageChops.multiply(a, inv.convert("L")))
    claro.save(d / "logo-claro.png", optimize=True)
    # favicon y icono táctil
    ic = Image.new("RGBA", (512, 512), (22, 20, 18, 255))
    c = claro.copy(); c.thumbnail((440, 440), Image.LANCZOS)
    ic.alpha_composite(c, ((512 - c.width) // 2, (512 - c.height) // 2))
    ic.convert("RGB").save(d / "apple-touch-icon.png")
    ic.resize((64, 64), Image.LANCZOS).save(d / "favicon.png")
    # imagen para compartir 1200×630
    og = Image.new("RGB", (1200, 630), (22, 20, 18))
    hero = Image.open(OUT / "hero" / "home-1920.webp").convert("RGB")
    hero = ImageOps.fit(hero, (1200, 630), Image.LANCZOS)
    og = Image.blend(og, hero, 0.38)
    c = claro.copy(); c.thumbnail((620, 420), Image.LANCZOS)
    og.paste(c, ((1200 - c.width) // 2, (630 - c.height) // 2), c)
    og.save(d / "og.jpg", quality=86)


if __name__ == "__main__":
    fotos()
    heroes()
    marca()
    print("listo")
