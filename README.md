# Luma

**A high-fidelity image-to-terminal renderer written in Python.**

Luma is an open-source terminal rendering engine focused on one goal:

> **Maximum visual fidelity with minimum terminal space.**

Unlike traditional ASCII converters that simply map image brightness to characters, Luma explores different terminal glyph systems, Linear RGB color mathematics, and rendering techniques to preserve as much visual information as possible within a limited number of terminal cells.

## Features

* High-fidelity image rendering in the terminal
* ASCII, Braille and Block-based rendering
* **OS-Style Rendering (`--os-style`)**: Classic terminal characters (dots, letters) for Neofetch-style logos.
* **Real-time Color Swapping (`--swap`)**: Dynamically swap up to 5 colors based on 3D Euclidean color distance.
* **Epic Color Engine (Default)**: Averages colors in Linear RGB space to prevent muddy output, while applying dynamic contrast and saturation (HDR).
* Configurable output width
* Truecolor terminal support (24-bit ANSI)
* Designed for extremely small output sizes
* Python-based and highly extensible

## Example

```bash
# Convert an image using Braille characters, colors, and replacing purple with pink
luma image.png -w 45 --braille -c --swap purple pink
```

## Installation

You can run Luma directly from the source code or build it into a native Linux package (DEB, RPM, or Arch PKGBUILD).

**Option 1: Clone and run directly**
```bash
git clone https://github.com/YOUR_USERNAME/Luma.git
cd Luma
# Ensure you have Pillow installed
pip install Pillow
```

**Option 2: Build a native package**
Luma includes an automated build script to package the tool into a standalone binary using PyInstaller.
```bash
./build_packages.sh
```
After building, you can install it globally via your package manager:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-2.0.0.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-2.0.0.rpm`
- **Arch Linux**: Use the generated PKGBUILD in `dist/arch/`.

## Usage

If you installed the package, you can run `lumart` or `luma` from anywhere. Otherwise, run the python script directly.

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

Force retro OS-style character rendering (useful for OS logos):
```bash
python3 lumart.py image.png --os-style -c
```

## Philosophy

Terminal rendering is a form of visual compression.

The challenge is not simply converting an image into characters. The challenge is representing the greatest amount of visual information possible using the fewest terminal cells.

Luma therefore focuses on **perceptual fidelity**, utilizing mathematically accurate color spaces (Linear RGB vs sRGB) and dynamic HDR curves, rather than simply producing recognizable ASCII art.

## Roadmap

* [x] Initial image-to-terminal renderer
* [x] Braille rendering
* [x] Block-based rendering
* [x] Improved perceptual rendering (Linear RGB Engine)
* [x] Contrast and luminance processing (Epic Engine)
* [x] Real-time color mapping and thresholds
* [ ] Advanced dithering
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

Luma is released under the AGPL License.
