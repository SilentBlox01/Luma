# 📖 Manual Maestro y Guía de Uso Completa de Lumart (Luma) v2.5.0
> **Guía exhaustiva paso a paso para dominar todos los comandos, motores, subcomandos, shaders y flags de Lumart.**

---

## 📑 Tabla de Contenidos

1. [Introducción y Fundamentos](#1-introducción-y-fundamentos)
   - [¿Qué es Lumart?](#qué-es-lumart)
   - [La Física del Carácter de Terminal y el Aspect Ratio](#la-física-del-carácter-de-terminal-y-el-aspect-ratio)
   - [Soporte TrueColor de 24 Bits](#soporte-truecolor-de-24-bits)
2. [Los Cuatro Motores Insignia](#2-los-cuatro-motores-insignia)
   - [Mary Apex 3.5 (Buque Insignia Fotorrealista Oklab)](#mary-apex-35)
   - [Trumble Orelx 2.2 (Anime Cel-Shading y Capcom CPS-2 Arcade)](#trumble-orelx-22)
   - [Luris Mono 2.6 (Manga Screentone, Boceto DoG y C++17)](#luris-mono-26)
   - [Spectra Weep 2.0 (Video en Vivo, Webcam y Shaders)](#spectra-weep-20)
3. [Subcomandos y Herramientas Especializadas](#3-subcomandos-y-herramientas-especializadas)
   - [`lumart fetch` (Generador de Presets para Fastfetch / Neofetch)](#lumart-fetch)
   - [`lumart bench` (Banco de Pruebas de Rendimiento y Latencia)](#lumart-bench)
   - [`lumart showcase` (Lienzo Comparativo 4-en-1)](#lumart-showcase)
   - [`lumart info` (Inspector Visual y Recomendador de Motores)](#lumart-info)
   - [`lumart diff` (Comparador Cromático Delta entre Dos Imágenes)](#lumart-diff)
   - [`lumart slideshow` (Pase de Diapositivas Interactivo en Terminal)](#lumart-slideshow)
   - [`lumart -I / --interactive` (Visor TUI Interactivo)](#lumart-tui)
   - [`lumart animate` (Compilador de Animaciones GIF)](#lumart-animate)
4. [Enciclopedia de Flags y Opciones](#4-enciclopedia-de-flags-y-opciones)
   - [A. Motores y Texturas de Glifos](#a-motores-y-texturas-de-glifos)
   - [B. Dimensiones, Vista y Geometría](#b-dimensiones-vista-y-geometría)
   - [C. Colorimetría, Calibración y Shaders](#c-colorimetría-calibración-y-shaders)
   - [D. Animación, GIFs y Framerates](#d-animación-gifs-y-framerates)
   - [E. Exportación Gráfica, Stickers y Portapapeles](#e-exportación-gráfica-stickers-y-portapapeles)
   - [F. Transmisión de Video y Cámara Web](#f-transmisión-de-video-y-cámara-web)
   - [G. Sistema, Diagnóstico e Idiomas](#g-sistema-diagnóstico-e-idiomas)
5. [Recetas y Casos de Uso del Mundo Real](#5-recetas-y-casos-de-uso-del-mundo-real)
   - [Receta 1: El Logo Perfecto para Fastfetch / Neofetch](#receta-1-el-logo-perfecto-para-fastfetch--neofetch)
   - [Receta 2: Stickers de Anime Transparentes para Discord / Telegram](#receta-2-stickers-de-anime-transparentes-para-discord--telegram)
   - [Receta 3: Animaciones GIF a 60 FPS sin Lag con Precarga en RAM](#receta-3-animaciones-gif-a-60-fps-sin-lag-con-precarga-en-ram)
   - [Receta 4: Cámara Web en Vivo Estilo Cyberpunk Matrix CRT](#receta-4-cámara-web-en-vivo-estilo-cyberpunk-matrix-crt)
   - [Receta 5: Automatización en Scripts Bash, Pipelines y MOTD](#receta-5-automatización-en-scripts-bash-pipelines-y-motd)
6. [Solución de Problemas y Preguntas Frecuentes](#6-solución-de-problemas-y-preguntas-frecuentes)

---

## 1. Introducción y Fundamentos

### ¿Qué es Lumart?
**Lumart (Luma)** es una suite de ingeniería visual avanzada para terminales modernos. Su propósito es convertir imágenes digitales, videos, cámaras web y animaciones en arte ANSI/Unicode de altísima resolución, optimizado matemáticamente para la cuadrícula de caracteres del emulador de terminal.

A diferencia de conversores tradicionales que simplemente reemplazan píxeles por caracteres ASCII toscos, Lumart utiliza:
1. **Espacios de color perceptuales humanos (Oklab)** para evitar distorsiones lumínicas.
2. **Subpíxeles tipográficos Unicode**:
   - **Sextantes (`-S`)**: 6 subpíxeles por celda ($2 \times 3$).
   - **Braille (`-B`)**: 8 subpíxeles por celda ($2 \times 4$).
   - **Cuadrantes (`-Q`)**: 4 subpíxeles por celda ($2 \times 2$).
   - **Medios Bloques (`--blocks`)**: 2 subpíxeles verticales (`▀` / `▄`) con TrueColor independiente de fondo y frente.
3. **Aceleración C++17 nativa**: Compilada con OpenMP y vectorización SIMD para procesar millones de píxeles en milisegundos.

### La Física del Carácter de Terminal y el Aspect Ratio
En una pantalla gráfica normal, los píxeles son cuadrados ($1:1$). Sin embargo, en cualquier emulador de terminal (Alacritty, Kitty, Ghostty, WezTerm, GNOME Terminal, Konsole, etc.), los caracteres de texto son rectangulares: típicamente tienen el doble de alto que de ancho ($1:2$).

Si intentas mapear una imagen $1:1$ a caracteres sin compensación, la imagen se verá estirada verticalmente como un acordeón.

* **El parámetro `--font-ratio`**: Por defecto está calibrado a `0.5`, compensando exactamente el factor $1:2$.
* Si tu tipografía de terminal es inusualmente condensada o ancha, puedes afinarlo:
  ```bash
  lumart imagen.png --font-ratio 0.45  # Si los caracteres son muy altos
  lumart imagen.png --font-ratio 0.55  # Si los caracteres son más anchos
  ```

### Soporte TrueColor de 24 Bits
Lumart genera secuencias de escape ANSI conformes al estándar ECMA-48 en formato TrueColor de 24 bits:
- Primer plano (Foreground): `\033[38;2;R;G;Bm`
- Fondo (Background): `\033[48;2;R;G;Bm`

Lumart incorpora un **compresor ANSI inteligente**: si dos celdas contiguas comparten el mismo color, omite la reemisión de códigos de escape repetidos, reduciendo el tamaño del archivo `.ans` o el flujo de salida hasta en un **65%**.

---

## 2. Los Cuatro Motores Insignia

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MOTORES INSIGNIA DE LUMART                      │
├─────────────────┬──────────────────┬─────────────────┬─────────────────┤
│    Mary Apex    │   Trumble Orelx  │    Luris Mono   │   Spectra Weep  │
│      v3.5       │       v2.2       │      v2.6       │       v2.0      │
├─────────────────┼──────────────────┼─────────────────┼─────────────────┤
│ Fotorrealismo   │ Cel-Shading      │ Manga Screentone│ Video & Webcam  │
│ Color Oklab     │ Capcom CPS-2     │ DoG Lineart     │ Shaders en vivo │
│ Sextantes/Braille│ Bloques TrueColor│ C++17 Nativo    │ 60 FPS Streams  │
└─────────────────┴──────────────────┴─────────────────┴─────────────────┘
```

### Mary Apex 3.5
* **Bandera:** `-E mary` (o simplemente invocación predeterminada)
* **Objetivo:** Máxima precisión fotográfica y fidelidad cromática.
* **Algoritmo:**
  - Convierte cada bloque de subpíxeles al espacio de color perceptual **Oklab**.
  - Ejecuta un agrupamiento **K-Means de 3 iteraciones** con la función de sensibilidad al contraste humana (CSF de Weber-Fechner).
  - Determina simultáneamente el color de primer plano, el color de fondo y el glifo Unicode exacto que minimiza la distancia cromática $\Delta E$.
* **Cuándo usarlo:** Fotografías de paisajes, retratos, capturas de videojuegos realistas, pósteres cinematográficos y carátulas de álbumes.

### Trumble Orelx 2.2
* **Bandera:** `-E trumble`
* **Objetivo:** Ilustración retro-arcade estilo años 90 (Neo-Geo, Capcom CPS-2) y cel-shading de anime.
* **Algoritmo:**
  - Extrae contornos entintados nítidos mediante una máscara de convolución Laplaciana.
  - Satura tonos medios y aplica un algoritmo de *color punch* dinámico con tramado ordenado Bayer.
* **Cuándo usarlo:** Dibujos animados, anime, sprites de pixel-art, logotipos vectoriales y arte retro.

### Luris Mono 2.6
* **Bandera:** `-E luris` (o `-m`, `-s`, `-ch`, `--no-color`)
* **Objetivo:** Monocromático de alta fidelidad, estilo manga tradicional y estética arquitectónica.
* **Sub-modos:**
  - **Manga Screentone (`-m`):** Tramado de semitonos estilo revista Shonen Jump con matriz Bayer $8 \times 8$ sobre fondo de papel y tinta.
  - **Sketch (`-s`):** Extracción de contornos limpios a lápiz mediante filtro Difference of Gaussians (DoG) sin rellenos oscuros parásitos.
  - **Crosshatch (`-ch`):** Tramado cruzado a pluma con 6 niveles de densidad a $45^\circ$ y $-45^\circ$.
* **Cuándo usarlo:** Fondos de pantalla minimalistas, dotfiles estilo Catppuccin/Nord, manga japonés y exportación de stickers PNG transparentes (`--transparent`).

### Spectra Weep 2.0
* **Bandera:** `-E spectra` (o `-W`, `--shader <nombre>`)
* **Objetivo:** Video en tiempo real, streaming de cámara web a 60 FPS y shaders multiespectrales.
* **Shaders disponibles:**
  - `neon`: Colores cyberpunk synthwave ultra-saturados con realce de bordes.
  - `thermal`: Mapa de calor infrarrojo tipo visión térmica militar FLIR.
  - `tron`: Líneas vectoriales brillantes sobre fondo negro.
  - `matrix`: Lluvia digital y fósforo verde P1 (525nm).
  - `amber`: Terminal clásica ámbar de fósforo de los años 70/80.
  - `hologram`: Interferencia electromagnética azul cian.
  - `glitch`: Aberración cromática RGB con desfase aleatorio de fotogramas.
  - `phosphor-bloom`: Resplandor analógico difuso de tubo de rayos catódicos.
* **Cuándo usarlo:** Transmisión de webcam en directo, reproducción de clips MP4/MKV en terminal y efectos visuales de ciencia ficción.

---

## 3. Subcomandos y Herramientas Especializadas

Lumart no es solo un conversor; incluye utilidades integradas de línea de comandos:

### `lumart fetch`
> **Generador de Presets para Fastfetch y Neofetch**

```bash
lumart fetch <imagen.png> [-w ANCHO]
```

* **Qué hace:**
  1. Abre la imagen y recorta automáticamente los bordes vacíos o transparentes (`--fastfetch`).
  2. Convierte la imagen a medios bloques Unicode TrueColor de 24 bits (`▀`).
  3. Guarda el arte directamente en `~/.config/fastfetch/<nombre>_logo.ans`.
  4. Imprime una vista previa en la terminal y el bloque JSON listo para copiar y pegar en `~/.config/fastfetch/config.jsonc`.
* **Ejemplo práctico:**
  ```bash
  lumart fetch "avatar.png" -w 38
  ```
  *Salida:*
  ```jsonc
  {
      "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
      "logo": {
          "source": "/home/usuario/.config/fastfetch/avatar_logo.ans",
          "type": "file",
          "padding": {
              "top": 1,
              "right": 2
          }
      }
  }
  ```

---

### `lumart bench`
> **Banco de Pruebas de Rendimiento Comparativo**

```bash
lumart bench [imagen.png] [-w ANCHO]
```

* **Qué hace:**
  - Ejecuta una batería de pruebas de estrés sobre todos los motores (Mary Oklab, Trumble Arcade, Luris Mono C++ y Spectra).
  - Mide la latencia en milisegundos (`ms`), la tasa de procesamiento en Megapíxeles por segundo (`MP/s`) y la tasa de refresco potencial en fotogramas por segundo (`FPS`).
* **Ejemplo práctico:**
  ```bash
  lumart bench "wallpaper.jpg" -w 120
  ```

---

### `lumart showcase`
> **Lienzo Comparativo 4-en-1**

```bash
lumart showcase <imagen.png> [-w ANCHO] [-o comparativa.png]
```

* **Qué hace:**
  - Divide la pantalla en 4 cuadrantes idénticos y renderiza la misma imagen simultáneamente con los 4 motores insignia:
    - **Cuadrante Superior Izquierdo:** Mary Apex 3.5 (Fotorrealista)
    - **Cuadrante Superior Derecho:** Trumble Orelx 2.2 (Cel-shading)
    - **Cuadrante Inferior Izquierdo:** Luris Mono 2.6 (Manga Screentone)
    - **Cuadrante Inferior Derecho:** Spectra Weep 2.0 (Shader Neon)
* **Ejemplo práctico:**
  ```bash
  lumart showcase "personaje.png" -w 100 -o showcase_review.png
  ```

---

### `lumart info`
> **Inspector Visual y Análisis de Paleta**

```bash
lumart info <imagen.png>
```

* **Qué hace:**
  - Analiza dimensiones de píxeles, resolución y relación de aspecto.
  - Calcula la luminancia media y el rango dinámico.
  - Extrae los **6 colores dominantes** con sus valores hexadecimales y muestras de color ANSI reales.
  - **Recomienda automáticamente** cuál de los 4 motores producirá el mejor resultado estético para esa imagen específica.

---

### `lumart diff`
> **Comparador Cromático Delta entre Dos Imágenes**

```bash
lumart diff <imagen_original.png> <imagen_editada.png> [-w ANCHO]
```

* **Qué hace:**
  - Alinea ambas imágenes y calcula el mapa de calor de diferencias cromáticas píxel a píxel.
  - Muestra visualmente las zonas alteradas con un mapa de calor en falso color y calcula el porcentaje de variación Delta ($\Delta E$).

---

### `lumart slideshow`
> **Pase de Diapositivas en la Terminal**

```bash
lumart slideshow <carpeta_con_imagenes/> [--delay 3.0] [-w ANCHO]
```

* **Qué hace:**
  - Escanea la carpeta en busca de imágenes (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`) y las proyecta en la terminal con transiciones limpias y un intervalo configurable (por defecto `3.0` segundos).
  - Soporta controles interactivos por teclado (`Espacio` para pausar, flechas para avanzar/retroceder, `Q` para salir).

---

### `lumart -I` / `--interactive`
> **Visor TUI Interactivo**

```bash
lumart -I <imagen.png>
```

* **Qué hace:**
  - Abre la imagen en una interfaz interactiva dentro de la terminal.
  - Permite cambiar de motor (`M` para Mary, `T` para Trumble, `L` para Luris), ajustar brillo (`+` / `-`), activar modo manga (`G`), alternar shaders y hacer zoom dinámico sin reiniciar el comando.

---

### `lumart animate`
> **Compilación y Transcodificación de Animaciones GIF**

```bash
lumart animate <clip.mp4 | carpeta_frames/> -o resultado.gif [--fps 30]
```

* **Qué hace:**
  - Convierte secuencias de imágenes o archivos de video directamente en GIFs animados procesados a través del pipeline ASCII/ANSI de Lumart.

---

## 4. Enciclopedia de Flags y Opciones

### A. Motores y Texturas de Glifos

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-E`, `--engine` | `string` | *auto* | Selecciona el motor: `mary`, `trumble`, `luris`, `spectra`, `color`, `mono`, `bw`, `manga`, `sketch`, `crosshatch`. |
| `-S`, `--sextants` | `switch` | *activo* | Activa bloques Sextantes Unicode $2 \times 3$ (6 subpíxeles por celda). Predeterminado en Mary Apex. |
| `-B`, `--braille` | `switch` | `false` | Activa matriz Braille Unicode $2 \times 4$ (8 subpíxeles por celda). Ideal para líneas vectoriales finas. |
| `-Q`, `--quadrants`| `switch` | `false` | Activa bloques Cuadrantes Unicode $2 \times 2$ (4 subpíxeles por celda). |
| `--blocks` | `switch` | `false` | Activa medios bloques Unicode (`▀` / `▄`). Resolución vertical 2x con color de fondo y frente. |
| `-m`, `--manga` | `switch` | `false` | Activa trama Manga Screentone (Bayer 8x8 halftone con entintado tradicional). |
| `-s`, `--sketch` | `switch` | `false` | Activa modo boceto limpio a lápiz (Difference of Gaussians) sin manchas negras. |
| `-ch`, `--crosshatch`| `switch` | `false` | Activa tramado cruzado a pluma a $45^\circ$ y $-45^\circ$. |
| `-cs`, `--charset` | `string` | `standard`| Rampa tipográfica de caracteres: `dense`, `standard`, `blocks`, `math`, `runes`, `katakana`, `crosshatch`. |

---

### B. Dimensiones, Vista y Geometría

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-w`, `--width` | `int` | *terminal* | Ancho de la salida en columnas de caracteres. |
| `-F`, `--fit` | `switch` | `false` | **Ajuste automático al viewport**: calcula ancho y alto para caber en la ventana sin scroll. |
| `--fastfetch`, `--logo`| `switch`| `false` | Recorta automáticamente márgenes transparentes o vacíos para logos compactos. |
| `--font-ratio` | `float` | `0.5` | Factor de proporción ancho/alto de la tipografía del terminal. |
| `--crop` | `string` | `None` | Recorta una región específica: `--crop "x,y,ancho,alto"` (ej. `--crop "100,50,400,400"`). |
| `--zoom` | `float` | `1.0` | Factor de magnificación digital (ej. `--zoom 1.5` para acercar un 50%). |
| `--rotate` | `int` | `0` | Rotación en grados en sentido horario: `0`, `90`, `180`, `270`. |
| `--flip`, `--mirror` | `string` | `None` | Espejado geométrico: `h` (horizontal) o `v` (vertical). |
| `--border` | `string` | `None` | Enmarca el render con un marco decorativo: `rounded`, `single`, `double`, `heavy`, `ascii`, `blocks`. |
| `--align` | `string` | `left` | Alineación horizontal en la ventana del terminal: `left`, `center`, `right`. |
| `--center` | `switch` | `false` | Atajo rápido para `--align center`. |

---

### C. Colorimetría, Calibración y Shaders

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-c`, `--color` | `switch` | `true` | Fuerza salida en color TrueColor de 24 bits. |
| `--no-color` | `switch` | `false` | Desactiva colores ANSI y conmuta al motor monocromático. |
| `--brightness` | `float` | `1.0` | Multiplicador de brillo (ej. `1.2` para iluminar, `0.8` para oscurecer). |
| `--contrast` | `float` | `1.0` | Multiplicador de contraste tonal (ej. `1.3` para intensificar luces y sombras). |
| `--saturation` | `float` | `1.0` | Multiplicador de saturación de color (ej. `1.4` para colores vivos, `0.0` para escala de grises). |
| `--boost`, `--vibrant`| `switch`| `false` | Aplica curvas de saturación y realce Retinex estilo arcade de los 90. |
| `--gamma` | `float` | `1.0` | Corrección gamma no lineal de tonos medios. |
| `-i`, `--invert` | `switch` | `false` | Invierte la escala de luminancia (útil para terminales de fondo claro). |
| `--swap` | `args` | `None` | Intercambia dos colores en caliente: `--swap "#800080" "#ff69b4"`. |
| `--theme`, `--palette`| `string` | `None` | Aplica una paleta predefinida: `cyberpunk`, `dracula`, `nord`, `catppuccin`, `gruvbox`, `synthwave`, `monokai`, `gameboy`, `amber`. |
| `--crt`, `--scanlines`| `string` | `None` | Simulación analógica de monitor CRT: `green`, `amber`, `color`, `scanlines`. |
| `--matrix` | `switch` | `false` | Transforma el render en arte digital Matrix con fósforo verde P1 y caracteres katakana. |
| `--matrix-rain` | `switch` | `false` | Modo animación de lluvia de código Matrix descendente. |
| `--shader` | `string` | `None` | Aplica shader multiespectral: `neon`, `cyberpunk`, `thermal`, `tron`, `matrix`, `amber`, `manga`, `hologram`, `glitch`, `phosphor-bloom`, `solarize`. |
| `-d`, `--dither` | `string` | *auto* | Algoritmo de difusión de error: `atkinson` (MacPaint 1984), `floyd` (Floyd-Steinberg), `bayer` (Bayer 8x8), `none`. |

---

### D. Animación, GIFs y Framerates

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--loop` | `switch` | `false` | Modo animación en bucle infinito en el terminal para archivos GIF o APNG. |
| `--fps`, `--target-fps`| `float` | *del gif* | Especifica la tasa de fotogramas objetivo (ej. `--fps 60` o `--fps 24`). |
| `--preload`, `--smooth`| `switch`| `false` | **Precarga total en RAM**: Pre-renderiza todos los fotogramas del GIF en memoria antes de reproducir, garantizando **60 FPS fluidos con 0 ms de lag**. |
| `--instant`, `--no-reveal`| `switch`| `true` | Imprime la imagen completa instantáneamente sin animación de barrido. |
| `--reveal` | `switch` | `false` | Efecto nostálgico de barrido progresivo línea por línea. |

---

### E. Exportación Gráfica, Stickers y Portapapeles

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-o`, `-O`, `--save` | `ruta` | `None` | Exporta el resultado como imagen gráfica de alta resolución (`.png`, `.jpg`) o GIF animado (`.gif`). |
| `--transparent` | `switch` | `false` | **Exclusivo de Luris Mono**: Exporta un sticker PNG con canal alfa transparente (sin fondo negro). |
| `-r`, `--remove-bg` | `switch` | `false` | Eliminación inteligente de fondo por inundación cromática perceptual. |
| `--bg-tolerance` | `int` | `32` | Tolerancia de color para el recorte de fondo (1 a 100). |
| `-C`, `--copy` | `switch` | `false` | Copia el arte generado con sus códigos de color ANSI directamente al portapapeles del sistema. |
| `--copy-plain` | `switch` | `false` | Copia el texto ASCII puro y limpio (sin secuencias de color ANSI) al portapapeles. |
| `--paste` | `switch` | `false` | Lee y renderiza la imagen actualmente copiada en el portapapeles del sistema (Ctrl+C). |

---

### F. Transmisión de Video y Cámara Web

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-W`, `--webcam` | `int` | `0` | Inicia transmisión en directo de cámara web en la terminal (0 = cámara integrada, 1 = USB externa). |
| `<video.mp4>` | `archivo` | `None` | Reproduce directamente archivos de video (`.mp4`, `.mkv`, `.webm`, `.mov`) en la terminal con audio opcional. |

---

### G. Sistema, Diagnóstico e Idiomas

| Flag | Tipo | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--lang` | `código` | *auto* | Selecciona o persiste el idioma: `es`, `en`, `pt`, `fr`, `ru`, `ja`, `de`, `ko` (también acepta nombres como `spanish`, `japanese`, etc.). |
| `-v`, `--version` | `switch` | `false` | Muestra la ficha de diagnóstico completa del sistema, terminal, resolución y estado de los motores nativos C++. |
| `-H`, `--history` | `int` | `10` | Muestra el historial de los últimos N comandos ejecutados en Lumart. |
| `-R`, `--replay` | `int` | *último* | Re-ejecuta el comando número N del historial. |
| `--clear-history` | `switch` | `false` | Vacía el historial de comandos de Lumart. |
| `--completions` | `shell` | `None` | Genera scripts de autocompletado para `bash`, `zsh` o `fish`. |
| `-u`, `--update` | `switch` | `false` | Verifica si existe una versión más reciente publicada en GitHub. |
| `-uu`, `--upgrade` | `opcional`| `latest` | Descarga e instala automáticamente la versión más reciente desde GitHub. |
| `-dg`, `--downgrade`| `opcional`| `prev` | Revierte la instalación a la versión anterior guardada en backup. |

---

## 5. Recetas y Casos de Uso del Mundo Real

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
*Si la imagen tiene fondo blanco o sólido que quieres eliminar automáticamente:*
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

## 6. Solución de Problemas y Preguntas Frecuentes

### 1. ¿Por qué los caracteres Braille (`-B`) o Sextantes (`-S`) se ven rotos o con huecos?
* **Causa:** La tipografía de tu terminal no incluye los glifos Unicode correspondientes.
* **Solución:** Instala una fuente moderna con soporte completo de glifos, como **JetBrains Mono Nerd Font**, **FiraCode Nerd Font**, **Hack Nerd Font** o **Cascadia Code**.
* Alternativamente, usa `--blocks`, que utiliza medios bloques estándar soportados por el 100% de los terminales del mundo.

### 2. Los colores se ven apagados o con bandas extrañas
* **Causa:** Tu emulador de terminal no tiene activada la variable de entorno de TrueColor de 24 bits.
* **Solución:** Añade a tu `~/.bashrc` o `~/.zshrc`:
  ```bash
  export COLORTERM=truecolor
  ```

### 3. Las líneas de arte se desbordan o se tuercen hacia abajo
* **Causa:** El ancho especificado con `-w` es superior al número de columnas disponibles en tu ventana de terminal.
* **Solución:** Usa `-F` / `--fit` para que Lumart adapte la imagen exactamente a la ventana disponible sin desbordar.

---

*Lumart (Luma) v2.5.0 • Desarrollado con ❤️ para los apasionados de la terminal.*
