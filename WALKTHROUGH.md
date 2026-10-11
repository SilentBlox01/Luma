# 📖 Lumart (Luma) v2.5.0 Master Manual, Walkthrough & Troubleshooting Guide
> **Comprehensive step-by-step master guide: architecture, flagship engines, subcommands, full flag encyclopedia, real-world recipes, and complete troubleshooting handbook.**

---

## 📑 Table of Contents

- [Part I: Foundations, Terminal Physics & Architecture](#part-i-foundations-terminal-physics--architecture)
  - [1.1 What is Lumart?](#11-what-is-lumart)
  - [1.2 Terminal Grid Physics & Character Aspect Ratio](#12-terminal-grid-physics--character-aspect-ratio)
  - [1.3 Unicode Typographic Subpixels](#13-unicode-typographic-subpixels)
  - [1.4 24-bit TrueColor & ECMA-48 Escape Sequence Compression](#14-24-bit-truecolor--ecma-48-escape-sequence-compression)
- [Part II: The Four Flagship Engines](#part-ii-the-four-flagship-engines)
  - [2.1 Mary Apex 3.5 (Photorealistic Oklab Flagship)](#21-mary-apex-35-photorealistic-oklab-flagship)
  - [2.2 Trumble Orelx 2.2 (Anime Cel-Shading & Capcom CPS-2 Arcade)](#22-trumble-orelx-22-anime-cel-shading--capcom-cps-2-arcade)
  - [2.3 Luris Mono 2.6 (Manga Screentone, DoG Sketch & C++17)](#23-luris-mono-26-manga-screentone-dog-sketch--c17)
  - [2.4 Spectra Weep 2.0 (Live Video, Webcam & Multi-Spectral Shaders)](#24-spectra-weep-20-live-video-webcam--multi-spectral-shaders)
- [Part III: Specialized Subcommands & Built-in Tools](#part-iii-specialized-subcommands--built-in-tools)
  - [3.1 lumart fetch (Fastfetch / Neofetch Preset Generator)](#31-lumart-fetch)
  - [3.2 lumart bench (Multi-Core Performance & Latency Benchmark)](#32-lumart-bench)
  - [3.3 lumart showcase (4-in-1 Comparison Canvas)](#33-lumart-showcase)
  - [3.4 lumart info (Visual Image Inspector & Engine Recommender)](#34-lumart-info)
  - [3.5 lumart diff (Chromatic Delta Heatmap Between Two Images)](#35-lumart-diff)
  - [3.6 lumart slideshow (Full-Screen Terminal Presentation)](#36-lumart-slideshow)
  - [3.7 lumart -I / --interactive (Interactive TUI Viewer)](#37-lumart-i----interactive)
  - [3.8 lumart animate (GIF Transcoder & Video Compiler)](#38-lumart-animate)
- [Part IV: Complete CLI Encyclopedia of Flags & Options](#part-iv-complete-cli-encyclopedia-of-flags--options)
  - [A. Engines & Glyph Textures](#a-engines--glyph-textures)
  - [B. Dimensions, Viewport & Geometry](#b-dimensions-viewport--geometry)
  - [C. Colorimetry, Shaders & Visual Tuning](#c-colorimetry-shaders--visual-tuning)
  - [D. Animation, GIFs & Framerates](#d-animation-gifs--framerates)
  - [E. Graphic Image Export, Stickers & Clipboard](#e-graphic-image-export-stickers--clipboard)
  - [F. Video & Live Webcam Streaming](#f-video--live-webcam-streaming)
  - [G. System, Diagnostics & Languages](#g-system-diagnostics--languages)
- [Part V: Real-World Recipes & Practical Workflows](#part-v-real-world-recipes--practical-workflows)
  - [Recipe 1: The Perfect Fastfetch / Neofetch Sidebar Logo](#recipe-1-the-perfect-fastfetch--neofetch-sidebar-logo)
  - [Recipe 2: Transparent Anime Stickers for Discord / Telegram](#recipe-2-transparent-anime-stickers-for-discord--telegram)
  - [Recipe 3: Zero-Lag 60 FPS Animated GIFs with RAM Preload](#recipe-3-zero-lag-60-fps-animated-gifs-with-ram-preload)
  - [Recipe 4: Cyberpunk Matrix CRT Live Webcam Stream](#recipe-4-cyberpunk-matrix-crt-live-webcam-stream)
  - [Recipe 5: Automation in Bash Scripts, Unix Pipelines & MOTD](#recipe-5-automation-in-bash-scripts-unix-pipelines--motd)
- [Part VI: Master Troubleshooting & Diagnostic Guide](#part-vi-master-troubleshooting--diagnostic-guide)
  - [6.1 Quick Diagnostic Checklist (Symptoms & Solutions)](#61-quick-diagnostic-checklist-symptoms--solutions)
  - [6.2 Visual "Dos & Don'ts" Master Guide](#62-visual-dos--donts-master-guide)
  - [6.3 Terminal Emulator & Font Compatibility (Nerd Fonts)](#63-terminal-emulator--font-compatibility-nerd-fonts)
  - [6.4 Color Fidelity & 24-bit TrueColor (Tmux, Screen & SSH)](#64-color-fidelity--24-bit-truecolor-tmux-screen--ssh)
  - [6.5 Line Wrapping, Viewport Fitting & --font-ratio Calibration](#65-line-wrapping-viewport-fitting----font-ratio-calibration)
  - [6.6 Transparent Sticker Policy & Permanent Ban on WebP](#66-transparent-sticker-policy--permanent-ban-on-webp)
  - [6.7 Animated GIF Performance & Frame Rate Drops](#67-animated-gif-performance--frame-rate-drops)
  - [6.8 Web Camera & OpenCV Troubleshooting](#68-web-camera--opencv-troubleshooting)
  - [6.9 Native C++ Engine Compilation & lumart -v Diagnostics](#69-native-c-engine-compilation--lumart--v-diagnostics)
  - [6.10 Updates, Upgrades, Rollback & Clean Uninstallation](#610-updates-upgrades-rollback--clean-uninstallation)

---

## Part I: Foundations, Terminal Physics & Architecture

### 1.1 What is Lumart?
**Lumart (Luma)** is an advanced terminal visual engineering suite. Its fundamental goal is to render digital images, videos, live webcams, and animations into ultra-high-definition ANSI/Unicode terminal art, mathematically adapted to the character grid of modern terminal emulators.

Unlike legacy ASCII converters that simply replace pixels with coarse single-ramp letters, Lumart implements:
1. **Human Perceptual Oklab Color Space ($\Delta E$)**: Completely eliminates color banding, blown-out highlights, and muddy midtones.
2. **High-Density Unicode Typographic Subpixels**: Sextants ($2 \times 3$), Braille ($2 \times 4$), Quadrants ($2 \times 2$), and Half-blocks ($1 \times 2$).
3. **Native C++17 OpenMP SIMD Acceleration**: Processes gigapixel images in milliseconds using multi-threaded vectorization.

---

### 1.2 Terminal Grid Physics & Character Aspect Ratio
On a graphic GPU display, pixels are strictly square with a $1:1$ aspect ratio. However, in any terminal emulator (Alacritty, Kitty, Ghostty, WezTerm, Konsole, GNOME Terminal, etc.), text character cells are rectangular: they are roughly twice as tall as they are wide (a typical $1:2$ ratio).

If an image is mapped directly to character cells without aspect ratio compensation, the output will appear stretched vertically to twice its proper height.

* **The `--font-ratio` Parameter**: Calibrated by default to `0.5`, precisely canceling out the $1:2$ font distortion.
* For atypical or custom condensed/expanded fonts:
  ```bash
  lumart photo.png --font-ratio 0.45  # If characters are taller and narrower
  lumart photo.png --font-ratio 0.55  # If characters are wider or square-ish
  ```

---

### 1.3 Unicode Typographic Subpixels

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   Sextants   │   Braille    │  Quadrants   │ Half-Blocks  │
│     2x3      │     2x4      │     2x2      │     1x2      │
├──────────────┼──────────────┼──────────────┼──────────────┤
│    🬀  🬁  🬂    │    ⠋  ⠙  ⠹    │    ▖  ▗  ▘    │    ▀   ▄     │
│  6 subpixels │  8 subpixels │  4 subpixels │  2 subpixels │
│   Solid HD   │ Smooth curves│ Dense blocks │ TrueColor F/B│
└──────────────┴──────────────┴──────────────┴──────────────┘
```

* **Sextants (`-S`)**: 6 subpixels per cell ($2 \times 3$). Flagship default for **Mary Apex 3.5**. Produces smooth, solid blocks without gaps.
* **Braille (`-B`)**: 8 subpixels per cell ($2 \times 4$). Highest geometric contour resolution for fine curves, outlines, and small text.
* **Quadrants (`-Q`)**: 4 subpixels per cell ($2 \times 2$).
* **Half-Blocks (`--blocks`)**: 2 vertical subpixels per cell (`▀` with independent foreground top and background bottom colors). Delivers 24-bit TrueColor with 2x vertical resolution. Default format for `lumart fetch`.

---

### 1.4 24-bit TrueColor & ECMA-48 Escape Sequence Compression
Lumart generates ECMA-48 standard ANSI escape codes in full 24-bit TrueColor (16.7 million colors):
* Foreground text color: `\033[38;2;R;G;Bm`
* Background color: `\033[48;2;R;G;Bm`

Lumart includes a **real-time ECMA-48 escape optimizer**: if consecutive character cells on a row share the same colors, Lumart suppresses redundant color codes, reducing file size and terminal rendering latency by up to **65%**.

---

## Part II: The Four Flagship Engines

### 2.1 Mary Apex 3.5 (Photorealistic Oklab Flagship)
* **Invocation:** `-E mary` (or zero-flag default invocation).
* **Target:** Ultimate photorealism and color fidelity.
* **Algorithm:**
  - Converts pixel clusters to the perceptual **Oklab** color space.
  - Runs a **3-iteration K-Means** algorithm coupled with the human Contrast Sensitivity Function (**Weber-Fechner CSF**).
  - Determines the exact foreground color, background color, and Unicode glyph that minimizes perceptual color error $\Delta E$.
* **Best for:** Portraits, landscape photography, photorealistic game renders, and album artwork.

### 2.2 Trumble Orelx 2.2 (Anime Cel-Shading & Capcom CPS-2 Arcade)
* **Invocation:** `-E trumble`
* **Target:** 1990s retro-arcade aesthetics (Capcom CPS-2, Neo-Geo) and anime cel-shading.
* **Algorithm:**
  - Uses Laplacian edge convolution to generate crisp G-Pen inking outlines.
  - Boosts midtone saturation with dynamic color punch and ordered Bayer dithering.
* **Best for:** Cartoons, anime illustrations, pixel-art sprites, retro posters, and vector logos.

### 2.3 Luris Mono 2.6 (Manga Screentone, DoG Sketch & C++17)
* **Invocation:** `-E luris` (or `-m`, `-s`, `-ch`, `--no-color`).
* **Target:** High-fidelity monochrome, traditional manga screentones, and transparent alpha sticker exports.
* **Sub-modes:**
  - **Manga Screentone (`-m`):** Shonen Jump-style screentone (*Ami-tone*) with calibrated $8 \times 8$ Bayer matrix over paper and ink.
  - **DoG Sketch (`-s`):** Pure Difference of Gaussians pencil line art without shadow blotches.
  - **Crosshatch (`-ch`):** Authentic $45^\circ / -45^\circ$ pen hatching with 6 perpendicular density tiers.
  - **Transparent Stickers (`--transparent`):** Exclusive to Luris Mono for exporting PNG stickers without black boxes.
* **Best for:** Manga pages, architectural sketches, minimal Catppuccin/Nord terminal themes, and Discord/Telegram stickers.

### 2.4 Spectra Weep 2.0 (Live Video, Webcam & Multi-Spectral Shaders)
* **Invocation:** `-E spectra` (or `-W`, video file path, `--shader <name>`).
* **Target:** Real-time video playback, 60 FPS live webcam streaming, and multi-spectral terminal shaders.
* **Shaders Available:**
  - `neon`: Hyper-saturated cyberpunk synthwave glow.
  - `thermal`: FLIR military infrared heat map vision.
  - `tron`: Glowing electric vector wireframes.
  - `matrix`: Falling digital code and 525nm P1 green phosphor.
  - `amber`: Vintage 1970s monochrome amber phosphor screen.
  - `hologram`: Sci-fi cyan holographic interference.
  - `glitch`: RGB chromatic aberration with temporal jitter.
  - `phosphor-bloom`: Diffuse analog CRT bloom.
* **Best for:** Live webcam streaming, playing MP4/MKV video files in the terminal, and sci-fi visual effects.

---

## Part III: Specialized Subcommands & Built-in Tools

### 3.1 `lumart fetch`
> **Fastfetch / Neofetch Preset Generator**

```bash
lumart fetch <image.png> [-w WIDTH]
```
1. Auto-crops empty or transparent borders (`--fastfetch`).
2. Renders into 24-bit TrueColor half-blocks (`▀`).
3. Saves the `.ans` art file to `~/.config/fastfetch/<name>_logo.ans`.
4. Outputs the ready-to-use JSON block for `~/.config/fastfetch/config.jsonc`.

---

### 3.2 `lumart bench`
> **Multi-Core Performance & Latency Benchmark**

```bash
lumart bench [image.png] [-w WIDTH]
```
Measures with microsecond precision:
- Rendering latency in milliseconds (`ms`).
- Throughput in Megapixels per second (`MP/s`).
- Potential refresh rate in frames per second (`FPS`).
Compares Mary Apex, Trumble Arcade, Luris Mono C++, and Spectra side by side.

---

### 3.3 `lumart showcase`
> **4-in-1 Comparison Canvas**

```bash
lumart showcase <image.png> [-w WIDTH] [-o review.png]
```
Divides the terminal into 4 quadrants rendering the same image across all flagship engines:
- Top-Left: Mary Apex 3.5 (Photorealistic)
- Top-Right: Trumble Orelx 2.2 (Cel-shading)
- Bottom-Left: Luris Mono 2.6 (Manga Screentone)
- Bottom-Right: Spectra Weep 2.0 (Neon Shader)

---

### 3.4 `lumart info`
> **Visual Image Inspector & Engine Recommender**

```bash
lumart info <image.png>
```
Extracts and reports:
- Native pixel dimensions, resolution, and aspect ratio.
- Average luminance and dynamic range.
- Top 6 dominant colors in HEX and ANSI swatch samples.
- **Automated optimal engine recommendation** for that specific image.

---

### 3.5 `lumart diff`
> **Chromatic Delta Heatmap Between Two Images**

```bash
lumart diff <image1.png> <image2.png> [-w WIDTH]
```
Computes pixel-by-pixel color deviation, generates a false-color heatmap, and calculates average color delta ($\Delta E$).

---

### 3.6 `lumart slideshow`
> **Full-Screen Terminal Presentation**

```bash
lumart slideshow <image_folder/> [--delay 3.0] [-w WIDTH]
```
Presents all images in a folder with clean terminal transitions and interactive keyboard controls (`Space` = pause, `Arrows` = navigate, `Q` = quit).

---

### 3.7 `lumart -I` / `--interactive`
> **Interactive TUI Viewer**

```bash
lumart -I <image.png>
```
Opens the image in an interactive terminal viewer with real-time keys:
- `+` / `-`: Adjust brightness.
- `M` / `T` / `L`: Switch between Mary, Trumble, and Luris engines.
- `G`: Toggle Manga screentone mode.
- `Z`: Zoom in/out.

---

### 3.8 `lumart animate`
> **GIF Transcoder & Video Compiler**

```bash
lumart animate <clip.mp4 | frame_dir/> -o result.gif [--fps 30]
```
Transcodes video clips or image sequences into optimized animated GIFs through Lumart's ASCII/ANSI rendering pipeline.

---

## Part IV: Complete CLI Encyclopedia of Flags & Options

### A. Engines & Glyph Textures

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `-E`, `--engine` | `string` | *auto* | Explicitly select engine: `mary`, `trumble`, `luris`, `spectra`, `color`, `mono`, `bw`, `manga`, `sketch`, `crosshatch`. |
| `-S`, `--sextants` | `switch` | *active* | Unicode $2 \times 3$ Sextant blocks (6 subpixels/cell). Mary Apex flagship default. |
| `-B`, `--braille` | `switch` | `false` | Unicode $2 \times 4$ Braille matrix (8 subpixels/cell). Highest outline precision. |
| `-Q`, `--quadrants`| `switch` | `false` | Unicode $2 \times 2$ Quadrant blocks (4 subpixels/cell). |
| `--blocks` | `switch` | `false` | Optimized half-blocks (`▀` / `▄`, 2 vertical pixels/cell with 24-bit TrueColor). |
| `-m`, `--manga` | `switch` | `false` | Manga Screentone mode (*Ami-tone* Bayer 8x8 + clean DoG ink contours). |
| `-s`, `--sketch` | `switch` | `false` | Clean pencil sketch mode without shadow blotches. |
| `-ch`, `--crosshatch`| `switch` | `false` | Authentic $45^\circ / -45^\circ$ pen crosshatch shading with 6 perpendicular density tiers. |
| `-cs`, `--charset` | `string` | `standard`| Font glyph ramp: `dense`, `standard`, `blocks`, `math`, `runes`, `katakana`, `crosshatch`. |
| `--matrix` | `switch` | `false` | Transform output into Matrix Katakana digital code with 525nm P1 green phosphor bloom. |
| `--matrix-rain` | `switch` | `false` | Animated downward falling Matrix digital code rain. |

---

### B. Dimensions, Viewport & Geometry

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `-w`, `--width` | `int` | *terminal* | Output width in columns (mutually exclusive with `-F`). |
| `-F`, `--fit` | `switch` | `false` | **Auto-fit viewport**: calculates optimal width & height to fit terminal without scrolling (mutually exclusive with `-w`). |
| `--fastfetch`, `--logo`| `switch`| `false` | Auto-crop empty/transparent margins for compact logos. |
| `--font-ratio` | `float` | `0.5` | Terminal font aspect ratio calibration width/height. |
| `--crop` | `string` | `None` | Crop region before rendering: `--crop "x,y,width,height"` (e.g. `--crop "100,50,400,400"`). |
| `--zoom` | `float` | `1.0` | Digital zoom magnification factor (e.g. `--zoom 1.5` for 150%). |
| `--rotate` | `int` | `0` | Clockwise rotation in degrees: `0`, `90`, `180`, `270`. |
| `--flip`, `--mirror` | `string` | `None` | Geometric mirroring: horizontal (`h`) or vertical (`v`). |
| `--border` | `string` | `None` | Enclose render in decorative Unicode border: `rounded`, `single`, `double`, `heavy`, `ascii`, `blocks`. |
| `--align` | `string` | `left` | Horizontal alignment in terminal viewport: `left`, `center`, `right`. |
| `--center` | `switch` | `false` | Shorthand alias for `--align center`. |

---

### C. Colorimetry, Shaders & Visual Tuning

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `-c`, `--color` | `switch` | `true` | Force 24-bit TrueColor output (default: enabled). |
| `--no-color` | `switch` | `false` | Disable ANSI color codes and route to monochrome engine. |
| `--brightness` | `float` | `1.0` | Brightness multiplier (e.g. `1.2` to brighten, `0.8` to darken). |
| `--contrast` | `float` | `1.0` | Tonal contrast multiplier (e.g. `1.3` for punchier contrast). |
| `--saturation` | `float` | `1.0` | Color saturation multiplier (e.g. `1.4` for vivid color, `0.0` for grayscale). |
| `--boost`, `--vibrant`| `switch`| `false` | Apply enhanced saturation, contrast, and Retinex curves for punchy arcade look. |
| `--gamma` | `float` | `1.0` | Non-linear midtone gamma curve correction exponent. |
| `-i`, `--invert` | `switch` | `false` | Invert brightness mapping (useful for light-themed terminals). |
| `--swap` | `args` | `None` | Dynamically swap two colors in 3D RGB space: `--swap "#800080" "#ff69b4"`. |
| `--theme`, `--palette`| `string` | `None` | Apply curated color palette: `cyberpunk`, `dracula`, `nord`, `catppuccin`, `gruvbox`, `synthwave`, `monokai`, `gameboy`, `amber`. |
| `--crt`, `--scanlines`| `string` | `None` | Vintage analog CRT monitor emulation: `green`, `amber`, `color`, `scanlines`. |
| `--shader` | `string` | `None` | Multi-spectral shaders: `neon`, `cyberpunk`, `thermal`, `tron`, `matrix`, `amber`, `manga`, `hologram`, `glitch`, `phosphor-bloom`, `solarize`. |
| `-d`, `--dither` | `string` | *auto* | Dithering algorithm: `atkinson` (MacPaint 1984), `floyd` (Floyd-Steinberg), `bayer` (Bayer 8x8), `none`. |

---

### D. Animation, GIFs & Framerates

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--loop` | `switch` | `false` | Infinite loop playback mode in terminal for GIF/APNG files. |
| `--fps`, `--target-fps`| `float` | *from gif*| Target framerate for playback or GIF duration export (e.g. `--fps 60`). |
| `--preload`, `--smooth`| `switch`| `false` | **Full RAM Preload**: pre-renders all frames in memory before playback for **silky 60 FPS with 0 ms lag**. |
| `--instant`, `--no-reveal`| `switch`| `true` | Output immediately without progressive scan delay (default). |
| `--reveal` | `switch` | `false` | Nostalgic progressive line-by-line reveal animation effect. |

---

### E. Graphic Image Export, Stickers & Clipboard

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `-o`, `-O`, `--save` | `path` | `None` | Export output to raster image (`.png`, `.jpg`) or animated GIF (`.gif`). |
| `--transparent` | `switch` | `false` | **Exclusive to Luris Mono**: exports transparent-background stickers (no black box). |
| `-r`, `--remove-bg` | `switch` | `false` | Intelligent perceptual flood-fill background removal. |
| `--bg-tolerance` | `int` | `32` | Color tolerance threshold for background removal (1 to 100). |
| `-C`, `--copy` | `switch` | `false` | Copy formatted ANSI art (with escape codes) directly to system clipboard. |
| `--copy-plain` | `switch` | `false` | Copy clean plain ASCII text (uncolored) directly to system clipboard. |
| `--paste` | `switch` | `false` | Read and render image currently in system clipboard (Ctrl+C). |

---

### F. Video & Live Webcam Streaming

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `-W`, `--webcam` | `int` | `0` | Stream live webcam to terminal at 30-60 FPS (0 = default camera, 1 = external USB). |
| `<video.mp4>` | `path` | `None` | Directly play video files (`.mp4`, `.mkv`, `.webm`, `.mov`) in the terminal. |

---

### G. System, Diagnostics & Languages

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--lang` | `code` | *auto* | Set display language (`en`, `es`, `pt`, `fr`, `ru`, `ja`, `de`, `ko` or full names like `spanish`, `japanese`). |
| `-v`, `--version` | `switch` | `false` | Display comprehensive diagnostic card of hardware, OS, and native C++ engines. |
| `-H`, `--history` | `int` | `10` | Display the last N commands stored in Lumart history. |
| `-R`, `--replay` | `int` | *last* | Re-run command N from history (default: last command). |
| `--clear-history` | `switch` | `false` | Wipe command history cache. |
| `--install-desktop` | `switch` | `false` | Register "Open with Lumart" in Linux file manager context menus. |
| `--completions` | `shell` | `None` | Generate shell autocomplete scripts (`bash`, `zsh`, `fish`). |
| `-u`, `--check-update`| `switch` | `false` | Check GitHub for newer releases. |
| `-uu`, `--upgrade` | `optional`| `latest` | Interactive upgrade assistant with automated backups. |
| `-dg`, `--downgrade` | `optional`| `prev` | Interactive rollback selector to restore previous version. |

---

## Part V: Real-World Recipes & Practical Workflows

### Recipe 1: The Perfect Fastfetch / Neofetch Sidebar Logo

#### Option A: TrueColor Half-Blocks (Recommended)
```bash
lumart fetch "avatar.png" -w 38
```
*Saves to `~/.config/fastfetch/avatar_logo.ans` and outputs copy-pasteable JSON block.*

#### Option B: Minimalist Manga Screentone for Nord / Catppuccin Themes
```bash
lumart "avatar.png" -w 38 --fastfetch -m -o ~/.config/fastfetch/logo_manga.ans
```

#### Option C: High-Density Braille $2 \times 4$
```bash
lumart "avatar.png" -w 38 --fastfetch -E mary -B -o ~/.config/fastfetch/logo_braille.ans
```

Test immediately in your terminal:
```bash
fastfetch --logo ~/.config/fastfetch/avatar_logo.ans --logo-type file
```

---

### Recipe 2: Transparent Anime Stickers for Discord / Telegram
Export a transparent cutout sticker without a black background box:
```bash
lumart "character.png" -w 80 -m --transparent -o sticker_manga.png
```
*With automated flood-fill background removal:*
```bash
lumart "character.png" -w 80 -m -r --bg-tolerance 40 --transparent -o sticker_clean.png
```

---

### Recipe 3: Zero-Lag 60 FPS Animated GIFs with RAM Preload
Play animated GIFs in the terminal with zero frame drops:
```bash
lumart "animation.gif" -w 70 --loop --fps 60 --preload
```
*Export rendered animation with a Synthwave palette to a new GIF:*
```bash
lumart "animation.gif" -w 60 --theme synthwave --fps 30 -o anim_synthwave.gif
```

---

### Recipe 4: Cyberpunk Matrix CRT Live Webcam Stream
Launch live webcam in terminal with Matrix digital rain and vintage scanlines:
```bash
lumart -W 0 --matrix --crt green --fps 60
```
*Or with military FLIR thermal vision:*
```bash
lumart -W 0 --shader thermal --fps 30
```

---

### Recipe 5: Automation in Bash Scripts, Unix Pipelines & MOTD

#### Welcome banner in `~/.bashrc`:
```bash
# Add to ~/.bashrc:
if command -v lumart &>/dev/null; then
    lumart ~/.config/banner.png -w 60 --border rounded --align center --instant
fi
```

#### Render directly from web HTTPS URL:
```bash
lumart "https://raw.githubusercontent.com/fastfetch-cli/fastfetch/dev/assets/arch.png" -w 50
```

#### Render image from system clipboard:
```bash
lumart --paste -w 60 --border double
```

#### Copy generated ANSI art to clipboard:
```bash
lumart "logo.png" -w 40 -C
```

---

## Part VI: Master Troubleshooting & Diagnostic Guide

### 6.1 Quick Diagnostic Checklist (Symptoms & Solutions)

| Symptom | Primary Cause | Immediate Resolution |
| :--- | :--- | :--- |
| `command not found: luma` or `lumart` | `~/.local/bin` missing from `$PATH` | Run `./install.sh` or add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc` / `~/.zshrc`. |
| `error: externally-managed-environment` | PEP 668 restriction on Fedora/Debian/Ubuntu | Install system package: `sudo dnf install python3-pillow` / `sudo apt install python3-pil`, or run `./install.sh`. |
| Braille dots or blocks look like `?`, ``, or empty boxes | Active terminal font lacks Unicode glyph coverage | Switch to a **Nerd Font** (JetBrains Mono Nerd Font, FiraCode, Cascadia Code). |
| Horizontal black gaps cutting through Braille rows | Terminal emulator line-height / row spacing is greater than `1.0` | Set terminal line-height to `1.0` or `0px` in terminal config. |
| Washed-out colors or harsh 16-color banding | Terminal emulator lacks 24-bit TrueColor advertisement | Check `echo $COLORTERM`. Add `export COLORTERM=truecolor` to `~/.bashrc` or switch to Ghostty, Kitty, Alacritty, or WezTerm. |
| Output wraps around lines and looks distorted | Specified width (`-w`) exceeds available terminal columns | Reduce width with `-w 80` or use auto-fit `-F` / `--fit`. |
| Braille or Monochrome output looks like an inverted negative | Terminal background is light (white/cream) instead of dark | Luris auto-detects light backgrounds. For manual override: pass `-i` / `--invert`. |
| Mary or Luris running on Python fallback instead of C++ | C++ shared libraries (`.so`) were not compiled | Install `g++` (`build-essential` or `gcc-c++`) and run `make -f Makefile.native` or `./install.sh`. |
| `OpenCV required for Spectra engine` error | `opencv-python` is not installed | Install via system packages: `sudo dnf install python3-opencv` / `sudo apt install python3-opencv` or `pip install opencv-python`. |
| Web camera fails to open in Spectra mode (`-W`) | Missing camera permissions or incorrect `/dev/video*` index | Add user to video group: `sudo usermod -aG video $USER`, or specify index: `lumart -W 1`. |
| Output vertically stretched or squashed | Terminal font has atypical aspect ratio (not $1:2$) | Calibrate with `--font-ratio <float>` (e.g. `--font-ratio 0.45` or `0.55`). Default: `0.5`. |
| Transparent sticker (`--transparent`) has black background | Transparent alpha is only supported in Luris Mono with `.png` | Run `lumart image.png -m --transparent -o sticker.png`. Color models export with solid terminal background. |
| WebP export rejected with error | WebP export was permanently disabled to protect visual quality | Export to `.png` or `.jpg` instead (`-o output.png`). |
| Language remains English or Spanish despite system locale | Locale environment variable not recognized | Set language explicitly: `lumart --lang <code>` (e.g. `lumart --lang fr` or `lumart --lang spanish`). |

---

### 6.2 Visual "Dos & Don'ts" Master Guide

| Aspect | ✅ What to DO | ❌ What NOT to do |
| :--- | :--- | :--- |
| **Photorealism & TrueColor** | **DO** use default **Mary Apex 3.5** (`lumart photo.jpg`) for portraits, natural skin tones, and rich real-world scenes with Oklab and Sextants 2x3. | **DON'T** force `--blocks` or `--boost` on delicate photographs or skin tones unless you explicitly want a saturated retro-arcade look. |
| **Retro Arcade & Cel-Shading** | **DO** use **Trumble Orelx 2.2** (`lumart art.png -E trumble --boost`) for Capcom CPS-2 / Neo-Geo style vibrant posters. | **DON'T** expect Trumble to produce smooth gradients; Trumble is designed for sharp comic edges and saturated posterized bands. |
| **Traditional Manga & Line Art** | **DO** use **Luris Mono 2.6** (`lumart manga.jpg -m`) to recreate authentic physical screentones (*Ami-tone*) and DoG ink contours. | **DON'T** use general ASCII tools that randomly scramble letters; Luris uses calibrated Bayer matrices and Atkinson error diffusion. |
| **Viewport Auto-Fitting** | **DO** use `-F` (`--fit`) to let Lumart calculate both width and height to fit your exact terminal window without vertical scrolling:<br>`lumart artwork.jpg -F` | **DON'T** combine `-F` and `-w` simultaneously:<br>`lumart artwork.jpg -F -w 80` ❌ *(Lumart will halt with an incompatibility error).* |
| **Fastfetch / Dashboards** | **DO** use `-w 36..42` with `--fastfetch` to auto-crop whitespace when embedding into sidebars. | **DON'T** set `-w` wider than terminal columns, which forces lines to wrap and distorts characters. |
| **Transparent Stickers** | **DO** use Luris Mono with `--transparent -o sticker.png` for Discord/Telegram stickers. | **DON'T** use color engines for transparent stickers; color terminal characters require a solid background canvas. |

---

### 6.3 Terminal Emulator & Font Compatibility (Nerd Fonts)

* **Top-Tier Accelerated Terminal Emulators (Recommended):**
  - **Ghostty**: Native GPU acceleration, flawless 24-bit TrueColor, complete Unicode coverage.
  - **Kitty**: Accelerated GPU rendering, superior font ligature handling, full escape sequence support.
  - **Alacritty**: Fast OpenGL rendering with zero-overhead TrueColor output.
  - **WezTerm**: Complete Nerd Font support and complex glyph layout handling.
* **Standard Desktop Terminals:**
  - **GNOME Terminal / Konsole / XFCE Terminal**: Support TrueColor and Unicode blocks when paired with a modern Nerd Font.
* **Recommended Typefaces:**
  - `JetBrains Mono Nerd Font` (Highest visual density and geometric accuracy).
  - `FiraCode Nerd Font`
  - `Cascadia Code Nerd Font`
  - `Hack Nerd Font`

---

### 6.4 Color Fidelity & 24-bit TrueColor (Tmux, Screen & SSH)

If colors appear washed out or degraded to 16/256 color banding:
1. Verify terminal TrueColor advertisement:
   ```bash
   echo $COLORTERM
   ```
2. If empty, add to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   export COLORTERM=truecolor
   ```
3. **Inside Tmux**: Add the following to `~/.tmux.conf` to enable 24-bit color passthrough:
   ```tmux
   set -g default-terminal "tmux-256color"
   set -ga terminal-overrides ",*256col*:Tc"
   ```

---

### 6.5 Line Wrapping, Viewport Fitting & `--font-ratio` Calibration
* If lines break and wrap downward forming skewed columns, the specified width `-w` exceeds available columns. Use `-F` (`--fit`) to auto-fit to the active viewport.
* If rendering appears squashed or stretched vertically, your terminal font deviates from the standard $1:2$ ratio. Calibrate with `--font-ratio 0.45` (taller fonts) or `--font-ratio 0.55` (wider fonts).

---

### 6.6 Transparent Sticker Policy & Permanent Ban on WebP
* **Why Transparent Stickers are Exclusive to Luris Mono:**
  In text terminals, color character cells define both a foreground and a background color. Generating alpha transparency on color models creates ugly black halos around pixels. Luris Mono renders pure black ink on transparent alpha, guaranteeing clean, artifact-free PNG stickers.
* **WebP Deprecation:**
  Lossy WebP compression introduces quantization artifacts that severely degrade subpixel glyph accuracy. Lumart strictly exports to `.png` (high-fidelity lossless) or `.jpg` / `.gif`.

---

### 6.7 Animated GIF Performance & Frame Rate Drops
* If animated GIFs experience stuttering or frame drops:
  1. Enable **Full RAM Preload**:
     ```bash
     lumart animation.gif -w 70 --loop --fps 60 --preload
     ```
  2. `--preload` pre-renders all frames into memory prior to playback, guaranteeing **silky 60 FPS with 0 ms disk I/O latency**.

---

### 6.8 Web Camera & OpenCV Troubleshooting
* If `lumart -W` or `lumart -E spectra` produces an OpenCV import error:
  ```bash
  # Fedora / RHEL:
  sudo dnf install python3-opencv
  # Debian / Ubuntu:
  sudo apt install python3-opencv
  # Or via pip:
  pip install opencv-python
  ```
* If the camera fails to initialize, verify video device permissions:
  ```bash
  sudo usermod -aG video $USER
  ```

---

### 6.9 Native C++ Engine Compilation & `lumart -v` Diagnostics
Run diagnostics anytime:
```bash
lumart -v
```
Check the diagnostic card:
- If it shows `Mary Apex 3.5 [C++17 OpenMP]` and `Luris Mono 2.6 [C++17 OpenMP]`, your native engines are running with full hardware SIMD acceleration.
- If it shows `Python Fallback`, compile native libraries directly:
  ```bash
  g++ -O3 -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so
  g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
  ```

---

### 6.10 Updates, Upgrades, Rollback & Clean Uninstallation

* **Check for GitHub updates:**
  ```bash
  lumart -u
  ```
* **Atomically upgrade to latest stable release:**
  ```bash
  lumart -uu
  ```
* **Roll back to previous version:**
  ```bash
  lumart -dg
  ```
* **Clean uninstallation:**
  ```bash
  # Script / source install:
  rm -rf ~/.local/bin/lumart ~/.local/bin/luma ~/.config/lumart
  # Distribution package managers:
  sudo dnf remove lumart    # Fedora / RHEL
  sudo apt remove lumart    # Debian / Ubuntu
  yay -R lumart             # Arch Linux
  ```

---

*Lumart (Luma) v2.5.0 • Engineered with passion for terminal enthusiasts.*
