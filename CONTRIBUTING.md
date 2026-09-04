[English](CONTRIBUTING.md) | [Español](CONTRIBUTING.es.md) | [Português](CONTRIBUTING.pt.md) | [Русский](CONTRIBUTING.ru.md) | [日本語](CONTRIBUTING.ja.md) | [Deutsch](CONTRIBUTING.de.md) | [한국어](CONTRIBUTING.ko.md)

# Contributing to Luma

Thank you for your interest in improving Luma! This project pushes the graphical boundaries of the terminal, and all contributions are warmly welcomed.

## 🐛 Reporting Bugs or Suggesting Features

If you encounter an issue or have an awesome idea (such as a new rendering algorithm, dithering pattern, or animation support), please open an **Issue** on GitHub. Please include:
- Your operating system and terminal emulator (e.g., Fedora with Alacritty, Ubuntu with Kitty, Windows Terminal).
- The exact command line and arguments you used.
- If possible, a sample of the generated ASCII/ANSI art or the input image.

## 🛠️ Contributing Code

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or fix (`git checkout -b feature/awesome-new-engine`).
3. **Write and test your code**. The core engine logic lives in `lumart.py`.
4. **Commit your changes** with a clear commit message (`git commit -m 'feat: add Floyd-Steinberg dithering'`).
5. **Push to your branch** (`git push origin feature/awesome-new-engine`).
6. **Open a Pull Request**.

### Project Architecture
- `lumart.py`: The single-file core engine containing perceptual Linear RGB color blending, Bayer dithering, Braille/Half-block glyph sculpting, and localized CLI argument parsing.
- `install.sh`: Universal Plug & Play installer compatible with Fedora, Debian/Ubuntu, Arch Linux, openSUSE, and macOS.
- `build_packages.sh`: Automated package builder for PyInstaller standalone binaries, Debian packages (`.deb`), Red Hat/Fedora RPMs (`.rpm`), and Arch Linux PKGBUILDs.
- `pyproject.toml`: Modern packaging definition allowing `pipx install .` and `pip install --user .`.

### Coding Guidelines
- **Zero Heavy Dependencies**: Keep Luma lightweight and plug-and-play. Rely only on Pillow (`PIL`) and standard library modules. Avoid heavy dependencies like OpenCV or PyTorch unless completely optional and isolated.
- **Terminal Aesthetics**: Every new mode or feature must prioritize visual excellence and fidelity.
- **Multilingual Support**: If you add new CLI arguments or user-facing messages, update all 7 language dictionaries in `TRANSLATIONS` (`en`, `es`, `pt`, `ru`, `ja`, `de`, `ko`).

Have fun hacking terminal colors and graphics! 🎨
