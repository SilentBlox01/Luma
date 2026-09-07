[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.3.0
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.3.0

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
3. [Exportación Gráfica y Política de Stickers](#exportación-gráfica-y-política-de-stickers)
4. [Idiomas Soportados (8 Idiomas)](#idiomas-soportados)
5. [Instalación Rápida y Empaquetado](#instalación)
6. [Referencia Completa de Comandos (CLI)](#referencia-completa-de-comandos)
7. [Cookbook y Ejemplos Prácticos](#cookbook-y-ejemplos-prácticos)
8. [Sistema de Actualizaciones y Rollback](#sistema-de-actualizaciones-y-rollback)
9. [Integración con el Sistema y Portapapeles](#integración-con-el-sistema)
10. [Arquitectura e Ingeniería Interna](#arquitectura-e-ingeniería-interna)
11. [Solución de Problemas y Compatibilidad](#solución-de-problemas)
12. [Licencia](#licencia)

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

## Exportación Gráfica y Política de Stickers

Lumart incorpora un rasterizador de texto terminal a imagen gráfica de ultra-alta definición (`-o imagen.png` o `-o imagen.jpg`) con resolución predeterminada de estudio de **160 columnas** ($320 \times 480$ subpíxeles en Sextantes y $320 \times 320$ en Cuadrantes).

### 1. Eliminación Permanente de WebP
* **El formato `.webp` ha sido deshabilitado permanentemente para exportación gráfica**.
* Si se intenta especificar una extensión `.webp`, Lumart rechaza la operación de forma limpia, requiriendo `.png` o `.jpg`.
* Formatos oficialmente soportados:
  * **`.png`**: Calidad sin pérdidas, compresión optimizada y soporte de canal alfa transparente.
  * **`.jpg` / `.jpeg`**: Máxima compatibilidad, calidad 95% y codificación Huffman optimizada.

### 2. Exclusividad de Stickers Transparentes para Luris Mono
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

### 1. Modificadores de Estilo y Textura
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `-m`, `--manga` | — | Transforma el arte a modo Manga Screentone 2.0 (trama Bayer 8x8 + trazos DoG). |
| `-s`, `--sketch`| — | Transforma el arte a modo Boceto limpio de líneas puras sin tramado. |
| `-B`, `--braille` | — | Renderiza mediante caracteres Braille Unicode 2x4 (8 subpíxeles por celda). |
| `-Q`, `--quadrants`| — | Renderiza mediante bloques Cuadrantes Unicode 2x2 (4 subpíxeles por celda). |
| `--blocks` | — | Renderiza mediante medios-bloques optimizados (`▀`). |

### 2. Dimensiones y Parámetros Visuales
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `-w`, `--width` | `<entero>` | Ancho de salida en columnas (por defecto: auto-ajuste al ancho de la terminal). |
| `--boost`, `--vibrant` | — | Aplica realce de saturación, contraste y curvas Retinex para salida estilo arcade vibrante. |
| `-i`, `--invert`| — | Invierte la luminosidad de los caracteres (para terminales claras; autodetección en `-m`). |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Algoritmo de tramado para simulación de gradientes. |
| `--swap` | `<color1> <color2>` | Intercambia dinámicamente un color por otro en espacio 3D RGB. |

### 3. Exportación a Imagen Gráfica y Portapapeles
| Parámetro | Argumento | Descripción |
| :--- | :--- | :--- |
| `-o`, `-O`, `--output` | `<archivo.png / .jpg>` | Rasteriza y guarda el arte en imagen gráfica de alta resolución. |
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

### 1. Arte en Alta Definición (Predeterminado sin Banderas)
```bash
# Renderiza directamente al ancho completo de tu terminal con colores naturales
lumart foto.jpg

# Ajustar un ancho personalizado en columnas
lumart retrato.png -w 110

# Realce cromático estilo arcade retro con saturación y Retinex
lumart foto.jpg --boost
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
