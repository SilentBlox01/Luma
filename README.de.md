[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Eine hochpräzise Bild-zu-Terminal Rendering-Engine, geschrieben in Python und modernem C/C++.**

Luma ist eine Open-Source Terminal-Rendering-Engine mit einem einzigen Ziel:

> **Maximale visuelle Wiedergabetreue bei minimalem Terminalplatz.**

Im Gegensatz zu herkömmlichen ASCII-Konvertern, die einfach die Bildhelligkeit Zeichen zuordnen, erforscht Luma verschiedene Terminal-Glyphen-Systeme, lineare RGB-Farbmathematik und native C/C++-Computer-Vision-Algorithmen, um so viele visuelle Informationen wie möglich innerhalb einer begrenzten Anzahl von Terminalzellen zu erhalten.

## Funktionen

* Hochpräzises Bildrendering im Terminal
* ASCII, Braille und blockbasiertes Rendering
* **Hybride Dual-Engine-Architektur**:
  * **Lineare RGB-Farb-Engine** (Python / Pillow): Dynamische HDR-Kontrastkurven, Mischung im linearen Farbraum ($C_{\text{linear}} = C_{\text{srgb}}^{2.2}$) und 24-Bit-ANSI-TrueColor.
  * **Hochleistungs-Monochrom- und Manga-Engine** (Natives C++17): Sub-10ms-Ausführung, Konturen-Extraktion durch Differenz von Gauß-Filtern (DoG), Bill-Atkinson-Fehlerdiffusion (1984, MacPaint) und 8x8-Bayer-Raster (*Ami-tone*).
* **Engine-Auswahl (`-E`, `--engine`)**: Dynamisches Umschalten zwischen `color`, `mono`, `bw`, `manga` und `sketch`.
* **Reiner Strichzeichnungsmodus (`-s`, `-E sketch`)**: Rauschfreie Linienextraktion für Anime und Illustrationen.
* **Manga Screentone 2.0 (`-m`, `-E manga`)**: Authentische Comic-Rasterung für Mitteltöne mit reinem Papierweiß und tiefschwarzer Tinte.
* **Atkinson & Halftone-Dithering (`-d` / `--dither`)**: Unterstützt `atkinson`, `floyd`, `bayer` und `none`.
* **2x2 Quadranten-HD-Blöcke (`--blocks`)**: 4 Subpixel pro Zelle mit Unicode-Quadrantenzeichen (`▘▝▀▖▌▞▛▗▚▐▜▄▙▟█`).
* **OS-Style Rendering (`--os-style`)**: Klassische Terminal-Zeichen (Punkte, Buchstaben) für Logos im Neofetch-Stil.
* **Echtzeit-Farbaustausch (`--swap`)**: Dynamischer Austausch von bis zu 5 Farben basierend auf der 3D-Euklidischen Farbdistanz.
* **Keine externen nativen Abhängigkeiten**: Die C++-Engine ist in sich geschlossen mit Public-Domain-Headern (`stb_image.h` und `stb_image_resize2.h`). Kein OpenCV oder libpng erforderlich.
* **Vollständige Python-Fallback-Parität**: Ist kein C++-Compiler vorhanden, schaltet Luma nahtlos auf die reine Python-Implementierung um.
* Konfigurierbare Ausgabebreite und automatische Erkennung von hellem/dunklem Terminal (`-i`, `--invert`)
* Interaktive Update- (`-uu`), Rollback- (`-dg`) und Prüfungs-Suite (`-u`)
* Umfassende System- und Engine-Diagnose (`-v`, `--version`)

## Beispiel

```bash
# Bild mit Braille-Zeichen und Farben konvertieren und Lila in Pink umwandeln
luma image.png -w 45 --braille -c --swap purple pink
```

## Installation

Sie können Luma mit einem einzigen Befehl installieren, direkt aus dem Quellcode ausführen oder es in ein natives Linux-Paket (DEB, RPM oder Arch PKGBUILD) kompilieren.

**Schnellinstallation (Empfohlen):**
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

**Option 1: Direkt aus dem Quellcode ausführen / Lokaler Installer**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
./install.sh
```

**Option 2: Vorkompilierte Pakete herunterladen**
Sie können sofort einsatzbereite `.deb` oder `.rpm` Pakete direkt von der [GitHub Releases](https://github.com/SilentBlox01/Luma/releases) Seite herunterladen.

**Option 3: Native Pakete selbst kompilieren und erstellen**
Luma enthält ein automatisiertes Build-Skript, um das Tool mit PyInstaller in eine eigenständige Binärdatei zu verpacken:
```bash
chmod +x build_packages.sh
./build_packages.sh
```
Nach dem Kompilieren können Sie es über Ihren Paketmanager global installieren:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-*.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-*.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

**Option 4: Manuelle Kompilierung der nativen C++-Engine**
Wenn Sie nur die native C++-Engine ohne vollständige Pakete kompilieren möchten:
```bash
# Standalone-CLI-Binärdatei:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono

# Shared Library (für In-Process-Beschleunigung via ctypes aus Python):
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
```

## Verwendung

Wenn Sie das Paket installiert oder den Installer verwendet haben, können Sie `lumart` oder `luma` von überall ausführen. Andernfalls führen Sie das Python-Skript direkt aus.

> **💡 Profi-Tipp:** Luma funktioniert hervorragend mit transparenten Hintergründen! Die Engine ignoriert transparente Pixel automatisch, wodurch Logos und Charaktere perfekt zur Geltung kommen.

```bash
# Grundlegende Verwendung
python3 lumart.py image.png
```

Ausgabebreite festlegen (in Zeichen):
```bash
python3 lumart.py image.png -w 30
```

Braille-Rendering mit Truecolor aktivieren:
```bash
python3 lumart.py image.png --braille -c
```

Reinen Strichzeichnungsmodus (saubere DoG-Konturen):
```bash
python3 lumart.py image.png -E sketch -w 100
# oder: python3 lumart.py image.png -s -w 100
```

Manga Screentone 2.0 (DoG-Konturen + 8x8 Bayer-Raster):
```bash
python3 lumart.py image.png -E manga -w 120
# oder: python3 lumart.py image.png -m -w 120
```

Monochrom mit Atkinson-Dithering (1984 MacPaint):
```bash
python3 lumart.py image.png -E mono -d atkinson -w 100
# oder klassisches Floyd-Steinberg: python3 lumart.py image.png -E mono -d floyd -w 100
```

2x2 Quadranten-HD-Blöcke:
```bash
python3 lumart.py image.png -E mono --blocks -w 80
```

Reines Monochrom ohne Farben:
```bash
python3 lumart.py image.png -E mono --braille -w 100
```

Klassisches OS-Style-Rendering:
```bash
python3 lumart.py image.png --os-style -c
```

Vollständige System- und Engine-Diagnose anzeigen:
```bash
luma -v
# oder: luma --version
```

## Aktualisierungen und Rollback

Luma bietet explizite Kontrolle über Updates und Rollbacks:

- **Auf Updates prüfen (ohne Änderungen herunterzuladen):**
  ```bash
  luma -u
  # oder: luma --update / luma --check-update
  ```
- **Interaktives Upgrade:**
  ```bash
  luma -uu
  # oder: luma --upgrade
  ```
  *(Erlaubt die Auswahl der gewünschten Version mit Versionshinweisen und automatischem Backup in `~/.config/luma/backup/`)*

- **Interaktives Rollback / Downgrade:**
  ```bash
  luma -dg
  # oder: luma --downgrade / luma --rollback
  ```
  *(Öffnet ein interaktives Terminalmenü zur Auswahl zwischen lokalen Backups und GitHub-Releases)*

  Sie können auch eine Zielversion direkt übergeben:
  ```bash
  luma -dg 2.1.0
  ```

## Deinstallation

Wenn Sie Luma von Ihrem System entfernen möchten:

**Bei Installation über Paketmanager (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**Bei Installation über pip:**
```bash
pip uninstall lumart
```

**Bei manueller Installation:**
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Philosophie

Terminal-Rendering ist eine Form visueller Kompression.

Die Herausforderung besteht nicht einfach darin, ein Bild in Zeichen umzuwandeln. Die Herausforderung besteht darin, die größtmögliche Menge an visuellen Informationen mit der geringsten Anzahl von Terminalzellen darzustellen.

Daher konzentriert sich Luma auf **perzeptuelle Wiedergabetreue** unter Verwendung mathematisch präziser Farbräume (Linear RGB vs sRGB) und dynamischer HDR-Kurven, anstatt lediglich erkennbare ASCII-Kunst zu erzeugen.

## Fehlerbehebung

Haben Sie Probleme mit Schriftarten, Farben oder fehlenden Modulen? Schauen Sie in unseren [Leitfaden zur Fehlerbehebung](TROUBLESHOOTING.md).
