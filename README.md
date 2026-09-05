[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**A high-fidelity image-to-terminal renderer written in Python and modern C/C++.**

Luma is an open-source terminal rendering engine focused on one goal:

> **Maximum visual fidelity with minimum terminal space.**

Unlike traditional ASCII converters that simply map image brightness to characters, Luma explores different terminal glyph systems, Linear RGB color mathematics, and native C/C++ computer vision algorithms to preserve as much visual information as possible within a limited number of terminal cells.

## Features

* High-fidelity image rendering in the terminal
* ASCII, Braille and Block-based rendering
* **Hybrid Dual-Engine Architecture**:
  * **Linear RGB Color Engine** (Python / Pillow): HDR contrast curves, linear color space blending ($C_{\text{linear}} = C_{\text{srgb}}^{2.2}$), and 24-bit TrueColor ANSI.
  * **High-Performance Monochrome & Manga Engine** (Native C++17): Sub-10ms execution, Difference of Gaussians (DoG) lineart extraction, Bill Atkinson (1984 MacPaint) error diffusion, and 8x8 Bayer screentone halftoning.
* **Engine Selector (`-E`, `--engine`)**: Switch dynamically between `color`, `mono`, `bw`, `manga`, and `sketch`.
* **Pure Line Art Sketch Mode (`-s`, `-E sketch`)**: Zero-noise anime and illustration contour extraction.
* **Manga Screentone 2.0 (`-m`, `-E manga`)**: Authentic print screentone (*Ami-tone*) for midtones with pure paper whites and solid black ink.
* **Atkinson & Halftone Dithering (`-d` / `--dither`)**: Supports `atkinson`, `floyd`, `bayer`, and `none`.
* **2x2 Quadrant HD Blocks (`--blocks`)**: 4 subpixels per cell using Unicode quadrant elements (`▘▝▀▖▌▞▛▗▚▐▜▄▙▟█`).
* **OS-Style Rendering (`--os-style`)**: Classic terminal characters (dots, letters) for Neofetch-style logos.
* **Real-time Color Swapping (`--swap`)**: Dynamically swap colors based on 3D Euclidean color distance.
* **Zero External Native Dependencies**: The C++ engine uses self-contained public domain C headers (`stb_image.h` and `stb_image_resize2.h`). No OpenCV or libpng required.
* **Full Python Fallback Parity**: If a C++ compiler is not available, Luma falls back to an identical pure Python implementation seamlessly.
* Configurable output width and automatic light/dark terminal detection (`-i`, `--invert`)
* Interactive upgrade (`-uu`), rollback (`-dg`), and update (`-u`) suite
* Full system & engine diagnostics (`-v`, `--version`)

## Example

```bash
# Convert an image using Braille characters, colors, and replacing purple with pink
luma image.png -w 45 --braille -c --swap purple pink
```

## Installation

You can install Luma with a single command, run it directly from source, or build it into a native Linux package (DEB, RPM, or Arch PKGBUILD).

**Quick Install (Recommended):**
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

**Option 1: Run directly from source / Local installer**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
./install.sh
```

**Option 2: Download Pre-built Packages**
You can download ready-to-use `.deb` or `.rpm` packages directly from the [GitHub Releases](https://github.com/SilentBlox01/Luma/releases) page.

**Option 3: Compile and build native packages yourself**
Luma includes an automated build script to package the tool into a standalone binary using PyInstaller.
```bash
chmod +x build_packages.sh
./build_packages.sh
```
After compiling, you can install it globally via your package manager:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-*.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-*.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

**Option 4: Compiling the Native C++ Engine Manually**
If you want to compile only the native C++ engine without building full packages:
```bash
# Standalone CLI binary:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono

# Shared library (for Python ctypes in-process acceleration):
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
```
*(No external dependencies needed — uses embedded `stb_image.h` and `stb_image_resize2.h`)*

## Usage

If you installed the package or used the installer, you can run `lumart` or `luma` from anywhere. Otherwise, run the python script directly.

> **💡 Pro Tip:** Luma works beautifully with transparent backgrounds! The engine automatically ignores transparent pixels, which makes logos and characters pop perfectly against your terminal's background.

```bash
# Basic usage
python3 lumart.py image.png
```

Specify the output width (in characters):
```bash
python3 lumart.py image.png -w 30
```

Enable high-fidelity Braille rendering with Truecolor:
```bash
python3 lumart.py image.png --braille -c
```

Render in Pure Line Art Sketch mode (clean DoG contours, no noise):
```bash
python3 lumart.py image.png -E sketch -w 100
# or: python3 lumart.py image.png -s -w 100
```

Render in Manga Screentone 2.0 mode (DoG outlines + 8x8 Bayer ami-tone screentone):
```bash
python3 lumart.py image.png -E manga -w 120
# or: python3 lumart.py image.png -m -w 120
```

Render in Monochrome with Atkinson Dithering (1984 MacPaint error diffusion):
```bash
python3 lumart.py image.png -E mono -d atkinson -w 100
# or classic floyd-steinberg: python3 lumart.py image.png -E mono -d floyd -w 100
```

Render in 2x2 Quadrant Subpixel HD Blocks:
```bash
python3 lumart.py image.png -E mono --blocks -w 80
```

Render in pure Monochrome without colors:
```bash
python3 lumart.py image.png -E mono --braille -w 100
```

Force retro OS-style character rendering (useful for OS logos):
```bash
python3 lumart.py image.png --os-style -c
```

Display full System & Engine Diagnostics:
```bash
luma -v
# or: luma --version
```

## Updating & Rollback

Luma gives you explicit control over updates and rollbacks:

- **Check for updates (no downloads or changes):**
  ```bash
  luma -u
  # or: luma --update / luma --check-update
  ```
  *(Displays your current version, the latest GitHub version, release history, and update status)*

- **Interactive Upgrade:**
  ```bash
  luma -uu
  # or: luma --upgrade
  ```
  *(Lets you select which version to install, previews release notes, and backs up your existing binary to `~/.config/luma/backup/`)*

- **Interactive Rollback / Downgrade:**
  ```bash
  luma -dg
  # or: luma --downgrade / luma --rollback
  ```
  *(Opens an interactive menu allowing you to pick from locally saved backup binaries or download any past GitHub release)*

  You can also pass a specific version directly:
  ```bash
  luma -dg 2.1.0
  ```

Luma also checks periodically in the background for new versions and non-intrusively notifies you in your terminal when an update is available.


## Uninstallation

If you want to remove Luma from your system, the command depends on how you installed it:

**If installed via Package Manager (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**If installed via pip:**
```bash
pip uninstall lumart
```

**If installed manually:**
You can run the provided uninstaller script:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Philosophy

Terminal rendering is a form of visual compression.

The challenge is not simply converting an image into characters. The challenge is representing the greatest amount of visual information possible using the fewest terminal cells.

Luma therefore focuses on **perceptual fidelity**, utilizing mathematically accurate color spaces (Linear RGB vs sRGB) and dynamic HDR curves, rather than simply producing recognizable ASCII art.

## Troubleshooting

Having issues with fonts, colors, or missing modules? Check out our [Troubleshooting Guide](TROUBLESHOOTING.md) for quick fixes to common problems.

## Roadmap

* [x] Initial image-to-terminal renderer
* [x] Braille rendering
* [x] Block-based rendering
* [x] Improved perceptual rendering (Linear RGB Engine)
* [x] Contrast and luminance processing (HDR Color Engine)
* [x] Dual-Engine Architecture (Color & Native C++ Monochrome/Manga)
* [x] Real-time color mapping and thresholds
* [x] Advanced ordered dithering (Bayer matrix)
* [ ] Automatic glyph selection
* [ ] Image similarity benchmarks
* [ ] Rendering optimization
* [ ] Machine-learning assisted rendering
* [ ] Video and GIF rendering support
* [ ] Expanded terminal glyph systems

## Contributing

Luma is an open-source project and contributions are welcome.

If you have an idea for a rendering algorithm, optimization, glyph system, benchmark, or improvement, feel free to open an issue or submit a pull request. (See `CONTRIBUTING.md` for more details).

## License

Luma is released under the GNU Affero General Public License v3.0 (AGPL-3.0). See the `LICENSE` file for more details.
