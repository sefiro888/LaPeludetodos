# Antes y después: cómo funciona y cómo añadir las fotos de Cova

## Qué hay ahora en la web
Hay un comparador con una barra que se desliza: a la izquierda se ve el **antes** y a la derecha el **después**. Funciona con el dedo en el móvil, con el ratón y con las flechas del teclado. Al aparecer en pantalla, la barra se mueve sola un momento para que se vea que se puede arrastrar.

Aparece en:
- **Portada**: los 3 pares, en la sección «Antes y después».
- **Galería**: los 3 pares.
- **Cada página de servicio** que tenga pares propios. Ahora mismo, coloración vegetal, mechas y alisados.

Mientras no tengamos fotos reales, salen **3 ejemplos de demostración** (fotos de Unsplash con licencia libre). Llevan la etiqueta «Ejemplo de demostración» y un aviso:

| Ejemplo | Servicio | Qué enseña |
| --- | --- | --- |
| Brillo y color con plantas | Coloración vegetal | Melena apagada → castaño con brillo (simulado sobre la misma foto) |
| Luz con balayage | Mechas y balayage | Tono uniforme → melena iluminada |
| Del encrespado al liso espejo | Alisados y keratina | Antes y después **reales** publicados en Unsplash |

**En cuanto haya un par real de un servicio, los ejemplos de ese servicio desaparecen solos.** Para quitarlos todos de golpe, pon `MOSTRAR_EJEMPLOS_AD = False` en `scripts/content.py`.

---

## Para Cova: cómo hacer las fotos (puedes reenviarle esto)

> Para que el antes y el después se puedan comparar deslizando la barra, las dos fotos tienen que estar hechas **igual**. Lo único que debe cambiar es el pelo.

1. **Mismo sitio.** Lo ideal es delante del photocall negro con el logo, que además hace marca.
2. **Misma luz.** Sin flash, y mejor siempre a la misma hora o con la misma lámpara.
3. **Misma distancia y altura.** Un truco: marca en el suelo dónde te pones tú y dónde se pone la clienta.
4. **Misma postura.** Si el antes es de espaldas, el después también. Si es de perfil, del mismo lado.
5. **En vertical** y con el móvil a la altura de la cabeza, sin inclinarlo.
6. **Sin filtros ni retoques** de Instagram. Las queremos tal cual salen.
7. **El antes, justo antes de empezar**, con el pelo suelto y peinado como viene. **El después, al terminar**, antes de que se vaya.
8. **Pide permiso a la clienta**, mejor por escrito (modelo abajo). Si prefiere no salir, hazla de espaldas o encuadra solo el pelo.

### Cómo pasármelas
- Por WhatsApp **como «Documento»** (no como foto), para que no pierdan calidad. También vale por correo.
- Con un nombre que diga qué es, por ejemplo: `vegetal-ane-antes.jpg` y `vegetal-ane-despues.jpg`.
- Y una frase de qué se hizo, por ejemplo: «Henna e índigo, dos aplicaciones. Cubría un 30 % de canas».

### Modelo de permiso (orientativo)
> Autorizo a La Pelu de Tod@s (Covadonga Izquierdo) a publicar en su página web y en sus redes sociales las fotografías de mi cabello tomadas antes y después del servicio del día ____, ☐ mostrando mi cara ☐ sin mostrar mi cara. Puedo retirar este permiso cuando quiera escribiendo al 676 67 98 07, y las fotos se retirarán.
> Nombre: __________ · Fecha: ____ · Firma: ____

*(Es un modelo orientativo. Si quieres un texto con garantías legales, que lo revise una gestoría.)*

---

## Para ti: cómo añadir un par real (2 minutos)
1. Guarda las fotos en `_fuentes/antes-despues/` con el mismo identificador:
   - `vegetal-ane-antes.jpg`
   - `vegetal-ane-despues.jpg`
2. Añade una entrada en `ANTES_DESPUES` dentro de `scripts/content.py`:
   ```python
   ANTES_DESPUES = [
       {"id": "vegetal-ane", "servicio": "coloracion-vegetal", "titulo": "Canas cubiertas con plantas",
        "texto": "Henna e índigo en dos aplicaciones. Brillo y cuerpo desde la primera."},
   ]
   ```
   Para `servicio` se usa el nombre de la página: `coloracion-vegetal`, `coloracion`, `mechas-balayage`, `colores-fantasia`, `alisados-keratina`, `rizos-permanentes`, `cortes`, `peinados-novias`, `tratamientos-nutricion`, `asesoria-imagen`, `diagnostico-capilar`…
3. Ejecuta estos dos comandos:
   ```bash
   python scripts/prepare_antes_despues.py
   ```
   ```bash
   python build.py
   ```
   El primero recorta las dos fotos a la misma proporción (vertical 4:5), iguala el tamaño y ajusta un poco el contraste para que se vean parejas.

Si añades un par nuevo con texto en castellano, ejecuta también `python scripts/i18n.py --extraer`. Los textos que falten por traducir al euskera aparecen en `i18n/pendientes-eu.txt`; mientras tanto, en la versión vasca salen en castellano.
