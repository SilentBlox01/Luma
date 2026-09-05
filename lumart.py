#!/usr/bin/env python3
import argparse
import sys
import locale
import os
try:
    from PIL import Image, ImageEnhance, ImageOps, ImageFilter
except ImportError:
    import subprocess
    import shutil
    # ¿Cómo coño alguien pretende renderizar imágenes sin Pillow? Intentemos salvarle el pellejo antes de que llore.
    print("[luma] Pillow no está instalado. ¿En qué cueva vives? Arreglando el desastre...")
    installed = False
    
    # 1. Intentar pip con --user y --break-system-packages (al carajo con PEP 668 y los puristas de Python)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--user", "--break-system-packages", "-q"])
        installed = True
    except Exception:
        pass

    # 2. Pip estándar de usuario
    if not installed:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
            installed = True
        except Exception:
            pass

    # 3. Gestores de paquetes nativos del sistema
    if not installed:
        if shutil.which("dnf"):  # Fedora / RHEL (por qué Red Hat nos odia tanto)
            try:
                subprocess.check_call(["sudo", "dnf", "install", "-y", "python3-pillow"])
                installed = True
            except Exception:
                pass
        elif shutil.which("apt-get"):  # Debian / Ubuntu (el viejo y confiable apt que te aguanta todo)
            try:
                subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3-pil"])
                installed = True
            except Exception:
                pass
        elif shutil.which("pacman"):  # Arch Linux (sí, ya sabemos que usas Arch btw y te compilas hasta el café)
            try:
                subprocess.check_call(["sudo", "pacman", "-S", "--noconfirm", "python-pillow"])
                installed = True
            except Exception:
                pass

    if not installed:
        print("\n❌ [ERROR] No se pudo instalar Pillow de forma automática.")
        print("Por favor instálalo manualmente con el gestor de tu sistema:")
        print("  • Fedora/RHEL:   sudo dnf install python3-pillow")
        print("  • Ubuntu/Debian: sudo apt install python3-pil")
        print("  • Arch Linux:    sudo pacman -S python-pillow")
        print("  • Python Pip:    pip install --user Pillow")
        sys.exit(1)

    from PIL import Image, ImageEnhance, ImageOps, ImageFilter

VERSION = "2.1.2"
GITHUB_REPO = "SilentBlox01/Luma"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/lumart.py"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# Rampa de densidad ASCII calibrada para percepción tonal uniforme
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Paleta de colores predefinidos para la funcionalidad de intercambio (--swap)
COLOR_MAP = {
    "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "purple": (128, 0, 128), 
    "pink": (255, 192, 203), "cyan": (0, 255, 255), 
    "orange": (255, 165, 0), "white": (255, 255, 255),
    "black": (0, 0, 0), "gray": (128, 128, 128), "magenta": (255, 0, 255),
    "blurple": (88, 101, 242) # Tono Discord Blurple clásico
}

# Diccionario de localizaciones para soporte multilingüe
TRANSLATIONS = {
    "en": {
        "pillow_not_found": "[luma] Pillow not found. Installing dependencies...",
        "usage": "Usage: lumart [options] <image_path>\n\nTry 'lumart --help' if you're too lazy to read docs.",
        "desc": "Lumart - Terminal Art Engine made by and for humans",
        "help_help": "Show this help message and exit.",
        "help_version": "Show program's version, system diagnostics, and engine status.",
        "help_image_path": "Path to the input image file (works best with transparent backgrounds).",
        "help_width": "Width of the output ASCII art (in characters). Default: 90",
        "help_engine": "Select rendering engine: 'color' (default), 'mono' (B&W), 'manga', or 'sketch'.",
        "help_color": "Output ASCII art in color (Color Engine).",
        "help_no_color": "Disable color output and use B&W engine.",
        "help_invert": "Invert the ASCII characters (useful for dark terminals).",
        "help_output": "Save the ASCII art to a file instead of printing to the console.",
        "help_binary": "Use only 1s and 0s for the ASCII characters.",
        "help_blocks": "Use half-blocks (Color) or 2x2 Quadrant HD blocks (B&W) for high resolution.",
        "help_braille": "Use Braille characters for smooth edges and high resolution shape (overrides binary).",
        "help_raw_colors": "Disable enhanced color processing and use the original raw image colors.",
        "help_os_style": "Use classic Neofetch/OS style characters (dots, letters, shapes).",
        "help_swap": "Swap colors using names (e.g. --swap purple pink blue red). Must provide an even number of arguments.",
        "help_dither": "Dithering algorithm for B&W shading: 'atkinson' (default), 'floyd', 'bayer', or 'none'.",
        "help_manga": "Authentic Manga/Anime style (clean DoG lineart, 8x8 Bayer screentone).",
        "help_sketch": "Pure line art sketch mode (clean contours, no screentone or background noise).",
        "help_lang": "Force a specific language (en, es, pt, ru, ja, de, ko).",
        "error_open": "❌ Where the hell is the image? Could not open it: {}",
        "error_swap": "❌ Pass pairs of colors to --swap damn it (e.g. --swap purple pink). I can't read your mind.",
        "saved_to": "ASCII art saved to {}",
        "error_save": "❌ Failed to save that damn file: {}",
        "lang_success": "Language successfully set to '{}'.",
        "lang_error": "❌ Error: Language '{}' is not supported, stop making things up.",
        "help_update": "Check for updates without installing (-u, --update, --check-update).",
        "help_upgrade": "Download and install the latest update with interactive selector (-uu, --upgrade).",
        "help_downgrade": "Roll back to previous or choose version from interactive menu (-dg, --downgrade [VER]).",
        "update_checking": "🔍 Checking for updates...",
        "update_already_latest": "✅ Luma is already up to date (v{}).",
        "update_available": "💡 New version available: v{} (current: v{}).\n   To install it, run: lumart -uu (or lumart --upgrade)",
        "update_downloading": "⬇️  Downloading and installing Luma v{}...",
        "update_success": "🎉 Successfully updated Luma from v{} to v{}!",
        "update_error": "❌ Error checking or applying updates: {}",
        "update_permission_error": "⚠️  Permission denied updating {}. Slap sudo on it: sudo lumart -uu",
        "update_notice": "💡 A new version of Luma is available: v{} (run 'lumart -uu' to upgrade)",
        "downgrade_checking": "🔍 Preparing to roll back version...",
        "downgrade_success": "⏪ Successfully rolled back Luma to v{}!",
        "downgrade_error": "❌ Error rolling back: {}",
        "downgrade_no_backup": "❌ No backup or previous release found to roll back to.",
    },
    "es": {
        "pillow_not_found": "[luma] Pillow no encontrado. Instalando dependencias...",
        "usage": "Uso: lumart [opciones] <ruta_imagen>\n\nIntenta 'lumart --help' si te da pereza leer la documentación.",
        "desc": "Lumart - Motor de Arte de Terminal hecho por y para humanos",
        "help_help": "Mostrar este mensaje de ayuda y salir.",
        "help_version": "Mostrar versión del programa, diagnóstico del sistema y estado de aceleración.",
        "help_image_path": "Ruta al archivo de imagen de entrada (funciona mejor con fondos transparentes).",
        "help_width": "Ancho del arte ASCII de salida (en caracteres). Por defecto: 90",
        "help_engine": "Seleccionar motor de renderizado: 'color' (por defecto), 'mono', 'manga' o 'sketch'.",
        "help_color": "Generar arte ASCII en color (Motor de Color).",
        "help_no_color": "Desactivar salida de color y usar motor blanco y negro.",
        "help_invert": "Invertir los caracteres ASCII (útil para terminales oscuras).",
        "help_output": "Guardar el arte ASCII en un archivo en lugar de imprimirlo en consola.",
        "help_binary": "Usar solo 1s y 0s para los caracteres ASCII.",
        "help_blocks": "Usar medio-bloques (Color) o bloques cuadrantes 2x2 HD (B&W) para alta resolución.",
        "help_braille": "Usar caracteres Braille para bordes suaves y formas de alta resolución.",
        "help_raw_colors": "Desactiva el realce de color y utiliza los colores originales sin procesar.",
        "help_os_style": "Usar caracteres clásicos estilo Neofetch/OS (puntos, letras, formas).",
        "help_swap": "Intercambiar colores por nombre (ej. --swap purple pink blue red). Debe ser un número par de argumentos.",
        "help_dither": "Algoritmo de tramado: 'atkinson' (por defecto), 'floyd', 'bayer' o 'none'.",
        "help_manga": "Estilo Manga/Anime auténtico (trazos limpios DoG, sombreado screentone 8x8 Bayer).",
        "help_sketch": "Modo boceto de trazo puro (contornos limpios sin sombreado ni ruido de fondo).",
        "help_lang": "Forzar un idioma específico (en, es, pt, ru, ja, de, ko).",
        "error_open": "❌ ¿Dónde coño está la imagen? No se pudo abrir: {}",
        "error_swap": "❌ Pásame pares de colores a --swap (ej: --swap purple pink). No leo mentes.",
        "saved_to": "Arte ASCII guardado en {}",
        "error_save": "❌ No se pudo guardar esa vaina en el archivo: {}",
        "lang_success": "Idioma cambiado exitosamente a '{}'.",
        "lang_error": "❌ Error: El idioma '{}' no existe ni en tus sueños.",
        "help_update": "Comprobar si hay actualizaciones sin instalar (-u, --update, --check-update).",
        "help_upgrade": "Descargar e instalar la actualización con selector interactivo (-uu, --upgrade).",
        "help_downgrade": "Volver a la versión previa o elegir en menú interactivo (-dg, --downgrade [VER]).",
        "update_checking": "🔍 Buscando actualizaciones...",
        "update_already_latest": "✅ Luma ya está en la versión más reciente (v{}).",
        "update_available": "💡 ¡Nueva versión disponible: v{} (actual: v{})!\n   Para instalarla, ejecuta: lumart -uu (o lumart --upgrade)",
        "update_downloading": "⬇️  Descargando e instalando Luma v{}...",
        "update_success": "🎉 ¡Luma actualizado exitosamente de v{} a v{}!",
        "update_error": "❌ Error al verificar o aplicar actualizaciones: {}",
        "update_permission_error": "⚠️  Permiso denegado al actualizar {}. Métele sudo carajo, no seas tímido: sudo lumart -uu",
        "update_notice": "💡 Nueva versión de Luma disponible: v{} (ejecuta 'lumart -uu' para actualizar)",
        "downgrade_checking": "🔍 Preparando para volver a la versión anterior...",
        "downgrade_success": "⏪ ¡Luma ha vuelto a la versión v{} exitosamente!",
        "downgrade_error": "❌ Error al volver a la versión anterior: {}",
        "downgrade_no_backup": "❌ No se encontró copia de seguridad ni versión previa disponible.",
    },
    "pt": {
        "pillow_not_found": "[luma] Pillow não encontrado. Instalando dependências...",
        "usage": "Uso: lumart [opções] <caminho_imagem>\n\nTente 'lumart --help' para mais opções.",
        "desc": "Lumart - Motor de Arte de Terminal",
        "help_help": "Mostrar esta mensagem de ajuda e sair.",
        "help_version": "Mostrar o número da versão do programa, diagnóstico e status do motor.",
        "help_image_path": "Caminho para o arquivo de imagem de entrada (funciona melhor com fundos transparentes).",
        "help_width": "Largura da arte ASCII de saída (em caracteres). Padrão: 90",
        "help_engine": "Selecionar motor de renderização: 'color' (padrão), 'mono', 'manga' ou 'sketch'.",
        "help_color": "Gerar arte ASCII em cores (Motor de Cores).",
        "help_no_color": "Desativar saída colorida e usar motor preto e branco.",
        "help_invert": "Inverter os caracteres ASCII (útil para terminais escuros).",
        "help_output": "Salvar a arte ASCII em um arquivo em vez de imprimir no console.",
        "help_binary": "Usar apenas 1s e 0s para os caracteres ASCII.",
        "help_blocks": "Usar meios-blocos ou blocos quadrantes 2x2 para alta resolução.",
        "help_braille": "Usar caracteres Braille para bordas suaves e formas de alta resolução.",
        "help_raw_colors": "Desativar o realce de cor e usar as cores originais sem processamento.",
        "help_os_style": "Usar caracteres clássicos estilo Neofetch/OS (pontos, letras, formas).",
        "help_swap": "Trocar cores usando nomes (ex: --swap purple pink blue red). Deve fornecer um número par de argumentos.",
        "help_dither": "Algoritmo de pontilhamento: 'atkinson' (padrão), 'floyd', 'bayer' ou 'none'.",
        "help_manga": "Estilo Manga/Anime autêntico (traços limpos DoG, sombreamento retícula 8x8).",
        "help_sketch": "Modo esboço de linha pura (contornos limpos sem retícula).",
        "help_lang": "Forçar um idioma específico (en, es, pt, ru, ja, de, ko).",
        "error_open": "Erro ao abrir a imagem: {}",
        "error_swap": "Erro: --swap requer pares de cores (ex: --swap purple pink).",
        "saved_to": "Arte ASCII salva em {}",
        "error_save": "Erro ao salvar o arquivo: {}",
        "lang_success": "Idioma alterado com sucesso para '{}'.",
        "lang_error": "Erro: O idioma '{}' não é suportado.",
        "help_update": "Verificar se há atualizações sem instalar (-u, --update).",
        "help_upgrade": "Baixar e instalar a versão mais recente (-uu, --upgrade).",
        "help_downgrade": "Reverter para a versão anterior ou escolher em menu (-dg, --downgrade [VER]).",
        "update_checking": "🔍 Verificando atualizações...",
        "update_already_latest": "✅ O Luma já está na versão mais recente (v{}).",
        "update_available": "💡 Nova versão disponível: v{} (atual: v{}).\n   Para instalar, execute: lumart -uu (ou lumart --upgrade)",
        "update_downloading": "⬇️  Baixando e instalando Luma v{}...",
        "update_success": "🎉 Luma atualizado com sucesso de v{} para v{}!",
        "update_error": "❌ Erro ao verificar atualizações: {}",
        "update_permission_error": "⚠️  Permissão negada ao atualizar {}. Tente executar: sudo lumart -uu",
        "update_notice": "💡 Nova versão do Luma disponível: v{} (execute 'lumart -uu' para atualizar)",
        "downgrade_checking": "🔍 Preparando para reverter a versão...",
        "downgrade_success": "⏪ Luma revertido para v{} com sucesso!",
        "downgrade_error": "❌ Erro ao reverter: {}",
        "downgrade_no_backup": "❌ Nenhum backup ou versão anterior encontrada.",
    },
    "ru": {
        "pillow_not_found": "[luma] Pillow не найден. Установка зависимостей...",
        "usage": "Использование: lumart [опции] <путь_к_изображению>\n\nПопробуйте 'lumart --help' для дополнительных опций.",
        "desc": "Lumart - Движок терминального искусства",
        "help_help": "Показать это справочное сообщение и выйти.",
        "help_version": "Показать версию программы, диагностику системы и статус движка.",
        "help_image_path": "Путь к исходному файлу изображения (лучше всего работает с прозрачным фоном).",
        "help_width": "Ширина выходного ASCII-арта (в символах). По умолчанию: 90",
        "help_engine": "Выбрать движок рендеринга: 'color' (по умолчанию), 'mono', 'manga' или 'sketch'.",
        "help_color": "Выводить ASCII-арт в цвете (Цветовой движок).",
        "help_no_color": "Отключить цветной вывод и использовать черно-белый движок.",
        "help_invert": "Инвертировать символы ASCII (полезно для темных терминалов).",
        "help_output": "Сохранить ASCII-арт в файл вместо вывода в консоль.",
        "help_binary": "Использовать только 1 и 0 для символов ASCII.",
        "help_blocks": "Использовать полублоки или 2x2 квадранты для высокого разрешения.",
        "help_braille": "Использовать шрифт Брайля для сглаженных краев и высокого разрешения.",
        "help_raw_colors": "Отключить улучшение цветов и использовать исходные цвета без обработки.",
        "help_os_style": "Использовать классические символы в стиле Neofetch/OS (точки, буквы, формы).",
        "help_swap": "Менять цвета по названию (напр. --swap purple pink blue red). Должно быть четное количество аргументов.",
        "help_dither": "Алгоритм дизеринга: 'atkinson' (по умолчанию), 'floyd', 'bayer' или 'none'.",
        "help_manga": "Стиль манги/аниме (чистый лайн-арт DoG, скринтоны 8x8).",
        "help_sketch": "Режим чистого эскиза (четкие контуры без растра).",
        "help_lang": "Принудительно установить язык (en, es, pt, ru, ja, de, ko).",
        "error_open": "Ошибка при открытии изображения: {}",
        "error_swap": "Ошибка: --swap требует пары цветов (напр. --swap purple pink).",
        "saved_to": "ASCII-арт сохранен в {}",
        "error_save": "Ошибка при сохранении в файл: {}",
        "lang_success": "Язык успешно изменен на '{}'.",
        "lang_error": "Ошибка: Язык '{}' не поддерживается.",
        "help_update": "Проверить наличие обновлений без установки (-u, --update).",
        "help_upgrade": "Скачать и установить последнее обновление (-uu, --upgrade).",
        "help_downgrade": "Откатиться к предыдущей версии или выбрать в меню (-dg, --downgrade [VER]).",
        "update_checking": "🔍 Проверка обновлений...",
        "update_already_latest": "✅ Luma уже обновлена до последней версии (v{}).",
        "update_available": "💡 Доступна новая версия: v{} (текущая: v{}).\n   Чтобы установить, запустите: lumart -uu (или lumart --upgrade)",
        "update_downloading": "⬇️  Загрузка и установка Luma v{}...",
        "update_success": "🎉 Luma успешно обновлена с v{} до v{}!",
        "update_error": "❌ Ошибка при проверке обновлений: {}",
        "update_permission_error": "⚠️  Отказано в доступе при обновлении {}. Попробуйте: sudo lumart -uu",
        "update_notice": "💡 Доступна новая версия Luma: v{} (запустите 'lumart -uu' для обновления)",
        "downgrade_checking": "🔍 Подготовка к откату версии...",
        "downgrade_success": "⏪ Luma успешно откачена до v{}!",
        "downgrade_error": "❌ Ошибка при откате: {}",
        "downgrade_no_backup": "❌ Резервная копия или предыдущая версия не найдены.",
    },
    "ja": {
        "pillow_not_found": "[luma] Pillowが見つかりません。依存関係をインストールしています...",
        "usage": "使用法: lumart [オプション] <画像パス>\n\n詳細なオプションについては 'lumart --help' をお試しください。",
        "desc": "Lumart - ターミナルアートエンジン",
        "help_help": "このヘルプメッセージを表示して終了します。",
        "help_version": "プログラムのバージョン、診断情報、エンジン状態を表示して終了します。",
        "help_image_path": "入力画像ファイルへのパス（透明な背景が最適です）。",
        "help_width": "出力するASCIIアートの幅（文字数）。デフォルト: 90",
        "help_engine": "レンダリングエンジンの選択: 'color' (デフォルト), 'mono', 'manga', 'sketch'。",
        "help_color": "ASCIIアートをカラーで出力します (カラーエンジン)。",
        "help_no_color": "カラー出力を無効にし、白黒エンジンを使用します。",
        "help_invert": "ASCII文字を反転します（暗いターミナルで便利です）。",
        "help_output": "コンソールに出力する代わりに、ASCIIアートをファイルに保存します。",
        "help_binary": "ASCII文字として1と0のみを使用します。",
        "help_blocks": "高解像度のためにハーフブロックまたは2x2ブロックを使用します。",
        "help_braille": "滑らかなエッジと高解像度の形状のために点字文字を使用します。",
        "help_raw_colors": "カラー補正を無効にし、元の画像の色を処理なしで使用します。",
        "help_os_style": "クラシックなNeofetch/OSスタイルの文字（ドット、文字、図形）を使用します。",
        "help_swap": "名前を使用して色を交換します（例: --swap purple pink blue red）。偶数個の引数を指定する必要があります。",
        "help_dither": "ディザリングアルゴリズム: 'atkinson' (デフォルト), 'floyd', 'bayer', 'none'。",
        "help_manga": "本物のマンガ/アニメスタイル (DoG線画、8x8スクリーントーン)。",
        "help_sketch": "純粋な線画スケッチモード（スクリーントーンなし、クリーンな輪郭）。",
        "help_lang": "特定の言語を強制します（en, es, pt, ru, ja, de, ko）。",
        "error_open": "画像を開く際のエラー: {}",
        "error_swap": "エラー: --swapには色のペアが必要です（例: --swap purple pink）。",
        "saved_to": "ASCIIアートを {} に保存しました",
        "error_save": "ファイルへの保存エラー: {}",
        "lang_success": "言語が正常に '{}' に変更されました。",
        "lang_error": "エラー: 言語 '{}' はサポートされていません。",
        "help_update": "インストールせずに更新を確認します (-u, --update)。",
        "help_upgrade": "最新の更新をダウンロードしてインストールします (-uu, --upgrade)。",
        "help_downgrade": "前のバージョンまたは対話型メニューからロールバックします (-dg, --downgrade [VER])。",
        "update_checking": "🔍 アップデートを確認中...",
        "update_already_latest": "✅ Lumaはすでに最新バージョンです（v{}）。",
        "update_available": "💡 新しいバージョンが利用可能です: v{} (現在: v{})。\n   インストールするには実行してください: lumart -uu (または lumart --upgrade)",
        "update_downloading": "⬇️  Luma v{} をダウンロードしてインストール中...",
        "update_success": "🎉 Lumaを v{} から v{} に正常に更新しました！",
        "update_error": "❌ アップデートエラー: {}",
        "update_permission_error": "⚠️  {} の更新でアクセスが拒否されました。sudo lumart -uu を実行してください",
        "update_notice": "💡 Lumaの新しいバージョンが利用可能です: v{} ('lumart -uu' で更新)",
        "downgrade_checking": "🔍 バージョンのロールバックを準備中...",
        "downgrade_success": "⏪ Lumaを v{} に正常にロールバックしました！",
        "downgrade_error": "❌ ロールバックエラー: {}",
        "downgrade_no_backup": "❌ バックアップまたは以前のバージョンが見つかりません。",
    },
    "de": {
        "pillow_not_found": "[luma] Pillow nicht gefunden. Installiere Abhängigkeiten...",
        "usage": "Verwendung: lumart [Optionen] <bildpfad>\n\nVersuche 'lumart --help' für weitere Optionen.",
        "desc": "Lumart - Terminal-Kunst-Engine",
        "help_help": "Diese Hilfemeldung anzeigen und beenden.",
        "help_version": "Versionsnummer, Systemdiagnose und Engine-Status anzeigen.",
        "help_image_path": "Pfad zur Eingabebilddatei (funktioniert am besten mit transparentem Hintergrund).",
        "help_width": "Breite der ASCII-Kunst (in Zeichen). Standard: 90",
        "help_engine": "Rendering-Engine auswählen: 'color' (Standard), 'mono', 'manga' oder 'sketch'.",
        "help_color": "ASCII-Kunst in Farbe ausgeben (Farb-Engine).",
        "help_no_color": "Farbausgabe deaktivieren und Schwarz-Weiß-Engine verwenden.",
        "help_invert": "ASCII-Zeichen umkehren (nützlich für dunkle Terminals).",
        "help_output": "ASCII-Kunst in einer Datei speichern, anstatt sie auf der Konsole auszugeben.",
        "help_binary": "Nur 1en und 0en für die ASCII-Zeichen verwenden.",
        "help_blocks": "Halbblöcke oder 2x2 Quadrant-Blöcke für hohe Auflösung verwenden.",
        "help_braille": "Braille-Zeichen für weiche Kanten und hohe Auflösung verwenden.",
        "help_raw_colors": "Farbverbesserung deaktivieren und die ursprünglichen Bildfarben verwenden.",
        "help_os_style": "Klassische Neofetch/OS-Zeichen (Punkte, Buchstaben, Formen) verwenden.",
        "help_swap": "Farben nach Name tauschen (z.B. --swap purple pink blue red). Es muss eine gerade Anzahl von Argumenten angegeben werden.",
        "help_dither": "Dithering-Algorithmus: 'atkinson' (Standard), 'floyd', 'bayer' oder 'none'.",
        "help_manga": "Authentischer Manga/Anime-Stil (saubere DoG-Linienführung, 8x8 Rastertönung).",
        "help_sketch": "Reiner Strichzeichnungsmodus (saubere Konturen ohne Rasterung).",
        "help_lang": "Eine bestimmte Sprache erzwingen (en, es, pt, ru, ja, de, ko).",
        "error_open": "Fehler beim Öffnen des Bildes: {}",
        "error_swap": "Fehler: --swap benötigt Farbpaare (z.B. --swap purple pink).",
        "saved_to": "ASCII-Kunst in {} gespeichert",
        "error_save": "Fehler beim Speichern in Datei: {}",
        "lang_success": "Sprache erfolgreich auf '{}' geändert.",
        "lang_error": "Fehler: Sprache '{}' wird nicht unterstützt.",
        "help_update": "Nach Updates suchen, ohne zu installieren (-u, --update).",
        "help_upgrade": "Das neueste Update herunterladen und installieren (-uu, --upgrade).",
        "help_downgrade": "Auf vorherige Version zurücksetzen oder im Menü wählen (-dg, --downgrade [VER]).",
        "update_checking": "🔍 Suche nach Updates...",
        "update_already_latest": "✅ Luma ist bereits auf dem neuesten Stand (v{}).",
        "update_available": "💡 Neue Version verfügbar: v{} (aktuell: v{}).\n   Zum Installieren ausführen: lumart -uu (oder lumart --upgrade)",
        "update_downloading": "⬇️  Lade Luma v{} herunter und installiere...",
        "update_success": "🎉 Luma erfolgreich von v{} auf v{} aktualisiert!",
        "update_error": "❌ Fehler beim Suchen nach Updates: {}",
        "update_permission_error": "⚠️  Keine Berechtigung zum Aktualisieren von {}. Versuchen Sie: sudo lumart -uu",
        "update_notice": "💡 Eine neue Luma-Version ist verfügbar: v{} (führe 'lumart -uu' aus)",
        "downgrade_checking": "🔍 Rollback der Version wird vorbereitet...",
        "downgrade_success": "⏪ Luma erfolgreich auf v{} zurückgesetzt!",
        "downgrade_error": "❌ Fehler beim Zurücksetzen: {}",
        "downgrade_no_backup": "❌ Kein Backup oder vorherige Version gefunden.",
    },
    "ko": {
        "pillow_not_found": "[luma] Pillow를 찾을 수 없습니다. 종속성을 설치하는 중...",
        "usage": "사용법: lumart [옵션] <이미지_경로>\n\n자세한 옵션은 'lumart --help'를 시도해 보세요.",
        "desc": "Lumart - 터미널 아트 엔진",
        "help_help": "이 도움말 메시지를 표시하고 종료합니다.",
        "help_version": "프로그램의 버전 번호, 시스템 진단 및 엔진 상태를 표시합니다.",
        "help_image_path": "입력 이미지 파일의 경로입니다 (투명한 배경이 가장 좋습니다).",
        "help_width": "출력 ASCII 아트의 너비(문자 수)입니다. 기본값: 90",
        "help_engine": "렌더링 엔진 선택: 'color' (기본값), 'mono', 'manga' 또는 'sketch'.",
        "help_color": "컬러로 ASCII 아트를 출력합니다 (컬러 엔진).",
        "help_no_color": "컬러 출력을 비활성화하고 흑백 엔진을 사용합니다.",
        "help_invert": "ASCII 문자를 반전시킵니다(어두운 터미널에 유용).",
        "help_output": "콘솔에 출력하는 대신 ASCII 아트를 파일에 저장합니다.",
        "help_binary": "ASCII 문자에 1과 0만 사용합니다.",
        "help_blocks": "고해상도를 위해 하프 블록 또는 2x2 쿼드런트 블록을 사용합니다.",
        "help_braille": "부드러운 가장자리와 고해상도 모양을 위해 점자 문자를 사용합니다.",
        "help_raw_colors": "컬러 향상을 비활성화하고 처리 없이 원래 이미지 색상을 사용합니다.",
        "help_os_style": "클래식 Neofetch/OS 스타일 문자(점, 글자, 도형)를 사용합니다.",
        "help_swap": "이름을 사용하여 색상을 교환합니다(예: --swap purple pink blue red). 짝수 개의 인수를 제공해야 합니다.",
        "help_dither": "디더링 알고리즘: 'atkinson' (기본값), 'floyd', 'bayer' 또는 'none'.",
        "help_manga": "정통 만화/애니메이션 스타일 (깔끔한 DoG 라인아트, 8x8 스크린톤).",
        "help_sketch": "순수 선화 스케치 모드 (스크린톤 없는 깔끔한 윤곽선).",
        "help_lang": "특정 언어를 강제 적용합니다(en, es, pt, ru, ja, de, ko).",
        "error_open": "이미지 열기 오류: {}",
        "error_swap": "오류: --swap에는 색상 쌍이 필요합니다(예: --swap purple pink).",
        "saved_to": "ASCII 아트를 {}에 저장했습니다.",
        "error_save": "파일 저장 오류: {}",
        "lang_success": "언어가 '{}'(으)로 성공적으로 변경되었습니다.",
        "lang_error": "오류: 언어 '{}'은(는) 지원되지 않습니다.",
        "help_update": "설치하지 않고 업데이트를 확인합니다 (-u, --update).",
        "help_upgrade": "최신 업데이트를 대화형 메뉴로 다운로드하고 설치합니다 (-uu, --upgrade).",
        "help_downgrade": "이전 버전으로 롤백하거나 대화형 메뉴에서 선택합니다 (-dg, --downgrade [VER]).",
        "update_checking": "🔍 업데이트 확인 중...",
        "update_already_latest": "✅ Luma가 이미 최신 버전입니다 (v{}).",
        "update_available": "💡 새 버전을 사용할 수 있습니다: v{} (현재: v{}).\n   설치하려면 다음을 실행하세요: lumart -uu (또는 lumart --upgrade)",
        "update_downloading": "⬇️  Luma v{} 다운로드 및 설치 중...",
        "update_success": "🎉 Luma가 v{}에서 v{}로 성공적으로 업데이트되었습니다!",
        "update_error": "❌ 업데이트 오류: {}",
        "update_permission_error": "⚠️  {} 업데이트 권한이 거부되었습니다. sudo lumart -uu 를 실행해 보세요",
        "update_notice": "💡 새로운 Luma 버전을 사용할 수 있습니다: v{} ('lumart -uu' 실행하여 업데이트)",
        "downgrade_checking": "🔍 버전 롤백 준비 중...",
        "downgrade_success": "⏪ Luma를 v{} 버전으로 성공적으로 롤백했습니다!",
        "downgrade_error": "❌ 롤백 오류: {}",
        "downgrade_no_backup": "❌ 백업 또는 이전 버전을 찾을 수 없습니다.",
    }
}

CURRENT_LANG = "en"

def set_language(lang_code):
    global CURRENT_LANG
    if lang_code in TRANSLATIONS:
        CURRENT_LANG = lang_code
    elif lang_code and lang_code.startswith("es"):
        CURRENT_LANG = "es"
    elif lang_code and lang_code.startswith("pt"):
        CURRENT_LANG = "pt"
    elif lang_code and lang_code.startswith("ru"):
        CURRENT_LANG = "ru"
    elif lang_code and lang_code.startswith("ja"):
        CURRENT_LANG = "ja"
    elif lang_code and lang_code.startswith("de"):
        CURRENT_LANG = "de"
    elif lang_code and lang_code.startswith("ko"):
        CURRENT_LANG = "ko"
    else:
        CURRENT_LANG = "en"

def _(key, *args):
    text = TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))
    if args:
        return text.format(*args)
    return text

# Gestor de idiomas: autodetección inteligente basada en entorno y locale
def auto_detect_language():
    try:
        # 1. Revisar variables de entorno estándar primero
        for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
            val = os.environ.get(var)
            if val:
                code = val.split(".")[0].split("_")[0].lower()
                if code in TRANSLATIONS:
                    set_language(code)
                    return code
        # 2. Revisar configuración regional del sistema
        lang, _ = locale.getdefaultlocale()
        if lang:
            code = lang[:2].lower()
            if code in TRANSLATIONS:
                set_language(code)
                return code
    except Exception:
        pass
    set_language("en")
    return "en"

def is_light_terminal():
    """Autodetecta si la terminal tiene fondo claro revisando COLORFGBG."""
    colorfgbg = os.environ.get("COLORFGBG", "")
    if colorfgbg and ";" in colorfgbg:
        parts = colorfgbg.split(";")
        try:
            bg = int(parts[-1])
            # Códigos ANSI para fondos claros: 7 (blanco/gris claro), 15 (blanco brillante)
            # Si alguien usa fondo blanco en 2026, invertimos para salvarle las retinas al psicópata
            if bg in (7, 15):
                return True
        except ValueError:
            pass
    return False

def apply_color_swap(image, swap_args):
    # Intercambio dinámico de colores en la imagen
    if not swap_args or len(swap_args) % 2 != 0:
        return image
        
    swaps = []
    # Verificamos que los argumentos vengan en pares de origen y destino
    for i in range(0, len(swap_args), 2):
        src_name = swap_args[i].lower()
        dst_name = swap_args[i+1].lower()
        if src_name in COLOR_MAP and dst_name in COLOR_MAP:
            swaps.append((COLOR_MAP[src_name], COLOR_MAP[dst_name]))
            
    if not swaps:
        return image
        
    img = image.convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    # Umbral de distancia euclidiana de color calibrado para sustituciones precisas
    THRESHOLD = 150
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0: continue
            
            for src_rgb, dst_rgb in swaps:
                # Pitágoras revolcándose en su tumba al ver su teorema usado para cambiarle el pelo a monas chinas
                dist = ((r - src_rgb[0])**2 + (g - src_rgb[1])**2 + (b - src_rgb[2])**2)**0.5
                if dist < THRESHOLD:
                    # Ajuste de brillo relativo para conservar sombras y luces de la imagen original
                    orig_brightness = max((r + g + b) / 765.0, 0.05)
                    dst_brightness = max((dst_rgb[0] + dst_rgb[1] + dst_rgb[2]) / 765.0, 0.05)
                    
                    ratio = orig_brightness / dst_brightness
                    new_r = min(255, int(dst_rgb[0] * ratio))
                    new_g = min(255, int(dst_rgb[1] * ratio))
                    new_b = min(255, int(dst_rgb[2] * ratio))
                    
                    pixels[x, y] = (new_r, new_g, new_b, a)
                    break
                    
    return img

# Matriz de Bayer 4x4: algoritmo clásico de difuminado ordenado (dithering) estilo retro
BAYER_MATRIX = [
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5]
]

def apply_bayer_dither(image):
    """Aplica tramado ordenado con matriz de Bayer para un estilo gráfico retro."""
    width, height = image.size
    has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    img = image.convert("RGBA") if has_alpha else image.convert("RGB")
    
    pixels = img.load()
    # Intensidad del tramado calibrada para contraste óptimo
    spread = 64
    
    for y in range(height):
        for x in range(width):
            # Normalizado al rango [-0.5, 0.5] para balancear luces y sombras sin saturar
            factor = (BAYER_MATRIX[y % 4][x % 4] / 16.0) - 0.5
            offset = int(factor * spread)
            
            p = pixels[x, y]
            r = max(0, min(255, p[0] + offset))
            g = max(0, min(255, p[1] + offset))
            b = max(0, min(255, p[2] + offset))
            
            if has_alpha:
                pixels[x, y] = (r, g, b, p[3])
            else:
                pixels[x, y] = (r, g, b)
                
    return img

def render_python_sketch(image, width, invert=False):
    """Fallback en Python para modo Sketch (Diferencia de Gaussianas pura, contornos sin tramado)."""
    aspect = image.height / image.width
    scaled_w = width * 2
    scaled_h = int(scaled_w * aspect * 0.5 * 2.0)
    scaled_h += (4 - scaled_h % 4) % 4
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    img_scaled = image.convert("RGBA").resize((scaled_w, scaled_h), resample=resample_filter)
    
    gray = img_scaled.convert("L")
    g1 = gray.filter(ImageFilter.GaussianBlur(0.7))
    g2 = gray.filter(ImageFilter.GaussianBlur(1.8))
    
    g1_p = list(g1.getdata())
    g2_p = list(g2.getdata())
    alpha_p = list(img_scaled.split()[3].getdata())
    
    dot_map = [
        [0x01, 0x08],
        [0x02, 0x10],
        [0x04, 0x20],
        [0x40, 0x80]
    ]
    
    lines = []
    for y in range(0, scaled_h, 4):
        chars = []
        for x in range(0, scaled_w, 2):
            braille_val = 0
            for dy in range(4):
                for dx in range(2):
                    cur_x = x + dx
                    cur_y = y + dy
                    if cur_x < scaled_w and cur_y < scaled_h:
                        idx = cur_y * scaled_w + cur_x
                        if alpha_p[idx] < 128:
                            continue
                        dog = g2_p[idx] - g1_p[idx]
                        is_on = (dog > 6.0) or (g1_p[idx] < 35)
                        if invert: is_on = not is_on
                        if is_on:
                            braille_val |= dot_map[dy][dx]
            chars.append(" " if braille_val == 0 else chr(0x2800 + braille_val))
        lines.append("".join(chars))
    return "\n".join(lines)

def render_python_manga(image, width, invert=False):
    """Fallback en Python para modo Manga Screentone 2.0 (DoG + 8x8 Bayer inteligente)."""
    aspect = image.height / image.width
    scaled_w = width * 2
    scaled_h = int(scaled_w * aspect * 0.5 * 2.0)
    scaled_h += (4 - scaled_h % 4) % 4
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    img_scaled = image.convert("RGBA").resize((scaled_w, scaled_h), resample=resample_filter)
    
    gray = img_scaled.convert("L")
    g1 = gray.filter(ImageFilter.GaussianBlur(0.7))
    g2 = gray.filter(ImageFilter.GaussianBlur(1.8))
    
    g1_p = list(g1.getdata())
    g2_p = list(g2.getdata())
    alpha_p = list(img_scaled.split()[3].getdata())
    
    bayer_8x8 = [
        [  0, 32,  8, 40,  2, 34, 10, 42 ],
        [ 48, 16, 56, 24, 50, 18, 58, 26 ],
        [ 12, 44,  4, 36, 14, 46,  6, 38 ],
        [ 60, 28, 52, 20, 62, 30, 54, 22 ],
        [  3, 35, 11, 43,  1, 33,  9, 41 ],
        [ 51, 19, 59, 27, 49, 17, 57, 25 ],
        [ 15, 47,  7, 39, 13, 45,  5, 37 ],
        [ 63, 31, 55, 23, 61, 29, 53, 21 ]
    ]
    
    dot_map = [
        [0x01, 0x08],
        [0x02, 0x10],
        [0x04, 0x20],
        [0x40, 0x80]
    ]
    
    lines = []
    for y in range(0, scaled_h, 4):
        chars = []
        for x in range(0, scaled_w, 2):
            braille_val = 0
            for dy in range(4):
                for dx in range(2):
                    cur_x = x + dx
                    cur_y = y + dy
                    if cur_x < scaled_w and cur_y < scaled_h:
                        idx = cur_y * scaled_w + cur_x
                        if alpha_p[idx] < 128:
                            continue
                        lum = g1_p[idx]
                        dog = g2_p[idx] - lum
                        ink = 255.0 - lum
                        is_on = False
                        if dog > 6.0:
                            is_on = True
                        elif ink > 215.0:
                            is_on = True
                        elif ink > 110.0:
                            thresh = (bayer_8x8[cur_y % 8][cur_x % 8] + 0.5) * (255.0 / 64.0)
                            if (ink - 50.0) >= thresh:
                                is_on = True
                        if invert: is_on = not is_on
                        if is_on:
                            braille_val |= dot_map[dy][dx]
            chars.append(" " if braille_val == 0 else chr(0x2800 + braille_val))
        lines.append("".join(chars))
    return "\n".join(lines)

def render_python_bw_quadrants(image, width, dither="atkinson", invert=False):
    """Fallback en Python para modo Bloques Cuadrantes HD (2x2 subpíxeles por celda en B&W)."""
    QUAD_BLOCKS = [
        " ", "▘", "▝", "▀",
        "▖", "▌", "▞", "▛",
        "▗", "▚", "▐", "▜",
        "▄", "▙", "▟", "█"
    ]
    aspect = image.height / image.width
    scaled_w = width * 2
    scaled_h = int(scaled_w * aspect * 0.5)
    scaled_h += (2 - scaled_h % 2) % 2
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    img_scaled = image.convert("RGBA").resize((scaled_w, scaled_h), resample=resample_filter)
    gray = img_scaled.convert("L")
    alpha = img_scaled.split()[3]
    
    gray_data = list(gray.getdata())
    alpha_data = list(alpha.getdata())
    
    buf = [float(255 - p) for p in gray_data]
    binary = [0] * len(buf)
    
    if dither in ("atkinson", "1", "true", "default"):
        for y in range(scaled_h):
            for x in range(scaled_w):
                idx = y * scaled_w + x
                old_val = buf[idx]
                new_val = 255 if old_val >= 128.0 else 0
                binary[idx] = new_val
                err = (old_val - new_val) / 8.0
                if x + 1 < scaled_w: buf[y * scaled_w + (x + 1)] += err
                if x + 2 < scaled_w: buf[y * scaled_w + (x + 2)] += err
                if y + 1 < scaled_h:
                    if x - 1 >= 0: buf[(y + 1) * scaled_w + (x - 1)] += err
                    buf[(y + 1) * scaled_w + x] += err
                    if x + 1 < scaled_w: buf[(y + 1) * scaled_w + (x + 1)] += err
                if y + 2 < scaled_h:
                    buf[(y + 2) * scaled_w + x] += err
    else:
        for i in range(len(buf)):
            binary[i] = 255 if buf[i] >= 128.0 else 0
            
    lines = []
    for y in range(0, scaled_h, 2):
        chars = []
        for x in range(0, scaled_w, 2):
            mask = 0
            idx_tl = y * scaled_w + x
            if alpha_data[idx_tl] >= 128 and (binary[idx_tl] > 0) != invert: mask |= 1
            if x + 1 < scaled_w:
                idx_tr = y * scaled_w + (x + 1)
                if alpha_data[idx_tr] >= 128 and (binary[idx_tr] > 0) != invert: mask |= 2
            if y + 1 < scaled_h:
                idx_bl = (y + 1) * scaled_w + x
                if alpha_data[idx_bl] >= 128 and (binary[idx_bl] > 0) != invert: mask |= 4
            if y + 1 < scaled_h and x + 1 < scaled_w:
                idx_br = (y + 1) * scaled_w + (x + 1)
                if alpha_data[idx_br] >= 128 and (binary[idx_br] > 0) != invert: mask |= 8
            chars.append(QUAD_BLOCKS[mask])
        lines.append("".join(chars))
    return "\n".join(lines)

def resize_image(image, new_width=90, is_blocks=False, is_braille=False):
    # Preservar la relación de aspecto original de la imagen
    width, height = image.size
    aspect_ratio = height / width
    
    # Filtro Lanczos de alta fidelidad para un remuestreo limpio y nítido
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    
    if is_braille:
        # Cada carácter Braille abarca una matriz de 2x4 puntos (2 de ancho x 4 de alto).
        # Multiplicamos el ancho por 2 y ajustamos la altura a múltiplos exactos de 4.
        target_pixel_width = new_width * 2
        target_pixel_height = int(target_pixel_width * aspect_ratio)
        target_pixel_height = target_pixel_height + (4 - target_pixel_height % 4) % 4
        return image.resize((target_pixel_width, target_pixel_height), resample=resample_filter)
    elif is_blocks:
        # Bloques de cuadrantes: 2x2 píxeles por celda.
        # Las fuentes de terminal son aproximadamente el doble de altas que de anchas (relación 1:2).
        # Aplicamos una compensación de 0.5 para mantener proporciones cuadradas.
        target_pixel_width = new_width * 2
        target_pixel_height = int(target_pixel_width * aspect_ratio * 0.5)
        target_pixel_height = target_pixel_height + (2 - target_pixel_height % 2) % 2
        return image.resize((target_pixel_width, target_pixel_height), resample=resample_filter)
    else:
        # ASCII tradicional: compensación vertical de 0.5 para celdas monoespaciadas
        new_height = int(new_width * aspect_ratio * 0.5)
        return image.resize((new_width, new_height), resample=resample_filter)

def get_ansi_color_code(r, g, b):
    # Secuencia ANSI TrueColor de 24 bits (16.7 millones de colores)
    return f"\033[38;2;{r};{g};{b}m"

def reset_ansi_color_code():
    # Restaurar atributos y estilos de color predeterminados de la terminal
    return "\033[0m"

def _color_dist_sq(c1, c2):
    """Distancia perceptual de color ponderada (aproximación redmean ajustada a la visión humana)."""
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    rmean = (c1[0] + c2[0]) * 0.5
    return (2.0 + rmean / 256.0) * (dr * dr) + 4.0 * (dg * dg) + (2.0 + (255.0 - rmean) / 256.0) * (db * db)

def convert_image_to_blocks(image):
    # Modo Cuadrantes HD: 2x2 subpíxeles por celda mediante caracteres de bloque Unicode
    img = image.convert("RGBA")
    width, height = img.size
    
    quad_map = {
        0: " ", 1: "▘", 2: "▝", 3: "▀", 
        4: "▖", 5: "▌", 6: "▞", 7: "▛", 
        8: "▗", 9: "▚", 10: "▐", 11: "▜", 
        12: "▄", 13: "▙", 14: "▟", 15: "█"
    }
    
    pixels_data = img.load()
    pm_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = pixels_data[x, y]
            alpha = a / 255.0
            row.append((r * alpha, g * alpha, b * alpha, a))
        pm_pixels.append(row)
        
    def from_premult(pm):
        r_p, g_p, b_p, a = pm
        if a < 1.0: return (0, 0, 0, 0)
        alpha = a / 255.0
        return (int(r_p / alpha), int(g_p / alpha), int(b_p / alpha), int(a))
        
    ascii_str = ""
    last_fg = None
    last_bg = None
    
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            P = []
            for dy in range(2):
                for dx in range(2):
                    if x+dx < width and y+dy < height:
                        P.append(pm_pixels[y+dy][x+dx])
                    else:
                        P.append((0, 0, 0, 0))
            
            # Celda completamente transparente
            if all(p[3] < 64 for p in P):
                if last_fg or last_bg:
                    ascii_str += "\033[0m"
                    last_fg = None
                    last_bg = None
                ascii_str += " "
                continue
            
            # Medir varianza local para adaptar la penalización dinámicamente
            colors = [p[:3] for p in P]
            variance = sum(_color_dist_sq(colors[i], colors[j]) for i in range(4) for j in range(i+1, 4)) / 6.0
            
            # Baja varianza (color plano) -> penalización alta para favorecer bloques sólidos
            # Alta varianza (líneas/bordes) -> penalización reducida para permitir diagonales y esquinas
            shape_penalty = max(100.0, 1800.0 - variance * 0.5)
            
            best_shape = 0
            min_error = float('inf')
            best_fg_pm = (0,0,0,0)
            best_bg_pm = (0,0,0,0)
            
            for shape in range(16):
                fg_indices = [i for i in range(4) if (shape & (1 << i))]
                bg_indices = [i for i in range(4) if not (shape & (1 << i))]
                
                fg_pm = (0,0,0,0)
                if fg_indices:
                    fg_pm = (
                        sum(P[i][0] for i in fg_indices) / len(fg_indices),
                        sum(P[i][1] for i in fg_indices) / len(fg_indices),
                        sum(P[i][2] for i in fg_indices) / len(fg_indices),
                        sum(P[i][3] for i in fg_indices) / len(fg_indices)
                    )
                
                bg_pm = (0,0,0,0)
                if bg_indices:
                    bg_pm = (
                        sum(P[i][0] for i in bg_indices) / len(bg_indices),
                        sum(P[i][1] for i in bg_indices) / len(bg_indices),
                        sum(P[i][2] for i in bg_indices) / len(bg_indices),
                        sum(P[i][3] for i in bg_indices) / len(bg_indices)
                    )
                
                error = 0
                for i in fg_indices:
                    error += (P[i][0]-fg_pm[0])**2 + (P[i][1]-fg_pm[1])**2 + (P[i][2]-fg_pm[2])**2 + (P[i][3]-fg_pm[3])**2
                for i in bg_indices:
                    error += (P[i][0]-bg_pm[0])**2 + (P[i][1]-bg_pm[1])**2 + (P[i][2]-bg_pm[2])**2 + (P[i][3]-bg_pm[3])**2
                    
                if shape not in (0, 15):
                    error += shape_penalty
                    
                if error < min_error:
                    min_error = error
                    best_shape = shape
                    best_fg_pm = fg_pm
                    best_bg_pm = bg_pm

            fg_rgba = from_premult(best_fg_pm)
            bg_rgba = from_premult(best_bg_pm)
            
            fg_opaque = fg_rgba[3] >= 128
            bg_opaque = bg_rgba[3] >= 128
            
            # Compresión de búfer ANSI por estado
            if fg_opaque and bg_opaque:
                char = quad_map[best_shape]
                fg_col = fg_rgba[:3]
                bg_col = bg_rgba[:3]
                code = ""
                if last_fg != fg_col:
                    code += f"\033[38;2;{fg_col[0]};{fg_col[1]};{fg_col[2]}m"
                    last_fg = fg_col
                if last_bg != bg_col:
                    code += f"\033[48;2;{bg_col[0]};{bg_col[1]};{bg_col[2]}m"
                    last_bg = bg_col
                ascii_str += code + char
            elif fg_opaque and not bg_opaque:
                char = quad_map[best_shape]
                fg_col = fg_rgba[:3]
                code = ""
                if last_bg is not None:
                    code += "\033[49m"
                    last_bg = None
                if last_fg != fg_col:
                    code += f"\033[38;2;{fg_col[0]};{fg_col[1]};{fg_col[2]}m"
                    last_fg = fg_col
                ascii_str += code + char
            elif not fg_opaque and bg_opaque:
                inv_shape = 15 - best_shape
                char = quad_map[inv_shape]
                bg_col = bg_rgba[:3]
                code = ""
                if last_bg is not None:
                    code += "\033[49m"
                    last_bg = None
                if last_fg != bg_col:
                    code += f"\033[38;2;{bg_col[0]};{bg_col[1]};{bg_col[2]}m"
                    last_fg = bg_col
                ascii_str += code + char
            else:
                if last_fg or last_bg:
                    ascii_str += "\033[0m"
                    last_fg = None
                    last_bg = None
                ascii_str += " "
                
        ascii_str += "\033[0m\n"
        last_fg = None
        last_bg = None
        
    return ascii_str

def _srgb_to_linear(c):
    # Conversión de sRGB no lineal a luz lineal para promedios físicamente precisos
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _linear_to_srgb(c):
    """Conversión de luz lineal de vuelta a sRGB perceptual para la terminal."""
    c = max(0.0, min(1.0, c))
    return round((c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1/2.4) - 0.055) * 255)

def _linear_avg(colors):
    """Promedio en espacio de luz lineal para cálculo perceptual sin bandas oscuras."""
    if not colors: return (0, 0, 0)
    lr = sum(_srgb_to_linear(c[0]) for c in colors) / len(colors)
    lg = sum(_srgb_to_linear(c[1]) for c in colors) / len(colors)
    lb = sum(_srgb_to_linear(c[2]) for c in colors) / len(colors)
    return (_linear_to_srgb(lr), _linear_to_srgb(lg), _linear_to_srgb(lb))

def convert_image_to_braille(image, use_color=False, invert=False):
    # Renderizado HD en cuadrícula de micropuntos Braille (resolución efectiva 2x4 por carácter)
    if not use_color:
        # En escala de grises aplicamos máscara de desenfoque y realce para perfilar bordes
        image = image.convert("L").filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        image = ImageEnhance.Contrast(image).enhance(1.5)
        
    has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    img = image.convert("RGBA") if has_alpha else image.convert("RGB")
    
    width, height = img.size
    
    dot_map = [
        [0x01, 0x08],
        [0x02, 0x10],
        [0x04, 0x20],
        [0x40, 0x80]
    ]
    
    ascii_str = ""
    last_fg = None
    last_bg = None
    
    for y in range(0, height, 4):
        for x in range(0, width, 2):
            cell_pixels = []
            alphas = []
            
            for dy in range(4):
                for dx in range(2):
                    px = x + dx
                    py = y + dy
                    if px < width and py < height:
                        p = img.getpixel((px, py))
                        cell_pixels.append(p[:3])
                        alphas.append(p[3] if has_alpha else 255)
                    else:
                        cell_pixels.append((0, 0, 0))
                        alphas.append(0)
                        
            # Si toda la celda es transparente
            if all(a < 64 for a in alphas):
                if last_fg or last_bg:
                    ascii_str += "\033[0m"
                    last_fg = None
                    last_bg = None
                ascii_str += " "
                continue
                
            has_transparent = any(a < 128 for a in alphas)
            
            if has_transparent or not use_color:
                # B&W o borde transparente
                braille_val = 0
                fg_pixels = []
                for i in range(8):
                    dy = i // 2
                    dx = i % 2
                    if not use_color:
                        lum = (cell_pixels[i][0] * 0.299 + cell_pixels[i][1] * 0.587 + cell_pixels[i][2] * 0.114)
                        is_drawn = (lum >= 128) if invert else (lum < 128)
                        if is_drawn and alphas[i] >= 128:
                            braille_val += dot_map[dy][dx]
                    else:
                        if alphas[i] >= 128:
                            braille_val += dot_map[dy][dx]
                            fg_pixels.append(cell_pixels[i])
                            
                if braille_val == 0:
                    if last_fg or last_bg:
                        ascii_str += "\033[0m"
                        last_fg = None
                        last_bg = None
                    ascii_str += " "
                else:
                    char = chr(0x2800 + braille_val)
                    if use_color and fg_pixels:
                        fg = _linear_avg(fg_pixels)
                        code = ""
                        if last_bg is not None:
                            code += "\033[49m"
                            last_bg = None
                        if last_fg != fg:
                            code += f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m"
                            last_fg = fg
                        ascii_str += code + char
                    else:
                        ascii_str += char
            else:
                # Celda sólida en modo color: análisis de contraste para Braille Bicolor vs Bloques
                max_d = -1
                p1_idx, p2_idx = 0, 7
                for i in range(8):
                    for j in range(i + 1, 8):
                        d = _color_dist_sq(cell_pixels[i], cell_pixels[j])
                        if d > max_d:
                            max_d = d
                            p1_idx, p2_idx = i, j
                            
                if max_d < 800:
                    # Degradado suave o color sólido -> medio-bloque ▀ superior e inferior
                    top_pixels = [cell_pixels[i] for i in range(4)]
                    bot_pixels = [cell_pixels[i] for i in range(4, 8)]
                    top_c = _linear_avg(top_pixels)
                    bot_c = _linear_avg(bot_pixels)
                    
                    code = ""
                    if last_fg != top_c:
                        code += f"\033[38;2;{top_c[0]};{top_c[1]};{top_c[2]}m"
                        last_fg = top_c
                    if last_bg != bot_c:
                        code += f"\033[48;2;{bot_c[0]};{bot_c[1]};{bot_c[2]}m"
                        last_bg = bot_c
                    ascii_str += code + "▀"
                else:
                    # Alto contraste (línea de dibujo, destello, detalle fino) -> Braille Bicolor
                    seed1 = cell_pixels[p1_idx]
                    seed2 = cell_pixels[p2_idx]
                    g1, g2 = [], []
                    g1_indices = []
                    for idx, c in enumerate(cell_pixels):
                        d1 = _color_dist_sq(c, seed1)
                        d2 = _color_dist_sq(c, seed2)
                        if d1 <= d2:
                            g1.append(c)
                            g1_indices.append(idx)
                        else:
                            g2.append(c)
                            
                    if len(g1) > len(g2):
                        fg_indices = [i for i in range(8) if i not in g1_indices]
                        fg_pixels = g2
                        bg_pixels = g1
                    else:
                        fg_indices = g1_indices
                        fg_pixels = g1
                        bg_pixels = g2
                        
                    fg_col = _linear_avg(fg_pixels)
                    bg_col = _linear_avg(bg_pixels)
                    
                    braille_val = 0
                    for idx in fg_indices:
                        dy = idx // 2
                        dx = idx % 2
                        braille_val += dot_map[dy][dx]
                        
                    char = chr(0x2800 + braille_val) if braille_val > 0 else " "
                    code = ""
                    if last_fg != fg_col:
                        code += f"\033[38;2;{fg_col[0]};{fg_col[1]};{fg_col[2]}m"
                        last_fg = fg_col
                    if last_bg != bg_col:
                        code += f"\033[48;2;{bg_col[0]};{bg_col[1]};{bg_col[2]}m"
                        last_bg = bg_col
                    ascii_str += code + char
                    
        ascii_str += "\033[0m\n"
        last_fg = None
        last_bg = None
        
    return ascii_str

def convert_image_to_ascii(image, use_color=False, invert=False, binary=False, os_style=False):
    """
    Motor clásico: mapeo tonal de píxeles a caracteres ASCII por luminosidad perceptual.
    """
    grayscale_image = image.convert("L")
    
    if not use_color and not binary:
        # En blanco y negro aplicamos realce de nitidez y contraste para definir bordes
        grayscale_image = grayscale_image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        grayscale_image = ImageEnhance.Contrast(grayscale_image).enhance(1.5)
        
    rgb_image = image.convert("RGB")
    
    # Preservar canal alfa si la imagen contiene transparencia
    has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    rgba_image = image.convert("RGBA") if has_alpha else None
    
    ascii_str = ""
    width, height = image.size
    
    if binary:
        base_chars = "01" # Modo binario (0 y 1)
    elif os_style:
        base_chars = " .-+*=#%@WM" # Rampa clásica estilo Neofetch / OS
    elif not use_color:
        base_chars = " .:-=+*#%@" # Alta densidad y detalle para escala de grises
    else:
        base_chars = ASCII_CHARS # Rampa ASCII extendida de alta precisión
    
    chars = base_chars[::-1] if invert else base_chars
    
    for y in range(height):
        for x in range(width):
            if has_alpha:
                _, _, _, a = rgba_image.getpixel((x, y))
                if a < 128:  # Píxel transparente: renderizar espacio en blanco
                    ascii_str += " "
                    continue
            
            grayscale_pixel = grayscale_image.getpixel((x, y))
            
            # Mapear la luminosidad del píxel al índice del carácter
            index = round(grayscale_pixel / 255 * (len(chars) - 1))
            char = chars[index]
            
            if use_color:
                r, g, b = rgb_image.getpixel((x, y))
                ascii_str += get_ansi_color_code(r, g, b) + char
            else:
                ascii_str += char
        
        # Reseteo de secuencias ANSI al final de cada línea para mantener limpio el búfer
        if use_color:
            ascii_str += reset_ansi_color_code()
        ascii_str += "\n"
        
    return ascii_str

def parse_version(v_str):
    try:
        clean = str(v_str).lstrip("v").strip()
        parts = []
        for x in clean.split("."):
            num = ""
            for ch in x:
                if ch.isdigit(): num += ch
                else: break
            parts.append(int(num) if num else 0)
        return tuple(parts)
    except Exception:
        return (0, 0, 0)

def fetch_latest_version():
    import urllib.request
    import json
    import re
    # 1. Consultar el archivo principal en GitHub (refleja inmediatamente nuevos commits/versiones)
    try:
        req = urllib.request.Request(
            GITHUB_RAW_URL,
            headers={"User-Agent": f"Luma-CLI/{VERSION}"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            m_ver = re.search(r'(?:VERSION|__version__)\s*=\s*["\']v?(\d+\.\d+\.\d+)["\']', content)
            if m_ver:
                return m_ver.group(1)
            m_banner = re.search(r'v(\d+\.\d+\.\d+)\s*-\s*(?:Epic\s+)?Terminal Art Engine', content)
            if m_banner:
                return m_banner.group(1)
    except Exception:
        pass

    # 2. Respaldo: API de GitHub Releases
    try:
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={"User-Agent": f"Luma-CLI/{VERSION}"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            tag = data.get("tag_name", "").lstrip("v")
            if tag:
                return tag
    except Exception:
        pass
    return None

def get_update_cache_file():
    config_dir = os.path.expanduser("~/.config/luma")
    return os.path.join(config_dir, "update_cache.json")

def save_update_cache(latest_ver):
    try:
        import time
        import json
        cache_file = get_update_cache_file()
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump({"last_check": int(time.time()), "latest_version": latest_ver}, f)
    except Exception:
        pass

def check_cached_update():
    """Retorna (has_update, latest_ver) usando caché local y consulta en segundo plano si está obsoleto."""
    import time
    import json
    import threading
    
    cache_file = get_update_cache_file()
    last_check = 0
    cached_latest = None
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
                last_check = data.get("last_check", 0)
                cached_latest = data.get("latest_version")
        except Exception:
            pass
            
    now = int(time.time())
    # Si la caché tiene más de 24 horas (86400s), lanzar verificación asíncrona en hilo secundario
    if now - last_check > 86400:
        def bg_worker():
            lv = fetch_latest_version()
            if lv:
                save_update_cache(lv)
        t = threading.Thread(target=bg_worker, daemon=True)
        t.start()
        
    if cached_latest and parse_version(cached_latest) > parse_version(VERSION):
        return True, cached_latest
    return False, None

def show_version_info():
    """Muestra un informe diagnóstico completo del sistema, entorno y motores de renderizado."""
    import platform
    import shutil
    
    banner = f"""\033[1;36m
 █    █ █ █▄ ▄█ ▄▀▄ █▀▄ ▀█▀
 █▄▄▄ ▀▄█ █ ▀ █ █▀█ █▀▄  █
 \033[0;36mv{VERSION} - Terminal Art Engine\033[0m
"""
    print(banner)
    
    # 1. Runtime environment
    is_frozen = getattr(sys, 'frozen', False)
    build_type = "Standalone Executable (PyInstaller)" if is_frozen else "Python Script"
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    
    print("📋 \033[1mInformación del Sistema y Runtime:\033[0m")
    print(f"  • Versión Luma:        \033[1;32mv{VERSION}\033[0m")
    print(f"  • Tipo de Ejecución:   {build_type}")
    print(f"  • Entorno Python:      v{py_ver} ({sys.executable})")
    print(f"  • Plataforma OS:       {os_info}")
    
    # 2. Acceleration Engines
    has_cpp = False
    cpp_detail = "No detectado (usando fallback en Python)"
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for cand in [
        os.path.join(exe_dir, "libmonochrome.so"),
        os.path.join(base_dir, "libmonochrome.so"),
        "/usr/local/share/luma/libmonochrome.so",
        "/usr/share/luma/libmonochrome.so",
        "libmonochrome.so"
    ]:
        if os.path.exists(cand):
            has_cpp = True
            cpp_detail = f"Activo ({cand})"
            break
    if not has_cpp and shutil.which("luma-mono"):
        has_cpp = True
        cpp_detail = f"Activo vía binario ({shutil.which('luma-mono')})"
        
    print("\n⚡ \033[1mMotores de Renderizado:\033[0m")
    print(f"  • Motor Color:         Activo (Linear RGB 2.2, Lanczos, ANSI 24-bit TrueColor)")
    print(f"  • Motor Monocromático: {'\033[1;32m' if has_cpp else '\033[1;33m'}{cpp_detail}\033[0m")
    print(f"  • Modos B&W Soportados: braille, manga 2.0 (DoG + Bayer), sketch (DoG puro), blocks (2x2 cuadrantes HD), ascii")
    print(f"  • Algoritmos Tramado:  atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8")
    
    # 3. Terminal Diagnostics
    cols, rows = shutil.get_terminal_size((90, 24))
    colorterm = os.environ.get("COLORTERM", "no detectado")
    term = os.environ.get("TERM", "no detectado")
    has_truecolor = colorterm in ("truecolor", "24bit") or "kitty" in term or "alacritty" in term
    
    print("\n🖥️  \033[1mDiagnóstico de Terminal:\033[0m")
    print(f"  • Resolución actual:   {cols} columnas × {rows} filas")
    print(f"  • $COLORTERM:          {colorterm}")
    print(f"  • $TERM:               {term}")
    print(f"  • TrueColor (24-bit):  {'\033[1;32m✅ Soportado' if has_truecolor else '\033[1;33m⚠️  No detectado (puede haber colores aproximados)'}\033[0m")
    
    # 4. Storage & Config
    cfg_path = os.path.expanduser("~/.config/luma/config.json")
    backup_dir = os.path.expanduser("~/.config/luma/backup")
    backup_count = 0
    if os.path.exists(backup_dir):
        backup_count = len([f for f in os.listdir(backup_dir) if f.startswith("lumart-v")])
        
    print("\n📁 \033[1mRutas y Configuración:\033[0m")
    print(f"  • Configuración:       {cfg_path} ({'Existe' if os.path.exists(cfg_path) else 'Predeterminado'})")
    print(f"  • Copias de Seguridad: {backup_dir} ({backup_count} backups guardados)")
    print(f"  • Repositorio GitHub:  https://github.com/{GITHUB_REPO}")
    print()

def fetch_all_releases_with_meta():
    """Consulta la API de GitHub y retorna una lista de releases con metadatos."""
    import urllib.request
    import json
    
    releases = []
    # 1. Intentar API de releases
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases",
            headers={"User-Agent": f"Luma-CLI/{VERSION}"}
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list):
                for item in data:
                    tag = item.get("tag_name", "").lstrip("v")
                    if tag:
                        releases.append({
                            "tag_name": tag,
                            "name": item.get("name", ""),
                            "body": item.get("body", ""),
                            "published_at": item.get("published_at", "")
                        })
    except Exception:
        pass
        
    # 2. Respaldo: API de tags
    if not releases:
        try:
            req = urllib.request.Request(
                f"https://api.github.com/repos/{GITHUB_REPO}/tags",
                headers={"User-Agent": f"Luma-CLI/{VERSION}"}
            )
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if isinstance(data, list):
                    for item in data:
                        tag = item.get("name", "").lstrip("v")
                        if tag:
                            releases.append({
                                "tag_name": tag,
                                "name": "",
                                "body": "",
                                "published_at": ""
                            })
        except Exception:
            pass
            
    releases.sort(key=lambda x: parse_version(x["tag_name"]), reverse=True)
    return releases

def fetch_all_releases():
    """Consulta los tags y releases públicos disponibles en GitHub (solo números de versión)."""
    releases = fetch_all_releases_with_meta()
    return [r["tag_name"] for r in releases]

def check_for_updates():
    """Comprueba si existe una versión más reciente sin instalar nada y muestra información detallada."""
    print(_("update_checking"))
    all_releases = fetch_all_releases_with_meta()
    if not all_releases:
        print(_("update_error", "No se pudo consultar información de versiones en GitHub."))
        return False
        
    latest_rel = all_releases[0]
    latest_ver = latest_rel["tag_name"]
    cur_tuple = parse_version(VERSION)
    latest_tuple = parse_version(latest_ver)
    
    print(f"\n📦 \033[1mEstado de Versiones de Luma:\033[0m")
    print(f"   • Versión actual instalada: \033[1;36mv{VERSION}\033[0m")
    print(f"   • Última versión en GitHub: \033[1;32mv{latest_ver}\033[0m")
    
    if latest_tuple > cur_tuple:
        print(f"\n💡 \033[1;33m¡Hay una nueva versión disponible!\033[0m")
        if latest_rel.get("name"):
            print(f"   Título del release: {latest_rel['name']}")
        print(f"   Para descargar e instalar automáticamente ejecuta:")
        print(f"   \033[1;32mlumart -uu\033[0m (o \033[1;32mlumart --upgrade\033[0m)")
    else:
        print(f"\n✅ \033[1;32m¡Tu instalación está al día con la versión más reciente!\033[0m")
        
    print(f"\n📜 \033[1mHistorial de Versiones Recientes:\033[0m")
    for r in all_releases[:5]:
        v = r["tag_name"]
        is_cur = " \033[1;36m(actual)\033[0m" if v == VERSION else ""
        date_str = r.get("published_at", "")[:10]
        date_disp = f" [{date_str}]" if date_str else ""
        print(f"   • v{v:<7}{date_disp}{is_cur}")
        
    print(f"\n💡 \033[1mComandos Útiles:\033[0m")
    print(f"   • lumart -uu              -> Descargar y aplicar última actualización")
    print(f"   • lumart -dg              -> Selector interactivo para volver a versión anterior")
    print(f"   • lumart -v               -> Ver diagnóstico completo del sistema")
    print()
    return True

def perform_upgrade(target_ver=None):
    """
    Descarga e instala una versión más reciente con menú interactivo si hay múltiples versiones.
    """
    import urllib.request
    import shutil
    import py_compile
    import time
    import json
    
    print(_("update_checking"))
    all_releases = fetch_all_releases_with_meta()
    if not all_releases:
        print(_("update_error", "No se pudo consultar información de versiones en GitHub."))
        return False
        
    cur_tuple = parse_version(VERSION)
    newer = [r for r in all_releases if parse_version(r["tag_name"]) > cur_tuple]
    
    if not newer and not target_ver:
        print(_("update_already_latest", VERSION))
        return True
        
    chosen_rel = None
    if target_ver:
        target_clean = target_ver.lstrip("v").strip()
        for r in all_releases:
            if r["tag_name"].lstrip("v") == target_clean:
                chosen_rel = r
                break
        if not chosen_rel:
            chosen_rel = {"tag_name": target_clean, "name": "", "body": "", "published_at": ""}
    elif len(newer) == 1 or not sys.stdin.isatty():
        chosen_rel = newer[0]
    else:
        print("🚀 \033[1mVersiones disponibles para Upgrade:\033[0m")
        print(f"   Versión actual instalada: \033[1;36mv{VERSION}\033[0m\n")
        for idx, r in enumerate(newer, 1):
            v = r["tag_name"]
            title = f" - {r['name']}" if r.get("name") else ""
            date_str = f" [{r['published_at'][:10]}]" if r.get("published_at") else ""
            rec = " \033[1;32m(Última versión recomendada)\033[0m" if idx == 1 else ""
            print(f"   \033[1m[{idx}]\033[0m v{v:<7}{date_str}{title}{rec}")
        print(f"   \033[1m[c]\033[0m Cancelar\n")
        
        try:
            ans = input(f"Elige una versión [1-{len(newer)}] o presiona Enter para [1]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")
            return False
            
        if ans.lower() in ("c", "cancel", "q", "salir"):
            print("Operación cancelada.")
            return False
        if ans == "":
            ans = "1"
        try:
            sel_idx = int(ans) - 1
            if 0 <= sel_idx < len(newer):
                chosen_rel = newer[sel_idx]
            else:
                print("❌ Selección inválida.")
                return False
        except ValueError:
            print("❌ Selección inválida.")
            return False
            
    dest_ver = chosen_rel["tag_name"].lstrip("v")
    print(f"\n⬇️  Preparando instalación de Luma v{dest_ver}...")
    if chosen_rel.get("name"):
        print(f"   Título: {chosen_rel['name']}")
        
    is_frozen = getattr(sys, 'frozen', False)
    target_path = sys.executable if is_frozen else os.path.realpath(__file__)
    target_dir = os.path.dirname(target_path)
    
    if not os.access(target_path, os.W_OK) or not os.access(target_dir, os.W_OK):
        print(_("update_permission_error", target_path))
        return False
        
    # Crear backup previo
    backup_dir = os.path.expanduser("~/.config/luma/backup")
    try:
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, f"lumart-v{VERSION}")
        shutil.copy2(target_path, backup_file)
        info_file = os.path.join(backup_dir, "last_backup.json")
        with open(info_file, "w") as f:
            json.dump({
                "version": VERSION,
                "backup_path": backup_file,
                "target_path": target_path,
                "is_frozen": is_frozen,
                "timestamp": int(time.time())
            }, f, indent=2)
        print(f"🛡️  Copia de seguridad de v{VERSION} guardada en: {backup_file}")
    except Exception as e:
        print(f"⚠️  Aviso: No se pudo crear la copia de seguridad previa ({e}).")

    tmp_path = target_path + ".tmp"
    try:
        if is_frozen:
            download_url = f"https://github.com/SilentBlox01/Luma/releases/download/v{dest_ver}/lumart"
        else:
            download_url = f"https://raw.githubusercontent.com/SilentBlox01/Luma/v{dest_ver}/lumart.py"
            
        req = urllib.request.Request(download_url, headers={"User-Agent": f"Luma-CLI/{VERSION}"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            
        with open(tmp_path, "wb") as f:
            f.write(content)
            
        if not is_frozen:
            py_compile.compile(tmp_path, doraise=True)
            
        os.replace(tmp_path, target_path)
        os.chmod(target_path, 0o755)
        
        save_update_cache(dest_ver)
        print(_("update_success", VERSION, dest_ver))
        print("💡 Si deseas volver a la versión anterior en cualquier momento, ejecuta: lumart -dg")
        return True
    except Exception as e:
        if os.path.exists(tmp_path):
            try: os.remove(tmp_path)
            except Exception: pass
        print(_("update_error", e))
        return False

def perform_downgrade(target_ver=None):
    """
    Restaura una versión anterior de Luma con selector interactivo y soporte de backups locales.
    """
    import urllib.request
    import shutil
    import py_compile
    import json
    
    is_frozen = getattr(sys, 'frozen', False)
    target_path = sys.executable if is_frozen else os.path.realpath(__file__)
    target_dir = os.path.dirname(target_path)
    
    if not os.access(target_path, os.W_OK) or not os.access(target_dir, os.W_OK):
        print(_("update_permission_error", target_path))
        return False

    backup_dir = os.path.expanduser("~/.config/luma/backup")
    os.makedirs(backup_dir, exist_ok=True)
    
    cur_tuple = parse_version(VERSION)
    options = []
    
    if os.path.exists(backup_dir):
        for f in sorted(os.listdir(backup_dir)):
            if f.startswith("lumart-v"):
                bver = f.replace("lumart-v", "")
                if parse_version(bver) < cur_tuple:
                    options.append((bver, "local", os.path.join(backup_dir, f)))
                    
    all_releases = fetch_all_releases()
    all_releases.sort(key=parse_version, reverse=True)
    for r in all_releases:
        if parse_version(r) < cur_tuple:
            if not any(opt[0] == r for opt in options):
                options.append((r, "github", None))
                
    options.sort(key=lambda x: parse_version(x[0]), reverse=True)
    
    if not options and not target_ver:
        print(_("downgrade_no_backup"))
        return False
        
    chosen_ver = None
    chosen_src = None
    chosen_path = None
    
    if target_ver and target_ver != "prev":
        chosen_ver = target_ver.lstrip("v").strip()
        for v, src, path in options:
            if v == chosen_ver:
                chosen_src = src
                chosen_path = path
                break
        if not chosen_src:
            chosen_src = "github"
    elif not sys.stdin.isatty() or len(options) == 0:
        chosen_ver, chosen_src, chosen_path = options[0]
    else:
        print("⏪ \033[1mSelector de Versión para Downgrade / Rollback:\033[0m")
        print(f"   Versión actual instalada: \033[1;36mv{VERSION}\033[0m\n")
        for idx, (ver, src, _) in enumerate(options, 1):
            src_tag = "\033[32m[Copia local - instantáneo]\033[0m" if src == "local" else "\033[34m[GitHub Release - descarga requerida]\033[0m"
            print(f"   \033[1m[{idx}]\033[0m v{ver:<7} {src_tag}")
        print(f"   \033[1m[c]\033[0m Cancelar\n")
        
        try:
            ans = input(f"Elige una versión [1-{len(options)}] o presiona Enter para [1]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")
            return False
            
        if ans.lower() in ("c", "cancel", "q", "salir"):
            print("Operación cancelada.")
            return False
        if ans == "":
            ans = "1"
        try:
            sel_idx = int(ans) - 1
            if 0 <= sel_idx < len(options):
                chosen_ver, chosen_src, chosen_path = options[sel_idx]
            else:
                print("❌ Selección inválida.")
                return False
        except ValueError:
            print("❌ Selección inválida.")
            return False

    print(f"\n🔄 Restaurando Luma a la versión v{chosen_ver}...")
    
    if chosen_src == "local" and chosen_path and os.path.exists(chosen_path):
        try:
            cur_backup = os.path.join(backup_dir, f"lumart-v{VERSION}")
            shutil.copy2(target_path, cur_backup)
            
            tmp_path = target_path + ".tmp"
            shutil.copy2(chosen_path, tmp_path)
            os.replace(tmp_path, target_path)
            os.chmod(target_path, 0o755)
            print(_("downgrade_success", chosen_ver))
            print(f"📦 Restaurado instantáneamente desde archivo local: {chosen_path}")
            return True
        except Exception as e:
            print(_("downgrade_error", e))
            return False
            
    print(f"⬇️  Descargando versión v{chosen_ver} desde GitHub Releases...")
    tmp_path = target_path + ".tmp"
    try:
        if is_frozen:
            download_url = f"https://github.com/SilentBlox01/Luma/releases/download/v{chosen_ver}/lumart"
        else:
            download_url = f"https://raw.githubusercontent.com/SilentBlox01/Luma/v{chosen_ver}/lumart.py"
            
        req = urllib.request.Request(download_url, headers={"User-Agent": f"Luma-CLI/{VERSION}"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            
        with open(tmp_path, "wb") as f:
            f.write(content)
            
        if not is_frozen:
            py_compile.compile(tmp_path, doraise=True)
            
        try:
            cur_backup = os.path.join(backup_dir, f"lumart-v{VERSION}")
            shutil.copy2(target_path, cur_backup)
        except Exception:
            pass

        os.replace(tmp_path, target_path)
        os.chmod(target_path, 0o755)
        print(_("downgrade_success", chosen_ver))
        return True
    except Exception as e:
        if os.path.exists(tmp_path):
            try: os.remove(tmp_path)
            except Exception: pass
        print(_("downgrade_error", e))
        return False

def try_render_native_monochrome(image_path, width, mode="braille", dither="none", invert=False):
    """
    Intenta ejecutar el motor nativo en C++ (luma-mono o libmonochrome.so).
    C++ a toda hostia para que los fans de Rust no vengan a romper las bolas con el rendimiento.
    Retorna el string de texto renderizado o None si no se encuentra el binario/librería.
    """
    import ctypes
    import shutil
    import subprocess

    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lib_paths = [
        os.path.join(exe_dir, "libmonochrome.so"),
        os.path.join(base_dir, "libmonochrome.so"),
        os.path.join(exe_dir, "..", "libmonochrome.so"),
        os.path.join(base_dir, "..", "libmonochrome.so"),
        "/usr/local/share/luma/libmonochrome.so",
        "/usr/share/luma/libmonochrome.so",
        "/usr/local/lib/libmonochrome.so",
        "/usr/lib/libmonochrome.so",
        "libmonochrome.so"
    ]
    for lp in lib_paths:
        if os.path.exists(lp):
            try:
                lib = ctypes.CDLL(lp)
                lib.render_monochrome_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]
                lib.render_monochrome_c.restype = ctypes.c_void_p
                lib.free_monochrome_buffer.argtypes = [ctypes.c_void_p]
                lib.free_monochrome_buffer.restype = None

                ptr = lib.render_monochrome_c(
                    image_path.encode("utf-8"),
                    int(width),
                    mode.encode("utf-8"),
                    str(dither).encode("utf-8"),
                    bool(invert)
                )
                if ptr:
                    res_bytes = ctypes.string_at(ptr)
                    lib.free_monochrome_buffer(ptr)
                    res = res_bytes.decode("utf-8", errors="replace")
                    if res and not res.startswith("❌"):
                        return res
            except Exception:
                pass

    bin_names = [
        os.path.join(exe_dir, "luma-mono"),
        os.path.join(base_dir, "luma-mono"),
        shutil.which("luma-mono")
    ]
    for b in bin_names:
        if b and os.path.exists(b) and os.access(b, os.X_OK):
            try:
                cmd = [b, "-w", str(width), "-m", mode]
                if dither and dither != "none":
                    cmd.extend(["-d", str(dither)])
                if invert:
                    cmd.append("-i")
                cmd.append(image_path)
                proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
                if proc.stdout and not proc.stdout.startswith("❌"):
                    return proc.stdout
            except Exception:
                pass

    return None

def main():
    import json
    
    # Inicialización de secuencias de escape ANSI en consolas Windows (cmd / powershell)
    if os.name == "nt":
        os.system("")
    
    # Preprocesamiento de --lang para aplicar la configuración de idioma antes de argparse
    lang_override = None
    if "--lang" in sys.argv:
        try:
            lang_idx = sys.argv.index("--lang")
            lang_override = sys.argv[lang_idx + 1]
        except IndexError:
            pass
            
    # Persistir configuración de usuario en ~/.config/luma/config.json
    config_dir = os.path.expanduser("~/.config/luma")
    config_file = os.path.join(config_dir, "config.json")
    
    # Si la invocación es solo para cambiar el idioma (ej: lumart --lang es), guardar y salir
    if len(sys.argv) == 3 and "--lang" in sys.argv:
        if lang_override in TRANSLATIONS:
            os.makedirs(config_dir, exist_ok=True)
            with open(config_file, "w") as f:
                json.dump({"lang": lang_override}, f)
            set_language(lang_override)
            print(_("lang_success", lang_override))
            sys.exit(0)
        else:
            set_language("en") # Idioma de respaldo predeterminado
            print(_("lang_error", lang_override))
            sys.exit(1)
            
    # Cargar configuración previa si existe
    saved_lang = None
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                saved_lang = json.load(f).get("lang")
        except Exception:
            pass

    if lang_override:
        set_language(lang_override)
    elif saved_lang:
        set_language(saved_lang)
    else:
        # Autodetección del idioma del sistema
        auto_detect_language()

    banner = f"""\033[1;36m
 █    █ █ █▄ ▄█ ▄▀▄ █▀▄ ▀█▀
 █▄▄▄ ▀▄█ █ ▀ █ █▀█ █▀▄  █
 \033[0;36mv{VERSION} - Terminal Art Engine\033[0m
"""
    
    # Intercepción inmediata de -v / --version para mostrar el diagnóstico e info completa
    if "-v" in sys.argv or "--version" in sys.argv:
        show_version_info()
        sys.exit(0)

    # Sin argumentos: mostrar banner informativo y ayuda básica de uso
    if len(sys.argv) == 1:
        print(banner)
        print(_("usage"))
        sys.exit(1)
        
    if "-h" in sys.argv or "--help" in sys.argv:
        print(banner)

    # Configuración de argumentos de línea de comandos con argparse
    parser = argparse.ArgumentParser(prog="lumart", description=_( "desc" ), add_help=False)
    parser.add_argument("-h", "--help", action="help", help=_("help_help"))
    parser.add_argument("-v", "--version", action="store_true", help=_("help_version"))
    parser.add_argument("-u", "--update", "--check-update", action="store_true", help=_("help_update"))
    parser.add_argument("-uu", "--upgrade", action="store_true", help=_("help_upgrade"))
    parser.add_argument("-dg", "--downgrade", "--rollback", nargs="?", const="prev", default=None, help=_("help_downgrade"))

    parser.add_argument("image_path", nargs="?", default=None, help=_("help_image_path"))
    parser.add_argument("-w", "--width", type=int, default=None, help=_("help_width"))
    parser.add_argument("-E", "--engine", choices=["color", "mono", "bw", "manga", "sketch"], default=None, help=_("help_engine"))
    parser.add_argument("-d", "--dither", nargs="?", const="atkinson", default=None, help=_("help_dither"))
    parser.add_argument("--no-color", action="store_false", dest="color", help=_("help_no_color"))
    parser.add_argument("-c", "--color", action="store_true", dest="color", default=True, help=_("help_color"))
    parser.add_argument("-i", "--invert", action="store_true", help=_("help_invert"))
    parser.add_argument("-o", "--output", help=_("help_output"))
    parser.add_argument("-b", "--binary", action="store_true", help=_("help_binary"))
    parser.add_argument("--blocks", action="store_true", help=_("help_blocks"))
    parser.add_argument("--braille", action="store_true", help=_("help_braille"))
    parser.add_argument("-m", "--manga", action="store_true", help=_("help_manga"))
    parser.add_argument("-s", "--sketch", action="store_true", help=_("help_sketch"))
    parser.add_argument("--epic", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--raw-colors", action="store_true", help=_("help_raw_colors"))
    parser.add_argument("--os-style", action="store_true", help=_("help_os_style"))
    parser.add_argument("--swap", nargs="+", help=_("help_swap"))
    parser.add_argument("--lang", help=_("help_lang"))
    
    args = parser.parse_args()

    # Si se solicitó versión
    if args.version:
        show_version_info()
        sys.exit(0)

    # Comprobar actualizaciones sin instalar (-u / --update / --check-update)
    if args.update:
        print(banner)
        check_for_updates()
        sys.exit(0)

    # Descargar e instalar la actualización más reciente (-uu / --upgrade)
    if args.upgrade:
        print(banner)
        success = perform_upgrade()
        sys.exit(0 if success else 1)

    # Volver a la versión anterior o especificada (-dg / --downgrade / --rollback)
    if args.downgrade is not None:
        print(banner)
        target = None if args.downgrade == "prev" else args.downgrade
        success = perform_downgrade(target)
        sys.exit(0 if success else 1)

    if not args.image_path:
        print(banner)
        print(_("usage"))
        sys.exit(1)

    # Comprobación no invasiva de actualización en segundo plano (aviso a stderr para no contaminar salida)
    has_update, update_ver = check_cached_update()
    if has_update:
        print(f"\033[1;33m{_('update_notice', update_ver)}\033[0m\n", file=sys.stderr)

    # Selección de motor mediante flag --engine / -E
    if args.engine:
        if args.engine in ("mono", "bw"):
            args.color = False
        elif args.engine == "manga":
            args.color = False
            args.braille = True
            args.manga = True
        elif args.engine == "sketch":
            args.color = False
            args.braille = True
            args.sketch = True
        elif args.engine == "color":
            args.color = True

    if getattr(args, "manga", False):
        args.color = False
        args.braille = True

    if getattr(args, "sketch", False):
        args.color = False
        args.braille = True

    # 1. Autodetección del estándar NO_COLOR (https://no-color.org)
    if "NO_COLOR" in os.environ and "--color" not in sys.argv and "-c" not in sys.argv:
        args.color = False

    # 2. Autodetección del ancho de la terminal: si no se especifica -w, nos adaptamos
    if args.width is None:
        try:
            import shutil
            term_cols = shutil.get_terminal_size((90, 24)).columns
            args.width = min(90, max(20, term_cols))
        except Exception:
            args.width = 90

    # 3. Autodetección de terminal clara (Light mode) para inversión automática de caracteres
    invert_mode = args.invert or is_light_terminal()
    
    try:
        image = Image.open(args.image_path)
    except Exception as e:
        # Error al abrir la imagen en la ruta especificada
        print(_("error_open", e))
        sys.exit(1)
        
    if args.swap:
        if len(args.swap) % 2 != 0:
            print(_("error_swap"))
            sys.exit(1)
        image = apply_color_swap(image, args.swap)

    # -------------------------------------------------------------
    # MOTOR SECUNDARIO: Blanco y Negro (Nativo C++ con fallback Python)
    # -------------------------------------------------------------
    if not args.color:
        if getattr(args, "sketch", False) or args.engine == "sketch":
            mono_mode = "sketch"
        elif getattr(args, "manga", False) or args.engine == "manga":
            mono_mode = "manga"
        elif args.braille:
            mono_mode = "braille"
        elif args.blocks:
            mono_mode = "blocks"
        else:
            mono_mode = "ascii"

        dither_algo = "none"
        if args.dither:
            dither_algo = "atkinson" if args.dither is True else str(args.dither).lower()

        native_art = try_render_native_monochrome(args.image_path, args.width, mono_mode, dither_algo, invert_mode)
        if native_art is not None:
            ascii_art = native_art
        else:
            if mono_mode == "sketch":
                ascii_art = render_python_sketch(image, args.width, invert_mode)
            elif mono_mode == "manga":
                ascii_art = render_python_manga(image, args.width, invert_mode)
            elif mono_mode == "blocks":
                ascii_art = render_python_bw_quadrants(image, args.width, dither_algo, invert_mode)
            else:
                image = resize_image(image, args.width, args.blocks, args.braille)
                if dither_algo in ("atkinson", "bayer", "floyd") or args.dither:
                    image = apply_bayer_dither(image)
                if args.braille:
                    ascii_art = convert_image_to_braille(image, args.color, invert_mode)
                elif args.blocks:
                    ascii_art = convert_image_to_blocks(image)
                else:
                    ascii_art = convert_image_to_ascii(image, args.color, invert_mode, args.binary, args.os_style)
    # -------------------------------------------------------------
    # MOTOR PRIMARIO: Motor de Color
    # -------------------------------------------------------------
    else:
        if not args.raw_colors:
            # Convertir a RGBA para compatibilidad con paletas indexadas y transparencia
            image = image.convert("RGBA")
            image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))
            image = ImageEnhance.Color(image).enhance(1.25)
            image = ImageEnhance.Contrast(image).enhance(1.15)
            
        image = resize_image(image, args.width, args.blocks, args.braille)
        
        # Difuminado ordenado con matriz de Bayer para simular sombreado retro
        if args.dither:
            image = apply_bayer_dither(image)
        
        if args.braille:
            ascii_art = convert_image_to_braille(image, args.color, invert_mode)
        elif args.blocks:
            ascii_art = convert_image_to_blocks(image)
        else:
            ascii_art = convert_image_to_ascii(image, args.color, invert_mode, args.binary, args.os_style)
    
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(ascii_art)
            print(_("saved_to", args.output))
        except Exception as e:
            # Error al guardar el archivo en disco
            print(_("error_save", e))
    else:
        # Imprimir salida directamente en la consola
        print(ascii_art)

if __name__ == "__main__":
    main()
