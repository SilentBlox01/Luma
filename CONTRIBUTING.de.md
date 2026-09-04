[English](CONTRIBUTING.md) | [Español](CONTRIBUTING.es.md) | [Português](CONTRIBUTING.pt.md) | [Русский](CONTRIBUTING.ru.md) | [日本語](CONTRIBUTING.ja.md) | [Deutsch](CONTRIBUTING.de.md) | [한국어](CONTRIBUTING.ko.md)

# Zu Luma beitragen

Vielen Dank für dein Interesse an der Weiterentwicklung von Luma! Dieses Projekt erweitert die grafischen Grenzen des Terminals, und alle Beiträge sind herzlich willkommen.

## 🐛 Fehler melden oder Funktionen vorschlagen

Wenn du auf einen Fehler stößt oder eine großartige Idee hast (wie einen neuen Rendering-Algorithmus, Dithering-Muster oder Animationsunterstützung), erstelle bitte ein **Issue** auf GitHub. Bitte gib Folgendes an:
- Dein Betriebssystem und Terminal-Emulator (z.B. Fedora mit Alacritty, Ubuntu mit Kitty, Windows Terminal).
- Den genauen Befehl und die verwendeten Argumente.
- Wenn möglich, ein Beispiel der generierten ASCII-Kunst oder des Originalbildes.

## 🛠️ Code beisteuern

1. **Forke das Repository** auf GitHub.
2. **Erstelle einen neuen Branch** für deine Funktion oder Korrektur (`git checkout -b feature/neue-funktion`).
3. **Schreibe und teste deinen Code**. Die Engine-Logik befindet sich in `lumart.py`.
4. **Commite deine Änderungen** mit einer aussagekräftigen Nachricht (`git commit -m 'feat: neuer Algorithmus XYZ'`).
5. **Pushe deinen Branch** (`git push origin feature/neue-funktion`).
6. **Erstelle einen Pull Request**.

### Projektarchitektur
- `lumart.py`: Der gesamte Kern der Engine: wahrnehmungsbezogene Linear-RGB-Farbverarbeitung, Bayer-Matrix-Dithering, Braille- und Halbblock-Rendering sowie die CLI mit mehrsprachiger Unterstützung.
- `install.sh`: Universeller Plug-and-Play-Installer, kompatibel mit Fedora, Debian/Ubuntu, Arch Linux, openSUSE und macOS.
- `build_packages.sh`: Automatisiertes Skript zum Erstellen von Standalone-Binärdateien mit `PyInstaller` und Paketen für `.deb`, `.rpm` und `PKGBUILD`.
- `pyproject.toml`: Moderne Paketierungsdefinition zur Unterstützung von `pipx install .` und `pip install --user .`.

### Richtlinien
- **Keine schweren Abhängigkeiten**: Luma bleibt leichtgewichtig und Plug-and-Play. Verwende nur Pillow (`PIL`) und die Python-Standardbibliothek.
- **Terminal-Ästhetik**: Jeder Modus muss höchste visuelle Wiedergabetreue bieten.
- **Mehrsprachigkeit**: Wenn du neue CLI-Optionen oder Meldungen hinzufügst, aktualisiere alle 7 Sprachen in `TRANSLATIONS` (`en`, `es`, `pt`, `ru`, `ja`, `de`, `ko`).

Viel Spaß beim Experimentieren mit Farben im Terminal! 🎨
