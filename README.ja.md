[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Pythonで書かれた高忠実度の画像からターミナルへのレンダリングエンジン。**

Lumaは、たった一つの目標に焦点を当てたオープンソースのターミナルレンダリングエンジンです：

> **最小限のターミナルスペースで最大限の視覚的忠実度を実現すること。**

画像の明るさを単純に文字にマッピングする従来のASCIIコンバーターとは異なり、Lumaは異なるターミナルグリフシステム、リニアRGBカラー演算、レンダリング技術を探求し、限られた数のターミナルセル内で可能な限り多くの視覚情報を保持します。

## 機能

* ターミナルでの高忠実度画像レンダリング
* ASCII、点字、ブロックベースのレンダリング
* **OSスタイルレンダリング (`--os-style`)**: Neofetchスタイルのロゴのためのクラシックなターミナル文字（ドット、文字）。
* **リアルタイムカラー交換 (`--swap`)**: 3Dユークリッド色距離に基づいて最大5つの色を動的に交換します。
* **エピックカラーエンジン（デフォルト）**: 濁った出力を防ぐためにリニアRGB空間で色を平均化し、同時に動的なコントラストと彩度（HDR）を適用します。
* 設定可能な出力幅
* Truecolorターミナルのサポート（24ビットANSI）
* 非常に小さな出力サイズ向けに設計
* Pythonベースで高い拡張性

## 例

```bash
# 点字文字、色を使用して画像を変換し、紫色をピンクに置き換えます
luma image.png -w 45 --braille -c --swap purple pink
```

## インストール

Lumaをソースコードから直接実行するか、ネイティブLinuxパッケージ（DEB、RPM、またはArch PKGBUILD）にビルドすることができます。

**オプション 1: コンパイル済みパッケージをダウンロードする（推奨）**
すぐに使用できる `.deb` または `.rpm` パッケージを [GitHub Releases](https://github.com/SilentBlox01/Luma/releases) ページから直接ダウンロードできます。

**オプション 2: ソースから直接実行する**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
# Pillowがインストールされていることを確認してください
pip install -r requirements.txt
python3 lumart.py --help
```

**オプション 3: ネイティブパッケージを自分でコンパイルして構築する**
Lumaには、PyInstallerを使用してツールをスタンドアロンバイナリにパッケージ化するための自動ビルドスクリプトが含まれています。
```bash
chmod +x build_packages.sh
./build_packages.sh
```
コンパイル後、パッケージマネージャーを使用してグローバルにインストールできます：
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-2.0.0.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-2.0.0.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

## 使用法

パッケージをインストールした場合、どこからでも `lumart` または `luma` を実行できます。そうでない場合は、直接pythonスクリプトを実行してください。

> **💡 プロのヒント:** Luma は背景が透明な画像で最もよく機能します！ エンジンは透明なピクセルを自動的に無視するため、ロゴやキャラクターがターミナルの背景に完璧に浮かび上がります。

```bash
# 基本的な使用方法
python3 lumart.py image.png
```

出力幅（文字数）を指定する：
```bash
python3 lumart.py image.png -w 30
```

Truecolorを使用した高忠実度点字レンダリングを有効にする：
```bash
python3 lumart.py image.png --braille -c
```

レトロなOSスタイルの文字レンダリングを強制する（OSロゴに便利です）：
```bash
python3 lumart.py image.png --os-style -c
```

## アンインストール

システムからLumaを削除する場合、インストール方法によってコマンドが異なります：

**パッケージマネージャー経由でインストールした場合 (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**pip経由でインストールした場合:**
```bash
pip uninstall lumart
```

**手動でインストールした場合:**
提供されているアンインストールスクリプトを実行できます：
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## 哲学

ターミナルレンダリングは視覚的圧縮の一形態です。

課題は、単に画像を文字に変換することではありません。課題は、最小限のターミナルセルを使用して、可能な限り多くの視覚情報を表現することです。

したがって、Lumaは単純に認識可能なASCIIアートを生成するのではなく、数学的に正確な色空間（Linear RGB vs sRGB）と動的HDRカーブを利用して、**知覚的忠実度**に焦点を当てています。

## トラブルシューティング

フォント、色、またはモジュールの欠落に関する問題がありますか？ 一般的な問題の迅速な解決については、[トラブルシューティングガイド](TROUBLESHOOTING.md)をご覧ください。

## ロードマップ

* [x] 初期の画像からターミナルへのレンダラー
* [x] 点字レンダリング
* [x] ブロックベースのレンダリング
* [x] 改善された知覚的レンダリング（Linear RGBエンジン）
* [x] コントラストと輝度の処理（エピックエンジン）
* [x] リアルタイムカラーマッピングと閾値
* [ ] 高度なディザリング
* [ ] 自動グリフ選択
* [ ] 画像類似度ベンチマーク
* [ ] レンダリングの最適化
* [ ] 機械学習（Machine Learning）支援レンダリング
* [ ] ビデオおよびGIFレンダリングのサポート
* [ ] 拡張されたターミナルグリフシステム

## 貢献

Lumaはオープンソースプロジェクトであり、貢献を歓迎します。

レンダリングアルゴリズム、最適化、グリフシステム、ベンチマーク、または改善に関するアイデアがある場合は、気軽にissueを開くかpull requestを送信してください。（詳細は [CONTRIBUTING.ja.md](CONTRIBUTING.ja.md) を参照してください）。

## ライセンス

LumaはGNU Affero General Public License v3.0 (AGPL-3.0)の下でリリースされています。詳細については `LICENSE` ファイルを参照してください。
