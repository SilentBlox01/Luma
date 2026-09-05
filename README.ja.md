[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**PythonとモダンC/C++で書かれた高忠実度の画像からターミナルへのレンダリングエンジン。**

Lumaは、たった一つの目標に焦点を当てたオープンソースのターミナルレンダリングエンジンです：

> **最小限のターミナルスペースで最大限の視覚的忠実度を実現すること。**

画像の明るさを単純に文字にマッピングする従来のASCIIコンバーターとは異なり、Lumaは異なるターミナルグリフシステム、リニアRGBカラー演算、そしてネイティブC/C++コンピュータビジョンアルゴリズムを探求し、限られた数のターミナルセル内で可能な限り多くの視覚情報を保持します。

## 機能

* ターミナルでの高忠実度画像レンダリング
* ASCII、点字、ブロックベースのレンダリング
* **ハイブリッドデュアルエンジンアーキテクチャ**:
  * **リニアRGBカラーエンジン** (Python / Pillow): 動的HDRコントラスト曲線、リニア色空間でのブレンド ($C_{\text{linear}} = C_{\text{srgb}}^{2.2}$)、24ビットANSI TrueColor。
  * **高性能モノクロ＆マンガエンジン** (ネイティブC++17): 10ミリ秒未満の高速処理、ガウス差分法 (DoG) による線画輪郭抽出、Bill Atkinson誤差拡散 (1984年 MacPaint)、8x8 Bayerスクリーントーン (*Ami-tone*)。
* **エンジンセレクター (`-E`, `--engine`)**: `color`、`mono`、`bw`、`manga`、`sketch` を動的に切り替え可能。
* **純粋な線画スケッチモード (`-s`, `-E sketch`)**: アニメやイラストのためのノイズのない輪郭抽出。
* **マンガスクリーントーン 2.0 (`-m`, `-E manga`)**: 中間トーンに本物の網点スクリーントーンを適用し、純白の肌と濃黒のインクを両立。
* **Atkinson ＆ ハーフトーンディザリング (`-d` / `--dither`)**: `atkinson`、`floyd`、`bayer`、`none` をサポート。
* **2x2 象限HDブロック (`--blocks`)**: Unicode象限文字 (`▘▝▀▖▌▞▛▗▚▐▜▄▙▟█`) によるセルあたり4サブピクセル描画。
* **OSスタイルレンダリング (`--os-style`)**: Neofetchスタイルのロゴのためのクラシックなターミナル文字（ドット、文字）。
* **リアルタイムカラー交換 (`--swap`)**: 3Dユークリッド色距離に基づいて最大5つの色を動的に交換します。
* **外部ネイティブ依存関係ゼロ**: パブリックドメインのヘッダー (`stb_image.h` および `stb_image_resize2.h`) で自己完結。OpenCVやlibpngは不要です。
* **完全なPythonフォールバックパリティ**: C++コンパイラがない環境でも、同一の純粋なPython実装にシームレスに切り替わります。
* 設定可能な出力幅と明暗ターミナルの自動検出 (`-i`, `--invert`)
* インタラクティブなアップデート (`-uu`)、ロールバック (`-dg`)、更新確認 (`-u`) スイート
* 包括的なシステム・エンジン診断 (`-v`, `--version`)

## 例

```bash
# 点字文字、色を使用して画像を変換し、紫色をピンクに置き換えます
luma image.png -w 45 --braille -c --swap purple pink
```

## インストール

Lumaは1行のコマンドでインストールするか、ソースコードから直接実行するか、ネイティブLinuxパッケージ（DEB、RPM、またはArch PKGBUILD）にビルドすることができます。

**クイックインストール（推奨）:**
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

**オプション 1: ソースから直接実行 / ローカルインストーラー**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
./install.sh
```

**オプション 2: コンパイル済みパッケージをダウンロードする**
[GitHub Releases](https://github.com/SilentBlox01/Luma/releases) ページから直接 `.deb` または `.rpm` パッケージをダウンロードできます。

**オプション 3: ネイティブパッケージを自分でコンパイルして構築する**
Lumaには、PyInstallerを使用してツールをスタンドアロンバイナリにパッケージ化するための自動ビルドスクリプトが含まれています：
```bash
chmod +x build_packages.sh
./build_packages.sh
```
コンパイル後、パッケージマネージャーを使用してグローバルにインストールできます：
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-*.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-*.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

**オプション 4: ネイティブC++エンジンの手動コンパイル**
完全なパッケージを作らずにネイティブC++エンジンのみをコンパイルする場合：
```bash
# スタンドアロンCLIバイナリ:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono

# 共有ライブラリ (Pythonからctypes経由でインプロセス高速化):
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
```

## 使用法

パッケージをインストールしたかインストーラーを実行した場合は、どこからでも `lumart` または `luma` を実行できます。それ以外の場合は、Pythonスクリプトを直接実行してください。

> **💡 プロのヒント:** Lumaは透過背景の画像と美しく連携します！透過ピクセルを自動的に無視するため、ロゴやキャラクターがターミナル背景に綺麗に映えます。

```bash
# 基本的な使用法
python3 lumart.py image.png
```

出力幅の指定（文字数）:
```bash
python3 lumart.py image.png -w 30
```

点字レンダリングとTruecolorの有効化:
```bash
python3 lumart.py image.png --braille -c
```

純粋な線画スケッチモード（クリーンなDoG輪郭線）:
```bash
python3 lumart.py image.png -E sketch -w 100
# または: python3 lumart.py image.png -s -w 100
```

マンガスクリーントーン 2.0 モード (DoG輪郭 + 8x8 Bayer網点):
```bash
python3 lumart.py image.png -E manga -w 120
# または: python3 lumart.py image.png -m -w 120
```

Atkinsonディザリングによるモノクロ表示 (1984 MacPaint):
```bash
python3 lumart.py image.png -E mono -d atkinson -w 100
# または従来のFloyd-Steinberg: python3 lumart.py image.png -E mono -d floyd -w 100
```

2x2 象限HDブロック:
```bash
python3 lumart.py image.png -E mono --blocks -w 80
```

純粋な白黒モノクロ:
```bash
python3 lumart.py image.png -E mono --braille -w 100
```

クラシックなOSスタイルレンダリング:
```bash
python3 lumart.py image.png --os-style -c
```

完全なシステムおよびエンジン診断の表示:
```bash
luma -v
# または: luma --version
```

## 更新とロールバック

Lumaはアップデートと復元を明示的に制御できます：

- **アップデートの確認（ダウンロードや変更は行いません）:**
  ```bash
  luma -u
  # または: luma --update / luma --check-update
  ```
- **インタラクティブアップグレード:**
  ```bash
  luma -uu
  # または: luma --upgrade
  ```
  *(リリースノートを確認しながらバージョンを選択可能。`~/.config/luma/backup/` に自動バックアップ)*

- **インタラクティブロールバック / ダウングレード:**
  ```bash
  luma -dg
  # または: luma --downgrade / luma --rollback
  ```
  *(ローカルバックアップまたはGitHubリリースのいずれかを選択して復元)*

  バージョンを直接指定することも可能です：
  ```bash
  luma -dg 2.1.0
  ```

## アンインストール

Lumaをシステムから削除する場合：

**パッケージマネージャー経由の場合 (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**pip経由の場合:**
```bash
pip uninstall lumart
```

**手動インストールの場合:**
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## 理念

ターミナルレンダリングは、視覚的圧縮の一形態です。

課題は、単に画像を文字に変換することではありません。最小限のターミナルセルを使用して、可能な限り多くの視覚情報を表現することです。

したがって、Lumaは単に認識可能なASCIIアートを生成するのではなく、数学的に正確な色空間（リニアRGB vs sRGB）と動的HDR曲線を使用した**知覚的忠実度**に焦点を当てています。

## トラブルシューティング

フォント、色、またはモジュールの欠落でお困りですか？[トラブルシューティングガイド](TROUBLESHOOTING.md) をご覧ください。
