[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.4.1 (Apex Horizon)
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.4.1

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Language: Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![C++: 17 Multi-Core](https://img.shields.io/badge/C%2B%2B-17%20OpenMP%20SIMD-orange.svg)](https://isocpp.org/)
[![Platform: Linux / macOS / BSD](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20BSD-lightgrey.svg)](https://github.com/SilentBlox01/Luma)
[![8 Languages Supported](https://img.shields.io/badge/Languages-8%20Locales-purple.svg)](#idiomas-soportados)

**Lumart** es una suite visual de alta ingeniería para terminales modernas, diseñada con un único principio rector:

> **Máxima densidad visual e impacto estético en el mínimo espacio de terminal.**

A diferencia de los conversores ASCII rudimentarios que únicamente proyectan luminancias sobre caracteres alfanuméricos simples, Lumart es un compendio de **cuatro motores especializados de visión artificial y renderizado subpíxel** escritos en C++17 nativo multihilo (OpenMP) y Python optimizado. Transforma cualquier fotografía, ilustración anime, sprite de videojuego o transmisión de cámara web en vivo en una experiencia gráfica inmersiva dentro de tu emulador de terminal.

---

## Tabla de Contenido
1. [Los Cuatro Motores Insignia](#los-cuatro-motores-insignia)
   - [Mary Apex 3.5](#1-mary-apex-35-buque-insignia-fotorrealista-vectorial)
   - [Trumble Orelx 2.2](#2-trumble-orelx-22-retro-arcade--anime-cel-shading)
   - [Luris Mono 2.6](#3-luris-mono-26-manga-screentone--monocromático)
   - [Spectra Weep 1.4](#4-spectra-weep-14-cámara-web-en-vivo)
2. [Tabla Comparativa de Modelos](#tabla-comparativa-de-modelos)
3. [Galería Visual y Demostración de Resultados](#galería-visual-y-demostración-de-resultados)
4. [Exportación Gráfica, Animaciones y Política de Stickers](#exportación-gráfica-animaciones-y-política-de-stickers)
5. [Idiomas Soportados (8 Idiomas)](#idiomas-soportados)
6. [Instalación](#instalación)
7. [Referencia Completa de Comandos (CLI)](#referencia-completa-de-comandos)
8. [Cookbook y Ejemplos Prácticos](#cookbook-y-ejemplos-prácticos)
9. [Secretos de Ingeniería, Pro-Tips y Filosofía de Terminal](#secretos-de-ingeniería-pro-tips-y-filosofía-de-terminal)
10. [Sistema de Actualizaciones y Rollback](#sistema-de-actualizaciones-y-rollback)
11. [Integración con el Sistema y Portapapeles](#integración-con-el-sistema)
12. [Arquitectura e Ingeniería Interna](#arquitectura-e-ingeniería-interna)
13. [Solución de Problemas y Compatibilidad](#solución-de-problemas)
14. [Licencia](#licencia)

---

## Los Cuatro Motores Insignia

Lumart no aplica una fórmula genérica. Cada tipo de imagen posee exigencias estéticas diferentes, por lo que el sistema desacopla el renderizado en cuatro arquitecturas independientes:

```
                  ┌──────────────────────────────────────────────┐
                  │                 LUMART CLI                   │
                  └──────┬────────────┬────────────┬─────────────┘
                         │            │            │             │
        ┌────────────────┘            │            │             └────────────────┐
        ▼                             ▼            ▼                              ▼
  ┌──────────────┐             ┌──────────────┐  ┌──────────────┐          ┌──────────────┐
  │  MARY APEX   │             │TRUMBLE ORELX │  │  LURIS MONO  │          │ SPECTRA WEEP │
  │    v3.5      │             │    v2.2      │  │    v2.6      │          │     v1.4     │
  ├──────────────┤             ├──────────────┤  ├──────────────┤          ├──────────────┤
  │• C++17 OpenMP│             │• Subpixel Ink│  │• C++17 Native│          │• Live Webcam │
  │• Oklab 31-Min│             │• Capcom CPS-2│  │• DoG Lineart │          │• 30-60 FPS   │
  │• Sextants 2x3│             │• 32-bit Punch│  │• Ami-tone 8x8│          │• 5 Shaders   │
  │• Specular Fit│             │• Quad-Blocks │  │• Stickers PNG│          │• Zero-Latency│
  └──────────────┘             └──────────────┘  └──────────────┘          └──────────────┘
```

### 1. Mary Apex 3.5 (Buque Insignia Fotorrealista Vectorial)
* **Objetivo**: Máxima fidelidad de gradientes, fotografías complejas, iluminación ambiental y retratos realistas.
* **Núcleo de C++17**: Acelerado nativamente con OpenMP multi-núcleo y vectorización SIMD (`libmary.so` y ejecutable `luma-mary`).
* **Bipartición Oklab Global Exacta ($2^5 - 1 = 31$ combinaciones discretas evaluadas por celda)**: Cero trampas de mínimos locales de K-Means. Encuentra por fuerza bruta matemática el mínimo global de error perceptual ($\Delta E$) en cada celda en menos de 700 nanosegundos.
* **Filtro Guiado Rápido $O(1)$ con Realce Especular ($L > 0.82$)**: Preserva destellos brillantes en ojos, joyas, metales y reflejos mientras suaviza transiciones cromáticas continuas en tonos de piel.
* **Sextantes Unicode 2x3 por Defecto**: 6 subpíxeles por carácter terminal utilizando la tabla Unicode 13.0 (`🬀`-`🬻`, `█`, `▌`, `▐`). Soporta además Braille 2x4 dual-color (`-B`), Cuadrantes 2x2 (`-Q`) y Medios Bloques (`--blocks`).
* **Aislamiento Alfa**: Las áreas transparentes no contaminan los colores de borde, evitando halos oscuros perimetrales.
* **Exportación de Alta Definición**: Las capturas a `.png` o `.jpg` se generan sobre un lienzo de terminal (`#0c0c0c`), garantizando que la imagen conserve su naturaleza de arte terminal sin parecer una imagen comprimida.

### 2. Trumble Orelx 2.2 (Retro-Arcade & Anime Cel-Shading)
* **Objetivo**: Ilustraciones de anime, sprites de videojuegos, cómics, arte pop y composiciones de alto contraste.
* **Entintado 1-a-1 a Resolución Subpíxel (Pre-Scale)**: El remuestreo se ejecuta *antes* de aplicar el filtro bilateral y la detección de bordes Canny. De este modo, los trazos de tinta negra conservan exactamente 1 subpíxel de grosor en la resolución destino, evitando que el filtro Lanczos los borronee o mezcle con colores adyacentes.
* **Paleta Arcade Capcom CPS-2 / SNK Neo-Geo de 32 bits**: Inyección de vivacidad (+28% de saturación cromática, +15% de contraste selectivo y realce de contornos) que hace que cada personaje resalte con la fuerza de un videojuego de lucha clásico de los años 90.
* **Penalización de Forma Adaptativa**: Reducción del piso de `shape_penalty` a 30 en el motor de cuadrantes, permitiendo que glifos diagonales (`▞`, `▚`, `▘`, `▝`) sigan con total precisión las curvas del cabello y la vestimenta.

### 3. Luris Mono 2.6 (Manga Screentone & Monocromático C++17)
* **Objetivo**: Estilo cómic japonés auténtico, tinta china, bocetos a pluma y stickers transparentes.
* **Extracción de Contornos DoG (Diferencia de Gaussianas)**: Trazo de líneas nítidas sin ruido de textura, escalando de manera inteligente los radios de convolución según la resolución de la terminal.
* **Manga Screentone 2.0 (*Ami-tone*)**: Emulación de tramas mecánicas de imprenta japonesa mediante matrices de dispersión Bayer 8x8, produciendo medios tonos con blancos de papel puro y tinta negra profunda.
* **Difusión de Error Atkinson (MacPaint 1984)**: Difusión clásica de error de Bill Atkinson que retiene un 25% de energía residual para generar texturas nítidas y limpias sin el grano desordenado de Floyd-Steinberg.
* **Exclusividad de Stickers Transparentes (`--transparent`)**: Luris Mono es el **único motor autorizado para generar stickers con fondo transparente en `.png`**, garantizando que el contorno entintado destaque limpiamente sobre fondos claros u oscuros en Discord, Telegram o WhatsApp.

### 4. Spectra Weep 1.4 (Cámara Web en Vivo en la Terminal)
* **Objetivo**: Proyección interactiva de cámara web en tiempo real a 30-60 FPS directamente en la consola.
* **Cero Latencia**: Captura directa mediante V4L2/OpenCV optimizada con buffers circulares y sincronización con el refresco de la terminal.
* **5 Filtros de Gradación en Vivo**:
  1. *Normal*: TrueColor fotorrealista adaptativo.
  2. *Weep Cyberpunk*: Neón magenta y azul eléctrico estilo synthwave.
  3. *Matrix*: Lluvia digital en código de fósforo verde monocromático.
  4. *Thermal FLIR*: Gradiente térmico infrarrojo (azul frío a blanco incandescente).
  5. *Manga Ink*: Estilo de dibujo animado monocromático en tinta viva.

---

## Tabla Comparativa de Modelos

| Característica | Mary Apex 3.5 | Trumble Orelx 2.2 | Luris Mono 2.6 | Spectra Weep 1.4 |
| :--- | :--- | :--- | :--- | :--- |
| **Enfoque Estético** | Fotorrealismo Vectorial | Retro-Arcade / Cel-Shading | Manga Japonés / Tintas | Vídeo en Vivo / Streaming |
| **Lenguaje Base** | C++17 OpenMP + SIMD | Python + OpenCV Acelerado | C++17 Nativo | Python + OpenCV V4L2 |
| **Espacio de Color** | Oklab Perceptual ($\Delta E$) | RGB Arcade Capcom CPS-2 | Monocromo / Ami-tone | TrueColor / Shaders RGB |
| **Modo Predeterminado**| **Sextantes 2x3 (`-S`)** | **Cuadrantes 2x2 (`--blocks`)** | **Manga 2.0 (`-m`)** | **Streaming 30-60 FPS** |
| **Resolución Subpíxel**| Hasta 6 subpíxeles/celda | Hasta 4 subpíxeles/celda | Hasta 4 subpíxeles/celda | Dinámica según terminal |
| **Entintado de Trazos**| Anti-aliasing suave | **Canny 1-a-1 subpíxel** | **DoG Adaptativo** | Opcional (Shader Manga) |
| **Lienzo de Exportación**| Terminal Canvas (`.png`, `.jpg`)| Terminal Canvas (`.png`, `.jpg`)| **Stickers PNG (`--transparent`)**| Capturas al vuelo |
| **Comando Rápido** | `lumart img.jpg` *(Por defecto)* | `lumart img.jpg --blocks` | `lumart img.jpg -m` | `-W` o `--webcam` |

---

## Galería Visual y Demostración de Resultados

### 1. Duelo de Titanes: Mary Apex 3.5 vs Trumble Orelx 2.2
![Lumart Flagship Engines Showdown](assets/engine_showdown.png)

### 2. Comparativa Cara a Cara: Color Fotorrealista vs Stickers Manga Transparentes

| Mary Apex 3.5 (Color TrueColor Oklab) | Luris Mono 2.6 (Stickers Manga Transparentes) |
| :---: | :---: |
| ![Cinderella Mary Apex](assets/cinderella_mary_apex.png)<br><sub>`lumart cinderella.jpg` *(Mary Sextantes por defecto)*</sub> | ![Cinderella Manga Sticker](assets/cinderella_manga_sticker.png)<br><sub>`lumart cinderella.jpg -m --transparent -o sticker.png`</sub> |
| ![Hanako Mary Boosted](assets/hanako_boosted.png)<br><sub>`lumart hanako.png --boost` *(Punch Arcade Retinex)*</sub> | ![Hanako Manga Sticker](assets/hanako_manga_sticker.png)<br><sub>`lumart hanako.png -m --transparent -o sticker.png`</sub> |
| ![Gothic Nun Mary](assets/gothic_nun_mary.png)<br><sub>`lumart gothic_nun.png` *(Alto Rango Dinámico)*</sub> | ![Gothic Nun Manga Sticker](assets/gothic_nun_manga_sticker.png)<br><sub>`lumart gothic_nun.png -m --transparent -o sticker.png`</sub> |
| ![Slime Mary](assets/slime_mary.png)<br><sub>`lumart slime.png` *(Tonos de Piel Naturales)*</sub> | ![Slime Manga Sticker](assets/slime_manga_sticker.png)<br><sub>`lumart slime.png -m --transparent -o sticker.png`</sub> |

### 3. Densidades de Glifos Subpíxel

| Sextantes 2x3 (`-S` / Mary Predeterminado) | Braille 2x4 (`-B`) | Cuadrantes 2x2 (`-Q`) |
| :---: | :---: | :---: |
| ![Sextantes 2x3 Micro-bloques](assets/texture_sextants.png)<br><sub>6 subpíxeles/celda (Gradientes continuos)</sub> | ![Braille 2x4 Puntos](assets/texture_braille.png)<br><sub>8 subpíxeles/celda (Puntillismo y retratos)</sub> | ![Cuadrantes 2x2 Bloques](assets/texture_quadrants.png)<br><sub>4 subpíxeles/celda (Pixel-art y arcade)</sub> |

---

## Exportación Gráfica, Animaciones y Política de Stickers

Lumart incorpora un rasterizador de texto terminal a imagen gráfica de ultra-alta definición (`-o imagen.png`, `-o imagen.jpg` o `-o anim.gif`) con resolución predeterminada de estudio de **160 columnas** ($320 \times 480$ subpíxeles en Sextantes y $320 \times 320$ en Cuadrantes).

### 1. Modo Animación y Exportación a GIF Animado (`--loop`)
![Demostración Animada en Terminal](assets/animated_demo.gif)

Lumart v2.4.0 introduce soporte nativo para archivos de animación múltiple (GIFs y APNGs):
* **Reproducción Fluida en Terminal**: `lumart animacion.gif --loop` pre-renderiza y cachea cada frame en secuencias ANSI para una reproducción a 60 FPS sin tirones en tu ventana de terminal.
* **Compilación a GIF Animado**: `lumart animacion.gif --loop -o resultado.gif` (o `--save resultado.gif`) rasteriza cada fotograma con geometría subpíxel exacta y compila un archivo GIF animado completo.

### 2. Eliminación Permanente de WebP
* **El formato `.webp` ha sido deshabilitado permanentemente para exportación gráfica**.
* Si se intenta especificar una extensión `.webp`, Lumart rechaza la operación de forma limpia, requiriendo `.png`, `.jpg` o `.gif`.
* Formatos oficialmente soportados:
  * **`.png`**: Calidad sin pérdidas, compresión optimizada y soporte de canal alfa transparente.
  * **`.jpg` / `.jpeg`**: Máxima compatibilidad, calidad 95% y codificación Huffman optimizada.
  * **`.gif`**: Animaciones multi-frame para web o terminal.

### 3. Exclusividad de Stickers Transparentes para Luris Mono
* **¿Por qué los modelos a color no hacen stickers transparentes?**
  Al recortar un personaje a color con 160 columnas de texto sobre un fondo transparente, en un visor de imágenes tradicional la silueta pierde el marco estético de la terminal y puede dar la falsa impresión de ser una "imagen comprimida o de menor calidad". En cambio, exportada con su **lienzo oscuro de terminal (`#0c0c0c`)**, la pieza se aprecia en todo su esplendor como una obra de arte digital terminal de alta gama.
* **Stickers Manga en Blanco y Negro (Luris Mono)**:
  La opción `--transparent` es **exclusiva de Luris Mono** (`-m`, `-s`, `-d`). El tramado screentone Bayer y los trazos DoG emulan a la perfección los recortes de cómics japoneses, produciendo stickers con canal alfa puro (>95% de transparencia comprobada).
* Si se invoca `--transparent` en Mary o Trumble, Lumart emite un aviso didáctico y exporta la imagen completa preservando el lienzo terminal para mantener la máxima fidelidad cromática.

---

## Idiomas Soportados

Lumart cuenta con localización integral de fábrica en **8 idiomas**. Todos los menús de ayuda, advertencias diagnósticas, mensajes de progreso y comandos están completamente traducidos:

| Código | Idioma | Autodetección | Forzar Idioma |
| :---: | :--- | :--- | :--- |
| `es` | Español | Automática vía `$LANG=es_*` | `lumart --lang es` |
| `en` | English | Automática vía `$LANG=en_*` (por defecto) | `lumart --lang en` |
| `pt` | Português | Automática vía `$LANG=pt_*` | `lumart --lang pt` |
| `fr` | Français | Automática vía `$LANG=fr_*` | `lumart --lang fr` |
| `ru` | Русский | Automática vía `$LANG=ru_*` | `lumart --lang ru` |
| `ja` | 日本語 | Automática vía `$LANG=ja_*` | `lumart --lang ja` |
| `de` | Deutsch | Automática vía `$LANG=de_*` | `lumart --lang de` |
| `ko` | 한국어 | Automática vía `$LANG=ko_*` | `lumart --lang ko` |

---

## Instalación

### Método 1: Instalador Automático de un Solo Comando (Recomendado)
El script de instalación detecta tu distribución Linux, compila los motores nativos C++ con OpenMP y registra el comando `lumart` y `luma` en tu sistema:
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### Método 2: Instalación Local desde el Repositorio
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
chmod +x install.sh
./install.sh
```

### Método 3: Paquetes Nativos Precompilados
Descarga los paquetes binarios desde [GitHub Releases](https://github.com/SilentBlox01/Luma/releases):
* **Debian / Ubuntu / Linux Mint**: `sudo apt install ./lumart-*.deb`
* **Fedora / RHEL / AlmaLinux**: `sudo dnf install ./lumart-*.rpm`
* **Arch Linux / Manjaro**: `makepkg -si` dentro del directorio `dist/arch`

### Método 4: Construcción Manual de Paquetes
```bash
chmod +x build_packages.sh
./build_packages.sh
```

### Método 5: Compilación Manual de los Motores C++
Si deseas compilar únicamente las librerías compartidas y ejecutables nativos:
```bash
# 1. Mary Apex 3.5 (Color Perceptual Oklab)
g++ -O3 -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so
g++ -O3 -std=c++17 -fopenmp mary.cpp -o luma-mary

# 2. Luris Mono 2.6 (Monocromático y Manga)
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono
```
*(No requiere librerías externas de imágenes: incluye cabeceras integradas `stb_image.h` y `stb_image_resize2.h`)*.

---

## Referencia Completa de Comandos

```text
Uso: lumart [OPCIONES] <ruta_o_url_de_imagen>
```

### 1. Motores y Modificadores de Textura
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | Selecciona el motor de renderizado explícitamente (auto-enrutado por defecto). |
| `-S`, `--sextants`| — | Renderiza mediante bloques Sextantes Unicode 2x3 (predeterminado de Mary Apex). |
| `-B`, `--braille` | — | Renderiza mediante caracteres Braille Unicode 2x4 (8 subpíxeles por celda). |
| `-Q`, `--quadrants`| — | Renderiza mediante bloques Cuadrantes Unicode 2x2 (4 subpíxeles por celda). |
| `--blocks` | — | Renderiza mediante medios-bloques optimizados (`▀` / `▄`). |
| `-m`, `--manga` | — | Transforma el arte a modo Manga Screentone 2.0 (trama Bayer 8x8 + trazos DoG). |
| `-s`, `--sketch`| — | Transforma el arte a modo Boceto limpio de líneas puras sin tramado. |

### 2. Color, Dimensiones y Parámetros Visuales
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `-w`, `--width` | `<entero>` | Ancho de salida en columnas (incompatible con `-F`). |
| `-F`, `--fit` | — | **Auto-ajuste al viewport**: calcula ancho y alto óptimos para encajar exactamente en la ventana sin scroll vertical (incompatible con `-w`). |
| `--fastfetch`, `--logo` | — | Recorta automáticamente márgenes transparentes/vacíos para logos compactos en Fastfetch o Neofetch. |
| `-c`, `--color` | — | Fuerza salida en modo color TrueColor completo (por defecto). |
| `--no-color` | — | Desactiva el color y enruta al motor monocromático. |
| `--font-ratio` | `<decimal>`| Calibración de relación de aspecto de fuente ancho/alto (por defecto: `0.5`). |
| `--boost`, `--vibrant` | — | Aplica realce de saturación, contraste y curvas Retinex para salida estilo arcade vibrante. |
| `-i`, `--invert`| — | Invierte la luminosidad de los caracteres (para terminales claras; autodetección en `-m`). |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Algoritmo de tramado para simulación de gradientes. |
| `--swap` | `<color1> <color2>` | Intercambia dinámicamente un color por otro en espacio 3D RGB. |
| `--instant` | — | Muestra la salida inmediatamente sin animación progresiva (por defecto). |
| `--reveal` | — | Activa la animación progresiva de escaneo línea por línea. |

### 3. Exportación a Imagen Gráfica, Animaciones y Portapapeles
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `-o`, `-O`, `--output`, `--save` | `<archivo.png / .jpg / .gif>` | Rasteriza y guarda el arte en imagen de alta resolución o GIF animado. |
| `--loop` | — | **Modo animación**: reproducción fluida en terminal para GIFs/APNGs, o compilación a GIF animado (`-o salida.gif` / `--save salida.gif`). |
| `--transparent` | — | **Exclusivo de Luris Mono**: genera stickers recortados con fondo transparente. |
| `--paste` | — | Carga y procesa automáticamente la imagen presente en el portapapeles. |

### 4. Cámara Web y Efectos Especiales
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `-W`, `--webcam`| `[id]` | Transmite vídeo de cámara web en vivo a 30-60 FPS (por defecto índice `0`). |

### 5. Administración, Historial e Idioma
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `--lang` | `<código>` | Configura el idioma de la interfaz (`es`, `en`, `pt`, `fr`, `ru`, `ja`, `de`, `ko`). |
| `-H`, `--history` | `[N]` | Muestra los últimos N comandos ejecutados en el historial de Lumart. |
| `-R`, `--replay` | `[N]` | Re-ejecuta de inmediato el comando N del historial (por defecto: el último). |
| `--clear-history`| — | Vacía por completo el archivo de historial de comandos. |
| `--install-desktop` | — | Registra la acción *"Abrir con Lumart"* en el menú contextual de Linux. |
| `-v`, `--version` | — | Muestra el panel diagnóstico completo de hardware, SO y motores. |
| `-u`, `--check-update`| — | Comprueba si existe una versión más reciente en GitHub. |
| `-uu`, `--upgrade` | — | Asistente interactivo de actualización a la última versión. |
| `-dg`, `--downgrade` | `[ver]` | Selector interactivo de restauración a versiones previas. |

---

## Cookbook y Ejemplos Prácticos

### 1. Arte en Alta Definición (Predeterminado Zero-Flag o Explícito)
```bash
# Renderiza directamente al ancho completo de tu terminal con colores naturales (Zero-Flag)
lumart foto.jpg

# Invocación explícita al buque insignia (mismo resultado idéntico)
lumart foto.jpg -E mary -S

# Ajustar un ancho personalizado en columnas
lumart retrato.png -w 110

# Realce cromático estilo arcade retro con saturación y Retinex
lumart foto.jpg --boost

# Renderizado retro-arcade en bloques con Trumble
lumart anime.png -E trumble --blocks
```

### 2. Modos de Textura de Caracteres
```bash
# Puntos Braille 2x4 suaves
lumart personaje.png -B

# Bloques Cuadrantes 2x2 ultra densos
lumart personaje.png -Q

# Medios bloques estilo Capcom CPS-2 / Neo-Geo
lumart personaje.png --blocks -w 85
```

### 3. Sticker de Manga Japonés con Luris Mono
```bash
# Crear un sticker con fondo 100% transparente en formato PNG
lumart ilustracion.png -m --transparent -o sticker_manga.png

# Boceto de arquitectura a pluma limpia DoG
lumart edificio.jpg -s -w 120

# Arte con tramado ordenado Bayer
lumart poster.jpg -m -d bayer -w 100
```

### 4. Transmisión de Cámara Web en Vivo (Spectra Weep 1.4)
```bash
# Iniciar streaming inmediato de cámara web en terminal
lumart -W

# Especificar segunda cámara web externa
lumart -W 1
```

### 5. Carga desde Internet, Portapapeles o Tuberías Unix
```bash
# Cargar directamente desde una URL HTTPS
lumart https://ejemplo.com/arte.png -w 80

# Pegar la imagen que acabas de copiar con Ctrl+C
lumart --paste

# Recibir flujo binario desde la terminal
curl -sL https://ejemplo.com/foto.jpg | lumart -
```

### 6. Intercambio de Colores en Caliente
```bash
# Reemplaza dinámicamente tonos morados por rosa pastel
lumart sprite.png --blocks --swap purple pink
```

---

## Secretos de Ingeniería, Pro-Tips y Filosofía de Terminal

> *"Un gran poder de renderizado conlleva una gran responsabilidad estética."*

### 1. La Ley de Gravitación de la Proporción de Fuente (`--font-ratio`)
* **La Realidad Matemática**: En una pantalla gráfica estándar, los píxeles son perfectamente cuadrados ($1:1$). En la jungla de los emuladores de terminal, cada celda de carácter es un rascacielos rectangular alargado (típicamente de proporción $1:2$ o $0.5$).
* **El Síntoma**: Si al renderizar a tu personaje favorito parece que acaba de sobrevivir a una prensa hidráulica (aplastado) o fue estirado como chicle en una película de ciencia ficción, la culpa no es del motor de renderizado: es la geometría de tu tipografía.
* **El Remedio Pro**:
  * Fuentes esbeltas o compactas (como *Fira Code* o *JetBrains Mono* sin espaciado vertical forzado): prueba `--font-ratio 0.45` a `0.48`.
  * Fuentes anchas o monospace cuadradas: prueba `--font-ratio 0.52` a `0.58`.
  * Lumart utiliza `0.5` por defecto, lo que cubre el 90% de los terminales modernos de la galaxia.

### 2. El Teorema del Fondo Oscuro y la Excomunión de WebP
* **¿Por qué los motores de color (Mary y Trumble) se niegan rotundamente a hacer stickers transparentes?**
  * Los colores TrueColor en consola se diseñan mediante emisión lumínica aditiva sobre el negro profundo del terminal (`#0c0c0c`).
  * Si intentas "recortar" ese personaje eliminando el fondo y lo pegas en un chat de WhatsApp con fondo blanco o en un visor transparente, el contraste óptico se destruye por completo: los bordes se vuelven irregulares y parece confeti digital tras una explosión en una fábrica de impresoras.
  * **Luris Mono es el Único Profeta del Sticker**: Al trabajar con tinta pura (blanco y negro), retícula de imprenta (*Ami-tone*) y líneas vectoriales DoG, Luris genera stickers con más del 92.9% de transparencia alfa real que lucen espectaculares en Telegram, Discord o Slack.
* **La Tragedia de WebP**:
  * Durante meses vimos visores de imágenes intentar decodificar artes de terminal guardados en `.webp` y convertirlos en masas borrosas de artefactos de compresión. En la versión 2.4.0, `.webp` fue enviado al reino de las sombras. Larga vida a la **Santísima Trinidad**: `.png` (alta fidelidad y stickers), `.jpg` (fotos compactas 95%) y `.gif` (animaciones).

### 3. El Duelo Oklab: ¿Por qué Mary evalúa 31 combinaciones en 700 nanosegundos?
* En el espacio de color RGB estándar, calcular la distancia entre dos colores con la fórmula euclidiana tradicional ($\sqrt{\Delta R^2 + \Delta G^2 + \Delta B^2}$) es una mentira biológica: el ojo humano es absurdamente sensible a variaciones de verde y casi ciego a cambios sutiles en azules oscuros.
* Mary Apex traslada cada subpíxel al espacio **Oklab** ($L, a, b$) y evalúa matemáticamente **las 31 posibles particiones de color por cada celda** usando instrucciones SIMD y OpenMP en C++17 nativo.
* ¿Por qué tanta matemática para un terminal? Porque los ciclos de tu CPU son baratos, pero el arte mediocre en terminal es un delito de lesa majestad estética.

### 4. Trumble Orelx y la Regla de Oro del Cel-Shading de Arcade
* El escalado tradicional (como Lanczos o Bicúbico) promedia los colores vecinos. Si tienes una línea negra fina de 1 píxel sobre fondo blanco, Lanczos la convierte en 3 píxeles de degradados grises descoloridos y cobardes.
* Trumble Orelx invierte el orden del universo: primero reduce la imagen y **luego ejecuta la detección de bordes Canny directamente en resolución subpixel**.
* El resultado: los contornos de los ojos, el cabello y los trajes de personajes de anime o sprites de videojuegos mantienen exactamente **1 subpíxel de grosor en negro puro**, logrando ese inconfundible impacto de cartucho de arcade Capcom CPS-2 de 1996.

### 5. Los Mandamientos Sagrados del Viewport (`-F` vs `-w`)
* **Mandamiento I**: Si quieres que tu imagen encaje como un guante en la pantalla sin que tengas que usar la rueda del ratón como si estuvieras pescando, usa `-F` (`--fit`).
* **Mandamiento II**: Si vas a insertar la imagen en una barra lateral de *Fastfetch* o en un dashboard con un ancho fijo de 60 columnas, usa `-w 60 --fastfetch`.
* **Mandamiento III**: Jamás ejecutes `lumart imagen.png -F -w 80`. Pedirle a Lumart que al mismo tiempo calcule el tamaño dinámico del terminal y le fuerces un ancho fijo es una herejía lógica. Lumart detendrá la ejecución con un amable `Código 2` y una pedagógica explicación.

### 6. El Misterio del Comando `animate`
* Si estás buscando el comando `animate` y te preguntas por qué usamos `--loop`: el creador del proyecto tiene reservado el nombre `animate` para un desarrollo secreto de dimensiones superiores. No hagas preguntas cuyas respuestas tu emulador de terminal aún no pueda renderizar. Usa `--loop` y sé feliz a 60 FPS.

---

## Sistema de Actualizaciones y Rollback

Lumart incluye una suite integrada de gestión de ciclo de vida para que nunca dependas de scripts externos:

* **Comprobar Nuevas Versiones (`lumart -u`)**:
  Consulta de forma segura el repositorio oficial en GitHub e informa si tu versión está al día sin alterar ningún archivo.
* **Actualización Asistida (`lumart -uu`)**:
  Descarga y reemplaza la versión activa, compila los binarios nativos C++ y realiza una copia de seguridad automática en `~/.config/luma/backup/`.
* **Restauración y Downgrade (`lumart -dg`)**:
  ¿Una versión introdujo un comportamiento no deseado? Ejecuta `lumart -dg` para abrir un menú interactivo con todas las copias de seguridad locales y versiones publicadas de GitHub, o indica directamente la versión deseada:
  ```bash
  lumart -dg 2.2.0
  ```

---

## Integración con el Sistema

### 1. Menú Contextual del Gestor de Archivos
Ejecuta una única vez:
```bash
lumart --install-desktop
```
Esto registrará un archivo `.desktop` y un script de acción para que puedas hacer **clic derecho sobre cualquier imagen** en:
* **GNOME Files (Nautilus)**
* **KDE Dolphin**
* **Cinnamon Nemo**
* **XFCE Thunar**

Y seleccionar *"Abrir con Lumart"*, abriendo una terminal de alta definición para proyectar la imagen de inmediato.

### 2. Diagnóstico del Entorno (`lumart -v`)
Verifica en cualquier momento si tu terminal soporta TrueColor de 24 bits, la presencia de compiladores C++ y librerías dinámicas (`libmary.so`, `libmonochrome.so`), así como rutas activas de caché y copias de seguridad.

---

## Arquitectura e Ingeniería Interna

### 1. Espacio Perceptual Oklab y Optimización Discreta
Las conversiones clásicas calculan distancias Euclidianas en el espacio sRGB no lineal, causando bandas cromáticas y desaturación en tonos medios. Mary Apex 3.5 convierte cada píxel a **RGB lineal** y posteriormente a **Oklab** ($L, a, b$):

$$\Delta E = \sqrt{(L_1 - L_2)^2 + (a_1 - a_2)^2 + (b_1 - b_2)^2}$$

En cada celda de Sextantes ($2 \times 3 = 6$ subpíxeles), existen exactamente $2^5 - 1 = 31$ formas únicas de dividir los subpíxeles en dos conjuntos de color (color de primer plano y color de fondo). Mary evalúa exhaustivamente las 31 particiones, garantizando una **solución matemáticamente óptima** con cero ruido estocástico.

### 2. Entintado Subpíxel 1-a-1 de Trumble
El flujo tradicional de arte ASCII aplica filtros a la resolución completa de la imagen y luego reduce su tamaño con Lanczos. Esto provoca que las líneas oscuras de 1 píxel se mezclen con los píxeles claros vecinos, desvaneciendo el entintado. Trumble Orelx escala la imagen a la resolución exacta de subpíxeles ($target\_width \times 2$) **antes** de procesar el gradiente Canny, asegurando que cada trazo conserve su nitidez pura de 1 subpíxel.

### 3. Compresor de Secuencias de Escape ANSI ECMA-48
Lumart utiliza un buffer inteligente de emisión de caracteres que rastrea el estado de color actual (`current_fg`, `current_bg`). Si la celda adyacente comparte el mismo color, se omiten las secuencias de escape repetitivas, reduciendo el tamaño del flujo de texto en hasta un **45%** y acelerando drásticamente el renderizado por SSH o terminales lentas.

---

## Solución de Problemas

### 1. Los colores se ven apagados o distorsionados
* Asegúrate de que tu terminal soporte TrueColor (24-bit). En muchas terminales basta con exportar la variable:
  ```bash
  export COLORTERM=truecolor
  ```
* Terminales totalmente compatibles recomendadas: **Kitty**, **Alacritty**, **WezTerm**, **iTerm2**, **Foot**, **GNOME Terminal**, **Konsole**, **Windows Terminal**.

### 2. Los caracteres Sextantes (`-S`) o Braille (`-B`) se ven como cuadrados vacíos
* Tu tipografía monoespaciada carece de los bloques Unicode 13.0.
* Instala tipografías con soporte completo de símbolos:
  * **Symbols Nerd Font** / **JetBrains Mono Nerd Font**
  * **DejaVu Sans Mono**
  * **Cascadia Code**

### 3. Desinstalación Limpia
Si necesitas remover Lumart de tu sistema:
```bash
./uninstall.sh
# O si instalaste vía paquete:
sudo apt remove lumart     # Debian/Ubuntu
sudo dnf remove lumart     # Fedora
sudo pacman -Rns lumart    # Arch Linux
```

---

## Licencia

Lumart se publica bajo la Licencia Pública General de GNU Affero v3.0 (**AGPL-3.0**). Consulta el archivo `LICENSE` para conocer los términos completos de distribución y libertad de software.
