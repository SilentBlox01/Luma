# 🔧 Luma Comprehensive Troubleshooting & Deep Technical Guide

Welcome to the definitive troubleshooting and operational guide for **Luma** (and `lumart`). This document provides comprehensive solutions to common issues, detailed terminal compatibility benchmarks, font rendering explanations, and internal architectural mechanics.

---

## 📑 Table of Contents
1. [Quick Diagnostic Checklist](#1-quick-diagnostic-checklist)
2. [Installation & Dependency Resolution (Fedora, Debian, Arch)](#2-installation--dependency-resolution)
3. [Terminal Emulators & Font Compatibility](#3-terminal-emulators--font-compatibility)
4. [Color Fidelity & TrueColor (24-bit ANSI)](#4-color-fidelity--truecolor-24-bit-ansi)
5. [Black & White, Manga Screentone & Braille Art](#5-black--white-manga-screentone--braille-art)
6. [Sizing, Aspect Ratio & Text-Wrapping Artifacts](#6-sizing-aspect-ratio--text-wrapping-artifacts)
7. [Color Swapping (`--swap`) Mechanics](#7-color-swapping---swap-mechanics)
8. [Configuration, Persistence & Localization (i18n)](#8-configuration-persistence--localization-i18n)
9. [Command Reference & Cheat Sheet](#9-command-reference--cheat-sheet)

---

## 1. Quick Diagnostic Checklist

If an image looks distorted, wrong, or fails to render, run this quick check:

| Symptom | Primary Cause | Immediate Fix |
| :--- | :--- | :--- |
| `command not found: luma` | `~/.local/bin` is not in `$PATH` | Run `./install.sh` or add `export PATH="$HOME/.local/bin:$PATH"` |
| `error: externally-managed-environment` | PEP 668 restriction on Fedora/Ubuntu | Use `./install.sh` or `sudo dnf install python3-pillow` / `sudo apt install python3-pil` |
| Braille dots or blocks look like `?`, ``, or boxes | Terminal font lacks Unicode symbols | Switch to a Nerd Font (JetBrains Mono, Fira Code) |
| Horizontal black lines cutting through Braille | Terminal line-height is greater than `1.0` | Set terminal line-height/spacing to `1.0` |
| Washed out colors or weird banding | Terminal does not support 24-bit TrueColor | Verify `$COLORTERM` or switch to a modern terminal (Kitty, Alacritty, Ghostty) |
| Output wraps and looks shredded | Image width (`-w`) is wider than terminal columns | Reduce width with `-w 80` or use `-w $(tput cols)` |
| B&W Braille shows negative image | Terminal background is light instead of dark | Add the `-i` / `--invert` flag |

---

## 2. Installation & Dependency Resolution

### The Universal Plug & Play Installer
Luma includes an automated installer that handles permissions, path links, and system dependencies across all major distributions:
```bash
# From local repository:
./install.sh

# Or directly from GitHub:
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### Distribution-Specific Package Installation

#### Fedora / RHEL / Rocky Linux / CentOS
Modern Fedora (38+) enforces **PEP 668**, because Red Hat decided developers cannot be trusted with their own system Python (and to be fair, they have a point).
```bash
# Recommended native package:
sudo dnf install -y python3-pillow

# Run installer or clone directly:
./install.sh
```

#### Debian / Ubuntu / Linux Mint / Pop!_OS
```bash
# Recommended native package:
sudo apt update && sudo apt install -y python3-pil

# Or run installer:
./install.sh
```

#### Arch Linux / Manjaro / EndeavourOS
*(Yes, we know you use Arch btw, congrats, now please stop bringing it up at parties).*
```bash
# Recommended native package:
sudo pacman -S --noconfirm python-pillow

# Or via AUR (if available) / install.sh:
./install.sh
```

#### Isolated Virtual Environment (Universal Rootless Fallback)
If you do not have `sudo` privileges (for any certain reasons — e.g. you're on a school/work PC you definitely shouldn't be rice-ing up, your sysadmin has trust issues, or you straight up forgot your root password) and system pip is locked:
```bash
python3 -m venv ~/.local/share/luma/venv
~/.local/share/luma/venv/bin/pip install Pillow
mkdir -p ~/.local/bin
cat << 'EOF' > ~/.local/bin/luma
#!/bin/bash
exec "$HOME/.local/share/luma/venv/bin/python" "/path/to/Luma/lumart.py" "$@"
EOF
chmod +x ~/.local/bin/luma
ln -sf ~/.local/bin/luma ~/.local/bin/lumart
```

---

## 3. Terminal Emulators & Font Compatibility

Luma relies on two key Unicode character blocks:
1. **Braille Patterns (`U+2800` - `U+28FF`)**: 2x4 dot matrix cells (`⡀`, `⣿`, `⣾`, `⢦`).
2. **Half-Blocks (`U+2580` - `U+259F`)**: Top half-block (`▀`), bottom half-block (`▄`), and full blocks (`█`).

### Recommended Terminal Emulators
- **Tier 1 (Flawless TrueColor & Unicode)**:
  - **Ghostty**: Exceptional font rendering, perfect Braille cell bounding boxes.
  - **Kitty**: Fast GPU rendering, customizable line-height.
  - **Alacritty**: High performance, zero-latency rendering.
  - **WezTerm**: Native support for custom font ligatures and Braille.
  - **Windows Terminal**: Modern direct-write engine with full 24-bit ANSI color support.
  - **iTerm2** (macOS): Comprehensive 24-bit truecolor support.
- **Problematic / Legacy Terminals**:
  - **macOS default `Terminal.app`**: Lacks 24-bit Truecolor support (caps at 256 colors like it's 1999). Apple charges $700 for Mac Pro wheels but can't be bothered to give Terminal.app modern color support. Colors will look muddy or approximated. *Recommendation: Install Ghostty, Kitty, or iTerm2 and save your eyeballs.*
  - **Windows `cmd.exe` / Classic PowerShell**: A Mesozoic relic that only God knows why it's still alive. Terrible UTF-8 character encoding support and breaks if you look at it funny. *Recommendation: Use Windows Terminal with PowerShell 7+.*

### Fixing Braille Line-Height Glitches
If you notice horizontal stripes or gaps between lines of Braille art:
- **Cause**: Many modern terminal emulators add extra line-height (e.g., `1.2` or `1.5`) for code readability because they think you're reading War and Peace. Because Braille characters are expected to touch vertically, extra spacing breaks the continuous dot matrix and makes it look like window blinds.
- **Fix in Kitty (`~/.config/kitty/kitty.conf`)**:
  ```conf
  adjust_line_height 0
  ```
- **Fix in Alacritty (`~/.config/alacritty/alacritty.toml`)**:
  ```toml
  [font.offset]
  y = 0
  ```

---

## 4. Color Fidelity & TrueColor (24-bit ANSI)

### Checking Truecolor Support
To check whether your current terminal session supports truecolor:
```bash
echo $COLORTERM
```
If this prints `truecolor` or `24bit`, your terminal is ready.

If you are running inside **tmux** or **screen**, truecolor may be disabled unless configured in `~/.tmux.conf`:
```tmux
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
```

### Linear RGB vs sRGB Color Blending
Luma performs color blending inside **Linear RGB** rather than standard sRGB:
- **The Problem in Normal Converters**: Blending colors directly in sRGB creates muddy, dark borders (the "dark halo" effect) because sRGB gamma is non-linear (averaging colors directly in gamma space without linear correction is a mortal sin punishable by 10 years of maintaining legacy COBOL code).
- **The Luma Fix**: All pixel sub-blocks are linearized ($C_{\text{linear}} = C_{\text{srgb}}^{2.2}$), averaged with physically accurate light summation, and converted back to sRGB.

### Disabling Image Pre-Processing (`--raw-colors`)
By default, Luma's *Epic Color Engine* dynamically boosts saturation ($1.5\times$), contrast ($1.2\times$), and sharpness ($1.5\times$) to compensate for dark terminal backgrounds.
If your input image is already saturated or contains delicate pastel shades that look over-processed:
```bash
luma input.png --raw-colors --braille
```

---

## 5. Black & White, Manga Screentone & Braille Art

Luma features a dedicated high-definition black-and-white engine designed to mimic traditional Japanese manga screen-tones (*Ami-tone*).

### The Manga Art Pipeline (`--braille --no-color -d`)
To get authentic manga/anime ASCII art:
```bash
luma anime_girl.png --braille --no-color -d -w 140
```
- **Unsharp Masking**: Edge sharpening highlights line-art boundaries before downscaling (sharper than a freshly forged katana).
- **Contrast Stretching**: Pushes faint paper textures to pure white or black.
- **Bayer Matrix Ordered Dithering (`-d`)**: Uses a $4 \times 4$ dispersed dither matrix to translate continuous grayscale tones into variable dot density.

### Light vs Dark Terminals (`-i` / `--invert`)
- **Dark Terminal (Default)**: Bright pixels are represented by active Braille dots (`⣿`, `⠶`). Dark pixels remain blank spaces, letting the terminal background serve as black ink.
- **Light Terminal (White/Cream Background)**: Invert the logic using `-i`:
  ```bash
  luma image.png --braille --no-color -d -i
  ```

> [!CAUTION]
> If you are unironically using a white/light terminal background in 2026, please seek professional medical help. In the meantime, pass `-i` / `--invert` to prevent immediate retina evaporation.

---

## 6. Sizing, Aspect Ratio & Text-Wrapping Artifacts

### The 1:2 Character Cell Aspect Ratio
In standard monospace fonts, a single character cell is roughly **twice as tall as it is wide** ($1:2$ ratio).
- If an image is rendered with 1 pixel per character without compensation, it will look squished horizontally (stretched vertically), as if flattened by an 18-wheeler truck.
- Luma automatically adjusts vertical height depending on the chosen rendering engine:
  - **Braille Mode (`--braille`)**: A Braille character contains 2 horizontal dots and 4 vertical dots. Because $2:4 = 1:2$, Braille dots naturally have a square $1:1$ ratio!
  - **Half-Block Mode (`--blocks`)**: Each character cell holds 2 vertical pixels (top and bottom half).

### Preventing Line Wrapping
If an image is rendered wider than your terminal window, each row wraps around, turning the image into an illegible spiral.
- Match your current terminal width dynamically:
  ```bash
  luma image.png --braille -w $(tput cols)
  ```
- Or save to a file and view it using `cat` or `less -R` (the `-R` preserves raw ANSI color codes):
  ```bash
  luma image.png --braille -w 160 -o art.txt
  less -R art.txt
  ```

---

## 7. Color Swapping (`--swap`) Mechanics

The `--swap` option dynamically replaces specific color ranges in the image using 3D Euclidean distance in RGB color space (Pythagoras rolling in his grave knowing his theorem is being used to recolor anime waifus).

### Rules:
1. Arguments must be provided in **pairs**: `[color_to_replace] [new_color]`.
2. Supported color names:
   `red`, `green`, `blue`, `yellow`, `purple`, `pink`, `cyan`, `orange`, `white`, `black`, `gray`, `magenta`, `blurple`

### Examples:
```bash
# Swap purple hair to red, and blue eyes to yellow:
luma character.png --swap purple red blue yellow --braille
```

---

## 8. Configuration, Persistence & Localization (i18n)

### Config File Location
Luma persists user settings (such as chosen language) in:
```
~/.config/luma/config.json
```

### Changing Default Language
Luma defaults to English (`en`). You can switch and persist another language anytime:
```bash
# Spanish
luma --lang es

# Japanese
luma --lang ja

# Portuguese
luma --lang pt

# Russian
luma --lang ru

# German
luma --lang de

# Korean
luma --lang ko

# English (reset)
luma --lang en
```

### Resetting Configuration
To reset all configurations back to factory defaults:
```bash
rm -rf ~/.config/luma
```

---

## 9. Command Reference & Cheat Sheet

```bash
# 1. High-Resolution Epic Color Art (Default)
luma photo.jpg --braille

# 2. Maximum ANSI Pixel Density (Half-Blocks)
luma photo.jpg --blocks -w 120

# 3. True Manga / Anime B&W Braille with Screentone
luma anime.png --braille --no-color -d -w 140

# 4. Classic Terminal ASCII Art
luma logo.png -w 80

# 5. Save directly to file without polluting terminal buffer
luma wallpaper.png --blocks -w 180 -o output.txt

# 6. View saved color art
cat output.txt
# or with scrolling:
less -R output.txt
```

---
*Still running into issues? Open an issue on [GitHub](https://github.com/SilentBlox01/Luma/issues) with the output of `luma -v` and your terminal emulator details.*
