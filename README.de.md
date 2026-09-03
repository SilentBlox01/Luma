[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Eine hochpräzise Bild-zu-Terminal Rendering-Engine, geschrieben in Python.**

Luma ist eine Open-Source Terminal-Rendering-Engine mit einem einzigen Ziel:

> **Maximale visuelle Wiedergabetreue bei minimalem Terminalplatz.**

Im Gegensatz zu herkömmlichen ASCII-Konvertern, die einfach die Bildhelligkeit Zeichen zuordnen, erforscht Luma verschiedene Terminal-Glyphen-Systeme, lineare RGB-Farbmathematik und Rendering-Techniken, um so viele visuelle Informationen wie möglich innerhalb einer begrenzten Anzahl von Terminalzellen zu erhalten.

## Funktionen

* Hochpräzises Bildrendering im Terminal
* ASCII, Braille und blockbasiertes Rendering
* **OS-Style Rendering (`--os-style`)**: Klassische Terminal-Zeichen (Punkte, Buchstaben) für Logos im Neofetch-Stil.
* **Echtzeit-Farbaustausch (`--swap`)**: Dynamischer Austausch von bis zu 5 Farben basierend auf der 3D-Euklidischen Farbdistanz.
* **Epische Farb-Engine (Standard)**: Bildet den Durchschnitt der Farben im linearen RGB-Raum, um unsaubere Ergebnisse zu vermeiden, während dynamischer Kontrast und Sättigung (HDR) angewendet werden.
* Konfigurierbare Ausgabebreite
* Truecolor-Terminal-Unterstützung (24-Bit ANSI)
* Konzipiert für extrem kleine Ausgabegrößen
* Python-basiert und hochgradig erweiterbar

## Beispiel

```bash
# Bild mit Braille-Zeichen und Farben konvertieren und Lila in Pink umwandeln
luma image.png -w 45 --braille -c --swap purple pink
```

## Installation

Sie können Luma direkt aus dem Quellcode ausführen oder es in ein natives Linux-Paket (DEB, RPM oder Arch PKGBUILD) kompilieren.

**Option 1: Vorkompilierte Pakete herunterladen (Empfohlen)**
Sie können sofort einsatzbereite `.deb` oder `.rpm` Pakete direkt von der [GitHub Releases](https://github.com/SilentBlox01/Luma/releases) Seite herunterladen.

**Option 2: Direkt aus dem Quellcode ausführen**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
# Stellen Sie sicher, dass Pillow installiert ist
pip install -r requirements.txt
python3 lumart.py --help
```

**Option 3: Native Pakete selbst kompilieren und erstellen**
Luma enthält ein automatisiertes Build-Skript, um das Tool mit PyInstaller in eine eigenständige Binärdatei zu verpacken.
```bash
chmod +x build_packages.sh
./build_packages.sh
```
Nach dem Kompilieren können Sie es über Ihren Paketmanager global installieren:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-2.0.0.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-2.0.0.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

## Verwendung

Wenn Sie das Paket installiert haben, können Sie `lumart` oder `luma` von überall aus ausführen. Andernfalls führen Sie das Python-Skript direkt aus.

```bash
# Grundlegende Verwendung
python3 lumart.py image.png
```

Ausgabebreite festlegen (in Zeichen):
```bash
python3 lumart.py image.png -w 30
```

Hochauflösendes Braille-Rendering mit Truecolor aktivieren:
```bash
python3 lumart.py image.png --braille -c
```

Retro-OS-Style Rendering erzwingen (nützlich für OS-Logos):
```bash
python3 lumart.py image.png --os-style -c
```

## Deinstallation

Wenn Sie Luma von Ihrem System entfernen möchten, hängt der Befehl davon ab, wie Sie es installiert haben:

**Bei Installation über Paketmanager (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**Bei Installation über pip:**
```bash
pip uninstall lumart
```

**Bei manueller Installation:**
Sie können das bereitgestellte Deinstallationsskript ausführen:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Philosophie

Terminal-Rendering ist eine Form der visuellen Kompression.

Die Herausforderung besteht nicht nur darin, ein Bild in Zeichen umzuwandeln. Die Herausforderung besteht darin, die größtmögliche visuelle Information mit der geringsten Anzahl von Terminalzellen darzustellen.

Daher konzentriert sich Luma auf **wahrnehmungsbezogene Wiedergabetreue** und verwendet mathematisch präzise Farbräume (Lineares RGB vs. sRGB) und dynamische HDR-Kurven, anstatt nur erkennbare ASCII-Kunst zu erzeugen.

## Roadmap

* [x] Initiale Bild-zu-Terminal-Engine
* [x] Braille-Rendering
* [x] Blockbasiertes Rendering
* [x] Verbessertes Wahrnehmungs-Rendering (Lineare RGB-Engine)
* [x] Kontrast- und Luminanzverarbeitung (Epische Engine)
* [x] Echtzeit-Farbzuordnung und Schwellenwerte
* [ ] Erweitertes Dithering
* [ ] Automatische Glyphenauswahl
* [ ] Bildähnlichkeits-Benchmarks
* [ ] Rendering-Optimierung
* [ ] Durch maschinelles Lernen gestütztes Rendering
* [ ] Unterstützung für Video- und GIF-Rendering
* [ ] Erweiterung der Terminal-Glyphen-Systeme

## Mitwirken

Luma ist ein Open-Source-Projekt und Beiträge sind willkommen.

Wenn Sie eine Idee für einen Rendering-Algorithmus, eine Optimierung, ein Glyphensystem, einen Benchmark oder eine Verbesserung haben, können Sie gerne ein Issue eröffnen oder einen Pull Request senden. (Siehe `CONTRIBUTING.md` für Details).

## Lizenz

Luma wird unter der GNU Affero General Public License v3.0 (AGPL-3.0) veröffentlicht. Weitere Details finden Sie in der `LICENSE` Datei.
