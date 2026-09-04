[English](CONTRIBUTING.md) | [Español](CONTRIBUTING.es.md) | [Português](CONTRIBUTING.pt.md) | [Русский](CONTRIBUTING.ru.md) | [日本語](CONTRIBUTING.ja.md) | [Deutsch](CONTRIBUTING.de.md) | [한국어](CONTRIBUTING.ko.md)

# Luma への貢献

Luma の改善にご興味をお持ちいただきありがとうございます！本プロジェクトはターミナルの描画限界に挑むものであり、あらゆる貢献を大歓迎します。

## 🐛 バグ報告と機能提案

問題を見つけた場合や、素晴らしいアイデア（新しいレンダリングアルゴリズム、ディザリングパターン、アニメーションサポートなど）がある場合は、GitHub で **Issue** を作成してください。以下の情報を含めてください：
- 使用しているOSとターミナルエミュレータ（例: Fedora + Alacritty、Ubuntu + Kitty、Windows Terminal）。
- 実行した正確なコマンドと引数。
- 可能であれば、生成されたASCIIアートまたは元画像。

## 🛠️ コードによる貢献

1. GitHub でリポジトリを **フォーク** します。
2. 機能や修正用の **新しいブランチを作成** します (`git checkout -b feature/awesome-new-engine`)。
3. コードを記述し、**テスト** します。主要なロジックは `lumart.py` にあります。
4. 明確なメッセージで **コミット** します (`git commit -m 'feat: 新しいレンダリング処理の追加'`)。
5. ブランチに **プッシュ** します (`git push origin feature/awesome-new-engine`)。
6. **プルリクエスト (Pull Request)** を作成します。

### プロジェクト構成
- `lumart.py`: エンジンのコア全体：Linear RGB 色空間による正確なブレンド、Bayer ディザリング、点字（Braille）/ハーフブロック描画、多言語 CLI。
- `install.sh`: Fedora、Debian/Ubuntu、Arch Linux、openSUSE、macOS に対応したユニバーサル Plug & Play インストーラー。
- `build_packages.sh`: `PyInstaller` によるスタンドアロンバイナリ、`.deb`、`.rpm`、`PKGBUILD` パッケージの自動ビルドスクリプト。
- `pyproject.toml`: `pipx install .` および `pip install --user .` をサポートする現代的なパッケージ定義。

### ガイドライン
- **重い依存関係の禁止**: Luma は軽量かつプラグ＆プレイを保ちます。Pillow (`PIL`) と標準ライブラリのみに依存してください。OpenCV 等の重いライブラリは使用しません。
- **ターミナルの美しさ**: すべての機能はターミナルでの最高の視覚的再現性を追求してください。
- **多言語サポート**: 新しい CLI オプションやメッセージを追加する場合は、`TRANSLATIONS` 辞書の7言語すべて (`en`, `es`, `pt`, `ru`, `ja`, `de`, `ko`) を更新してください。

ターミナルグラフィックのハッキングをお楽しみください！ 🎨
