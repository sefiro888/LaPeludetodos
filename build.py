# -*- coding: utf-8 -*-
"""Genera la web estática de La Pelu de Tod@s.

    python scripts/prepare_assets.py   # (solo si cambian fotos o logo)
    python build.py
"""
import json
import re
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from content import (NEGOCIO as N, HORARIO, HORARIO_FILAS, RESENAS, CATEGORIAS,  # noqa: E402
                     SERVICIOS, SERV, FAQ_GENERAL, QUIZ, CABECERAS_PELU)

VERSION = "4"
IA = ROOT / "assets" / "img" / "ia"
e = escape


# ------------------------------------------------------------------ utilidades
def wa(texto: str) -> str:
    return f"https://wa.me/{N['wa']}?text={quote(texto)}"


def foto(nombre, sm=False):
    return f"assets/img/fotos/{'sm/' if sm else ''}{nombre}.webp"


ICONOS = {
    "wa": '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3Z" fill="currentColor"/>',
    "tel": '<path d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.2 11.4 11.4 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .6 3.6 1 1 0 0 1-.3 1Z" fill="currentColor"/>',
    "pin": '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z" fill="currentColor"/>',
    "reloj": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/>',
    "fb": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5a.5.5 0 0 1 .5-.5Z" fill="currentColor"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "estrella": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z" fill="currentColor"/>',
    "check": '<path d="m5 12.5 4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "hoja": '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15M5 19l8-8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "chispa": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    "corazon": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    "wifi": '<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.5a9.5 9.5 0 0 1 13 0M8.5 16a5 5 0 0 1 7 0" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="19" r="1.3" fill="currentColor"/>',
    "acceso": '<circle cx="12" cy="4.5" r="2" fill="currentColor"/><path d="M5 8.5h14M12 8.5v5l-3.5 7M12 13.5l3.5 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "tijera": '<circle cx="6" cy="6" r="3" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="6" cy="18" r="3" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M8.2 7.8 20 18M8.2 16.2 20 6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "lupa": '<circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m16 16 4.5 4.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "calendario": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M3.5 10h17M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "persona": '<circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M4 21a8 8 0 0 1 16 0" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "mas": '<path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "ruta": '<path d="M6 19a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM18 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM8.5 14.5 15.5 9.5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
}


def ico(n, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONOS[n]}</svg>'


def estrellas(n=5):
    return '<span class="stars" aria-label="%d de 5 estrellas">%s</span>' % (n, ico("estrella") * n)


# ------------------------------------------------------------------ cabecera
def nav_mega():
    tag = ' <em class="tag">Estrella</em>'

    def col(cat):
        items = "".join(
            f'<li><a href="{s["slug"]}.html" class="mega-link" data-img="{foto(s["thumb"], True)}">'
            f'<span class="mega-name">{e(s["nombre"])}{tag if s.get("estrella") else ""}</span>'
            f'<span class="mega-desc">{e(s["menu"])}</span></a></li>'
            for s in SERVICIOS if s["cat"] == cat)
        return items
    pelu = col("pelu")
    otros = col("terapia")
    est = col("estetica")
    return f"""
<div class="mega" id="mega-servicios" role="region" aria-label="Servicios">
  <div class="mega-inner">
    <div class="mega-col mega-col--wide">
      <p class="mega-title">{e(CATEGORIAS['pelu'][0])}</p>
      <ul class="mega-list mega-list--2">{pelu}</ul>
    </div>
    <div class="mega-col">
      <p class="mega-title">{e(CATEGORIAS['terapia'][0])}</p>
      <ul class="mega-list">{otros}</ul>
      <p class="mega-title mt">{e(CATEGORIAS['estetica'][0])}</p>
      <ul class="mega-list">{est}</ul>
    </div>
    <div class="mega-preview" aria-hidden="true">
      <img src="{foto('vegetal-rizo-cobre', True)}" alt="" class="mega-img" loading="lazy">
      <div class="mega-preview-txt"><span>Servicio estrella</span><strong>Coloración vegetal con plantas</strong></div>
      <a class="mega-all" href="servicios.html">Ver todos los servicios {ico('flecha')}</a>
    </div>
  </div>
</div>"""


def header(activo):
    def a(href, txt, key):
        cur = ' aria-current="page"' if key == activo else ""
        return f'<a href="{href}" class="nav-link"{cur}>{txt}</a>'
    return f"""
<a class="skip" href="#main">Saltar al contenido</a>
<div class="topbar">
  <div class="wrap topbar-in">
    <span class="estado" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></span>
    <span class="topbar-mid">Carretera Circunvalación 15 · Errekalde, Bilbao</span>
    <span class="topbar-right">
      <a href="tel:{N['tel_fijo_href']}">{ico('tel')} {N['tel_fijo']}</a>
      <a href="{N['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ico('ig')}</a>
      <a href="{N['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{ico('fb')}</a>
    </span>
  </div>
</div>
<header class="site-header" data-header>
  <div class="wrap header-in">
    <a href="index.html" class="brand" aria-label="La Pelu de Tod@s · inicio">
      <img src="assets/img/brand/logo-claro.png" alt="" class="brand-logo" width="70" height="57">
      <span class="brand-txt"><span class="brand-name">La Pelu de Tod<span class="arroba">@</span>s</span><span class="brand-sub">Covadonga Izquierdo · desde 1983</span></span>
    </a>
    <nav class="nav" aria-label="Principal">
      {a('index.html', 'Inicio', 'inicio')}
      <div class="nav-item has-mega">
        <button class="nav-link nav-btn" aria-expanded="false" aria-controls="mega-servicios"{' aria-current="page"' if activo == 'servicios' else ''}>Servicios <span class="chev"></span></button>
        {nav_mega()}
      </div>
      <div class="nav-item has-drop">
        <button class="nav-link nav-btn" aria-expanded="false" aria-controls="drop-pelu"{' aria-current="page"' if activo == 'pelu' else ''}>La Pelu <span class="chev"></span></button>
        <div class="drop" id="drop-pelu">
          <a href="sobre-cova.html"><strong>Sobre Cova</strong><span>Más de 30 años de oficio</span></a>
          <a href="espacio-para-todos.html"><strong>Un espacio para tod@s</strong><span>Inclusivo y seguro</span></a>
          <a href="galeria.html"><strong>Galería de trabajos</strong><span>Color, cortes y rizos reales</span></a>
          <a href="opiniones.html"><strong>Opiniones</strong><span>4,8 ★ en Google</span></a>
        </div>
      </div>
      {a('ubicacion.html', 'Cómo llegar', 'ubicacion')}
      {a('contacto.html', 'Contacto', 'contacto')}
    </nav>
    <a href="contacto.html#cita" class="btn btn-brass btn-sm header-cta">{ico('wa')} Pedir cita</a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu-movil" data-burger>
      <span class="burger-lines"><i></i><i></i><i></i></span><span class="burger-txt">Menú</span>
    </button>
  </div>
</header>
{menu_movil()}"""


def menu_movil():
    grupos = ""
    for cat, (titulo, sub) in CATEGORIAS.items():
        items = "".join(
            f'<a href="{s["slug"]}.html" class="mm-serv"><img src="{foto(s["thumb"], True)}" alt="" loading="lazy">'
            f'<span><strong>{e(s["nombre"])}</strong><small>{e(s["menu"])}</small></span></a>'
            for s in SERVICIOS if s["cat"] == cat)
        grupos += f"""
      <details class="mm-group">
        <summary><span>{e(titulo)}</span><span class="mm-plus">{ico('mas')}</span></summary>
        <div class="mm-servs">{items}</div>
      </details>"""
    return f"""
<div class="mmenu" id="menu-movil" data-mmenu aria-hidden="true">
  <div class="mmenu-bg"></div>
  <div class="mmenu-in">
    <div class="mmenu-top">
      <img src="assets/img/brand/logo-claro.png" alt="La Pelu de Tod@s" class="mmenu-logo">
      <button class="mmenu-close" data-close aria-label="Cerrar menú">{ico('x')}</button>
    </div>
    <p class="estado estado--menu" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
    <nav class="mm-nav" aria-label="Menú móvil">
      <a href="index.html" class="mm-link"><em>01</em>Inicio</a>
      <a href="servicios.html" class="mm-link"><em>02</em>Todos los servicios</a>
      {grupos}
      <a href="sobre-cova.html" class="mm-link"><em>03</em>Sobre Cova</a>
      <a href="espacio-para-todos.html" class="mm-link"><em>04</em>Espacio para tod@s</a>
      <a href="galeria.html" class="mm-link"><em>05</em>Galería</a>
      <a href="opiniones.html" class="mm-link"><em>06</em>Opiniones</a>
      <a href="ubicacion.html" class="mm-link"><em>07</em>Cómo llegar</a>
      <a href="contacto.html" class="mm-link"><em>08</em>Contacto y cita</a>
    </nav>
    <div class="mm-actions">
      <a class="btn btn-brass" href="{wa('¡Hola Cova! Me gustaría pedir cita en La Pelu de Tod@s.')}" target="_blank" rel="noopener">{ico('wa')} WhatsApp</a>
      <a class="btn btn-ghost-light" href="tel:{N['tel_fijo_href']}">{ico('tel')} Llamar</a>
      <a class="btn btn-ghost-light" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('pin')} Cómo llegar</a>
    </div>
    <div class="mm-social">
      <a href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} @lapeludet2</a>
      <a href="{N['facebook']}" target="_blank" rel="noopener">{ico('fb')} La pelu de todos</a>
    </div>
    <button class="paleta mm-paleta" data-paleta type="button"><span class="paleta-sw"></span><span class="paleta-txt"><span data-paleta-nombre>Paleta latón</span><small>Cambiar a la otra paleta</small></span></button>
    <div class="pride-line" aria-hidden="true"></div>
  </div>
</div>"""


# ------------------------------------------------------------------ hero
def hero(clave, eyebrow, h1, intro, ctas="", extra="", alto="", banco=False):
    ia = IA / f"hero-{clave}.webp"
    stock = ROOT / "assets" / "img" / "stock" / f"{clave}.webp"
    if ia.exists():  # imagen generada por IA guardada por el cliente
        src_d = src_l = src_m = f"assets/img/ia/hero-{clave}.webp"
    elif banco and CABECERAS_PELU == "banco" and stock.exists():  # banco de imágenes
        src_d, src_l, src_m = (f"assets/img/stock/{clave}-1920.webp", f"assets/img/stock/{clave}.webp",
                               f"assets/img/stock/{clave}-m.webp")
    else:
        src_d, src_l, src_m = (f"assets/img/hero/{clave}-1920.webp", f"assets/img/hero/{clave}.webp",
                               f"assets/img/hero/{clave}-m.webp")
    return f"""
<section class="hero {alto}" data-hero>
  <picture class="hero-media">
    <source media="(max-width: 700px)" srcset="{src_m}">
    <source media="(min-width: 1921px)" srcset="{src_l}">
    <img src="{src_d}" alt="" fetchpriority="high" decoding="async">
  </picture>
  <div class="hero-shade"></div>
  <div class="wrap hero-in">
    <p class="eyebrow eyebrow--light">{e(eyebrow)}</p>
    <h1 class="hero-title">{h1}</h1>
    <p class="hero-intro">{e(intro)}</p>
    <div class="hero-ctas">{ctas}</div>
    {extra}
  </div>
  <a href="#main" class="hero-scroll" aria-label="Bajar al contenido"><span></span></a>
</section>"""


def ctas_cita(texto_wa, segundo=("Ver servicios", "servicios.html")):
    return (f'<a class="btn btn-brass" href="{wa(texto_wa)}" target="_blank" rel="noopener">{ico("wa")} Pedir cita por WhatsApp</a>'
            f'<a class="btn btn-ghost-light" href="{segundo[1]}">{segundo[0]} {ico("flecha")}</a>')


# ------------------------------------------------------------------ bloques comunes
def cinta(items=None):
    items = items or ["Coloración vegetal", "Corte y color", "Mechas y balayage", "Diagnóstico capilar",
                      "Láser capilar", "Presoterapia", "Solárium", "Novias y eventos", "Espacio para tod@s"]
    seq = "".join(f"<span>{e(t)}</span><i>✦</i>" for t in items)
    return f'<div class="cinta" aria-hidden="true"><div class="cinta-track">{seq}{seq}</div></div>'


def tarjeta_servicio(s, grande=False):
    return f"""
<a href="{s['slug']}.html" class="card-serv{' card-serv--big' if grande else ''}" data-cat="{s['cat']}">
  <span class="card-img"><img src="{foto(s['thumb'], True)}" alt="{e(s['nombre'])}" loading="lazy"></span>
  <span class="card-body">
    <span class="card-cat">{e(CATEGORIAS[s['cat']][0])}</span>
    <strong class="card-title">{e(s['nombre'])}</strong>
    <span class="card-txt">{e(s['menu'])}</span>
    <span class="card-more">Descubrir {ico('flecha')}</span>
  </span>
  {"<span class='badge-star'>" + ico('hoja') + " Estrella</span>" if s.get('estrella') else ''}
</a>"""


def resena_card(i):
    autor, fuente, n, txt = RESENAS[i]
    return f"""
<figure class="review">
  {estrellas(n)}
  <blockquote>«{e(txt)}»</blockquote>
  <figcaption><span class="avatar">{e(autor[0])}</span><span><strong>{e(autor)}</strong><small>{e(fuente)}</small></span></figcaption>
</figure>"""


def carrusel_resenas(titulo="Lo que dicen de Cova", sub="4,8 ★ de media en Google · 26 reseñas"):
    cards = "".join(resena_card(i) for i in range(len(RESENAS)))
    return f"""
<section class="section section--ink reviews-sec" aria-labelledby="t-resenas">
  <div class="wrap">
    <div class="sec-head sec-head--row">
      <div>
        <p class="eyebrow eyebrow--light">Opiniones reales</p>
        <h2 id="t-resenas" class="h2">{titulo}</h2>
        <p class="lead lead--light">{sub}</p>
      </div>
      <div class="car-ctrl">
        <button class="car-btn" data-car-prev aria-label="Anterior">{ico('flecha', 'ico flip')}</button>
        <button class="car-btn" data-car-next aria-label="Siguiente">{ico('flecha')}</button>
      </div>
    </div>
    <div class="carousel" data-carousel tabindex="0" aria-label="Reseñas de clientas">{cards}</div>
    <p class="center mt-l"><a href="opiniones.html" class="link-light">Leer todas las opiniones {ico('flecha')}</a></p>
  </div>
</section>"""


def faq_list(faqs, abierto=True):
    out = ""
    for i, (q, a) in enumerate(faqs):
        out += f"""
<details class="faq"{' open' if (abierto and i == 0) else ''}>
  <summary><span>{e(q)}</span><span class="faq-ico">{ico('mas')}</span></summary>
  <div class="faq-a"><p>{e(a)}</p></div>
</details>"""
    return out


def horario_tabla():
    filas = "".join(
        f'<tr data-dia="{i}"><th scope="row">{d}</th><td>{h}</td><td class="muted">{n}</td></tr>'
        for i, (d, h, n) in enumerate(HORARIO_FILAS))
    return f'<table class="horario">{filas}</table>'


def bloque_visita(titulo="Ven a vernos"):
    return f"""
<section class="section visit" aria-labelledby="t-visita">
  <div class="wrap visit-grid">
    <div class="visit-info">
      <p class="eyebrow">Dónde y cuándo</p>
      <h2 id="t-visita" class="h2">{titulo}</h2>
      <ul class="info-list">
        <li>{ico('pin')}<span><strong>{e(N['direccion'])}</strong><br>{e(N['barrio'])} · {N['cp']} {N['ciudad']} ({N['provincia']})</span></li>
        <li>{ico('wa')}<span><strong>WhatsApp y reservas</strong><br><a href="{wa('¡Hola! Quería pedir cita.')}" target="_blank" rel="noopener">{N['movil']}</a></span></li>
        <li>{ico('tel')}<span><strong>Llamadas e información</strong><br><a href="tel:{N['tel_fijo_href']}">{N['tel_fijo']}</a></span></li>
      </ul>
      <h3 class="h4 mt">Horario</h3>
      {horario_tabla()}
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
      <div class="btn-row">
        <a class="btn btn-ink" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('ruta')} Cómo llegar</a>
        <a class="btn btn-outline" href="ubicacion.html">Ver el barrio {ico('flecha')}</a>
      </div>
    </div>
    {mapa()}
  </div>
</section>"""


def mapa():
    return f"""
<div class="map" data-map data-src="https://www.google.com/maps?q={N['lat']},{N['lng']}&z=17&output=embed">
  <img src="assets/img/hero/ubicacion-m.webp" alt="" loading="lazy">
  <div class="map-cover">
    <span class="map-pin">{ico('pin')}</span>
    <strong>La Pelu de Tod@s</strong>
    <span>Circunvalación 15 · Errekalde</span>
    <button class="btn btn-brass btn-sm" data-map-load>Cargar mapa interactivo</button>
    <small>Al pulsar se carga Google Maps.</small>
  </div>
</div>"""


def cta_final(texto="¿Te damos cita?", sub="Escríbenos por WhatsApp y te respondemos en cuanto terminemos con la clienta que está en el sillón.", msg="¡Hola Cova! Me gustaría pedir cita."):
    return f"""
<section class="cta-final">
  <div class="cta-bg" style="background-image:url('assets/img/hero/contacto-1920.webp')"></div>
  <div class="wrap cta-in">
    <img src="assets/img/brand/logo-claro.png" alt="" class="cta-logo" loading="lazy">
    <h2 class="h2">{texto}</h2>
    <p class="lead lead--light">{sub}</p>
    <div class="btn-row center">
      <a class="btn btn-brass btn-lg" href="{wa(msg)}" target="_blank" rel="noopener">{ico('wa')} {N['movil']}</a>
      <a class="btn btn-ghost-light btn-lg" href="tel:{N['tel_fijo_href']}">{ico('tel')} {N['tel_fijo']}</a>
    </div>
  </div>
</section>"""


def footer():
    serv = lambda cat: "".join(f'<li><a href="{s["slug"]}.html">{e(s["nombre"])}</a></li>' for s in SERVICIOS if s["cat"] == cat)
    return f"""
<footer class="footer">
  <div class="pride-line" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="assets/img/brand/logo-claro.png" alt="La Pelu de Tod@s · Covadonga Izquierdo · desde 1983" class="footer-logo" loading="lazy">
      <p>Peluquería, coloración natural con plantas, terapias capilares y bienestar en Errekalde, Bilbao. Un salón inclusivo, seguro y cercano, donde cada persona es bienvenida.</p>
      <div class="footer-social">
        <a href="{N['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ico('ig')}</a>
        <a href="{N['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{ico('fb')}</a>
        <a href="{wa('¡Hola!')}" target="_blank" rel="noopener" aria-label="WhatsApp">{ico('wa')}</a>
      </div>
    </div>
    <div><p class="f-title">Peluquería</p><ul>{serv('pelu')}</ul></div>
    <div><p class="f-title">Terapias y estética</p><ul>{serv('terapia')}{serv('estetica')}</ul>
      <p class="f-title mt">La Pelu</p><ul><li><a href="sobre-cova.html">Sobre Cova</a></li><li><a href="espacio-para-todos.html">Espacio para tod@s</a></li><li><a href="galeria.html">Galería</a></li><li><a href="opiniones.html">Opiniones</a></li></ul></div>
    <div>
      <p class="f-title">Visítanos</p>
      <p>{e(N['direccion'])}<br>{e(N['barrio'])}<br>{N['cp']} {N['ciudad']} ({N['provincia']})</p>
      <p><a href="tel:{N['tel_fijo_href']}">{N['tel_fijo']}</a> · <a href="{wa('¡Hola!')}" target="_blank" rel="noopener">{N['movil']}</a></p>
      <p class="f-hours">Mar–Vie 9:30–18:00<br>Sáb 9:00–14:00 (con cita)<br>Lun y Dom cerrado</p>
      <p class="f-extras">{ico('wifi')} Wi-Fi gratis · {ico('acceso')} A pie de calle</p>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© 2026 La Pelu de Tod@s · Covadonga Izquierdo</span>
    <span>Web de demostración · Fotos: @lapeludet2</span>
  </div>
</footer>
<nav class="actionbar" aria-label="Acciones rápidas">
  <a href="tel:{N['tel_fijo_href']}">{ico('tel')}<span>Llamar</span></a>
  <a href="{wa('¡Hola Cova! Me gustaría pedir cita.')}" target="_blank" rel="noopener" class="ab-main">{ico('wa')}<span>Cita</span></a>
  <a href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('pin')}<span>Llegar</span></a>
</nav>
<button class="paleta" data-paleta type="button" aria-label="Cambiar paleta de colores"><span class="paleta-sw"></span><span class="paleta-txt"><span data-paleta-nombre>Paleta latón</span><small>Toca para cambiar</small></span></button>
<a class="wa-float" href="{wa('¡Hola Cova! Me gustaría pedir cita.')}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{ico('wa')}<span>¿Hablamos?</span></a>
<div class="lightbox" data-lightbox hidden><button class="lb-close" aria-label="Cerrar">{ico('x')}</button><button class="lb-prev" aria-label="Anterior">{ico('flecha', 'ico flip')}</button><img alt=""><button class="lb-next" aria-label="Siguiente">{ico('flecha')}</button><p class="lb-cap"></p></div>"""


_MEDIDAS = {}


def _con_medidas(m):
    ruta = m.group(1)
    if ruta not in _MEDIDAS:
        from PIL import Image
        with Image.open(ROOT / ruta) as im:
            _MEDIDAS[ruta] = im.size
    w, h = _MEDIDAS[ruta]
    return f'<img src="{ruta}" width="{w}" height="{h}"'


def pagina(archivo, titulo, desc, activo, cuerpo, og="assets/img/brand/og.jpg", jsonld=None):
    horario_js = json.dumps({str(k): v for k, v in HORARIO.items()})
    ld = ""
    if jsonld:
        ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#161412">
<script>try{{if(localStorage.getItem("lpdt-paleta")==="mono")document.documentElement.dataset.theme="mono"}}catch(e){{}}</script>
<meta property="og:type" content="website">
<meta property="og:site_name" content="La Pelu de Tod@s · Bilbao">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/brand/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&family=Manrope:wght@400;500;600;700&family=Oswald:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={VERSION}">
{ld}
</head>
<body data-page="{activo}">
{header(activo)}
<main id="main">
{cuerpo}
</main>
{footer()}
<script>window.HORARIO={horario_js};</script>
<script src="assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""
    # la «@» de Fraunces es poco legible: en el texto visible se compone con Manrope
    cab, sep, resto = html.partition("<body")
    def _at(m):
        txt = m.group(1)
        if "@s" not in txt:
            return m.group(0)
        return '><span class="atw">' + txt.replace("@s", '<span class="at">@</span>s') + "</span><"
    resto = re.sub(r">([^<]*)<", _at, resto)
    resto = re.sub(r'(<option[^>]*>)([^<]*)<span class="at">@</span>s', r"@s", resto)
    html = cab + sep + resto
    # ancho y alto en cada imagen local: reserva su hueco y evita saltos al cargar
    html = re.sub(r'<img src="(assets/[^"]+)"(?![^>]*width=)', _con_medidas, html)
    (ROOT / archivo).write_text(html, encoding="utf-8")
    return archivo


JSONLD_NEGOCIO = {
    "@context": "https://schema.org", "@type": "HairSalon", "name": "La Pelu de Tod@s",
    "image": "assets/img/brand/og.jpg", "telephone": "+34946240479",
    "address": {"@type": "PostalAddress", "streetAddress": "Carretera Circunvalación 15, local 5",
                "addressLocality": "Bilbao", "postalCode": "48002", "addressRegion": "Bizkaia", "addressCountry": "ES"},
    "geo": {"@type": "GeoCoordinates", "latitude": N["lat"], "longitude": N["lng"]},
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "26"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:30", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"}],
    "sameAs": [N["instagram"], N["facebook"]],
}


# ------------------------------------------------------------------ asistente de cita
def asistente(preseleccion=""):
    opts = "".join(
        f'<option value="{e(s["nombre"])}"{" selected" if s["slug"] == preseleccion else ""}>{e(s["nombre"])}</option>'
        for s in SERVICIOS)
    return f"""
<form class="wizard" data-wizard id="cita" autocomplete="off">
  <div class="wizard-head">
    <p class="eyebrow">Reserva guiada</p>
    <h2 class="h3">Prepara tu mensaje de cita</h2>
    <p class="muted">Rellena lo que quieras y abriremos WhatsApp con el mensaje escrito. No guardamos ningún dato.</p>
  </div>
  <label class="field"><span>¿Qué te apetece?</span>
    <select name="servicio"><option value="">Aún no lo sé, quiero que me asesores</option>{opts}</select></label>
  <fieldset class="field"><legend>¿Qué días te vienen bien?</legend>
    <div class="chips" data-multi="dias">
      <button type="button" class="chip">Martes</button><button type="button" class="chip">Miércoles</button>
      <button type="button" class="chip">Jueves</button><button type="button" class="chip">Viernes</button>
      <button type="button" class="chip">Sábado</button><button type="button" class="chip">Lo antes posible</button>
    </div></fieldset>
  <fieldset class="field"><legend>¿Mejor por la mañana o por la tarde?</legend>
    <div class="chips" data-single="franja">
      <button type="button" class="chip">Mañana</button><button type="button" class="chip">Mediodía</button><button type="button" class="chip">Tarde</button><button type="button" class="chip">Me da igual</button>
    </div></fieldset>
  <fieldset class="field"><legend>¿Es tu primera vez en La Pelu?</legend>
    <div class="chips" data-single="primera"><button type="button" class="chip">Sí, primera vez</button><button type="button" class="chip">Ya soy clienta/e</button></div></fieldset>
  <label class="check"><input type="checkbox" name="preso"> <span>Añadir presoterapia por 5 € (con servicio de color)</span></label>
  <div class="field-row">
    <label class="field"><span>Tu nombre</span><input name="nombre" type="text" placeholder="Opcional"></label>
    <label class="field"><span>Algo que debamos saber</span><input name="notas" type="text" placeholder="Alergias, ideas, fotos que enviarás…"></label>
  </div>
  <div class="wizard-preview"><span class="muted">Así quedará tu mensaje:</span><p data-preview></p></div>
  <a class="btn btn-brass btn-lg btn-block" data-send href="{wa('¡Hola Cova!')}" target="_blank" rel="noopener">{ico('wa')} Enviar por WhatsApp</a>
</form>"""


# ------------------------------------------------------------------ páginas de servicio
def pagina_servicio(s):
    cat_t = CATEGORIAS[s["cat"]][0]
    msg = f"¡Hola Cova! Me interesa el servicio de {s['nombre']}. ¿Me das cita?"
    hero_html = hero(s["hero"], s["eyebrow"], e(s["h1"]), s["intro"], ctas_cita(msg, ("Cómo es la sesión", "#pasos")),
                     banco=s["cat"] == "pelu")
    migas = f'<nav class="crumbs wrap" aria-label="Ruta"><a href="index.html">Inicio</a><span>/</span><a href="servicios.html">Servicios</a><span>/</span><span>{e(cat_t)}</span></nav>'
    toc_items = [("que-es", "Qué es"), ("beneficios", "Beneficios"), ("para-quien", "Para quién"), ("pasos", "La sesión"),
                 ("opciones", "Opciones")]
    if s["galeria"]:
        toc_items.append(("trabajos", "Trabajos"))
    toc_items += [("cuidados", "Cuidados")]
    if s["mitos"]:
        toc_items.append(("mitos", "Mitos"))
    toc_items += [("preguntas", "Preguntas"), ("cita", "Cita")]
    toc = "".join(f'<a href="#{i}">{t}</a>' for i, t in toc_items)

    que = "".join(f"<p>{e(p)}</p>" for p in s["que_es"])
    benef = "".join(f'<div class="benef reveal"><span class="benef-n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (t, d) in enumerate(s["beneficios"]))
    quien = "".join(f'<li>{ico("check")}<span>{e(x)}</span></li>' for x in s["para_quien"])
    pasos = "".join(f'<li class="step reveal"><span class="step-n">{i+1}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'
                    for i, (t, d) in enumerate(s["pasos"]))
    opciones = "".join(f"""
<article class="opt reveal">
  <h3>{e(n)}</h3><p>{e(d)}</p>
  <a class="opt-link" href="{wa(f'¡Hola Cova! Me interesa: {n} ({s["nombre"]}). ¿Me informas y me das cita?')}" target="_blank" rel="noopener">{ico('wa')} Consultar esta opción</a>
</article>""" for n, d in s["opciones"])
    gal = ""
    if s["galeria"]:
        figs = "".join(f'<figure class="g-item reveal"><button data-lb="{foto(g)}" aria-label="Ampliar foto"><img src="{foto(g, True)}" alt="Trabajo real de La Pelu de Tod@s" loading="lazy"></button></figure>'
                       for g in s["galeria"])
        gal = f"""
<section class="section section--bone" id="trabajos" aria-labelledby="t-trab">
  <div class="wrap">
    <div class="sec-head sec-head--row">
      <div><p class="eyebrow">Hecho en La Pelu</p><h2 id="t-trab" class="h2">Trabajos reales</h2>
      <p class="lead">Fotos de clientas y clientes de Cova publicadas en <a href="{N['instagram']}" target="_blank" rel="noopener">@lapeludet2</a>. Pulsa para ampliar.</p></div>
      <a class="btn btn-outline" href="galeria.html">Ver galería completa {ico('flecha')}</a>
    </div>
    <div class="g-grid g-grid--{min(len(s['galeria']), 4)}" data-gallery>{figs}</div>
  </div>
</section>"""
    tit_cons, cons = s["consejos"]
    cons_html = "".join(f'<li><span class="tip-n">{i+1}</span><p>{e(c)}</p></li>' for i, c in enumerate(cons))
    mitos = ""
    if s["mitos"]:
        m = "".join(f'<div class="myth reveal"><p class="myth-q"><span>Mito</span>{e(a)}</p><p class="myth-a"><span>Realidad</span>{e(b)}</p></div>'
                    for a, b in s["mitos"])
        mitos = f"""
<section class="section" id="mitos" aria-labelledby="t-mitos">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Sin humo</p><h2 id="t-mitos" class="h2">Mitos y realidades</h2></div>
    <div class="myths">{m}</div>
  </div>
</section>"""
    rel = "".join(tarjeta_servicio(SERV[r]) for r in s["relacionados"])
    autor, fuente, n, txt = RESENAS[s["resena"]]
    combo = ""
    if s["slug"] in ("coloracion", "coloracion-vegetal", "mechas-balayage"):
        combo = f"""
<aside class="promo reveal">
  <div class="promo-img"><img src="{foto('presoterapia-botas', True)}" alt="" loading="lazy"></div>
  <div class="promo-txt"><p class="eyebrow eyebrow--light">Mímate un poquito más</p>
  <h3 class="h3">Presoterapia por solo 5 € más</h3>
  <p>Mientras se fija tu color, relaja las piernas y mejora la circulación. Sal de la pelu con el cuerpo y el cabello renovados.</p>
  <a class="btn btn-brass btn-sm" href="presoterapia.html">Saber más {ico('flecha')}</a></div>
</aside>"""

    galeria_lateral = s["galeria"][0] if s["galeria"] else s["thumb"]
    cuerpo = f"""
{hero_html}
{migas}
<div class="toc-wrap" data-toc><nav class="toc wrap" aria-label="En esta página">{toc}</nav></div>

<section class="section" id="que-es" aria-labelledby="t-que">
  <div class="wrap split">
    <div class="split-txt prose">
      <p class="eyebrow">{e(cat_t)}</p>
      <h2 id="t-que" class="h2">¿En qué consiste?</h2>
      {que}
      <blockquote class="pull">{e(s['destacado'])}</blockquote>
    </div>
    <div class="split-media reveal">
      <figure class="frame"><img src="{foto(galeria_lateral)}" alt="{e(s['nombre'])} en La Pelu de Tod@s" loading="lazy"></figure>
      <figure class="review review--mini">
        {estrellas(n)}<blockquote>«{e(txt)}»</blockquote><figcaption><strong>{e(autor)}</strong> · <small>{e(fuente)}</small></figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="section section--ink" id="beneficios" aria-labelledby="t-ben">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow eyebrow--light">Por qué elegirlo</p><h2 id="t-ben" class="h2">Beneficios</h2></div>
    <div class="benefs">{benef}</div>
  </div>
</section>

<section class="section" id="para-quien" aria-labelledby="t-quien">
  <div class="wrap split split--rev">
    <div class="split-txt">
      <p class="eyebrow">¿Es para mí?</p>
      <h2 id="t-quien" class="h2">Para quién es</h2>
      <ul class="ticks">{quien}</ul>
      {combo}
    </div>
    <div class="split-txt" id="pasos">
      <p class="eyebrow">Paso a paso</p>
      <h2 class="h2">Así es tu cita</h2>
      <ol class="steps">{pasos}</ol>
    </div>
  </div>
</section>

<section class="section section--bone" id="opciones" aria-labelledby="t-opc">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Elige</p><h2 id="t-opc" class="h2">Opciones del servicio</h2>
    <p class="lead">Cada opción tiene su botón: te abre WhatsApp con el mensaje escrito para que Cova te informe de precio y disponibilidad.</p></div>
    <div class="opts">{opciones}</div>
  </div>
</section>
{gal}
<section class="section" id="cuidados" aria-labelledby="t-cuid">
  <div class="wrap split">
    <div class="split-txt">
      <p class="eyebrow">Consejos de Cova</p>
      <h2 id="t-cuid" class="h2">{e(tit_cons)}</h2>
      <ol class="tips">{cons_html}</ol>
    </div>
    <div class="split-media reveal">
      <figure class="frame frame--tall"><img src="{foto(s['galeria'][1] if len(s['galeria']) > 1 else s['thumb'])}" alt="" loading="lazy"></figure>
    </div>
  </div>
</section>
{mitos}
<section class="section section--bone" id="preguntas" aria-labelledby="t-faq">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">Dudas frecuentes</p><h2 id="t-faq" class="h2">Preguntas sobre {e(s['nombre'].lower())}</h2>
    <p class="lead">¿No encuentras tu respuesta? Escríbenos y te contestamos encantadas.</p>
    <a class="btn btn-ink" href="{wa(msg)}" target="_blank" rel="noopener">{ico('wa')} Preguntar por WhatsApp</a></div>
    <div class="faqs">{faq_list(s['faqs'])}</div>
  </div>
</section>

<section class="section" aria-labelledby="t-cita">
  <div class="wrap wizard-wrap">
    <div class="wizard-side">
      <p class="eyebrow">Reserva</p>
      <h2 id="t-cita" class="h2">Pide tu cita</h2>
      <p class="lead">Ya hemos elegido «{e(s['nombre'])}» por ti en el formulario. Martes a viernes de 9:30 a 18:00 en horario continuo. Sábados de 9:00 a 14:00, solo con cita previa.</p>
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
      <ul class="mini-facts">
        <li>{ico('wifi')} Wi-Fi gratis mientras esperas</li>
        <li>{ico('corazon')} Espacio inclusivo y seguro</li>
        <li>{ico('acceso')} Local a pie de calle</li>
      </ul>
    </div>
    {asistente(s['slug'])}
  </div>
</section>

<section class="section section--bone" aria-labelledby="t-rel">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Combina bien con</p><h2 id="t-rel" class="h2">Servicios relacionados</h2></div>
    <div class="cards cards--3">{rel}</div>
  </div>
</section>
{cta_final()}"""
    return pagina(f"{s['slug']}.html", f"{s['nombre']} en Bilbao · La Pelu de Tod@s", s["meta"],
                  "servicios", cuerpo, jsonld={"@context": "https://schema.org", "@type": "Service", "name": s["nombre"],
                                               "provider": {"@type": "HairSalon", "name": "La Pelu de Tod@s"},
                                               "areaServed": "Bilbao", "description": s["meta"]})


# ------------------------------------------------------------------ portada
def pagina_inicio():
    extra = f"""
<div class="hero-badges">
  <span class="hb">{estrellas()}<span><b>4,8</b> en Google</span></span>
  <span class="hb">{ico('hoja')}<span>Coloración 100 % vegetal</span></span>
  <span class="hb hb--pride">{ico('corazon')}<span>Espacio para tod@s</span></span>
</div>"""
    h = hero("home", "Peluquería y bienestar · Errekalde, Bilbao",
             'La Pelu de Tod<span class="arroba">@</span>s.<br><em>Tu espacio de belleza y bienestar en Bilbao.</em>',
             "Liderado por Cova Izquierdo, con más de 30 años de experiencia combinando la peluquería de vanguardia, la coloración natural con barros y tratamientos estéticos avanzados.",
             ctas_cita("¡Hola Cova! Me gustaría pedir cita en La Pelu de Tod@s."), extra, "hero--home")

    cards = "".join(tarjeta_servicio(s) for s in SERVICIOS)
    quiz = "".join(f'<button type="button" class="chip chip--quiz" data-quiz=\'{json.dumps(v)}\'>{e(k)}</button>' for k, v in QUIZ)
    quiz_cards = "".join(f'<template data-tpl="{s["slug"]}">{tarjeta_servicio(s)}</template>' for s in SERVICIOS)
    galeria = ["mechas-balayage-ondas", "fantasia-rosa-lila", "vegetal-rizo-cobre", "corte-bob-rubio", "color-burdeos-liso",
               "rizo-definido", "recogido-rizos", "fantasia-rosa-ondas", "color-cobre-melena", "corte-chico-cova", "mechas-ombre-cobre", "color-violeta-liso"]
    strip = "".join(f'<figure><img src="{foto(g, True)}" alt="Trabajo de La Pelu de Tod@s" loading="lazy"></figure>' for g in galeria)

    cuerpo = f"""
{h}
{cinta()}

<section class="section intro" aria-labelledby="t-intro">
  <div class="wrap intro-grid">
    <div class="intro-quote reveal">
      <p class="eyebrow">Nuestra filosofía</p>
      <h2 id="t-intro" class="display">«Un salón inclusivo, seguro y pensado para cuidar de ti de forma cercana, donde cada persona es bienvenida.»</h2>
      <p class="sign">— Cova Izquierdo</p>
    </div>
    <div class="intro-stats">
      <div class="stat reveal"><strong data-count="1983">1983</strong><span>Desde entonces con tijeras en la mano</span></div>
      <div class="stat reveal"><strong>+30</strong><span>Años de experiencia de Cova</span></div>
      <div class="stat reveal"><strong>4,8<small>★</small></strong><span>Media en Google · 26 reseñas</span></div>
      <div class="stat reveal"><strong>100<small>%</small></strong><span>Coloración vegetal, sin amoniaco ni PPD</span></div>
    </div>
  </div>
</section>

<section class="section section--ink star" aria-labelledby="t-star">
  <div class="wrap star-grid">
    <div class="star-media reveal">
      <img src="{foto('vegetal-rizo-cobre')}" alt="Melena rizada cobriza teñida con plantas" loading="lazy" class="star-a">
      <img src="{foto('vegetal-productos', True)}" alt="Cosmética natural en La Pelu de Tod@s" loading="lazy" class="star-b">
      <span class="star-seal">{ico('hoja')}<b>Servicio<br>estrella</b></span>
    </div>
    <div class="star-txt">
      <p class="eyebrow eyebrow--light">Coloración botánica · plantas y barros</p>
      <h2 id="t-star" class="h2">Color que cuida: henna, índigo, cassia y amla</h2>
      <p class="lead lead--light">Nuestro tratamiento estrella de salud capilar. Coloración 100 % vegetal que envuelve la fibra en lugar de dañarla: cubre canas con reflejos naturales y devuelve un brillo terapéutico espectacular.</p>
      <ul class="ticks ticks--light">
        <li>{ico('check')}<span>Sin amoniaco, sin PPD y sin resorcinol.</span></li>
        <li>{ico('check')}<span>Ideal para cueros cabelludos sensibles o personas alérgicas.</span></li>
        <li>{ico('check')}<span>Más densidad, brillo y fuerza con cada aplicación.</span></li>
      </ul>
      <div class="btn-row"><a class="btn btn-brass" href="coloracion-vegetal.html">Descubrir la coloración vegetal {ico('flecha')}</a></div>
    </div>
  </div>
</section>

<section class="section" id="servicios" aria-labelledby="t-serv">
  <div class="wrap">
    <div class="sec-head sec-head--row">
      <div><p class="eyebrow">Qué hacemos</p><h2 id="t-serv" class="h2">Servicios para tod@s</h2>
      <p class="lead">Peluquería de autor, terapias capilares y bienestar corporal en un mismo salón.</p></div>
      <div class="filters" role="tablist" data-filter>
        <button class="filter is-on" data-f="all">Todos</button>
        <button class="filter" data-f="pelu">Peluquería</button>
        <button class="filter" data-f="terapia">Terapias</button>
        <button class="filter" data-f="estetica">Estética</button>
      </div>
    </div>
    <div class="cards" data-cards>{cards}</div>
  </div>
</section>

<section class="section section--bone quiz" aria-labelledby="t-quiz">
  <div class="wrap">
    <div class="sec-head center"><p class="eyebrow">Test rápido</p><h2 id="t-quiz" class="h2">¿Qué necesita tu pelo hoy?</h2>
    <p class="lead">Toca lo que más se parezca a tu caso y te sugerimos por dónde empezar.</p></div>
    <div class="chips chips--center" data-quizbox>{quiz}</div>
    <div class="quiz-out" data-quiz-out aria-live="polite"></div>
    {quiz_cards}
  </div>
</section>

<section class="section cova" aria-labelledby="t-cova">
  <div class="wrap split">
    <div class="split-media reveal">
      <div class="cova-stack">
        <img src="{foto('cova-clienta')}" alt="Cova con una clienta" loading="lazy" class="cs-a">
        <img src="{foto('corte-chico-cova', True)}" alt="Cova cortando el pelo a un cliente" loading="lazy" class="cs-b">
      </div>
    </div>
    <div class="split-txt prose">
      <p class="eyebrow">Quién está detrás</p>
      <h2 id="t-cova" class="h2">Cova: tres décadas escuchando antes de cortar</h2>
      <p>Detrás de La Pelu de Tod@s está Covadonga «Cova» Izquierdo, una estilista apasionada con más de tres décadas de trayectoria en el sector de la estética en el País Vasco.</p>
      <p>El salón nació con una idea clara: romper con las peluquerías rígidas y crear un punto de encuentro donde el trato esté basado en la escucha activa y la confianza mutua. Con los años, las clientas no son solo usuarias: son amigas.</p>
      <blockquote class="pull">«En La Pelu de Tod@s no solo cuidamos el cabello… también compartimos risas, charlas, confianza y esa energía bonita que nace cuando te sientes como en casa.»</blockquote>
      <a class="btn btn-ink" href="sobre-cova.html">Conoce a Cova {ico('flecha')}</a>
    </div>
  </div>
</section>

<section class="pride-band" aria-labelledby="t-pride">
  <div class="wrap pride-in">
    <div>
      <p class="eyebrow eyebrow--light">Un espacio para tod@s</p>
      <h2 id="t-pride" class="h2">Aquí tienes total libertad para expresarte tal y como eres</h2>
    </div>
    <ul class="pride-list">
      <li>{ico('corazon')} Amigable con el colectivo LGBTQ+</li>
      <li>{ico('persona')} Transgender safe space</li>
      <li>{ico('tijera')} Cortes unisex, sin etiquetas</li>
      <li>{ico('acceso')} Aseos inclusivos y local a pie de calle</li>
    </ul>
    <a class="btn btn-ghost-light" href="espacio-para-todos.html">Nuestro compromiso {ico('flecha')}</a>
  </div>
</section>

<section class="section promo-sec" aria-labelledby="t-promo">
  <div class="wrap promo-grid">
    <article class="promo-card reveal">
      <img src="{foto('presoterapia-botas')}" alt="" loading="lazy">
      <div><p class="eyebrow">Mímate por 5 € más</p><h3 id="t-promo" class="h3">Presoterapia mientras se fija tu color</h3>
      <p>Al reservar tu coloración, añade una sesión de presoterapia por solo 5 € más. Color para tu melena y bienestar para tu cuerpo.</p>
      <a class="link" href="presoterapia.html">Ver presoterapia {ico('flecha')}</a></div>
    </article>
    <article class="promo-card reveal">
      <img src="{foto('raiz-cana-2')}" alt="" loading="lazy">
      <div><p class="eyebrow">Novedad</p><h3 class="h3">Color exprés y primeras canas</h3>
      <p>Tapamos tus canas en poco tiempo, o solo las primeras sin cambiar tu color natural. Rápido, discreto y natural.</p>
      <a class="link" href="coloracion.html">Ver coloración {ico('flecha')}</a></div>
    </article>
    <article class="promo-card reveal">
      <img src="{foto('color-dorado')}" alt="" loading="lazy">
      <div><p class="eyebrow">Para habituales</p><h3 class="h3">Bonos de color, presoterapia y solárium</h3>
      <p>Si vienes con regularidad, aprovecha nuestros bonos: cómodos, económicos y adaptados a tu ritmo.</p>
      <a class="link" href="{wa('¡Hola Cova! Me gustaría información sobre los bonos.')}" target="_blank" rel="noopener">Preguntar por los bonos {ico('flecha')}</a></div>
    </article>
  </div>
</section>

<section class="section section--bone strip-sec" aria-labelledby="t-strip">
  <div class="wrap sec-head sec-head--row">
    <div><p class="eyebrow">@lapeludet2</p><h2 id="t-strip" class="h2">Recién salidas del sillón</h2></div>
    <div class="btn-row"><a class="btn btn-outline" href="galeria.html">Galería</a><a class="btn btn-ink" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} Síguenos</a></div>
  </div>
  <div class="strip" data-strip><div class="strip-track">{strip}{strip}</div></div>
</section>

{carrusel_resenas()}

<section class="section" aria-labelledby="t-faqh">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">Antes de venir</p><h2 id="t-faqh" class="h2">Preguntas frecuentes</h2>
    <p class="lead">Todo lo práctico: cómo pedir cita, horarios, bonos y qué te vas a encontrar.</p></div>
    <div class="faqs">{faq_list(FAQ_GENERAL)}</div>
  </div>
</section>

{bloque_visita()}
{cta_final()}"""
    return pagina("index.html", "La Pelu de Tod@s · Peluquería, coloración vegetal y bienestar en Bilbao",
                  "Peluquería en Errekalde (Bilbao) de Cova Izquierdo: corte, color, coloración vegetal con plantas, diagnóstico y láser capilar, presoterapia y solárium. Espacio inclusivo. 4,8 ★ en Google.",
                  "inicio", cuerpo, jsonld=JSONLD_NEGOCIO)


# ------------------------------------------------------------------ servicios
def pagina_servicios():
    h = hero("servicios", "Carta de servicios", "Todo lo que podemos hacer por ti",
             "Peluquería y estilismo, terapias capilares avanzadas y estética y bienestar corporal. Cada servicio empieza con lo mismo: escucharte.",
             ctas_cita("¡Hola Cova! Quería información sobre vuestros servicios.", ("Pedir cita", "contacto.html#cita")))
    bloques = ""
    for cat, (titulo, sub) in CATEGORIAS.items():
        cs = [s for s in SERVICIOS if s["cat"] == cat]
        lista = "".join(f"""
<a class="serv-row reveal" href="{s['slug']}.html">
  <img src="{foto(s['thumb'], True)}" alt="" loading="lazy">
  <span class="serv-row-txt"><strong>{e(s['nombre'])}{' <em class="tag">Estrella</em>' if s.get('estrella') else ''}</strong><span>{e(s['intro'])}</span></span>
  <span class="serv-row-go">{ico('flecha')}</span>
</a>""" for s in cs)
        bloques += f"""
<section class="section{' section--bone' if cat == 'terapia' else ''}" id="{cat}" aria-labelledby="t-{cat}">
  <div class="wrap serv-cat">
    <div class="serv-cat-head"><p class="eyebrow">{len(cs)} servicios</p><h2 id="t-{cat}" class="h2">{e(titulo)}</h2><p class="lead">{e(sub)}</p></div>
    <div class="serv-list">{lista}</div>
  </div>
</section>"""
    extras = f"""
<section class="section section--ink" aria-labelledby="t-extras">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow eyebrow--light">Ventajas</p><h2 id="t-extras" class="h2">Bonos, combinaciones y detalles</h2></div>
    <div class="benefs">
      <div class="benef reveal"><span class="benef-n">5 €</span><h3>Presoterapia + color</h3><p>Añádela a tu coloración por solo 5 € más y relájate mientras actúa el tinte.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('calendario')}</span><h3>Bonos de color</h3><p>Para quien se tiñe con regularidad: cómodos, económicos y adaptados a tu ritmo.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('chispa')}</span><h3>Bonos de presoterapia y solárium</h3><p>Más constancia, mejores resultados y mejor precio.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('reloj')}</span><h3>Color exprés</h3><p>Cubrimos tus canas en un corto espacio de tiempo, sin renunciar a la calidad.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('lupa')}</span><h3>Diagnóstico previo</h3><p>Evaluamos cuero cabelludo y fibra antes de aplicar cualquier químico.</p></div>
      <div class="benef reveal"><span class="benef-n">{ico('wifi')}</span><h3>Wi-Fi gratis</h3><p>Para tus esperas y los tiempos de exposición.</p></div>
    </div>
    <p class="note-light">Trabajamos con marcas profesionales como {', '.join(N['marcas'])}, y con coloración y cosmética 100 % vegetal.</p>
  </div>
</section>"""
    cuerpo = f"""{h}
<div class="toc-wrap" data-toc><nav class="toc wrap" aria-label="Categorías"><a href="#pelu">Peluquería</a><a href="#terapia">Terapias capilares</a><a href="#estetica">Estética y bienestar</a></nav></div>
{bloques}{extras}{cta_final()}"""
    return pagina("servicios.html", "Servicios · La Pelu de Tod@s · Bilbao",
                  "Cortes, coloración, mechas, coloración vegetal, alisados, rizos, novias, diagnóstico y láser capilar, presoterapia, solárium y depilación láser en Bilbao.",
                  "servicios", cuerpo)


# ------------------------------------------------------------------ sobre cova
def pagina_cova():
    h = hero("sobre-cova", "La Pelu · Sobre nosotras", "Detrás de La Pelu está Cova",
             "Covadonga «Cova» Izquierdo, estilista apasionada con más de tres décadas de trayectoria en el sector de la estética en el País Vasco.",
             ctas_cita("¡Hola Cova! Me gustaría conocerte y pedir cita.", ("Ver su trabajo", "galeria.html")))
    linea = [
        ("1983", "El origen", "La marca nace con una fecha que luce en el logo: desde 1983. Tijeras, peine y mucho oficio."),
        ("+30 años", "Oficio", "Más de tres décadas cortando, coloreando y peinando en el País Vasco. Especialista en corte y color."),
        ("Errekalde", "La Pelu de Tod@s", "Un salón de barrio, acogedor y elegante, en la Carretera Circunvalación: un punto de encuentro."),
        ("Hoy", "Salud capilar", "Coloración vegetal, diagnósticos capilares, láser capilar, presoterapia y solárium. Siempre aprendiendo."),
    ]
    tl = "".join(f'<li class="tl-item reveal"><span class="tl-year">{a}</span><div><h3>{b}</h3><p>{c}</p></div></li>' for a, b, c in linea)
    valores = [
        ("Escucha activa", "Antes de meter la tijera, escuchamos. Lo que quieres, lo que te preocupa, cómo te peinas."),
        ("Confianza", "Te decimos la verdad sobre tu pelo, aunque sea «hoy no, mejor en dos pasos»."),
        ("Cercanía", "Con el tiempo, el trato se convierte en amistad. Aquí te sientes como en casa."),
        ("Salud capilar", "Diagnóstico, cosmética respetuosa y opciones 100 % naturales."),
        ("Inclusión", "Un espacio para tod@s: LGBTQ+ friendly y transgender safe space."),
        ("Oficio", "Más de 30 años de técnica, formación y amor por la peluquería."),
    ]
    val = "".join(f'<div class="benef reveal"><span class="benef-n">{i+1:02d}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(valores))
    cuerpo = f"""{h}
<section class="section" aria-labelledby="t-hist">
  <div class="wrap split">
    <div class="split-txt prose">
      <p class="eyebrow">Nuestra historia</p>
      <h2 id="t-hist" class="h2">Romper con las peluquerías rígidas</h2>
      <p>Detrás de La Pelu de Tod@s está Covadonga «Cova» Izquierdo, una estilista apasionada con más de tres décadas de trayectoria en el sector de la estética en el País Vasco.</p>
      <p>Nuestro salón nació con una idea clara: romper con las peluquerías rígidas y crear un punto de encuentro donde el trato al cliente esté basado en la escucha activa y la confianza mutua. Con los años, nuestras clientas no son solo usuarias: son amigas.</p>
      <p>Además, nos enorgullece ser un espacio oficialmente amigable con el colectivo LGBTQ+ y un entorno seguro para personas transgénero (transgender safe space). Aquí tienes la total libertad de expresarte tal y como eres.</p>
      <blockquote class="pull">«Gracias por confiar en mí. Gracias por recomendarme. Gracias por elegir esta pequeña pelu para mimar vuestra melena.» — Cova</blockquote>
    </div>
    <div class="split-media reveal">
      <div class="cova-stack">
        <img src="{foto('corte-chico-cova')}" alt="Cova cortando el pelo a un cliente" loading="lazy" class="cs-a">
        <img src="{foto('cova-clienta', True)}" alt="Cova con una clienta" loading="lazy" class="cs-b">
      </div>
    </div>
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-tl">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Trayectoria</p><h2 id="t-tl" class="h2">Una vida entre tijeras</h2></div>
    <ol class="timeline">{tl}</ol>
  </div>
</section>
<section class="section section--ink" aria-labelledby="t-val">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow eyebrow--light">Lo que nos mueve</p><h2 id="t-val" class="h2">Nuestros valores</h2></div>
    <div class="benefs">{val}</div>
  </div>
</section>
<section class="section" aria-labelledby="t-amig">
  <div class="wrap split split--rev">
    <div class="split-txt prose">
      <p class="eyebrow">Clientas y amigas</p>
      <h2 id="t-amig" class="h2">Cada visita es más que una cita</h2>
      <p>Es un ratito para ti, un espacio seguro para desconectar y una relación que se llena de amistad con el tiempo. Cada visita, cada charla, cada cambio de look y cada sonrisa hacen que este trabajo sea especial.</p>
      <p>Seguimos creando color, luz, peinados, momentos bonitos y esa sensación de salir de la peluquería sintiéndote mejor que cuando llegaste.</p>
      <p class="sign">— Cova, con vosotras siempre</p>
    </div>
    <div class="split-media reveal">
      <figure class="frame"><img src="{foto('cova-grupo')}" alt="Cova con clientas y amigas" loading="lazy"></figure>
    </div>
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-marcas">
  <div class="wrap center">
    <p class="eyebrow">Con qué trabajamos</p>
    <h2 id="t-marcas" class="h2">Marcas profesionales y cosmética natural</h2>
    <div class="brands">{''.join(f'<span>{m}</span>' for m in N['marcas'])}<span>Coloración 100 % vegetal</span></div>
  </div>
</section>
{carrusel_resenas('Lo que dicen de Cova')}
{cta_final()}"""
    return pagina("sobre-cova.html", "Sobre Cova Izquierdo · La Pelu de Tod@s · Bilbao",
                  "Conoce a Covadonga «Cova» Izquierdo, estilista con más de 30 años de experiencia y alma de La Pelu de Tod@s en Errekalde, Bilbao.",
                  "pelu", cuerpo)


# ------------------------------------------------------------------ espacio para todos
def pagina_espacio():
    h = hero("espacio", "La Pelu · Inclusión", 'Un espacio para tod<span class="arroba">@</span>s',
             "Un salón inclusivo, amigable con el colectivo LGBTQ+ y un espacio seguro para personas trans. Aquí cada persona es bienvenida, tal y como es.",
             ctas_cita("¡Hola Cova! Me gustaría pedir cita.", ("Conoce a Cova", "sobre-cova.html")))
    comp = [
        ("corazon", "LGBTQ+ friendly", "Así nos identifica también Google: un negocio amigable con el colectivo LGBTQ+."),
        ("persona", "Transgender safe space", "Te tratamos con el nombre y los pronombres que nos digas. Sin preguntas incómodas."),
        ("tijera", "Cortes sin etiquetas", "El corte es para la persona: mujer, hombre, no binarie… da igual. Lo que te represente."),
        ("acceso", "Accesible e inclusivo", "Local a pie de calle y aseos inclusivos."),
        ("chispa", "Exprésate", "Colores fantasía, cambios radicales o lo más clásico: tu imagen, tus reglas."),
        ("hoja", "Mujer al frente", "Negocio identificado como propiedad de mujeres, con alma de barrio."),
    ]
    c = "".join(f'<div class="benef reveal"><span class="benef-n">{ico(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in comp)
    cuerpo = f"""{h}
<section class="section" aria-labelledby="t-nom">
  <div class="wrap split">
    <div class="split-txt prose">
      <p class="eyebrow">Por qué «Tod@s»</p>
      <h2 id="t-nom" class="h2">Una arroba que lo dice todo</h2>
      <p>En el logo pone «La Pelu de Todos», pero desde hace años la llamamos La Pelu de Tod@s. Esa arroba no es un adorno: es una forma de decir que este salón es para cualquier persona, sea cual sea su género, su edad, su estilo o su historia.</p>
      <p>Una peluquería dedicada a tod@s y para tod@s. Un lugar donde el trato es cercano, la escucha es real y nadie tiene que dar explicaciones sobre cómo quiere verse.</p>
      <blockquote class="pull">Aquí tienes total libertad para expresarte tal y como eres.</blockquote>
    </div>
    <div class="split-media reveal">
      <figure class="frame"><img src="{foto('fantasia-rosa-lila')}" alt="Corte corto con color fantasía rosa y lila" loading="lazy"></figure>
    </div>
  </div>
</section>
<section class="pride-band" aria-labelledby="t-comp">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow eyebrow--light">Nuestro compromiso</p><h2 id="t-comp" class="h2">Lo que significa para nosotras</h2></div>
    <div class="benefs benefs--glass">{c}</div>
  </div>
</section>
<section class="section" aria-labelledby="t-prac">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">En la práctica</p><h2 id="t-prac" class="h2">Cómo te cuidamos</h2>
    <p class="lead">Pequeños gestos que hacen que te sientas en casa desde que cruzas la puerta.</p></div>
    <div class="faqs">{faq_list([
        ("¿Cómo pido cita si quiero que usen otro nombre?", "Escríbenos por WhatsApp con el nombre que quieres que usemos. Así lo anotamos y será el que usemos siempre."),
        ("¿Los precios dependen del género?", "No. Lo que cuenta es el servicio, el largo y el trabajo, nunca el género."),
        ("¿Puedo venir acompañade?", "Claro. Puedes venir con quien quieras y hay Wi-Fi gratis para las esperas."),
        ("¿Y si es mi primera vez en un salón y me da corte?", "Cuéntanoslo. Vamos a tu ritmo, explicamos cada paso y paramos cuando quieras."),
        ("¿Qué hago si algo me incomoda?", "Dínoslo con total confianza. Queremos saberlo para mejorar."),
    ])}</div>
  </div>
</section>
{carrusel_resenas('Te sientes a gusto desde que entras')}
{cta_final()}"""
    return pagina("espacio-para-todos.html", "Un espacio para tod@s · LGBTQ+ friendly · La Pelu de Tod@s",
                  "La Pelu de Tod@s es un salón inclusivo en Bilbao: LGBTQ+ friendly, transgender safe space, cortes sin etiquetas y aseos inclusivos.",
                  "pelu", cuerpo)


# ------------------------------------------------------------------ galería
GAL_CATS = {
    "color": ["color-cobre-melena", "color-burdeos-liso", "color-violeta-liso", "color-dorado", "color-cobre-largo", "color-cobre-espalda",
              "color-castano-claro", "color-cobre-salon", "color-negro-liso", "color-antes-despues", "color-castano-oscuro"],
    "mechas": ["mechas-balayage-ondas", "mechas-balayage-logo", "mechas-degradado-logo", "mechas-ombre-cobre", "mechas-ombre-cobre-2",
               "mechas-rubias", "mechas-capas", "mechas-clienta", "mechas-reflejos", "mechas-largo-logo", "color-rojo-mechas"],
    "fantasia": ["fantasia-rosa-lila", "fantasia-rojo-negro", "fantasia-rosa-ondas", "fantasia-azul", "fantasia-trenza-azul"],
    "vegetal": ["vegetal-rizo-cobre", "vegetal-largo", "vegetal-castano", "vegetal-bob", "vegetal-productos", "vegetal-cosmetica"],
    "cortes": ["corte-bob-rubio", "corte-bob-cobre", "corte-bob-cobre-2", "corte-bob-castano", "corte-corto-negro", "corte-pixie-cobre",
               "corte-chico-cova", "corte-capas-mechas", "corte-ninos", "corte-media-melena"],
    "texturas": ["liso-largo", "liso-espejo", "rizo-definido", "rizo-corto", "rizo-mechas", "rizo-lavado", "recogido-rizos", "trenza-boho"],
}
GAL_NOMBRES = {"color": "Color", "mechas": "Mechas y balayage", "fantasia": "Fantasía", "vegetal": "Vegetal", "cortes": "Cortes", "texturas": "Liso, rizo y peinados"}


def pagina_galeria():
    h = hero("galeria", "La Pelu · Trabajos reales", "Galería: recién salidas del sillón",
             "Color, mechas, cortes, rizos y coloración vegetal. Fotos reales de clientas y clientes de Cova, publicadas en Instagram.",
             ctas_cita("¡Hola Cova! He visto la galería y me encanta. ¿Me das cita?", ("Ver servicios", "servicios.html")))
    filtros = '<button class="filter is-on" data-f="all">Todo</button>' + "".join(
        f'<button class="filter" data-f="{k}">{v}</button>' for k, v in GAL_NOMBRES.items())
    items = ""
    for k, lista in GAL_CATS.items():
        for g in lista:
            items += f'<figure class="m-item" data-cat="{k}"><button data-lb="{foto(g)}" aria-label="Ampliar · {GAL_NOMBRES[k]}"><img src="{foto(g, True)}" alt="{GAL_NOMBRES[k]} · La Pelu de Tod@s" loading="lazy"><span>{GAL_NOMBRES[k]}</span></button></figure>'
    cuerpo = f"""{h}
<section class="section" aria-labelledby="t-gal">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><p class="eyebrow">{sum(len(v) for v in GAL_CATS.values())} trabajos</p><h2 id="t-gal" class="h2">Filtra por estilo</h2></div>
    <div class="filters" data-filter data-target="[data-masonry]">{filtros}</div></div>
    <div class="masonry" data-masonry data-gallery>{items}</div>
    <p class="center mt-l"><a class="btn btn-ink" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')} Ver más en @lapeludet2</a></p>
  </div>
</section>
{cta_final('¿Quieres ser la siguiente?')}"""
    return pagina("galeria.html", "Galería de trabajos · La Pelu de Tod@s · Bilbao",
                  "Galería de trabajos reales de La Pelu de Tod@s: color, mechas, balayage, colores fantasía, coloración vegetal, cortes, rizos y recogidos.",
                  "pelu", cuerpo)


# ------------------------------------------------------------------ opiniones
def pagina_opiniones():
    h = hero("opiniones", "La Pelu · Opiniones", "4,8 ★ de media y muchas amigas",
             "Reseñas reales de Google, Treatwell e Instagram. Lo que más repiten: que Cova escucha de verdad, que acierta con el color y que te sientes como en casa.",
             ctas_cita("¡Hola Cova! He leído las opiniones y me gustaría pedir cita."))
    muro = "".join(resena_card(i) for i in range(len(RESENAS)))
    barras = "".join(f'<div class="bar"><span>{n} ★</span><i style="--w:{w}%"></i></div>' for n, w in [(5, 85), (4, 11), (3, 4), (2, 0), (1, 0)])
    cuerpo = f"""{h}
<section class="section" aria-labelledby="t-op">
  <div class="wrap rating-grid">
    <div class="rating-box reveal">
      <strong class="rating-big">4,8</strong>{estrellas()}
      <p>26 reseñas en Google</p>
      <div class="bars">{barras}</div>
      <p class="muted small">También 5,0 en Treatwell y 5,0 en Facebook (100 % la recomiendan).</p>
      <a class="btn btn-outline btn-sm" href="{N['maps']}" target="_blank" rel="noopener">Ver en Google Maps</a>
    </div>
    <div class="prose">
      <p class="eyebrow">Lo que más se repite</p>
      <h2 id="t-op" class="h2">Escucha, acierto y cariño</h2>
      <div class="kw">
        <span>«Te escuchan de verdad»</span><span>«Acertó con el color»</span><span>«Trato cercano y familiar»</span>
        <span>«Gran profesional»</span><span>«Muy acogedora»</span><span>«Buen precio»</span><span>«Me sentí confiada»</span>
      </div>
      <p>Las reseñas de las clientas recurrentes destacan un trato muy cercano que con el tiempo se convierte en amistad, donde predomina la confianza y la escucha activa antes de meter la tijera.</p>
    </div>
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-muro">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Muro de opiniones</p><h2 id="t-muro" class="h2">En sus propias palabras</h2></div>
    <div class="review-wall">{muro}</div>
  </div>
</section>
<section class="section center" aria-labelledby="t-tu">
  <div class="wrap">
    <p class="eyebrow">¿Ya nos conoces?</p>
    <h2 id="t-tu" class="h2">Cuéntanos qué tal tu experiencia</h2>
    <p class="lead">Tu opinión ayuda a otras personas del barrio a encontrarnos.</p>
    <div class="btn-row center"><a class="btn btn-ink" href="{N['maps']}" target="_blank" rel="noopener">{estrellas()} Dejar reseña en Google</a></div>
  </div>
</section>
{cta_final()}"""
    return pagina("opiniones.html", "Opiniones · 4,8 ★ en Google · La Pelu de Tod@s",
                  "Opiniones reales de La Pelu de Tod@s en Bilbao: 4,8 ★ en Google con 26 reseñas, 5,0 en Treatwell y Facebook.",
                  "pelu", cuerpo)


# ------------------------------------------------------------------ ubicación
def pagina_ubicacion():
    h = hero("ubicacion", "Cómo llegar", "En el corazón de Errekalde",
             "Carretera Circunvalación nº 15, local 5. Barrio de Errekalde / Uretamendi, 48002 Bilbao. Local a pie de calle, junto al parque de Betolatza.",
             f'<a class="btn btn-brass" href="{N["maps_dir"]}" target="_blank" rel="noopener">{ico("ruta")} Abrir ruta en Google Maps</a>'
             f'<a class="btn btn-ghost-light" href="tel:{N["tel_fijo_href"]}">{ico("tel")} {N["tel_fijo"]}</a>')
    cuerpo = f"""{h}
<section class="section" aria-labelledby="t-dir">
  <div class="wrap visit-grid">
    <div class="visit-info">
      <p class="eyebrow">Dirección</p>
      <h2 id="t-dir" class="h2">Carretera Circunvalación, 15</h2>
      <address class="addr">La Pelu de Tod@s<br>{e(N['direccion'])}<br>{e(N['barrio'])}<br>{N['cp']} {N['ciudad']}, {N['provincia']}</address>
      <ul class="info-list">
        <li>{ico('pin')}<span><strong>Código plus</strong><br>63X2+P3 Bilbao</span></li>
        <li>{ico('acceso')}<span><strong>Accesible</strong><br>Local a pie de calle, sin escalones.</span></li>
        <li>{ico('wifi')}<span><strong>Wi-Fi gratis</strong><br>Para tus esperas y procesos técnicos.</span></li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-ink" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('ruta')} Cómo llegar</a>
        <button class="btn btn-outline" data-copy="{e(N['direccion'])}, {N['cp']} {N['ciudad']}">Copiar dirección</button>
      </div>
    </div>
    {mapa()}
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-como">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Llegar es fácil</p><h2 id="t-como" class="h2">Elige cómo venir</h2></div>
    <div class="opts">
      <article class="opt reveal"><h3>{ico('ruta')} En coche</h3><p>Estamos en la propia Carretera Circunvalación (Circunvalacion Errepidea), en la zona alta de Errekalde. Usa el botón «Cómo llegar» y Google Maps te guía hasta la puerta.</p></article>
      <article class="opt reveal"><h3>{ico('persona')} Andando</h3><p>Desde la zona comercial de Errekalde (Gordoniz, Altube) subes en pocos minutos. El local queda junto al parque de Betolatza.</p></article>
      <article class="opt reveal"><h3>{ico('calendario')} En transporte público</h3><p>Varias líneas de Bilbobus conectan Errekalde con el centro. Consulta la ruta en tiempo real en Google Maps o en la app de Bilbobus.</p></article>
      <article class="opt reveal"><h3>{ico('wa')} ¿Te pierdes?</h3><p>Escríbenos por WhatsApp al {N['movil']} o llama al {N['tel_fijo']} y te guiamos.</p></article>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="t-hor">
  <div class="wrap split">
    <div class="split-txt">
      <p class="eyebrow">Cuándo venir</p>
      <h2 id="t-hor" class="h2">Horario de atención</h2>
      {horario_tabla()}
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
      <p class="muted">En festivos y vacaciones publicamos los horarios especiales en Instagram y Facebook.</p>
    </div>
    <div class="split-media reveal"><figure class="frame"><img src="{foto('mechas-degradado-logo')}" alt="Clienta ante el photocall con el logo de La Pelu de Tod@s" loading="lazy"></figure></div>
  </div>
</section>
{cta_final('¿Te esperamos?')}"""
    return pagina("ubicacion.html", "Cómo llegar · La Pelu de Tod@s · Errekalde, Bilbao",
                  "Dirección, mapa, horario y cómo llegar a La Pelu de Tod@s: Carretera Circunvalación 15, local 5, Errekalde / Uretamendi, 48002 Bilbao.",
                  "ubicacion", cuerpo, jsonld=JSONLD_NEGOCIO)


# ------------------------------------------------------------------ contacto
def pagina_contacto():
    h = hero("contacto", "Contacto y cita", "Hablemos de tu pelo",
             "La forma más rápida de pedir cita es por WhatsApp. Cuéntanos qué te apetece y Cova te responde en cuanto termine con la clienta que está en el sillón.",
             ctas_cita("¡Hola Cova! Me gustaría pedir cita.", ("Reserva guiada", "#cita")))
    canales = f"""
<div class="channels">
  <a class="channel reveal" href="{wa('¡Hola Cova! Me gustaría pedir cita.')}" target="_blank" rel="noopener">{ico('wa')}<strong>WhatsApp</strong><span>{N['movil']}</span><small>Citas y consultas</small></a>
  <a class="channel reveal" href="tel:{N['tel_fijo_href']}">{ico('tel')}<strong>Teléfono</strong><span>{N['tel_fijo']}</span><small>Llamadas e información</small></a>
  <a class="channel reveal" href="tel:{N['movil_href']}">{ico('tel')}<strong>Móvil</strong><span>{N['movil']}</span><small>También llamadas</small></a>
  <a class="channel reveal" href="{N['instagram']}" target="_blank" rel="noopener">{ico('ig')}<strong>Instagram</strong><span>@lapeludet2</span><small>Trabajos y avisos</small></a>
  <a class="channel reveal" href="{N['facebook']}" target="_blank" rel="noopener">{ico('fb')}<strong>Facebook</strong><span>La pelu de todos</span><small>Novedades</small></a>
  <a class="channel reveal" href="{N['maps_dir']}" target="_blank" rel="noopener">{ico('pin')}<strong>Visítanos</strong><span>Circunvalación 15</span><small>Errekalde, Bilbao</small></a>
</div>"""
    cuerpo = f"""{h}
<section class="section" aria-labelledby="t-can">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Canales</p><h2 id="t-can" class="h2">Elige cómo hablar con nosotras</h2></div>
    {canales}
  </div>
</section>
<section class="section section--bone" aria-labelledby="t-cita">
  <div class="wrap wizard-wrap">
    <div class="wizard-side">
      <p class="eyebrow">Reserva</p>
      <h2 id="t-cita" class="h2">Tu cita en tres toques</h2>
      <p class="lead">Elige servicio, días y franja. Nosotras te confirmamos el hueco por WhatsApp.</p>
      {horario_tabla()}
      <p class="estado estado--block" data-estado><span class="dot"></span><span class="estado-txt">Consultando horario…</span></p>
    </div>
    {asistente()}
  </div>
</section>
<section class="section" aria-labelledby="t-faqc">
  <div class="wrap faq-grid">
    <div><p class="eyebrow">Dudas</p><h2 id="t-faqc" class="h2">Preguntas frecuentes</h2></div>
    <div class="faqs">{faq_list(FAQ_GENERAL)}</div>
  </div>
</section>
{bloque_visita('Te esperamos en Errekalde')}"""
    return pagina("contacto.html", "Contacto y cita · La Pelu de Tod@s · Bilbao",
                  "Pide cita en La Pelu de Tod@s por WhatsApp (676 67 98 07) o teléfono (946 24 04 79). Carretera Circunvalación 15, Errekalde, Bilbao.",
                  "contacto", cuerpo, jsonld=JSONLD_NEGOCIO)


def pagina_404():
    cuerpo = f"""
<section class="section notfound">
  <div class="wrap center">
    <img src="assets/img/brand/logo-negro.png" alt="" class="nf-logo">
    <h1 class="h2">Esta página se ha ido a cortar las puntas</h1>
    <p class="lead">No la encontramos, pero todo lo demás sigue en su sitio.</p>
    <div class="btn-row center"><a class="btn btn-ink" href="index.html">Volver al inicio</a><a class="btn btn-outline" href="servicios.html">Ver servicios</a></div>
  </div>
</section>"""
    return pagina("404.html", "Página no encontrada · La Pelu de Tod@s", "Página no encontrada.", "", cuerpo)


if __name__ == "__main__":
    hechas = [pagina_inicio(), pagina_servicios()]
    hechas += [pagina_servicio(s) for s in SERVICIOS]
    hechas += [pagina_cova(), pagina_espacio(), pagina_galeria(), pagina_opiniones(), pagina_ubicacion(), pagina_contacto(), pagina_404()]
    print(f"{len(hechas)} páginas generadas")
