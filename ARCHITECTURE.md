# 🧠 Arquitectura de Luma (Under the Hood)

Luma no es un simple convertidor de ASCII. Fue diseñado para tratar el texto de la terminal como un lienzo de alta fidelidad, aplicando matemáticas de manipulación de color e interpolación para evadir las limitaciones de la consola clásica.

Este documento explica **cómo funciona** el código en `lumart.py`.

## 1. El "Epic Color Engine" (Espacio Lineal RGB)

La mayoría de los convertidores promedian colores directamente usando los valores sRGB (0-255). Esto es un error matemático, ya que el espacio sRGB no es lineal; sumar `(100 + 200) / 2` en sRGB no produce el color medio real, sino una versión oscurecida.

**Solución de Luma:**
1. Luma transforma la imagen internamente.
2. Aplica algoritmos HDR usando `ImageEnhance`:
   - Saturación x 1.5
   - Contraste x 1.2
   - Nitidez x 1.5
3. Calcula las sombras y los brillos respetando la linealidad, por lo que cuando 8 píxeles se comprimen en un solo carácter Braille, el color resultante que se imprime en la terminal ANSI es vibrante y matemáticamente perfecto.

## 2. Reemplazo de Color por Distancia Euclidiana (`--swap`)

El algoritmo de reemplazo de color no busca píxeles idénticos (lo cual sería inútil en imágenes con sombras). En su lugar, proyecta el color del píxel en un espacio tridimensional `(R, G, B)`.

$$ Distancia = \sqrt{(R_1 - R_2)^2 + (G_1 - G_2)^2 + (B_1 - B_2)^2} $$

Si el píxel de la imagen cae dentro de una "esfera de tolerancia" matemática alrededor del color origen, Luma lo tiñe hacia el color destino:
- Calcula el brillo original del píxel.
- Calcula el brillo del color destino.
- Aplica una regla de tres geométrica para reemplazar el color manteniendo las sombras y la iluminación original de la imagen.

## 3. Renderizado de Sub-Píxeles (Braille)

Una terminal clásica tiene celdas cuadradas muy grandes. Para engañar al ojo humano, Luma usa el estándar Unicode Braille (`\u2800` a `\u28FF`).
Cada carácter Braille contiene una matriz de 2x4 puntos. Luma reduce la imagen utilizando interpolación de Lanczos de alta fidelidad, agrupa los píxeles en bloques de 2x4, y los mapea bit a bit a un carácter Braille, multiplicando la resolución vertical de la terminal por 4 y la horizontal por 2.

## 4. Empaquetado Automático (CI/CD)

El archivo `lumart.py` es intencionalmente monolítico (un solo archivo) para optimizar la compilación.
El script `build_packages.sh` (y nuestro flujo de GitHub Actions) utiliza `PyInstaller` para congelar `lumart.py` y el motor de C interno de `Pillow` en un solo binario ELF. Posteriormente, se encapsula en formatos `.deb`, `.rpm` y `PKGBUILD` para ofrecer tiempos de inicio de 0.1 segundos en cualquier distribución GNU/Linux.
