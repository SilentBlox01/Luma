# 🔧 Guía Maestra de Solución de Problemas (Troubleshooting) y Manual Técnico de Lumart (Luma) v2.5.0

[English](TROUBLESHOOTING.md) | [Español (Predeterminado)](TROUBLESHOOTING.es.md) | [Português](TROUBLESHOOTING.pt.md) | [Français](TROUBLESHOOTING.fr.md) | [Deutsch](TROUBLESHOOTING.de.md) | [Русский](TROUBLESHOOTING.ru.md) | [日本語](TROUBLESHOOTING.ja.md) | [한국어](TROUBLESHOOTING.ko.md)

> **El Documento Maestro Insignia de Lumart (Luma)**: Listas de diagnóstico rápido, guía visual "Lo que se debe y no se debe hacer", física del terminal, inmersión técnica en los cuatro motores de renderizado, subcomandos especializados, enciclopedia completa de opciones, recetas prácticas y resolución exhaustiva de problemas técnicos.

---

## 📑 Tabla de Contenidos
1. [Lista Rápida de Diagnóstico (Síntomas y Soluciones)](#1-lista-rápida-de-diagnóstico-síntomas-y-soluciones)
   - [1.1 Guía Visual "Lo que se DEBE y NO se debe hacer" (Dos & Don'ts)](#11-guía-visual-lo-que-se-debe-y-no-se-debe-hacer-dos--donts)
2. [Instalación y Resolución de Dependencias Nativas C++](#2-instalación-y-resolución-de-dependencias-nativas-c)
3. [Compatibilidad de Emuladores de Terminal y Tipografías](#3-compatibilidad-de-emuladores-de-terminal-y-tipografías)
4. [Fidelidad de Color y TrueColor de 24 Bits (ANSI ECMA-48)](#4-fidelidad-de-color-y-truecolor-de-24-bits-ansi-ecma-48)
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
8. [Exportación Gráfica de Alta Definición y Stickers (-o, --loop, --preload)](#8-exportación-gráfica-de-alta-definición-y-stickers--o---loop---preload)
9. [Configuración, Persistencia y Localización (i18n)](#9-configuración-persistencia-y-localización-i18n)
10. [Historial de Comandos y Reproducción Interactiva (-H, -R)](#10-historial-de-comandos-y-reproducción-interactiva--h--r)
11. [Sistema de Actualizaciones, Mejoras y Rollback (-u, -uu, -dg)](#11-sistema-de-actualizaciones-mejoras-y-rollback--u--uu--dg)
12. [Integración con el Escritorio y Gestores de Archivos de Linux (--install-desktop)](#12-integración-con-el-escritorio-y-gestores-de-archivos-de-linux---install-desktop)
13. [Recetas Prácticas del Mundo Real y Flujos de Trabajo](#13-recetas-prácticas-del-mundo-real-y-flujos-de-trabajo)
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

| Aspecto | ✅ Lo que se DEBE hacer | ❌ Lo que NO se debe hacer |
| :--- | :--- | :--- |
| **Fotografías y TrueColor** | **SÍ** usa **Mary Apex 3.5** (`lumart foto.jpg`) para retratos y paisajes realistas con espacio Oklab y Sextantes 2x3. | **NO** fuerces `--blocks` o `--boost` en fotos delicadas a menos que busques un estilo retro saturado explícito. |
| **Arcade y Cel-Shading** | **SÍ** usa **Trumble Orelx 2.2** (`lumart arte.png -E trumble --boost`) para pósteres estilo Capcom CPS-2 / Neo-Geo. | **NO** esperes gradientes suaves de Trumble; está diseñado para líneas de cómic duras y bloques posterizados. |
| **Manga Tradicional** | **SÍ** usa **Luris Mono 2.6** (`lumart manga.jpg -m`) para tramas físicas *Ami-tone* y líneas de entintado DoG. | **NO** uses herramientas genéricas que desordenan caracteres ASCII al azar; Luris utiliza matrices de Bayer matemáticamente ordenadas. |
| **Ajuste de Pantalla** | **SÍ** usa `-F` (`--fit`) para ajustar la imagen a la ventana exacta sin scroll ni desbordamiento:<br>`lumart arte.jpg -F` | **NO** combines `-F` y `-w` en el mismo comando:<br>`lumart arte.jpg -F -w 80` ❌ *(Lumart se detendrá con error de incompatibilidad).* |
| **Fastfetch / Dashboards** | **SÍ** usa `-w 36..42` con `--fastfetch` para recortar márgenes vacíos e integrar el logo en barras laterales. | **NO** uses `-w` mayor al ancho de tu terminal, ya que forzará saltos de línea y destruirá la alineación. |
| **Stickers Transparentes** | **SÍ** usa Luris Mono con `--transparent -o sticker.png` para exportar a Discord/Telegram. | **NO** uses motores en color para stickers transparentes; los caracteres TrueColor requieren fondo de terminal sólido. |

---

## 2. Instalación y Resolución de Dependencias Nativas C++

### 2.1 Método 1: Instalador Automático de un Solo Comando (Recomendado)
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### 2.2 Método 2: Gestores de Paquetes de Distribución (AUR, APT, DNF)
* **Arch Linux / Manjaro (AUR)**:
  ```bash
  yay -S lumart
  # o bien: paru -S lumart
  ```
* **Debian / Ubuntu / Linux Mint (`.deb`)**:
  ```bash
  sudo apt install ./dist/deb/lumart_2.5.0-1_all.deb
  ```
* **Fedora / RHEL / AlmaLinux (`.rpm`)**:
  ```bash
  sudo dnf install ./dist/rpm/lumart-2.5.0-1.noarch.rpm
  ```

### 2.3 Compilación Manual de Librerías C++
Si deseas compilar manualmente las librerías nativas con vectorización SIMD:
```bash
# 1. Compilar Mary Apex 3.5 (Color Perceptual Oklab)
g++ -O3 -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so
g++ -O3 -std=c++17 -fopenmp mary.cpp -o luma-mary

# 2. Compilar Luris Mono 2.6 (Monocromático, Manga y Bocetos)
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono
```

---

## 3. Compatibilidad de Emuladores de Terminal y Tipografías

* **Emuladores de Rendimiento Máximo (Recomendados):**
  - **Ghostty**: Renderizado nativo por GPU, TrueColor perfecto y soporte completo de Unicode.
  - **Kitty**: Aceleración por GPU, excelente soporte de fuentes ligadas y secuencias de escape.
  - **Alacritty**: Motor OpenGL ultrarrápido con soporte completo de TrueColor.
  - **WezTerm**: Soporte completo de fuentes Nerd Font y renderizado de glifos complejos.
* **Tipografías Recomendadas:**
  - `JetBrains Mono Nerd Font` (La más recomendada para arte ANSI y densidad geométrica).
  - `FiraCode Nerd Font`
  - `Cascadia Code Nerd Font`
  - `Hack Nerd Font`

---

## 4. Fidelidad de Color y TrueColor de 24 Bits (ANSI ECMA-48)

Lumart genera secuencias de escape ANSI conformes al estándar ECMA-48 en formato TrueColor (16.7 millones de colores):
* Primer plano (Foreground): `[38;2;R;G;Bm`
* Fondo (Background): `[48;2;R;G;Bm`

Si los colores se ven apagados o con bandas de 16 colores:
1. Comprueba si tu terminal tiene activada la variable TrueColor:
   ```bash
   echo $COLORTERM
   ```
2. Si está vacía, añade a tu `~/.bashrc` o `~/.zshrc`:
   ```bash
   export COLORTERM=truecolor
   ```
3. **Uso dentro de Tmux**: Añade a tu `~/.tmux.conf` para permitir el paso de secuencias TrueColor:
   ```tmux
   set -g default-terminal "tmux-256color"
   set -ga terminal-overrides ",*256col*:Tc"
   ```

---

## 5. Los Cuatro Motores Insignia (Inmersión Técnica y Arquitectura)

### 5.1 Mary Apex 3.5 (Color Perceptual Oklab y Micro-Bloques Subpíxel)
* **Comando Insignia**: `lumart foto.jpg` (o `lumart foto.jpg -E mary -S`)
* **Tecnología**:
  1. Convierte píxeles al espacio uniforme **Oklab** ($\Delta E$).
  2. K-Means de 3 iteraciones combinado con la función de sensibilidad al contraste humana (**CSF de Weber-Fechner**).
  3. Micro-bloques Sextantes $2 	imes 3$ (6 subpíxeles por celda).

### 5.2 Trumble Orelx 2.2 (Cel-Shading Retro-Arcade y Entintado Anime)
* **Comando Insignia**: `lumart arte.png -E trumble --boost`
* **Tecnología**:
  1. Máscara Laplaciana para extracción de bordes de entintado tipo G-Pen.
  2. Sombreado cel-shading arcade con tramado ordenado Bayer.

### 5.3 Luris Mono 2.6 (Manga Screentone Monocromático y Stickers Transparentes)
* **Comando Insignia**: `lumart manga.jpg -m` (o `-s`, `-ch`)
* **Tecnología**:
  1. Tramado de semitonos *Ami-tone* Bayer $8 	imes 8$.
  2. Bocetos limpios Difference of Gaussians (DoG) sin manchas negras.
  3. Tramado cruzado auténtico a $45^\circ$ y $-45^\circ$ con 6 niveles de densidad de pluma.
  4. **Exportación exclusiva de stickers transparentes**:
     ```bash
     lumart personaje.png -m --transparent -o sticker.png
     ```

### 5.4 Spectra Weep 2.0 (Video en Vivo, Cámara Web y 12 Shaders)
* **Comando Insignia**: `lumart -E spectra` (o `lumart --webcam`, `lumart -W`, `lumart clip.mp4`, `lumart imagen.png --shader neon`)
* **Tecnología**:
  1. Pipeline de video OpenCV sin latencia (30–60 FPS).
  2. **12 Shaders Multiespectrales**:
     - `neon`: Resplandor cyberpunk synthwave con realce de bordes.
     - `thermal`: Visión térmica infrarroja militar FLIR.
     - `tron`: Líneas vectoriales brillantes en azul y cian.
     - `matrix`: Código digital Katakana + fósforo verde P1 (525nm).
     - `amber`: Terminal clásica ámbar de fósforo de los años 70.
     - `hologram`: Interferencia holográfica electromagnética.
     - `glitch`: Aberración cromática RGB con desfase aleatorio.
     - `phosphor-bloom`: Resplandor analógico difuso de tubo CRT.
     - `solarize`, `manga`, `theme`, `normal`.
  3. **Reproducción directa de video**: Reproduce cualquier archivo `.mp4`, `.mkv`, `.webm` o `.mov` en el terminal a framerates nativos.

---

## 6. Subcomandos Especializados y Herramientas Integradas

### 6.1 `lumart fetch` (Generador de Presets para Fastfetch / Neofetch)
```bash
lumart fetch <imagen.png> [-w ANCHO]
```
- Recorta automáticamente márgenes transparentes (`--fastfetch`).
- Renderiza en medios bloques TrueColor de 24 bits (`▀`).
- Guarda el archivo en `~/.config/fastfetch/<nombre>_logo.ans`.
- Imprime el bloque JSON listo para copiar a `~/.config/fastfetch/config.jsonc`.

### 6.2 `lumart bench` (Banco de Pruebas de Rendimiento y Latencia Multi-Núcleo)
```bash
lumart bench [imagen.png] [-w ANCHO]
```
- Mide latencia (`ms`), throughput (`MP/s`) y `FPS` en todos los motores.

### 6.3 `lumart showcase` (Lienzo Comparativo 4-en-1)
```bash
lumart showcase <imagen.png> [-w ANCHO] [-o comparativa.png]
```
- Divide la pantalla en 4 cuadrantes comparando Mary, Trumble, Luris y Spectra lado a lado.

### 6.4 `lumart info` (Inspector Visual y Recomendador de Motores)
```bash
lumart info <imagen.png>
```
- Reporta resolución, luminancia, relación de aspecto, 6 colores dominantes HEX/ANSI y el mejor motor recomendado.

### 6.5 `lumart diff` (Mapa de Calor Cromático Delta entre Dos Imágenes)
```bash
lumart diff <img1.png> <img2.png> [-w ANCHO]
```
- Calcula diferencias cromáticas píxel a píxel con mapa de calor y variación media $\Delta E$.

### 6.6 `lumart slideshow` (Pase de Diapositivas en Pantalla Completa en Terminal)
```bash
lumart slideshow <carpeta/> [--delay 3.0] [-w ANCHO]
```
- Proyecta imágenes en pantalla completa con controles de teclado (`Espacio`, flechas, `Q`).

### 6.7 `lumart -I` / `--interactive` (Visor TUI Interactivo)
```bash
lumart -I <imagen.png>
```
- Interfaz interactiva con controles en vivo para brillo (`+/-`), motores (`M/T/L`), modo manga (`G`) y zoom (`Z`).

### 6.8 `lumart animate` (Transcodificador de GIFs y Compilador de Video)
```bash
lumart animate <clip.mp4 | carpeta_frames/> -o resultado.gif [--fps 30]
```
- Convierte videos o secuencias de imágenes en GIFs animados optimizados.

---

## 7. Dimensiones, Relación de Aspecto y Calibración de Fuente (--font-ratio)

Las celdas de caracteres de texto del terminal no son cuadradas; miden aproximadamente el doble de alto que de ancho ($1:2$).
* Calibra con `--font-ratio <decimal>` si tu fuente no es estándar:
  ```bash
  lumart foto.png --font-ratio 0.45  # Fuentes muy altas y estrechas
  lumart foto.png --font-ratio 0.55  # Fuentes anchas o cuadradas
  ```

---

## 8. Exportación Gráfica de Alta Definición y Stickers (-o, --loop, --preload)

* **Exportar a archivo de imagen de alta resolución:**
  ```bash
  lumart imagen.png -w 120 -o arte.png
  ```
* **Stickers transparentes:** Exclusivo de Luris Mono:
  ```bash
  lumart anime.png -m --transparent -o sticker.png
  ```
* **Precarga total en RAM para 60 FPS sin lag:**
  ```bash
  lumart animacion.gif -w 70 --loop --fps 60 --preload
  ```

---

## 9. Configuración, Persistencia y Localización (i18n)

Lumart soporta 8 idiomas de forma nativa con persistencia de configuración en `~/.config/lumart/config.json`:
```bash
lumart --lang es        # Cambiar a español
lumart --lang en        # Cambiar a inglés
lumart --lang pt        # Cambiar a portugués
lumart --lang fr        # Cambiar a francés
lumart --lang de        # Cambiar a alemán
lumart --lang ru        # Cambiar a ruso
lumart --lang ja        # Cambiar a japonés
lumart --lang ko        # Cambiar a coreano
```

---

## 10. Historial de Comandos y Reproducción Interactiva (-H, -R)

* **Ver historial:** `lumart -H` (o `lumart -H 10` para los últimos 10).
* **Re-ejecutar último comando:** `lumart -R`
* **Re-ejecutar comando específico:** `lumart -R 3`
* **Limpiar historial:** `lumart --clear-history`

---

## 11. Sistema de Actualizaciones, Mejoras y Rollback (-u, -uu, -dg)

* **Comprobar si hay versiones nuevas:** `lumart -u`
* **Actualizar a la última versión:** `lumart -uu`
* **Revertir a la versión anterior (Rollback):** `lumart -dg`

---

## 12. Integración con el Escritorio y Gestores de Archivos de Linux (--install-desktop)

```bash
lumart --install-desktop
```
Registra *"Abrir con Lumart"* en el menú contextual de clic derecho en GNOME Files (Nautilus), Nemo, Dolphin y Thunar.

---

## 13. Recetas Prácticas del Mundo Real y Flujos de Trabajo

### Receta 1: El Logo Perfecto para Fastfetch / Neofetch
```bash
# Opción A: Bloques TrueColor (Recomendada)
lumart fetch "avatar.png" -w 38

# Opción B: Manga Screentone minimalista
lumart "avatar.png" -w 38 --fastfetch -m -o ~/.config/fastfetch/logo_manga.ans

# Opción C: Puntos Braille 2x4
lumart "avatar.png" -w 38 --fastfetch -E mary -B -o ~/.config/fastfetch/logo_braille.ans
```
*Probar en el terminal:*
```bash
fastfetch --logo ~/.config/fastfetch/avatar_logo.ans --logo-type file
```

### Receta 2: Stickers de Anime Transparentes para Discord / Telegram
```bash
lumart "personaje.png" -w 80 -m --transparent -o sticker.png
lumart "personaje.png" -w 80 -m -r --bg-tolerance 40 --transparent -o sticker_limpio.png
```

### Receta 3: GIFs Animados a 60 FPS con Precarga en RAM
```bash
lumart "animacion.gif" -w 70 --loop --fps 60 --preload
lumart "animacion.gif" -w 60 --theme synthwave --fps 30 -o anim_synthwave.gif
```

### Receta 4: Cámara Web en Vivo Estilo Cyberpunk Matrix CRT
```bash
lumart -W 0 --matrix --crt green --fps 60
lumart -W 0 --shader thermal --fps 30
```

### Receta 5: Automatización en Scripts Bash, Pipelines y MOTD
```bash
# Banner en ~/.bashrc:
if command -v lumart &>/dev/null; then
    lumart ~/.config/banner.png -w 60 --border rounded --align center --instant
fi

# Renderizar desde URL web:
lumart "https://raw.githubusercontent.com/fastfetch-cli/fastfetch/dev/assets/arch.png" -w 50

# Renderizar imagen del portapapeles:
lumart --paste -w 60 --border double

# Copiar arte ANSI al portapapeles:
lumart "logo.png" -w 40 -C
```

---

## 14. Enciclopedia Completa de Opciones y Flags de la Línea de Comandos

### A. Motores y Texturas de Glifos
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | *auto* | Selecciona el motor de renderizado explícitamente. |
| `-S`, `--sextants`| — | *activo* | Bloques Sextantes Unicode 2x3 (Mary Apex por defecto, 6 subpíxeles/celda). |
| `-B`, `--braille` | — | `false` | Matriz Braille Unicode 2x4 (8 subpíxeles/celda, máxima definición de curvas). |
| `-Q`, `--quadrants`| — | `false` | Bloques Cuadrantes Unicode 2x2 (4 subpíxeles/celda). |
| `--blocks` | — | `false` | Medios bloques optimizados (`▀` / `▄`, 2 píxeles verticales/celda en TrueColor). |
| `-m`, `--manga` | — | `false` | Modo Manga Screentone (*Ami-tone* Bayer 8x8 + trazos limpios DoG). |
| `-s`, `--sketch`| — | `false` | Modo boceto limpio a lápiz sin manchas oscuras parásitas. |
| `-ch`, `--crosshatch`| — | `false` | Tramado cruzado a pluma a 45 grados con 6 niveles perpendiculares de densidad. |
| `-cs`, `--charset` | `<nombre>` | `standard` | Rampa tipográfica de caracteres: `dense`, `standard`, `blocks`, `math`, `runes`, `katakana`, `crosshatch`. |
| `--matrix` | — | `false` | Transforma el arte en código Matrix Katakana con fósforo verde P1 (525nm). |
| `--matrix-rain` | — | `false` | Modo animación de lluvia digital Matrix descendente en el terminal. |

### B. Geometría, Dimensiones y Encuadre
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-w`, `--width` | `<int>` | *terminal* | Ancho de salida en columnas (incompatible con `-F`). |
| `-F`, `--fit` | — | `false` | **Auto-ajuste al viewport**: calcula ancho y alto para caber en la ventana sin scroll. |
| `--fastfetch`, `--logo` | — | `false` | Recorta automáticamente márgenes transparentes/vacíos para logos compactos. |
| `--font-ratio` | `<float>` | `0.5` | Factor de proporción ancho/alto de la tipografía del terminal. |
| `--crop` | `"x,y,w,h"` | `None` | Recorta una región específica antes de renderizar (ej. `--crop "100,50,400,400"`). |
| `--zoom` | `<float>` | `1.0` | Factor de zoom o magnificación digital (ej. `--zoom 1.5` para 150%). |
| `--rotate` | `0` \| `90` \| `180` \| `270` | `0` | Rotación en grados en sentido horario. |
| `--flip`, `--mirror` | `h` \| `v` | `None` | Espejado geométrico: horizontal (`h`) o vertical (`v`). |
| `--border` | `rounded` \| `single` \| `double` \| `heavy` \| `ascii` \| `blocks` | `None` | Enmarca el arte en un marco decorativo Unicode. |
| `--align` | `left` \| `center` \| `right` | `left` | Alineación horizontal en el viewport de la terminal. |
| `--center` | — | `false` | Alias rápido para `--align center`. |

### C. Colorimetría, Shaders y Parámetros Visuales
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-c`, `--color` | — | `true` | Fuerza salida en modo color TrueColor de 24 bits. |
| `--no-color` | — | `false` | Desactiva el color ANSI y enruta al motor monocromático. |
| `--brightness` | `<float>` | `1.0` | Multiplicador de brillo (ej. `1.2` para iluminar, `0.8` para oscurecer). |
| `--contrast` | `<float>` | `1.0` | Multiplicador de contraste tonal (ej. `1.3` para intensificar luces y sombras). |
| `--saturation` | `<float>` | `1.0` | Multiplicador de saturación cromática (ej. `1.4` para colores vivos, `0.0` escala de grises). |
| `--boost`, `--vibrant` | — | `false` | Aplica curvas de saturación, contraste y realce Retinex estilo arcade. |
| `--gamma` | `<float>` | `1.0` | Corrección gamma no lineal de tonos medios. |
| `-i`, `--invert`| — | `false` | Invierte la luminosidad de los caracteres (útil para terminales claras). |
| `--swap` | `<c1> <c2>` | `None` | Intercambia dos colores en caliente en espacio 3D RGB. |
| `--theme`, `--palette` | `<nombre>` | `None` | Aplica paleta cromática seleccionada: `cyberpunk`, `dracula`, `nord`, `catppuccin`, `gruvbox`, `synthwave`, `monokai`, `gameboy`, `amber`. |
| `--crt`, `--scanlines` | `green` \| `amber` \| `color` \| `scanlines` | `None` | Simulación analógica de monitor CRT vintage con scanlines. |
| `--shader` | `<nombre>` | `None` | Shaders multiespectrales: `neon`, `cyberpunk`, `thermal`, `tron`, `matrix`, `amber`, `manga`, `hologram`, `glitch`, `phosphor-bloom`, `solarize`. |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | *auto* | Algoritmo de tramado para simulación de gradientes. |

### D. Animación, GIFs y Framerates
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--loop` | — | `false` | Reproducción continua en bucle en el terminal para archivos GIF o APNG. |
| `--fps`, `--target-fps` | `<float>` | *del gif* | Tasa de fotogramas objetivo para reproducción o exportación GIF (ej. `--fps 60`). |
| `--preload`, `--smooth` | — | `false` | **Precarga total en RAM**: pre-renderiza todos los fotogramas en memoria para **60 FPS fluidos con 0 ms de lag**. |
| `--instant`, `--no-reveal`| — | `true` | Muestra la salida inmediatamente sin animación progresiva. |
| `--reveal` | — | `false` | Efecto nostálgico de escaneo progresivo línea por línea. |

### E. Exportación Gráfica, Stickers y Portapapeles
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-o`, `-O`, `--save` | `<archivo.png / .jpg / .gif>` | `None` | Exporta a imagen gráfica de alta resolución o GIF animado. |
| `--transparent` | — | `false` | **Exclusivo de Luris Mono**: genera stickers recortados con fondo transparente (sin cuadro negro). |
| `-r`, `--remove-bg` | — | `false` | Eliminación inteligente de fondo por inundación cromática perceptual. |
| `--bg-tolerance` | `<1-100>` | `32` | Umbral de tolerancia de color para recorte de fondo. |
| `-C`, `--copy` | — | `false` | Copia el arte ANSI (con códigos de color) directamente al portapapeles. |
| `--copy-plain` | — | `false` | Copia el texto ASCII puro y limpio (sin colores ANSI) al portapapeles. |
| `--paste` | — | `false` | Lee y procesa automáticamente la imagen presente en el portapapeles (Ctrl+C). |

### F. Video y Cámara Web
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `-W`, `--webcam`| `[id]` | `0` | Transmite vídeo de cámara web en vivo a 30-60 FPS (0 = integrada, 1 = externa). |
| `<video.mp4>` | `<archivo>` | `None` | Reproduce directamente archivos de vídeo (`.mp4`, `.mkv`, `.webm`, `.mov`) en el terminal. |

### G. Administración, Historial e Idioma
| Flag | Parámetro | Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `--lang` | `<código>` | *auto* | Configura el idioma de la interfaz (`es`, `en`, `pt`, `fr`, `ru`, `ja`, `de`, `ko` o nombres como `spanish`). |
| `-H`, `--history` | `[N]` | `10` | Muestra los últimos N comandos ejecutados en el historial de Lumart. |
| `-R`, `--replay` | `[N]` | *último* | Re-ejecuta de inmediato el comando N del historial (por defecto: el último). |
| `--clear-history`| — | `false` | Vacía por completo el archivo de historial de comandos. |
| `--install-desktop` | — | `false` | Registra la acción *"Abrir con Lumart"* en el menú contextual de Linux. |
| `--completions` | `bash` \| `zsh` \| `fish` | `None` | Genera scripts de autocompletado para la shell correspondiente. |
| `-v`, `--version` | — | `false` | Muestra el panel diagnóstico completo de hardware, SO y motores C++ nativos. |
| `-u`, `--check-update`| — | `false` | Comprueba si existe una versión más reciente en GitHub. |
| `-uu`, `--upgrade` | `opcional` | `latest` | Asistente interactivo de actualización a la última versión con backup. |
| `-dg`, `--downgrade` | `opcional` | `prev` | Selector interactivo de restauración a versiones previas. |

---

## 15. Referencia Maestra de Comandos y Hoja de Trucos

```bash
# ==============================================================================
# 1. VERSIÓN, DIAGNÓSTICO DEL SISTEMA Y LOCALIZACIÓN
# ==============================================================================
lumart -v                                # Diagnóstico completo de hardware, SO y motores C++
lumart --lang es                         # Fijar idioma a Español
lumart --lang en                         # Fijar idioma a Inglés
lumart --lang pt                         # Fijar idioma a Portugués
lumart --lang fr                         # Fijar idioma a Francés
lumart --lang de                         # Fijar idioma a Alemán
lumart --lang ru                         # Fijar idioma a Ruso
lumart --lang ja                         # Fijar idioma a Japonés
lumart --lang ko                         # Fijar idioma a Coreano

# ==============================================================================
# 2. MARY APEX 3.5 (COLOR PERCEPTUAL OKLAB) — PREDETERMINADO O EXPLÍCITO
# ==============================================================================
lumart foto.png                          # Mary Sextantes HD + TrueColor natural (Zero-Flag)
lumart foto.png -E mary -S               # Invocación explícita (mismo resultado)
lumart foto.png -B                       # Caracteres Braille 2x4 dual-color TrueColor
lumart foto.png -Q                       # Bloques Cuadrantes 2x2
lumart foto.png --blocks                 # Medios bloques (▀ / ▄)
lumart foto.png --boost                  # Realce de saturación arcade + Retinex
lumart foto.png -c                       # Forzar salida TrueColor (predeterminado)
lumart foto.png --no-color               # Desactivar color y enrutar a monocromático
lumart foto.png --font-ratio 0.45        # Calibrar relación de aspecto de la fuente
lumart foto.png --reveal                 # Animación progresiva línea por línea
lumart foto.png --instant                # Salida instantánea sin animación (predeterminado)

# ==============================================================================
# 3. TRUMBLE ORELX 2.2 (CEL-SHADING RETRO-ARCADE)
# ==============================================================================
lumart anime.png -E trumble --blocks     # Renderizado en bloques cel-shaded estilo arcade
lumart anime.png --boost                 # Saturación arcade Capcom CPS-2 / Neo-Geo + Inking
lumart anime.png -d bayer                # Tramado ordenado Bayer 8x8
lumart anime.png --swap purple pink      # Intercambio de colores dinámico en 3D RGB

# ==============================================================================
# 4. LURIS MONO 2.6 (MANGA MONOCROMÁTICO Y STICKERS)
# ==============================================================================
lumart manga.png -E luris -m             # Modo Manga Screentone explícito (DoG + Bayer)
lumart boceto.png -s                     # Boceto limpio a lápiz de líneas puras DoG
lumart foto.png -d atkinson              # Tramado MacPaint 1984 de Bill Atkinson
lumart foto.png -d floyd                 # Tramado de difusión de error Floyd-Steinberg
lumart anime.png -i                      # Invertir luminosidad (para fondos claros)
lumart waifu.png -m --transparent -o sticker.png  # ¡Sticker recortado transparente!

# ==============================================================================
# 5. SPECTRA WEEP 2.0 (VIDEO Y CÁMARA WEB EN TIEMPO REAL)
# ==============================================================================
lumart -E spectra                        # Transmitir cámara web vía selector de motor
lumart --webcam                          # Transmitir cámara web predeterminada (/dev/video0)
lumart -W 1                              # Transmitir cámara web secundaria (/dev/video1)
lumart video.mp4                         # Reproducir archivo de video en la terminal

# ==============================================================================
# 6. SHADERS AVANZADOS v2.5.0, CRT Y LLUVIA MATRIX
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
# 7. SUBCOMANDOS ESPECIALIZADOS
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

# ==============================================================================
# 8. EXPORTACIÓN GRÁFICA A ARCHIVO
# ==============================================================================
lumart imagen.png -w 120 -o arte.png     # Exportar imagen de alta resolución en PNG
lumart imagen.png --blocks -o arte.jpg   # Exportar imagen de alta resolución en JPG

# ==============================================================================
# 9. HISTORIAL Y REPRODUCCIÓN
# ==============================================================================
lumart -H                                # Ver historial completo de ejecución
lumart -H 10                             # Ver los últimos 10 comandos
lumart -R                                # Re-ejecutar el último comando
lumart -R 3                              # Re-ejecutar el comando #3 del historial
lumart --clear-history                   # Vaciar el archivo de historial

# ==============================================================================
# 10. ACTUALIZACIONES E INTEGRACIÓN CON EL ESCRITORIO
# ==============================================================================
lumart -u                                # Comprobar actualizaciones en GitHub sin instalar
lumart -uu                               # Descargar e instalar la última versión
lumart -dg                               # Revertir a la versión anterior desde backup
lumart --install-desktop                 # Instalar lanzador de escritorio y menús de clic derecho
lumart --paste                           # Cargar y renderizar imagen del portapapeles
```

---
*¿Aún experimentas problemas? Abre un issue en GitHub: [https://github.com/SilentBlox01/Luma/issues](https://github.com/SilentBlox01/Luma/issues) adjuntando la salida de `lumart -v`.*
