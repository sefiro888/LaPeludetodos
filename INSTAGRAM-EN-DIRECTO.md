# Instagram en directo y reels

## Muro «Recién salidas del sillón»
Está en la portada y en la galería. Muestra 8 publicaciones de @lapeludet2 con su texto. Al pasar el ratón (o siempre, en el móvil) se ve el comienzo del texto, y cada foto lleva a su publicación.

**Ahora mismo:** es una copia fija de 8 publicaciones (`INSTAGRAM_POSTS` en `scripts/content.py`).

**Para que se actualice sola con lo último que publique Cova**, se conecta un servicio que convierte el Instagram en un «feed» que la web lee. La web ya está preparada para **Behold** (behold.so), que tiene plan gratuito:

1. Crea una cuenta en https://behold.so con el correo del salón.
2. Conecta el Instagram **@lapeludet2**. Tiene que ser una cuenta **profesional o de creador**; se cambia en Instagram → Configuración → Tipo de cuenta, es gratis y no cambia nada para los seguidores.
3. Crea un *feed* de tipo **JSON** y copia su dirección. Será parecida a `https://feeds.behold.so/AbCdEf123`.
4. Pégala en `scripts/content.py`:
   ```python
   INSTAGRAM_FEED_URL = "https://feeds.behold.so/AbCdEf123"
   ```
5. Ejecuta `python build.py` y sube la web.

A partir de ahí, cada visita carga las últimas 8 publicaciones y aparece la etiqueta roja **«En directo»**. Si algún día falla la conexión, la web muestra la copia fija, así que nunca queda vacía.

> Comprueba en behold.so los límites actuales del plan gratuito. Para una web como esta suele bastar.
> Lo he probado con un feed simulado con el formato de Behold. Con la cuenta real conviene hacer una comprobación rápida al conectarla.

## Reels
Están en la portada («La pelu en vídeo») y en las páginas de Sobre Cova, coloración, mechas, alisados y tratamientos. La lista está en `REELS`, dentro de `scripts/content.py`.

- **Ahora:** se ve la portada del reel con un botón de reproducir. Al pulsarlo se abre el **reproductor oficial de Instagram** dentro de la web, con su sonido.
- **Mejor todavía:** si Cova te pasa los vídeos originales (`.mp4`), guárdalos como `assets/video/<código>.mp4` y ejecuta `python build.py`. Así se reproducen en bucle y sin sonido dentro de la tarjeta, solo cuando están a la vista, y al pulsar se ven a pantalla completa con sonido.
  - El código es el de la dirección del reel: `instagram.com/reel/`**`DEhGw37tpSz`**`/`.
- Para cambiar qué reels salen, edita `REELS` y ejecuta `python scripts/prepare_reels.py`, que descarga las portadas.
