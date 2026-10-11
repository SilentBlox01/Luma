# 📖 Manual Maestro, Guía de Uso y Solución de Problemas de Lumart (Luma) v2.5.0
> **Manual exhaustivo paso a paso: arquitectura, motores, subcomandos, enciclopedia de flags, recetas del mundo real y guía completa de resolución de problemas (Troubleshooting).**

---

## 📑 Tabla de Contenidos

- [Parte I: Fundamentos, Física del Terminal y Arquitectura](#parte-i-fundamentos-física-del-terminal-y-arquitectura)
  - [1.1 ¿Qué es Lumart?](#11-qué-es-lumart)
  - [1.2 La Física del Carácter de Terminal y el Aspect Ratio](#12-la-física-del-carácter-de-terminal-y-el-aspect-ratio)
  - [1.3 Subpíxeles Tipográficos Unicode](#13-subpíxeles-tipográficos-unicode)
  - [1.4 Color TrueColor de 24 Bits y Compresión ECMA-48](#14-color-truecolor-de-24-bits-y-compresión-ecma-48)
- [Parte II: Los Cuatro Motores Insignia](#parte-ii-los-cuatro-motores-insignia)
  - [2.1 Mary Apex 3.5 (Buque Insignia Fotorrealista Oklab)](#21-mary-apex-35-buque-insignia-fotorrealista-oklab)
  - [2.2 Trumble Orelx 2.2 (Anime Cel-Shading y Capcom CPS-2 Arcade)](#22-trumble-orelx-22-anime-cel-shading-y-capcom-cps-2-arcade)
  - [2.3 Luris Mono 2.6 (Manga Screentone, Boceto DoG y C++17)](#23-luris-mono-26-manga-screentone-boceto-dog-y-c17)
  - [2.4 Spectra Weep 2.0 (Video en Vivo, Webcam y Shaders)](#24-spectra-weep-20-video-en-vivo-webcam-y-shaders)
- [Parte III: Subcomandos y Herramientas Especializadas](#parte-iii-subcomandos-y-herramientas-especializadas)
  - [3.1 lumart fetch (Generador de Presets para Fastfetch / Neofetch)](#31-lumart-fetch)
  - [3.2 lumart bench (Banco de Pruebas de Rendimiento y Latencia)](#32-lumart-bench)
  - [3.3 lumart showcase (Lienzo Comparativo 4-en-1)](#33-lumart-showcase)
  - [3.4 lumart info (Inspector Visual y Recomendador de Motores)](#34-lumart-info)
  - [3.5 lumart diff (Comparador Cromático Delta entre Dos Imágenes)](#35-lumart-diff)
  - [3.6 lumart slideshow (Pase de Diapositivas en Terminal)](#36-lumart-slideshow)
  - [3.7 lumart -I / --interactive (Visor TUI Interactivo)](#37-lumart-i----interactive)
  - [3.8 lumart animate (Compilador y Transcodificador de GIFs)](#38-lumart-animate)
- [Parte IV: Enciclopedia Completa de Flags y Opciones](#parte-iv-enciclopedia-completa-de-flags-y-opciones)
  - [A. Motores y Texturas de Glifos](#a-motores-y-texturas-de-glifos)
  - [B. Dimensiones, Vista y Geometría](#b-dimensiones-vista-y-geometría)
  - [C. Colorimetría, Calibración y Shaders](#c-colorimetría-calibración-y-shaders)
  - [D. Animación, GIFs y Framerates](#d-animación-gifs-y-framerates)
  - [E. Exportación Gráfica, Stickers y Portapapeles](#e-exportación-gráfica-stickers-y-portapapeles)
  - [F. Transmisión de Video y Cámara Web](#f-transmisión-de-video-y-cámara-web)
  - [G. Sistema, Diagnóstico e Idiomas](#g-sistema-diagnóstico-e-idiomas)
- [Parte V: Recetas del Mundo Real y Flujos de Trabajo](#parte-v-recetas-del-mundo-real-y-flujos-de-trabajo)
  - [Receta 1: El Logo Perfecto para Fastfetch / Neofetch](#receta-1-el-logo-perfecto-para-fastfetch--neofetch)
  - [Receta 2: Stickers de Anime Transparentes para Discord / Telegram](#receta-2-stickers-de-anime-transparentes-para-discord--telegram)
  - [Receta 3: Animaciones GIF a 60 FPS sin Lag con Precarga en RAM](#receta-3-animaciones-gif-a-60-fps-sin-lag-con-precarga-en-ram)
  - [Receta 4: Cámara Web en Vivo Estilo Cyberpunk Matrix CRT](#receta-4-cámara-web-en-vivo-estilo-cyberpunk-matrix-crt)
  - [Receta 5: Automatización en Scripts Bash, Pipelines y MOTD](#receta-5-automatización-en-scripts-bash-pipelines-y-motd)
- [Parte VI: Guía Maestra de Solución de Problemas (Troubleshooting)](#parte-vi-guía-maestra-de-solución-de-problemas-troubleshooting)
  - [6.1 Tabla Rápida de Diagnóstico (Síntomas y Soluciones)](#61-tabla-rápida-de-diagnóstico-síntomas-y-soluciones)
  - [6.2 Guía Visual "Lo que se DEBE y NO se debe hacer" (Dos & Don'ts)](#62-guía-visual-lo-que-se-debe-y-no-se-debe-hacer-dos--donts)
  - [6.3 Compatibilidad de Emuladores de Terminal y Tipografías](#63-compatibilidad-de-emuladores-de-terminal-y-tipografías)
  - [6.4 Fidelidad de Color y TrueColor de 24 Bits (Tmux, Screen y SSH)](#64-fidelidad-de-color-y-truecolor-de-24-bits-tmux-screen-y-ssh)
  - [6.5 Desbordamiento de Líneas, Viewport y Proporción (--font-ratio)](#65-desbordamiento-de-líneas-viewport-y-proporción---font-ratio)
  - [6.6 Política de Stickers Transparentes y Prohibición de WebP](#66-política-de-stickers-transparentes-y-prohibición-de-webp)
  - [6.7 Rendimiento de GIFs Animados y Pérdida de FPS](#67-rendimiento-de-gifs-animados-y-pérdida-de-fps)
  - [6.8 Diagnóstico de Cámara Web y OpenCV](#68-diagnóstico-de-cámara-web-y-opencv)
  - [6.9 Compilación de Motores Nativos C++ y Diagnóstico lumart -v](#69-compilación-de-motores-nativos-c-y-diagnóstico-lumart--v)
  - [6.10 Actualizaciones, Rollback y Desinstalación Limpia](#610-actualizaciones-rollback-y-desinstalación-limpia)

---

## Parte I: Fundamentos, Física del Terminal y Arquitectura

### 1.1 ¿Qué es Lumart?
**Lumart (Luma)** es una suite de ingeniería visual avanzada para terminales modernos. Su propósito fundamental es convertir imágenes digitales, videos, transmisiones de cámara web y animaciones en arte ANSI/Unicode de altísima resolución, matemáticamente adaptado a la cuadrícula de caracteres del emulador de terminal.

A diferencia de los conversores tradicionales que simplemente reemplazan píxeles por letras ASCII toscas de una sola rampa, Lumart implementa:
1. **Espacio de color perceptual humano Oklab ($\Delta E$)**: Elimina aberraciones cromáticas y sobreexposiciones.
2. **Subpíxeles tipográficos de alta densidad**: Sextantes ($2 \times 3$), Braille ($2 \times 4$), Cuadrantes ($2 \times 2$) y Medios Bloques ($1 \times 2$).
3. **Aceleración C++17 OpenMP SIMD**: Procesa imágenes gigapíxel en milisegundos con despacho multi-núcleo.

---

### 1.2 La Física del Carácter de Terminal y el Aspect Ratio
En una pantalla gráfica normal (GPU), los píxeles son estrictamente cuadrados con relación de aspecto $1:1$. Sin embargo, en cualquier emulador de terminal (Alacritty, Kitty, Ghostty, WezTerm, Konsole, GNOME Terminal, etc.), las celdas de caracteres de texto son rectangulares: miden aproximadamente el doble de alto que de ancho (típicamente una proporción $1:2$).

Si intentas mapear píxeles directamente a caracteres de texto sin compensación, la imagen resultante se verá verticalmente estirada al doble de su altura.

* **El parámetro `--font-ratio`**: Por defecto está fijado en `0.5`, lo que compensa con precisión matemática el factor $1:2$.
* Si tu tipografía de terminal es especialmente condensada o expandida:
  ```bash
  lumart foto.png --font-ratio 0.45  # Si la fuente es muy alta y delgada
  lumart foto.png --font-ratio 0.55  # Si la fuente es más ancha o cuadrada
  ```

---

### 1.3 Subpíxeles Tipográficos Unicode

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│  Sextantes   │   Braille    │  Cuadrantes  │ Medios Bloq. │
│     2x3      │     2x4      │     2x2      │     1x2      │
├──────────────┼──────────────┼──────────────┼──────────────┤
│    🬀  🬁  🬂    │    ⠋  ⠙  ⠹    │    ▖  ▗  ▘    │    ▀   ▄     │
│ 6 subpíxeles │ 8 subpíxeles │ 4 subpíxeles │  2 subpíxel. │
│ Sólido HD    │ Curvas finas │ Bloques 2x2  │ TrueColor F/B│
└──────────────┴──────────────┴──────────────┴──────────────┘
```

* **Sextantes (`-S`)**: 6 subpíxeles por celda. Es el estándar de **Mary Apex 3.5**. Proporciona bloques completamente sólidos sin agujeros.
* **Braille (`-B`)**: 8 subpíxeles por celda. La máxima resolución geométrica para trazar siluetas, curvas vectoriales y letras pequeñas.
* **Cuadrantes (`-Q`)**: 4 subpíxeles por celda.
* **Medios Bloques (`--blocks`)**: 2 subpíxeles verticales por celda (`▀` con color foreground arriba y background abajo). Permite TrueColor 24-bit real con resolución 2x vertical. Es el formato oficial de `lumart fetch`.

---

### 1.4 Color TrueColor de 24 Bits y Compresión ECMA-48
Lumart genera secuencias de escape ANSI conformes al estándar internacional ECMA-48 en formato TrueColor (16.7 millones de colores):
* Color de texto (Foreground): `\033[38;2;R;G;Bm`
* Color de fondo (Background): `\033[48;2;R;G;Bm`

Lumart incorpora un **compresor de secuencias ANSI en tiempo real**: si dos caracteres contiguos en la misma línea comparten el mismo color, Lumart evita emitir el código de escape de color repetido, reduciendo el tamaño del archivo `.ans` o la latencia de la terminal hasta en un **65%**.

---

## Parte II: Los Cuatro Motores Insignia

### 2.1 Mary Apex 3.5 (Buque Insignia Fotorrealista Oklab)
* **Invocación:** `-E mary` (o invocación predeterminada sin flags).
* **Propósito:** Máxima fidelidad fotográfica y realismo en color.
* **Algoritmo:**
  - Convierte cada celda de píxeles al espacio de color perceptual **Oklab**.
  - Ejecuta un agrupamiento **K-Means de 3 iteraciones** acoplado a la función de sensibilidad al contraste humana (**CSF de Weber-Fechner**).
  - Determina simultáneamente el color frontal, el color de fondo y el carácter Unicode que minimiza la distancia perceptual $\Delta E$.
* **Recomendado para:** Retratos, paisajes, capturas de videojuegos realistas, fotos familiares y carátulas de álbumes.

### 2.2 Trumble Orelx 2.2 (Anime Cel-Shading y Capcom CPS-2 Arcade)
* **Invocación:** `-E trumble`
* **Propósito:** Estética retro-arcade de los años 90 (Neo-Geo, Capcom CPS-2) y cel-shading de animación japonesa.
* **Algoritmo:**
  - Aplica un filtro de convolución Laplaciana para extraer contornos de entintado nítidos estilo pluma G-Pen.
  - Satura tonos medios y ejecuta un algoritmo de *color punch* dinámico con tramado ordenado Bayer.
* **Recomendado para:** Dibujos animados, anime, sprites de pixel-art, pósteres retro e ilustraciones vectoriales.

### 2.3 Luris Mono 2.6 (Manga Screentone, Boceto DoG y C++17)
* **Invocación:** `-E luris` (o `-m`, `-s`, `-ch`, `--no-color`).
* **Propósito:** Monocromático de alta fidelidad, páginas de manga y exportación de stickers con canal alfa.
* **Modos de render:**
  - **Manga Screentone (`-m`):** Tramado de semitonos estilo revista Shonen Jump con matriz Bayer $8 \times 8$ calibrada sobre fondo de papel y tinta.
  - **Boceto a Lápiz (`-s`):** Filtro Difference of Gaussians (DoG) puro que extrae solo contornos de grafito sin manchas negras de sombra.
  - **Crosshatch (`-ch`):** Tramado cruzado auténtico a $45^\circ$ y $-45^\circ$ con 6 niveles de densidad de pluma.
  - **Stickers Transparentes (`--transparent`):** Exclusivo de Luris Mono para exportar imágenes PNG sin fondo negro.
* **Recomendado para:** Manga japonés, dotfiles minimalistas estilo Nord/Catppuccin y stickers de Discord/Telegram.

### 2.4 Spectra Weep 2.0 (Video en Vivo, Webcam y Shaders)
* **Invocación:** `-E spectra` (o `-W`, video file, `--shader <nombre>`).
* **Propósito:** Reproductor de video en terminal, streaming de cámara web a 60 FPS y shaders multiespectrales en tiempo real.
* **Shaders disponibles:**
  - `neon`: Colores cyberpunk synthwave ultra-vibrantes.
  - `thermal`: Visión infrarroja térmica militar FLIR.
  - `tron`: Líneas vectoriales brillantes en azul y cian.
  - `matrix`: Código digital y fósforo verde P1 (525nm).
  - `amber`: Terminal clásica ámbar de fósforo de los años 70.
  - `hologram`: Interferencia holográfica electromagnética.
  - `glitch`: Aberración cromática RGB con desfase aleatorio.
  - `phosphor-bloom`: Resplandor analógico difuso de tubo CRT.
* **Recomendado para:** Transmisión de webcam en directo, reproducción de clips MP4/MKV en terminal y efectos visuales de ciencia ficción.

---

## Parte III: Subcomandos y Herramientas Especializadas

### 3.1 `lumart fetch`
> **Generador de Presets para Fastfetch y Neofetch**

```bash
lumart fetch <imagen.png> [-w ANCHO]
```
1. Recorta automáticamente márgenes transparentes o vacíos (`--fastfetch`).
2. Convierte la imagen a medios bloques Unicode TrueColor de 24 bits (`▀`).
3. Guarda el archivo `.ans` en `~/.config/fastfetch/<nombre>_logo.ans`.
4. Muestra la vista previa y el fragmento JSON listo para copiar a `~/.config/fastfetch/config.jsonc`.

---

### 3.2 `lumart bench`
> **Banco de Pruebas de Rendimiento y Latencia**

```bash
lumart bench [imagen.png] [-w ANCHO]
```
Mide con precisión de microsegundos:
- Latencia de renderizado en milisegundos (`ms`).
- Throughput de procesamiento en Megapíxeles por segundo (`MP/s`).
- Tasa de refresco potencial en fotogramas por segundo (`FPS`).
Compara simultáneamente Mary Apex, Trumble Arcade, Luris Mono C++ y Spectra.

---

### 3.3 `lumart showcase`
> **Lienzo Comparativo 4-en-1**

```bash
lumart showcase <imagen.png> [-w ANCHO] [-o comparativa.png]
```
Divide la pantalla en 4 cuadrantes y renderiza la misma imagen simultáneamente:
- Arriba-Izquierda: Mary Apex 3.5 (Fotorrealista)
- Arriba-Derecha: Trumble Orelx 2.2 (Cel-shading)
- Abajo-Izquierda: Luris Mono 2.6 (Manga Screentone)
- Abajo-Derecha: Spectra Weep 2.0 (Shader Neon)

---

### 3.4 `lumart info`
> **Inspector Visual y Recomendador de Motores**

```bash
lumart info <imagen.png>
```
Analiza y reporta:
- Dimensiones nativas de píxeles, resolución y relación de aspecto.
- Luminancia media y rango dinámico.
- Paleta de los 6 colores dominantes en valores HEX y muestras de color ANSI.
- **Recomendación automática del mejor motor** para las características de esa imagen.

---

### 3.5 `lumart diff`
> **Comparador Cromático Delta entre Dos Imágenes**

```bash
lumart diff <imagen_original.png> <imagen_modificada.png> [-w ANCHO]
```
Calcula la desviación cromática píxel a píxel, genera un mapa de calor en falso color y reporta el porcentaje medio de variación Delta ($\Delta E$).

---

### 3.6 `lumart slideshow`
> **Pase de Diapositivas en la Terminal**

```bash
lumart slideshow <carpeta_imagenes/> [--delay 3.0] [-w ANCHO]
```
Proyecta todas las imágenes de una carpeta en pantalla completa con transiciones limpias y controles de teclado (`Espacio` = pausa, `Flechas` = avanzar/retroceder, `Q` = salir).

---

### 3.7 `lumart -I` / `--interactive`
> **Visor TUI Interactivo**

```bash
lumart -I <imagen.png>
```
Abre la imagen en una interfaz interactiva con controles en vivo:
- `+` / `-`: Ajustar brillo.
- `M` / `T` / `L`: Conmutar entre motores Mary, Trumble y Luris.
- `G`: Alternar modo Manga / Screentone.
- `Z`: Zoom interactivo.

---

### 3.8 `lumart animate`
> **Compilador y Transcodificador de GIFs**

```bash
lumart animate <clip.mp4 | carpeta_frames/> -o resultado.gif [--fps 30]
```
Convierte clips de video o secuencias de imágenes directamente a GIFs animados procesados mediante el pipeline de Lumart.

---

## Parte IV: Enciclopedia Completa de Flags y Opciones

### A. Motores y Texturas de Glifos

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-E`, `--engine` | `string` | *auto* | Selecciona el motor: `mary`, `trumble`, `luris`, `spectra`, `color`, `mono`, `bw`, `manga`, `sketch`, `crosshatch`. |
| `-S`, `--sextants` | `switch` | *activo* | Activa bloques Sextantes Unicode $2 \times 3$ (6 subpíxeles/celda). Predeterminado de Mary Apex. |
| `-B`, `--braille` | `switch` | `false` | Activa matriz Braille Unicode $2 \times 4$ (8 subpíxeles/celda). Máxima definición de contornos. |
| `-Q`, `--quadrants`| `switch` | `false` | Activa bloques Cuadrantes Unicode $2 \times 2$ (4 subpíxeles/celda). |
| `--blocks` | `switch` | `false` | Activa medios bloques Unicode (`▀` / `▄`, 2 píxeles verticales/celda en TrueColor de 24 bits). |
| `-m`, `--manga` | `switch` | `false` | Activa trama Manga Screentone (Bayer 8x8 halftone con entintado tradicional). |
| `-s`, `--sketch` | `switch` | `false` | Activa modo boceto limpio de líneas puras a lápiz sin manchas oscuras parásitas. |
| `-ch`, `--crosshatch`| `switch` | `false` | Activa tramado cruzado auténtico a pluma a $45^\circ$ y $-45^\circ$ con 6 niveles de densidad. |
| `-cs`, `--charset` | `string` | `standard`| Rampa tipográfica de caracteres: `dense`, `standard`, `blocks`, `math`, `runes`, `katakana`, `crosshatch`. |
| `--matrix` | `switch` | `false` | Transforma el arte en código Matrix Katakana con fósforo verde P1 (525nm). |
| `--matrix-rain` | `switch` | `false` | Modo animación de lluvia digital Matrix descendente en el terminal. |

---

### B. Dimensiones, Vista y Geometría

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-w`, `--width` | `int` | *terminal* | Ancho de salida en columnas (incompatible con `-F`). |
| `-F`, `--fit` | `switch` | `false` | **Auto-ajuste al viewport**: calcula ancho y alto óptimos para encajar exactamente en la ventana sin scroll vertical (incompatible con `-w`). |
| `--fastfetch`, `--logo`| `switch`| `false` | Recorta automáticamente márgenes transparentes o vacíos para logos compactos. |
| `--font-ratio` | `float` | `0.5` | Factor de proporción ancho/alto de la tipografía del terminal. |
| `--crop` | `string` | `None` | Recorta una región específica antes de renderizar: `--crop "x,y,ancho,alto"` (ej. `--crop "100,50,400,400"`). |
| `--zoom` | `float` | `1.0` | Factor de zoom o magnificación digital (ej. `--zoom 1.5` para 150%). |
| `--rotate` | `int` | `0` | Rotación en grados en sentido horario: `0`, `90`, `180`, `270`. |
| `--flip`, `--mirror` | `string` | `None` | Espejado geométrico: horizontal (`h`) o vertical (`v`). |
| `--border` | `string` | `None` | Enmarca el arte en un marco decorativo Unicode: `rounded`, `single`, `double`, `heavy`, `ascii`, `blocks`. |
| `--align` | `string` | `left` | Alineación horizontal en el viewport de la terminal: `left`, `center`, `right`. |
| `--center` | `switch` | `false` | Atajo rápido para `--align center`. |

---

### C. Colorimetría, Calibración y Shaders

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-c`, `--color` | `switch` | `true` | Fuerza salida en modo color TrueColor de 24 bits (por defecto: activo). |
| `--no-color` | `switch` | `false` | Desactiva el color ANSI y enruta al motor monocromático. |
| `--brightness` | `float` | `1.0` | Multiplicador de brillo (ej. `1.2` para iluminar, `0.8` para oscurecer). |
| `--contrast` | `float` | `1.0` | Multiplicador de contraste tonal (ej. `1.3` para intensificar luces y sombras). |
| `--saturation` | `float` | `1.0` | Multiplicador de saturación cromática (ej. `1.4` para colores vivos, `0.0` para escala de grises). |
| `--boost`, `--vibrant`| `switch`| `false` | Aplica curvas de saturación, contraste y realce Retinex estilo arcade de los 90. |
| `--gamma` | `float` | `1.0` | Corrección gamma no lineal de tonos medios. |
| `-i`, `--invert` | `switch` | `false` | Invierte la luminosidad de los caracteres (útil para terminales claras). |
| `--swap` | `args` | `None` | Intercambia dos colores en caliente: `--swap "#800080" "#ff69b4"`. |
| `--theme`, `--palette`| `string` | `None` | Aplica una paleta predefinida: `cyberpunk`, `dracula`, `nord`, `catppuccin`, `gruvbox`, `synthwave`, `monokai`, `gameboy`, `amber`. |
| `--crt`, `--scanlines`| `string` | `None` | Simulación analógica de monitor CRT vintage: `green`, `amber`, `color`, `scanlines`. |
| `--shader` | `string` | `None` | Shaders multiespectrales: `neon`, `cyberpunk`, `thermal`, `tron`, `matrix`, `amber`, `manga`, `hologram`, `glitch`, `phosphor-bloom`, `solarize`. |
| `-d`, `--dither` | `string` | *auto* | Algoritmo de tramado: `atkinson` (MacPaint 1984), `floyd` (Floyd-Steinberg), `bayer` (Bayer 8x8), `none`. |

---

### D. Animación, GIFs y Framerates

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--loop` | `switch` | `false` | Modo animación en bucle infinito en el terminal para archivos GIF o APNG. |
| `--fps`, `--target-fps`| `float` | *del gif* | Tasa de fotogramas objetivo para reproducción o exportación GIF (ej. `--fps 60`). |
| `--preload`, `--smooth`| `switch`| `false` | **Precarga total en RAM**: Pre-renderiza todos los fotogramas del GIF en memoria para **60 FPS fluidos con 0 ms de lag**. |
| `--instant`, `--no-reveal`| `switch`| `true` | Muestra la salida inmediatamente sin animación progresiva (por defecto). |
| `--reveal` | `switch` | `false` | Efecto nostálgico de escaneo progresivo línea por línea. |

---

### E. Exportación Gráfica, Stickers y Portapapeles

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-o`, `-O`, `--save` | `ruta` | `None` | Exporta el arte a imagen gráfica de alta resolución (`.png`, `.jpg`) o GIF animado (`.gif`). |
| `--transparent` | `switch` | `false` | **Exclusivo de Luris Mono**: genera stickers recortados con fondo 100% transparente (sin fondo negro). |
| `-r`, `--remove-bg` | `switch` | `false` | Eliminación inteligente de fondo por inundación cromática perceptual. |
| `--bg-tolerance` | `int` | `32` | Umbral de tolerancia de color para recorte de fondo (1 a 100). |
| `-C`, `--copy` | `switch` | `false` | Copia el arte ANSI (con secuencias de color) directamente al portapapeles. |
| `--copy-plain` | `switch` | `false` | Copia el texto ASCII puro y limpio (sin colores ANSI) al portapapeles. |
| `--paste` | `switch` | `false` | Lee y procesa automáticamente la imagen presente en el portapapeles (Ctrl+C). |

---

### F. Transmisión de Video y Cámara Web

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-W`, `--webcam` | `int` | `0` | Transmite vídeo de cámara web en vivo a 30-60 FPS (0 = cámara integrada, 1 = USB externa). |
| `<video.mp4>` | `archivo` | `None` | Reproduce directamente archivos de vídeo (`.mp4`, `.mkv`, `.webm`, `.mov`) en el terminal. |

---

### G. Sistema, Diagnóstico e Idiomas

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--lang` | `código` | *auto* | Configura el idioma de la interfaz (`es`, `en`, `pt`, `fr`, `ru`, `ja`, `de`, `ko` o nombres como `spanish`, `japonés`). |
| `-v`, `--version` | `switch` | `false` | Muestra el panel diagnóstico completo de hardware, SO y motores C++ nativos. |
| `-H`, `--history` | `int` | `10` | Muestra los últimos N comandos ejecutados en el historial de Lumart. |
| `-R`, `--replay` | `int` | *último* | Re-ejecuta de inmediato el comando N del historial (por defecto: el último). |
| `--clear-history` | `switch` | `false` | Vacía por completo el archivo de historial de comandos. |
| `--install-desktop` | `switch` | `false` | Registra la acción *"Abrir con Lumart"* en el menú contextual de Linux. |
| `--completions` | `shell` | `None` | Genera scripts de autocompletado para `bash`, `zsh` o `fish`. |
| `-u`, `--check-update`| `switch` | `false` | Comprueba si existe una versión más reciente en GitHub. |
| `-uu`, `--upgrade` | `opcional`| `latest` | Asistente interactivo de actualización a la última versión con backup. |
| `-dg`, `--downgrade` | `opcional`| `prev` | Selector interactivo de restauración a versiones previas. |

---

## Parte V: Recetas del Mundo Real y Flujos de Trabajo

### Receta 1: El Logo Perfecto para Fastfetch / Neofetch

#### Opción A: Bloques TrueColor de Máxima Fidelidad (Recomendada)
```bash
lumart fetch "avatar.png" -w 38
```
*Guarda en `~/.config/fastfetch/avatar_logo.ans` y proporciona el bloque JSON exacto.*

#### Opción B: Estilo Manga Monocromático para Temas Nord / Catppuccin
```bash
lumart "avatar.png" -w 38 --fastfetch -m -o ~/.config/fastfetch/logo_manga.ans
```

#### Opción C: Puntos Braille $2 \times 4$ de Alta Resolución
```bash
lumart "avatar.png" -w 38 --fastfetch -E mary -B -o ~/.config/fastfetch/logo_braille.ans
```

Para probarlo inmediatamente en tu terminal:
```bash
fastfetch --logo ~/.config/fastfetch/avatar_logo.ans --logo-type file
```

---

### Receta 2: Stickers de Anime Transparentes para Discord / Telegram
Para crear un sticker recortado con fondo 100% transparente:
```bash
lumart "personaje.png" -w 80 -m --transparent -o sticker_manga.png
```
*Si la imagen tiene fondo blanco o sólido que deseas eliminar automáticamente:*
```bash
lumart "personaje.png" -w 80 -m -r --bg-tolerance 40 --transparent -o sticker_limpio.png
```

---

### Receta 3: Animaciones GIF a 60 FPS sin Lag con Precarga en RAM
Reproducir un GIF animado en terminal sin caídas de framerate:
```bash
lumart "animacion.gif" -w 70 --loop --fps 60 --preload
```
*Para exportar la animación renderizada con una paleta Synthwave a un nuevo GIF:*
```bash
lumart "animacion.gif" -w 60 --theme synthwave --fps 30 -o anim_synthwave.gif
```

---

### Receta 4: Cámara Web en Vivo Estilo Cyberpunk Matrix CRT
Inicia tu cámara web en la terminal con lluvia digital Matrix y líneas de escaneo analógicas:
```bash
lumart -W 0 --matrix --crt green --fps 60
```
*O con visión térmica militar FLIR:*
```bash
lumart -W 0 --shader thermal --fps 30
```

---

### Receta 5: Automatización en Scripts Bash, Pipelines y MOTD

#### Generar un banner de bienvenida diario en `~/.bashrc`:
```bash
# Agregar al final de ~/.bashrc:
if command -v lumart &>/dev/null; then
    lumart ~/.config/banner.png -w 60 --border rounded --align center --instant
fi
```

#### Renderizar imágenes directamente desde una URL en internet:
```bash
lumart "https://raw.githubusercontent.com/fastfetch-cli/fastfetch/dev/assets/arch.png" -w 50
```

#### Renderizar una imagen que acabas de copiar al portapapeles:
```bash
lumart --paste -w 60 --border double
```

#### Copiar el arte ANSI generado para pegarlo en un issue o mensaje:
```bash
lumart "logo.png" -w 40 -C
```

---

## Parte VI: Guía Maestra de Solución de Problemas (Troubleshooting)

### 6.1 Tabla Rápida de Diagnóstico (Síntomas y Soluciones)

| Síntoma | Causa Principal | Solución Inmediata |
| :--- | :--- | :--- |
| `command not found: luma` o `lumart` | `~/.local/bin` no está en tu `$PATH` | Ejecuta `./install.sh` o agrega `export PATH="$HOME/.local/bin:$PATH"` a tu `~/.bashrc` / `~/.zshrc`. |
| `error: externally-managed-environment` | Restricción PEP 668 en Fedora, Debian o Ubuntu | Instala paquetes del sistema: `sudo dnf install python3-pillow` / `sudo apt install python3-pil`, o ejecuta `./install.sh`. |
| Los puntos Braille o bloques se ven como `?` o cajas vacías | La fuente activa del terminal no tiene soporte de glifos Unicode | Cambia a una **Nerd Font** (JetBrains Mono Nerd Font, FiraCode, Cascadia Code). |
| Huecos horizontales cortan las filas de caracteres Braille | El interlineado (line-height) del terminal es mayor a `1.0` | Ajusta `line-height` a `1.0` o `0px` en la configuración de tu emulador de terminal. |
| Colores apagados o bandas duras de 16 colores | El terminal no tiene activado el soporte de TrueColor de 24 bits | Comprueba `echo $COLORTERM`. Agrega `export COLORTERM=truecolor` a tu `~/.bashrc` o usa Alacritty, Kitty, Ghostty o WezTerm. |
| Las líneas se desbordan y el arte se ve torcido | El ancho especificado (`-w`) supera las columnas disponibles | Reduce con `-w 80` o usa el ajuste dinámico `-F` / `--fit`. |
| La salida en Braille o Manga se ve como un negativo fotográfico | El fondo del terminal es claro (blanco/crema) en vez de oscuro | Luris detecta fondos claros automáticamente. Para forzarlo manualmente: añade `-i` / `--invert`. |
| Mary o Luris usan el fallback de Python en vez de C++ nativo | Las librerías `.so` nativas no fueron compiladas | Instala `g++` (`build-essential` o `gcc-c++`) y ejecuta `make -f Makefile.native` o `./install.sh`. |
| Error `OpenCV required for Spectra engine` | Falta la librería `opencv-python` | Instala con `sudo dnf install python3-opencv`, `sudo apt install python3-opencv` o `pip install opencv-python`. |
| La cámara web no abre en modo Spectra (`-W`) | Permisos insuficientes o índice incorrecto de dispositivo | Añade tu usuario al grupo: `sudo usermod -aG video $USER`, o especifica el índice: `lumart -W 1`. |
| El render se ve estirado o aplastado verticalmente | La fuente del terminal tiene una proporción distinta a $1:2$ | Calibra con `--font-ratio <decimal>` (ej. `--font-ratio 0.45` o `0.55`). |
| Sticker transparente (`--transparent`) exporta fondo negro | La transparencia alfa solo está soportada en Luris Mono con `.png` | Ejecuta `lumart imagen.png -m --transparent -o sticker.png`. Los modelos en color usan fondo sólido de terminal. |
| Error al intentar exportar en formato WebP | La exportación a WebP fue eliminada definitivamente | Exporta a `.png` o `.jpg` (`-o salida.png`). |
| El idioma se mantiene en inglés a pesar del sistema | Variable de entorno local no reconocida | Fija el idioma explícitamente: `lumart --lang es` o `lumart --lang spanish`. |

---

### 6.2 Guía Visual "Lo que se DEBE y NO se debe hacer" (Dos & Don'ts)

| Aspecto | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Fotografías y TrueColor** | **SÍ** usa **Mary Apex 3.5** (`lumart foto.jpg`) para retratos y paisajes realistas con espacio Oklab y Sextantes 2x3. | **NO** fuerces `--blocks` o `--boost` en fotos delicadas a menos que busques un estilo retro saturado explícito. |
| **Arcade y Cel-Shading** | **SÍ** usa **Trumble Orelx 2.2** (`lumart arte.png -E trumble --boost`) para pósteres estilo Capcom CPS-2 / Neo-Geo. | **NO** esperes gradientes suaves de Trumble; está diseñado para líneas de cómic duras y bloques posterizados. |
| **Manga Tradicional** | **SÍ** usa **Luris Mono 2.6** (`lumart manga.jpg -m`) para tramas físicas *Ami-tone* y líneas de entintado DoG. | **NO** uses herramientas genéricas que desordenan caracteres ASCII al azar; Luris utiliza matrices de Bayer matemáticamente ordenadas. |
| **Ajuste de Pantalla** | **SÍ** usa `-F` (`--fit`) para ajustar la imagen a la ventana exacta sin scroll ni desbordamiento:<br>`lumart arte.jpg -F` | **NO** combines `-F` y `-w` en el mismo comando:<br>`lumart arte.jpg -F -w 80` ❌ *(Lumart se detendrá con error de incompatibilidad).* |
| **Fastfetch / Dashboards** | **SÍ** usa `-w 36..42` con `--fastfetch` para recortar márgenes vacíos e integrar el logo en barras laterales. | **NO** uses `-w` mayor al ancho de tu terminal, ya que forzará saltos de línea y destruirá la alineación. |
| **Stickers Transparentes** | **SÍ** usa Luris Mono con `--transparent -o sticker.png` para exportar a Discord/Telegram. | **NO** uses motores en color para stickers transparentes; los caracteres TrueColor requieren fondo de terminal sólido. |

---

### 6.3 Compatibilidad de Emuladores de Terminal y Tipografías

* **Emuladores de Rendimiento Máximo (Recomendados):**
  - **Ghostty**: Soporte nativo de GPU, TrueColor perfecto y glifos Unicode completos.
  - **Kitty**: Renderizado por GPU acelerado, excelente soporte de fuentes y secuencias de escape.
  - **Alacritty**: Motor OpenGL ultrarrápido con soporte completo de TrueColor.
  - **WezTerm**: Soporte completo de fuentes Nerd Font y renderizado de glifos complejos.
* **Emuladores de Escritorio Estándar:**
  - **GNOME Terminal / Konsole / XFCE Terminal**: Soportan TrueColor y bloques Unicode completos si se configura una Nerd Font adecuada.
* **Tipografías Recomendadas:**
  - `JetBrains Mono Nerd Font` (La más recomendada para arte ANSI y densidad geométrica).
  - `FiraCode Nerd Font`
  - `Cascadia Code Nerd Font`
  - `Hack Nerd Font`

---

### 6.4 Fidelidad de Color y TrueColor de 24 Bits (Tmux, Screen y SSH)

Si los colores se ven lavados, apagados o con bandas toscas de 16 colores:
1. Comprueba si tu terminal tiene activada la variable TrueColor:
   ```bash
   echo $COLORTERM
   ```
2. Si está vacía, añade a tu `~/.bashrc` o `~/.zshrc`:
   ```bash
   export COLORTERM=truecolor
   ```
3. **Uso dentro de Tmux**: Añade a tu `~/.tmux.conf` para permitir el paso de secuencias TrueColor de 24 bits:
   ```tmux
   set -g default-terminal "tmux-256color"
   set -ga terminal-overrides ",*256col*:Tc"
   ```

---

### 6.5 Desbordamiento de Líneas, Viewport y Proporción (`--font-ratio`)
* Si las líneas se doblan hacia abajo formando una columna partida, el ancho `-w` excede el número de columnas de tu ventana de terminal. Usa `-F` para auto-ajustar.
* Si el arte se ve aplastado o estirado verticalmente, la relación de aspecto de tu fuente no es $1:2$. Ajusta con `--font-ratio 0.45` (para fuentes altas) o `--font-ratio 0.55` (para fuentes anchas).

---

### 6.6 Política de Stickers Transparentes y Prohibición de WebP
* **Por qué los stickers transparentes son exclusivos de Luris Mono:**
  En los terminales de texto, los caracteres en color asignan tanto un color frontal como un color de fondo a la celda. Generar transparencia alfa sobre colores TrueColor crea bordes negros anti-estéticos. Luris Mono trabaja exclusivamente con tinta negra sobre canal alfa transparente, garantizando stickers PNG puros y recortados.
* **Prohibición de WebP:**
  La compresión con pérdida de WebP introduce artefactos de cuantización que arruinan la precisión subpíxel del arte ANSI. Lumart exporta exclusivamente en `.png` (lossless de alta fidelidad) o `.jpg` / `.gif`.

---

### 6.7 Rendimiento de GIFs Animados y Pérdida de FPS
* Si un GIF animado parpadea o pierde fluidez al reproducirse:
  1. Activa la **precarga total en RAM**:
     ```bash
     lumart animacion.gif -w 70 --loop --fps 60 --preload
     ```
  2. `--preload` pre-renderiza todos los fotogramas en memoria antes de comenzar, garantizando **60 FPS constantes con 0 ms de lag de I/O de disco**.

---

### 6.8 Diagnóstico de Cámara Web y OpenCV
* Si `lumart -W` o `lumart -E spectra` produce un error de importación de OpenCV:
  ```bash
  # En Fedora / RHEL:
  sudo dnf install python3-opencv
  # En Debian / Ubuntu:
  sudo apt install python3-opencv
  # O mediante pip:
  pip install opencv-python
  ```
* Si la cámara no abre, verifica los permisos del usuario para acceder al dispositivo de video:
  ```bash
  sudo usermod -aG video $USER
  ```

---

### 6.9 Compilación de Motores Nativos C++ y Diagnóstico `lumart -v`
Ejecuta en cualquier momento:
```bash
lumart -v
```
Verifica la tarjeta de diagnóstico:
- Si muestra `Mary Apex 3.5 [C++17 OpenMP]` y `Luris Mono 2.6 [C++17 OpenMP]`, tus motores nativos están funcionando a máxima aceleración SIMD por hardware.
- Si muestra `Python Fallback`, compila las librerías nativas ejecutando:
  ```bash
  g++ -O3 -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so
  g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
  ```

---

### 6.10 Actualizaciones, Rollback y Desinstalación Limpia

* **Comprobar actualizaciones en GitHub:**
  ```bash
  lumart -u
  ```
* **Actualizar a la última versión:**
  ```bash
  lumart -uu
  ```
* **Revertir a la versión anterior (Rollback):**
  ```bash
  lumart -dg
  ```
* **Desinstalación limpia:**
  ```bash
  # Si instalaste vía script o git:
  rm -rf ~/.local/bin/lumart ~/.local/bin/luma ~/.config/lumart
  # Si instalaste vía paquete:
  sudo dnf remove lumart    # Fedora
  sudo apt remove lumart    # Debian/Ubuntu
  yay -R lumart             # Arch Linux
  ```

---

*Lumart (Luma) v2.5.0 • Desarrollado con pasión para los amantes de la terminal.*
