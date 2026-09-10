[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.4.0 (Apex Horizon)
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.4.0

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Language: Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![C++: 17 Multi-Core](https://img.shields.io/badge/C%2B%2B-17%20OpenMP%20SIMD-orange.svg)](https://isocpp.org/)
[![Platform: Linux / macOS / BSD](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20BSD-lightgrey.svg)](https://github.com/SilentBlox01/Luma)
[![8 Langues Supportées](https://img.shields.io/badge/Langues-8%20Locales-purple.svg)](#langues-supportées)

**Lumart** est une suite visuelle d'ingénierie avancée pour terminaux modernes, conçue selon un principe directeur fondamental :

> **Densité visuelle maximale et impact esthétique dans un espace terminal minimal.**

Contrairement aux convertisseurs ASCII basiques qui se contentent d'associer la luminosité des pixels à des caractères alphanumériques simples, Lumart réunit **quatre moteurs spécialisés de vision par ordinateur et de rendu sous-pixel** développés en C++17 natif multithread (OpenMP) et Python optimisé. Il transforme photographies, illustrations anime, sprites arcade et flux webcam en direct en véritables chefs-d'œuvre graphiques au sein de votre émulateur de terminal.

---

## Table des Matières
1. [Les Quatre Moteurs Phares](#les-quatre-moteurs-phares)
   - [Mary Apex 3.5](#1-mary-apex-35-photoréaliste-vectoriel)
   - [Trumble Orelx 2.2](#2-trumble-orelx-22-rétro-arcade--anime-cel-shading)
   - [Luris Mono 2.6](#3-luris-mono-26-manga-screentone--monochrome)
   - [Spectra Weep 1.4](#4-spectra-weep-14-webcam-en-direct)
2. [Matrice Comparative des Moteurs](#matrice-comparative-des-moteurs)
3. [Galerie Visuelle et Face-à-face](#galerie-visuelle-et-face-à-face)
4. [Exportation Graphique, Animations et Politique de Stickers](#exportation-graphique-animations-et-politique-de-stickers)
5. [Langues Supportées (8 Langues)](#langues-supportées)
6. [Installation Rapide et Paquets](#installation)
7. [Référence Complète des Commandes (CLI)](#référence-complète-des-commandes)
8. [Exemples Pratiques et Guide d'Utilisation](#exemples-pratiques)
9. [Secrets d'Ingénierie, Astuces de Pro et Philosophie du Terminal](#secrets-dingénierie-astuces-de-pro-et-philosophie-du-terminal)
10. [Système de Mises à Jour et Restauration](#système-de-mises-à-jour-et-restauration)
11. [Intégration au Système et au Bureau](#intégration-au-système-et-au-bureau)
12. [Architecture et Ingénierie Interne](#architecture-et-ingénierie-interne)
13. [Dépannage et Compatibilité](#dépannage)
14. [Licence](#licence)

---

## Les Quatre Moteurs Phares

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

### 1. Mary Apex 3.5 (Photoréaliste Vectoriel)
* **Objectif** : Micro-dégradés continus, photographies complexes, éclairages d'ambiance et portraits fidèles.
* **Cœur C++17 Multi-Cœur** : Accéléré par OpenMP et instructions SIMD (`libmary.so` et binaire `luma-mary`).
* **Bipartition Oklab Globale Exacte (31 combinaisons évaluées par cellule)** : Élimine les pièges de minima locaux des algorithmes heuristiques. Évalue exhaustivement toutes les bipartitions de couleur par cellule en moins de 700 nanosecondes, garantissant le minimum absolu d'erreur perceptuelle ($\Delta E$).
* **Filtre Guidé Rapide $O(1)$ avec Rehaussement Spéculaire ($L > 0.82$)** : Accentue les reflets brillants dans les yeux, les métaux et l'eau tout en préservant la douceur des teintes de peau.
* **Sextants Unicode 2x3 par Défaut** : 6 sous-pixels par caractère de terminal via la table Unicode 13.0 (`🬀`-`🬻`, `█`, `▌`, `▐`). Prend également en charge le Braille 2x4 bicolore (`-B`), les Quadrants 2x2 (`-Q`) et les Demi-Blocs (`--blocks`).
* **Isolation Alpha Stricte** : Les zones transparentes ne contaminent pas les bordures du sujet, éliminant les halos sombres.
* **Exportation avec Toile de Terminal** : Les rendus sauvegardés en `.png` ou `.jpg` sont générés sur un fond sombre de terminal (`#0c0c0c`), préservant l'esthétique d'art de terminal sans paraître être une image compressée.

### 2. Trumble Orelx 2.2 (Rétro-Arcade & Anime Cel-Shading)
* **Objectif** : Dessins animés japonais, sprites de jeux vidéo, bandes dessinées et pop-art rétro.
* **Encrage 1-pour-1 à Résolution Sous-Pixel** : Le redimensionnement intervient *avant* le filtrage bilatéral et la détection de contours Canny. Les traits d'encre noire conservent exactement 1 sous-pixel d'épaisseur, évitant que la réduction Lanczos n'estompe ou ne mélange les contours.
* **Palette Arcade Capcom CPS-2 / SNK Neo-Geo 32-bit** : Dynamique de couleur punchy (+28% de vivacité, +15% de contraste sélectif) inspirée des bornes d'arcade mythiques des années 90.
* **Pénalité de Forme Adaptative** : Plafond abaissé à 30 pour les quadrants, permettant aux glyphes diagonaux (`▞`, `▚`, `▘`, `▝`) d'épouser naturellement les courbes des yeux, des cheveux et des vêtements.

### 3. Luris Mono 2.6 (Manga Screentone & Monochrome C++17)
* **Objectif** : Mangas japonais traditionnels, encre de Chine, dessins à la plume et stickers transparents.
* **Extraction de Lignes DoG (Différence de Gaussiennes)** : Lignes nettes exemptes de bruit de texture, adaptant les rayons de convolution à la largeur du terminal.
* **Manga Screentone 2.0 (*Ami-tone*)** : Trame pointillée mécanique inspirée de l'imprimerie nippone via des matrices Bayer 8x8, produisant des demi-teintes parfaites avec des blancs de papier purs et un noir d'encre profond.
* **Diffusion d'Erreur Atkinson (MacPaint 1984)** : L'algorithme légendaire de Bill Atkinson qui retient 25% d'énergie résiduelle pour générer des textures nettes sans grains parasites.
* **Exclusivité des Stickers Transparents (`--transparent`)** : Luris Mono est le **seul moteur habilité à créer des stickers découpés avec arrière-plan transparent en `.png`**, idéal pour Discord, Telegram ou WhatsApp.

### 4. Spectra Weep 1.4 (Webcam en Direct dans le Terminal)
* **Objectif** : Diffusion vidéo interactive en temps réel à 30-60 FPS directement dans la console (`lumart --webcam` ou `lumart -W`).
* **Latence Zéro** : Capture optimisée via OpenCV/V4L2 avec synchronisation directe au taux de rafraîchissement du terminal.
* **5 Filtres Shaders en Temps Réel** : Normal TrueColor, Weep Cyberpunk, Matrix Green Rain, Thermal FLIR Infrarouge et Manga Ink.

---

## Matrice Comparative des Moteurs

| Fonctionnalité | Mary Apex 3.5 | Trumble Orelx 2.2 | Luris Mono 2.6 | Spectra Weep 1.4 |
| :--- | :--- | :--- | :--- | :--- |
| **Style Visuel** | Photoréaliste Vectoriel | Rétro-Arcade / Cel-Shading | Manga Japonais / Encre | Vidéo Direct / Webcam |
| **Langage de Base** | C++17 OpenMP + SIMD | Python + OpenCV Optimisé | C++17 Natif | Python + OpenCV V4L2 |
| **Espace Couleur** | Oklab Perceptuel ($\Delta E$) | 32-bit Capcom CPS-2 | Monochrome / Ami-tone | TrueColor / Shaders RGB |
| **Mode par Défaut** | **Sextants 2x3 (`-S`)** | **Quadrants 2x2 (`--blocks`)**| **Manga 2.0 (`-m`)** | **Flux 30-60 FPS** |
| **Densité Sous-Pixel**| Jusqu'à 6 sous-pixels/cellule| Jusqu'à 4 sous-pixels/cellule| Jusqu'à 4 sous-pixels/cellule| Dynamique |
| **Encrage des Lignes**| Anti-aliasing Doux | **Canny 1-pour-1 Sous-Pixel** | **Lignes DoG Adaptatives** | Optionnel (Shader Manga) |
| **Exportation** | Toile Terminal (`.png`, `.jpg`)| Toile Terminal (`.png`, `.jpg`)| **Stickers PNG (`--transparent`)**| Capture instantanée |
| **Commande Rapide** | `-E mary -S` | `-E trumble --blocks` | `-E luris -m` | `-W` ou `--webcam` |

---

## Galerie Visuelle et Démonstrations de Résultats

### 1. Duel des Moteurs : Mary Apex 3.5 vs Trumble Orelx 2.2
![Démonstration des Moteurs Lumart](assets/engine_showdown.png)

### 2. Comparatif Côte à Côte : Couleur Photoréaliste vs Stickers Manga Transparents

| Mary Apex 3.5 (TrueColor Photoréaliste) | Luris Mono 2.6 (Stickers Manga Transparents) |
| :---: | :---: |
| ![Cinderella Mary](assets/cinderella_mary_apex.png)<br><sub>`lumart cinderella.jpg` *(Mary Sextants par défaut)*</sub> | ![Cinderella Manga Sticker](assets/cinderella_manga_sticker.png)<br><sub>`lumart cinderella.jpg -m --transparent -o sticker.png`</sub> |
| ![Hanako Mary Boosted](assets/hanako_boosted.png)<br><sub>`lumart hanako.png --boost` *(Punch Arcade Retinex)*</sub> | ![Hanako Manga Sticker](assets/hanako_manga_sticker.png)<br><sub>`lumart hanako.png -m --transparent -o sticker.png`</sub> |
| ![Gothic Nun Mary](assets/gothic_nun_mary.png)<br><sub>`lumart gothic_nun.png`</sub> | ![Gothic Nun Manga Sticker](assets/gothic_nun_manga_sticker.png)<br><sub>`lumart gothic_nun.png -m --transparent -o sticker.png`</sub> |
| ![Slime Mary](assets/slime_mary.png)<br><sub>`lumart slime.png`</sub> | ![Slime Manga Sticker](assets/slime_manga_sticker.png)<br><sub>`lumart slime.png -m --transparent -o sticker.png`</sub> |

### 3. Densités de Glyphes Sous-Pixels

| Sextants 2x3 (`-S` / Défaut) | Braille 2x4 (`-B`) | Quadrants 2x2 (`-Q`) |
| :---: | :---: | :---: |
| ![Sextants 2x3](assets/texture_sextants.png)<br><sub>6 sous-pixels/cellule (Dégradés continus)</sub> | ![Braille 2x4](assets/texture_braille.png)<br><sub>8 sous-pixels/cellule (Points fins & portraits)</sub> | ![Quadrants 2x2](assets/texture_quadrants.png)<br><sub>4 sous-pixels/cellule (Pixel-art & arcade)</sub> |

---

## Exportation Graphique, Animations et Politique de Stickers

Lumart intègre un rasteriseur haute définition (`-o image.png`, `-o image.jpg` ou `-o anim.gif`) avec une largeur standard de studio de **160 colonnes**.

### 1. Mode Animation et Exportation GIF Animé (`--loop`)
![Démonstration Animée dans le Terminal](assets/animated_demo.gif)

Lumart v2.4.0 introduit la prise en charge native des fichiers d'animation (GIFs et APNGs) :
* **Lecture Fluide dans le Terminal** : `lumart animation.gif --loop` pré-calcule et met en cache chaque image en séquences ANSI pour une lecture fluide à 60 FPS dans votre terminal.
* **Compilation en GIF Animé** : `lumart animation.gif --loop -o rendu.gif` (ou `--save rendu.gif`) rasterise chaque image avec une précision sous-pixel et produit un GIF animé complet.

### 2. Désactivation Définitive du Format WebP
* **Le format `.webp` a été désactivé de manière permanente pour l'exportation graphique**.
* Toute tentative de spécifier une extension `.webp` entraîne un refus propre avec un message invitant à utiliser `.png`, `.jpg` ou `.gif`.
* Formats officiellement supportés :
  * **`.png`** : Qualité sans perte, compression optimisée et prise en charge du canal alpha transparent.
  * **`.jpg` / `.jpeg`** : Compatibilité universelle, qualité 95% et tables de Huffman optimisées.
  * **`.gif`** : Animations multi-images pour web ou terminal.

### 3. Exclusivité des Stickers Transparents pour Luris Mono
* **Pourquoi les moteurs couleur n'exportent-ils pas en sticker transparent ?**
  Découper un personnage couleur à 160 colonnes sur fond transparent donne souvent l'illusion d'une image dégradée ou basse résolution dans les visionneuses classiques. Exportée sur une **toile sombre de terminal (`#0c0c0c`)**, l'œuvre prend tout son sens en tant que pièce d'art de terminal haute fidélité.
* **Stickers Manga en Noir et Blanc (Luris Mono)** :
  L'option `--transparent` est **réservée exclusivement à Luris Mono** (`-m`, `-s`, `-E luris`). Les trames de mangá et les lignes DoG produisent d'authentiques stickers découpés avec une transparence alpha supérieure à 95%.
* En cas d'utilisation de `--transparent` avec Mary ou Trumble, Lumart affiche une notification et sauvegarde l'image avec son fond de terminal.

---

## Langues Supportées

Lumart intègre une localisation complète dans **8 langues** :

| Code | Langue | Autodétection | Sélection Manuelle |
| :---: | :--- | :--- | :--- |
| `fr` | Français | Automatique via `$LANG=fr_*` | `lumart --lang fr` |
| `en` | English | Automatique via `$LANG=en_*` (Défaut) | `lumart --lang en` |
| `es` | Español | Automatique via `$LANG=es_*` | `lumart --lang es` |
| `pt` | Português | Automatique via `$LANG=pt_*` | `lumart --lang pt` |
| `ru` | Русский | Automatique via `$LANG=ru_*` | `lumart --lang ru` |
| `ja` | 日本語 | Automatique via `$LANG=ja_*` | `lumart --lang ja` |
| `de` | Deutsch | Automatique via `$LANG=de_*` | `lumart --lang de` |
| `ko` | 한국어 | Automatique via `$LANG=ko_*` | `lumart --lang ko` |

---

## Installation

### Méthode 1 : Installateur Automatique en Une Ligne (Recommandé)
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### Méthode 2 : Installation Manuelle depuis GitHub
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
chmod +x install.sh
./install.sh
```

### Méthode 3 : Paquets Linux Natifs Précompilés
Téléchargez les paquets binaires depuis [GitHub Releases](https://github.com/SilentBlox01/Luma/releases) :
* **Debian / Ubuntu / Linux Mint** : `sudo apt install ./lumart-*.deb`
* **Fedora / RHEL / AlmaLinux** : `sudo dnf install ./lumart-*.rpm`
* **Arch Linux / Manjaro** : `makepkg -si` dans le dossier `dist/arch`

---

## Référence Complète des Commandes

```text
Utilisation : lumart [OPTIONS] <chemin_ou_url_de_l'image>
```

| Option | Paramètre | Description |
| :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | Sélectionne le moteur de rendu explicitement (auto-détecté par défaut). |
| `-S`, `--sextants`| — | Active les blocs Sextants Unicode 2x3 (standard par défaut de Mary Apex). |
| `-m`, `--manga` | — | Active le mode Manga Screentone 2.0 (trames Bayer 8x8 + lignes DoG). |
| `-s`, `--sketch`| — | Active le mode croquis épuré de lignes pures. |
| `-B`, `--braille` | — | Active les caractères Braille Unicode 2x4 (8 sous-pixels/cellule). |
| `-Q`, `--quadrants`| — | Active les blocs Quadrants Unicode 2x2 (4 sous-pixels/cellule). |
| `--blocks` | — | Active les blocs de terminal optimisés (`▀` / `▄`). |
| `-w`, `--width` | `<int>` | Largeur de sortie en colonnes (incompatible avec `-F`). |
| `-F`, `--fit` | — | **Ajustement Viewport** : calcule largeur et hauteur optimales pour s'adapter à l'écran sans défilement (incompatible avec `-w`). |
| `--fastfetch`, `--logo` | — | Rognage automatique des marges vides/transparentes pour logos compacts. |
| `-c`, `--color` | — | Force la sortie en mode couleur TrueColor complet (défaut). |
| `--no-color` | — | Désactive la sortie couleur et utilise le moteur monochrome. |
| `--font-ratio` | `<float>` | Calibration du ratio largeur/hauteur de la police du terminal (défaut : `0.5`). |
| `--boost`, `--vibrant` | — | Applique une saturation renforcée, du contraste et un traitement Retinex pour un rendu arcade vif. |
| `-i`, `--invert`| — | Inverse la luminosité (idéal pour terminaux à fond clair ; auto-détecté dans `-m`). |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Algorithme de tramage pour simuler des dégradés. |
| `--swap` | `<couleur1> <couleur2>` | Échange dynamiquement des couleurs dans l'espace 3D RGB. |
| `-o`, `-O`, `--output`, `--save` | `<fichier.png / .jpg / .gif>` | Exporte le résultat en image graphique ou GIF animé. |
| `--loop` | — | **Mode animation** : lecture en direct dans le terminal ou exportation en GIF animé. |
| `--transparent` | — | **Exclusif à Luris Mono** : exporte un sticker découpé avec transparence. |
| `--instant` | — | Affiche immédiatement sans animation de balayage progressif (défaut). |
| `--reveal` | — | Active l'animation de balayage progressif ligne par ligne. |
| `--paste` | — | Charge et restitue l'image actuellement dans le presse-papiers. |
| `-W`, `--webcam`| `[id]` | Diffuse la webcam en direct dans le terminal (30-60 FPS). |
| `--lang` | `<code>` | Définit la langue de l'interface (`fr`, `en`, `es`, etc.). |
| `-H`, `--history` | `[N]` | Affiche les N dernières commandes enregistrées dans l'historique. |
| `-R`, `--replay` | `[N]` | Réexécute la commande N de l'historique (défaut : la dernière). |
| `--clear-history`| — | Efface l'historique des commandes enregistrées. |
| `--install-desktop` | — | Ajoute l'action "Ouvrir avec Lumart" dans le menu contextuel Linux. |
| `-v`, `--version` | — | Affiche le rapport complet de diagnostic matériel, OS et moteurs. |
| `-u`, `--check-update`| — | Vérifie si de nouvelles versions sont disponibles sur GitHub. |
| `-uu`, `--upgrade` | — | Assistant interactif de mise à jour vers la version la plus récente. |
| `-dg`, `--downgrade` | `[ver]` | Sélecteur interactif de retour vers des versions antérieures. |

---

## Exemples Pratiques

### 1. Rendu Vectoriel Haute Définition
```bash
# Rendu direct à la largeur du terminal avec couleurs naturelles (Zéro Drapeau)
lumart photo.jpg

# Commande explicite équivalente
lumart photo.jpg -E mary -S -w 90

# Définir une largeur personnalisée en colonnes
lumart portrait.png -w 110

# Rendu percutant style arcade avec saturation et Retinex
lumart photo.jpg --boost

# Rendu cel-shading arcade avec Trumble
lumart anime.png -E trumble --blocks
```

### 2. Modes de Texture de Caractères
```bash
# Braille fluide 2x4 sous-pixels
lumart character.png -B

# Quadrants denses 2x2 blocs
lumart character.png -Q

# Demi-blocs Capcom CPS-2 / Neo-Geo
lumart character.png --blocks -w 85
```

### 3. Sticker Manga Découpé avec Transparence (Luris Mono)
```bash
# Créer un sticker PNG transparent pour Discord ou Telegram
lumart artwork.png -m --transparent -o manga_sticker.png

# Dessin d'architecture pur à la plume
lumart building.jpg -s -w 120

# Affiche rétro avec tramage ordonné de Bayer
lumart poster.jpg -m -d bayer -w 100
```

### 4. Diffusion Webcam en Direct dans le Terminal (Spectra Weep 1.4)
```bash
# Diffuser la webcam par défaut avec filtres shader temps réel
lumart -W

# Diffuser un deuxième périphérique webcam externe
lumart -W 1
```

### 5. URLs Web, Presse-papiers et Pipelines Unix
```bash
# Télécharger et rendre directement depuis une URL HTTPS
lumart https://example.com/art.png -w 80

# Rendre l'image actuellement copiée dans le presse-papiers
lumart --paste

# Entrée en pipeline depuis curl
curl -sL https://example.com/photo.jpg | lumart -
```

### 6. Remplacement Dynamique de Couleurs
```bash
# Remplacer les tons violets par du rose bonbon
lumart sprite.png --blocks --swap purple pink
```

---

## Secrets d'Ingénierie, Astuces de Pro et Philosophie du Terminal

> *"Un grand pouvoir de rendu implique une grande responsabilité esthétique."*

### 1. La Loi Gravitationnelle du Ratio de Police (`--font-ratio`)
* **Réalité Mathématique** : Sur un écran graphique standard, les pixels sont parfaitement carrés ($1:1$). Dans la jungle des émulateurs de terminal, chaque cellule de caractère est un monolithe rectangulaire allongé (généralement dans un rapport de $1:2$ ou $0.5$).
* **Le Symptôme** : Si votre personnage d'anime ressemble à une crêpe écrasée par une presse hydraulique de 50 tonnes ou étirée comme un élastique dans un trou de ver, n'accusez pas le moteur de rendu : accusez la géométrie de votre typographie.
* **Le Remède de Pro** :
  * Polices fines et élancées (comme *Fira Code* ou *JetBrains Mono* sans espacement vertical forcé) : essayez `--font-ratio 0.45` à `0.48`.
  * Polices monospace larges ou carrées : essayez `--font-ratio 0.52` à `0.58`.
  * Lumart applique `0.5` par défaut, ce qui couvre 90% des émulateurs modernes de la galaxie.

### 2. Le Théorème de la Toile Sombre et l'Excommunication de WebP
* **Pourquoi les moteurs TrueColor (Mary et Trumble) refusent-ils catégoriquement de générer des stickers transparents ?**
  * Les couleurs TrueColor en console sont conçues par émission lumineuse additive sur le noir profond du terminal (`#0c0c0c`).
  * Si vous retirez cet arrière-plan et collez l'image sur un fond blanc immaculé de WhatsApp ou dans une visionneuse transparente, le contraste optique s'effondre : les contours deviennent dentelés et le personnage ressemble à des confettis après une explosion dans une usine de cartouches d'encre.
  * **Luris Mono est le Seul Prophète du Sticker** : En travaillant à l'encre noire pure, trame d'imprimerie (*Ami-tone*) et lignes vectorielles DoG, Luris produit des stickers avec plus de 92.9% de vraie transparence alpha qui font fureur sur Telegram, Discord et Slack.
* **La Tragédie de WebP** :
  * Pendant des mois, les visionneuses d'images de bureau ont transformé les créations de terminal au format `.webp` en bouillies floues d'artefacts. Dans la version 2.4.0, le format `.webp` a été banni au royaume des ombres. Longue vie à la **Sainte Trinité** : `.png` (haute fidélité & stickers), `.jpg` (photos compactes à 95%) et `.gif` (animations multi-trames).

### 3. Le Duel Oklab : Pourquoi Mary Évalue 31 Combinaisons en 700 Nanosecondes
* Dans l'espace RVB euclidien classique, calculer la distance entre deux couleurs avec la formule de Pythagore ($\sqrt{\Delta R^2 + \Delta G^2 + \Delta B^2}$) est une illusion biologique : l'œil humain est ultra-sensible aux nuances de vert et presque aveugle aux variations subtiles de bleu foncé.
* Mary Apex projette chaque sous-pixel dans l'espace perceptuel **Oklab** ($L, a, b$) et évalue rigoureusement **les 31 bipartitions de couleur possibles par cellule** grâce aux instructions SIMD et OpenMP en C++17 natif.
* Pourquoi déployer une telle puissance de calcul pour un terminal ? Parce que les cycles CPU sont bon marché, mais un rendu médiocre en console est un crime de lèse-majesté esthétique.

### 4. Trumble Orelx et la Règle d'Or du Cel-Shading d'Arcade des Années 90
* Le redimensionnement classique (Lanczos ou bicubique) moyenne les pixels voisins. Une ligne d'encre noire fine de 1 pixel devient une brume grise et lâche de 3 pixels.
* Trumble Orelx inverse l'ordre du cosmos : il réduit l'image d'abord, puis **exécute la détection de contours Canny directement à la résolution sous-pixel exacte de la grille du terminal**.
* Résultat : les contours des yeux, des cheveux et des vêtements conservent une netteté absolue de **1 sous-pixel d'épaisseur en noir absolu**, retrouvant l'énergie brute d'une borne d'arcade Capcom CPS-2 de 1996.

### 5. Les Commandements Sacrés de l'Ajustement d'Écran (`-F` vs `-w`)
* **1er Commandement** : Si vous voulez que l'image épouse parfaitement votre écran sans avoir à faire défiler la molette de la souris comme un moulinet de pêche, utilisez `-F` (`--fit`).
* **2e Commandement** : Si vous intégrez l'image dans une barre latérale fixe de 60 colonnes pour *Fastfetch*, utilisez `-w 60 --fastfetch`.
* **3e Commandement** : N'exécutez jamais `lumart image.png -F -w 80`. Demander simultanément à Lumart de calculer la hauteur dynamique de l'écran et de respecter une largeur fixe est une hérésie logique. Lumart s'arrêtera poliment avec un `Code de sortie 2` et une explication limpide.

### 6. Le Mystère de la Commande `animate`
* Si vous cherchez la commande `animate` en vous demandant pourquoi nous utilisons `--loop` : le créateur du projet réserve `animate` pour un développement secret dans une dimension supérieure. Ne posez pas de questions dont votre émulateur de terminal ne saurait encore restituer les réponses. Utilisez `--loop` et profitez d'une fluidité parfaite à 60 FPS.

---

## Système de Mises à Jour et Restauration

Lumart intègre une gestion complète de son cycle de vie directement depuis le terminal :

* **Vérifier les Mises à Jour (`lumart -u`)** :
  Interroge l'API GitHub de façon sécurisée sans modifier vos fichiers locaux.
* **Mise à Niveau Automatique (`lumart -uu`)** :
  Télécharge la dernière version, recompile les bibliothèques C++ natives et effectue une sauvegarde dans `~/.config/luma/backup/`.
* **Restauration et Downgrade Immédiat (`lumart -dg`)** :
  Permet de revenir à n'importe quelle version précédente ou sauvegarde locale via un menu interactif ou en spécifiant la version :
  ```bash
  lumart -dg 2.2.0
  ```

---

## Intégration au Système et au Bureau

### 1. Menu Contextuel du Gestionnaire de Fichiers
Exécutez une seule fois :
```bash
lumart --install-desktop
```
Ceci enregistre un fichier `.desktop` et ajoute l'action *"Ouvrir avec Lumart"* au clic droit dans :
* **GNOME Files (Nautilus)**
* **KDE Dolphin**
* **Cinnamon Nemo**
* **XFCE Thunar**

### 2. Diagnostic d'Environnement (`lumart -v`)
Affiche l'état du support TrueColor 24 bits, la disponibilité du compilateur C++, les bibliothèques dynamiques (`libmary.so`, `libmonochrome.so`), les extensions vectorielles SIMD et les chemins de configuration actifs.

---

## Architecture et Ingénierie Interne

### 1. Espace Perceptuel Oklab et Optimisation Discrète
Les convertisseurs classiques calculent des distances euclidiennes dans l'espace sRGB non linéaire, provoquant des ruptures de teintes. Mary Apex 3.5 convertit chaque pixel en **RVB linéaire** puis en **Oklab** ($L, a, b$) :

$$\Delta E = \sqrt{(L_1 - L_2)^2 + (a_1 - a_2)^2 + (b_1 - b_2)^2}$$

Dans chaque cellule Sextants ($2 \times 3 = 6$ sous-pixels), il existe exactement $2^5 - 1 = 31$ manières distinctes de séparer les sous-pixels entre premier plan et arrière-plan. Mary évalue exhaustivement les 31 partitions, garantissant une **solution mathématiquement optimale** sans bruit stochastique.

### 2. Encrage Sous-Pixel 1-pour-1 de Trumble
Trumble Orelx redimensionne l'image à la résolution sous-pixel exacte de la cible **avant** d'appliquer le gradient de Canny, assurant que chaque trait d'encre conserve sa pureté d'origine.

### 3. Compresseur de Séquences d'Échappement ANSI ECMA-48
Lumart utilise un tampon d'émission qui mémorise l'état colorimétrique courant (`current_fg`, `current_bg`). Lorsque des cellules adjacentes partagent les mêmes couleurs, les codes d'échappement redondants sont supprimés, allégeant le flux de données jusqu'à **45%** et accélérant considérablement l'affichage via SSH.

---

## Dépannage et Compatibilité

### 1. Les couleurs paraissent ternes ou déformées
* Vérifiez que votre terminal supporte le TrueColor (24 bits) :
  ```bash
  export COLORTERM=truecolor
  ```
* Terminaux recommandés : **Kitty**, **Alacritty**, **WezTerm**, **iTerm2**, **Foot**, **GNOME Terminal**, **Konsole**, **Windows Terminal**.

### 2. Les caractères Sextants (`-S`) ou Braille (`-B`) s'affichent sous forme de carrés vides
* Votre police de caractères ne dispose pas des blocs Unicode 13.0.
* Polices recommandées avec prise en charge complète des symboles :
  * **Symbols Nerd Font** / **JetBrains Mono Nerd Font**
  * **DejaVu Sans Mono**
  * **Cascadia Code**

### 3. Désinstallation Propre
```bash
./uninstall.sh
# Ou si installé via paquet :
sudo apt remove lumart     # Debian/Ubuntu
sudo dnf remove lumart     # Fedora
sudo pacman -Rns lumart    # Arch Linux
```

---

## Licence

Lumart est publié sous licence GNU Affero General Public License v3.0 (**AGPL-3.0**). Consultez le fichier `LICENSE` pour connaître l'ensemble des termes.
