# La Pelu de Tod@s · web de demostración

Peluquería y bienestar de **Covadonga «Cova» Izquierdo**, en Carretera Circunvalación nº 15, local 5, Errekalde / Uretamendi, 48002 Bilbao. Web estática generada con Python.

**Ver en local:** `python -m http.server 5240` → http://localhost:5240

## Identidad
- **Paleta sacada del logo:** tinta negra `#161412` sobre hueso `#f7f2ea`, con latón vintage `#b8894a` como acento, como en las barberías clásicas. Una línea arcoíris discreta y la «@» en degradado representan el «Tod@s».
- **Tipografías:** Fraunces para los titulares editoriales, Oswald para las etiquetas (recuerda al «Covadonga Izquierdo» del sello) y Manrope para el texto.
- **Logo:** versión negra y versión clara (invertida en tono hueso) en `assets/img/brand/`.

## Páginas (25 en castellano + 25 en euskera)
- `index.html`: portada con
  - cabecera panorámica y estado «abierto ahora»
  - cinta de servicios en movimiento
  - filosofía y cifras
  - servicio estrella (coloración vegetal)
  - 15 servicios con filtro
  - test «¿Qué necesita tu pelo hoy?»
  - Cova
  - franja «Espacio para tod@s»
  - promociones (presoterapia por 5 €, color exprés, bonos)
  - **antes y después** con barra deslizante
  - **reels** de Instagram con reproductor
  - **muro de Instagram** (preparado para ir en directo)
  - reseñas reales en carrusel, con enlace directo para valorar en Google
  - preguntas frecuentes, horario y mapa
- `servicios.html`: carta completa por categorías, con los bonos y las ventajas.
- **15 páginas de servicio.** Cada una tiene:
  - cabecera a todo el ancho con introducción
  - índice fijo
  - qué es, con una cita destacada y una reseña
  - 6 beneficios
  - para quién es y la cita paso a paso
  - opciones, cada una con su botón de WhatsApp
  - «Palabras que oirás en la cita», que enlazan al glosario
  - antes y después, y reels del servicio cuando los hay
  - trabajos reales con visor
  - consejos de cuidado, y mitos y realidades
  - preguntas frecuentes
  - asistente de cita con el servicio ya elegido
  - servicios relacionados
  - Peluquería: asesoría de imagen, cortes, coloración, mechas y balayage, colores fantasía, **coloración vegetal (estrella)**, alisados y keratina, rizos y permanentes, novias y eventos, tratamientos de nutrición.
  - Terapias capilares: diagnóstico capilar y láser capilar.
  - Estética: presoterapia, solárium y depilación láser (sesión mensual).
- `sobre-cova.html` (historia, trayectoria, valores, marcas), `espacio-para-todos.html` (LGBTQ+ friendly, safe space trans), `galeria.html` (51 trabajos con filtro y visor), `opiniones.html` (nota, palabras clave y muro de reseñas), `ubicacion.html` (mapa, cómo llegar, horario), `contacto.html` (canales, reserva guiada y preguntas frecuentes), **`glosario.html`** (42 palabras de la pelu con buscador e índice A–Z) y `404.html`.
- **`eu/`**: la web entera en **euskera**, con selector ES/EU en la barra superior, en el menú móvil y en el pie. Los mensajes de WhatsApp, el horario «abierto ahora» y el asistente de cita también salen en euskera.

## Menú
- **Escritorio:** barra superior con estado del horario, cabecera transparente que se vuelve sólida al bajar y se esconde al seguir bajando, y **mega menú** de servicios con vista previa de foto en cada servicio. Desplegable «La Pelu».
- **Móvil:** menú a pantalla completa que se abre en círculo desde el botón, con enlaces numerados, servicios agrupados en 3 desplegables con miniatura, estado del horario, WhatsApp, llamar, cómo llegar y redes. Además lleva una **barra fija inferior** (Llamar · Cita · Llegar).

## WhatsApp
Móvil y WhatsApp: **676 67 98 07** (`34676679807`). Todos los botones abren WhatsApp con un mensaje escrito según el servicio o la opción. El asistente de cita compone el mensaje en el navegador (servicio, días, franja, primera vez, presoterapia +5 €, nombre y notas) y no guarda nada.

## Imágenes
- Las fotos son reales, de @lapeludet2, y están en `_fuentes/instagram/`. `scripts/prepare_assets.py` las recorta (quita la marca de agua), ajusta contraste y color, las enfoca y monta las cabeceras panorámicas: un tríptico de 3240 px en escritorio y la foto central en vertical en móvil.
- **Imágenes IA opcionales:** lee `PROMPTS-IMAGENES.md`. Si guardas `assets/img/ia/hero-<página>.webp`, esa cabecera la usa sola.

## Cabeceras de peluquería: banco de imágenes o fotos propias
Ahora mismo, las 10 páginas de **peluquería y estilismo** llevan una cabecera de banco de imágenes (Unsplash, licencia libre). Así no se usan fotos de clientas sin permiso. Para volver a las fotos de @lapeludet2:
1. En `scripts/content.py`, cambia `CABECERAS_PELU = "banco"` por `CABECERAS_PELU = "propias"`.
2. Ejecuta `python build.py`.

No se ha borrado nada: los trípticos originales siguen en `assets/img/hero/` y los de banco en `assets/img/stock/`. Para cambiar alguna foto de banco, edita `scripts/prepare_stock.py` y ejecuta `python scripts/prepare_stock.py`. Los créditos están en `CREDITOS-IMAGENES.md`.

## Mejoras de la segunda ronda
| Mejora | Dónde | Guía |
| --- | --- | --- |
| Muro de Instagram «en directo» | Portada y galería | `INSTAGRAM-EN-DIRECTO.md` |
| Reels integrados | Portada, Sobre Cova y 4 servicios | `INSTAGRAM-EN-DIRECTO.md` |
| Antes y después (con ejemplos de demostración) | Portada, galería y servicios | `ANTES-DESPUES.md` |
| Ficha de Google: botón directo de reseña + datos estructurados | Pie, opiniones y carrusel | `FICHA-GOOGLE.md` |
| Glosario | `glosario.html` y enlaces desde los servicios | — |
| Versión en euskera | `eu/` | más abajo |
| Detalles de autor | Animación de entrada con tijeras (solo en la primera visita de la sesión), sello «La Pelu de Tod@s · desde 1983» que gira al hacer scroll y tijeras que «cortan» una línea entre secciones | — |

Todas respetan la opción del sistema «reducir movimiento».

## Al compartir el enlace (WhatsApp, Facebook, X…)
Cada página lleva imagen de 1200×630 con el logo (`assets/img/brand/og.jpg`, y `og-eu.jpg` en euskera; se regeneran con `python scripts/og.py`), título y descripción propios, con direcciones completas para que WhatsApp los cargue.

## Euskera
- `python build.py` genera `/eu/` traduciendo el HTML con `i18n/eu.json`.
- Las traducciones están en `i18n/eu/b*.txt` (número de texto según `i18n/cadenas-bloques.json`) y en `i18n/eu/extra.tsv` (castellano⇥euskera, para textos nuevos). Se unen con `python scripts/compila_eu.py`.
- Si añades textos nuevos, `python build.py` los lista en `i18n/pendientes-eu.txt`: cópialos a `extra.tsv` con su traducción. Hasta entonces se ven en castellano.
- Las reseñas de clientas se mantienen en el idioma original.
- **Conviene que una persona euskaldun revise la traducción antes de publicar.**

## Editar
- Textos y datos: `scripts/content.py`
- Plantillas: `build.py`. Después ejecuta `python build.py`.
- Estilos: `assets/css/site.css` · interacción: `assets/js/site.js`
- Revisión (usa Playwright global y el servidor local en 5240):
  - `python scripts/check.py`: enlaces e imágenes de las 50 páginas
  - `node scripts/shots.cjs <carpeta> [eu/]`: capturas y desbordes
  - `node scripts/scrolltest.cjs [eu/]`: rebotes de scroll y saltos de contenido

## Fuentes de información
- Material facilitado por el cliente.
- Instagram @lapeludet2: unas 50 publicaciones leídas (novias, maquillaje y desplazamiento, color exprés y primeras canas, bonos, presoterapia por +5 €, sesión mensual de depilación láser, mitos de la coloración vegetal, cuidados, rizos, keratina…).
- Ficha de Google: 4,8 ★ y 26 reseñas, LGBTQ+ friendly, propiedad de mujeres, coordenadas.
- Treatwell: 5,0 y marcas Yunsey, Salerm y Alfaparf.
- Facebook: 5,0 y 674 seguidores.

## Pendiente de confirmar con el salón
- **Local 5 o local 6:** la bio de Instagram y algunos carteles dicen «local 6»; la mayoría de publicaciones dicen «local 5». La web usa el 5.
- **Horario del sábado:** Treatwell dice 8:30–14:00; la web usa 9:00–14:00, como indicaste.
- **Precios:** solo se ha publicado el de presoterapia (+5 € con color). En lo demás, los botones invitan a consultar.
- Si siguen haciendo **maquillaje**, **pedicura** (aparece en una reseña antigua) y **parafina** (aparece en las destacadas de Instagram, sin detalle).
- Las **reseñas de ejemplo** que facilitaste (Marta G., Javi R., Leire U.) se han sustituido por **reseñas reales** de Google, Treatwell e Instagram, para no publicar opiniones inventadas.
- Quitar `noindex` al publicar.
