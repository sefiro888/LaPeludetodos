# Prompts de imágenes para La Pelu de Tod@s

La web ya funciona con **fotos reales de @lapeludet2** retocadas (nitidez, color, sin la marca «Galaxy Z Fold4») y montadas en cabeceras panorámicas de 3240 px.

Hay cuatro páginas sin fotos propias del servicio, y sus cabeceras son las más flojas. Para esas conviene generar una imagen:

| Prioridad | Archivo | Página | Qué lleva ahora |
| --- | --- | --- | --- |
| ★★★ | `hero-presoterapia.webp` | presoterapia.html | Ilustración de piernas ampliada |
| ★★★ | `hero-depilacion.webp` | depilacion-laser.html | La misma ilustración de piernas |
| ★★★ | `hero-laser-capilar.webp` | laser-capilar.html | Primeros planos de raíz |
| ★★ | `hero-diagnostico.webp` | diagnostico-capilar.html | Productos y raíces |
| ★★ | `hero-solarium.webp` | solarium.html | Foto de cabina de 1080 px ampliada |
| ★ | `hero-tratamientos.webp` | tratamientos-nutricion.html | Productos y melenas |

**Cómo usarlas:** guarda la imagen con ese nombre exacto en `assets/img/ia/` (en `.webp`; si te da PNG, pásamela y la convierto) y ejecuta `python build.py`. La cabecera de esa página la usará sola, tanto en escritorio como en móvil.

**Formato:** horizontal **16:9, 2400 × 1350 px o mayor**. El texto va encima a la izquierda, así que **el tercio izquierdo tiene que quedar oscuro, tranquilo y desenfocado**. En móvil se recorta por el centro, así que el motivo principal debe quedar en el centro o un poco a la derecha.

> Son imágenes ilustrativas generadas por IA. Cuando haya fotos reales del salón, conviene sustituirlas. No generes imágenes de Cova ni de clientas «reales»: en la web solo salen personas de verdad en sus fotos de Instagram.

---

## Estilo común (ya va incluido al final de cada prompt)

> Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

---

## 1. `hero-presoterapia.webp` · Presoterapia ★★★

> Una mujer de unos 40 años, relajada y recostada en un sillón reclinable de cuero color crema, con unas botas de presoterapia gris perla inflables que le cubren las piernas hasta los muslos. Lleva una camiseta y unos pantalones cortos de algodón en tono crudo. Tiene los ojos cerrados y una ligera sonrisa. Al fondo, muy desenfocado, un salón de peluquería con estanterías negras, una planta potos colgante y la luz cálida de una lámpara de latón. El motivo ocupa el centro y la derecha; a la izquierda, sombra profunda. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

## 2. `hero-depilacion.webp` · Depilación láser ★★★

> Primer plano elegante de unas piernas femeninas muy suaves y luminosas sobre una camilla con sábana de lino blanco roto. Una esteticista con guantes de nitrilo negros aplica un cabezal de depilación láser moderno, blanco y gris, sobre la pantorrilla. Gafas protectoras apoyadas en la camilla. Fondo de cabina estética en tonos crema y negro, con una rama verde de eucalipto. Sensación de limpieza, calma y tecnología. Sin caras visibles. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

## 3. `hero-laser-capilar.webp` · Láser capilar ★★★

> Vista de tres cuartos de una persona sentada de espaldas en un sillón de peluquería negro, con un casco de láser capilar de baja potencia sobre la cabeza que emite una suave luz roja anaranjada por su cara interior. Cabello castaño sano y brillante que cae sobre los hombros, envuelto en una capa negra. Ambiente oscuro, íntimo y tecnológico, con reflejos dorados en un espejo redondo con marco de latón. La luz roja del casco es el único punto de color intenso. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

## 4. `hero-diagnostico.webp` · Diagnóstico capilar ★★

> Las manos de una estilista sujetan una microcámara capilar de mano (tricoscopio) junto a la raíz de una melena castaña con algunas canas, y al lado una tableta muestra la imagen ampliada del cuero cabelludo con folículos y raíces muy nítidos. Sobre un tocador de madera oscura hay frascos ámbar de aceites naturales, una mascarilla en tarro de cristal y un peine de carey. Atmósfera de laboratorio artesanal: precisa pero cálida. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

## 5. `hero-solarium.webp` · Solárium ★★

> Cabina de solárium moderna y muy limpia en una sala pequeña con paredes color crema y suelo de microcemento gris cálido. La cama solar está abierta y emite una luz azul violácea suave que contrasta con la luz dorada de una lámpara de pared de latón. Hay una toalla blanca doblada y unas gafas protectoras sobre un taburete de madera, y una palmera kentia en maceta negra. Sin personas. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

## 6. `hero-tratamientos.webp` · Tratamientos de nutrición ★

> Lavacabezas negro de peluquería visto de lado: una melena larga castaña, brillante y mojada cae sobre el lavabo mientras unas manos aplican una mascarilla nutritiva cremosa color marfil. Encima del mueble hay aceites vegetales en botellas ámbar, un cuenco de cerámica con mascarilla y una toalla de lino doblada. Vapor suave. Sensación de ritual de cuidado y de calma. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

---

## Extras opcionales (para redes o para cambiar alguna otra cabecera)

### `hero-vegetal.webp` · Coloración vegetal
> Bodegón cenital sobre una mesa de madera oscura: cuencos de cerámica artesanal con polvos de henna (verde oliva), índigo (azul grisáceo), cassia (amarillo verdoso) y amla (beige), una brocha de tinte de madera, ramas de hojas frescas, un bol con la mezcla ya preparada de color cobre y un mechón de pelo cobrizo brillante enrollado. La luz natural entra por la derecha. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

### `hero-servicios.webp` · Carta de servicios
> Tocador de peluquería vintage con un espejo redondo de marco de latón, tijeras de acero, un peine de carey, una brocha de tinte y un cuenco con una mezcla color cobre, sobre una encimera de mármol crema. Al fondo hay una pared negra con un sutil patrón de rombos y una planta potos colgante. Sin personas. Fotografía editorial realista, ultra nítida, alta resolución, estética de salón de barrio cuidado y elegante con aire de barbería vintage. Paleta de negro tinta, crema hueso cálido y detalles en latón dorado envejecido, toques de verde de plantas. Luz cálida, suave y lateral, contraste profundo, poca saturación, grano fino de película. Composición panorámica 16:9 con el tercio izquierdo oscuro, limpio y desenfocado para poner texto encima. Sin texto, sin letras, sin logotipos, sin marcas de agua. Manos y anatomía perfectas.

---

## Consejos al generar
- Genera 3 o 4 variantes de cada una y elige la más natural (fíjate en las manos y en las piernas).
- Si sale texto o algún logotipo, repite añadiendo «sin ninguna letra ni texto en la imagen».
- Descarga siempre el tamaño original, sin comprimir.
- Si una imagen queda demasiado clara a la izquierda, pide «más sombra en la izquierda» o pásamela y oscurezco yo el degradado.
