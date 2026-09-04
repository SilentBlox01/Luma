# 🧠 Arquitectura de Luma (Bajo el Capó)

Luma no es un simple convertidor de ASCII. Fue diseñado para tratar el texto de la terminal como un lienzo de alta fidelidad, aplicando matemáticas de manipulación de color, interpolación sub-píxel y aceleración nativa para evadir las limitaciones de la consola clásica.

A partir de la versión **v2.1.1**, Luma implementa una **Arquitectura de Motor Dual**:
1. **Motor de Color (Python / Pillow)**: Tratamiento en espacio lineal RGB, curvas dinámicas de contraste y TrueColor ANSI de 24 bits.
2. **Motor Monocromático Nativo (C++ / `luma-mono` / `libmonochrome.so`)**: Algoritmos de entintado manga (*Ami-tone*), preservación de trazo fino, dithering ordenado y alto rendimiento.

---

## 1. El Motor de Color de Alta Fidelidad (Espacio Lineal RGB)

La mayoría de los convertidores promedian colores directamente usando los valores sRGB (0-255). Esto es un error matemático, ya que el espacio sRGB no es lineal; sumar `(100 + 200) / 2` en sRGB no produce el color medio real, sino una versión oscurecida (efecto de borde oscuro o "halo sucio").

**Solución de Luma:**
1. Luma transforma la imagen internamente.
2. Aplica algoritmos de realce fotográfico:
   - Saturación $\times 1.5$
   - Contraste $\times 1.2$
   - Nitidez $\times 1.5$
3. Convierte y procesa los sub-bloques en espacio Lineal ($C_{\text{lineal}} = C_{\text{srgb}}^{2.2}$), calculando sombras y brillos respetando la física de la luz. Cuando 8 píxeles se comprimen en un solo glifo Braille o 2 en un medio bloque, el color ANSI resultante es vivo y fiel al original.

---

## 2. El Motor Monocromático y Manga Screentone (C++ Nativo)

Para ilustraciones, manga, anime o logotipos monocromáticos, la reducción de color estándar suele empastar los trazos negros finos y destruir las tramas de sombreado. Luma resuelve esto mediante un pipeline especializado:

```
[Imagen Entrada] 
       │
       ▼
[Escala de Grises + Normalización]
       │
       ├──► [Filtro Laplaciano / Sobel] ──► Detección de Bordes (Tinta Pura)
       │
       └──► [Unsharp Masking + Dither Bayer 4x4] ──► Tramas de Semitono (Ami-tone)
       │
       ▼
[Unión de Capas: Tinta + Trama]
       │
       ▼
[Empaquetado Bit a Bit en Matriz Braille 2x4]
       │
       ▼
[Salida ANSI UTF-8]
```

- **Aceleración C++ (`monochrome.cpp`)**: Implementado en C++17 sin dependencias externas pesadas (usando `stb_image` y `stb_image_resize2`). Se compila con optimizaciones `-O3` como ejecutable `luma-mono` y como librería compartida `libmonochrome.so`.
- **Integración Transparente**: `lumart.py` detecta automáticamente si el motor nativo está disponible junto al ejecutable o en el sistema. Si no está presente, conmuta sin errores a la implementación pura de Python.

---

## 3. Selector de Motor (`-E` / `--engine`)

El CLI permite seleccionar explícitamente el pipeline deseado:
- `--engine color` (Por defecto): Ejecuta el motor a color con espacio lineal y realce.
- `--engine mono` o `--engine bw`: Desactiva la paleta cromática y optimiza para luminosidad pura.
- `--engine manga`: Activa el modo de entintado manga con tramas dither y realce de bordes.

---

## 4. Reemplazo de Color por Distancia Euclidiana (`--swap`)

El algoritmo de reemplazo de color no busca píxeles idénticos (lo cual sería inútil en imágenes con sombras o degradados). En su lugar, proyecta el color del píxel en un espacio tridimensional $(R, G, B)$:

$$ \text{Distancia} = \sqrt{(R_1 - R_2)^2 + (G_1 - G_2)^2 + (B_1 - B_2)^2} $$

Si el píxel de la imagen cae dentro de una "esfera de tolerancia" matemática alrededor del color origen, Luma lo tiñe hacia el color destino:
- Conserva el brillo y luminancia relativa original del píxel.
- Aplica el matiz del color destino.
- Mantiene las sombras y la iluminación tridimensional de la imagen sin producir manchas planas.

---

## 5. Renderizado de Sub-Píxeles (Braille y Medios Bloques)

Una terminal clásica tiene celdas cuadradas muy grandes con una relación de aspecto de celda de aproximadamente $1:2$ (el doble de alta que de ancha).

- **Modo Braille (`--braille`)**: Utiliza el bloque Unicode Braille (`\u2800` a `\u28FF`). Cada carácter Braille representa una matriz de $2 \times 4$ puntos físicos. Como $2:4 = 1:2$, la relación de aspecto de cada punto Braille individual es exactamente $1:1$ (cuadrada perfecta), cuadruplicando la resolución vertical y duplicando la horizontal.
- **Modo Bloques (`--blocks`)**: Utiliza medios bloques Unicode (`▀` y `▄`), permitiendo dibujar 2 píxeles independientes de color ANSI por cada celda de terminal.

---

## 6. Empaquetado y Distribución

1. **PyInstaller**: Congela el código Python junto al intérprete y el motor C de Pillow en un binario autónomo `dist/lumart`.
2. **Binario Nativo C++**: El script `build_packages.sh` compila `dist/luma-mono` y `dist/libmonochrome.so`.
3. **Paquetes Nativos de Linux**:
   - `.deb` (Debian, Ubuntu, Linux Mint): Instala binarios en `/usr/bin/` y librerías en `/usr/lib/`.
   - `.rpm` (Fedora, RHEL, openSUSE): Empaquetado nativo mediante `rpmbuild`.
   - `PKGBUILD` (Arch Linux): Instalación estandarizada para Pacman.
