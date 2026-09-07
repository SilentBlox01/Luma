[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.3.0
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.3.0

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Language: Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![C++: 17 Multi-Core](https://img.shields.io/badge/C%2B%2B-17%20OpenMP%20SIMD-orange.svg)](https://isocpp.org/)
[![Platform: Linux / macOS / BSD](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20BSD-lightgrey.svg)](https://github.com/SilentBlox01/Luma)
[![8 Unterstützte Sprachen](https://img.shields.io/badge/Languages-8%20Locales-purple.svg)](#unterstützte-sprachen)

**Lumart** ist eine hochentwickelte visuelle Engine für moderne Terminalemulatoren, entwickelt nach einem zentralen Leitsatz:

> **Maximale visuelle Dichte und ästhetische Wirkung auf minimalem Raum.**

Im Gegensatz zu herkömmlichen ASCII-Konvertern, die lediglich die Helligkeit von Pixeln auf einfache Textzeichen abbilden, vereint Lumart **vier spezialisierte Computer-Vision- und Subpixel-Rendering-Engines**, programmiert in nativem Multi-Core C++17 (OpenMP) und optimiertem Python. Es verwandelt digitale Fotografien, Anime-Illustrationen, Arcade-Sprites und Live-Webcam-Streams in beeindruckende Kunstwerke direkt auf der Terminalkonsole.

---

## Inhaltsverzeichnis
1. [Die Vier Flaggschiff-Engines](#die-vier-flaggschiff-engines)
   - [Mary Apex 3.5](#1-mary-apex-35-fotorealistisch-vektoriell)
   - [Trumble Orelx 2.2](#2-trumble-orelx-22-retro-arcade--anime-cel-shading)
   - [Luris Mono 2.6](#3-luris-mono-26-manga-screentone--monochrom)
   - [Spectra Weep 1.4](#4-spectra-weep-14-live-webcam-streaming)
2. [Vergleichsmatrix der Modelle](#vergleichsmatrix-der-modelle)
3. [Grafikexport und Sticker-Richtlinie](#grafikexport-und-sticker-richtlinie)
4. [Unterstützte Sprachen (8 Sprachen)](#unterstützte-sprachen)
5. [Schnellinstallation & Pakete](#installation)
6. [Vollständige Befehlsreferenz (CLI)](#vollständige-befehlsreferenz)
7. [Praxisbeispiele und Kochbuch](#praxisbeispiele)
8. [Update- und Rollback-System](#update--und-rollback-system)
9. [System- und Desktop-Integration](#system--und-desktop-integration)
10. [Mathematik und Interne Architektur](#mathematik-und-interne-architektur)
11. [Fehlerbehebung](#fehlerbehebung)
12. [Lizenz](#lizenz)

---

## Die Vier Flaggschiff-Engines

```
                  ┌──────────────────────────────────────────────┐
                  │                 LUMART CLI                   │
                  └──────┬────────────┬────────────┬─────────────┘
                         │            │            │             │
        ┌────────────────┘            │            │             └────────────────┐
        ▼                             ▼            ▼                              ▼
  ┌──────────────┐             ┌──────────────┐  ┌──────────────┐          ┌──────────────┐
  │  MARY APEX   │             │TRUMBLE ORELX │  │  LURIS MONO  │          │ SPECTRA WEEP │
  │    v3.5      │             │    v2.2      │  │    v2.6      │          │     v1.4     │
  ├──────────────┤             ├──────────────┤  ├──────────────┤          ├──────────────┤
  │• C++17 OpenMP│             │• Subpixel Ink│  │• C++17 Native│          │• Live Webcam │
  │• Oklab 31-Min│             │• Capcom CPS-2│  │• DoG Lineart │          │• 30-60 FPS   │
  │• Sextants 2x3│             │• 32-bit Punch│  │• Ami-tone 8x8│          │• 5 Shaders   │
  │• Specular Fit│             │• Quad-Blocks │  │• Stickers PNG│          │• Zero-Latency│
  └──────────────┘             └──────────────┘  └──────────────┘          └──────────────┘
```

### 1. Mary Apex 3.5 (Fotorealistisch Vektoriell)
* **Zielsetzung**: Glatte Mikro-Farbverläufe, anspruchsvolle Beleuchtung und lebensechte Porträts.
* **C++17 Multi-Core-Kern**: Beschleunigt mit OpenMP und SIMD-Vektorisierung (`libmary.so` und Binary `luma-mary`).
* **Exakte Globale Diskrete Oklab-Bipartition (31 Kombinationen pro Zelle)**: Vollständige Überwindung lokaler Minima-Fallen. Überprüft alle 31 Farbteilungen pro Zelle in unter 700 Nanosekunden und garantiert das absolute globale Minimum des wahrnehmbaren Farbunterschieds ($\Delta E$).
* **Schneller Geführter Filter $O(1)$ mit Glanz-Verstärkung ($L > 0.82$)**: Hebt Glanzlichter in Augen und spiegelnden Oberflächen hervor, während sanfte Hauttöne erhalten bleiben.
* **Standardmäßige Unicode 13.0 Sextanten 2x3**: 6 Subpixel pro Terminalzeichen in soliden Blöcken (`🬀`-`🬻`, `█`, `▌`, `▐`). Unterstützt außerdem zweifarbiges Braille 2x4 (`-B`), Quadranten 2x2 (`-Q`) und Halbblöcke (`--blocks`).
* **Strenge Alpha-Isolierung**: Transparente Bereiche verfälschen keine Kantenfarben und verhindern dunkle Ränder.
* **Export auf Terminal-Leinwand**: PNG- und JPG-Exporte werden auf einem eleganten dunklen Terminal-Hintergrund (`#0c0c0c`) gerendert, um den authentischen Charakter hochwertiger Konsolenkunst zu wahren.

### 2. Trumble Orelx 2.2 (Retro-Arcade & Anime Cel-Shading)
* **Zielsetzung**: Anime-Zeichnungen, Comic-Illustrationen, Gaming-Sprites und plakative Pop-Art.
* **1-zu-1 Subpixel-Inking vor Skalierung**: Die Reskalierung erfolgt *vor* dem bilateralen Filter und der Canny-Kantenerkennung. Dadurch behalten schwarze Tuschelinien exakt 1 Subpixel Stärke, ohne durch Lanczos-Interpolation verwischt zu werden.
* **32-Bit Capcom CPS-2 / SNK Neo-Geo Arcade-Farbprofil**: Lebendige Farbdynamik (+28% Farbsättigung, +15% selektiver Kontrast) im Stil legendärer 90er-Jahre Arcade-Klassiker.
* **Adaptive Quadrantenform**: Herabsetzung der Formstrafe auf 30, wodurch diagonale Zeichen (`▞`, `▚`, `▘`, `▝`) geschmeidigen Konturen von Haaren und Kleidung präzise folgen.

### 3. Luris Mono 2.6 (Manga Screentone & Monochrom C++17)
* **Zielsetzung**: Japanischer Manga-Stil, Tuschezeichnungen, feine Federstriche und transparente Sticker.
* **DoG-Kantenerkennung (Difference of Gaussians)**: Rauschfreie, saubere Linienführung mit automatischer Radius-Anpassung.
* **Manga Screentone 2.0 (*Ami-tone*)**: Authentische Druckraster-Emulation via 8x8 Bayer-Matrizen mit tiefschwarzer Tinte und reinem Papierweiß.
* **Atkinson-Fehlerdiffusion (MacPaint 1984)**: Der renommierte Algorithmus von Bill Atkinson, der 25% Restenergie speichert und scharfe Halbtöne ohne störendes Bildrauschen liefert.
* **Exklusiver Transparenter Sticker-Export (`--transparent`)**: Luris Mono ist die **einzige Engine, die freigestellte transparente PNG-Sticker erzeugt**, perfekt für Messenger wie Discord, Telegram oder WhatsApp.

### 4. Spectra Weep 1.4 (Live-Webcam im Terminal)
* **Zielsetzung**: Echtzeit-Videostreaming mit 30 bis 60 FPS direkt in der Terminal-Konsole (`lumart --webcam` oder `lumart -W`).
* **Null Latenz**: Optimierte OpenCV/V4L2-Erfassung synchronisiert mit der Bildwiederholrate des Terminals.
* **5 Live-Shader-Filter**: Normal TrueColor, Weep Cyberpunk, Matrix Green Rain, Thermal FLIR und Manga Ink.

---

## Grafikexport und Sticker-Richtlinie

Lumart verfügt über einen hochauflösenden Text-zu-Bild-Konverter (`-o bild.png` oder `-o bild.jpg`) mit einer Studio-Standardbreite von **160 Spalten**.

### 1. Dauerhafte Deaktivierung des WebP-Formats
* **Der Export in das `.webp`-Format wurde dauerhaft deaktiviert**.
* Bei Angabe einer `.webp`-Datei weist Lumart die Aktion sauber ab und empfiehlt `.png` oder `.jpg`.
* Offiziell unterstützte Formate:
  * **`.png`**: Verlustfreie Speicherung, optimierte Kompression und volle Alpha-Transparenz.
  * **`.jpg` / `.jpeg`**: Maximale Kompatibilität, 95% Qualität und Huffman-Optimierung.

### 2. Transparente Sticker exklusiv für Luris Mono
* **Warum erzeugen Farbmodelle keine transparenten Sticker?**
  Wird eine farbige Figur mit 160 Spalten auf transparentem Hintergrund ohne Terminalrahmen betrachtet, wirkt sie in Bildbetrachtern oft wie eine unschärfere oder komprimierte Bilddatei. Auf einer **edlen dunklen Terminal-Leinwand (`#0c0c0c`)** hingegen entfaltet sie ihre volle Ästhetik als detailreiches Terminal-Kunstwerk.
* **Manga-Sticker in Schwarz-Weiß (Luris Mono)**:
  Die Option `--transparent` ist **ausschließlich für Luris Mono** reserviert. Die Druckraster und DoG-Linien erzeugen authentische Manga-Ausschnitte mit über 95% verifizierter Transparenz.
* Wird `--transparent` bei Mary oder Trumble angegeben, informiert Lumart den Nutzer und exportiert das Werk auf der Terminal-Leinwand.

---

## Unterstützte Sprachen

Lumart bietet vollständige Lokalisierung in **8 Sprachen**:

| Code | Sprache | Automatische Erkennung | Manuelle Auswahl |
| :---: | :--- | :--- | :--- |
| `de` | Deutsch | `$LANG=de_*` | `lumart --lang de` |
| `en` | English | `$LANG=en_*` (Standard) | `lumart --lang en` |
| `es` | Español | `$LANG=es_*` | `lumart --lang es` |
| `pt` | Português | `$LANG=pt_*` | `lumart --lang pt` |
| `fr` | Français | `$LANG=fr_*` | `lumart --lang fr` |
| `ru` | Русский | `$LANG=ru_*` | `lumart --lang ru` |
| `ja` | 日本語 | `$LANG=ja_*` | `lumart --lang ja` |
| `ko` | 한국어 | `$LANG=ko_*` | `lumart --lang ko` |

---

## Installation

### Einzeilen-Schnellinstallation (Empfohlen)
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### Installation aus dem Quellcode
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
chmod +x install.sh
./install.sh
```

---

## Vollständige Befehlsreferenz

```text
Aufruf: lumart [OPTIONEN] <bildpfad_oder_url>
```

| Option | Parameter | Beschreibung |
| :--- | :--- | :--- |
| `-m`, `--manga` | — | Manga Screentone 2.0 (Bayer 8x8 Raster + DoG-Linien). |
| `-s`, `--sketch`| — | Sauberer Federzeichnungs-Modus. |
| `-B`, `--braille` | — | Unicode 2x4 Braille-Zeichen (8 Subpixel pro Zelle). |
| `-Q`, `--quadrants`| — | Unicode 2x2 Quadranten-Zeichen (4 Subpixel pro Zelle). |
| `--blocks` | — | Optimierte Terminal-Blockzeichen (`▀`). |
| `-w`, `--width` | `<int>` | Ausgabebreite in Spalten (Standard: automatische Erkennung). |
| `-i`, `--invert`| — | Invertiert die Helligkeit (für helle Terminal-Themes; automatische Erkennung in `-m`). |
| `--boost`, `--vibrant` | — | Aktiviert erhöhte Farbsättigung, Kontrast und Retinex-Verarbeitung für lebhafte Arcade-Ausgabe. |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Dithering-Algorithmus für Halbtöne. |
| `--swap` | `<farbe1> <farbe2>` | Dynamischer Farbaustausch im 3D-RGB-Farbraum. |
| `-o`, `--output` | `<datei.png / .jpg>` | Exportiert das Terminal-Kunstwerk als Bilddatei. |
| `--transparent` | — | **Nur Luris Mono**: erzeugt freigestellte transparente Sticker. |
| `--paste` | — | Rendert das Bild direkt aus der Zwischenablage. |
| `-W`, `--webcam`| `[id]` | Live-Webcam-Streaming in der Konsole (30-60 FPS). |
| `--lang` | `<code>` | Legt die Sprache fest (`de`, `en`, `es`, etc.). |
| `-H`, `--history` | `[N]` | Zeigt die letzten N Befehle aus dem Verlauf. |
| `-R`, `--replay` | `[N]` | Wiederholt den N-ten Befehl aus dem Verlauf. |
| `--clear-history`| — | Löscht den gespeicherten Befehlsverlauf. |
| `--install-desktop` | — | Fügt "Mit Lumart öffnen" zum Linux-Kontextmenü hinzu. |
| `-v`, `--version` | — | Zeigt System-, Terminal- und Engine-Diagnosen an. |
| `-u`, `--check-update`| — | Sucht nach neuen Versionen auf GitHub. |
| `-uu`, `--upgrade` | — | Interaktiver Upgrade-Assistent. |
| `-dg`, `--downgrade` | `[ver]` | Interaktives Rollback auf frühere Versionen. |

---

## Praxisbeispiele

### 1. High-Definition Terminal-Kunst (Standard ohne Flags)
```bash
lumart foto.jpg -w 90
```

### 2. Anime-Illustration mit Blöcken
```bash
lumart anime.png --blocks -w 85
```

### 3. Freigestellter transparenter Manga-Sticker (Luris Mono)
```bash
lumart manga.png -m --transparent -o sticker.png
```

### 4. Webcam-Liveübertragung in der Konsole
```bash
lumart -W
```

### 5. Direktes Rendern aus der Zwischenablage
```bash
lumart --paste
```

---

## Lizenz

Lumart steht unter der GNU Affero General Public License v3.0 (**AGPL-3.0**). Siehe die Datei `LICENSE` für Details.
