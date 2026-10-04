# 📜 Lumart Changelog & Engineering Chronicle

All notable changes to the **Lumart (Luma)** visual engineering suite will be documented in this chronicle.  
The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.5.0] — "Apex Nova" — 2026-10-03

> *"To bring graphics into the terminal is not to compromise; it is to elevate text into an art form."*

Lumart v2.5.0 "Apex Nova" introduces 11 major features, expanding Lumart from a terminal image renderer into a comprehensive, industrial-grade terminal visual suite with real-time interactivity, intelligent background removal, retro monitor simulation, visual diffing, and native shell ecosystem integration.

### 🚀 11 Major New Features

1. **Intelligent Background Removal (`-r`, `--remove-bg`)**:
   * **Standalone Zero-Loss Mode**: Running `lumart -r <image>` isolates the primary subject and exports a full-resolution transparent PNG with 100% of original fidelity preserved.
   * **Model-Integrated Mode**: Combining `-r` with engine flags (e.g. `lumart -r -E mary <image>`) automatically removes the background first and renders the isolated subject into terminal ANSI/ASCII.
   * Seamless multi-backend architecture with GrabCut contour isolation and automated `rembg` integration.

2. **Terminal Theme Palette Synchronization (`--theme`, `--palette`)**:
   * Harmonize visual outputs with your favorite terminal color schemes in 3D Euclidean RGB space:
     * `catppuccin` (warm pastel aesthetic)
     * `dracula` (high-contrast dark purple aesthetic)
     * `nord` (arctic icy blue aesthetic)
     * `gruvbox` (retro groove earthy aesthetic)
     * `synthwave` / `vaporwave` (neon magenta & cyan 80s aesthetic)
     * `gameboy` (classic 1989 Nintendo 4-shade green LCD aesthetic)
     * `solarized` (precision low-contrast solarized palette)

3. **Retro CRT Scanlines & Phosphor Monitor Simulation (`--crt`, `--scanlines`)**:
   * Simulates classic analog cathode ray tube monitors:
     * `green`: Monochrome P1 green phosphor monitor.
     * `amber`: Warm P3 amber monochrome display.
     * `color`: Aperture grille CRT with alternating scanline luminescence.
     * `scanlines`: Subtle dark horizontal beam scanlines.

4. **Interactive Terminal Slideshow Gallery (`--slideshow`, `--delay`)**:
   * Transform your terminal into a responsive interactive art gallery for folders or file lists:
     * Keyboard controls: `[Space]` next slide, `[Left/Right Arrows]` navigate, `[P]` pause/resume, `[R]` random shuffle, `[Q]` quit.
     * Fully compatible with `--theme`, `--crt`, and custom width constraints.

5. **Matrix Code Ramp & Digital Rain Engine (`--matrix`, `--matrix-rain`)**:
   * Dedicated Katakana (`ﾘ`, `ﾕ`, `ﾒ`, `ﾓ`, `ﾊ`, etc.) and binary code ramp mapped to luminosity.
   * `--matrix`: Static high-density Matrix render in phosphor green.
   * `--matrix-rain`: Dynamic falling digital Katakana rain animation resolving smoothly into the target image.

6. **Direct UNIX STDIN Piping (`cat img.png | lumart -`)**:
   * Load and render image streams directly from standard input without creating temporary files on disk:
     * `cat logo.png | lumart - -w 80`
     * `curl -sL https://example.com/art.png | lumart - -F`

7. **Raw ANSI & Plain Text Fast-Export (`-o banner.ans`, `-o banner.txt`)**:
   * Export raw TrueColor ANSI escape sequences to `.ans` / `.asc` for instant (0.0001 ms) MOTD and `.bashrc` load times with zero processing latency.
   * Export `.txt` with all ANSI codes stripped for clean plain text documentation and Markdown code blocks.

8. **Smart System Clipboard Integration (`-C`, `--copy`, `--copy-plain`)**:
   * `-C` / `--copy`: Automatically pipes ANSI TrueColor art to the native clipboard via `wl-copy` (Wayland), `xclip` / `xsel` (X11), `pbcopy` (macOS), or `clip.exe` (WSL).
   * `--copy-plain`: Copies clean plain ASCII text without escape sequences.

9. **Visual Side-by-Side Image Diff (`lumart diff <img1> <img2>`, `--diff`)**:
   * Dual-pane terminal comparison layout displaying both images side by side with real-time RMSE pixel color delta telemetry.

10. **Framing Crop & Digital Zoom Resampling (`--crop`, `--zoom`)**:
    * `--crop`: Frame images with presets (`center`, `square` 1:1) or custom bounds `x,y,w,h` in pixels or percentages.
    * `--zoom`: Centered digital zoom with high-fidelity Lanczos resampling.

11. **Interactive Live Parameter Tuning TUI (`-I`, `--interactive`, `--tui`)**:
    * Real-time keyboard-driven terminal dashboard to experiment with aesthetics on the fly:
      * `[+/-]`: Dynamic width adjustment.
      * `[M]`: Cycle engines (Mary Apex, Trumble Orelx, Luris Mono).
      * `[T]`: Cycle themes and color palettes.
      * `[C]`: Cycle CRT phosphor monitor filters.
      * `[D]`: Cycle dithering algorithms (Atkinson, Floyd-Steinberg, Bayer).
      * `[B]`: Toggle Retinex arcade boost.
      * `[S]`: Export current render directly to file.
      * `[Enter]`: Freeze and print render to standard output.
      * `[Q]`: Exit TUI.

12. **Spectra Weep 2.0 ("Nova Vision") Real-Time Video & Stream Engine**:
    * **Universal Video & Camera Player**: Plays local video files (`.mp4`, `.webm`, `.mkv`, `.mov`, `.avi`, `.flv`, etc.) and webcam streams (`-W`) at smooth 30-60 FPS directly in the terminal.
    * **8 Interactive Real-Time Shaders**:
      * `[1] Normal`: Adaptive TrueColor photorealism.
      * `[2] Cyberpunk Neon`: Vibrant magenta/cyan synthwave color grade.
      * `[3] Matrix Phosphor`: Falling digital code stream in classic P1 green.
      * `[4] Thermal FLIR`: Infrared false-color heat map (cold blue to white-hot).
      * `[5] Manga Ink`: High-contrast dynamic graphic novel ink in motion.
      * `[6] Edge Tron`: Real-time Canny edge detection with electric cyan glow.
      * `[7] Amber Phosphor`: Warm vintage P3 monochrome terminal aesthetic.
      * `[8] Theme Sync`: Maps live video dynamically to the active CLI `--theme`.
    * **4 Dynamic Texture Modes (`[T]`)**: Half-blocks (`▀/▄`), Braille 2x4 (`⣿`), ASCII Glyphs (` .:-=+*#%@`), and Matrix Katakana (`ﾘﾕﾒﾓﾊ...`).
    * **Hotkeys in Hot-Stream**: `[Space]` pause, `[◄/►]` frame-by-frame step, `[+/-]` playback speed, `[S]` instant snapshot saved to high-res PNG, `[C]` toggle CRT scanlines, `[R]` rewind, `[Q]` quit.
    * **Direct Video-to-GIF Conversion**: Running `lumart video.mp4 -o out.gif` renders and exports the clip straight into an optimized animated GIF with all active styling applied.

13. **Animated GIF Engine Overhaul & Zero-Lag Playback**:
    * **Instantaneous 0 ms Startup (Zero-Lag Lazy Caching)**: Eliminates pre-rendering pauses. The first frame displays in 0 ms, subsequent frames render lazily on the fly and are stored in memory for smooth looping.
    * **Full Aesthetic Pipeline Support**: Animated GIFs now honor `--theme` (Dracula, Synthwave, Catppuccin, etc.), `--crt` scanlines, `--crop`, and `--remove-bg` seamlessly across terminal playback and GIF exports (`-o anim.gif`).
    * **Interactive Hotkeys**: `[Space]` pause, `[◄/►]` step, `[+/-]` speed, `[S]` snapshot, `[R]` restart, `[Q]` quit.

---

## [2.4.1] — "Apex Horizon" — 2026-09-10

> *"The greatest feat of automation is having the wisdom to do nothing when nothing needs to be done."*

Lumart v2.4.1 is a quality-of-life and safety patch introducing foolproof safeguards for update and rollback commands, ensuring that attempting to upgrade or downgrade to the currently active version is handled gracefully without redundant downloads, unnecessary backups, or file modifications.

### 🛡️ Foolproof Version Safeguards & Directional Guards
* **Zero-Action Idempotency (`already_on_version`)**:
  * Running an upgrade (`lumart -uu [VERSION]`) or downgrade (`lumart -dg [VERSION]`) pointing to the version already currently installed immediately notifies the user:
    ```text
    ℹ️ You are already on version v2.4.1. No actions were taken.
    ```
  * Exits cleanly with status `0` without making network queries to GitHub, without downloading files, and without creating redundant backups on disk.
* **Auto-Upgrade Clean Notification**:
  * Running `lumart -uu` when already on the latest available release now explicitly clarifies that no actions were taken:
    ```text
    ✅ Luma is already on the latest version (v2.4.1). No actions were taken.
    ```
* **Directional Guidance**:
  * Attempting to "upgrade" to an older version (`lumart -uu <older_version>`) warns the user and suggests using `lumart -dg`.
  * Attempting to "downgrade" to a newer version (`lumart -dg <newer_version>`) warns the user and suggests using `lumart -uu`.
* **Optional Version Target for `-uu`**:
  * `--upgrade` (`-uu`) now supports an optional positional target version string (`nargs="?"`), matching `--downgrade` (`-dg`).
* **Multilingual Localization Across 8 Locales**:
  * New foolproof status messages and directional alerts fully translated and tested across English (`en`), Spanish (`es`), Portuguese (`pt`), Russian (`ru`), Japanese (`ja`), German (`de`), Korean (`ko`), and French (`fr`).

---

## [2.4.0] — "Apex Horizon" — 2026-09-09

> *"CPU cycles are cheap, memory is abundant, but ugly terminal art is an unforgivable aesthetic crime against humanity."*

Lumart v2.4.0 is our biggest architectural and user-experience upgrade yet. We completely overhauled the CLI flag architecture, introduced high-speed continuous multi-frame terminal animations, enforced strict diplomatic relations between incompatible command-line flags, and modernized the entire installation and packaging pipeline.

### 🌟 New Features & Flag Additions

* **The `--loop` Arcade Animation Mode**:
  * Added `--loop` flag for ultra-smooth, jitter-free terminal playback of multi-frame GIFs and APNGs.
  * **Why not `animate`?** The creator has officially quarantined the word `animate` for top-secret, classified future plans that our 3D terminals are not yet enlightened enough to witness. Do not question the plan. Embrace `--loop`.
  * **Zero-Jitter RAM Pre-Caching**: Rather than parsing frames on the fly (which causes horrible frame-drops and disk chattering), Lumart pre-renders all frames into ANSI escape sequences in RAM. Playback hits a silky-smooth 60 FPS directly in your terminal console.
  * **Interactive Keyboard Catch**: Pressing `Ctrl+C` cleanly restores terminal cursor visibility, resets ANSI colors, and exits without leaving your terminal in an existential crisis where typed text is invisible.

* **Multi-Frame Animated GIF Compilation (`-o` / `--save`)**:
  * You can now export full multi-frame animations directly to disk!
  * Running `lumart dance.gif --loop -o result.gif` (or `--save result.gif`) rasterizes every single frame through the active engine with subpixel geometry and stitches them into a standardized, shareable `.gif`.

* **Terminal Viewport Auto-Fitting (`-F`, `--fit`)**:
  * **The Problem**: Running an ASCII converter that spews 300 lines of output into an 80x24 terminal, forcing you to scroll up for five minutes to see your anime character's forehead.
  * **The Solution**: `-F` (or `--fit`) calculates the 2D aspect ratio, factors in the non-square terminal font height ratio (default `0.5`), and scales the output so the entire image fits snugly inside your viewport. Zero scrolling required.

* **Fastfetch / Logo Auto-Cropping (`--fastfetch`, `--logo`)**:
  * Automatically detects and crops empty whitespace or transparent alpha margins from the outer perimeter of an image. Perfect for tight system-fetch banners where every column of screen real estate is sacred.

* **EXIF Auto-Orientation for Smartphone Photos**:
  * Photos taken with mobile phones (which store orientation metadata instead of rotating pixels) now pass through `ImageOps.exif_transpose()`. No more seeing your cat tilted sideways at a 90-degree angle.

* **Minimalist & Fast Diagnostics Card (`lumart -v` / `--version`)**:
  * Replaced the verbose essay of text with a sleek, minimalist diagnostics card inspired by `fastfetch` and `neofetch`.
  * Instantly reports active engine backends (C++17 OpenMP vs Python fallback), terminal dimensions, color banding depth (TrueColor vs 16-color), and Python runtime.

---

### 🛡️ Semantic CLI Flag Diplomatic Accords (Incompatibility Handling)

In previous versions, passing conflicting flags like `--instant` and `--reveal` simultaneously resulted in a philosophical paradox where the computer tried to both hurry up and take its time.

v2.4.0 introduces strict pedagogical error enforcement with **Exit Code 2**:

| Conflicting Flags | The Philosophical Crime | The Verdict |
| :--- | :--- | :--- |
| `-F / --fit` + `-w / --width` | Asking Lumart to simultaneously auto-fit the screen *and* force a rigid fixed width is like ordering a vegan steak, extra rare. | **Exit 2**: Choose auto-fit OR manual width. |
| `--instant` + `--reveal` | Quantum superposition has not yet been backported to ANSI terminals. You cannot display instantly and scan line-by-line. | **Exit 2**: Pick a rendering speed. |
| `-S` + `-B` + `-Q` + `--blocks` | Trying to merge Sextants, Braille, and Quadrants creates a typographic hydra that Unicode Consortium warned us about. | **Exit 2**: Select exactly one glyph style. |
| `-m` (Manga) + `-s` (Sketch) | Bayer 8x8 halftone screentone and pure minimalist contour lines are fundamentally distinct art schools. | **Exit 2**: Pick Manga or Sketch. |
| `file.png` + `--paste` + `-W` | Feeding a file, the clipboard, and your live webcam all at once causes an identity crisis. | **Exit 2**: Provide exactly one input source. |
| `--loop` + `-o output.png` | Trying to cram a 60-frame animation into a static single-frame PNG is a crime against physics. | **Exit 2**: Use `-o output.gif` or `--save output.gif`. |
| `--transparent` + `-o out.jpg` | JPEG has not supported alpha transparency since 1992. It never will. | **Exit 2**: Use `.png` for transparency. |

---

### 🏛️ The Excommunication of WebP

* **`.webp` is permanently excommunicated from Lumart graphical exports**.
* **Why?** Outside browsers, image viewers and desktop previewers routinely fail to render terminal-rasterized WebP palettes correctly, producing washed-out sludge and broken transparency previews.
* If a user tries to export to `.webp`, Lumart gently redirects them to the **Holy Trinity of Formats**:
  * **`.png`**: For lossless TrueColor and alpha-transparent manga stickers.
  * **`.jpg`**: For universal compatibility and 95% Huffman-optimized photos.
  * **`.gif`**: For multi-frame terminal animations.

---

### 🎨 The Sacred Doctrine of Sticker Transparency (`--transparent`)

* **Color Engines (Mary & Trumble)**:
  * Attempting to export a full-color character on a transparent background outside the terminal creates a ragged, floating contour that looks like a compressed web thumbnail.
  * Color terminal art **needs** its prestigious `#0c0c0c` dark terminal canvas to preserve optical contrast and visual depth.
* **Luris Mono (Manga & Ink Engine)**:
  * The **only** engine anointed to create `--transparent` stickers. With DoG adaptive contours and Bayer/Atkinson halftones, black ink lines on a transparent background produce authentic, studio-grade manga stickers with **>92.9% verified alpha transparency**.
  * Perfect for Telegram, Discord, and WhatsApp sticker packs.

---

### ⚡ Engine & Performance Upgrades

* **Mary Apex 3.5 (C++17 OpenMP + SIMD)**:
  * Evaluates all 31 color bipartitions per cell in under **700 nanoseconds** via OpenMP multi-threading.
  * Oklab perceptual color-difference metric ($\Delta E$) ensures zero muddy brown transitions.
  * Specular highlight preservation ($L > 0.82$) keeps reflections in anime eyes and shiny surfaces sparkling.
* **Trumble Orelx 2.2**:
  * 1-to-1 subpixel Canny edge detection executed *after* downsampling to guarantee crisp 1-subpixel outlines without Lanczos blurring.
  * 32-bit Capcom CPS-2 / SNK Neo-Geo arcade punch color grading (+28% vibrancy).
* **Luris Mono 2.6**:
  * Difference of Gaussians (DoG) line extraction filters out texture noise while locking onto expressive hair and eye contours.
  * Bill Atkinson 1984 error diffusion maintains 25% residual energy to prevent chaotic stochastic noise.
* **Spectra Weep 1.4**:
  * Live webcam streaming at 30–60 FPS with zero buffering lag and 5 real-time shaders (TrueColor, Cyberpunk, Matrix Green Rain, FLIR Thermal, Manga Ink).

---

### 🧹 Ecosytem & Packaging Modernization

* **Cleaned Ghost Towns**:
  * Purged empty, deserted directories `(Resolute/` and `LTS/`.
  * Reaffirmed our eternal love for historical, nostalgic modules (`ascii_art.py`, `pixelterm/`, `engine/`), which remain intact in the codebase.
* **Native Packaging (`build_packages.sh`)**:
  * Auto-detects host distributions and compiles `.deb` (Debian/Ubuntu), `.rpm` (Fedora/RHEL), Arch Linux PKGBUILD, and portable `.tar.gz` archives.
  * Compiler flags updated to `-O3 -march=native` for maximum throughput on modern x86_64 CPUs.
* **PowerShell 7+ Native Installer (`install.ps1`)**:
  * Fully modernized with UTF-8 enforcement and clean PATH resolution for Windows terminal users.

---

## [2.3.0] — 2026-08-15
* Introduced Mary Apex engine with Oklab color space bipartition.
* Added live webcam streaming support (`-W` / `--webcam`) via Spectra Weep.
* Added 8-language localization framework (`en`, `es`, `fr`, `de`, `pt`, `ru`, `ja`, `ko`).
* Implemented desktop file-manager integration (`--install-desktop`).

## [2.2.0] — 2026-07-20
* Introduced Trumble Orelx arcade engine with Canny subpixel outlines.
* Added 3D RGB color swapping (`--swap`).
* Added Atkinson, Floyd-Steinberg, and Bayer dithering algorithms.

## [2.0.0] — 2026-05-10
* Migration from legacy ASCII brightness mapping to Unicode Sextants and Quadrants.
* Multi-core C++ backend introduced for monochrome rendering.

## [1.0.0] — 2026-01-01
* Initial release of Luma terminal ASCII art renderer.
