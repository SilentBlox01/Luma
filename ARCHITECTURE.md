# 🧠 Arquitectura de Luma (Bajo el Capó)

Luma no es un simple convertidor de ASCII. Fue diseñado para tratar el texto de la terminal como un lienzo de alta fidelidad, aplicando matemáticas de manipulación de color, interpolación sub-píxel y aceleración nativa para evadir las limitaciones de la consola clásica.

En la versión **v2.5.0 ("Apex Nova")**, Luma implementa una **Arquitectura de Cuatro Motores Especializados**:
1. **Mary Apex 3.5 (C++17 OpenMP + SIMD / Python)**: Fotorrealismo vectorial en espacio perceptual Oklab ($\Delta E$), micro-bloques sextantes 2x3 y renderizado natural continuo de máxima resolución.
2. **Trumble Orelx 2.2 (Python + OpenCV Acelerado)**: Estilo retro-arcade Capcom CPS-2 / Neo-Geo, entintado de bordes Canny subpíxel y cel-shading de alto impacto.
3. **Luris Mono 2.6 (C++17 OpenMP / `luma-mono` / `libmonochrome.so`)**: Entintado manga (*Ami-tone*), extracción de contornos por Diferencia de Gaussianas (DoG), difusión de error Atkinson y generación exclusiva de stickers transparentes PNG.
4. **Spectra Weep 2.0 ("Nova Vision") (Python + OpenCV V4L2)**: Streaming universal de vídeo local (`.mp4`, `.webm`, `.mkv`), webcams y feeds en tiempo real a 30-60 FPS con 8 shaders interactivos, 4 texturas dinámicas y exportación directa a GIF.

---

## 1. El Motor de Color de Alta Fidelidad (Espacio Lineal RGB)

La mayoría de los convertidores promedian colores directamente usando los valores sRGB (0-255). Esto es un error matemático, ya que el espacio sRGB no es lineal; sumar `(100 + 200) / 2` en sRGB no produce el color medio real, sino una versión oscurecida (efecto de borde oscuro o "halo sucio").

**Solución de Luma:**
1. Luma transforma la imagen internamente.
2. Aplica algoritmos de realce fotográfico:
   - Saturación $\times 1.25$
   - Contraste $\times 1.15$
   - Nitidez mediante máscara de desenfoque no lineal (Unsharp Mask)
3. Convierte y procesa los sub-bloques en espacio Lineal ($C_{\text{lineal}} = C_{\text{srgb}}^{2.2}$), calculando sombras y brillos respetando la física de la luz. Cuando 8 píxeles se comprimen en un solo glifo Braille o 2 en un medio bloque, el color ANSI resultante es vivo y fiel al original.

---

## 2. El Motor Monocromático y Manga Screentone 2.0 (C++ Nativo)

Para ilustraciones, manga, anime o logotipos monocromáticos, la reducción de color estándar suele empastar los trazos negros finos y destruir las tramas de sombreado. Luma resuelve esto mediante un pipeline especializado:

```
[Imagen Entrada] 
       │
       ▼
[Escala de Grises + Normalización]
       │
       ├──► [Diferencia de Gaussianas (DoG): G_0.7 - G_1.8] ──► Contornos Limpios (Tinta Pura)
       │
       ├──► [Filtro de Tonos Medios + Dither Bayer 8x8] ──────► Tramas de Semitono (Ami-tone)
       │
       └──► [Difusión de Error Bill Atkinson 1984] ──────────► Sombreado Orgánico sin Ruido
       │
       ▼
[Unión de Capas: Contornos DoG + Sombras Sólidas + Tramado]
       │
       ▼
[Empaquetado Bit a Bit en Matriz Braille 2x4 o Cuadrantes HD 2x2]
       │
       ▼
[Salida ANSI UTF-8]
```

- **Aceleración C++ (`monochrome.cpp`)**: Implementado en C++17 sin dependencias externas pesadas (usando las cabeceras libres `stb_image.h` y `stb_image_resize2.h`). Se compila con optimizaciones `-O3` como ejecutable `luma-mono` y como librería compartida `libmonochrome.so`.
- **Integración Transparente**: `lumart.py` detecta automáticamente la librería compartida mediante `ctypes` o el binario compilado. Si no están presentes en el sistema, conmuta con paridad visual idéntica a la implementación pura de Python.

---

## 3. Arquitectura Híbrida: Zero-Flag UX y Selector Explícito (`-E`)

Luma ofrece lo mejor de dos mundos: ejecución instantánea a máxima calidad sin flags para el usuario cotidiano, y control total determinista mediante flags modernas para scripting y usuarios avanzados:

### 3.1 Ejecución Directa por Defecto (Zero-Flag Baseline)
- **`lumart archivo.jpg`**: Ejecuta Mary Apex 3.5 con Unicode Sextants 2x3 (`-S`), espacio perceptual Oklab, TrueColor natural, ajuste automático al ancho del terminal y salida instantánea sin necesidad de especificar un solo parámetro.

### 3.2 Selector Explícito de Motor (`-E`, `--engine`)
Permite anular cualquier inferencia automática y seleccionar determinísticamente el motor deseado:
- **`-E mary`** (alias `-E color`): Fuerza Mary Apex 3.5 perceptual Oklab (compatible con `-S`, `-B`, `-Q`, `--blocks`).
- **`-E trumble`**: Fuerza Trumble Orelx 2.2 con paleta cel-shading arcade retro y medias sombras.
- **`-E luris`** (alias `-E mono`, `-E bw`, `-E manga`, `-E sketch`): Fuerza Luris Mono 2.6 para arte monocromático, tramas y stickers.
- **`-E spectra`**: Fuerza Spectra Weep 2.0 para captura y streaming en vivo de webcam o vídeo.

### 3.3 Enrutamiento Inteligente Contextual (sin `-E`)
Cuando no se pasa `-E`, Luma enruta inteligentemente según las flags y variables de entorno:
- Si se pasa un archivo de vídeo (`.mp4`, `.mkv`, `.webm`, etc.) o `-W` (`--webcam`) $\rightarrow$ Enruta a **Spectra Weep 2.0**.
- Si se activa `--no-color`, `-m` (`--manga`), `-s` (`--sketch`), `-d` (`--dither`), o si existe la variable `$NO_COLOR` en el entorno $\rightarrow$ Enruta automáticamente a **Luris Mono 2.6**.
- En cualquier otro caso $\rightarrow$ Enruta a **Mary Apex 3.5**.

---

## 4. Reemplazo de Color por Distancia Euclidiana (`--swap`)

El algoritmo de reemplazo de color no busca píxeles idénticos (lo cual sería inútil en imágenes con sombras o degradados). En su lugar, proyecta el color del píxel en un espacio tridimensional $(R, G, B)$:

$$ \text{Distancia} = \sqrt{(R_1 - R_2)^2 + (G_1 - G_2)^2 + (B_1 - B_2)^2} $$

Si el píxel de la imagen cae dentro de una "esfera de tolerancia" matemática alrededor del color origen, Luma lo tiñe hacia el color destino:
- Conserva el brillo y luminancia relativa original del píxel.
- Aplica el matiz del color destino.
- Mantiene las sombras y la iluminación tridimensional de la imagen sin producir manchas planas.

---

## 5. Renderizado Sub-Píxel y Geometría de Fuentes

Una terminal clásica tiene celdas rectangulares cuya relación de aspecto es aproximadamente $1:2$ (el doble de alta que de ancha). Para evitar distorsión vertical u horizontal, Luma ofrece múltiples modos geométricos:

- **Modo Sextants (`-S`, Estándar Mary Apex)**: Utiliza caracteres Unicode de bloque sextante 2x3 (`\u1FB00`–`\u1FB3B`). Divide cada celda en 6 subpíxeles continuos sólidos, proporcionando la mayor densidad de color sin perforaciones.
- **Modo Braille (`-B`, `--braille`)**: Utiliza el bloque Unicode Braille (`\u2800` a `\u28FF`). Cada carácter representa una matriz de $2 \times 4$ puntos. Como $2:4 = 1:2$, la relación de aspecto de cada punto Braille individual es exactamente $1:1$ (cuadrada).
- **Modo Cuadrantes (`-Q`, `--quadrants`)**: Utiliza caracteres Unicode 2x2 (4 subpíxeles por celda), ideal para terminales sin soporte de sextantes.
- **Modo Bloques (`--blocks`)**: Utiliza medios bloques Unicode (`▀` y `▄`), permitiendo dibujar 2 píxeles independientes de color ANSI por cada celda.
- **Calibración de Relación de Aspecto (`--font-ratio`)**: Permite ajustar con precisión el ratio ancho/alto de la celda de la terminal (por defecto `0.5`, calibrable entre `0.40` y `0.60`).

---

## 6. Empaquetado y Distribución

1. **PyInstaller**: Congela el código Python junto al intérprete y el motor C de Pillow en un binario autónomo `dist/lumart`.
2. **Binario Nativo C++**: El script `build_packages.sh` compila `dist/luma-mono` y `dist/libmonochrome.so`.
3. **Paquetes Nativos de Linux**:
   - `.deb` (Debian, Ubuntu, Linux Mint): Instala binarios en `/usr/bin/` y librerías en `/usr/lib/`.
   - `.rpm` (Fedora, RHEL, openSUSE): Empaquetado nativo mediante `rpmbuild`.
   - `PKGBUILD` (Arch Linux): Instalación estandarizada para Pacman.

---

## 7. Pipeline de Video en Tiempo Real y GIFs Animados (Zero-Lag Lazy Caching)

### 7.1 Spectra Weep 2.0: Desacoplamiento de E/S y Shaders en Caliente
Spectra Weep 2.0 opera sobre un bucle de refresco no bloqueante con sondeo asíncrono (`select.select`) a baja latencia:
- **Pipeline de Captura**: Conexión directa a hardware V4L2 o decodificadores FFmpeg/OpenCV con paso de fotogramas adaptativo según FPS objetivo.
- **8 Shaders Matemáticos**: Mapeo matricial vectorial de color (RGB $\rightarrow$ Espacio temático / Canny edge gradient / Pseudo-color térmico FLIR).
- **4 Texturas Dinámicas**: Alternancia instantánea en caliente sin reiniciar la captura (`[T]`) entre Half-blocks (`▀/▄`), Braille 2x4 (`⣿`), Glifos ASCII y Matrix Katakana.
- **Exportación Directa a GIF**: `lumart clip.mp4 -o out.gif` desacopla la reproducción en pantalla y serializa los fotogramas directamente al codificador GIF optimizado.

### 7.2 GIFs Animados: Arranque Instantáneo en 0 ms
Para evitar el retraso tradicional de pre-renderizado (que congelaba la terminal durante varios segundos antes de reproducir el primer fotograma en GIFs largos), Luma implementa **Zero-Lag Lazy Caching**:
1. **Fotograma 1 en 0 ms**: El primer fotograma se procesa y proyecta de inmediato en pantalla.
2. **Caché Progresivo**: Los fotogramas subsiguientes se renderizan bajo demanda solo en la primera pasada y se indexan en un búfer circular en memoria (`cached_arts = [None] * total_frames`).
3. **Bucle Fluido**: A partir del segundo ciclo, todos los fotogramas se leen del caché con cero uso de CPU y sincronización milimétrica al framerate original del archivo.
4. **Interactividad Completa**: Controles en caliente mediante `cbreak` (`[Espacio]` pausa, `[◄/►]` paso a paso, `[+/-]` velocidad, `[S]` captura HD, `[Q]` salida limpia).
