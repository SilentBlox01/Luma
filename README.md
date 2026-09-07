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
[![8 Languages Supported](https://img.shields.io/badge/Languages-8%20Locales-purple.svg)](#supported-languages)

**Lumart** is an advanced terminal visual engineering suite crafted around a single core philosophy:

> **Maximum visual density and aesthetic impact within minimal terminal space.**

Unlike rudimentary ASCII converters that merely map pixel brightness to arbitrary alphanumeric characters, Lumart combines **four specialized computer vision and subpixel rendering engines** written in native multi-core C++17 (OpenMP) and optimized Python. It transforms digital photography, anime illustrations, arcade sprites, and live webcam feeds into breathtaking graphic experiences inside modern terminal emulators.

---

## Table of Contents
1. [The Four Flagship Engines](#the-four-flagship-engines)
   - [Mary Apex 3.5](#1-mary-apex-35-photorealistic-vectorial-flagship)
   - [Trumble Orelx 2.2](#2-trumble-orelx-22-retro-arcade--anime-cel-shading)
   - [Luris Mono 2.6](#3-luris-mono-26-manga-screentone--monochrome)
   - [Spectra Weep 1.4](#4-spectra-weep-14-live-webcam-streaming)
2. [Engine Comparison Matrix](#engine-comparison-matrix)
3. [Graphic Image Export & Sticker Policy](#graphic-image-export--sticker-policy)
4. [Supported Languages (8 Locales)](#supported-languages)
5. [Quick Installation & Packages](#installation)
6. [Complete CLI Reference](#complete-cli-reference)
7. [Cookbook & Practical Examples](#cookbook--practical-examples)
8. [Interactive Updates & Rollback](#interactive-updates--rollback)
9. [Desktop & System Integration](#desktop--system-integration)
10. [Under the Hood: Math & Engineering](#under-the-hood-math--engineering)
11. [Troubleshooting & Terminal Setup](#troubleshooting)
12. [License](#license)

---

## The Four Flagship Engines

Lumart avoids one-size-fits-all compromises. Different image types demand distinct artistic algorithms:

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

### 1. Mary Apex 3.5 (Photorealistic Vectorial Flagship)
* **Design Goal**: Continuous tonal micro-gradients, complex photographic lighting, and ultra-smooth portraiture.
* **C++17 Engine Core**: Multi-threaded with OpenMP and vectorized SIMD instructions (`libmary.so` shared library and `luma-mary` binary).
* **Exact Global Minimum Oklab Bipartition ($2^5 - 1 = 31$ discrete combinations evaluated per cell)**: Eliminates heuristic K-means local minima traps. Exhaustively evaluates all mathematical bipartitions of cell colors, guaranteeing the absolute global minimum $\Delta E$ in less than 700 nanoseconds per cell.
* **$O(1)$ Fast Guided Filter with Specular Boost ($L > 0.82$)**: Sharpens specular highlights in eyes, metals, water, and gloss while smoothing skin tones and sky gradients.
* **Default Unicode 13.0 Sextants 2x3**: 6 subpixels per terminal character using solid Unicode sextants (`🬀`-`🬻`, `█`, `▌`, `▐`). Also supports dual-color Braille 2x4 (`-B`), Quadrants 2x2 (`-Q`), and Half Blocks (`--blocks`).
* **Alpha Edge Isolation**: Transparent pixels are excluded from color clustering, preventing dark halos around character silhouettes.
* **Terminal Canvas Export**: Renderings saved to `.png` or `.jpg` are exported onto a dark terminal canvas (`#0c0c0c`), preserving terminal art aesthetics without looking like a downsampled image.

### 2. Trumble Orelx 2.2 (Retro-Arcade & Anime Cel-Shading)
* **Design Goal**: Anime artwork, video game sprites, comics, pop-art, and high-contrast illustrations.
* **Pre-Scaled 1-to-1 Subpixel Inking**: Rescaling occurs *before* applying bilateral filtering and Canny edge detection. Outlines are guaranteed to be exactly 1 subpixel thick at output resolution, preventing Lanczos downsampling from smudging or blurring black ink strokes.
* **32-bit Capcom CPS-2 / SNK Neo-Geo Arcade Palette**: Color punch curve (+28% chromatic vibrancy, +15% selective contrast, and unsharp masking) inspired by classic 90s coin-op fighting games.
* **Adaptive Quadrant Matching**: Lowered `shape_penalty` floor to 30 in quadrant matching, allowing diagonal and corner glyphs (`▞`, `▚`, `▘`, `▝`) to accurately follow organic anime hair and costume curves.

### 3. Luris Mono 2.6 (Manga Screentone & Monochrome C++17)
* **Design Goal**: Authentic Japanese comic book illustrations, print halftones, pen sketches, and transparent stickers.
* **Difference of Gaussians (DoG) Edge Extraction**: Generates pristine line art free of high-frequency noise, dynamically adjusting convolution radii based on terminal width.
* **Manga Screentone 2.0 (*Ami-tone*)**: Recreates physical comic printing dots using 8x8 Bayer dispersion matrices, producing paper-white highlights and rich black inks.
* **Bill Atkinson Error Diffusion (1984 MacPaint)**: The legendary error-diffusion algorithm that retains 25% residual energy, generating clean, organic tones without chaotic Floyd-Steinberg worm artifacts.
* **Exclusive Transparent Sticker Export (`--transparent`)**: Luris Mono is the **sole engine authorized to generate transparent-background PNG stickers**, ensuring crisp silhouette edges that pop over light and dark backgrounds in messaging apps.

### 4. Spectra Weep 1.4 (Live Webcam Streaming)
* **Design Goal**: Real-time live video streaming at 30-60 FPS directly in the terminal window (`lumart --webcam` or `lumart -W`).
* **Zero Latency**: Direct V4L2/OpenCV capture optimized with circular ring buffers and terminal refresh rate synchronization.
* **5 Interactive Live Shaders**:
  1. *Normal*: TrueColor adaptive photorealism.
  2. *Weep Cyberpunk*: Synthwave neon magenta and electric cyan color grading.
  3. *Matrix*: Monochrome digital phosphor rain.
  4. *Thermal FLIR*: Infrared heat-map false color (cold blue to white-hot).
  5. *Manga Ink*: High-contrast comic ink drawing in motion.

---

## Engine Comparison Matrix

| Feature | Mary Apex 3.5 | Trumble Orelx 2.2 | Luris Mono 2.6 | Spectra Weep 1.4 |
| :--- | :--- | :--- | :--- | :--- |
| **Aesthetic Focus** | Photorealistic Vectorial | Retro-Arcade / Cel-Shading | Japanese Manga / Ink | Live Video / Webcam |
| **Base Language** | C++17 OpenMP + SIMD | Python + Accelerated OpenCV | C++17 Native | Python + OpenCV V4L2 |
| **Color Space** | Perceptual Oklab ($\Delta E$) | 32-bit Capcom CPS-2 Punch | Monochrome / Ami-tone | TrueColor / RGB Shaders |
| **Default Mode** | **Sextants 2x3 (`-S`)** | **Quadrants 2x2 (`--blocks`)**| **Manga 2.0 (`-m`)** | **30-60 FPS Stream** |
| **Subpixel Density**| Up to 6 subpixels/cell | Up to 4 subpixels/cell | Up to 4 subpixels/cell | Dynamic based on cols |
| **Edge Inking** | Smooth Anti-aliasing | **Canny 1-to-1 Subpixel** | **Adaptive DoG Lineart** | Optional (Manga Shader) |
| **Export Canvas** | Terminal Canvas (`.png`, `.jpg`)| Terminal Canvas (`.png`, `.jpg`)| **PNG Stickers (`--transparent`)**| Snapshot on the fly |
| **CLI Flag** | `lumart img.jpg` *(Default)* | `lumart img.jpg -E trumble` | `lumart img.jpg -m` | `-W` or `--webcam` |

---

## Graphic Image Export & Sticker Policy

Lumart includes a built-in terminal-to-image rasterizer (`-o output.png` or `-o output.jpg`) with an Ultra-HD studio default resolution of **160 terminal columns** ($320 \times 480$ subpixels in Sextants and $320 \times 320$ in Quadrants).

### 1. Permanent Deprecation of WebP
* **The `.webp` format has been permanently disabled for export**.
* If an output path ending in `.webp` is specified, Lumart halts cleanly with an informative message advising `.png` or `.jpg`.
* Supported image formats:
  * **`.png`**: Lossless rasterization, optimized compression, and full alpha channel transparency.
  * **`.jpg` / `.jpeg`**: Universal compatibility, 95% quality rating, and optimized Huffman tables.

### 2. Transparent Stickers Exclusive to Luris Mono
* **Why don't color engines create transparent cutouts?**
  When exporting high-resolution 160-column color text over a transparent background, viewing it in standard image galleries removes the terminal frame context, creating the misleading impression of a downsampled or compressed graphic. When exported on a sleek **dark terminal canvas (`#0c0c0c`)**, it is immediately recognized as a stunning, high-definition terminal art masterwork.

> [!NOTE]
> The `--transparent` flag is **exclusive to Luris Mono** (`-m`, `-s`, `-d`). Bayer screentone patterns and DoG ink lines authentically emulate manga print cutouts, producing transparent `.png` stickers with >95% validated alpha transparency.

* If `--transparent` is supplied with Mary or Trumble, Lumart issues a helpful notice and exports the artwork with its terminal canvas to guarantee maximum color fidelity.

---

## Supported Languages

Lumart features built-in localization for **8 languages**. All CLI help strings, diagnostics, status banners, and warning messages are fully translated:

| Code | Language | Autodetection | Force via CLI |
| :---: | :--- | :--- | :--- |
| `en` | English | Automatic via `$LANG=en_*` (Default) | `lumart --lang en` |
| `es` | Español | Automatic via `$LANG=es_*` | `lumart --lang es` |
| `pt` | Português | Automatic via `$LANG=pt_*` | `lumart --lang pt` |
| `fr` | Français | Automatic via `$LANG=fr_*` | `lumart --lang fr` |
| `ru` | Русский | Automatic via `$LANG=ru_*` | `lumart --lang ru` |
| `ja` | 日本語 | Automatic via `$LANG=ja_*` | `lumart --lang ja` |
| `de` | Deutsch | Automatic via `$LANG=de_*` | `lumart --lang de` |
| `ko` | 한국어 | Automatic via `$LANG=ko_*` | `lumart --lang ko` |

---

## Installation

### Method 1: Single-Line Automatic Installer (Recommended)
Automatically detects your Linux distribution, compiles native C++ engines with OpenMP, and registers `lumart` and `luma` in your `$PATH`:
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### Method 2: Manual Clone & Install
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
chmod +x install.sh
./install.sh
```

### Method 3: Pre-built Distribution Packages
Download native packages from [GitHub Releases](https://github.com/SilentBlox01/Luma/releases):
* **Debian / Ubuntu / Pop!_OS**: `sudo apt install ./lumart-*.deb`
* **Fedora / RHEL / AlmaLinux**: `sudo dnf install ./lumart-*.rpm`
* **Arch Linux / Manjaro**: Run `makepkg -si` inside `dist/arch`

### Method 4: Manual Native C++ Compilation
To build the shared libraries and standalone C++ binaries directly:
```bash
# 1. Mary Apex 3.5 (Perceptual Oklab Engine)
g++ -O3 -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so
g++ -O3 -std=c++17 -fopenmp mary.cpp -o luma-mary

# 2. Luris Mono 2.6 (Monochrome & Manga Engine)
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono
```
*(Zero external image dependencies — built-in single-header `stb_image.h` and `stb_image_resize2.h` are included)*.

---

## Complete CLI Reference

```text
Usage: lumart [OPTIONS] <image_path_or_url>
```

### 1. Style & Character Modifiers
| Flag | Parameter | Description |
| :--- | :--- | :--- |
| `-m`, `--manga` | — | Transform artwork into Manga Screentone 2.0 (*Ami-tone* Bayer 8x8 + DoG lineart). |
| `-s`, `--sketch`| — | Transform artwork into pure line art sketch mode (clean contours). |
| `-B`, `--braille` | — | Render using Unicode Braille 2x4 (8 subpixels/cell). |
| `-Q`, `--quadrants`| — | Render using Unicode Quadrants 2x2 (4 subpixels/cell). |
| `--blocks` | — | Render using optimized half-blocks (`▀`). |

### 2. Dimensions & Visual Tuning
| Flag | Parameter | Description |
| :--- | :--- | :--- |
| `-w`, `--width` | `<int>` | Output width in columns (default: auto-fit to terminal window). |
| `--boost`, `--vibrant` | — | Apply enhanced saturation, contrast, and Retinex curves for punchy arcade output. |
| `-i`, `--invert`| — | Invert brightness mapping (essential for light-theme terminals; auto-detected in `-m`). |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Dithering algorithm for shading. |
| `--swap` | `<color1> <color2>` | Dynamically swap colors in 3D Euclidean RGB space. |

### 3. Graphic Export & Clipboard
| Flag | Parameter | Description |
| :--- | :--- | :--- |
| `-o`, `-O`, `--output` | `<file.png / .jpg>` | Rasterize and export terminal artwork to high-res image. |
| `--transparent` | — | **Luris Mono exclusive**: exports transparent-background stickers. |
| `--paste` | — | Load and render image currently in system clipboard. |

### 4. Webcam & Live Video
| Flag | Parameter | Description |
| :--- | :--- | :--- |
| `-W`, `--webcam`| `[id]` | Stream live webcam to terminal at 30-60 FPS (default ID: `0`). |

### 5. Management, History & Language
| Flag | Parameter | Description |
| :--- | :--- | :--- |
| `--lang` | `<code>` | Set display language (`en`, `es`, `pt`, `fr`, `ru`, `ja`, `de`, `ko`). |
| `-H`, `--history` | `[N]` | Display the last N commands stored in Lumart history. |
| `-R`, `--replay` | `[N]` | Re-run command N from history (default: last command). |
| `--clear-history`| — | Wipe the command history cache. |
| `--install-desktop` | — | Register "Open with Lumart" in Linux file manager context menus. |
| `-v`, `--version` | — | Show full diagnostic report of hardware, OS, and engines. |
| `-u`, `--check-update`| — | Check GitHub for newer releases. |
| `-uu`, `--upgrade` | — | Interactive upgrade assistant with automated backups. |
| `-dg`, `--downgrade` | `[ver]` | Interactive rollback selector to restore previous versions. |

---

## Cookbook & Practical Examples

### 1. High-Definition Terminal Art (Default Zero-Flag)
```bash
# Render directly at full terminal width with natural TrueColor fidelity
lumart photo.jpg

# Specify custom width in columns
lumart portrait.png -w 110

# Arcade punch with saturation & Retinex enhancement
lumart photo.jpg --boost
```

### 2. Character Texture Modes
```bash
# Smooth Braille 2x4 subpixels
lumart character.png -B

# Dense Quadrants 2x2 blocks
lumart character.png -Q

# Capcom CPS-2 / Neo-Geo half-blocks
lumart character.png --blocks -w 85
```

### 3. Transparent Japanese Manga Sticker with Luris Mono
```bash
# Create transparent PNG sticker for Discord or Telegram
lumart artwork.png -m --transparent -o manga_sticker.png

# Pure architectural pen sketch
lumart building.jpg -s -w 120

# Retro poster with Bayer ordered dithering
lumart poster.jpg -m -d bayer -w 100
```

### 4. Live Webcam Streaming in Terminal (Spectra Weep 1.4)
```bash
# Stream default webcam with real-time shader filters
lumart -W

# Stream secondary external webcam device
lumart -W 1
```

### 5. Web URLs, Clipboard, and Unix Pipelines
```bash
# Fetch and render directly from HTTPS URL
lumart https://example.com/art.png -w 80

# Render image currently copied in clipboard
lumart --paste

# Pipeline input from curl
curl -sL https://example.com/photo.jpg | lumart -
```

### 6. Dynamic Color Swapping
```bash
# Replace purple tones with bubblegum pink
lumart sprite.png --blocks --swap purple pink
```

---

## Interactive Updates & Rollback

Lumart provides complete lifecycle control directly within the CLI:

* **Check for Updates (`lumart -u`)**:
  Queries the GitHub releases API without touching local files.
* **Automated Upgrade (`lumart -uu`)**:
  Fetches the latest release, rebuilds native C++ shared libraries, and creates an automatic backup in `~/.config/luma/backup/`.
* **Instant Rollback / Downgrade (`lumart -dg`)**:
  Roll back to any previous version or local backup with an interactive menu, or specify the target version directly:
  ```bash
  lumart -dg 2.2.0
  ```

---

## Desktop & System Integration

### 1. File Manager Context Menu Integration
Run once:
```bash
lumart --install-desktop
```
Registers desktop actions allowing you to **right-click any image file** inside:
* **GNOME Files (Nautilus)**
* **KDE Dolphin**
* **Cinnamon Nemo**
* **XFCE Thunar**

Selecting *"Open with Lumart"* launches a high-definition terminal window displaying the image immediately.

### 2. Environment Diagnostics (`lumart -v`)
Inspect TrueColor support, OpenMP C++ compiler availability, active dynamic libraries (`libmary.so`, `libmonochrome.so`), terminal size, and configuration paths.

---

## Under the Hood: Math & Engineering

### 1. Perceptual Oklab Color Space & Discrete Optimization
Standard terminal tools evaluate colors in non-linear sRGB, causing muddy mid-tones and hue shifts. Mary Apex 3.5 transforms sRGB to linear RGB and projects it into **Oklab** ($L, a, b$):

$$\Delta E = \sqrt{(L_1 - L_2)^2 + (a_1 - a_2)^2 + (b_1 - b_2)^2}$$

In each Sextant cell ($2 \times 3 = 6$ subpixels), there are exactly $2^5 - 1 = 31$ unique non-trivial bipartitions. Mary evaluates all 31 bipartitions directly, guaranteeing a mathematically optimal solution with zero stochastic noise.

### 2. Trumble 1-to-1 Pre-Scaled Inking
Downsampling high-resolution edge maps with Lanczos blends 1-pixel dark lines into light backgrounds, causing lines to disappear. Trumble Orelx rescales the source image to the exact subpixel resolution ($target\_width \times 2$) *before* computing Canny gradients, ensuring lines maintain a crisp 1-subpixel thickness.

### 3. ECMA-48 ANSI Escape Code Optimizer
Lumart tracks active terminal styling state (`current_fg`, `current_bg`). Redundant color codes are omitted for adjacent cells with matching colors, shrinking ANSI output payloads by up to **45%** and speeding up SSH rendering.

---

## Troubleshooting

### 1. Colors appear washed out or banding occurs
* Ensure your terminal supports TrueColor (24-bit). In your shell profile (`.bashrc` / `.zshrc`):
  ```bash
  export COLORTERM=truecolor
  ```
* Recommended full TrueColor terminals: **Kitty**, **Alacritty**, **WezTerm**, **iTerm2**, **Foot**, **GNOME Terminal**, **Konsole**, **Windows Terminal**.

### 2. Sextants (`-S`) or Braille (`-B`) show missing character boxes
* Install a monospaced font with full Unicode 13.0 symbol coverage:
  * **Symbols Nerd Font** / **JetBrains Mono Nerd Font**
  * **DejaVu Sans Mono**
  * **Cascadia Code**

### 3. Clean Uninstallation
```bash
./uninstall.sh
# Or via package manager:
sudo apt remove lumart     # Debian/Ubuntu
sudo dnf remove lumart     # Fedora
sudo pacman -Rns lumart    # Arch Linux
```

---

## License

Lumart is released under the GNU Affero General Public License v3.0 (**AGPL-3.0**). See the `LICENSE` file for full terms and conditions.
