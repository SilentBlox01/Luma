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
3. [Exportation Graphique et Politique de Stickers](#exportation-graphique-et-politique-de-stickers)
4. [Langues Supportées (8 Langues)](#langues-supportées)
5. [Installation Rapide et Paquets](#installation)
6. [Référence Complète des Commandes (CLI)](#référence-complète-des-commandes)
7. [Exemples Pratiques et Guide d'Utilisation](#exemples-pratiques)
8. [Système de Mises à Jour et Restauration](#système-de-mises-à-jour-et-restauration)
9. [Intégration au Système et Presse-papiers](#intégration-au-système)
10. [Architecture et Ingénierie Interne](#architecture-et-ingénierie-interne)
11. [Dépannage et Compatibilité](#dépannage)
12. [Licence](#licence)

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

## Exportation Graphique et Politique de Stickers

Lumart intègre un rasteriseur haute définition (`-o image.png` ou `-o image.jpg`) avec une largeur standard de studio de **160 colonnes**.

### 1. Désactivation Définitive du Format WebP
* **Le format `.webp` a été désactivé de manière permanente pour l'exportation graphique**.
* Toute tentative de spécifier une extension `.webp` entraîne un refus propre avec un message invitant à utiliser `.png` ou `.jpg`.
* Formats officiellement supportés :
  * **`.png`** : Qualité sans perte, compression optimisée et prise en charge du canal alpha transparent.
  * **`.jpg` / `.jpeg`** : Compatibilité universelle, qualité 95% et tables de Huffman optimisées.

### 2. Exclusivité des Stickers Transparents pour Luris Mono
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

---

## Référence Complète des Commandes

```text
Utilisation : lumart [OPTIONS] <chemin_ou_url_de_l'image>
```

| Option | Paramètre | Description |
| :--- | :--- | :--- |
| `-m`, `--manga` | — | Active le mode Manga Screentone 2.0 (trames Bayer 8x8 + lignes DoG). |
| `-s`, `--sketch`| — | Active le mode croquis épuré de lignes pures. |
| `-B`, `--braille` | — | Active les caractères Braille Unicode 2x4 (8 sous-pixels/cellule). |
| `-Q`, `--quadrants`| — | Active les blocs Quadrants Unicode 2x2 (4 sous-pixels/cellule). |
| `--blocks` | — | Active les blocs de terminal optimisés (`▀`). |
| `-w`, `--width` | `<int>` | Largeur de sortie en colonnes (défaut : largeur du terminal). |
| `-i`, `--invert`| — | Inverse la luminosité (idéal pour terminaux à fond clair ; auto-détecté dans `-m`). |
| `--boost`, `--vibrant` | — | Applique une saturation renforcée, du contraste et un traitement Retinex pour un rendu arcade vif. |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Algorithme de tramage pour simuler des dégradés. |
| `--swap` | `<couleur1> <couleur2>` | Échange dynamiquement des couleurs dans l'espace 3D RGB. |
| `-o`, `--output` | `<fichier.png / .jpg>` | Exporte le résultat en image graphique haute résolution. |
| `--transparent` | — | **Exclusif à Luris Mono** : exporte un sticker découpé avec transparence. |
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

### 1. Rendu Haute Définition (Zéro Drapeau)
```bash
lumart photo.jpg -w 90
```

### 2. Illustration Anime avec Blocs HD
```bash
lumart anime.png --blocks -w 85
```

### 3. Sticker Manga Découpé avec Transparence (Luris Mono)
```bash
lumart manga.png -m --transparent -o sticker.png
```

### 4. Diffusion Vidéo Webcam en Direct
```bash
lumart -W
```

### 5. Rendu depuis le Presse-papiers
```bash
lumart --paste
```

---

## Licence

Lumart est publié sous licence GNU Affero General Public License v3.0 (**AGPL-3.0**). Consultez le fichier `LICENSE` pour connaître l'ensemble des termes.
