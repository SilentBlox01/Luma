# 🔧 Luma Comprehensive Troubleshooting & Deep Technical Guide

Welcome to the definitive troubleshooting, architectural reference, and operational manual for **Luma** (and `lumart`). This guide provides in-depth solutions to common issues, terminal emulator compatibility benchmarks, native C++ compilation guides, rendering engine mechanics, localization configuration, and internal architectural details.

---

## 📑 Table of Contents
1. [Quick Diagnostic Checklist](#1-quick-diagnostic-checklist)
2. [Installation & Native C++ Dependency Resolution](#2-installation--native-c-dependency-resolution)
3. [Terminal Emulators & Font Compatibility](#3-terminal-emulators--font-compatibility)
4. [Color Fidelity & TrueColor (24-bit ANSI)](#4-color-fidelity--truecolor-24-bit-ansi)
5. [The Four Flagship Rendering Engines (Deep Dive & Troubleshooting)](#5-the-four-flagship-rendering-engines)
   - [Mary Apex 3.5 (Perceptual Oklab & Subpixel Micro-Blocks)](#51-mary-apex-35-perceptual-oklab--subpixel-micro-blocks)
   - [Trumble Orelx 2.2 (Retro-Arcade Cel-Shading & Anime Ink)](#52-trumble-orelx-22-retro-arcade-cel-shading--anime-ink)
   - [Luris Mono 2.6 (Monochrome Manga Screentone & Transparent Stickers)](#53-luris-mono-26-monochrome-manga-screentone--stickers)
   - [Spectra Weep 1.4 (Real-Time Live Webcam Streaming)](#54-spectra-weep-14-real-time-live-webcam-streaming)
6. [Sizing, Aspect Ratio & Character Font Calibration](#6-sizing-aspect-ratio--font-calibration)
7. [High-Definition Graphic Image & Sticker Export (`-o`)](#7-high-definition-graphic-image--sticker-export)
8. [Configuration, Persistence & Localization (i18n)](#8-configuration-persistence--localization-i18n)
9. [Command History & Interactive Replay System (`-H`, `-R`)](#9-command-history--interactive-replay-system)
10. [Updates, Upgrades & Rollback System (`-u`, `-uu`, `-dg`)](#10-updates-upgrades--rollback-system)
11. [Linux Desktop & File Manager Integration (`--install-desktop`)](#11-linux-desktop--file-manager-integration)
12. [Master Command Reference & Cheat Sheet](#12-master-command-reference--cheat-sheet)

---

## 1. Quick Diagnostic Checklist

If an image looks distorted, pixelated, fails to render, or displays unexpected output, consult this quick reference:

| Symptom | Primary Cause | Immediate Resolution |
| :--- | :--- | :--- |
| `command not found: luma` or `lumart` | `~/.local/bin` is missing from `$PATH` | Run `./install.sh` or add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc` / `~/.zshrc`. |
| `error: externally-managed-environment` | PEP 668 restriction on Fedora, Debian, or Ubuntu | Install native system packages: `sudo dnf install python3-pillow` / `sudo apt install python3-pil`, or run `./install.sh`. |
| Braille dots or blocks look like `?`, ``, or empty boxes | Active terminal font lacks Unicode glyph coverage | Switch to a Nerd Font (JetBrains Mono Nerd Font, Fira Code, Cascadia Code). |
| Horizontal black gaps cutting through Braille characters | Terminal emulator line-height / row spacing is greater than `1.0` | Set terminal line-height / padding offset to `1.0` or `0px` in terminal config. |
| Washed-out colors or harsh 16-color banding | Terminal emulator does not advertise or support 24-bit TrueColor | Verify `$COLORTERM` (`echo $COLORTERM`) or switch to Ghostty, Kitty, Alacritty, or WezTerm. |
| Output wraps around lines and looks shredded | Specified render width (`-w`) exceeds terminal columns | Reduce width with `-w 90` or dynamically fit with `-w $(tput cols)`. |
| Braille or Monochrome output looks like an inverted photographic negative | Terminal background is light (white/cream) instead of dark | Luris Mono auto-detects white backgrounds and inverts automatically. For manual override: add `-i` / `--invert`. |
| Mary or Luris running on Python fallback instead of C++ | C++ shared libraries (`libmary.so`, `libmonochrome.so`) not compiled | Install `g++` (`build-essential` / `gcc-c++`) and run `make -f Makefile.native` or `./install.sh`. |
| `OpenCV required for Spectra engine` error | `opencv-python` is not installed | Install via your system package manager (`python3-opencv`) or `pip install opencv-python`. |
| Web camera fails to open in Spectra mode (`-W`) | Missing camera permissions or incorrect `/dev/video*` index | Add user to video group: `sudo usermod -aG video $USER`, or specify camera index: `lumart -W 1`. |
| Transparent sticker output (`--transparent`) has black background | Transparent alpha is only supported in Luris Mono engine with `.png` | Run `lumart image.png -m --transparent -o sticker.png`. Color models export with solid terminal background. |
| WebP export rejected with error | WebP export was permanently disabled to protect visual quality | Export to `.png` or `.jpg` instead (`-o output.png`). |
| Language remains Spanish or English despite system locale | Locale environment variable not recognized or overridden by config | Set language explicitly: `lumart --lang <code` (e.g., `lumart --lang fr` for French). |

---

## 2. Installation & Native C++ Dependency Resolution

Luma utilizes a hybrid architecture: high-level CLI management, color grading, and terminal formatting in Python 3, paired with ultra-optimized, multi-threaded C++17 shared libraries (`libmary.so`, `libmonochrome.so`) for computationally intensive perceptual algorithms.

### 2.1 The Universal Plug & Play Installer
Run the automated installer from the cloned repository:
```bash
./install.sh
```
Or execute directly from GitHub:
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### 2.2 Native C++17 Compiler Setup
To achieve sub-10 millisecond rendering times on 4K/8K images, Luma compiles native C++ modules. Install a C++17 capable compiler before installation:

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
- **macOS (Apple Silicon & Intel)**:
  ```bash
  xcode-select --install
  brew install libomp pillow
  ```

### 2.3 Compiling Native Acceleration Libraries Manually
If you are developing or compiling binaries manually from source:

#### 1. Mary Apex 3.5 Native Engine (`libmary.so` & `luma-mary`):
```bash
# Shared library (loaded automatically by Python via ctypes):
g++ -O3 -std=c++17 -fPIC -shared -fopenmp mary.cpp -o libmary.so

# Standalone CLI binary:
g++ -O3 -std=c++17 -fopenmp mary.cpp -o luma-mary
```

#### 2. Luris Mono 2.6 Native Engine (`libmonochrome.so` & `luma-mono`):
```bash
# Shared library:
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so

# Standalone CLI binary:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono
```

> [!NOTE]
> Both `mary.cpp` and `monochrome.cpp` are self-contained using public domain single-file headers (`stb_image.h`, `stb_image_resize2.h`). You do not need external OpenCV, libpng, or libjpeg packages to compile the core rendering libraries!

### 2.4 Verifying Engine Status (`lumart -v`)
Run the diagnostics report:
```bash
lumart -v
```
Inspect the **⚡ Rendering Engines** section:
- `Mary (Perceptual Color Apex 3.5): Active (Native C++ (.../libmary.so))` -> ✅ Native multi-core acceleration active.
- `Luris (Monochrome Mono 2.6): Active (.../libmonochrome.so)` -> ✅ Native C++ monochrome active.
- If it displays `(Python Fallback)`, ensure `libmary.so` and `libmonochrome.so` are placed in the same directory as `lumart.py` or in `/usr/local/lib/` / `/usr/local/share/luma/`.

---

## 3. Terminal Emulators & Font Compatibility

Luma renders complex graphics using specialized Unicode character blocks:
1. **Braille Patterns (`U+2800` – `U+28FF`)**: 2x4 dot matrix subpixels (`⡀`, `⣿`, `⣾`, `⢦`).
2. **Sextants (`U+1FB00` – `U+1FB3B`)**: 2x3 solid micro-blocks (`🬀`, `🬭`, `🬵`, `█`).
3. **Quadrants (`U+2596` – `U+259F`)**: 2x2 square micro-blocks (`▘`, `▝`, `▖`, `▗`, `▚`, `▛`, `▟`).
4. **Half-Blocks (`U+2580` – `U+2588`)**: Top half (`▀`), bottom half (`▄`), and full blocks (`█`).

### 3.1 Terminal Emulator Compatibility Matrix

| Terminal Emulator | TrueColor (24-bit) | Braille Alignment | Sextants (2x3) | Quadrants (2x2) | Performance | Recommended Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Ghostty** | ✅ Flawless | ✅ Pixel-exact | ✅ Full | ✅ Full | ⭐⭐⭐⭐⭐ (GPU) | **Tier 1 (Recommended)** |
| **Kitty** | ✅ Flawless | ✅ Perfect (with line-height fix) | ✅ Full | ✅ Full | ⭐⭐⭐⭐⭐ (GPU) | **Tier 1 (Recommended)** |
| **Alacritty** | ✅ Flawless | ✅ Perfect | ✅ Full | ✅ Full | ⭐⭐⭐⭐⭐ (OpenGL) | **Tier 1 (Recommended)** |
| **WezTerm** | ✅ Flawless | ✅ Perfect | ✅ Full | ✅ Full | ⭐⭐⭐⭐⭐ (GPU) | **Tier 1 (Recommended)** |
| **Windows Terminal** | ✅ Flawless | ✅ Perfect | ✅ Full | ✅ Full | ⭐⭐⭐⭐ (DirectWrite) | **Tier 1 on Windows** |
| **iTerm2 (macOS)** | ✅ Flawless | ✅ Perfect | ⚠️ Requires font | ✅ Full | ⭐⭐⭐⭐ | **Tier 1 on macOS** |
| **GNOME Terminal** | ✅ Supported | ⚠️ Small gaps | ⚠️ Depends on font | ✅ Full | ⭐⭐⭐ | Standard |
| **macOS Terminal.app** | ❌ 256 colors only | ⚠️ Distorted | ❌ Missing glyphs | ⚠️ Approximate | ⭐⭐ | **Not Recommended** |
| **Windows cmd.exe** | ❌ Broken | ❌ Broken | ❌ Broken | ❌ Broken | ⭐ | **Unusable (Use Windows Terminal)** |

### 3.2 Fixing Vertical Gaps in Braille & Blocks (Line-Height Fix)
Many modern terminals inject extra vertical line padding (`1.2` or `1.3`) for text readability. Because subpixel terminal blocks must touch vertically to create a continuous raster image, line spacing will cause horizontal gaps.

- **Kitty**: Add to `~/.config/kitty/kitty.conf`:
  ```conf
  adjust_line_height 0
  ```
- **Alacritty**: Add to `~/.config/alacritty/alacritty.toml`:
  ```toml
  [font.offset]
  y = 0
  ```
- **WezTerm**: Add to `~/.wezterm.lua`:
  ```lua
  config.line_height = 1.0
  ```

### 3.3 Recommended Fonts
For optimal alignment and zero missing glyphs, use a modern monospaced font with extended Unicode coverage:
- **JetBrains Mono Nerd Font** (Best contrast and dot geometry)
- **Fira Code Nerd Font**
- **Symbols Nerd Font** (Fallback for missing icons and sextants)
- **Cascadia Code** (Built into Windows Terminal)

---

## 4. Color Fidelity & TrueColor (24-bit ANSI)

### 4.1 Checking TrueColor Support
Verify that your current shell session supports 24-bit RGB ANSI escape sequences:
```bash
echo $COLORTERM
```
If this outputs `truecolor` or `24bit`, your terminal is ready.

If running inside **tmux**, configure 24-bit pass-through in `~/.tmux.conf`:
```tmux
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
```

### 4.2 Linear RGB vs Standard sRGB Gamma Blending
Most ASCII converters perform mathematical averaging directly on raw sRGB pixel values. Because sRGB is a non-linear perceptual encoding ($V \approx L^{1/2.2}$), averaging sRGB numbers produces the notorious **dark border artifact** (dirty muddy lines between bright colors).

Luma executes all downsampling and dual-color cell extraction in **linear radiometric space**:
$$C_{\text{linear}} = \left(\frac{C_{\text{sRGB}}}{255}\right)^{2.2}$$
Colors are averaged in physical light units, clustered, and re-encoded to sRGB for terminal output, ensuring vibrant, non-muddy transitions.

---

## 5. The Four Flagship Rendering Engines

Luma features four dedicated rendering engines, each mathematically engineered for a distinct visual paradigm:

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
                                  │  Stream 1.4   │
                                  └───────────────┘
```

### 5.1 Mary Apex 3.5 (Perceptual Oklab & Subpixel Micro-Blocks)
- **Flagship Command**: `lumart image.png` (or `-B`, `-Q`, `--blocks`)
- **Core Technology**:
  1. **Guided Filter in Oklab Color Space**: Edge-preserving spatial smoothing that suppresses JPEG high-frequency noise while keeping crisp anime and photo silhouettes.
  2. **Weber-Fechner Adaptive Contrast**: Contrast sensitivity adjustment modeled after the human visual cortex, bringing out shadow details without blowing out specular highlights.
  3. **Multi-Subpixel Modes**:
     - *Default*: 2x3 solid Unicode sextant blocks. Yields continuous, non-perforated solid color rendering.
     - `-B` / `--braille`: 2x4 Braille matrix with dual-color foreground and background ANSI pairing.
     - `-Q` / `--quadrants`: 2x2 square subpixel blocks.
     - `--blocks`: Classic half-blocks (`▀` / `▄`).
- **Troubleshooting Mary**:
  - *Symptom*: Characters look like strange letters instead of solid blocks.
    - *Cause*: Your font lacks Unicode 13.0 Symbols for Legacy Computing (`U+1FB00`).
    - *Fix*: Use `-B` (Braille) or `-Q` (Quadrants) which are supported by all fonts, or install JetBrains Mono Nerd Font v3+.

### 5.2 Trumble Orelx 2.2 (Retro-Arcade Cel-Shading & Anime Ink)
- **Flagship Command**: `lumart image.png --blocks`
- **Core Technology**:
  1. **Capcom CPS-2 / Neo-Geo Color Punch**: Gamut mapping that maximizes color saturation and contrast for terminal environments without clipping hues.
  2. **Anime Ink Outlines**: Dynamic edge-detection overlay that draws fine dark ink contours around characters and foreground objects.
  3. **Lanczos Downsampling + Bayer Dither**: Smooth anti-aliased geometry reduction with optional retro matrix dithering (`-d bayer`).

### 5.3 Luris Mono 2.6 (Monochrome Manga Screentone & Stickers)
- **Flagship Command**: `lumart image.png -m`
- **Core Technology**:
  1. **Difference of Gaussians (DoG) Lineart**:
     $$\text{DoG}(x, y) = G_{\sigma_1}(x, y) - G_{\sigma_2}(x, y)$$
     Extracts G-pen style manga ink lines while discarding flat background gradients.
  2. **Smart Manga 2.6 Screentone**: Inks crisp outer lines, applies 8x8 Bayer halftone dots to clothing/shadows, and leaves paper/skin pure white.
  3. **Bill Atkinson Dithering (1984, MacPaint)**: Discards 25% of diffused error to keep clean highlights without speckling.
  4. **Exclusive Transparent Sticker Export (`--transparent`)**:
     ```bash
     lumart character.png -m --transparent -o sticker.png
     ```
     Creates an authentic manga cutout sticker with transparent alpha channel!

### 5.4 Spectra Weep 1.4 (Real-Time Live Webcam Streaming)
- **Flagship Command**: `lumart --webcam` (or `lumart -W`)
- **Core Technology**:
  1. **Zero-Lag OpenCV Video Pipeline**: Captures video frames, downsamples in real time, and renders high-FPS ANSI terminal streams (30–60 FPS).
  2. **5 Live Weep Filters**: Real-time edge enhancement, cyber neon, inverted infrared, and retro monochrome streaming.
- **Troubleshooting Spectra**:
  - *Symptom*: `Permission denied: '/dev/video0'`
    - *Fix*: `sudo usermod -aG video $USER` and log out/log back in.
  - *Symptom*: Blank screen or `Camera index out of range`
    - *Fix*: Specify alternative camera index: `lumart -W 1` or `lumart -W 2`.

---

## 6. Sizing, Aspect Ratio & Font Calibration

### 6.1 The 1:2 Character Cell Calibration
Terminal character cells are not square; standard monospace characters are roughly **twice as tall as they are wide** ($1:2$ ratio).
If an image is downscaled without aspect ratio compensation, it will look vertically stretched by 200%.

Luma automatically applies calibrated mathematical scaling based on character geometry:
- **Braille Mode (`-B`)**: 2 dots wide $\times$ 4 dots tall ($2:4 = 1:2$). Each Braille cell compensates for font ratio natively!
- **Half-Blocks (`--blocks`)**: 1 character wide $\times$ 2 pixels tall ($1:2$).
- **Sextants (Default)**: 2 subpixels wide $\times$ 3 subpixels tall ($2:3$). Calibrated at the standard 0.5 font ratio for distortion-free geometry.

---

## 7. High-Definition Graphic Image & Sticker Export

Luma can rasterize terminal art into crisp, high-resolution graphic images (`.png`, `.jpg`):

```bash
# Export Mary Apex subpixel art to 1080p/4K PNG:
lumart photo.png -w 120 -o render.png

# Export anime block art to JPEG:
lumart photo.png --blocks -w 100 -o render.jpg

# Export transparent manga sticker (Exclusive to Luris Mono):
lumart anime.png -m --transparent -o sticker.png
```

### Why was WebP (`.webp`) Export Removed?
WebP lossy and near-lossless compression algorithms apply spatial chroma subsampling and macroblock frequency transforms that blur discrete subpixel glyphs (Sextants, Braille dots, Quadrant boundaries). To guarantee pristine, uncorrupted pixel-art fidelity and transparent alpha cutouts, Luma strictly standardizes on lossless `.png` (with optional transparent alpha) and high-quality `.jpg`.

---

## 8. Configuration, Persistence & Localization (i18n)

Starting with version 2.3.1 ("Rosetta"), Luma features a comprehensive, zero-leak internationalization engine supporting 8 languages with runtime and persistent configuration.

### 8.1 Supported Languages Matrix

| Code | Language | Native Name | Command Example |
| :---: | :--- | :--- | :--- |
| `en` | **English** (Default) | English | `lumart --lang en` |
| `es` | **Spanish** | Español | `lumart --lang es` |
| `fr` | **French** | Français | `lumart --lang fr` |
| `pt` | **Portuguese** | Português | `lumart --lang pt` |
| `ru` | **Russian** | Русский | `lumart --lang ru` |
| `ja` | **Japanese** | 日本語 | `lumart --lang ja` |
| `de` | **German** | Deutsch | `lumart --lang de` |
| `ko` | **Korean** | 한국어 | `lumart --lang ko` |

### 8.2 Persistent vs Ephemeral / Runtime Override
Luma offers two flexible modes for localization:

#### 1. Persistent Setting (Saves across all future terminal sessions):
Run `lumart --lang <code>` with no other action arguments. Luma saves your choice to `~/.config/luma/config.json`:
```bash
# Switch default language to French:
lumart --lang fr

# Switch default language to Japanese:
lumart --lang ja
```

#### 2. Runtime Override (Applies only to current command):
Add `--lang <code>` or `--lang=<code>` anywhere in your command line:
```bash
# View diagnostic information in French:
lumart --lang fr -v

# Render an image with Spanish interface:
lumart character.png --lang es

# View command history in German:
lumart --lang de -H 5
```

### 8.3 Hierarchy of Language Resolution
When Luma starts up, it resolves language using this strict 4-tier hierarchy:
1. **Command Line Flag**: `--lang <code>` or `--lang=<code>` (highest priority).
2. **Persistent User Config**: `~/.config/luma/config.json` (if previously saved).
3. **Environment Locale Detection**: Evaluates `$LC_ALL`, `$LC_MESSAGES`, and `$LANG`, extracting the ISO 639-1 two-letter language code (e.g. `fr_FR.UTF-8` $\to$ `fr`).
4. **Fallback Default**: English (`en`).

### 8.4 Troubleshooting Localization Issues

- **Issue 1: `UnicodeEncodeError: 'ascii' codec can't encode character` in Docker / Containers**
  - *Cause*: Minimal Linux containers or chroots often lack UTF-8 locale definitions and default to `POSIX` or `C`.
  - *Solution*: Export standard UTF-8 environment variables before running:
    ```bash
    export LANG=C.UTF-8
    export LC_ALL=C.UTF-8
    ```

- **Issue 2: CJK (Japanese / Korean) or Cyrillic Characters Display as Tofu (Empty Rectangles / Question Marks)**
  - *Cause*: Your terminal's primary monospace font does not contain glyphs for Kanji, Hiragana, Hangul, or Cyrillic.
  - *Solution*: Install a comprehensive fallback font package:
    - Debian/Ubuntu: `sudo apt install fonts-noto-cjk fonts-noto-core`
    - Fedora: `sudo dnf install google-noto-sans-cjk-fonts google-noto-sans-fonts`
    - Arch Linux: `sudo pacman -S noto-fonts noto-fonts-cjk`

- **Issue 3: Resetting All Configuration to Factory Defaults**
  - If your `config.json` becomes corrupted or permissions are locked:
    ```bash
    rm -rf ~/.config/luma/config.json
    lumart --lang en
    ```

---

## 9. Command History & Interactive Replay System

Luma automatically records execution history with timestamps, version tags, and command lines.

### 9.1 Viewing History (`-H` / `--history`)
```bash
# View recent commands (default: all):
lumart -H

# Limit output to the last 5 commands:
lumart -H 5
```
Example Output:
```
📜 Lumart Command History (5 recorded):

  [#]   Ver       Date / Time         Command
  ──────────────────────────────────────────────────────────────────────────────
  [01]  v2.3.1    2026-09-07 15:06:25 lumart render.png -w 100
  [02]  v2.3.1    2026-09-07 14:58:39 lumart slime.jpg -m --transparent -o sticker.png
  [03]  v2.3.0    2026-09-07 13:32:28 lumart photo.jpg --blocks -o retro.jpg
  ──────────────────────────────────────────────────────────────────────────────
  💡 To re-execute any command, run: lumart --replay <number> (e.g.: lumart -R 1)
```

### 9.2 Instant Replay (`-R` / `--replay`)
Re-execute any previous command directly without retyping:
```bash
# Re-run the most recent command:
lumart -R

# Re-run command #2 from history:
lumart -R 2
```

### 9.3 Clearing History (`--clear-history`)
```bash
lumart --clear-history
```

---

## 10. Updates, Upgrades & Rollback System

Luma includes a built-in release manager with automatic rollback protection:

### 10.1 Checking for Updates (`-u` / `--update`)
Check GitHub for new releases without modifying any files:
```bash
lumart -u
```

### 10.2 Applying Upgrades (`-uu` / `--upgrade`)
Download and atomically upgrade to the latest stable release:
```bash
lumart -uu
```
Before updating, Luma automatically archives your current version in `~/.config/luma/backup/lumart-v<VERSION>`.

### 10.3 Rolling Back / Downgrading (`-dg` / `--downgrade`)
If an update causes issues on your system, roll back immediately:
```bash
# Interactive rollback selector (restores from local backup instantly without network):
lumart -dg

# Or specify a target version explicitly:
lumart -dg 2.3.0
```

---

## 11. Linux Desktop & File Manager Integration

Integrate Luma directly into your desktop environment and file managers (GNOME Files/Nautilus, Nemo, Dolphin, Thunar):

```bash
lumart --install-desktop
```
This performs:
1. Installs `lumart.desktop` in `~/.local/share/applications` (allowing you to set Lumart as default image viewer).
2. Installs right-click contextual scripts in Nautilus and Nemo (`Scripts > Abrir con Lumart` / `Open with Lumart`).
3. Updates system MIME and desktop database caches.

---

## 12. Master Command Reference & Cheat Sheet

```bash
# ==============================================================================
# 1. VERSION, SYSTEM DIAGNOSTICS & LOCALIZATION
# ==============================================================================
lumart -v                                # Complete system & runtime diagnostics
lumart --lang fr                         # Switch persistent language to French
lumart --lang en                         # Switch persistent language to English
lumart --lang es                         # Switch persistent language to Spanish
lumart --lang ja                         # Switch persistent language to Japanese
lumart --lang ru                         # Switch persistent language to Russian
lumart --lang de                         # Switch persistent language to German
lumart --lang pt                         # Switch persistent language to Portuguese
lumart --lang ko                         # Switch persistent language to Korean

# ==============================================================================
# 2. MARY APEX 3.5 (PERCEPTUAL OKLAB COLOR) — DEFAULT ZERO-FLAG
# ==============================================================================
lumart photo.png                         # Default: Mary Sextants HD + Natural TrueColor
lumart photo.png -B                      # Dual-Color TrueColor Braille (2x4)
lumart photo.png -Q                      # 2x2 Quadrant Blocks
lumart photo.png --blocks                # Half-Blocks (▀ / ▄)
lumart photo.png --boost                 # Arcade-style enhanced saturation + Retinex
lumart photo.png --vibrant               # Same as --boost (alias)

# ==============================================================================
# 3. RETRO & VISUAL TUNING
# ==============================================================================
lumart anime.png --blocks                # Retro half-block cel rendering
lumart anime.png --boost                 # Punchy Capcom CPS-2 / Neo-Geo saturation + Ink
lumart anime.png -d bayer                # Retro Bayer 8x8 ordered dither
lumart anime.png --swap purple pink      # Dynamic color swapping (3D RGB space)

# ==============================================================================
# 4. LURIS MONO 2.6 (MONOCHROME MANGA & STICKERS)
# ==============================================================================
lumart manga.png -m                      # Authentic Manga Screentone (DoG + Bayer)
lumart sketch.png -s                     # Clean G-Pen lineart sketch (pure contours)
lumart photo.png -d atkinson             # Bill Atkinson 1984 MacPaint Dithering
lumart photo.png -d floyd                # Floyd-Steinberg error diffusion
lumart anime.png -i                      # Force invert (auto-detected on white backgrounds)
lumart waifu.png -m --transparent -o sticker.png  # Transparent sticker!

# ==============================================================================
# 5. SPECTRA WEEP 1.4 (LIVE WEBCAM STREAMING)
# ==============================================================================
lumart --webcam                          # Stream default webcam (/dev/video0)
lumart -W 1                              # Stream alternate webcam (/dev/video1)

# ==============================================================================
# 6. GRAPHIC IMAGE EXPORT
# ==============================================================================
lumart image.png -w 120 -o art.png       # Export high-res raster PNG
lumart image.png --blocks -o art.jpg     # Export high-res raster JPG

# ==============================================================================
# 7. HISTORY & REPLAY
# ==============================================================================
lumart -H                                # View full execution history with version
lumart -H 10                             # View last 10 commands
lumart -R                                # Re-execute last command
lumart -R 3                              # Re-execute command #3 from history
lumart --clear-history                   # Purge history file

# ==============================================================================
# 8. UPDATES & DESKTOP INTEGRATION
# ==============================================================================
lumart -u                                # Check for GitHub updates without installing
lumart -uu                               # Download and apply latest update
lumart -dg                               # Roll back to previous version from backup
lumart --install-desktop                 # Install desktop launcher & right-click scripts
lumart --paste                           # Load and render image from system clipboard
```

---
*Still experiencing issues? Open an issue on GitHub: [https://github.com/SilentBlox01/Luma/issues](https://github.com/SilentBlox01/Luma/issues) with the output of `lumart -v`.*
