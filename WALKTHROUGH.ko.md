# 📖 Lumart (Luma) v2.5.0 마스터 매뉴얼, 사용 가이드 & 문제 해결 가이드
> **종합 단계별 마스터 가이드: 아키텍처, 4대 엔진, 서브커맨드, 완전한 플래그 백과사전, 실전 레시피, 그리고 완벽한 문제 해결 가이드(Troubleshooting).**

---

## 📑 목차

- [제1부: 기초 이론, 터미널 물리 & 아키텍처](#1)
  - [1.1 Lumart란 무엇인가?](#11)
  - [1.2 터미널 문자 그리드 물리와 화면비](#12)
  - [1.3 유니코드 타이포그래피 서브픽셀](#13)
  - [1.4 24비트 TrueColor & ECMA-48 이스케이프 시퀀스 압축](#14)
- [제2부: 4대 플래그십 엔진](#2)
  - [2.1 Mary Apex 3.5 (사실적 Oklab 지각 컬러 엔진)](#21)
  - [2.2 Trumble Orelx 2.2 (애니메이션 셀 셰이딩 & Capcom CPS-2 아케이드)](#22)
  - [2.3 Luris Mono 2.6 (만화 스크린톤, DoG 선화 & C++17)](#23)
  - [2.4 Spectra Weep 2.0 (실시간 비디오, 웹캠 & 다중 스펙트럼 셰이더)](#24)
- [제3부: 특수 서브커맨드 및 내장 도구](#3)
  - [3.1 lumart fetch (Fastfetch / Neofetch 프리셋 생성기)](#31)
  - [3.2 lumart bench (멀티코어 성능 및 지연 시간 벤치마크)](#32)
  - [3.3 lumart showcase (4-in-1 비교 캔버스)](#33)
  - [3.4 lumart info (시각적 이미지 분석기 및 최적 엔진 추천)](#34)
  - [3.5 lumart diff (두 이미지 간의 크로매틱 델타 히트맵)](#35)
  - [3.6 lumart slideshow (터미널 전체 화면 슬라이드쇼)](#36)
  - [3.7 lumart -I / --interactive (대화형 TUI 뷰어)](#37)
  - [3.8 lumart animate (GIF 트랜스코더 & 비디오 컴파일러)](#38)
- [제4부: 명령어 플래그 및 옵션 전체 백과사전](#4)
- [제5부: 실전 레시피 및 실무 워크플로우](#5)
- [제6부: 마스터 문제 해결 가이드 (Troubleshooting)](#6)

---

## 1. 제1부: 기초 이론, 터미널 물리 & 아키텍처

### 1.1 1.1 Lumart란 무엇인가?
Lumart (Luma) v2.5.0 Apex Nova.

### 1.2 1.2 터미널 문자 그리드 물리와 화면비
* `--font-ratio`: Default `0.5` (width/height ratio compensation).

```bash
lumart photo.png --font-ratio 0.45  # condensed fonts
lumart photo.png --font-ratio 0.55  # expanded fonts
```

### 1.3 1.3 유니코드 타이포그래피 서브픽셀
* **Sextants (`-S`)**: 2x3 (6 subpixels/cell) — Mary Apex default.
* **Braille (`-B`)**: 2x4 (8 subpixels/cell) — Fine curves and outlines.
* **Quadrants (`-Q`)**: 2x2 (4 subpixels/cell).
* **Half-Blocks (`--blocks`)**: 1x2 (2 vertical pixels/cell) with 24-bit TrueColor.

### 1.4 1.4 24비트 TrueColor & ECMA-48 이스케이프 시퀀스 압축
* Foreground: `\033[38;2;R;G;Bm`
* Background: `\033[48;2;R;G;Bm`
* ECMA-48 escape compression reduces terminal payload by up to 65%.

---

## 2. 제2부: 4대 플래그십 엔진

### 2.1 2.1 Mary Apex 3.5 (사실적 Oklab 지각 컬러 엔진)
* `-E mary`
* Perceptual Oklab space (\Delta E), 3-iteration K-Means clustering, Weber-Fechner Contrast Sensitivity Function (CSF).

### 2.2 2.2 Trumble Orelx 2.2 (애니메이션 셀 셰이딩 & Capcom CPS-2 아케이드)
* `-E trumble`
* 1990s Capcom CPS-2 / Neo-Geo cel-shading, Laplacian ink outlines, Bayer ordered dithering.

### 2.3 2.3 Luris Mono 2.6 (만화 스크린톤, DoG 선화 & C++17)
* `-E luris` (`-m`, `-s`, `-ch`)
* Native C++17 OpenMP SIMD, Manga Screentone Bayer 8x8 (`-m`), clean DoG pencil sketch (`-s`), 45-degree pen crosshatch (`-ch`), transparent stickers (`--transparent`).

### 2.4 2.4 Spectra Weep 2.0 (실시간 비디오, 웹캠 & 다중 스펙트럼 셰이더)
* `-E spectra` (`-W`, `--shader <name>`)
* Real-time video player, 60 FPS live webcam streaming, 12 multi-spectral shaders: `neon`, `thermal`, `tron`, `matrix`, `amber`, `manga`, `hologram`, `glitch`, `phosphor-bloom`, `solarize`.

---

## 3. 제3부: 특수 서브커맨드 및 내장 도구

### 3.1 3.1 lumart fetch (Fastfetch / Neofetch 프리셋 생성기)
```bash
lumart fetch avatar.png -w 38
```
* Auto-crops empty borders (`--fastfetch`), generates TrueColor half-blocks in `~/.config/fastfetch/<name>_logo.ans`, and prints ready-to-copy `config.jsonc` block.

### 3.2 3.2 lumart bench (멀티코어 성능 및 지연 시간 벤치마크)
```bash
lumart bench photo.jpg -w 100
```
* Measures rendering latency (`ms`), throughput (`MP/s`), and `FPS` across all engines.

### 3.3 3.3 lumart showcase (4-in-1 비교 캔버스)
```bash
lumart showcase art.png -w 80 -o showcase.png
```
* 4-in-1 comparison quad-view (Mary, Trumble, Luris, Spectra).

### 3.4 3.4 lumart info (시각적 이미지 분석기 및 최적 엔진 추천)
```bash
lumart info art.png
```
* Resolution, aspect ratio, luminance, top 6 dominant colors (HEX/ANSI), and optimal engine recommendation.

### 3.5 3.5 lumart diff (두 이미지 간의 크로매틱 델타 히트맵)
```bash
lumart diff img1.png img2.png -w 80
```
* Pixel-by-pixel delta heatmap and average color deviation percentage.

### 3.6 3.6 lumart slideshow (터미널 전체 화면 슬라이드쇼)
```bash
lumart slideshow ./wallpapers/ --delay 3.0
```
* Fullscreen terminal slideshow with keyboard controls.

### 3.7 3.7 lumart -I / --interactive (대화형 TUI 뷰어)
```bash
lumart -I image.png
```
* Interactive TUI viewer (`+`/`-` brightness, `M`/`T`/`L` engine switch, `G` manga mode, `Z` zoom).

### 3.8 3.8 lumart animate (GIF 트랜스코더 & 비디오 컴파일러)
```bash
lumart animate clip.mp4 -o output.gif --fps 30
```
* Transcode video or frame sequences to optimized animated GIFs.

---

## 4. 제4부: 명령어 플래그 및 옵션 전체 백과사전

### Engines & Textures
* `-E, --engine <name>`: `mary`, `trumble`, `luris`, `spectra`, `color`, `mono`, `bw`, `manga`, `sketch`, `crosshatch`.
* `-S, --sextants`: Unicode 2x3 micro-blocks (Mary Apex default).
* `-B, --braille`: Unicode 2x4 Braille dots (8 subpixels/cell).
* `-Q, --quadrants`: Unicode 2x2 blocks.
* `--blocks`: Half-blocks (`▀` / `▄`, 24-bit TrueColor).
* `-m, --manga`: Manga screentone (Bayer 8x8 + DoG).
* `-s, --sketch`: Pure pencil sketch line art.
* `-ch, --crosshatch`: 45-degree pen crosshatch shading.
* `-cs, --charset <name>`: `dense`, `standard`, `blocks`, `math`, `runes`, `katakana`, `crosshatch`.
* `--matrix`: Matrix Katakana code + green P1 phosphor bloom (525nm).
* `--matrix-rain`: Animated downward falling digital rain.

### Dimensions & Viewport
* `-w, --width <cols>`: Fixed output width in columns.
* `-F, --fit`: Auto-fit viewport to terminal without vertical scroll.
* `--fastfetch, --logo`: Auto-crop whitespace/transparent margins.
* `--font-ratio <float>`: Terminal font aspect ratio (default: `0.5`).
* `--crop "x,y,w,h"`: Crop specific region before rendering.
* `--zoom <float>`: Digital zoom multiplier (e.g. `1.5` for 150%).
* `--rotate <0|90|180|270>`: Clockwise rotation in degrees.
* `--flip <h|v>`: Geometric mirror: horizontal (`h`) or vertical (`v`).
* `--border <style>`: Unicode decorative border (`rounded`, `single`, `double`, `heavy`, `ascii`, `blocks`).
* `--align <left|center|right>`: Viewport horizontal alignment.
* `--center`: Shorthand alias for `--align center`.

### Color & Shaders
* `-c, --color`: Enable 24-bit TrueColor (default).
* `--no-color`: Disable ANSI colors (monochrome route).
* `--brightness <float>`: Brightness multiplier (default: `1.0`).
* `--contrast <float>`: Contrast multiplier (default: `1.0`).
* `--saturation <float>`: Saturation multiplier (default: `1.0`).
* `--boost, --vibrant`: Enhanced saturation and Retinex curve punch.
* `--gamma <float>`: Non-linear midtone gamma exponent.
* `-i, --invert`: Invert luminance mapping.
* `--swap <c1> <c2>`: Dynamically swap two colors in 3D RGB space.
* `--theme, --palette <name>`: `cyberpunk`, `dracula`, `nord`, `catppuccin`, `gruvbox`, `synthwave`, `monokai`, `gameboy`, `amber`.
* `--crt, --scanlines [green|amber|color|scanlines]`: Analog CRT monitor simulation.
* `--shader <name>`: `neon`, `cyberpunk`, `thermal`, `tron`, `matrix`, `amber`, `manga`, `hologram`, `glitch`, `phosphor-bloom`, `solarize`.
* `-d, --dither <algo>`: `atkinson`, `floyd`, `bayer`, `none`.

### Animation & Performance
* `--loop`: Continuous loop playback in terminal.
* `--fps, --target-fps <float>`: Target playback or GIF export framerate.
* `--preload, --smooth`: Preload and pre-render all frames in RAM for zero-lag 60 FPS.
* `--instant`: Immediate render output (default).
* `--reveal`: Progressive line-by-line reveal animation.

### Export, Stickers & Clipboard
* `-o, -O, --save <path>`: Export to high-res image or animated GIF (`.png`, `.jpg`, `.gif`).
* `--transparent`: Exclusive to Luris Mono: transparent alpha sticker export.
* `-r, --remove-bg`: Perceptual flood-fill background removal.
* `--bg-tolerance <1-100>`: Tolerance threshold for background removal (default: `32`).
* `-C, --copy`: Copy formatted ANSI art (with color codes) to clipboard.
* `--copy-plain`: Copy clean plain uncolored ASCII text to clipboard.
* `--paste`: Render image from clipboard (Ctrl+C).

### System & Localization
* `--lang <code>`: Set language (`en`, `es`, `fr`, `de`, `pt`, `ru`, `ja`, `ko`).
* `-v, --version`: Full diagnostic report of hardware, OS, and native engines.
* `-H, --history [N]`: View last N commands in history.
* `-R, --replay [N]`: Re-execute command N from history.
* `--clear-history`: Purge history file.
* `--completions <bash|zsh|fish>`: Generate shell completion scripts.
* `-u, --check-update`: Check GitHub for updates.
* `-uu, --upgrade`: Interactive auto-upgrade assistant.
* `-dg, --downgrade`: Roll back to previous version from backup.

---

## 5. 제5부: 실전 레시피 및 실무 워크플로우

### Recipe 1: Fastfetch Logo
```bash
# TrueColor blocks (Recommended)
lumart fetch avatar.png -w 38

# Minimalist manga screentone
lumart avatar.png -w 38 --fastfetch -m -o ~/.config/fastfetch/logo_manga.ans

# High-resolution Braille
lumart avatar.png -w 38 --fastfetch -E mary -B -o ~/.config/fastfetch/logo_braille.ans
```

### Recipe 2: Transparent Stickers
```bash
lumart character.png -w 80 -m --transparent -o sticker.png
lumart character.png -w 80 -m -r --bg-tolerance 40 --transparent -o sticker_clean.png
```

### Recipe 3: 60 FPS RAM Preloaded GIFs
```bash
lumart anim.gif -w 70 --loop --fps 60 --preload
lumart anim.gif -w 60 --theme synthwave --fps 30 -o anim_synthwave.gif
```

### Recipe 4: Cyberpunk Live Webcam Stream
```bash
lumart -W 0 --matrix --crt green --fps 60
lumart -W 0 --shader thermal --fps 30
```

### Recipe 5: Bash Automation & MOTD
```bash
lumart ~/.config/banner.png -w 60 --border rounded --align center --instant
lumart "https://raw.githubusercontent.com/fastfetch-cli/fastfetch/dev/assets/arch.png" -w 50
lumart --paste -w 60 --border double
lumart logo.png -w 40 -C
```

---

## 6. 제6부: 마스터 문제 해결 가이드 (Troubleshooting)

### Diagnostic Checklist
| Symptom | Primary Cause | Immediate Resolution |
| :--- | :--- | :--- |
| `command not found: lumart` | `~/.local/bin` missing from `$PATH` | Add `export PATH="$HOME/.local/bin:$PATH"` to shell config or run `./install.sh`. |
| Braille dots or blocks look like `?` or empty boxes | Active font lacks Unicode glyph coverage | Install and set a **Nerd Font** (JetBrains Mono Nerd Font, FiraCode, Cascadia Code). |
| Horizontal black gaps between Braille lines | Terminal line-height > 1.0 | Set terminal line-height to `1.0` or `0px` in terminal settings. |
| Washed-out colors / 16-color banding | Terminal lacks TrueColor support | Run `export COLORTERM=truecolor` or use Ghostty, Kitty, Alacritty, WezTerm. |
| Output wraps around lines and shreds | Width exceeds terminal columns | Use `-F` (`--fit`) or reduce width with `-w 80`. |
| Light background looks inverted | Light terminal background | Auto-detected in Luris Mono; pass `-i` / `--invert` for manual override. |
| Python fallback instead of native C++ | Native shared libraries not compiled | Run `g++ -O3 -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so` and `monochrome.cpp`. |
| OpenCV error in Spectra engine | `opencv-python` missing | Install with system package manager (`python3-opencv`) or `pip install opencv-python`. |
| Webcam permission error | Insufficient video device permissions | Run `sudo usermod -aG video $USER`. |
| Image vertically stretched or squashed | Terminal font ratio deviates from 1:2 | Calibrate with `--font-ratio <float>` (e.g. `--font-ratio 0.45` or `0.55`). |
| Transparent sticker exports black background | Transparency exclusive to Luris Mono | Run with `-m --transparent -o out.png`. Color models require solid terminal canvas. |
| WebP export rejected | WebP permanently banned | Export to `.png` or `.jpg` (`-o out.png`). |

### Terminal Emulator & TrueColor Settings
* **Tmux TrueColor Passthrough (`~/.tmux.conf`)**:
  ```tmux
  set -g default-terminal "tmux-256color"
  set -ga terminal-overrides ",*256col*:Tc"
  ```
* **Verify System Diagnostics**:
  ```bash
  lumart -v
  ```
* **Package Managers**:
  * Arch / AUR: `yay -S lumart`
  * Debian / Ubuntu: `sudo apt install ./dist/deb/lumart_2.5.0-1_all.deb`
  * Fedora / RHEL: `sudo dnf install ./dist/rpm/lumart-2.5.0-1.noarch.rpm`

---
*Lumart (Luma) v2.5.0 • Apex Nova*
