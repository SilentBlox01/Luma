[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.4.1 (Apex Horizon)
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.4.1

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Language: Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![C++: 17 Multi-Core](https://img.shields.io/badge/C%2B%2B-17%20OpenMP%20SIMD-orange.svg)](https://isocpp.org/)
[![Platform: Linux / macOS / BSD](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20BSD-lightgrey.svg)](https://github.com/SilentBlox01/Luma)
[![8言語対応](https://img.shields.io/badge/Languages-8%20Locales-purple.svg)](#対応言語)

**Lumart**は、現代のターミナルエミュレータのために開発された高度なビジュアルエンジニアリングスイートです。その設計思想は極めてシンプルです。

> **最小のターミナル領域で最大の視覚密度と審美性を実現する。**

単に画像の輝度を文字記号に置き換える従来のアスキーアート変換器とは根本的に異なり、LumartはネイティブマルチコアC++17（OpenMP）と高度に最適化されたPythonで構築された**4つの専門画像処理・サブピクセルレンダリングエンジン**を統合しています。写真、アニメイラスト、ゲームスプライト、ライブWebカメラ映像を、ターミナル上で圧倒的なグラフィックアート体験へと昇華させます。

---

## 目次
1. [4大主力レンダリングエンジン](#4大主力レンダリングエンジン)
   - [Mary Apex 3.5](#1-mary-apex-35-写実的ベクターカラー旗艦)
   - [Trumble Orelx 2.2](#2-trumble-orelx-22-レトロアーケード--アニメセルルック)
   - [Luris Mono 2.6](#3-luris-mono-26-漫画スクリーントーン--モノクロ)
   - [Spectra Weep 1.4](#4-spectra-weep-14-リアルタイムwebカメラ映像)
2. [エンジン比較マトリックス](#エンジン比較マトリックス)
3. [ビジュアルギャラリー＆出力例](#ビジュアルギャラリー出力例)
4. [画像エクスポート、アニメーションおよび透過ステッカー方針](#画像エクスポートアニメーションおよび透過ステッカー方針)
5. [対応言語（8言語）](#対応言語)
6. [インストール](#インストール)
7. [CLIコマンド完全リファレンス](#cliコマンド完全リファレンス)
8. [実践クックブック＆サンプル](#実践クックブック)
9. [エンジニアリングの秘密、Pro-Tips＆ターミナル哲学](#エンジニアリングの秘密pro-tipsターミナル哲学)
10. [アップデートおよびロールバックシステム](#アップデートおよびロールバックシステム)
11. [デスクトップ環境・OSとの統合](#デスクトップ環境osとの統合)
12. [内部アーキテクチャと数学](#内部アーキテクチャと数学)
13. [トラブルシューティング](#トラブルシューティング)
14. [ライセンス](#ライセンス)

---

## 4大主力レンダリングエンジン

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

### 1. Mary Apex 3.5 (写実的ベクターカラー旗艦)
* **設計目標**: 連続的なマイクログラデーション、複雑な写真ライティング、写実的なポートレート。
* **C++17 OpenMPマルチコア**: SIMD並列化アクセラレーション（共有ライブラリ `libmary.so` およびバイナリ `luma-mary`）。
* **厳密大域最小Oklab二分割法（セルあたり31通りの全離散探索）**: K-Means等の局所解トラップを完全排除。1セルあたり700ナノ秒未満で31通りの色彩二分割を全探索し、知覚色差（$\Delta E$）の大域的絶対最小解を保証。
* **$O(1)$ 高速ガイデッドフィルタ＆鏡面反射ブースト（$L > 0.82$）**: 肌の階調を滑らかに保持しながら、瞳や金属のハイライト光沢をクリアに強調。
* **Unicode 13.0 セクスタント 2x3 標準搭載**: 1文字あたり6サブピクセルを持つブロック文字（`🬀`-`🬻`, `█`, `▌`, `▐`）。さらに2x4点字（`-B`）、2x2クアドラント（`-Q`）、ハーフブロック（`--blocks`）にも対応。
* **厳密アルファ分離**: 背景の透過領域が輪郭ピクセルの色計算を汚染せず、暗いフリンジや黒ずみを根絶。
* **ターミナルキャンバス出力**: 画像ファイル（`.png` / `.jpg`）への書き出し時、端正なターミナルダーク背景（`#0c0c0c`）上で描画され、ターミナルアートとしての高い品位を保証。

### 2. Trumble Orelx 2.2 (レトロアーケード & アニメセルルック)
* **設計目標**: アニメイラスト、ゲームスプライト、コミック、ポップアート。
* **1対1サブピクセル先行インキング**: リサイズ処理をバイラテラルフィルタおよびCanny輪郭検出の*前*に実行。黒インク輪郭線が出力解像度において正確に1サブピクセルの太さを維持し、Lanczos補間によるぼやけや色混じりを防止。
* **32-bit Capcom CPS-2 / SNK Neo-Geo アーケードパレット**: 90年代の格闘ゲームを彷彿とさせる色彩強調（彩度+28%、選択的コントラスト+15%）。
* **適応型クアドラント形状補正**: 形状ペナルティ下限を30に緩和し、斜めブロック（`▞`, `▚`, `▘`, `▝`）が瞳や衣服の有機的な曲線を忠実に追従。

### 3. Luris Mono 2.6 (漫画スクリーントーン & モノクロ C++17)
* **設計目標**: 本格的な日本漫画スタイル、インク画、ペン画、透過ステッカー。
* **DoG（ガウシアン差分法）輪郭抽出**: ターミナル幅に合わせて畳み込み半径を最適化し、テクスチャノイズのないクリーンな線画を抽出。
* **Manga Screentone 2.0 (*Ami-tone*)**: 伝統的な印刷アミ点をBayer 8x8マトリクスで再現。純白の紙地と深みのある黒インクで階調を表現。
* **Atkinson誤差拡散法 (MacPaint 1984)**: 25%の誤差をあえて保持することで、不規則なざらつきを抑えた美しいグラデーションを生み出す名作アルゴリズム。
* **透過ステッカー専用エンジン（`--transparent`）**: Luris Monoは**透過背景付きPNGステッカーを出力できる唯一のエンジン**であり、DiscordやTelegram用スタンプの作成に最適。

### 4. Spectra Weep 1.4 (リアルタイムWebカメラ映像)
* **設計目標**: ターミナル内での秒間30〜60フレーム超低遅延ビデオストリーミング（`lumart --webcam` または `lumart -W`）。
* **ゼロレイテンシ**: V4L2/OpenCVの最適化キャプチャとターミナルリフレッシュレートの同期。
* **5種のリアルタイムシェーダー**: Normal TrueColor, Weep Cyberpunk, Matrix Green Rain, Thermal FLIR, Manga Ink。

---

## エンジン比較マトリックス

| 項目 | Mary Apex 3.5 | Trumble Orelx 2.2 | Luris Mono 2.6 | Spectra Weep 1.4 |
| :--- | :--- | :--- | :--- | :--- |
| **美学的フォーカス** | 写実的ベクター表現 | レトロアーケード / セルルック | 日本の漫画 / ペン画 | リアルタイム動画 / Webカメラ |
| **実装言語** | C++17 OpenMP + SIMD | Python + 高速化OpenCV | C++17 ネイティブ | Python + OpenCV V4L2 |
| **色空間** | 知覚的Oklab（$\Delta E$） | 32-bit カプコンCPS-2パンチ | モノクロ / Ami-tone | TrueColor / RGBシェーダー |
| **標準モード** | **セクスタント 2x3 (`-S`)** | **クアドラント 2x2 (`--blocks`)**| **漫画 2.0 (`-m`)** | **30-60 FPS ストリーム** |
| **サブピクセル密度**| 最大 6 サブピクセル/セル | 最大 4 サブピクセル/セル | 最大 4 サブピクセル/セル | ターミナル幅に応じ動的決定 |
| **輪郭線インキング** | 滑らかなアンチエイリアス | **Canny 1対1 サブピクセル** | **適応型DoG線画抽出** | 任意（漫画シェーダー） |
| **出力キャンバス** | ターミナル背景（`.png`, `.jpg`）| ターミナル背景（`.png`, `.jpg`）| **透過PNGステッカー (`--transparent`)**| リアルタイムスナップショット |
| **CLIフラグ** | `lumart img.jpg` *(標準)* | `lumart img.jpg -E trumble` | `lumart img.jpg -m` | `-W` または `--webcam` |

---

## ビジュアルギャラリー＆出力例

### 1. エンジン対決：Mary Apex 3.5 vs Trumble Orelx 2.2
![Lumart エンジン比較デモ](assets/engine_showdown.png)

### 2. サイドバイサイド比較：フォトリアルTrueColor vs 透過マンガステッカー

| Mary Apex 3.5 (写実的TrueColor) | Luris Mono 2.6 (透過マンガステッカー) |
| :---: | :---: |
| ![Cinderella Mary](assets/cinderella_mary_apex.png)<br><sub>`lumart cinderella.jpg` *(Mary セクスタント標準)*</sub> | ![Cinderella Manga Sticker](assets/cinderella_manga_sticker.png)<br><sub>`lumart cinderella.jpg -m --transparent -o sticker.png`</sub> |
| ![Hanako Mary Boosted](assets/hanako_boosted.png)<br><sub>`lumart hanako.png --boost` *(Punch Arcade Retinex)*</sub> | ![Hanako Manga Sticker](assets/hanako_manga_sticker.png)<br><sub>`lumart hanako.png -m --transparent -o sticker.png`</sub> |
| ![Gothic Nun Mary](assets/gothic_nun_mary.png)<br><sub>`lumart gothic_nun.png`</sub> | ![Gothic Nun Manga Sticker](assets/gothic_nun_manga_sticker.png)<br><sub>`lumart gothic_nun.png -m --transparent -o sticker.png`</sub> |
| ![Slime Mary](assets/slime_mary.png)<br><sub>`lumart slime.png`</sub> | ![Slime Manga Sticker](assets/slime_manga_sticker.png)<br><sub>`lumart slime.png -m --transparent -o sticker.png`</sub> |

### 3. サブピクセル文字テクスチャ密度

| セクスタント 2x3 (`-S` / 標準) | 点字 Braille 2x4 (`-B`) | クアドラント 2x2 (`-Q`) |
| :---: | :---: | :---: |
| ![Sextants 2x3](assets/texture_sextants.png)<br><sub>6サブピクセル/セル（滑らかなグラデーション）</sub> | ![Braille 2x4](assets/texture_braille.png)<br><sub>8サブピクセル/セル（精密な点描・ポートレート）</sub> | ![Quadrants 2x2](assets/texture_quadrants.png)<br><sub>4サブピクセル/セル（ピクセルアート・アーケード）</sub> |

---

## 画像エクスポート、アニメーションおよび透過ステッカー方針

Lumartは、ターミナルアートを160列（セクスタントで320×480サブピクセル）のスタジオ解像度で画像出力（`-o output.png`、`-o output.jpg` または `-o anim.gif`）できます。

### 1. アニメーションモード＆アニメーションGIFエクスポート（`--loop`）
![ターミナルアニメーション再生デモ](assets/animated_demo.gif)

Lumart v2.4.0では、アニメーションファイル（GIFおよびAPNG）のネイティブサポートが追加されました：
* **ターミナルでのスムーズな再生**: `lumart anim.gif --loop` は各フレームを事前に計算してANSIシーケンスとしてキャッシュし、ターミナル内で60 FPSのスムーズなループ再生を実現します。
* **アニメーションGIFへのレンダリング**: `lumart anim.gif --loop -o output.gif`（または `--save output.gif`）により、各フレームを高精細サブピクセル精度でラスタライズし、完全なアニメーションGIFを生成します。

### 2. WebP形式の恒久的一般廃止
* **`.webp`形式へのエクスポートは恒久的に無効化されました**。
* `.webp`を指定した場合はエラーを表示し、`.png`、`.jpg` または `.gif` の利用を案内します。
* 正式対応形式:
  * **`.png`**: 可逆圧縮、高精細、アルファチャンネル完全対応。
  * **`.jpg` / `.jpeg`**: 普遍的互換性、品質95%最適化。
  * **`.gif`**: Webおよびターミナル用マルチフレームアニメーション。

### 3. 透過ステッカー出力はLuris Mono専用
* カラーエンジン（MaryおよびTrumble）を透明背景で切り抜いて通常の画像ビューアで見ると、ターミナルの枠組みがないため解像度の粗い画像と誤認されやすくなります。そのため、カラーモデルは常に**洗練されたダークターミナル背景（`#0c0c0c`）**上で出力されます。
* 一方、**モノクロ（Luris Mono）**は漫画アミ点とインク線がステッカーとしての美しさを完璧に表現できるため、`--transparent`による透過ステッカー出力が可能です（95%以上の検証済み透過率）。
* MaryやTrumbleで `--transparent` を指定した場合は通知メッセージを表示し、ターミナル背景付きで高品位に出力します。

---

## 対応言語

Lumartは**8つの言語**に完全対応しています：

| コード | 言語名 | 自動判定 | 手動指定 |
| :---: | :--- | :--- | :--- |
| `ja` | 日本語 | `$LANG=ja_*` | `lumart --lang ja` |
| `en` | English | `$LANG=en_*` (標準) | `lumart --lang en` |
| `es` | Español | `$LANG=es_*` | `lumart --lang es` |
| `pt` | Português | `$LANG=pt_*` | `lumart --lang pt` |
| `fr` | Français | `$LANG=fr_*` | `lumart --lang fr` |
| `ru` | Русский | `$LANG=ru_*` | `lumart --lang ru` |
| `de` | Deutsch | `$LANG=de_*` | `lumart --lang de` |
| `ko` | 한국어 | `$LANG=ko_*` | `lumart --lang ko` |

---

## インストール

### 自動ワンライナー導入（推奨）
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### ソースコードからの導入
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
chmod +x install.sh
./install.sh
```

### ネイティブLinuxパッケージ（ビルド済み）
[GitHub Releases](https://github.com/SilentBlox01/Luma/releases) からバイナリパッケージをダウンロード：
* **Debian / Ubuntu / Linux Mint**: `sudo apt install ./lumart-*.deb`
* **Fedora / RHEL / AlmaLinux**: `sudo dnf install ./lumart-*.rpm`
* **Arch Linux / Manjaro**: `dist/arch` ディレクトリで `makepkg -si`

---

## CLIコマンド完全リファレンス

```text
使用方法: lumart [オプション] <画像ファイルまたはURL>
```

### 1. エンジン＆文字テクスチャ
| オプション | 引数 | 説明 |
| :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | レンダリングエンジンを明示的に指定（デフォルトは自動選択）。 |
| `-S`, `--sextants`| — | ソリッドUnicode Sextants 2x3で描画（Mary Apexフラグシップ標準）。 |
| `-B`, `--braille` | — | Unicode 2x4 点字文字で描画（1セル8サブピクセル）。 |
| `-Q`, `--quadrants`| — | Unicode 2x2 クアドラント文字で描画（1セル4サブピクセル）。 |
| `--blocks` | — | 最適化されたハーフブロック文字（`▀` / `▄`）を使用。 |
| `-m`, `--manga` | — | Manga 2.0 スクリーントーン（Bayerアミ点＋DoG線画）。 |
| `-s`, `--sketch`| — | クリーンな輪郭のペン画スケッチモード。 |

### 2. 色彩・寸法・視覚調整
| オプション | 引数 | 説明 |
| :--- | :--- | :--- |
| `-w`, `--width` | `<数値>` | 出力横幅（文字数、`-F` と排他）。 |
| `-F`, `--fit` | — | **ビューポート自動最適化**: スクロールなしで画面に収まるよう幅と高さを自動計算（`-w` と排他）。 |
| `--fastfetch`, `--logo` | — | コンパクトロゴ用に余白・透過マージンを自動トリミング。 |
| `-c`, `--color` | — | フルTrueColorカラー出力を強制（デフォルト）。 |
| `--no-color` | — | カラー出力を無効化しモノクロエンジンにルーティング。 |
| `--font-ratio` | `<実数値>` | 端末フォント縦横比の幅/高さキャリブレーション（デフォルト: `0.5`）。 |
| `--boost`, `--vibrant` | — | 鮮やかなアーケード発色にするため、彩度・コントラスト強調およびRetinex処理を適用。 |
| `-i`, `--invert`| — | 明暗の反転（白背景ターミナル向け；`-m` モードで自動検出対応）。 |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | ディザリングアルゴリズムの選択。 |
| `--swap` | `<色1> <色2>` | RGB空間におけるリアルタイム色彩置換。 |
| `--instant` | — | プログレッシブ走査アニメーションを行わず即座に出力（デフォルト）。 |
| `--reveal` | — | 1行ずつのプログレッシブ走査スキャン表示アニメーションを有効化。 |

### 3. 画像エクスポート＆アニメーション
| オプション | 引数 | 説明 |
| :--- | :--- | :--- |
| `-o`, `-O`, `--output`, `--save` | `<出力先.png / .jpg / .gif>` | 高精細画像ファイルまたはアニメーションGIFへのエクスポート。 |
| `--loop` | — | **アニメーションモード**: ターミナル内ループ再生またはアニメーションGIFエクスポート。 |
| `--transparent` | — | **Luris Mono専用**: 透過背景付きステッカーを出力。 |
| `--paste` | — | クリップボード内の画像を直接読み込んで描画。 |

### 4. Webカメラ＆ライブ映像
| オプション | 引数 | 説明 |
| :--- | :--- | :--- |
| `-W`, `--webcam`| `[id]` | Webカメラ映像のライブストリーミング（30-60 FPS、デフォルトID: `0`）。 |

### 5. 管理・履歴・言語設定
| オプション | 引数 | 説明 |
| :--- | :--- | :--- |
| `--lang` | `<言語コード>` | インターフェース言語を設定（`ja`, `en`, `es`等）。 |
| `-H`, `--history` | `[件数]` | 過去の実行履歴を表示。 |
| `-R`, `--replay` | `[番号]` | 履歴からコマンドを再実行。 |
| `--clear-history`| — | 保存されたコマンド履歴を消去。 |
| `--install-desktop` | — | Linux右クリックメニューに「Lumartで開く」を登録。 |
| `-v`, `--version` | — | ハードウェア・OS・エンジンの詳細診断を表示。 |
| `-u`, `--check-update`| — | GitHub上の最新バージョンを確認。 |
| `-uu`, `--upgrade` | — | 対話型自動アップグレードを実行。 |
| `-dg`, `--downgrade` | `[バージョン]`| 過去バージョンへの安全なロールバック。 |

---

## 実践クックブック

### 1. 高解像度ターミナルレンダリング（ゼロフラグまたは明示的フラグ）
```bash
# フラグ不要でフル解像度・TrueColor忠実描画（ゼロフラグ）
lumart photo.jpg

# 明示的なフラグシップ指定（同等の出力）
lumart photo.jpg -E mary -S

# 出力横幅をカラム数で指定
lumart portrait.png -w 110

# 彩度とRetinex強調によるアーケード発色
lumart photo.jpg --boost

# Trumbleによるレトロアーケード・セルルック描画
lumart anime.png -E trumble --blocks
```

### 2. 文字テクスチャモード
```bash
# 滑らかなUnicode点字 2x4 サブピクセル
lumart character.png -B

# 高密度Unicodeクアドラント 2x2
lumart character.png -Q

# 最適化ハーフブロック
lumart character.png --blocks -w 85
```

### 3. 透過背景の漫画ステッカーPNG作成（Luris Mono）
```bash
# DiscordやTelegram向けの透過PNGステッカーを作成
lumart artwork.png -m --transparent -o manga_sticker.png

# 純粋な建築・ペン画スケッチ
lumart building.jpg -s -w 120

# Bayer組織的ディザリングによるレトロポスター調
lumart poster.jpg -m -d bayer -w 100
```

### 4. ターミナル内リアルタイムWebカメラ映像 (Spectra Weep 1.4)
```bash
# デフォルトWebカメラのリアルタイムシェーダー描画
lumart -W

# 外部接続Webカメラ（ID: 1）の描画
lumart -W 1
```

### 5. Web URL、クリップボードおよびUnixパイプライン
```bash
# HTTPS URLから直接フェッチしてレンダリング
lumart https://example.com/art.png -w 80

# クリップボード内の画像を即座にレンダリング
lumart --paste

# curlからの標準入力をパイプで受けて描画
curl -sL https://example.com/photo.jpg | lumart -
```

### 6. 動的カラー置換
```bash
# 紫系の色合いをバブルガムピンクに置換
lumart sprite.png --blocks --swap purple pink
```

---

## エンジニアリングの秘密、Pro-Tips＆ターミナル哲学

> *「大いなるレンダリング能力には、大いなる美的責任が伴う。」*

### 1. 文字アスペクト比の万有引力則 (`--font-ratio`)
* **数学的現実**: 通常のグラフィックキャンバスでは、ピクセルは完全な正方形（$1:1$）です。しかしターミナルエミュレータという過酷な荒野では、すべての文字セルは縦長の長方形モノリス（通常 $1:2$ または $0.5$ のアスペクト比）です。
* **症状**: レンダリングされたアニメキャラクターが、まるで50トンの油圧プレスで潰されたか、あるいはワームホールで引き伸ばされたガムのように見える場合、エンジンを責めてはいけません。フォントの幾何構造を疑ってください。
* **Proの処方箋**:
  * 細長く背の高いフォント（カスタムパディングなしの *Fira Code* や *JetBrains Mono* など）：`--font-ratio 0.45` 〜 `0.48` を試してください。
  * 幅広または正方形に近い等幅フォント：`--font-ratio 0.52` 〜 `0.58` を試してください。
  * Lumartのデフォルト値は `0.5` であり、既知の宇宙に存在する最新ターミナルエミュレータの90%に完璧に適合します。

### 2. 暗黒キャンバスの定理＆WebP追放令
* **なぜTrueColorエンジン（Mary＆Trumble）は透過ステッカーの出力を断固拒否するのか？**
  * TrueColorターミナルアートは、ターミナルの背景である漆黒の `#0c0c0c` に対する加法混色発光を前提に設計されています。
  * もしこの背景を取り去って純白のチャットアプリや透過ビューアに貼り付けると、光学的コントラストは完全に崩壊します。輪郭はジャギーだらけになり、キャラはトナー工場で爆破されたデジタル紙吹雪のように見えてしまいます。
  * **Luris Monoこそが選ばれし者**: 純粋な黒インク、ハーフトーン・スクリーントーン（*Ami-tone*）、DoGベクトル輪郭線を操るLurisは、92.9%以上の検証済みアルファ透明度を誇る本物のステッカーを生成し、Telegram、Discord、Slackで圧倒的な美しさを放ちます。
* **WebPの悲劇**:
  * 何ヶ月もの間、一般的なデスクトップ画像ビューアはターミナルラスタライズされた `.webp` ファイルの処理に苦しみ、シャープなANSIアートをぼやけたゴミへと変えてしまいました。v2.4.0において、`.webp` は正式に影の領域へと追放されました。**三位一体**万歳：`.png`（可逆超高解像度＆ステッカー）、`.jpg`（95%ハフマン圧縮写真）、`.gif`（マルチフレームアニメーション）。

### 3. Oklabの頂上決戦：なぜMaryは700ナノ秒で31通りの組み合わせを評価するのか
* 標準的なRGBユークリッド空間でピタゴラスの定理（$\sqrt{\Delta R^2 + \Delta G^2 + \Delta B^2}$）を用いて色差を計算するのは生物学的な妄想です。人間の網膜は緑の輝度変化には極めて敏感ですが、微妙な暗青色の違いにはほぼ盲目です。
* Mary Apexはすべてのサブピクセルを知覚空間 **Oklab**（$L, a, b$）へ写像し、C++17 OpenMP SIMDベクトル化を駆使して**セルあたりの全31通りの色分割**を厳密に評価します。
* ターミナルのためになぜこれほどの演算パワーを注ぎ込むのか？ CPUサイクルは安価ですが、醜悪なターミナルアートは美学上の重罪だからです。

### 4. Trumble Orelx＆1990年代アーケード・セルルックの黄金律
* 従来の画像縮小アルゴリズム（Lanczosやバイキュービックなど）は隣接ピクセルを平均化します。その結果、くっきりとした1ピクセルの黒インク輪郭線は、3ピクセルのぼやけた灰色モヤへと薄まってしまいます。
* Trumble Orelxは宇宙の秩序を逆転させます。画像を*先に*目標セル解像度へとリサイズし、**その後にターミナルの実サブピクセル解像度上でCannyエッジ検出を実行します**。
* その結果、キャラクターの髪の毛、瞳の輪郭、服のシワが**漆黒インクの正確な1サブピクセル**の鋭さを保ち、1996年のカプコンCPS-2アーケード筐体のような鮮烈なパンチ力を再現します。

### 5. 画面フィットの神聖なる戒律 (`-F` vs `-w`)
* **第1戒**: カジキ釣りリールのようにホイールを回転させることなく、画面に完璧にフィットさせたいときは `-F`（`--fit`）を使用せよ。
* **第2戒**: *Fastfetch* の固定60列サイドバーやステータスダッシュボードに埋め込むときは `-w 60 --fastfetch` を使用せよ。
* **第3戒**: 決して `lumart image.png -F -w 80` を実行してはならない。動的なビューポート高さの計算と固定幅の強制を同時にLumartへ要求することは、アリストテレス的論理学への冒涜である。Lumartは親切な `Exit Code 2` と丁寧な解説を返して停止する。

### 6. `animate` コマンドの謎
* もしあなたが `animate` コマンドを探していて、なぜ `--loop` を使うのか不思議に思っているなら：作者は `animate` という名を、現在準備中のより高次元な極秘プロジェクトのために温存しています。あなたのターミナルエミュレータがまだ描画できない答えについて尋ねてはなりません。`--loop` を使用し、極上の60 FPSの快楽に浸ってください。

---

## アップデートおよびロールバックシステム

LumartはCLIから直接完全なライフサイクル管理を提供します：

* **アップデート確認 (`lumart -u`)**:
  ローカルファイルを一切変更することなくGitHub Releases APIに問い合わせます。
* **自動アップグレード (`lumart -uu`)**:
  最新リリースを取得し、ネイティブC++共有ライブラリを再コンパイルし、`~/.config/luma/backup/` に自動バックアップを作成します。
* **即時ロールバック / ダウングレード (`lumart -dg`)**:
  対話型メニューから過去のバージョンやローカルバックアップへ復元できます。バージョン番号を直接指定することも可能です：
  ```bash
  lumart -dg 2.2.0
  ```

---

## デスクトップ環境・OSとの統合

### 1. ファイルマネージャーの右クリックメニュー統合
初回に一度実行：
```bash
lumart --install-desktop
```
`.desktop` ファイルと右クリックアクションが登録され、以下のファイルマネージャーで**画像ファイルを右クリック**して直接開けるようになります：
* **GNOME Files (Nautilus)**
* **KDE Dolphin**
* **Cinnamon Nemo**
* **XFCE Thunar**

「Lumartで開く」を選択すると、高解像度ターミナルウィンドウが立ち上がり瞬時にグラフィックが描画されます。

### 2. 環境診断 (`lumart -v`)
TrueColor（24-bit）対応状況、C++ OpenMPコンパイラの有無、アクティブな共有ライブラリ（`libmary.so`, `libmonochrome.so`）、ターミナルサイズ、設定パスを瞬時に診断します。

---

## 内部アーキテクチャと数学

### 1. 知覚的Oklab色空間と離散組合せ最適化
従来のツールは非線形sRGB空間で色距離を計算するため、中光度域の濁りや色相ズレが発生します。Mary Apex 3.5はsRGBを線形RGBに変換した上で **Oklab**（$L, a, b$）へ射影します：

$$\Delta E = \sqrt{(L_1 - L_2)^2 + (a_1 - a_2)^2 + (b_1 - b_2)^2}$$

各セクスタントセル（$2 \times 3 = 6$ サブピクセル）において、前景色と背景色への非自明な分割方法は正確に $2^5 - 1 = 31$ 通り存在します。Maryはこの31通りを直接全探索し、確率的ノイズの一切ない数学的最適解を保証します。

### 2. Trumbleの1対1事前スケール・インキング
高解像度のエッジマップをLanczos等の縮小補間にかけると、1ピクセルの細い線が背景に溶け込んで消失します。Trumble OrelxはCanny勾配計算を走らせる*前*に、画像をセルの正確なサブピクセル解像度（$target\_width \times 2$）へとリサイズし、輪郭線が正確に1サブピクセルの鋭さを維持できるようにします。

### 3. ECMA-48 ANSIエスケープシーケンス・コンプレッサ
Lumartはアクティブなターミナル描画状態（`current_fg`, `current_bg`）を追跡します。同色を持つ隣接セルに対して重複するカラーコードを省略することで、ANSI出力ペイロードを最大 **45%** 削減し、SSH経由での描画速度を劇的に向上させます。

---

## トラブルシューティング

### 1. 色が褪せて見える、またはカラーバンディングが発生する
* お使いのターミナルがTrueColor（24-bit）に対応していることを確認してください。シェル設定ファイル（`.bashrc` / `.zshrc`）に追記します：
  ```bash
  export COLORTERM=truecolor
  ```
* 推奨TrueColorターミナル：**Kitty**, **Alacritty**, **WezTerm**, **iTerm2**, **Foot**, **GNOME Terminal**, **Konsole**, **Windows Terminal**。

### 2. セクスタント（`-S`）や点字（`-B`）が四角い「豆腐」記号になる
* お使いの等幅フォントにUnicode 13.0記号が含まれていません。
* 推奨フォント：
  * **Symbols Nerd Font** / **JetBrains Mono Nerd Font**
  * **DejaVu Sans Mono**
  * **Cascadia Code**

### 3. 完全アンインストール
```bash
./uninstall.sh
# またはパッケージマネージャ経由：
sudo apt remove lumart     # Debian/Ubuntu
sudo dnf remove lumart     # Fedora
sudo pacman -Rns lumart    # Arch Linux
```

---

## ライセンス

Lumartは GNU Affero General Public License v3.0 (**AGPL-3.0**) のもとで公開されています。詳細は `LICENSE` ファイルをご確認ください。

