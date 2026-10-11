# 🔧 Guía Maestra de Solución de Problemas (Troubleshooting) y Manual Técnico de Lumart (Luma) v2.5.0

[English](TROUBLESHOOTING.md) | [Español (Predeterminado)](TROUBLESHOOTING.es.md) | [Português](TROUBLESHOOTING.pt.md) | [Français](TROUBLESHOOTING.fr.md) | [Deutsch](TROUBLESHOOTING.de.md) | [Русский](TROUBLESHOOTING.ru.md) | [日本語](TROUBLESHOOTING.ja.md) | [한국어](TROUBLESHOOTING.ko.md)

> **El Documento Maestro Insignia de Lumart (Luma)**: Fundamentos arquitectónicos, listas de diagnóstico rápido, guía visual "Lo que se debe y no se debe hacer", física de la grilla del terminal, inmersión técnica en los cuatro motores de renderizado, subcomandos CLI especializados, enciclopedia completa de opciones, recetas prácticas y resolución exhaustiva de problemas técnicos.

---

Bienvenido al manual operativo definitivo, referencia arquitectónica y guía de solución de problemas de **Luma** (y `lumart`). Esta guía proporciona soluciones detalladas a problemas frecuentes, pruebas de compatibilidad de emuladores de terminal, guías de compilación nativa en C++, mecánica interna de los motores de renderizado, configuración de internacionalización y arquitectura interna del sistema.

---

## 📑 Tabla de Contenidos
1. [Lista Rápida de Diagnóstico (Síntomas y Soluciones)](#1-lista-rápida-de-diagnóstico-síntomas-y-soluciones)
   - [1.1 Guía Visual "Lo que se DEBE y NO se debe hacer" (Dos & Don'ts)](#11-guía-visual-lo-que-se-debe-y-no-se-debe-hacer-dos--donts)
2. [Instalación y Resolución de Dependencias Nativas C++](#2-instalación-y-resolución-de-dependencias-nativas-c)
   - [2.1 El Instalador Universal Plug & Play](#21-el-instalador-universal-plug--play)
   - [2.2 Configuración del Compilador C++17 Nativo](#22-configuración-del-compilador-c17-nativo)
   - [2.3 Compilación Manual de Librerías de Aceleración Nativas](#23-compilación-manual-de-librerías-de-aceleración-nativas)
   - [2.4 Verificación del Estado de Motores (lumart -v)](#24-verificación-del-estado-de-motores-lumart--v)
   - [2.5 Empaquetado de Distribución y Configuración para Arch Linux / AUR (yay)](#25-empaquetado-de-distribución-y-configuración-para-arch-linux--aur-yay)
3. [Emuladores de Terminal y Compatibilidad de Tipografías](#3-emuladores-de-terminal-y-compatibilidad-de-tipografías)
   - [3.1 Matriz de Compatibilidad de Emuladores de Terminal](#31-matriz-de-compatibilidad-de-emuladores-de-terminal)
   - [3.2 Corrección de Huecos Verticales en Braille y Bloques (Ajuste de Line-Height)](#32-corrección-de-huecos-verticales-en-braille-y-bloques-ajuste-de-line-height)
   - [3.3 Tipografías Recomendadas](#33-tipografías-recomendadas)
4. [Fidelidad de Color y TrueColor de 24 Bits (ANSI ECMA-48)](#4-fidelidad-de-color-y-truecolor-de-24-bits-ansi-ecma-48)
   - [4.1 Comprobación del Soporte de TrueColor](#41-comprobación-del-soporte-de-truecolor)
   - [4.2 Mezcla Gamma en RGB Lineal vs sRGB Estándar](#42-mezcla-gamma-en-rgb-lineal-vs-srgb-estándar)
5. [Los Cuatro Motores Insignia (Inmersión Técnica y Arquitectura)](#5-los-cuatro-motores-insignia-inmersión-técnica-y-arquitectura)
   - [5.1 Mary Apex 3.5 (Color Perceptual Oklab y Micro-Bloques Subpíxel)](#51-mary-apex-35-color-perceptual-oklab-y-micro-bloques-subpíxel)
   - [5.2 Trumble Orelx 2.2 (Cel-Shading Retro-Arcade y Entintado Anime)](#52-trumble-orelx-22-cel-shading-retro-arcade-y-entintado-anime)
   - [5.3 Luris Mono 2.6 (Manga Screentone Monocromático y Stickers Transparentes)](#53-luris-mono-26-manga-screentone-monocromático-y-stickers-transparentes)
   - [5.4 Spectra Weep 2.0 (Video en Vivo, Cámara Web y 12 Shaders)](#54-spectra-weep-20-video-en-vivo-cámara-web-y-12-shaders)
6. [Subcomandos Especializados y Herramientas Integradas](#6-subcomandos-especializados-y-herramientas-integradas)
   - [6.1 lumart fetch (Generador de Presets para Fastfetch / Neofetch)](#61-lumart-fetch-generador-de-presets-para-fastfetch--neofetch)
   - [6.2 lumart bench (Banco de Pruebas de Rendimiento y Latencia Multi-Núcleo)](#62-lumart-bench-banco-de-pruebas-de-rendimiento-y-latencia-multi-núcleo)
   - [6.3 lumart showcase (Lienzo Comparativo 4-en-1)](#63-lumart-showcase-lienzo-comparativo-4-en-1)
   - [6.4 lumart info (Inspector Visual y Recomendador de Motores)](#64-lumart-info-inspector-visual-y-recomendador-de-motores)
   - [6.5 lumart diff (Mapa de Calor Cromático Delta entre Dos Imágenes)](#65-lumart-diff-mapa-de-calor-cromático-delta-entre-dos-imágenes)
   - [6.6 lumart slideshow (Pase de Diapositivas en Pantalla Completa en Terminal)](#66-lumart-slideshow-pase-de-diapositivas-en-pantalla-completa-en-terminal)
   - [6.7 lumart -I / --interactive (Visor TUI Interactivo)](#67-lumart--i----interactive-visor-tui-interactivo)
   - [6.8 lumart animate (Transcodificador de GIFs y Compilador de Video)](#68-lumart-animate-transcodificador-de-gifs-y-compilador-de-video)
7. [Dimensiones, Relación de Aspecto y Calibración de Fuente (--font-ratio)](#7-dimensiones-relación-de-aspecto-y-calibración-de-fuente---font-ratio)
   - [7.1 La Calibración de Celda de Carácter 1:2](#71-la-calibración-de-celda-de-carácter-12)
   - [7.2 Auto-Ajuste al Viewport (-F) vs Ancho Fijo (-w)](#72-auto-ajuste-al-viewport--f-vs-ancho-fijo--w)
   - [7.3 Calibración de la Relación de Aspecto de Fuente (--font-ratio)](#73-calibración-de-la-relación-de-aspecto-de-fuente---font-ratio)
8. [Exportación Gráfica de Alta Definición y Stickers (-o, --loop, --preload)](#8-exportación-gráfica-de-alta-definición-y-stickers--o---loop---preload)
   - [8.1 Exportación Gráfica de Alta Definición y Rasterización](#81-exportación-gráfica-de-alta-definición-y-rasterización)
   - [8.2 Exportación de Stickers Manga Transparentes (--transparent)](#82-exportación-de-stickers-manga-transparentes---transparent)
   - [8.3 Precarga Total en RAM y Compilación de GIFs Animados a 60 FPS](#83-precarga-total-en-ram-y-compilación-de-gifs-animados-a-60-fps)
   - [8.4 Por Qué se Eliminó la Exportación a WebP (.webp)](#84-por-qué-se-eliminó-la-exportación-a-webp-webp)
9. [Configuración, Persistencia y Localización (i18n)](#9-configuración-persistencia-y-localización-i18n)
   - [9.1 Matriz de Idiomas Soportados](#91-matriz-de-idiomas-soportados)
   - [9.2 Ajuste Persistente vs Reemplazo Efímero en Ejecución](#92-ajuste-persistente-vs-reemplazo-efímero-en-ejecución)
   - [9.3 Jerarquía Estricta de Resolución de Idioma](#93-jerarquía-estricta-de-resolución-de-idioma)
   - [9.4 Solución de Problemas de Configuración Regional (Locale)](#94-solución-de-problemas-de-configuración-regional-locale)
10. [Historial de Comandos y Reproducción Interactiva (-H, -R)](#10-historial-de-comandos-y-reproducción-interactiva--h--r)
    - [10.1 Visualización del Historial (-H / --history)](#101-visualización-del-historial--h---history)
    - [10.2 Reproducción Instantánea (-R / --replay)](#102-reproducción-instantánea--r---replay)
    - [10.3 Limpieza del Historial (--clear-history)](#103-limpieza-del-historial---clear-history)
11. [Sistema de Actualizaciones, Mejoras y Rollback (-u, -uu, -dg)](#11-sistema-de-actualizaciones-mejoras-y-rollback--u--uu--dg)
    - [11.1 Comprobación de Actualizaciones (-u / --update)](#111-comprobación-de-actualizaciones--u---update)
    - [11.2 Aplicación Atómica de Actualizaciones (-uu / --upgrade)](#112-aplicación-atómica-de-actualizaciones--uu---upgrade)
    - [11.3 Rollback / Retroceso de Versión (-dg / --downgrade)](#113-rollback--retroceso-de-versión--dg---downgrade)
12. [Integración con el Escritorio y Gestores de Archivos de Linux (--install-desktop)](#12-integración-con-el-escritorio-y-gestores-de-archivos-de-linux---install-desktop)
    - [12.1 Lanzador de Escritorio e Integración MIME](#121-lanzador-de-escritorio-e-integración-mime)
    - [12.2 Scripts para el Menú Contextual de Clic Derecho en Gestores de Archivos](#122-scripts-para-el-menú-contextual-de-clic-derecho-en-gestores-de-archivos)
13. [Recetas Prácticas del Mundo Real y Flujos de Trabajo](#13-recetas-prácticas-del-mundo-real-y-flujos-de-trabajo)
    - [13.1 Receta 1: El Logo Perfecto para la Barra Lateral de Fastfetch / Neofetch](#131-receta-1-el-logo-perfecto-para-la-barra-lateral-de-fastfetch--neofetch)
    - [13.2 Receta 2: Stickers de Anime Transparentes para Discord / Telegram](#132-receta-2-stickers-de-anime-transparentes-para-discord--telegram)
    - [13.3 Receta 3: GIFs Animados a 60 FPS con Cero Lag y Precarga en RAM](#133-receta-3-gifs-animados-a-60-fps-con-cero-lag-y-precarga-en-ram)
    - [13.4 Receta 4: Transmisión de Cámara Web en Vivo Estilo Cyberpunk Matrix CRT](#134-receta-4-transmisión-de-cámara-web-en-vivo-estilo-cyberpunk-matrix-crt)
    - [13.5 Receta 5: Automatización en Scripts Bash, Pipelines de Unix y MOTD](#135-receta-5-automatización-en-scripts-bash-pipelines-de-unix-y-motd)
14. [Enciclopedia Completa de Opciones y Flags de la Línea de Comandos](#14-enciclopedia-completa-de-opciones-y-flags-de-la-línea-de-comandos)
15. [Referencia Maestra de Comandos y Hoja de Trucos](#15-referencia-maestra-de-comandos-y-hoja-de-trucos)

---

## 1. Lista Rápida de Diagnóstico (Síntomas y Soluciones)

Si una imagen se ve distorsionada, pixelada, no se procesa o muestra caracteres extraños, consulta esta tabla rápida:

| Síntoma | Causa Principal | Solución Inmediata |
| :--- | :--- | :--- |
| `command not found: luma` o `lumart` | `~/.local/bin` no está en tu `$PATH` | Ejecuta `./install.sh` o agrega `export PATH="$HOME/.local/bin:$PATH"` a tu `~/.bashrc` / `~/.zshrc`. |
| `error: externally-managed-environment` | Restricción PEP 668 en Fedora, Debian o Ubuntu | Instala paquetes del sistema: `sudo dnf install python3-pillow` / `sudo apt install python3-pil`, o ejecuta `./install.sh`. |
| Los puntos Braille o bloques se ven como `?` o cajas vacías | La fuente activa del terminal no tiene soporte de glifos Unicode | Cambia a una **Nerd Font** (JetBrains Mono Nerd Font, FiraCode, Cascadia Code). |
| Huecos negros cortan horizontalmente los caracteres Braille | El interlineado (line-height) del terminal es mayor a `1.0` | Ajusta `line-height` a `1.0` o `0px` en la configuración de tu emulador de terminal. |
| Colores apagados o bandas toscas de 16 colores | El terminal no tiene activado el soporte de TrueColor de 24 bits | Comprueba `echo $COLORTERM`. Agrega `export COLORTERM=truecolor` a tu `~/.bashrc` o usa Ghostty, Kitty, Alacritty o WezTerm. |
| Las líneas se desbordan y el arte se ve torcido | El ancho especificado (`-w`) supera las columnas de la ventana | Reduce con `-w 80` o usa el auto-ajuste dinámico `-F` / `--fit`. |
| La salida en Braille o Manga se ve como un negativo fotográfico | El fondo del terminal es claro (blanco/crema) en vez de oscuro | Luris detecta fondos claros automáticamente. Para forzarlo manualmente: añade `-i` / `--invert`. |
| Mary o Luris usan el fallback de Python en vez de C++ nativo | Las librerías `.so` nativas no fueron compiladas | Instala `g++` (`build-essential` o `gcc-c++`) y ejecuta `make -f Makefile.native` o `./install.sh`. |
| Error `OpenCV required for Spectra engine` | Falta la librería `opencv-python` | Instala con `sudo dnf install python3-opencv`, `sudo apt install python3-opencv` o `pip install opencv-python`. |
| La cámara web no abre en modo Spectra (`-W`) | Permisos insuficientes o índice incorrecto de dispositivo | Añade tu usuario al grupo: `sudo usermod -aG video $USER`, o especifica el índice: `lumart -W 1`. |
| El render se ve estirado o aplastado verticalmente | La fuente del terminal tiene una proporción distinta a 1:2 | Calibra con `--font-ratio <decimal>` (ej. `--font-ratio 0.45` o `0.55`). Por defecto es `0.5`. |
| Sticker transparente (`--transparent`) exporta fondo negro | La transparencia alfa solo está soportada en Luris Mono con `.png` | Ejecuta `lumart imagen.png -m --transparent -o sticker.png`. Los modelos en color usan fondo sólido de terminal. |
| Error al intentar exportar en formato WebP | La exportación a WebP fue eliminada definitivamente | Exporta a `.png` o `.jpg` (`-o salida.png`). |
| El idioma se mantiene en inglés a pesar del sistema | Variable de entorno regional no reconocida | Fija el idioma explícitamente: `lumart --lang es` o `lumart --lang spanish`. |

---

## 1.1 Guía Visual "Lo que se DEBE y NO se debe hacer" (Dos & Don'ts)

Para garantizar la máxima fidelidad visual y prevenir errores operativos, sigue estos principios arquitectónicos:

### 1. Elección de Motor y Carácter Visual: Fotorrealismo vs Anime vs Manga

![Comparativa de Motores Lumart](assets/engine_showdown.png)

| Aspecto | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Fotorrealismo y TrueColor** | **SÍ** usa **Mary Apex 3.5** por defecto (`lumart foto.jpg`) para retratos, tonos de piel naturales y paisajes ricos en color. Utiliza el espacio de color perceptual Oklab ($\Delta E$) con micro-bloques Sextantes 2x3. | **NO** fuerces `--blocks` o `--boost` en fotos delicadas a menos que busques intencionalmente un aspecto retro-arcade saturado. |
| **Arcade Retro y Cel-Shading** | **SÍ** usa **Trumble Orelx 2.2** (`lumart arte.png -E trumble`) con `--boost` para pósteres vibrantes inspirados en las placas arcade Capcom CPS-2 / Neo-Geo. | **NO** esperes gradientes suaves de Trumble; está diseñado para bordes nítidos de cómic y bandas de color posterizadas. |
| **Manga Tradicional y Tinta** | **SÍ** usa **Luris Mono 2.6** (`lumart manga.jpg -m`) para recrear tramas físicas de imprenta (*Ami-tone*) y contornos limpios de tinta DoG. | **NO** uses herramientas genéricas que desordenan caracteres ASCII al azar; Luris utiliza matrices de Bayer ordenadas y difusión Atkinson. |

---

### 2. Auto-Ajuste al Viewport (`-F`) vs Ancho Fijo (`-w`)

| Principio | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Visualización Interactiva en Terminal** | **SÍ** usa `-F` (`--fit`) para que Lumart calcule ancho y alto adaptándose exactamente a tu ventana sin scroll vertical ni desbordamientos:<br>`lumart arte.jpg -F` | **NO** combines `-F` y `-w` simultáneamente:<br>`lumart arte.jpg -F -w 80` ❌<br>*Lumart se detendrá con código de error 2 explicando que el cálculo dinámico de `--fit` entra en conflicto con el ancho fijo `--width`.* |
| **Pipelining o Barras Laterales Fetch** | **SÍ** usa `-w <columnas>` al integrar en un fetch fijo (Neofetch, Fastfetch) o dashboard. Combina con `--fastfetch` para recortar márgenes vacíos. | **NO** definas `-w` mayor a las columnas de tu terminal, lo cual obligará a saltos de línea y deformará los glifos. |

---

### 3. Stickers Transparentes y Política de Transparencia Alfa

| Mary Apex 3.5 (Lienzo Sólido) | Luris Mono 2.6 (Sticker Transparente) |
| :---: | :---: |
| ![Cinderella Mary](assets/cinderella_mary_apex.png)<br><sub>**SÍ**: Exportar arte a color sobre lienzo oscuro sólido</sub> | ![Cinderella Manga Sticker](assets/cinderella_manga_sticker.png)<br><sub>**SÍ**: Exportar stickers manga con `--transparent -o .png`</sub> |

| Principio | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Stickers PNG Transparentes** | **SÍ** usa `--transparent` exclusivamente con **Luris Mono** (`-m`, `-s`, `-d`) exportando a `.png`:<br>`lumart personaje.png -m --transparent -o sticker.png`<br>Produce recortes manga con más del 90% de transparencia alfa, perfectos para Discord, Telegram y Slack. | **NO** uses `--transparent` con `-o salida.jpg`. El formato JPEG no soporta canales alfa; Lumart rechazará la operación con `[Lumart Error]`. |
| **Arte a Todo Color TrueColor** | **SÍ** exporta arte en color sobre su lienzo oscuro nativo de terminal (`#111116`):<br>`lumart foto.png -o foto_arte.png`<br>Esto preserva el contraste perceptual y evita que el texto coloreado se desvanezca fuera del terminal. | **NO** esperes que los motores a color (Mary/Trumble) recorten fondos de forma transparente; los colores del terminal requieren el fondo oscuro para el balance de luminancia. |

---

### 4. Animaciones Multi-Fotograma y Exportación de GIF (`--loop`)

![Demostración Animada en Terminal](assets/animated_demo.gif)

| Principio | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Reproducción Interactiva en Terminal** | **SÍ** ejecuta `lumart animacion.gif --loop` para reproducción interactiva a 60 FPS en tu ventana. Lumart precarga y cachea cada fotograma ANSI para bucles fluidos. Presiona `Ctrl+C` para salir limpiamente y restaurar el cursor. | **NO** ejecutes `--loop` sobre imágenes estáticas individuales esperando animación; Lumart simplemente renderizará el único cuadro. |
| **Compilación de GIFs Animados** | **SÍ** exporta animaciones completas especificando `-o anim.gif` o `--save anim.gif`:<br>`lumart anim.gif --loop -o salida.gif`<br>Lumart itera todos los cuadros, los rasteriza con precisión subpíxel y compila un nuevo GIF animado. | **NO** especifiques extensiones estáticas al usar `--loop`:<br>`lumart anim.gif --loop -o anim.png` ❌<br>*Lumart se detendrá explicando que las animaciones no pueden guardarse en imágenes estáticas individuales.* |

---

### 5. Temas Claros vs Oscuros e Inversión Automática

| Principio | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Terminales con Fondo Claro** | **SÍ** agrega `-i` (`--invert`) si usas fondos claros (Solarized Light, PaperColor). En Luris Mono (`-m`), Lumart inspecciona automáticamente los bordes y auto-invierte si detecta fondos blancos. | **NO** dejes salidas monocromáticas o Braille sin invertir en terminales blancos, o la imagen se verá como un negativo de rayos X. |

---

### 6. Selección de Glifos Subpíxel (Texturas Mutuamente Excluyentes)

| Sextantes 2x3 (`-S`) | Braille 2x4 (`-B`) | Cuadrantes 2x2 (`-Q`) |
| :---: | :---: | :---: |
| ![Sextantes](assets/texture_sextants.png)<br><sub>Micro-bloques (Predeterminado)</sub> | ![Braille](assets/texture_braille.png)<br><sub>Puntos Finos y Curvas</sub> | ![Cuadrantes](assets/texture_quadrants.png)<br><sub>Bloques Pixel-Art</sub> |

| Principio | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Elección de Modo de Textura** | **SÍ** elige el estilo de glifo subpíxel que coincida con tu objetivo estético:<br>• `-S` (Sextantes): Micro-bloques suaves, degradados continuos.<br>• `-B` (Braille): Matriz fina de puntos, retratos, contornos precisos.<br>• `-Q` (Cuadrantes): Bloques densos 2x2.<br>• `--blocks`: Medios bloques retro (`▀`/`▄`). | **NO** pases múltiples opciones de textura en el mismo comando:<br>`lumart foto.jpg -S -B -Q` ❌<br>*Lumart se detendrá de inmediato con código 2 informando que las banderas de textura son mutuamente excluyentes.* |

---

### 7. Tipografías de Terminal y Calibración de Interlineado

| Principio | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Fuente y Espaciado** | **SÍ** usa una fuente monospace Unicode moderna (JetBrains Mono Nerd Font, Fira Code, Cascadia Code) y fija el interlineado / espaciado de línea en `1.0` (o `0px`). | **NO** uses espaciados mayores a `1.0` (como `1.2` o `1.5`), ya que generarán líneas horizontales negras que cortan los glifos de Braille y Sextantes. |

---

## 2. Instalación y Resolución de Dependencias Nativas C++

Luma utiliza una arquitectura híbrida: interfaz CLI de alto nivel, gradación de color y formateo de secuencias de escape en Python 3, combinadas con librerías compartidas en C++17 ultra-optimizadas con paralelismo multihilo (`libmary.so`, `libmonochrome.so`) para los algoritmos perceptuales pesados.

### 2.1 El Instalador Universal Plug & Play
Ejecuta el instalador automatizado desde el repositorio clonado:
```bash
./install.sh
```
O ejecútalo directamente desde GitHub:
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### 2.2 Configuración del Compilador C++17 Nativo
Para lograr tiempos de renderizado inferiores a 10 milisegundos en imágenes 4K/8K, Luma compila módulos nativos en C++. Instala un compilador compatible con C++17 antes de la instalación:

- **Ubuntu / Debian / Linux Mint / Pop!_OS**:
  ```bash
  sudo apt update && sudo apt install -y build-essential g++ libgomp1 python3-pil
  ```
- **Fedora / RHEL / Rocky Linux / AlmaLinux**:
  ```bash
  sudo dnf install -y gcc-c++ make libgomp python3-pillow
  ```
- **Arch Linux / Manjaro / EndeavourOS**:
  ```bash
  sudo pacman -S --noconfirm base-devel gcc python-pillow
  ```
- **openSUSE**:
  ```bash
  sudo zypper install -y gcc-c++ make python3-Pillow
  ```
- **macOS (Apple Silicon e Intel)**:
  ```bash
  xcode-select --install
  brew install libomp pillow
  ```

### 2.3 Compilación Manual de Librerías de Aceleración Nativas
Si deseas compilar manualmente las librerías nativas desde el código fuente:

#### 1. Motor Nativo Mary Apex 3.5 (`libmary.so` y `luma-mary`):
```bash
# Librería compartida (cargada automáticamente por Python vía ctypes):
g++ -O3 -std=c++17 -fPIC -shared -fopenmp mary.cpp -o libmary.so

# Binario CLI independiente:
g++ -O3 -std=c++17 -fopenmp mary.cpp -o luma-mary
```

#### 2. Motor Nativo Luris Mono 2.6 (`libmonochrome.so` y `luma-mono`):
```bash
# Librería compartida:
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so

# Binario CLI independiente:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono
```

> [!NOTE]
> Tanto `mary.cpp` como `monochrome.cpp` son completamente autosuficientes y utilizan encabezados de dominio público de un solo archivo (`stb_image.h`, `stb_image_resize2.h`). ¡No necesitas librerías externas de OpenCV, libpng o libjpeg para compilar las librerías centrales de renderizado!

### 2.4 Verificación del Estado de Motores (`lumart -v`)
Ejecuta el informe de diagnóstico:
```bash
lumart -v
```
Inspecciona la sección **⚡ Rendering Engines**:
- `Mary (Perceptual Color Apex 3.5): Active (Native C++ (.../libmary.so))` -> ✅ Aceleración nativa multi-núcleo activa.
- `Luris (Monochrome Mono 2.6): Active (.../libmonochrome.so)` -> ✅ Monocromático C++ nativo activo.
- Si muestra `(Python Fallback)`, asegúrate de que `libmary.so` y `libmonochrome.so` se encuentren en el mismo directorio que `lumart.py` o en `/usr/local/lib/` / `/usr/local/share/luma/`.

### 2.5 Empaquetado de Distribución y Configuración para Arch Linux / AUR (`yay`)
Luma ofrece soporte oficial para gestores de paquetes nativos:
- **Arch Linux & Manjaro (`makepkg` / `yay`)**:
  Compila e instala directamente desde la especificación oficial incluida en el proyecto:
  ```bash
  cd dist/arch && makepkg -si
  ```
  O instala mediante tu asistente AUR preferido:
  ```bash
  yay -S lumart-bin
  ```
  *(Instala `/usr/bin/lumart`, `/usr/bin/luma`, librerías nativas C++ en `/usr/lib/`, autocompletado en bash/zsh/fish y páginas man).*
- **Debian / Ubuntu / Linux Mint (`.deb`)**:
  ```bash
  sudo apt install ./dist/lumart-2.5.0.deb
  ```
- **Fedora / RHEL / openSUSE (`.rpm`)**:
  ```bash
  sudo dnf install ./dist/lumart-2.5.0-1.x86_64.rpm
  ```
- **Windows 10 / 11 (Instalador Nativo de PowerShell)**:
  Ejecuta el instalador automático en PowerShell:
  ```powershell
  irm https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.ps1 | iex
  # O localmente desde el repositorio clonado:
  powershell -ExecutionPolicy Bypass -File .\install.ps1
  ```

---

## 3. Emuladores de Terminal y Compatibilidad de Tipografías

Luma renderiza gráficos de alta fidelidad utilizando bloques especializados de caracteres Unicode:
1. **Patrones Braille (`U+2800` – `U+28FF`)**: Subpíxeles en matriz de puntos 2x4 (`⡀`, `⣿`, `⣾`, `⢦`).
2. **Sextantes (`U+1FB00` – `U+1FB3B`)**: Micro-bloques sólidos 2x3 (`🬀`, `🬭`, `🬵`, `█`).
3. **Cuadrantes (`U+2596` – `U+259F`)**: Micro-bloques cuadrados 2x2 (`▘`, `▝`, `▖`, `▗`, `▚`, `▛`, `▟`).
4. **Medios Bloques (`U+2580` – `U+2588`)**: Mitad superior (`▀`), mitad inferior (`▄`) y bloques completos (`█`).

### 3.1 Matriz de Compatibilidad de Emuladores de Terminal

| Emulador de Terminal | TrueColor (24 bits) | Alineación Braille | Sextantes (2x3) | Cuadrantes (2x2) | Rendimiento | Estado Recomendado |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Ghostty** | ✅ Impecable | ✅ Píxel exacto | ✅ Completo | ✅ Completo | ⭐⭐⭐⭐⭐ (GPU) | **Tier 1 (Recomendado)** |
| **Kitty** | ✅ Impecable | ✅ Perfecto (con ajuste line-height) | ✅ Completo | ✅ Completo | ⭐⭐⭐⭐⭐ (GPU) | **Tier 1 (Recomendado)** |
| **Alacritty** | ✅ Impecable | ✅ Perfecto | ✅ Completo | ✅ Completo | ⭐⭐⭐⭐⭐ (OpenGL) | **Tier 1 (Recomendado)** |
| **WezTerm** | ✅ Impecable | ✅ Perfecto | ✅ Completo | ✅ Completo | ⭐⭐⭐⭐⭐ (GPU) | **Tier 1 (Recomendado)** |
| **Windows Terminal** | ✅ Impecable | ✅ Perfecto | ✅ Completo | ✅ Completo | ⭐⭐⭐⭐ (DirectWrite) | **Tier 1 en Windows** |
| **iTerm2 (macOS)** | ✅ Impecable | ✅ Perfecto | ⚠️ Requiere fuente | ✅ Completo | ⭐⭐⭐⭐ | **Tier 1 en macOS** |
| **GNOME Terminal** | ✅ Soportado | ⚠️ Pequeños huecos | ⚠️ Según fuente | ✅ Completo | ⭐⭐⭐ | Estándar |
| **macOS Terminal.app** | ❌ Solo 256 colores | ⚠️ Deformado | ❌ Faltan glifos | ⚠️ Aproximado | ⭐⭐ | **No Recomendado** |
| **Windows cmd.exe** | ❌ Incompatible | ❌ Incompatible | ❌ Incompatible | ❌ Incompatible | ⭐ | **Inutilizable (Usa Windows Terminal)** |

### 3.2 Corrección de Huecos Verticales en Braille y Bloques (Ajuste de Line-Height)
Muchos terminales modernos aplican espaciado vertical adicional (`1.2` o `1.3`) para lectura de texto. Dado que los bloques subpíxel del terminal deben tocarse verticalmente para formar una imagen continua, el espaciado causa líneas horizontales vacías.

- **Kitty**: Añade a `~/.config/kitty/kitty.conf`:
  ```conf
  adjust_line_height 0
  ```
- **Alacritty**: Añade a `~/.config/alacritty/alacritty.toml`:
  ```toml
  [font.offset]
  y = 0
  ```
- **WezTerm**: Añade a `~/.wezterm.lua`:
  ```lua
  config.line_height = 1.0
  ```

### 3.3 Tipografías Recomendadas
Para una alineación perfecta sin glifos faltantes, utiliza una fuente monospaced moderna con cobertura Unicode extendida:
- **JetBrains Mono Nerd Font** (Mejor geometría de puntos y contraste)
- **Fira Code Nerd Font**
- **Symbols Nerd Font** (Respaldo para iconos y sextantes faltantes)
- **Cascadia Code** (Incluida en Windows Terminal)

---

## 4. Fidelidad de Color y TrueColor de 24 Bits (ANSI ECMA-48)

Luma genera secuencias de escape ANSI conformes al estándar internacional ECMA-48 en formato TrueColor (16.7 millones de colores reales):
- Color de primer plano (Foreground): `[38;2;R;G;Bm`
- Color de fondo (Background): `[48;2;R;G;Bm`

### 4.1 Comprobación del Soporte de TrueColor
Comprueba si tu terminal informa compatibilidad con color de 24 bits:
```bash
echo $COLORTERM
```
Si devuelve `truecolor` o `24bit`, tu terminal soporta color completo. Si está vacío, agrégalo a tu archivo `~/.bashrc` o `~/.zshrc`:
```bash
export COLORTERM=truecolor
```

### 4.2 Mezcla Gamma en RGB Lineal vs sRGB Estándar
Al promediar colores de subpíxeles dentro de un bloque de celda, el promedio ingenuo en sRGB produce oscurecimiento perceptual ("efecto borde negro"). Luma linealiza los valores RGB mediante corrección gamma:
$$C_{	ext{lineal}} = C_{	ext{sRGB}}^{2.2}$$
Calcula el color subpíxel medio en espacio lineal y reconvierte a sRGB:
$$C_{	ext{salida}} = C_{	ext{medio}}^{1 / 2.2}$$
Esto garantiza que los gradientes y transiciones de color en Mary y Trumble se mantengan luminosos y fieles a la imagen original.

---

## 5. Los Cuatro Motores Insignia (Inmersión Técnica y Arquitectura)

```
                  ┌──────────────────────────────────────────────┐
                  │                 LUMA SUITE                   │
                  └───────┬──────────────┬───────────────┬───────┘
                          │              │               │
            ┌─────────────┴──┐    ┌──────┴────────┐    ┌─┴─────────────┐
            │   MARY APEX    │    │ TRUMBLE ORELX │    │  LURIS MONO   │
            │  Perceptual    │    │ Retro-Arcade  │    │  Monochrome   │
            │  Color 3.5     │    │ Cel-Shading   │    │  Manga 2.6    │
            └────────────────┘    └───────────────┘    └───────────────┘
                                         │
                                  ┌──────┴────────┐
                                  │ SPECTRA WEEP  │
                                  │  Live Webcam  │
                                  │  Stream 2.0   │
                                  └───────────────┘
```

### 5.1 Mary Apex 3.5 (Color Perceptual Oklab y Micro-Bloques Subpíxel)
- **Comando Insignia**: `lumart imagen.png` (Predeterminado sin parámetros) o `lumart imagen.png -E mary -S` (explícito).
- **Tecnología Central**:
  1. **Filtro Guiado en Espacio de Color Oklab**: Suavizado espacial con preservación de bordes que suprime el ruido de alta frecuencia de imágenes JPEG mientras preserva siluetas nítidas en anime y fotografías.
  2. **Contraste Adaptativo Weber-Fechner**: Ajuste de sensibilidad al contraste modelado según la corteza visual humana, resaltando detalles en sombras sin quemar las altas luces.
  3. **Múltiples Modos Subpíxel**:
     - *Predeterminado*: Micro-bloques sólidos Unicode Sextantes 2x3 (`-S`). Produce un renderizado continuo y sólido sin perforaciones.
     - `-B` / `--braille`: Matriz Braille 2x4 con emparejamiento dual de color ANSI en primer plano y fondo.
     - `-Q` / `--quadrants`: Bloques subpíxel cuadrados 2x2.
     - `--blocks`: Medios bloques clásicos (`▀` / `▄`).
- **Resolución de Problemas en Mary**:
  - *Síntoma*: Los caracteres se ven como letras extrañas en vez de bloques sólidos.
    - *Causa*: Tu fuente carece de los símbolos Unicode 13.0 para Computación Clásica (`U+1FB00`).
    - *Solución*: Usa `-B` (Braille) o `-Q` (Cuadrantes), soportados por todas las fuentes, o instala JetBrains Mono Nerd Font v3+.

### 5.2 Trumble Orelx 2.2 (Cel-Shading Retro-Arcade y Entintado Anime)
- **Comando Insignia**: `lumart imagen.png -E trumble --blocks` (o `lumart imagen.png --blocks`).
- **Tecnología Central**:
  1. **Color Punch Estilo Capcom CPS-2 / Neo-Geo**: Mapeo de gama cromática que maximiza la saturación y el contraste para entornos de terminal sin recortar matices.
  2. **Contornos de Tinta Anime**: Superposición dinámica con detección de bordes que traza líneas de tinta oscuras alrededor de personajes y objetos en primer plano.
  3. **Remuestreo Lanczos + Difuminado Bayer**: Reducción geométrica anti-aliasing con tramado matricial retro opcional (`-d bayer`).

### 5.3 Luris Mono 2.6 (Manga Screentone Monocromático y Stickers Transparentes)
- **Comando Insignia**: `lumart imagen.png -E luris -m` (o `lumart imagen.png -m`, `lumart imagen.png --no-color`).
- **Tecnología Central**:
  1. **Lineart por Diferencia de Gaussianas (DoG)**:
     $$\text{DoG}(x, y) = G_{\sigma_1}(x, y) - G_{\sigma_2}(x, y)$$
     Extrae líneas de tinta limpias estilo plumilla G-pen mientras descarta gradientes planos de fondo.
  2. **Trama Manga Inteligente 2.6**: Entinta contornos exteriores nítidos, aplica puntos de medio tono Bayer 8x8 a sombras y ropa, y mantiene la piel y el papel en blanco puro.
  3. **Difusión de Error Bill Atkinson (1984, MacPaint)**: Descarta el 25% del error residual para mantener altas luces completamente limpias sin artefactos dispersos.
  4. **Exportación Exclusiva de Stickers Transparentes (`--transparent`)**:
     ```bash
     lumart personaje.png -m --transparent -o sticker.png
     ```
     ¡Genera un sticker de manga auténtico con canal alfa 100% transparente!

### 5.4 Spectra Weep 2.0 (Video en Vivo, Cámara Web y 12 Shaders)
- **Comando Insignia**: `lumart -E spectra` (o `lumart --webcam`, `lumart -W`, `lumart clip.mp4`, `lumart imagen.png --shader neon`).
- **Tecnología Central**:
  1. **Pipeline de Video OpenCV con Cero Lag**: Captura cuadros de video, realiza submuestreo en tiempo real y transmite secuencias ANSI de alto rendimiento (30–60 FPS).
  2. **12 Shaders Multi-Espectrales**:
     - `neon`: Resplandor cyberpunk synthwave híper-saturado con realce de bordes.
     - `thermal`: Visión de mapa de calor infrarrojo militar FLIR.
     - `tron`: Mallas vectoriales brillantes de color cian sobre fondo negro absoluto.
     - `matrix`: Código digital Katakana auténtico con bloom de fósforo verde P1 (525nm).
     - `amber`: Monitor vintage CRT de fósforo ámbar de los años 70.
     - `hologram`: Interferencia holográfica de ciencia ficción en tonos cian.
     - `glitch`: Aberración cromática RGB con oscilaciones temporales.
     - `phosphor-bloom`: Resplandor analógico difuso de tubo CRT.
     - `solarize`, `manga`, `theme`, `normal`.
  3. **Reproducción Directa de Archivos de Video**: Renderiza cualquier archivo `.mp4`, `.mkv`, `.webm` o `.mov` directamente en el terminal a su tasa nativa de fotogramas.
- **Resolución de Problemas en Spectra**:
  - *Síntoma*: `Permission denied: '/dev/video0'`
    - *Solución*: Agrega tu usuario al grupo: `sudo usermod -aG video $USER`, luego cierra e inicia sesión.
  - *Síntoma*: Pantalla en blanco o `Camera index out of range`
    - *Solución*: Especifica el índice del dispositivo: `lumart -W 1` o `lumart -W 2`.
  - *Síntoma*: `OpenCV required for Spectra engine`
    - *Solución*: Instala `python3-opencv` mediante tu gestor de paquetes o ejecuta `pip install opencv-python`.

---

## 6. Subcomandos Especializados y Herramientas Integradas

Más allá del renderizado de imágenes individuales, Lumart v2.5.0 integra herramientas dedicadas en la línea de comandos para personalización del sistema, auditoría de rendimiento y automatización de flujos de trabajo:

### 6.1 `lumart fetch` (Generador de Presets para Fastfetch / Neofetch)
```bash
lumart fetch <imagen.png> [-w ANCHO]
```
- **Flujo de Trabajo Automatizado**:
  1. Detecta y recorta bordes transparentes o vacíos automáticamente mediante el algoritmo de contorno `--fastfetch`.
  2. Redimensiona y renderiza la imagen en medios bloques TrueColor de 24 bits (`▀` / `▄`, 2 píxeles verticales por celda).
  3. Guarda el arte ANSI directamente en `~/.config/fastfetch/<nombre>_logo.ans`.
  4. Genera e imprime el bloque JSON listo para copiar a `~/.config/fastfetch/config.jsonc`.
- **Ancho Óptimo**: Recomendamos entre `-w 36` y `-w 42`. Anchos superiores a 45 columnas provocan saltos de línea y desalinean la columna de información del sistema en ventanas estándar.

### 6.2 `lumart bench` (Banco de Pruebas de Rendimiento y Latencia Multi-Núcleo)
```bash
lumart bench [imagen.png] [-w ANCHO]
```
- Ejecuta una prueba de estrés comparativa entre los 4 motores insignia (Mary Apex, Trumble Arcade, Luris Mono C++ y Spectra Weep).
- Informa métricas precisas:
  - **Latencia**: Tiempo de procesamiento por fotograma en milisegundos (`ms`).
  - **Rendimiento**: Megapíxeles procesados por segundo (`MP/s`).
  - **Tasa Potencial**: Capacidad de cuadros por segundo (`FPS`).

### 6.3 `lumart showcase` (Lienzo Comparativo 4-en-1)
```bash
lumart showcase <imagen.png> [-w ANCHO] [-o comparativa.png]
```
- Divide el lienzo del terminal en 4 cuadrantes iguales mostrando la misma imagen a través de los cuatro motores insignia lado a lado:
  - **Superior Izquierdo**: Mary Apex 3.5 (Fotorrealismo Oklab K-Means)
  - **Superior Derecho**: Trumble Orelx 2.2 (Cel-Shading Retro-Arcade)
  - **Inferior Izquierdo**: Luris Mono 2.6 (Trama Manga Bayer 8x8)
  - **Inferior Derecho**: Spectra Weep 2.0 (Shader Cyberpunk Neón)
- Permite exportar la cuadrícula comparativa completa directamente a PNG mediante `-o`.

### 6.4 `lumart info` (Inspector Visual y Recomendador de Motores)
```bash
lumart info <imagen.png>
```
- Realiza una inspección visual y estadística exhaustiva de la imagen:
  - Resolución nativa, ancho, alto y relación física de aspecto.
  - Luminancia media, rango dinámico y contraste tonal.
  - Los 6 colores dominantes representados con valores HEX y muestras ANSI reales.
  - **Recomendación Inteligente de Motor**: Analiza si la imagen es fotografía, ilustración o dibujo lineal, recomendando la opción óptima.

### 6.5 `lumart diff` (Mapa de Calor Cromático Delta entre Dos Imágenes)
```bash
lumart diff <img1.png> <img2.png> [-w ANCHO]
```
- Calcula las diferencias euclidianas y perceptuales píxel a píxel entre dos imágenes.
- Muestra un mapa de calor en falso color de las regiones alteradas e informa el porcentaje Delta medio ($\Delta E$).

### 6.6 `lumart slideshow` (Pase de Diapositivas en Pantalla Completa en Terminal)
```bash
lumart slideshow <carpeta/> [--delay 3.0] [-w ANCHO]
```
- Recorre todas las imágenes de un directorio con proyección a pantalla completa y transiciones limpias.
- Controles interactivos: `Espacio` (pausa/reanudar), flechas `Izquierda`/`Derecha` (anterior/siguiente), `Q` (salir).

### 6.7 `lumart -I` / `--interactive` (Visor TUI Interactivo)
```bash
lumart -I <imagen.png>
```
- Inicia una interfaz de usuario interactiva en la terminal con atajos de teclado en vivo:
  - `+` / `-`: Aumentar o disminuir brillo.
  - `M` / `T` / `L`: Cambiar en tiempo real entre los motores Mary, Trumble y Luris.
  - `G`: Alternar el modo de trama Manga Screentone.
  - `Z`: Acercar o alejar zoom digitalmente.

### 6.8 `lumart animate` (Transcodificador de GIFs y Compilador de Video)
```bash
lumart animate <clip.mp4 | carpeta_frames/> -o resultado.gif [--fps 30]
```
- Compila archivos de video o secuencias de imágenes directamente en GIFs animados procesados a través del motor ANSI de Lumart.

---

## 7. Dimensiones, Relación de Aspecto y Calibración de Fuente (--font-ratio)

### 7.1 La Calibración de Celda de Carácter 1:2
Las celdas de caracteres de texto en los emuladores de terminal no son cuadradas; los caracteres estándar monospace miden aproximadamente **el doble de alto que de ancho** (relación $1:2$).
Si una imagen se escala sin compensar esta geometría, aparecerá estirada verticalmente en un 200%.

Luma aplica automáticamente una escala geométrica matemáticamente calibrada según el tipo de glifo:
- **Modo Braille (`-B`)**: 2 puntos de ancho $\times$ 4 puntos de alto ($2:4 = 1:2$). ¡Cada celda Braille compensa la proporción de la fuente de manera nativa!
- **Medios Bloques (`--blocks`)**: 1 carácter de ancho $\times$ 2 píxeles de alto ($1:2$).
- **Sextantes (Predeterminado / `-S`)**: 2 subpíxeles de ancho $\times$ 3 subpíxeles de alto ($2:3$). Calibrados para la proporción estándar 0.5 para una geometría libre de distorsión.

### 7.2 Auto-Ajuste al Viewport (`-F`) vs Ancho Fijo (`-w`)
- **Auto-Ajuste al Viewport (`-F` / `--fit`)**: Consulta dinámicamente las dimensiones de la ventana del terminal (`shutil.get_terminal_size()`), considerando la proporción geométrica de los caracteres para maximizar el tamaño sin provocar scroll vertical ni desbordamientos de prompt.
- **Ancho Fijo en Columnas (`-w <columnas>`)**: Fuerza la salida a un número fijo de columnas horizontales. Es ideal para barras laterales de fetch (36–42 columnas) y automatización en scripts.
> [!WARNING]
> `-F` y `-w` son mutuamente excluyentes. Proporcionar ambas banderas provocará que Lumart se detenga con código de error 2.

### 7.3 Calibración de la Relación de Aspecto de Fuente (`--font-ratio`)
Aunque `0.5` representa la relación estándar 1:2, ciertas fuentes monospaced específicas (como Victor Mono, Terminus o configuraciones con interlineado personalizado) pueden variar entre `0.42` y `0.58`. Puedes calibrar el escalado vertical de forma dinámica:
```bash
# Fuentes estrechas o condensadas:
lumart foto.png --font-ratio 0.45

# Fuentes anchas o cuadradas:
lumart foto.png --font-ratio 0.55
```

---

## 8. Exportación Gráfica de Alta Definición y Stickers (-o, --loop, --preload)

### 8.1 Exportación Gráfica de Alta Definición y Rasterización
Luma puede rasterizar el arte del terminal directamente en imágenes gráficas nítidas en alta resolución (`.png`, `.jpg`):

```bash
# Exportar arte subpíxel de Mary Apex a PNG en 1080p/4K:
lumart foto.png -w 120 -o render.png

# Exportar bloques anime estilo arcade a JPEG:
lumart foto.png --blocks -w 100 -o render.jpg
```

### 8.2 Exportación de Stickers Manga Transparentes (`--transparent`)
Exclusivo del motor **Luris Mono**, `--transparent` elimina el fondo oscuro sólido y genera contornos con canal alfa puro:
```bash
# Exportar sticker manga transparente (Exclusivo de Luris Mono):
lumart personaje.png -m --transparent -o sticker.png

# Combinado con eliminación inteligente de fondo por tolerancia:
lumart personaje.png -m -r --bg-tolerance 40 --transparent -o sticker_limpio.png
```

### 8.3 Precarga Total en RAM y Compilación de GIFs Animados a 60 FPS
Renderiza y transcodifica animaciones a altas tasas de fotogramas con precarga en memoria:
```bash
# Precarga total en RAM para 60 FPS ultra-fluidos sin lag en el terminal:
lumart anim.gif --loop --fps 60 --preload

# Exportar animación procesada con una paleta de color a un nuevo GIF:
lumart anim.gif --loop --theme synthwave --fps 30 -o salida_synthwave.gif
```

### 8.4 Por Qué se Eliminó la Exportación a WebP (`.webp`)
Los algoritmos de compresión con pérdida y casi sin pérdida de WebP aplican submuestreo cromático espacial y transformaciones macrobloque que desdibujan los glifos subpíxel discretos (Sextantes, puntos Braille y bordes de Cuadrantes). Para garantizar una fidelidad absoluta píxel por píxel y contornos alfa transparentes sin artefactos, Luma estandariza estrictamente en `.png` sin pérdida (con soporte de canal alfa) y `.jpg` de alta calidad.

---

## 9. Configuración, Persistencia y Localización (i18n)

A partir de la versión 2.3.1 ("Rosetta"), Luma incorpora un motor integral de internacionalización con soporte para 8 idiomas, permitiendo configuración tanto en tiempo de ejecución como persistente.

### 9.1 Matriz de Idiomas Soportados

| Código | Idioma | Nombre Nativo | Ejemplo de Comando |
| :---: | :--- | :--- | :--- |
| `en` | **Inglés** (Predeterminado) | English | `lumart --lang en` |
| `es` | **Español** | Español | `lumart --lang es` |
| `fr` | **Francés** | Français | `lumart --lang fr` |
| `pt` | **Portugués** | Português | `lumart --lang pt` |
| `ru` | **Ruso** | Русский | `lumart --lang ru` |
| `ja` | **Japonés** | 日本語 | `lumart --lang ja` |
| `de` | **Alemán** | Deutsch | `lumart --lang de` |
| `ko` | **Coreano** | 한국어 | `lumart --lang ko` |

### 9.2 Ajuste Persistente vs Reemplazo Efímero en Ejecución
Luma ofrece dos modos flexibles para la configuración de idioma:

#### 1. Configuración Persistente (Se guarda para todas las sesiones futuras):
Ejecuta `lumart --lang <código>` sin otros argumentos. Luma guardará tu elección en `~/.config/luma/config.json`:
```bash
# Cambiar el idioma predeterminado a español:
lumart --lang es

# Cambiar el idioma predeterminado a japonés:
lumart --lang ja
```

#### 2. Reemplazo Efímero (Aplica únicamente al comando actual):
Añade `--lang <código>` o `--lang=<código>` en cualquier lugar de tu línea de comandos:
```bash
# Ver informe de diagnóstico en español:
lumart --lang es -v

# Renderizar una imagen con interfaz en francés:
lumart personaje.png --lang fr

# Ver el historial en alemán:
lumart --lang de -H 5
```

### 9.3 Jerarquía Estricta de Resolución de Idioma
Al iniciar, Luma resuelve el idioma mediante esta estricta jerarquía de 4 niveles:
1. **Bandera de Línea de Comandos**: `--lang <código>` o `--lang=<código>` (máxima prioridad).
2. **Configuración de Usuario Persistente**: `~/.config/luma/config.json` (si fue guardada previamente).
3. **Detección Regional del Entorno**: Evalúa `$LC_ALL`, `$LC_MESSAGES` y `$LANG`, extrayendo el código ISO 639-1 de dos letras (ej. `es_ES.UTF-8` $	o$ `es`).
4. **Respaldo por Defecto**: Inglés (`en`).

### 9.4 Solución de Problemas de Configuración Regional (Locale)

- **Problema 1: `UnicodeEncodeError: 'ascii' codec can't encode character` en Docker / Contenedores**
  - *Causa*: Los contenedores mínimos de Linux o entornos chroot a menudo carecen de definiciones UTF-8 y usan `POSIX` o `C`.
  - *Solución*: Exporta variables de entorno estándar UTF-8 antes de ejecutar:
    ```bash
    export LANG=C.UTF-8
    export LC_ALL=C.UTF-8
    ```

- **Problema 2: Caracteres CJK (Japonés / Coreano) o Cirílicos se Muestran como Cajas Vacías ("Tofu")**
  - *Causa*: La fuente monospace principal de tu terminal no incluye glifos para Kanji, Hiragana, Hangul o Cirílico.
  - *Solución*: Instala un paquete completo de fuentes tipográficas:
    - Debian/Ubuntu: `sudo apt install fonts-noto-cjk fonts-noto-core`
    - Fedora: `sudo dnf install google-noto-sans-cjk-fonts google-noto-sans-fonts`
    - Arch Linux: `sudo pacman -S noto-fonts noto-fonts-cjk`

- **Problema 3: Restablecer Toda la Configuración a Valores de Fábrica**
  - Si tu archivo `config.json` se corrompe o tiene permisos bloqueados:
    ```bash
    rm -rf ~/.config/luma/config.json
    lumart --lang es
    ```

---

## 10. Historial de Comandos y Reproducción Interactiva (-H, -R)

Luma registra automáticamente el historial de ejecuciones con marcas de tiempo, versión y parámetros utilizados.

### 10.1 Visualización del Historial (`-H` / `--history`)
```bash
# Ver historial reciente (por defecto: todos):
lumart -H

# Limitar salida a los últimos 5 comandos:
lumart -H 5
```
Ejemplo de Salida:
```
📜 Lumart Command History (5 recorded):

  [#]   Ver       Date / Time         Command
  ──────────────────────────────────────────────────────────────────────────────
  [01]  v2.5.0    2026-10-11 12:00:25 lumart render.png -w 100
  [02]  v2.5.0    2026-10-11 11:58:39 lumart slime.jpg -m --transparent -o sticker.png
  [03]  v2.4.1    2026-10-03 13:32:28 lumart photo.jpg --blocks -o retro.jpg
  ──────────────────────────────────────────────────────────────────────────────
  💡 Para re-ejecutar cualquier comando: lumart --replay <número> (ej: lumart -R 1)
```

### 10.2 Reproducción Instantánea (`-R` / `--replay`)
Vuelve a ejecutar cualquier comando anterior directamente sin volver a escribirlo:
```bash
# Re-ejecutar el comando más reciente:
lumart -R

# Re-ejecutar el comando #2 del historial:
lumart -R 2
```

### 10.3 Limpieza del Historial (`--clear-history`)
```bash
lumart --clear-history
```

---

## 11. Sistema de Actualizaciones, Mejoras y Rollback (-u, -uu, -dg)

Luma incorpora un administrador de versiones integrado con protección automática de retroceso (rollback):

### 11.1 Comprobación de Actualizaciones (`-u` / `--update`)
Comprueba en GitHub si existen nuevas versiones estables sin modificar ningún archivo:
```bash
lumart -u
```

### 11.2 Aplicación Atómica de Actualizaciones (`-uu` / `--upgrade`)
Descarga y actualiza de manera atómica a la versión más reciente:
```bash
lumart -uu
```
Antes de actualizar, Luma archiva automáticamente tu versión actual en `~/.config/luma/backup/lumart-v<VERSION>`.

### 11.3 Rollback / Retroceso de Versión (`-dg` / `--downgrade`)
Si una actualización presenta incompatibilidades con tu sistema, regresa inmediatamente a la versión anterior:
```bash
# Selector interactivo de rollback (restaura desde el respaldo local al instante sin conexión):
lumart -dg

# O especifica una versión de destino directamente:
lumart -dg 2.4.1
```

---

## 12. Integración con el Escritorio y Gestores de Archivos de Linux (--install-desktop)

Integra Luma directamente en tu entorno de escritorio y gestores de archivos (GNOME Files/Nautilus, Nemo, Dolphin, Thunar):

```bash
lumart --install-desktop
```

### 12.1 Lanzador de Escritorio e Integración MIME
Instala `lumart.desktop` en `~/.local/share/applications` con asociaciones completas de tipos MIME (`image/png`, `image/jpeg`, `image/gif`, `image/webp`). Esto permite configurar Lumart como visor de imágenes predeterminado o abrir archivos directamente desde lanzadores del sistema (Rofi, Wofi, KRunner, GNOME Dash).

### 12.2 Scripts para el Menú Contextual de Clic Derecho en Gestores de Archivos
Instala scripts contextuales en Nautilus (`~/.local/share/nautilus/scripts/`) y Nemo (`~/.local/share/nemo/scripts/`):
- Haz clic derecho sobre cualquier imagen en tu explorador $	o$ **Scripts** $	o$ **Abrir con Lumart (Terminal)**.
- Abre tu terminal predeterminado mostrando la imagen renderizada en arte ANSI de alta fidelidad.
Actualiza automáticamente las bases de datos de escritorio mediante `update-desktop-database`.

---

## 13. Recetas Prácticas del Mundo Real y Flujos de Trabajo

### 13.1 Receta 1: El Logo Perfecto para la Barra Lateral de Fastfetch / Neofetch
```bash
# Opción A: Medios bloques TrueColor (Recomendada)
lumart fetch "avatar.png" -w 38

# Opción B: Trama Manga Screentone minimalista (Ideal para temas Catppuccin / Nord)
lumart "avatar.png" -w 38 --fastfetch -m -o ~/.config/fastfetch/logo_manga.ans

# Opción C: Matriz de alta densidad en Braille 2x4
lumart "avatar.png" -w 38 --fastfetch -E mary -B -o ~/.config/fastfetch/logo_braille.ans
```
*Configuración en `~/.config/fastfetch/config.jsonc`:*
```jsonc
{
  "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
  "logo": {
    "source": "~/.config/fastfetch/avatar_logo.ans",
    "type": "file",
    "width": 38,
    "padding": {
      "top": 1,
      "left": 1,
      "right": 2
    }
  },
  "modules": [
    "title",
    "separator",
    "os",
    "kernel",
    "uptime",
    "packages",
    "shell",
    "wm",
    "terminal",
    "cpu",
    "gpu",
    "memory",
    "colors"
  ]
}
```
*Prueba inmediatamente en tu terminal:*
```bash
fastfetch --logo ~/.config/fastfetch/avatar_logo.ans --logo-type file
```

### 13.2 Receta 2: Stickers de Anime Transparentes para Discord / Telegram
```bash
# Exportar sticker transparente (sin caja negra de fondo):
lumart "personaje.png" -w 80 -m --transparent -o sticker.png

# Con recorte automático de fondo por inundación:
lumart "personaje.png" -w 80 -m -r --bg-tolerance 40 --transparent -o sticker_limpio.png
```

### 13.3 Receta 3: GIFs Animados a 60 FPS con Cero Lag y Precarga en RAM
```bash
# Reproducción suave a 60 FPS precargada en memoria RAM:
lumart "animacion.gif" -w 70 --loop --fps 60 --preload

# Exportar animación con paleta Synthwave a un nuevo GIF:
lumart "animacion.gif" -w 60 --theme synthwave --fps 30 -o anim_synthwave.gif
```

### 13.4 Receta 4: Transmisión de Cámara Web en Vivo Estilo Cyberpunk Matrix CRT
```bash
# Código Matrix Katakana en fósforo verde P1 con líneas de escaneo:
lumart -W 0 --matrix --crt green --fps 60

# Visión térmica infrarroja FLIR de grado militar:
lumart -W 0 --shader thermal --fps 30
```

### 13.5 Receta 5: Automatización en Scripts Bash, Pipelines de Unix y MOTD
```bash
# Banner de bienvenida en ~/.bashrc:
if command -v lumart &>/dev/null; then
    lumart ~/.config/banner.png -w 60 --border rounded --align center --instant
fi

# Renderizar directamente desde URL HTTPS en la web:
lumart "https://raw.githubusercontent.com/fastfetch-cli/fastfetch/dev/assets/arch.png" -w 50

# Renderizar imagen contenida en el portapapeles del sistema:
lumart --paste -w 60 --border double

# Copiar el arte ANSI generado directamente al portapapeles:
lumart "logo.png" -w 40 -C
```

---

## 14. Enciclopedia Completa de Opciones y Flags de la Línea de Comandos

### A. Motores y Texturas de Glifos
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | *auto* | Selecciona explícitamente el motor (enrutado automático por defecto). |
| `-S`, `--sextants`| — | *activo* | Bloques Unicode Sextantes 2x3 (predeterminado en Mary Apex, 6 subpíxeles/celda). |
| `-B`, `--braille` | — | `false` | Matriz Unicode Braille 2x4 (8 subpíxeles/celda, máxima precisión en contornos). |
| `-Q`, `--quadrants`| — | `false` | Bloques Unicode Cuadrantes 2x2 (4 subpíxeles/celda). |
| `--blocks` | — | `false` | Medios bloques optimizados (`▀` / `▄`, 2 píxeles verticales/celda con TrueColor de 24 bits). |
| `-m`, `--manga` | — | `false` | Modo Manga Screentone (*Ami-tone* Bayer 8x8 + contornos limpios de tinta DoG). |
| `-s`, `--sketch`| — | `false` | Modo de boceto a lápiz limpio sin manchas ni artefactos de sombras. |
| `-ch`, `--crosshatch`| — | `false` | Sombreado auténtico a pluma con trazos cruzados a 45 grados en 6 niveles de densidad. |
| `-cs`, `--charset` | `<nombre>` | `standard` | Rampa de caracteres tipográficos: `dense`, `standard`, `blocks`, `math`, `runes`, `katakana`, `crosshatch`. |
| `--matrix` | — | `false` | Transforma la salida en código digital Matrix Katakana con bloom verde de fósforo P1 (525nm). |
| `--matrix-rain` | — | `false` | Animación continua de lluvia de código digital Matrix descendente. |

### B. Geometría, Dimensiones y Encuadre
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-w`, `--width` | `<int>` | *terminal* | Ancho de salida en columnas (mutuamente excluyente con `-F`). |
| `-F`, `--fit` | — | `false` | **Auto-ajuste al viewport**: calcula ancho y alto óptimos para llenar la ventana sin scroll. |
| `--fastfetch`, `--logo` | — | `false` | Recorta bordes vacíos/transparentes para logos compactos y pantallas de fetch. |
| `--font-ratio` | `<float>` | `0.5` | Calibración de la proporción geométrica ancho/alto de la fuente del terminal. |
| `--crop` | `"x,y,w,h"` | `None` | Recorta una región específica antes de renderizar: `--crop "100,50,400,400"`. |
| `--zoom` | `<float>` | `1.0` | Factor de aumento de zoom digital (ej. `--zoom 1.5` para 150%). |
| `--rotate` | `0` \| `90` \| `180` \| `270` | `0` | Rotación en sentido horario en grados. |
| `--flip`, `--mirror` | `h` \| `v` | `None` | Reflejo especular geométrico: horizontal (`h`) o vertical (`v`). |
| `--border` | `rounded` \| `single` \| `double` \| `heavy` \| `ascii` \| `blocks` | `None` | Enmarca el renderizado en un borde decorativo Unicode. |
| `--align` | `left` \| `center` \| `right` | `left` | Alineación horizontal dentro del viewport del terminal. |
| `--center` | — | `false` | Alias abreviado de `--align center`. |

### C. Colorimetría, Shaders y Parámetros Visuales
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-c`, `--color` | — | `true` | Fuerza la salida en TrueColor de 24 bits. |
| `--no-color` | — | `false` | Desactiva las secuencias de escape ANSI de color y redirige al motor monocromático. |
| `--brightness` | `<float>` | `1.0` | Multiplicador de brillo (ej. `1.2` para aclarar, `0.8` para oscurecer). |
| `--contrast` | `<float>` | `1.0` | Multiplicador de contraste tonal (ej. `1.3` para mayor fuerza de tonos). |
| `--saturation` | `<float>` | `1.0` | Multiplicador de saturación de color (ej. `1.4` para colores vivos, `0.0` para escala de grises). |
| `--boost`, `--vibrant` | — | `false` | Saturación mejorada y curvas Retinex para un aspecto retro-arcade vibrante. |
| `--gamma` | `<float>` | `1.0` | Exponente de corrección no lineal de curva gamma en medios tonos. |
| `-i`, `--invert`| — | `false` | Invierte el mapeo de luminancia (muy útil en terminales con fondo blanco). |
| `--swap` | `<c1> <c2>` | `None` | Intercambia dinámicamente dos colores en el espacio tridimensional RGB. |
| `--theme`, `--palette` | `<nombre>` | `None` | Paleta de color curada: `cyberpunk`, `dracula`, `nord`, `catppuccin`, `gruvbox`, `synthwave`, `monokai`, `gameboy`, `amber`. |
| `--crt`, `--scanlines` | `green` \| `amber` \| `color` \| `scanlines` | `None` | Emulación analógica de monitor CRT vintage con líneas de escaneo. |
| `--shader` | `<nombre>` | `None` | Shaders multi-espectrales: `neon`, `cyberpunk`, `thermal`, `tron`, `matrix`, `amber`, `manga`, `hologram`, `glitch`, `phosphor-bloom`, `solarize`. |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | *auto* | Algoritmo de difusión de error para sombreado y tramas. |

### D. Animación, GIFs y Framerates
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--loop` | — | `false` | Modo de reproducción en bucle continuo en terminal para archivos GIF o APNG. |
| `--fps`, `--target-fps` | `<float>` | *del gif* | Tasa de fotogramas objetivo para reproducción o exportación (ej. `--fps 60`). |
| `--preload`, `--smooth` | — | `false` | **Precarga total en RAM**: pre-renderiza todos los cuadros en memoria para **60 FPS sedosos con 0 ms de latencia**. |
| `--instant`, `--no-reveal`| — | `true` | Imprime la imagen completa inmediatamente sin retraso progresivo. |
| `--reveal` | — | `false` | Efecto de animación progresiva línea por línea en pantalla. |

### E. Exportación Gráfica, Stickers y Portapapeles
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-o`, `-O`, `--output`, `--save` | `<archivo.png / .jpg / .gif>` | `None` | Exporta la salida procesada a imagen rasterizada o GIF animado. |
| `--transparent` | — | `false` | **Exclusivo de Luris Mono**: exporta stickers con fondo transparente puro (sin recuadro negro). |
| `-r`, `--remove-bg` | — | `false` | Eliminación inteligente de fondo por inundación perceptual de color. |
| `--bg-tolerance` | `<1-100>` | `32` | Umbral de tolerancia de color para la eliminación de fondo. |
| `-C`, `--copy` | — | `false` | Copia el arte ANSI formateado (con secuencias de escape de color) directamente al portapapeles del sistema. |
| `--copy-plain` | — | `false` | Copia texto ASCII limpio (sin códigos de color) directamente al portapapeles para Discord/Markdown. |
| `--paste` | — | `false` | Lee y renderiza la imagen presente actualmente en el portapapeles del sistema (Ctrl+C). |

### F. Video y Transmisión de Cámara Web en Vivo
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-W`, `--webcam`| `[id]` | `0` | Transmite cámara web en vivo al terminal a 30-60 FPS (0 = cámara integrada, 1 = USB externa). |
| `<video.mp4>` | `<ruta>` | `None` | Reproduce directamente archivos de video (`.mp4`, `.mkv`, `.webm`, `.mov`) en el terminal. |

### G. Administración, Historial e Idioma
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--lang` | `<código>` | *auto* | Fija el idioma de la interfaz (`en`, `es`, `pt`, `fr`, `ru`, `ja`, `de`, `ko` o nombres como `spanish`, `japanese`). |
| `-H`, `--history` | `[N]` | `10` | Muestra los últimos N comandos registrados en el historial de Lumart. |
| `-R`, `--replay` | `[N]` | *último* | Re-ejecuta el comando N del historial (por defecto: el último comando ejecutado). |
| `--clear-history`| — | `false` | Vacía el archivo de historial de comandos. |
| `--install-desktop` | — | `false` | Registra "Abrir con Lumart" en los menús contextuales de clic derecho de Linux. |
| `--completions` | `bash` \| `zsh` \| `fish` | `None` | Genera scripts de autocompletado para el shell seleccionado. |
| `-v`, `--version` | — | `false` | Muestra el reporte completo de diagnóstico del sistema, hardware y librerías C++. |
| `-u`, `--check-update`| — | `false` | Comprueba en GitHub si existen nuevas versiones disponibles. |
| `-uu`, `--upgrade` | `opcional` | `latest` | Asistente de actualización atómica con respaldo automático de seguridad. |
| `-dg`, `--downgrade` | `opcional` | `prev` | Selector interactivo de rollback para restaurar la versión anterior. |

---

## 15. Referencia Maestra de Comandos y Hoja de Trucos

```bash
# ==============================================================================
# 1. VERSIÓN, DIAGNÓSTICO DEL SISTEMA Y LOCALIZACIÓN
# ==============================================================================
lumart -v                                # Informe completo de diagnóstico del sistema
lumart --lang es                         # Cambiar idioma persistente a español
lumart --lang en                         # Cambiar idioma persistente a inglés
lumart --lang fr                         # Cambiar idioma persistente a francés
lumart --lang ja                         # Cambiar idioma persistente a japonés
lumart --lang ru                         # Cambiar idioma persistente a ruso
lumart --lang de                         # Cambiar idioma persistente a alemán
lumart --lang pt                         # Cambiar idioma persistente a portugués
lumart --lang ko                         # Cambiar idioma persistente a coreano

# ==============================================================================
# 2. MARY APEX 3.5 (COLOR PERCEPTUAL OKLAB) — PREDETERMINADO O EXPLÍCITO
# ==============================================================================
lumart foto.png                          # Predeterminado: Sextantes HD + TrueColor natural (Zero-Flag)
lumart foto.png -E mary -S               # Invocación explícita del motor insignia (salida idéntica)
lumart foto.png -B                       # Matriz Braille TrueColor de dos colores (2x4)
lumart foto.png -Q                       # Bloques Cuadrantes 2x2
lumart foto.png --blocks                 # Medios Bloques clásicos (▀ / ▄)
lumart foto.png --boost                  # Saturación estilo arcade + curvas Retinex
lumart foto.png --vibrant                # Alias de --boost
lumart foto.png -c                       # Forzar salida en TrueColor (predeterminado)
lumart foto.png --no-color               # Desactivar colores y redirigir a monocromático
lumart foto.png --font-ratio 0.45        # Calibrar relación de aspecto de la fuente
lumart foto.png --reveal                 # Animación progresiva de barrido línea por línea
lumart foto.png --instant                # Salida instantánea sin animación (predeterminado)

# ==============================================================================
# 3. TRUMBLE ORELX 2.2 (CEL-SHADING RETRO-ARCADE)
# ==============================================================================
lumart anime.png -E trumble --blocks     # Renderizado arcade en medios bloques cel-shaded
lumart anime.png --boost                 # Saturación vibrante estilo Capcom CPS-2 / Neo-Geo + Tinta
lumart anime.png -d bayer                # Tramado matricial retro ordenado Bayer 8x8
lumart anime.png --swap purple pink      # Intercambio dinámico de colores en espacio 3D RGB

# ==============================================================================
# 4. LURIS MONO 2.6 (MANGA MONOCROMÁTICO Y STICKERS)
# ==============================================================================
lumart manga.png -E luris -m             # Invocación explícita de Manga Screentone (DoG + Bayer)
lumart boceto.png -s                     # Boceto limpio a plumilla G-Pen (solo contornos)
lumart foto.png -d atkinson              # Tramado Bill Atkinson 1984 de MacPaint
lumart foto.png -d floyd                 # Difusión de error Floyd-Steinberg
lumart anime.png -i                      # Forzar inversión (auto-detectado en fondos blancos)
lumart waifu.png -m --transparent -o sticker.png # ¡Sticker transparente con canal alfa!

# ==============================================================================
# 5. SPECTRA WEEP 2.0 (TRANSMISIÓN DE CÁMARA WEB Y VIDEO EN VIVO)
# ==============================================================================
lumart -E spectra                        # Transmitir cámara web en vivo vía selector de motor
lumart --webcam                          # Transmitir cámara web predeterminada (/dev/video0)
lumart -W 1                              # Transmitir cámara web secundaria (/dev/video1)
lumart video.mp4                         # Reproducir archivo de video en la terminal

# ==============================================================================
# 6. EXPORTACIÓN GRÁFICA A ARCHIVO
# ==============================================================================
lumart imagen.png -w 120 -o arte.png     # Exportar imagen rasterizada de alta resolución en PNG
lumart imagen.png --blocks -o arte.jpg   # Exportar imagen rasterizada en JPG

# ==============================================================================
# 7. HISTORIAL Y REPRODUCCIÓN
# ==============================================================================
lumart -H                                # Ver historial completo de ejecución
lumart -H 10                             # Ver los últimos 10 comandos
lumart -R                                # Re-ejecutar el último comando
lumart -R 3                              # Re-ejecutar el comando #3 del historial
lumart --clear-history                   # Vaciar el archivo de historial

# ==============================================================================
# 8. ACTUALIZACIONES E INTEGRACIÓN CON EL ESCRITORIO
# ==============================================================================
lumart -u                                # Comprobar actualizaciones en GitHub sin instalar
lumart -uu                               # Descargar e instalar la última versión
lumart -dg                               # Revertir a la versión anterior desde backup
lumart --install-desktop                 # Instalar lanzador de escritorio y menús de clic derecho
lumart --paste                           # Cargar y renderizar imagen del portapapeles

# ==============================================================================
# 9. SHADERS AVANZADOS v2.5.0, EMULACIÓN CRT Y LLUVIA MATRIX
# ==============================================================================
lumart imagen.png --matrix               # Código digital Matrix Katakana + P1 fósforo verde (525nm)
lumart imagen.png --matrix-rain          # Animación de lluvia digital Matrix descendente
lumart imagen.png --shader neon          # Resplandor cyberpunk synthwave
lumart imagen.png --shader thermal       # Mapa térmico infrarrojo militar FLIR
lumart imagen.png --shader tron          # Líneas vectoriales cian brillantes
lumart imagen.png --theme catppuccin     # Paleta de color Catppuccin
lumart imagen.png --theme dracula        # Paleta de color Dracula
lumart imagen.png --theme synthwave      # Paleta de color Synthwave de los 80
lumart imagen.png --crt green            # Monitor analógico CRT fósforo verde vintage
lumart imagen.png --crt amber            # Monitor analógico CRT fósforo ámbar
lumart imagen.png --border rounded       # Enmarcar en marco decorativo Unicode redondeado
lumart imagen.png --border double        # Enmarcar en marco decorativo de doble línea
lumart imagen.png --align center         # Centrar horizontalmente en la terminal
lumart imagen.png --crop "100,50,400,400"# Recortar región específica antes de renderizar
lumart imagen.png --zoom 1.5             # Zoom digital de 150%
lumart imagen.png -C                     # Copiar arte ANSI (con colores) al portapapeles
lumart imagen.png --copy-plain           # Copiar texto ASCII limpio (sin colores) al portapapeles

# ==============================================================================
# 10. SUBCOMANDOS ESPECIALIZADOS
# ==============================================================================
lumart fetch avatar.png -w 38            # Auto-recorte, generar logo Fastfetch & bloque JSON
lumart bench foto.jpg -w 100             # Ejecutar benchmark de latencia, throughput y FPS
lumart showcase imagen.png -w 90         # Lienzo comparativo 4-en-1 (Mary, Trumble, Luris, Spectra)
lumart info foto.jpg                     # Inspector visual, perfilador de paleta y recomendación
lumart diff img1.png img2.png -w 80      # Mapa de calor de diferencias cromáticas delta
lumart slideshow ./fondos/ --delay 3     # Pase de diapositivas interactivo en pantalla completa
lumart -I imagen.png                     # Visor TUI interactivo (+/- brillo, Z zoom, motores)
lumart animate clip.mp4 -o out.gif       # Transcodificar clip de video a GIF animado
lumart anim.gif --preload --loop --fps 60# Reproducción GIF a 60 FPS sin lag precargada en RAM
```

---
*¿Aún experimentas problemas? Abre un issue en GitHub: [https://github.com/SilentBlox01/Luma/issues](https://github.com/SilentBlox01/Luma/issues) adjuntando la salida de `lumart -v`.*
