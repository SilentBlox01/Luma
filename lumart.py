#!/usr/bin/env python3
import argparse
import sys
import locale
import os
import io
import urllib.request
import shlex
import time
import datetime
import re
import subprocess
import shutil
import tempfile
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

# Importación del motor de renderizado a color de nueva generación: Mary
try:
    import mary
except ImportError:
    _base_dir = os.path.dirname(os.path.abspath(__file__))
    if _base_dir not in sys.path:
        sys.path.insert(0, _base_dir)
    for _cand_dir in ["/usr/local/share/luma", "/usr/share/luma"]:
        if os.path.exists(_cand_dir) and _cand_dir not in sys.path:
            sys.path.append(_cand_dir)
    try:
        import mary
    except ImportError:
        mary = None


VERSION = "2.5.0"
CODENAME = "Apex Nova"
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
        "diag_title_system": "📋 System & Runtime Diagnostics:",
        "diag_luma_ver": "Luma Version:",
        "diag_exec_type": "Execution Type:",
        "diag_standalone": "Standalone Executable (PyInstaller)",
        "diag_script": "Python Script",
        "diag_python_env": "Python Environment:",
        "diag_platform_os": "OS Platform:",
        "diag_title_engines": "⚡ Rendering Engines:",
        "diag_trumble_desc": "Active (Default) (Cel-Shading Anime Ink Outlines, Capcom CPS-2 / Neo-Geo Color Punch, Lanczos, Bayer Dither, TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (Perceptual Color Apex 3.5):",
        "diag_mary_modes": "Supported Mary Modes:",
        "diag_mary_modes_list": "sextants (2x3 solid HD blocks), braille (2x4 dual-color), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (Monochrome Mono 2.6):",
        "diag_luris_modes": "Supported Luris Modes:",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (pure DoG), blocks (2x2 HD quadrants), ascii",
        "diag_dither_algos": "Dithering Algorithms:",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (Live Webcam Weep 1.4):",
        "diag_spectra_avail": "Available (OpenCV 30-60 FPS Terminal Stream with 5 Live Weep Filters)",
        "diag_spectra_req": "Requires opencv-python",
        "diag_title_terminal": "🖥️  Terminal Diagnostics:",
        "diag_res_label": "Current Resolution:",
        "diag_res_format": "{} columns × {} rows",
        "diag_truecolor_label": "TrueColor (24-bit):",
        "diag_truecolor_supported": "✅ Supported",
        "diag_truecolor_unsupported": "⚠️  Not detected (colors may be approximated)",
        "diag_title_paths": "📁 Paths & Configuration:",
        "diag_config_label": "Configuration:",
        "diag_config_exists": "Exists",
        "diag_config_default": "Default",
        "diag_backup_label": "Backups:",
        "diag_backup_count": "{} backups saved",
        "diag_repo_label": "GitHub Repository:",
        "diag_native_active": "Active ({})",
        "diag_native_active_bin": "Active via binary ({})",
        "diag_native_cpp": "Native C++ ({})",
        "diag_native_cpp_bin": "Native C++ via binary ({})",
        "diag_py_fallback": "Not detected (using Python fallback)",
        "diag_mary_fallback": "Python Fallback",
        "diag_not_available": "Not available (using Trumble)",
        "ver_status_title": "📦 Luma Version Status:",
        "ver_current_installed": "Current installed version:",
        "ver_latest_github": "Latest version on GitHub:",
        "ver_new_available": "💡 A new version is available!",
        "ver_release_title": "Release title:",
        "ver_install_hint": "To automatically download and install, run:",
        "ver_up_to_date": "✅ Your installation is up to date with the latest version!",
        "ver_recent_history": "📜 Recent Version History:",
        "ver_useful_commands": "💡 Useful Commands:",
        "ver_cmd_uu": "Download and apply latest update",
        "ver_cmd_dg": "Interactive selector to roll back to previous version",
        "ver_cmd_v": "View full system diagnostic report",
        "ver_tag_current": "(current)",
        "upg_avail_title": "🚀 Available Versions for Upgrade:",
        "upg_recommended": "(Latest recommended version)",
        "upg_cancel": "Cancel",
        "upg_choose_prompt": "Choose a version [1-{}] or press Enter for [1]: ",
        "upg_cancelled": "Operation cancelled.",
        "upg_invalid_sel": "❌ Invalid selection.",
        "upg_preparing": "⬇️  Preparing to install Luma v{}...",
        "upg_title": "Title:",
        "upg_backup_saved": "🛡️  Backup of v{} saved to: {}",
        "upg_backup_warn": "⚠️  Warning: Could not create backup ({}).",
        "upg_rollback_hint": "💡 To rollback to previous version at any time, run: lumart -dg",
        "dg_title": "⏪ Available Versions for Rollback (Downgrade):",
        "dg_choose_prompt": "Choose a version to restore [1-{}] or press Enter for [1]: ",
        "hist_title": "📜 Lumart Command History ({} recorded):",
        "hist_empty": "  (No commands recorded in history yet)",
        "hist_header_num": "[#]",
        "hist_header_ver": "Ver",
        "hist_header_date": "Date / Time",
        "hist_header_cmd": "Command",
        "hist_replay_hint": "💡 To re-execute any command, run: lumart --replay <number> (e.g.: lumart -R 1)",
        "hist_out_of_range": "❌ Index [{}] out of range. There are {} available commands.",
        "hist_int_required": "❌ Index must be an integer (e.g.: lumart --replay 1).",
        "hist_replaying": "🚀 Re-executing [{}]: {}",
        "hist_cleared": "✅ Lumart command history cleared successfully.",
        "hist_already_empty": "ℹ️ Command history was already empty.",
        "desktop_installing": "🖥️  Installing desktop integration and file manager actions...",
        "desktop_installed_launcher": "  ✅ Desktop launcher installed: {}",
        "desktop_launcher_error": "  ❌ Error creating {}: {}",
        "desktop_context_menu": "  ✅ {} context menu script: {}",
        "desktop_completed": "🎉 Desktop integration completed successfully!\n   Now you can right-click any image in your file manager and select 'Open with Lumart'.",
        "spectra_webcam_only": "💡 The 'Spectra' engine is exclusively for live video and webcam streaming.\n   To activate it, run:\n   lumart --webcam  (or: lumart -W / lumart -W 1 for alternate camera)\n",
        "export_webp_disabled": "❌ WebP format (.webp) export has been permanently disabled. Please use .png or .jpg.",
        "export_sticker_mono_only": "ℹ️  Transparent background stickers (--transparent) are exclusive to Luris Mono (B&W). Exporting full image with terminal background for maximum color fidelity.",
        "export_success": "✨ Terminal art successfully exported to image: {}",
        "export_error": "❌ Error exporting image: {}",
        "pillow_not_found": "[luma] Pillow not found. Installing dependencies...",
        "usage": "Usage: lumart [options] <image_path>\n\nTry 'lumart --help' if you're too lazy to read docs.",
        "desc": "Lumart - Terminal Art Engine made by and for humans",
        "help_help": "Show this help message and exit.",
        "help_version": "Show program's version, system diagnostics, and engine status.",
        "help_completions": "Generate shell tab-completion script (bash, zsh, fish).",
        "help_image_path": "Path to the input image file (works best with transparent backgrounds).",
        "help_width": "Width of the output ASCII art (in characters). Default: auto-fit to terminal window.",
        "help_engine": "Select rendering engine: 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6), or 'spectra' (Spectra Weep 1.4 live webcam).",
        "help_webcam": "Stream live webcam feed to terminal (exclusive 'Spectra' engine).",
        "help_instant": "Disable progressive reveal effect and output immediately (default).",
        "help_reveal": "Enable progressive scan line-by-line reveal animation.",
        "help_transparent": "Export PNG sticker with transparent background (Luris Mono exclusive).",
        "help_history": "Show command execution history (optional: number of entries).",
        "help_replay": "Re-execute a previous command from history (default: last command).",
        "help_clear_history": "Clear the saved command history.",
        "help_paste": "Load image directly from the system clipboard.",
        "help_install_desktop": "Install Linux desktop entry and file manager right-click integration.",
        "help_color": "Force output in full TrueColor color mode.",
        "help_no_color": "Disable color output and route to monochrome engine.",
        "help_invert": "Invert the ASCII characters (useful for dark terminals).",
        "help_output": "Save the ASCII art to a file instead of printing to the console.",
        "help_blocks": "Use half-blocks (Color) or 2x2 Quadrant HD blocks (B&W) for high resolution.",
        "help_quadrants": "Use 2x2 Unicode quadrant blocks for ultra-dense subpixel rendering.",
        "help_sextants": "Use 2x3 Unicode sextant blocks for solid subpixel rendering (Mary Apex flagship).",
        "help_font_ratio": "Terminal font aspect ratio width/height calibration (default: 0.5).",
        "help_braille": "Use Braille characters for smooth edges and high resolution shape.",
        "help_boost": "Apply enhanced color saturation, contrast, and Retinex processing for vivid arcade-style output.",
        "help_swap": "Swap colors using names (e.g. --swap purple pink blue red). Must provide an even number of arguments.",
        "help_dither": "Dithering algorithm for B&W shading: 'atkinson' (default), 'floyd', 'bayer', or 'none'.",
        "help_manga": "Authentic Manga/Anime style (clean DoG lineart, 8x8 Bayer screentone).",
        "help_sketch": "Pure line art sketch mode (clean contours, no screentone or background noise).",
        "help_lang": "Force a specific language (en, es, pt, ru, ja, de, ko, fr).",
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
        "update_already_latest": "✅ Luma is already on the latest version (v{}). No actions were taken.",
        "already_on_version": "ℹ️ You are already on version v{}. No actions were taken.",
        "upgrade_target_older": "⚠️ Version v{} is older than currently installed (v{}).\n💡 To roll back to an earlier version, use: lumart -dg {}",
        "downgrade_target_newer": "⚠️ Version v{} is newer than currently installed (v{}).\n💡 To upgrade to a newer version, use: lumart -uu {}",
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
        "help_loop": "Play animated GIF/APNG in terminal loop (or export animation with -o <file.gif> / --save).",
        "help_fit": "Scale image to fit terminal window without vertical scrolling (incompatible with -w/--width).",
        "help_save": "Save rendered animated GIF to disk.",
        "help_fastfetch": "Output compact ANSI logo cropped of empty borders for Fastfetch / Neofetch.",
        "render_anim_export": "Rendering {} animation frames",
        "err_conflict_fit_width": "Incompatible options: -F/--fit and -w/--width cannot be used together (--fit dynamically computes optimal width to fit your terminal window).",
        "err_conflict_instant_reveal": "Incompatible options: --instant and --reveal are mutually exclusive (choose immediate rendering or progressive reveal animation).",
        "err_conflict_textures": "Incompatible texture flags: choose only one option among -S/--sextants, -B/--braille, -Q/--quadrants, or --blocks.",
        "err_conflict_styles": "Incompatible style flags: choose either -m/--manga (screentone halftones) or -s/--sketch (pure line contours).",
        "err_conflict_inputs": "Incompatible input sources: cannot specify a local image file alongside --paste or -W/--webcam.",
        "err_conflict_loop_static": "Incompatible format: --loop is an animated mode and cannot be exported to a static image format (.png/.jpg). To save the animation, explicitly specify an animated format (.gif), e.g.: -o output.gif or --save output.gif.",
        "err_conflict_transparent_jpg": "Incompatible format: --transparent requires export to .png (JPEG does not support alpha channel transparency).",
        "help_remove_bg": "Remove background from image without losing quality (-r, --remove-bg). If used without engine flags, saves HD transparent PNG.",
        "help_theme": "Synchronize colors with terminal theme (catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized).",
        "help_crt": "Simulate retro CRT scanlines and phosphor monitor (--crt [green|amber|color]).",
        "help_matrix": "Render image in digital Katakana and binary green Matrix code (--matrix).",
        "help_matrix_rain": "Play falling Katakana Matrix rain animation resolving into image (--matrix-rain).",
        "help_slideshow": "Play interactive terminal slideshow gallery for multiple images.",
        "help_delay": "Slideshow delay between images in seconds (default: 3.0).",
        "help_crop": "Crop image: 'center', 'square' (1:1), or 'x,y,w,h'.",
        "help_zoom": "Digital zoom factor centered on subject (e.g. --zoom 1.5).",
        "help_interactive": "Interactive live terminal adjustment TUI (-I, --interactive, --tui).",
        "help_copy": "Copy rendered ANSI art to system clipboard (-C, --copy).",
        "help_copy_plain": "Copy plain ASCII text (no ANSI color codes) to clipboard for Discord/Markdown.",
        "help_diff": "Visual side-by-side terminal image comparison (lumart diff <img1> <img2>).",
        "remove_bg_success": "✅ Background removed cleanly with zero quality loss: {} ({}x{})",
        "clipboard_copied_ansi": "Render copied to system clipboard (ANSI truecolor)!",
        "clipboard_copied_plain": "Render copied to system clipboard (plain ASCII)!",
        "diff_delta": "Average pixel color delta: {:.1f}%",
    },
    "es": {
        "diag_title_system": "📋 Información del Sistema y Runtime:",
        "diag_luma_ver": "Versión Luma:",
        "diag_exec_type": "Tipo de Ejecución:",
        "diag_standalone": "Ejecutable Independiente (PyInstaller)",
        "diag_script": "Script de Python",
        "diag_python_env": "Entorno Python:",
        "diag_platform_os": "Plataforma OS:",
        "diag_title_engines": "⚡ Motores de Renderizado:",
        "diag_trumble_desc": "Activo (Por defecto) (Cel-Shading Anime Ink Outlines, Capcom CPS-2 / Neo-Geo Color Punch, Lanczos, Bayer Dither, TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (Color Perceptual Apex 3.5):",
        "diag_mary_modes": "Modos Mary Soportados:",
        "diag_mary_modes_list": "sextants (bloques sólidos 2x3 HD), braille (2x4 bicolor), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (Monocromático Mono 2.6):",
        "diag_luris_modes": "Modos Luris Soportados:",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (DoG puro), blocks (cuadrantes 2x2 HD), ascii",
        "diag_dither_algos": "Algoritmos Tramado:",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (Cámara Web Weep 1.4):",
        "diag_spectra_avail": "Disponible (OpenCV 30-60 FPS Terminal Stream con 5 Filtros Weep en Vivo)",
        "diag_spectra_req": "Requiere opencv-python",
        "diag_title_terminal": "🖥️  Diagnóstico de Terminal:",
        "diag_res_label": "Resolución actual:",
        "diag_res_format": "{} columnas × {} filas",
        "diag_truecolor_label": "TrueColor (24-bit):",
        "diag_truecolor_supported": "✅ Soportado",
        "diag_truecolor_unsupported": "⚠️  No detectado (puede haber colores aproximados)",
        "diag_title_paths": "📁 Rutas y Configuración:",
        "diag_config_label": "Configuración:",
        "diag_config_exists": "Existe",
        "diag_config_default": "Predeterminado",
        "diag_backup_label": "Copias de Seguridad:",
        "diag_backup_count": "{} backups guardados",
        "diag_repo_label": "Repositorio GitHub:",
        "diag_native_active": "Activo ({})",
        "diag_native_active_bin": "Activo vía binario ({})",
        "diag_native_cpp": "Nativo C++ ({})",
        "diag_native_cpp_bin": "Nativo C++ vía binario ({})",
        "diag_py_fallback": "No detectado (usando fallback en Python)",
        "diag_mary_fallback": "Fallback en Python",
        "diag_not_available": "No disponible (usando Trumble)",
        "ver_status_title": "📦 Estado de Versiones de Luma:",
        "ver_current_installed": "Versión actual instalada:",
        "ver_latest_github": "Última versión en GitHub:",
        "ver_new_available": "💡 ¡Hay una nueva versión disponible!",
        "ver_release_title": "Título del release:",
        "ver_install_hint": "Para descargar e instalar automáticamente ejecuta:",
        "ver_up_to_date": "✅ ¡Tu instalación está al día con la versión más reciente!",
        "ver_recent_history": "📜 Historial de Versiones Recientes:",
        "ver_useful_commands": "💡 Comandos Útiles:",
        "ver_cmd_uu": "Descargar y aplicar última actualización",
        "ver_cmd_dg": "Selector interactivo para volver a versión anterior",
        "ver_cmd_v": "Ver diagnóstico completo del sistema",
        "ver_tag_current": "(actual)",
        "upg_avail_title": "🚀 Versiones disponibles para Upgrade:",
        "upg_recommended": "(Última versión recomendada)",
        "upg_cancel": "Cancelar",
        "upg_choose_prompt": "Elige una versión [1-{}] o presiona Enter para [1]: ",
        "upg_cancelled": "Operación cancelada.",
        "upg_invalid_sel": "❌ Selección inválida.",
        "upg_preparing": "⬇️  Preparando instalación de Luma v{}...",
        "upg_title": "Título:",
        "upg_backup_saved": "🛡️  Copia de seguridad de v{} guardada en: {}",
        "upg_backup_warn": "⚠️  Aviso: No se pudo crear la copia de seguridad previa ({}).",
        "upg_rollback_hint": "💡 Si deseas volver a la versión anterior en cualquier momento, ejecuta: lumart -dg",
        "dg_title": "⏪ Versiones disponibles para Restaurar (Downgrade):",
        "dg_choose_prompt": "Elige una versión para restaurar [1-{}] o presiona Enter para [1]: ",
        "hist_title": "📜 Historial de Comandos de Lumart ({} registrados):",
        "hist_empty": "  (No hay comandos registrados en el historial todavía)",
        "hist_header_num": "[#]",
        "hist_header_ver": "Ver",
        "hist_header_date": "Fecha / Hora",
        "hist_header_cmd": "Comando",
        "hist_replay_hint": "💡 Para re-ejecutar cualquiera usa: lumart --replay <número> (ej: lumart -R 1)",
        "hist_out_of_range": "❌ Índice [{}] fuera de rango. Hay {} comandos disponibles.",
        "hist_int_required": "❌ El índice debe ser un número entero (ej: lumart --replay 1).",
        "hist_replaying": "🚀 Re-ejecutando [{}]: {}",
        "hist_cleared": "✅ Historial de comandos de Lumart limpiado exitosamente.",
        "hist_already_empty": "ℹ️ El historial de comandos ya estaba vacío.",
        "desktop_installing": "🖥️  Instalando integración de escritorio y gestores de archivos...",
        "desktop_installed_launcher": "  ✅ Lanzador de escritorio instalado: {}",
        "desktop_launcher_error": "  ❌ Error creando {}: {}",
        "desktop_context_menu": "  ✅ Menú contextual de {}: {}",
        "desktop_completed": "🎉 ¡Integración completada exitosamente!\n   Ahora puedes hacer clic derecho sobre cualquier imagen en tu gestor de archivos\n   y seleccionar 'Abrir con Lumart' o 'Scripts > Abrir con Lumart'.",
        "spectra_webcam_only": "💡 El motor 'Spectra' es exclusivo para transmisión de vídeo y cámara web en tiempo real.\n   Para activarlo, usa:\n   lumart --webcam  (o: lumart -W / lumart -W 1 para otra cámara)\n",
        "export_webp_disabled": "❌ La exportación a formato WebP (.webp) ha sido deshabilitada permanentemente. Por favor use .png o .jpg.",
        "export_sticker_mono_only": "ℹ️  Los stickers con fondo transparente (--transparent) son exclusivos del motor Luris Mono (blanco y negro). Exportando imagen completa con fondo de terminal para máxima fidelidad de color.",
        "export_success": "✨ Arte terminal exportado exitosamente a imagen: {}",
        "export_error": "❌ Error al exportar imagen: {}",
        "pillow_not_found": "[luma] Pillow no encontrado. Instalando dependencias...",
        "usage": "Uso: lumart [opciones] <ruta_imagen>\n\nIntenta 'lumart --help' si te da pereza leer la documentación.",
        "desc": "Lumart - Motor de Arte de Terminal hecho por y para humanos",
        "help_help": "Mostrar este mensaje de ayuda y salir.",
        "help_version": "Mostrar versión del programa, diagnóstico del sistema y estado de aceleración.",
        "help_completions": "Generar script de autocompletado para el shell (bash, zsh, fish).",
        "help_image_path": "Ruta al archivo de imagen de entrada (funciona mejor con fondos transparentes).",
        "help_width": "Ancho del arte ASCII de salida (en caracteres). Por defecto: ancho real de la terminal.",
        "help_engine": "Seleccionar motor: 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6) o 'spectra' (Spectra Weep 1.4 en vivo).",
        "help_webcam": "Transmitir vídeo de cámara web en vivo a la terminal (motor exclusivo 'Spectra').",
        "help_instant": "Desactivar efecto de escaneo reveal y mostrar de inmediato (por defecto).",
        "help_reveal": "Activar animación progresiva de escaneo línea por línea.",
        "help_transparent": "Exportar sticker PNG con fondo transparente (exclusivo de Luris Mono).",
        "help_history": "Mostrar historial de comandos de Lumart (opcional: número de entradas).",
        "help_replay": "Re-ejecutar un comando previo del historial (por defecto: el último).",
        "help_clear_history": "Vaciar el historial de comandos guardado.",
        "help_paste": "Cargar imagen directamente desde el portapapeles del sistema.",
        "help_install_desktop": "Instalar integración de escritorio y clic derecho en gestores de archivos.",
        "help_color": "Forzar salida en modo color TrueColor.",
        "help_no_color": "Desactivar salida de color y usar motor blanco y negro.",
        "help_invert": "Invertir los caracteres ASCII (útil para terminales oscuras).",
        "help_output": "Guardar el arte ASCII en un archivo en lugar de imprimirlo en consola.",
        "help_blocks": "Usar medio-bloques (Color) o bloques cuadrantes 2x2 HD (B&W) para alta resolución.",
        "help_quadrants": "Usar bloques cuadrantes 2x2 Unicode para renderizado subpíxel ultra denso.",
        "help_sextants": "Usar bloques sextantes 2x3 Unicode para renderizado subpíxel sólido (buque insignia Mary Apex).",
        "help_font_ratio": "Calibración de relación aspecto ancho/alto de fuente de terminal (por defecto: 0.5).",
        "help_braille": "Usar caracteres Braille para bordes suaves y formas de alta resolución.",
        "help_boost": "Aplicar saturación, contraste y procesamiento Retinex para una salida vibrante estilo arcade.",
        "help_swap": "Intercambiar colores por nombre (ej. --swap purple pink blue red). Debe ser un número par de argumentos.",
        "help_dither": "Algoritmo de tramado: 'atkinson' (por defecto), 'floyd', 'bayer' o 'none'.",
        "help_manga": "Estilo Manga/Anime auténtico (trazos limpios DoG, sombreado screentone 8x8 Bayer).",
        "help_sketch": "Modo boceto de trazo puro (contornos limpios sin sombreado ni ruido de fondo).",
        "help_lang": "Forzar un idioma específico (en, es, pt, ru, ja, de, ko, fr).",
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
        "update_already_latest": "✅ Luma ya está en la versión más reciente (v{}). No se tomaron acciones.",
        "already_on_version": "ℹ️ Ya estás en la versión v{}. No se tomaron acciones.",
        "upgrade_target_older": "⚠️ La versión v{} es anterior a la instalada actualmente (v{}).\n💡 Para volver a una versión anterior, utiliza: lumart -dg {}",
        "downgrade_target_newer": "⚠️ La versión v{} es superior a la instalada actualmente (v{}).\n💡 Para actualizar a una versión más reciente, utiliza: lumart -uu {}",
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
        "help_loop": "Reproducir GIF/APNG animado en bucle en terminal (o exportar animación con -o <archivo.gif> / --save).",
        "help_fit": "Ajustar imagen para que quepa en la ventana del terminal sin scroll vertical (incompatible con -w/--width).",
        "help_save": "Guardar GIF animado renderizado en disco.",
        "help_fastfetch": "Generar logo ANSI compacto sin márgenes vacíos para Fastfetch / Neofetch.",
        "render_anim_export": "Renderizando {} fotogramas de animación",
        "err_conflict_fit_width": "Opciones incompatibles: -F/--fit y -w/--width no pueden usarse juntos (--fit calcula automáticamente el ancho óptimo para encajar en tu terminal).",
        "err_conflict_instant_reveal": "Opciones incompatibles: --instant y --reveal son mutuamente excluyentes (elige renderizado inmediato o animación progresiva).",
        "err_conflict_textures": "Texturas incompatibles: elige solo una opción entre -S/--sextants, -B/--braille, -Q/--quadrants o --blocks.",
        "err_conflict_styles": "Estilos incompatibles: elige entre -m/--manga (tramas screentone) o -s/--sketch (líneas de contorno puras).",
        "err_conflict_inputs": "Fuentes de entrada en conflicto: no puedes especificar una imagen en disco junto a --paste o -W/--webcam.",
        "err_conflict_loop_static": "Incompatibilidad de formato: --loop es un modo animado y no puede exportarse a una imagen estática (.png/.jpg). Para guardar la animación completa, especifica explícitamente un archivo .gif (ej: -o salida.gif o --save salida.gif).",
        "err_conflict_transparent_jpg": "Incompatibilidad de formato: --transparent requiere exportación en formato .png (el formato JPEG no admite canal alfa transparente).",
        "help_remove_bg": "Quitar el fondo sin perder calidad (-r, --remove-bg). Si se usa solo, guarda PNG transparente HD sin aplicar modelos ASCII.",
        "help_theme": "Sincronizar colores con tema de terminal (catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized).",
        "help_crt": "Simular monitor CRT retro con líneas de barrido y fósforo (--crt [green|amber|color]).",
        "help_matrix": "Renderizar imagen en glifos Katakana y código binario Matrix verde (--matrix).",
        "help_matrix_rain": "Animación de lluvia de código Matrix que se ensambla en la imagen (--matrix-rain).",
        "help_slideshow": "Pase interactivo de diapositivas en terminal para múltiples imágenes.",
        "help_delay": "Tiempo de espera en segundos entre imágenes del slideshow (defecto: 3.0).",
        "help_crop": "Recortar imagen: 'center', 'square' (1:1) o 'x,y,w,h'.",
        "help_zoom": "Factor de zoom digital centrado en el sujeto (ej. --zoom 1.5).",
        "help_interactive": "Modo TUI interactivo en vivo en terminal (-I, --interactive, --tui).",
        "help_copy": "Copiar arte ANSI generado al portapapeles del sistema (-C, --copy).",
        "help_copy_plain": "Copiar texto ASCII plano (sin códigos de color) al portapapeles para Discord/Markdown.",
        "help_diff": "Comparación visual de imágenes lado a lado en la terminal (lumart diff <img1> <img2>).",
        "remove_bg_success": "✅ Fondo removido exitosamente sin pérdida de calidad: {} ({}x{})",
        "clipboard_copied_ansi": "¡Arte copiado al portapapeles del sistema (ANSI truecolor)!",
        "clipboard_copied_plain": "¡Arte copiado al portapapeles del sistema (ASCII plano)!",
        "diff_delta": "Variación cromática media (Delta): {:.1f}%",
    },
    "pt": {
        "diag_title_system": "📋 Informações do Sistema e Runtime:",
        "diag_luma_ver": "Versão Luma:",
        "diag_exec_type": "Tipo de Execução:",
        "diag_standalone": "Executável Independente (PyInstaller)",
        "diag_script": "Script Python",
        "diag_python_env": "Ambiente Python:",
        "diag_platform_os": "Plataforma do SO:",
        "diag_title_engines": "⚡ Motores de Renderização:",
        "diag_trumble_desc": "Ativo (Padrão) (Cel-Shading Anime Ink Outlines, Capcom CPS-2 / Neo-Geo Color Punch, Lanczos, Bayer Dither, TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (Cor Perceptual Apex 3.5):",
        "diag_mary_modes": "Modos Mary Suportados:",
        "diag_mary_modes_list": "sextants (blocos sólidos 2x3 HD), braille (2x4 bicolor), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (Monocromático Mono 2.6):",
        "diag_luris_modes": "Modos Luris Suportados:",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (DoG puro), blocks (quadrantes 2x2 HD), ascii",
        "diag_dither_algos": "Algoritmos de Pontilhamento:",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (Webcam ao Vivo Weep 1.4):",
        "diag_spectra_avail": "Disponível (Transmissão de Terminal OpenCV 30-60 FPS com 5 Filtros Weep ao Vivo)",
        "diag_spectra_req": "Requer opencv-python",
        "diag_title_terminal": "🖥️  Diagnóstico do Terminal:",
        "diag_res_label": "Resolução atual:",
        "diag_res_format": "{} colunas × {} linhas",
        "diag_truecolor_label": "TrueColor (24-bit):",
        "diag_truecolor_supported": "✅ Suportado",
        "diag_truecolor_unsupported": "⚠️  Não detectado (as cores podem ser aproximadas)",
        "diag_title_paths": "📁 Caminhos e Configuração:",
        "diag_config_label": "Configuração:",
        "diag_config_exists": "Existe",
        "diag_config_default": "Padrão",
        "diag_backup_label": "Cópias de Segurança:",
        "diag_backup_count": "{} backups salvos",
        "diag_repo_label": "Repositório GitHub:",
        "diag_native_active": "Ativo ({})",
        "diag_native_active_bin": "Ativo via binário ({})",
        "diag_native_cpp": "Nativo C++ ({})",
        "diag_native_cpp_bin": "Nativo C++ via binário ({})",
        "diag_py_fallback": "Não detectado (usando fallback em Python)",
        "diag_mary_fallback": "Fallback em Python",
        "diag_not_available": "Não disponível (usando Trumble)",
        "ver_status_title": "📦 Status de Versões do Luma:",
        "ver_current_installed": "Versão atual instalada:",
        "ver_latest_github": "Última versão no GitHub:",
        "ver_new_available": "💡 Uma nova versão está disponível!",
        "ver_release_title": "Título do lançamento:",
        "ver_install_hint": "Para baixar e instalar automaticamente, execute:",
        "ver_up_to_date": "✅ Sua instalação está atualizada com a versão mais recente!",
        "ver_recent_history": "📜 Histórico de Versões Recientes:",
        "ver_useful_commands": "💡 Comandos Úteis:",
        "ver_cmd_uu": "Baixar e aplicar a atualização mais recente",
        "ver_cmd_dg": "Seletor interativo para reverter para versão anterior",
        "ver_cmd_v": "Ver diagnóstico completo do sistema",
        "ver_tag_current": "(atual)",
        "upg_avail_title": "🚀 Versões disponíveis para Upgrade:",
        "upg_recommended": "(Última versão recomendada)",
        "upg_cancel": "Cancelar",
        "upg_choose_prompt": "Escolha uma versão [1-{}] ou pressione Enter para [1]: ",
        "upg_cancelled": "Operação cancelada.",
        "upg_invalid_sel": "❌ Seleção inválida.",
        "upg_preparing": "⬇️  Preparando instalação do Luma v{}...",
        "upg_title": "Título:",
        "upg_backup_saved": "🛡️  Cópia de segurança da v{} salva em: {}",
        "upg_backup_warn": "⚠️  Aviso: Não foi possível criar cópia de segurança ({}).",
        "upg_rollback_hint": "💡 Para voltar à versão anterior a qualquer momento, execute: lumart -dg",
        "dg_title": "⏪ Versões disponíveis para Reverter (Downgrade):",
        "dg_choose_prompt": "Escolha uma versão para restaurar [1-{}] ou pressione Enter para [1]: ",
        "hist_title": "📜 Histórico de Comandos do Lumart ({} registrados):",
        "hist_empty": "  (Nenhum comando registrado no histórico ainda)",
        "hist_header_num": "[#]",
        "hist_header_ver": "Ver",
        "hist_header_date": "Data / Hora",
        "hist_header_cmd": "Comando",
        "hist_replay_hint": "💡 Para reexecutar qualquer comando: lumart --replay <número> (ex: lumart -R 1)",
        "hist_out_of_range": "❌ Índice [{}] fora do intervalo. Existem {} comandos disponíveis.",
        "hist_int_required": "❌ O índice deve ser um número inteiro (ex: lumart --replay 1).",
        "hist_replaying": "🚀 Reexecutando [{}]: {}",
        "hist_cleared": "✅ Histórico de comandos do Lumart limpo com sucesso.",
        "hist_already_empty": "ℹ️ O histórico de comandos já estava vazio.",
        "desktop_installing": "🖥️  Instalando integração com área de trabalho e gerenciadores de arquivos...",
        "desktop_installed_launcher": "  ✅ Atalho de área de trabalho instalado: {}",
        "desktop_launcher_error": "  ❌ Erro ao criar {}: {}",
        "desktop_context_menu": "  ✅ Menu de contexto do {}: {}",
        "desktop_completed": "🎉 Integração concluída com sucesso!\n   Agora você pode clicar com o botão direito em qualquer imagem no gerenciador de arquivos e selecionar 'Abrir com Lumart'.",
        "spectra_webcam_only": "💡 O motor 'Spectra' é exclusivo para transmissão de vídeo e webcam em tempo real.\n   Para ativá-lo, use:\n   lumart --webcam  (ou: lumart -W / lumart -W 1 para outra câmera)\n",
        "export_webp_disabled": "❌ A exportação para o formato WebP (.webp) foi desativada permanentemente. Use .png ou .jpg.",
        "export_sticker_mono_only": "ℹ️  Adesivos com fundo transparente (--transparent) são exclusivos do motor Luris Mono (preto e branco). Exportando imagem completa com fundo do terminal.",
        "export_success": "✨ Arte de terminal exportada com sucesso para imagem: {}",
        "export_error": "❌ Erro ao exportar imagem: {}",
        "pillow_not_found": "[luma] Pillow não encontrado. Instalando dependências...",
        "usage": "Uso: lumart [opções] <caminho_imagem>\n\nTente 'lumart --help' para mais opções.",
        "desc": "Lumart - Motor de Arte de Terminal",
        "help_help": "Mostrar esta mensagem de ajuda e sair.",
        "help_version": "Mostrar o número da versão do programa, diagnóstico e status do motor.",
        "help_completions": "Gerar script de autocompletamento para o terminal (bash, zsh, fish).",
        "help_image_path": "Caminho para o arquivo de imagem de entrada (funciona melhor com fundos transparentes).",
        "help_width": "Largura da arte ASCII de saída (em caracteres). Padrão: largura real do terminal.",
        "help_engine": "Selecionar motor: 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6) ou 'spectra' (Spectra Weep 1.4 ao vivo).",
        "help_webcam": "Transmitir vídeo de webcam ao vivo para o terminal (motor exclusivo 'Spectra').",
        "help_instant": "Desativar efeito de revelação progressiva e exibir imediatamente (padrão).",
        "help_reveal": "Ativar animação de varredura progressiva linha por linha.",
        "help_transparent": "Exportar sticker PNG com fundo transparente (exclusivo do Luris Mono).",
        "help_history": "Mostrar histórico de comandos do Lumart (opcional: número de entradas).",
        "help_replay": "Reexecutar um comando anterior do histórico (padrão: o último).",
        "help_clear_history": "Limpar o histórico de comandos salvo.",
        "help_paste": "Carregar imagem diretamente da área de transferência do sistema.",
        "help_install_desktop": "Instalar atalho de área de trabalho e integração de clique direito no gerenciador de arquivos.",
        "help_color": "Forçar saída em modo colorido TrueColor.",
        "help_no_color": "Desativar saída de cor e usar motor monocromático.",
        "help_invert": "Inverter os caracteres ASCII (útil para terminais escuros).",
        "help_output": "Salvar a arte ASCII em um arquivo em vez de imprimir no console.",
        "help_blocks": "Usar meios-blocos ou blocos quadrantes 2x2 para alta resolução.",
        "help_quadrants": "Usar blocos de quadrantes 2x2 Unicode para renderização subpíxel ultradensa.",
        "help_sextants": "Usar blocos sextantes 2x3 Unicode para renderização subpixel sólida (carro-chefe Mary Apex).",
        "help_font_ratio": "Calibração de proporção largura/altura da fonte do terminal (padrão: 0.5).",
        "help_braille": "Usar caracteres Braille para bordas suaves e formas de alta resolução.",
        "help_boost": "Aplicar saturação, contraste e processamento Retinex para saída vibrante estilo arcade.",
        "help_swap": "Trocar cores usando nomes (ex: --swap purple pink blue red). Deve fornecer um número par de argumentos.",
        "help_dither": "Algoritmo de pontilhamento: 'atkinson' (padrão), 'floyd', 'bayer' ou 'none'.",
        "help_manga": "Estilo Manga/Anime autêntico (traços limpos DoG, sombreamento retícula 8x8).",
        "help_sketch": "Modo esboço de linha pura (contornos limpos sem retícula).",
        "help_lang": "Forçar um idioma específico (en, es, pt, ru, ja, de, ko, fr).",
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
        "update_already_latest": "✅ O Luma já está na versão mais recente (v{}). Nenhuma ação foi realizada.",
        "already_on_version": "ℹ️ Você já está na versão v{}. Nenhuma ação foi realizada.",
        "upgrade_target_older": "⚠️ A versão v{} é mais antiga que a versão instalada atualmente (v{}).\n💡 Para reverter para uma versão anterior, use: lumart -dg {}",
        "downgrade_target_newer": "⚠️ A versão v{} é mais recente que a versão instalada atualmente (v{}).\n💡 Para atualizar para uma versão mais recente, use: lumart -uu {}",
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
        "help_loop": "Reproduzir GIF/APNG animado em loop no terminal (ou exportar com -o <arquivo.gif> / --save).",
        "help_fit": "Ajustar imagem à janela do terminal sem rolagem vertical (incompatível com -w/--width).",
        "help_save": "Salvar GIF animado renderizado no disco.",
        "help_fastfetch": "Gerar logo ANSI compacto sem bordas vazias para Fastfetch / Neofetch.",
        "render_anim_export": "Renderizando {} quadros de animação",
        "err_conflict_fit_width": "Opções incompatíveis: -F/--fit e -w/--width não podem ser usados juntos (--fit calcula a largura ideal para sua janela).",
        "err_conflict_instant_reveal": "Opções incompatíveis: --instant e --reveal são mutuamente exclusivos.",
        "err_conflict_textures": "Texturas incompatíveis: escolha apenas uma opção entre -S/--sextants, -B/--braille, -Q/--quadrants ou --blocks.",
        "err_conflict_styles": "Estilos incompatíveis: escolha entre -m/--manga (retículas) ou -s/--sketch (contornos puros).",
        "err_conflict_inputs": "Fontes em conflito: não especifique arquivo de imagem junto a --paste ou -W/--webcam.",
        "err_conflict_loop_static": "Formato incompatível: --loop não pode ser exportado para formato estático (.png/.jpg). Especifique .gif (ex: -o saida.gif).",
        "err_conflict_transparent_jpg": "Formato incompatível: --transparent requer exportação em .png (JPEG não suporta canal alfa).",
        "help_remove_bg": "Remover fundo da imagem sem perder qualidade (-r, --remove-bg). Se usado sozinho, salva PNG transparente HD.",
        "help_theme": "Sincronizar cores com tema do terminal (catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized).",
        "help_crt": "Simular monitor CRT retrô com linhas de varredura (--crt [green|amber|color]).",
        "help_matrix": "Renderizar imagem em glifos Katakana e código Matrix verde (--matrix).",
        "help_matrix_rain": "Animação de chuva de código Matrix que se transforma na imagem (--matrix-rain).",
        "help_slideshow": "Apresentação interativa de slides no terminal para várias imagens.",
        "help_delay": "Tempo de espera em segundos entre as imagens da apresentação (padrão: 3.0).",
        "help_crop": "Recortar imagem: 'center', 'square' (1:1) ou 'x,y,w,h'.",
        "help_zoom": "Fator de zoom digital centralizado (ex.: --zoom 1.5).",
        "help_interactive": "Modo TUI interativo em tempo real no terminal (-I, --interactive, --tui).",
        "help_copy": "Copiar arte ANSI gerada para a área de transferência (-C, --copy).",
        "help_copy_plain": "Copiar texto ASCII simples para a área de transferência para Discord/Markdown.",
        "help_diff": "Comparação visual de imagens lado a lado no terminal (lumart diff <img1> <img2>).",
        "remove_bg_success": "✅ Fundo removido com sucesso sem perda de qualidade: {} ({}x{})",
        "clipboard_copied_ansi": "Arte copiada para a área de transferência (ANSI truecolor)!",
        "clipboard_copied_plain": "Arte copiada para a área de transferência (ASCII simples)!",
        "diff_delta": "Variação cromática média (Delta): {:.1f}%",
    },
    "ru": {
        "diag_title_system": "📋 Информация о системе и среде выполнения:",
        "diag_luma_ver": "Версия Luma:",
        "diag_exec_type": "Тип запуска:",
        "diag_standalone": "Автономный исполняемый файл (PyInstaller)",
        "diag_script": "Скрипт Python",
        "diag_python_env": "Окружение Python:",
        "diag_platform_os": "Платформа ОС:",
        "diag_title_engines": "⚡ Движки рендеринга:",
        "diag_trumble_desc": "Активен (По умолчанию) (Cel-Shading Anime Ink Outlines, палитра Capcom CPS-2 / Neo-Geo, Lanczos, дизеринг Байера, TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (Перцептивный цвет Apex 3.5):",
        "diag_mary_modes": "Поддерживаемые режимы Mary:",
        "diag_mary_modes_list": "sextants (сплошные блоки 2x3 HD), braille (2x4 двухцветный), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (Монохромный Mono 2.6):",
        "diag_luris_modes": "Поддерживаемые режимы Luris:",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (чистый DoG), blocks (квадранты 2x2 HD), ascii",
        "diag_dither_algos": "Алгоритмы дизеринга:",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (Веб-камера в реальном времени Weep 1.4):",
        "diag_spectra_avail": "Доступен (Терминальный поток OpenCV 30-60 кадров/с с 5 живыми фильтрами Weep)",
        "diag_spectra_req": "Требуется opencv-python",
        "diag_title_terminal": "🖥️  Диагностика терминала:",
        "diag_res_label": "Текущее разрешение:",
        "diag_res_format": "{} колонок × {} строк",
        "diag_truecolor_label": "TrueColor (24-бит):",
        "diag_truecolor_supported": "✅ Поддерживается",
        "diag_truecolor_unsupported": "⚠️  Не обнаружено (цвета могут быть приближенными)",
        "diag_title_paths": "📁 Пути и конфигурация:",
        "diag_config_label": "Конфигурация:",
        "diag_config_exists": "Существует",
        "diag_config_default": "По умолчанию",
        "diag_backup_label": "Резервные копии:",
        "diag_backup_count": "{} резервных копий сохранено",
        "diag_repo_label": "Репозиторий GitHub:",
        "diag_native_active": "Активен ({})",
        "diag_native_active_bin": "Активен через бинарник ({})",
        "diag_native_cpp": "Нативный C++ ({})",
        "diag_native_cpp_bin": "Нативный C++ через бинарник ({})",
        "diag_py_fallback": "Не обнаружен (используется резервный вариант на Python)",
        "diag_mary_fallback": "Резервный вариант на Python",
        "diag_not_available": "Недоступен (используется Trumble)",
        "ver_status_title": "📦 Статус версий Luma:",
        "ver_current_installed": "Текущая установленная версия:",
        "ver_latest_github": "Последняя версия на GitHub:",
        "ver_new_available": "💡 Доступна новая версия!",
        "ver_release_title": "Название релиза:",
        "ver_install_hint": "Для автоматической загрузки и установки выполните:",
        "ver_up_to_date": "✅ Ваша установка обновлена до самой последней версии!",
        "ver_recent_history": "📜 Недавняя история версий:",
        "ver_useful_commands": "💡 Полезные команды:",
        "ver_cmd_uu": "Загрузить и применить последнее обновление",
        "ver_cmd_dg": "Интерактивный выбор для отката на предыдущую версию",
        "ver_cmd_v": "Просмотреть полную диагностику системы",
        "ver_tag_current": "(текущая)",
        "upg_avail_title": "🚀 Доступные версии для Upgrade:",
        "upg_recommended": "(Последняя рекомендуемая версия)",
        "upg_cancel": "Отмена",
        "upg_choose_prompt": "Выберите версию [1-{}] или нажмите Enter для [1]: ",
        "upg_cancelled": "Операция отменена.",
        "upg_invalid_sel": "❌ Неверный выбор.",
        "upg_preparing": "⬇️  Подготовка к установке Luma v{}...",
        "upg_title": "Заголовок:",
        "upg_backup_saved": "🛡️  Резервная копия v{} сохранена в: {}",
        "upg_backup_warn": "⚠️  Предупреждение: Не удалось создать резервную копию ({}).",
        "upg_rollback_hint": "💡 Чтобы вернуться к предыдущей версии в любое время, выполните: lumart -dg",
        "dg_title": "⏪ Доступные версии для отката (Downgrade):",
        "dg_choose_prompt": "Выберите версию для восстановления [1-{}] или нажмите Enter для [1]: ",
        "hist_title": "📜 История команд Lumart (записано: {}):",
        "hist_empty": "  (В истории пока нет зарегистрированных команд)",
        "hist_header_num": "[#]",
        "hist_header_ver": "Вер",
        "hist_header_date": "Дата / Время",
        "hist_header_cmd": "Команда",
        "hist_replay_hint": "💡 Для повторного выполнения используйте: lumart --replay <номер> (напр.: lumart -R 1)",
        "hist_out_of_range": "❌ Индекс [{}] вне диапазона. Доступно {} команд.",
        "hist_int_required": "❌ Индекс должен быть целым числом (напр.: lumart --replay 1).",
        "hist_replaying": "🚀 Повторное выполнение [{}]: {}",
        "hist_cleared": "✅ История команд Lumart успешно очищена.",
        "hist_already_empty": "ℹ️ История команд уже была пуста.",
        "desktop_installing": "🖥️  Установка интеграции с рабочим столом и файловыми менеджерами...",
        "desktop_installed_launcher": "  ✅ Ярлык рабочего стола установлен: {}",
        "desktop_launcher_error": "  ❌ Ошибка создания {}: {}",
        "desktop_context_menu": "  ✅ Контекстное меню {}: {}",
        "desktop_completed": "🎉 Интеграция с рабочим столом успешно завершена!\n   Теперь вы можете нажать правой кнопкой мыши на любое изображение в файловом менеджере и выбрать 'Открыть с помощью Lumart'.",
        "spectra_webcam_only": "💡 Движок 'Spectra' предназначен исключительно для потоковой передачи видео и веб-камеры в реальном времени.\n   Для запуска используйте:\n   lumart --webcam  (или: lumart -W / lumart -W 1 для другой камеры)\n",
        "export_webp_disabled": "❌ Экспорт в формат WebP (.webp) навсегда отключен. Пожалуйста, используйте .png или .jpg.",
        "export_sticker_mono_only": "ℹ️  Стикеры с прозрачным фоном (--transparent) доступны только для Luris Mono (ч/б). Полное изображение экспортируется с фоном терминала.",
        "export_success": "✨ Терминал-арт успешно экспортирован в изображение: {}",
        "export_error": "❌ Ошибка при экспорте изображения: {}",
        "pillow_not_found": "[luma] Pillow не найден. Установка зависимостей...",
        "usage": "Использование: lumart [опции] <путь_к_изображению>\n\nПопробуйте 'lumart --help' для дополнительных опций.",
        "desc": "Lumart - Движок терминального искусства",
        "help_help": "Показать это справочное сообщение и выйти.",
        "help_version": "Показать версию программы, диагностику системы и статус движка.",
        "help_completions": "Сгенерировать скрипт автодополнения для командной строки (bash, zsh, fish).",
        "help_image_path": "Путь к исходному файлу изображения (лучше всего работает с прозрачным фоном).",
        "help_width": "Ширина выходного ASCII-арта (в символах). По умолчанию: ширина окна терминала.",
        "help_engine": "Выбор движка рендеринга: 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6) или 'spectra' (Spectra Weep 1.4 веб-камера).",
        "help_webcam": "Трансляция видео с веб-камеры в терминал (эксклюзивный движок 'Spectra').",
        "help_instant": "Отключить эффект прогрессивного сканирования и выводить мгновенно (по умолчанию).",
        "help_reveal": "Включить построчную анимацию прогрессивного сканирования.",
        "help_transparent": "Экспортировать PNG-стикер с прозрачным фоном (только для Luris Mono).",
        "help_history": "Показать историю команд Lumart (опционально: количество записей).",
        "help_replay": "Повторно выполнить предыдущую команду из истории (по умолчанию: последнюю).",
        "help_clear_history": "Очистить сохраненную историю команд.",
        "help_paste": "Загрузить изображение прямо из системного буфера обмена.",
        "help_install_desktop": "Установить ярлык на рабочий стол и контекстное меню файлового менеджера.",
        "help_color": "Принудительный вывод в полноцветном режиме TrueColor.",
        "help_no_color": "Отключить цветной вывод и использовать черно-белый движок.",
        "help_invert": "Инвертировать символы ASCII (полезно для темных терминалов).",
        "help_output": "Сохранить ASCII-арт в файл вместо вывода в консоль.",
        "help_blocks": "Использовать полублоки или 2x2 квадранты для высокого разрешения.",
        "help_quadrants": "Использовать квадранты 2x2 Unicode для сверхплотного субпиксельного рендеринга.",
        "help_sextants": "Использовать блоки секстантов Unicode 2x3 для сплошного субпиксельного рендеринга (Mary Apex).",
        "help_font_ratio": "Калибровка соотношения сторон шрифта терминала ширина/высота (по умолчанию: 0.5).",
        "help_braille": "Использовать шрифт Брайля для сглаженных краев и высокого разрешения.",
        "help_boost": "Применить усиленную насыщенность, контраст и обработку Retinex для яркого аркадного вывода.",
        "help_swap": "Менять цвета по названию (напр. --swap purple pink blue red). Должно быть четное количество аргументов.",
        "help_dither": "Алгоритм дизеринга: 'atkinson' (по умолчанию), 'floyd', 'bayer' или 'none'.",
        "help_manga": "Стиль манги/аниме (чистый лайн-арт DoG, скринтоны 8x8).",
        "help_sketch": "Режим чистого эскиза (четкие контуры без растра).",
        "help_lang": "Принудительно установить язык (en, es, pt, ru, ja, de, ko, fr).",
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
        "update_already_latest": "✅ Luma уже обновлена до последней версии (v{}). Никаких действий не выполнено.",
        "already_on_version": "ℹ️ Вы уже используете версию v{}. Никаких действий не выполнено.",
        "upgrade_target_older": "⚠️ Версия v{} старее текущей установленной версии (v{}).\n💡 Чтобы откатиться к более ранней версии, используйте: lumart -dg {}",
        "downgrade_target_newer": "⚠️ Версия v{} новее текущей установленной версии (v{}).\n💡 Для обновления до более новой версии используйте: lumart -uu {}",
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
        "help_loop": "Воспроизведение GIF/APNG в терминале (или экспорт с -o <файл.gif> / --save).",
        "help_fit": "Масштабировать по окну терминала без прокрутки (несовместимо с -w/--width).",
        "help_save": "Сохранить анимированный GIF на диск.",
        "help_fastfetch": "Компактный ANSI логотип для Fastfetch / Neofetch.",
        "render_anim_export": "Рендеринг {} кадров анимации",
        "err_conflict_fit_width": "Несовместимые опции: -F/--fit и -w/--width нельзя использовать вместе.",
        "err_conflict_instant_reveal": "Несовместимые опции: --instant и --reveal взаимоисключающие.",
        "err_conflict_textures": "Несовместимые текстуры: выберите только одну из -S, -B, -Q или --blocks.",
        "err_conflict_styles": "Несовместимые стили: выберите либо -m/--manga, либо -s/--sketch.",
        "err_conflict_inputs": "Конфликт источников: нельзя указывать файл вместе с --paste или -W/--webcam.",
        "err_conflict_loop_static": "Несовместимый формат: --loop нельзя экспортировать в статичный формат (.png/.jpg). Укажите .gif (напр. -o out.gif).",
        "err_conflict_transparent_jpg": "Несовместимый формат: --transparent требует формат .png (JPEG не поддерживает альфа-канал).",
        "help_remove_bg": "Удалить фон изображения без потери качества (-r, --remove-bg). Без флагов моделей сохраняет прозрачный PNG.",
        "help_theme": "Синхронизировать цвета с темой терминала (catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized).",
        "help_crt": "Эмулировать ретро-ЭЛТ монитор со сканлайнами (--crt [green|amber|color]).",
        "help_matrix": "Отобразить изображение в виде зеленого матричного кода Katakana (--matrix).",
        "help_matrix_rain": "Анимация падающего дождя Matrix, переходящая в изображение (--matrix-rain).",
        "help_slideshow": "Интерактивное слайд-шоу в терминале для нескольких изображений.",
        "help_delay": "Задержка между изображениями слайд-шоу в секундах (по умолчанию: 3.0).",
        "help_crop": "Обрезать изображение: 'center', 'square' (1:1) или 'x,y,w,h'.",
        "help_zoom": "Коэффициент цифрового зума по центру (напр., --zoom 1.5).",
        "help_interactive": "Интерактивный TUI-режим настройки в реальном времени (-I, --interactive, --tui).",
        "help_copy": "Скопировать ANSI-арт в буфер обмена системы (-C, --copy).",
        "help_copy_plain": "Скопировать чистый ASCII-текст без цветов в буфер обмена для Discord/Markdown.",
        "help_diff": "Визуальное сравнение изображений бок о бок в терминале (lumart diff <img1> <img2>).",
        "remove_bg_success": "✅ Фон успешно удален без потери качества: {} ({}x{})",
        "clipboard_copied_ansi": "Арт скопирован в буфер обмена (ANSI truecolor)!",
        "clipboard_copied_plain": "Арт скопирован в буфер обмена (чистый ASCII)!",
        "diff_delta": "Средняя цветовая разница (Delta): {:.1f}%",
    },
    "ja": {
        "diag_title_system": "📋 システムおよびランタイム診断:",
        "diag_luma_ver": "Lumaバージョン:",
        "diag_exec_type": "実行タイプ:",
        "diag_standalone": "スタンドアロン実行可能ファイル (PyInstaller)",
        "diag_script": "Pythonスクリプト",
        "diag_python_env": "Python環境:",
        "diag_platform_os": "OSプラットフォーム:",
        "diag_title_engines": "⚡ レンダリングエンジン:",
        "diag_trumble_desc": "有効 (デフォルト) (アニメインク輪郭セルシェーディング、Capcom CPS-2 / Neo-Geo鮮烈パレット、Lanczos、Bayerディザ、TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (知覚的カラー Apex 3.5):",
        "diag_mary_modes": "サポートされているMaryモード:",
        "diag_mary_modes_list": "sextants (2x3ソリッドHDブロック), braille (2x4デュアルカラー), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (モノクローム Mono 2.6):",
        "diag_luris_modes": "サポートされているLurisモード:",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (純DoG), blocks (2x2 HD象限), ascii",
        "diag_dither_algos": "ディザリングアルゴリズム:",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (ライブWebカメラ Weep 1.4):",
        "diag_spectra_avail": "利用可能 (OpenCV 30-60 FPS ターミナルストリーム、5つのライブWeepフィルター搭載)",
        "diag_spectra_req": "opencv-python が必要です",
        "diag_title_terminal": "🖥️  ターミナル診断:",
        "diag_res_label": "現在の解像度:",
        "diag_res_format": "{} 列 × {} 行",
        "diag_truecolor_label": "TrueColor (24ビット):",
        "diag_truecolor_supported": "✅ サポートされています",
        "diag_truecolor_unsupported": "⚠️  未検出 (色が近似される場合があります)",
        "diag_title_paths": "📁 パスと設定:",
        "diag_config_label": "設定:",
        "diag_config_exists": "存在します",
        "diag_config_default": "デフォルト",
        "diag_backup_label": "バックアップ:",
        "diag_backup_count": "{} 件のバックアップが保存されています",
        "diag_repo_label": "GitHubリポジトリ:",
        "diag_native_active": "有効 ({})",
        "diag_native_active_bin": "バイナリ経由で有効 ({})",
        "diag_native_cpp": "ネイティブ C++ ({})",
        "diag_native_cpp_bin": "バイナリ経由のネイティブ C++ ({})",
        "diag_py_fallback": "未検出 (Pythonフォールバックを使用)",
        "diag_mary_fallback": "Pythonフォールバック",
        "diag_not_available": "利用不可 (Trumbleを使用)",
        "ver_status_title": "📦 Lumaのバージョンステータス:",
        "ver_current_installed": "現在インストールされているバージョン:",
        "ver_latest_github": "GitHub上の最新バージョン:",
        "ver_new_available": "💡 新しいバージョンが利用可能です！",
        "ver_release_title": "リリースタイトル:",
        "ver_install_hint": "自動ダウンロードおよびインストールを行うには次を実行してください:",
        "ver_up_to_date": "✅ お使いの環境は最新バージョンに更新されています！",
        "ver_recent_history": "📜 最近のバージョン履歴:",
        "ver_useful_commands": "💡 便利なコマンド:",
        "ver_cmd_uu": "最新の更新プログラムをダウンロードして適用",
        "ver_cmd_dg": "以前のバージョンにロールバックするための対話型セレクター",
        "ver_cmd_v": "完全なシステム診断レポートを表示",
        "ver_tag_current": "(現在)",
        "upg_avail_title": "🚀 アップグレード可能なバージョン:",
        "upg_recommended": "(最新推奨バージョン)",
        "upg_cancel": "キャンセル",
        "upg_choose_prompt": "バージョンを選択 [1-{}] または Enter で [1]: ",
        "upg_cancelled": "操作がキャンセルされました。",
        "upg_invalid_sel": "❌ 無効な選択です。",
        "upg_preparing": "⬇️  Luma v{} のインストールを準備中...",
        "upg_title": "タイトル:",
        "upg_backup_saved": "🛡️  v{} のバックアップを保存しました: {}",
        "upg_backup_warn": "⚠️  警告: バックアップを作成できませんでした ({}).",
        "upg_rollback_hint": "💡 いつでも以前のバージョンに戻すには次を実行してください: lumart -dg",
        "dg_title": "⏪ ロールバック (ダウングレード) 可能なバージョン:",
        "dg_choose_prompt": "復元するバージョンを選択 [1-{}] または Enter で [1]: ",
        "hist_title": "📜 Lumartコマンド履歴 ({} 件記録):",
        "hist_empty": "  (履歴に記録されたコマンドはまだありません)",
        "hist_header_num": "[#]",
        "hist_header_ver": "Ver",
        "hist_header_date": "日付 / 時刻",
        "hist_header_cmd": "コマンド",
        "hist_replay_hint": "💡 再実行するには次を使用します: lumart --replay <番号> (例: lumart -R 1)",
        "hist_out_of_range": "❌ インデックス [{}] は範囲外です。利用可能なコマンドは {} 件です。",
        "hist_int_required": "❌ インデックスは整数である必要があります (例: lumart --replay 1)。",
        "hist_replaying": "🚀 再実行中 [{}]: {}",
        "hist_cleared": "✅ Lumartのコマンド履歴を正常にクリアしました。",
        "hist_already_empty": "ℹ️ コマンド履歴はすでに空でした。",
        "desktop_installing": "🖥️  デスクトップ統合とファイルマネージャー操作をインストール中...",
        "desktop_installed_launcher": "  ✅ デスクトップランチャーをインストールしました: {}",
        "desktop_launcher_error": "  ❌ {} の作成中にエラーが発生しました: {}",
        "desktop_context_menu": "  ✅ {} コンテキストメニュー: {}",
        "desktop_completed": "🎉 デスクトップ統合が正常に完了しました！\n   ファイルマネージャーで任意の画像を右クリックし、「Lumartで開く」を選択できるようになりました。",
        "spectra_webcam_only": "💡 「Spectra」エンジンは、リアルタイムのビデオおよびWebカメラストリーミング専用です。\n   有効にするには次を実行してください:\n   lumart --webcam  (または別のカメラの場合は lumart -W / lumart -W 1)\n",
        "export_webp_disabled": "❌ WebP形式 (.webp) のエクスポートは恒久的に無効化されました。.png または .jpg を使用してください。",
        "export_sticker_mono_only": "ℹ️  透明背景ステッカー (--transparent) は Luris Mono (モノクロ) 専用です。色の忠実度を最大にするため、ターミナル背景付きでエクスポートします。",
        "export_success": "✨ ターミナルアートが画像として正常にエクスポートされました: {}",
        "export_error": "❌ 画像のエクスポート中にエラーが発生しました: {}",
        "pillow_not_found": "[luma] Pillowが見つかりません。依存関係をインストールしています...",
        "usage": "使用法: lumart [オプション] <画像パス>\n\n詳細なオプションについては 'lumart --help' をお試しください。",
        "desc": "Lumart - ターミナルアートエンジン",
        "help_help": "このヘルプメッセージを表示して終了します。",
        "help_version": "プログラムのバージョン、診断情報、エンジン状態を表示して終了します。",
        "help_completions": "シェルのタブ補完スクリプトを生成します (bash, zsh, fish)。",
        "help_image_path": "入力画像ファイルへのパス（透明な背景が最適です）。",
        "help_width": "出力するASCIIアートの幅（文字数）。デフォルト: ターミナル画面幅に自動適合。",
        "help_engine": "レンダリングエンジンを選択: 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6), 'spectra' (Spectra Weep 1.4 Webカメラ)。",
        "help_webcam": "ライブWebカメラ映像をターミナルにストリーミング（専用エンジン 'Spectra'）。",
        "help_instant": "プログレッシブ走査エフェクトを無効化し即時描画（デフォルト）。",
        "help_reveal": "プログレッシブ走査ラインアニメーションを有効化。",
        "help_transparent": "透明な背景でPNGステッカーをエクスポートします（Luris Mono専用）。",
        "help_history": "Lumartのコマンド履歴を表示します（オプション：表示件数）。",
        "help_replay": "履歴から以前のコマンドを再実行します（デフォルト：最後のコマンド）。",
        "help_clear_history": "保存されたコマンド履歴をクリアします。",
        "help_paste": "システムのクリップボードから直接画像を読み込みます。",
        "help_install_desktop": "デスクトップエントリとファイルマネージャーの右クリック統合をインストールします。",
        "help_color": "フルカラーTrueColorモードで出力。",
        "help_no_color": "カラー出力を無効化し、モノクロエンジンを使用。",
        "help_invert": "ASCII文字を反転します（暗いターミナルで便利です）。",
        "help_output": "コンソールに出力する代わりに、ASCIIアートをファイルに保存します。",
        "help_blocks": "高解像度のためにハーフブロックまたは2x2ブロックを使用します。",
        "help_quadrants": "2x2 Unicode象限ブロックを使用した超高密度サブピクセルレンダリング。",
        "help_sextants": "Unicode 2x3 セクスタント文字による高密度サブピクセル描画（Mary Apex 標準）。",
        "help_font_ratio": "ターミナルフォントの幅/高さアスペクト比キャリブレーション（デフォルト：0.5）。",
        "help_braille": "滑らかなエッジと高解像度の形状のために点字文字を使用します。",
        "help_boost": "鮮やかなアーケード風の出力のために彩度・コントラスト・Retinex処理を適用します。",
        "help_swap": "名前を使用して色を交換します（例: --swap purple pink blue red）。偶数個の引数を指定する必要があります。",
        "help_dither": "ディザリングアルゴリズム: 'atkinson' (デフォルト), 'floyd', 'bayer', 'none'。",
        "help_manga": "本物のマンガ/アニメスタイル (DoG線画、8x8スクリーントーン)。",
        "help_sketch": "純粋な線画スケッチモード（スクリーントーンなし、クリーンな輪郭）。",
        "help_lang": "特定の言語を強制します（en, es, pt, ru, ja, de, ko, fr）。",
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
        "update_already_latest": "✅ Lumaはすでに最新バージョンです（v{}）。操作は実行されませんでした。",
        "already_on_version": "ℹ️ すでにバージョン v{} を使用しています。操作は実行されませんでした。",
        "upgrade_target_older": "⚠️ バージョン v{} は現在インストールされているバージョン（v{}）より古いバージョンです。\n💡 以前のバージョンに戻すには、次を実行してください: lumart -dg {}",
        "downgrade_target_newer": "⚠️ バージョン v{} は現在インストールされているバージョン（v{}）より新しいバージョンです。\n💡 より新しいバージョンにアップグレードするには、次を実行してください: lumart -uu {}",
        "update_available": "💡 新しいバージョンが利用可能です: v{} (現在: v{}).\n   インストールするには実行してください: lumart -uu (または lumart --upgrade)",
        "update_downloading": "⬇️  Luma v{} をダウンロードしてインストール中...",
        "update_success": "🎉 Lumaを v{} から v{} に正常に更新しました！",
        "update_error": "❌ アップデートエラー: {}",
        "update_permission_error": "⚠️  {} の更新でアクセスが拒否されました。sudo lumart -uu を実行してください",
        "update_notice": "💡 Lumaの新しいバージョンが利用可能です: v{} ('lumart -uu' で更新)",
        "downgrade_checking": "🔍 バージョンのロールバックを準備中...",
        "downgrade_success": "⏪ Lumaを v{} に正常にロールバックしました！",
        "downgrade_error": "❌ ロールバックエラー: {}",
        "downgrade_no_backup": "❌ バックアップまたは以前のバージョンが見つかりません。",
        "help_loop": "端末内でGIF/APNGアニメーションをループ再生（または -o <出力.gif> / --save で保存）。",
        "help_fit": "垂直スクロールなしで端末画面に収まるよう自動調整（-w/--width と併用不可）。",
        "help_save": "レンダリングされたアニメーションGIFを保存。",
        "help_fastfetch": "Fastfetch / Neofetch向けの余白なしコンパクトANSIロゴを出力。",
        "render_anim_export": "{} コマのアニメーションをレンダリング中",
        "err_conflict_fit_width": "互換性のないオプション: -F/--fit と -w/--width は同時に指定できません（--fit が自動計算します）。",
        "err_conflict_instant_reveal": "互換性のないオプション: --instant と --reveal は相互排他的です。",
        "err_conflict_textures": "テクスチャ指定の重複: -S, -B, -Q, --blocks の中から1つだけ選択してください。",
        "err_conflict_styles": "スタイルの重複: -m/--manga または -s/--sketch のいずれかを選択してください。",
        "err_conflict_inputs": "入力ソースの競合: 画像ファイルと --paste または -W/--webcam は同時に指定できません。",
        "err_conflict_loop_static": "無効な形式: --loop は静止画 (.png/.jpg) に出力できません。アニメーション保存には .gif を指定してください（例: -o out.gif）。",
        "err_conflict_transparent_jpg": "無効な形式: --transparent は .png 出力が必要です（JPEGは透過非対応です）。",
        "help_remove_bg": "画質を落とさずに画像の背景を削除します (-r, --remove-bg)。単独で使用するとHD透過PNGを保存します。",
        "help_theme": "ターミナルテーマと色を同期します（catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized）。",
        "help_crt": "レトロCRT走査線と蛍光体モニターをシミュレートします (--crt [green|amber|color])。",
        "help_matrix": "カタカナと2進数コードによる緑のMatrixスタイルで描画します (--matrix)。",
        "help_matrix_rain": "画像へと収束するMatrixデジタルの雨のアニメーションを再生 (--matrix-rain)。",
        "help_slideshow": "複数画像の対話型ターミナルスライドショーを再生します。",
        "help_delay": "スライドショーの画像切り替え秒数（デフォルト: 3.0）。",
        "help_crop": "画像を切り抜く: 'center', 'square' (1:1), または 'x,y,w,h'。",
        "help_zoom": "中央を基準としたデジタルズーム倍率（例: --zoom 1.5）。",
        "help_interactive": "リアルタイム対話型ターミナルTUI調整モード (-I, --interactive, --tui)。",
        "help_copy": "レンダリングされたANSIアートをクリップボードにコピー (-C, --copy)。",
        "help_copy_plain": "カラーコード無しのプレーンASCIIをDiscord/Markdown用にコピー。",
        "help_diff": "ターミナル内での画像の並列視覚比較 (lumart diff <img1> <img2>)。",
        "remove_bg_success": "✅ 画質を損なうことなく背景を正常に削除しました: {} ({}x{})",
        "clipboard_copied_ansi": "レンダリング結果をクリップボードにコピーしました（ANSI truecolor）！",
        "clipboard_copied_plain": "レンダリング結果をクリップボードにコピーしました（プレーンASCII）！",
        "diff_delta": "平均ピクセル色差（Delta）: {:.1f}%",
    },
    "de": {
        "diag_title_system": "📋 System- und Laufzeitdiagnose:",
        "diag_luma_ver": "Luma-Version:",
        "diag_exec_type": "Ausführungstyp:",
        "diag_standalone": "Eigenständige ausführbare Datei (PyInstaller)",
        "diag_script": "Python-Skript",
        "diag_python_env": "Python-Umgebung:",
        "diag_platform_os": "Betriebssystem-Plattform:",
        "diag_title_engines": "⚡ Rendering-Engines:",
        "diag_trumble_desc": "Aktiv (Standard) (Cel-Shading Anime-Ink-Konturen, Capcom CPS-2 / Neo-Geo Color Punch, Lanczos, Bayer-Dither, TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (Perzeptive Farben Apex 3.5):",
        "diag_mary_modes": "Unterstützte Mary-Modi:",
        "diag_mary_modes_list": "sextants (2x3 solide HD-Blöcke), braille (2x4 zweifarbig), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (Monochrom Mono 2.6):",
        "diag_luris_modes": "Unterstützte Luris-Modi:",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (reines DoG), blocks (2x2 HD-Quadranten), ascii",
        "diag_dither_algos": "Dithering-Algorithmen:",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (Live-Webcam Weep 1.4):",
        "diag_spectra_avail": "Verfügbar (OpenCV 30-60 FPS Terminal-Stream mit 5 Live-Weep-Filtern)",
        "diag_spectra_req": "Erfordert opencv-python",
        "diag_title_terminal": "🖥️  Terminal-Diagnose:",
        "diag_res_label": "Aktuelle Auflösung:",
        "diag_res_format": "{} Spalten × {} Zeilen",
        "diag_truecolor_label": "TrueColor (24-Bit):",
        "diag_truecolor_supported": "✅ Unterstützt",
        "diag_truecolor_unsupported": "⚠️  Nicht erkannt (Farben können angenähert sein)",
        "diag_title_paths": "📁 Pfade und Konfiguration:",
        "diag_config_label": "Konfiguration:",
        "diag_config_exists": "Vorhanden",
        "diag_config_default": "Standard",
        "diag_backup_label": "Backups:",
        "diag_backup_count": "{} Backups gespeichert",
        "diag_repo_label": "GitHub-Repository:",
        "diag_native_active": "Aktiv ({})",
        "diag_native_active_bin": "Aktiv über Binärdatei ({})",
        "diag_native_cpp": "Natives C++ ({})",
        "diag_native_cpp_bin": "Natives C++ über Binärdatei ({})",
        "diag_py_fallback": "Nicht erkannt (Python-Fallback wird verwendet)",
        "diag_mary_fallback": "Python-Fallback",
        "diag_not_available": "Nicht verfügbar (Trumble wird verwendet)",
        "ver_status_title": "📦 Luma-Versionsstatus:",
        "ver_current_installed": "Aktuell installierte Version:",
        "ver_latest_github": "Neueste Version auf GitHub:",
        "ver_new_available": "💡 Eine neue Version ist verfügbar!",
        "ver_release_title": "Release-Titel:",
        "ver_install_hint": "Führen Sie Folgendes aus, um automatisch herunterzuladen und zu installieren:",
        "ver_up_to_date": "✅ Ihre Installation ist auf dem neuesten Stand!",
        "ver_recent_history": "📜 Neueste Versionshistorie:",
        "ver_useful_commands": "💡 Nützliche Befehle:",
        "ver_cmd_uu": "Neuestes Update herunterladen und anwenden",
        "ver_cmd_dg": "Interaktive Auswahl zum Zurücksetzen auf eine frühere Version",
        "ver_cmd_v": "Vollständigen Systemdiagnosebericht anzeigen",
        "ver_tag_current": "(aktuell)",
        "upg_avail_title": "🚀 Verfügbare Versionen für Upgrade:",
        "upg_recommended": "(Neueste empfohlene Version)",
        "upg_cancel": "Abbrechen",
        "upg_choose_prompt": "Wählen Sie eine Version [1-{}] oder drücken Sie Enter für [1]: ",
        "upg_cancelled": "Vorgang abgebrochen.",
        "upg_invalid_sel": "❌ Ungültige Auswahl.",
        "upg_preparing": "⬇️  Vorbereitung der Installation von Luma v{}...",
        "upg_title": "Titel:",
        "upg_backup_saved": "🛡️  Backup von v{} gespeichert in: {}",
        "upg_backup_warn": "⚠️  Warnung: Backup konnte nicht erstellt werden ({}).",
        "upg_rollback_hint": "💡 Um jederzeit zur vorherigen Version zurückzukehren: lumart -dg",
        "dg_title": "⏪ Verfügbare Versionen für Rollback (Downgrade):",
        "dg_choose_prompt": "Version zur Wiederherstellung wählen [1-{}] oder Enter für [1]: ",
        "hist_title": "📜 Lumart-Befehlsverlauf ({} aufgezeichnet):",
        "hist_empty": "  (Noch keine Befehle im Verlauf aufgezeichnet)",
        "hist_header_num": "[#]",
        "hist_header_ver": "Ver",
        "hist_header_date": "Datum / Uhrzeit",
        "hist_header_cmd": "Befehl",
        "hist_replay_hint": "💡 Um einen Befehl erneut auszuführen: lumart --replay <Nummer> (z.B.: lumart -R 1)",
        "hist_out_of_range": "❌ Index [{}] außerhalb des Bereichs. Es sind {} Befehle verfügbar.",
        "hist_int_required": "❌ Der Index muss eine ganze Zahl sein (z.B.: lumart --replay 1).",
        "hist_replaying": "🚀 Erneute Ausführung von [{}]: {}",
        "hist_cleared": "✅ Lumart-Befehlsverlauf erfolgreich gelöscht.",
        "hist_already_empty": "ℹ️ Der Befehlsverlauf war bereits leer.",
        "desktop_installing": "🖥️  Desktop-Integration und Dateimanager-Aktionen werden installiert...",
        "desktop_installed_launcher": "  ✅ Desktop-Starter installiert: {}",
        "desktop_launcher_error": "  ❌ Fehler beim Erstellen von {}: {}",
        "desktop_context_menu": "  ✅ Kontextmenü für {}: {}",
        "desktop_completed": "🎉 Desktop-Integration erfolgreich abgeschlossen!\n   Sie können jetzt mit der rechten Maustaste auf ein beliebiges Bild im Dateimanager klicken und 'Mit Lumart öffnen' wählen.",
        "spectra_webcam_only": "💡 Die 'Spectra'-Engine ist ausschließlich für Live-Video- und Webcam-Streaming gedacht.\n   Führen Sie zum Aktivieren Folgendes aus:\n   lumart --webcam  (oder: lumart -W / lumart -W 1 für eine andere Kamera)\n",
        "export_webp_disabled": "❌ Der Export in das WebP-Format (.webp) wurde dauerhaft deaktiviert. Bitte verwenden Sie .png oder .jpg.",
        "export_sticker_mono_only": "ℹ️  Sticker mit transparentem Hintergrund (--transparent) sind exklusiv für Luris Mono (S/W). Das vollständige Bild wird mit Terminal-Hintergrund exportiert.",
        "export_success": "✨ Terminal-Kunst erfolgreich als Bild exportiert: {}",
        "export_error": "❌ Fehler beim Exportieren des Bildes: {}",
        "pillow_not_found": "[luma] Pillow nicht gefunden. Installiere Abhängigkeiten...",
        "usage": "Verwendung: lumart [Optionen] <bildpfad>\n\nVersuche 'lumart --help' für weitere Optionen.",
        "desc": "Lumart - Terminal-Kunst-Engine",
        "help_help": "Diese Hilfemeldung anzeigen und beenden.",
        "help_version": "Versionsnummer, Systemdiagnose und Engine-Status anzeigen.",
        "help_completions": "Shell-Autovervollständigungsskript generieren (bash, zsh, fish).",
        "help_image_path": "Pfad zur Eingabebilddatei (funktioniert am besten mit transparentem Hintergrund).",
        "help_width": "Breite der ASCII-Kunst (in Zeichen). Standard: automatische Anpassung an Terminalgröße.",
        "help_engine": "Rendering-Engine auswählen: 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6) oder 'spectra' (Spectra Weep 1.4 Live-Webcam).",
        "help_webcam": "Live-Webcam-Stream im Terminal anzeigen (exklusive 'Spectra'-Engine).",
        "help_instant": "Progressiven Reveal-Effekt deaktivieren und sofort ausgeben (Standard).",
        "help_reveal": "Progressiven zeilenweisen Scan-Effekt aktivieren.",
        "help_transparent": "PNG-Sticker mit transparentem Hintergrund exportieren (exklusiv für Luris Mono).",
        "help_history": "Lumart-Befehlsverlauf anzeigen (optional: Anzahl der Einträge).",
        "help_replay": "Vorherigen Befehl aus dem Verlauf erneut ausführen (Standard: letzter Befehl).",
        "help_clear_history": "Gespeicherten Befehlsverlauf löschen.",
        "help_paste": "Bild direkt aus der Systemzwischenablage laden.",
        "help_install_desktop": "Desktop-Eintrag und Kontextmenü-Integration für Dateimanager installieren.",
        "help_color": "Ausgabe im TrueColor-Vollfarbmodus erzwingen.",
        "help_no_color": "Farbausgabe deaktivieren und monochrome Engine verwenden.",
        "help_invert": "ASCII-Zeichen umkehren (nützlich für dunkle Terminals).",
        "help_output": "ASCII-Kunst in einer Datei speichern, anstatt sie auf der Konsole auszugeben.",
        "help_blocks": "Halbblöcke oder 2x2 Quadrant-Blöcke für hohe Auflösung verwenden.",
        "help_quadrants": "2x2 Unicode-Quadrantblöcke für ultra-dichtes Subpixel-Rendering verwenden.",
        "help_sextants": "2x3 Unicode-Sextantenblöcke für solides Subpixel-Rendering verwenden (Mary Apex Flaggschiff).",
        "help_font_ratio": "Kalibrierung des Schrift-Seitenverhältnisses Breite/Höhe des Terminals (Standard: 0.5).",
        "help_braille": "Braille-Zeichen für weiche Kanten und hohe Auflösung verwenden.",
        "help_boost": "Verbesserte Farbsättigung, Kontrast und Retinex-Verarbeitung für lebhafte Arcade-Ausgabe anwenden.",
        "help_swap": "Farben nach Name tauschen (z.B. --swap purple pink blue red). Es muss eine gerade Anzahl von Argumenten angegeben werden.",
        "help_dither": "Dithering-Algorithmus: 'atkinson' (Standard), 'floyd', 'bayer' oder 'none'.",
        "help_manga": "Authentischer Manga/Anime-Stil (saubere DoG-Linienführung, 8x8 Rastertönung).",
        "help_sketch": "Reiner Strichzeichnungsmodus (saubere Konturen ohne Rasterung).",
        "help_lang": "Eine bestimmte Sprache erzwingen (en, es, pt, ru, ja, de, ko, fr).",
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
        "update_already_latest": "✅ Luma ist bereits auf dem neuesten Stand (v{}). Es wurden keine Aktionen durchgeführt.",
        "already_on_version": "ℹ️ Sie befinden sich bereits auf Version v{}. Es wurden keine Aktionen durchgeführt.",
        "upgrade_target_older": "⚠️ Version v{} ist älter als die aktuell installierte Version (v{}).\n💡 Um auf eine frühere Version zurückzusetzen, verwenden Sie: lumart -dg {}",
        "downgrade_target_newer": "⚠️ Version v{} ist neuer als die aktuell installierte Version (v{}).\n💡 Um auf eine neuere Version zu aktualisieren, verwenden Sie: lumart -uu {}",
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
        "help_loop": "Animiertes GIF/APNG in Terminal-Schleife abspielen (oder mit -o <datei.gif> / --save exportieren).",
        "help_fit": "Bild an Terminalfenster anpassen ohne Scrollen (inkompatibel mit -w/--width).",
        "help_save": "Gerendertes animiertes GIF speichern.",
        "help_fastfetch": "Kompaktes ANSI-Logo ohne Ränder für Fastfetch / Neofetch ausgeben.",
        "render_anim_export": "Rendere {} Animationsframes",
        "err_conflict_fit_width": "Inkompatible Optionen: -F/--fit und -w/--width können nicht zusammen verwendet werden.",
        "err_conflict_instant_reveal": "Inkompatible Optionen: --instant und --reveal schließen sich gegenseitig aus.",
        "err_conflict_textures": "Inkompatible Texturen: Wählen Sie nur eine aus -S, -B, -Q oder --blocks.",
        "err_conflict_styles": "Inkompatible Stile: Wählen Sie entweder -m/--manga oder -s/--sketch.",
        "err_conflict_inputs": "Eingabekonflikt: Bilddatei kann nicht zusammen mit --paste oder -W/--webcam angegeben werden.",
        "err_conflict_loop_static": "Inkompatibles Format: --loop kann nicht in statisches Bild (.png/.jpg) exportiert werden. Bitte .gif angeben (z.B. -o out.gif).",
        "err_conflict_transparent_jpg": "Inkompatibles Format: --transparent erfordert .png-Format (JPEG unterstützt kein Alpha).",
        "help_remove_bg": "Hintergrund ohne Qualitätsverlust entfernen (-r, --remove-bg). Speichert transparentes HD-PNG bei alleiniger Nutzung.",
        "help_theme": "Farben mit Terminal-Design synchronisieren (catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized).",
        "help_crt": "Retro-Röhrenmonitor mit Scanlines simulieren (--crt [green|amber|color]).",
        "help_matrix": "Bild im digitalen grünen Katakana-Matrix-Code rendern (--matrix).",
        "help_matrix_rain": "Fallende Katakana-Matrix-Regenanimation abspielen (--matrix-rain).",
        "help_slideshow": "Interaktive Terminal-Diashow für mehrere Bilder abspielen.",
        "help_delay": "Verzögerung zwischen Bildern der Diashow in Sekunden (Standard: 3.0).",
        "help_crop": "Bild zuschneiden: 'center', 'square' (1:1) oder 'x,y,w,h'.",
        "help_zoom": "Digitaler Zoomfaktor zentriert auf das Motiv (z.B. --zoom 1.5).",
        "help_interactive": "Interaktiver Live-Terminal-TUI-Anpassungsmodus (-I, --interactive, --tui).",
        "help_copy": "Generierte ANSI-Grafik in die Zwischenablage kopieren (-C, --copy).",
        "help_copy_plain": "Reinen ASCII-Text ohne Farbcodes in die Zwischenablage kopieren.",
        "help_diff": "Visueller Bildvergleich nebeneinander im Terminal (lumart diff <img1> <img2>).",
        "remove_bg_success": "✅ Hintergrund erfolgreich ohne Qualitätsverlust entfernt: {} ({}x{})",
        "clipboard_copied_ansi": "Grafik in Zwischenablage kopiert (ANSI truecolor)!",
        "clipboard_copied_plain": "Grafik in Zwischenablage kopiert (reiner ASCII-Text)!",
        "diff_delta": "Durchschnittliche Pixelfarbabweichung (Delta): {:.1f}%",
    },
    "ko": {
        "diag_title_system": "📋 시스템 및 런타임 진단:",
        "diag_luma_ver": "Luma 버전:",
        "diag_exec_type": "실행 유형:",
        "diag_standalone": "독립 실행형 바이너리 (PyInstaller)",
        "diag_script": "파이썬 스크립트",
        "diag_python_env": "파이썬 환경:",
        "diag_platform_os": "OS 플랫폼:",
        "diag_title_engines": "⚡ 렌더링 엔진:",
        "diag_trumble_desc": "활성 (기본값) (셀 셰이딩 애니메이션 잉크 외곽선, 캡콤 CPS-2 / 네오지오 펀치 색감, 란초스, 바이어 디더, TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (지각 색상 Apex 3.5):",
        "diag_mary_modes": "지원되는 Mary 모드:",
        "diag_mary_modes_list": "sextants (2x3 솔리드 HD 블록), braille (2x4 듀얼 컬러), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (단색 모노 2.6):",
        "diag_luris_modes": "지원되는 Luris 모드:",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (순수 DoG), blocks (2x2 HD 사분면), ascii",
        "diag_dither_algos": "디더링 알고리즘:",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (실시간 웹캠 Weep 1.4):",
        "diag_spectra_avail": "사용 가능 (OpenCV 30-60 FPS 터미널 스트림, 5개 실시간 Weep 필터 지원)",
        "diag_spectra_req": "opencv-python 필요",
        "diag_title_terminal": "🖥️  터미널 진단:",
        "diag_res_label": "현재 해상도:",
        "diag_res_format": "{} 열 × {} 행",
        "diag_truecolor_label": "TrueColor (24비트):",
        "diag_truecolor_supported": "✅ 지원됨",
        "diag_truecolor_unsupported": "⚠️  감지되지 않음 (색상이 근사치로 표현될 수 있습니다)",
        "diag_title_paths": "📁 경로 및 설정:",
        "diag_config_label": "설정:",
        "diag_config_exists": "존재함",
        "diag_config_default": "기본값",
        "diag_backup_label": "백업:",
        "diag_backup_count": "{}개 백업 저장됨",
        "diag_repo_label": "GitHub 저장소:",
        "diag_native_active": "활성 ({})",
        "diag_native_active_bin": "바이너리를 통해 활성 ({})",
        "diag_native_cpp": "네이티브 C++ ({})",
        "diag_native_cpp_bin": "바이너리를 통한 네이티브 C++ ({})",
        "diag_py_fallback": "감지되지 않음 (파이썬 대체 모드 사용)",
        "diag_mary_fallback": "파이썬 대체 모드",
        "diag_not_available": "사용 불가 (Trumble 사용)",
        "ver_status_title": "📦 Luma 버전 상태:",
        "ver_current_installed": "현재 설치된 버전:",
        "ver_latest_github": "GitHub의 최신 버전:",
        "ver_new_available": "💡 새로운 버전을 사용할 수 있습니다!",
        "ver_release_title": "릴리스 제목:",
        "ver_install_hint": "자동으로 다운로드하고 설치하려면 다음을 실행하세요:",
        "ver_up_to_date": "✅ 최신 버전으로 업데이트되어 있습니다!",
        "ver_recent_history": "📜 최근 버전 기록:",
        "ver_useful_commands": "💡 유용한 명령어:",
        "ver_cmd_uu": "최신 업데이트 다운로드 및 적용",
        "ver_cmd_dg": "이전 버전으로 롤백하기 위한 대화형 선택기",
        "ver_cmd_v": "전체 시스템 진단 보고서 보기",
        "ver_tag_current": "(현재)",
        "upg_avail_title": "🚀 업그레이드 가능한 버전:",
        "upg_recommended": "(최신 권장 버전)",
        "upg_cancel": "취소",
        "upg_choose_prompt": "버전 선택 [1-{}] 또는 Enter로 [1] 선택: ",
        "upg_cancelled": "작업이 취소되었습니다.",
        "upg_invalid_sel": "❌ 잘못된 선택입니다.",
        "upg_preparing": "⬇️  Luma v{} 설치 준비 중...",
        "upg_title": "제목:",
        "upg_backup_saved": "🛡️  v{} 백업 저장 완료: {}",
        "upg_backup_warn": "⚠️  경고: 백업을 생성할 수 없습니다 ({}).",
        "upg_rollback_hint": "💡 언제든지 이전 버전으로 돌아가려면 다음을 실행하세요: lumart -dg",
        "dg_title": "⏪ 롤백 (다운그레이드) 가능한 버전:",
        "dg_choose_prompt": "복원할 버전 선택 [1-{}] 또는 Enter로 [1] 선택: ",
        "hist_title": "📜 Lumart 명령어 기록 ({}개 기록됨):",
        "hist_empty": "  (기록된 명령어가 아직 없습니다)",
        "hist_header_num": "[#]",
        "hist_header_ver": "버전",
        "hist_header_date": "날짜 / 시간",
        "hist_header_cmd": "명령어",
        "hist_replay_hint": "💡 명령어를 재실행하려면 다음을 사용하세요: lumart --replay <번호> (예: lumart -R 1)",
        "hist_out_of_range": "❌ 인덱스 [{}]가 범위를 벗어났습니다. 사용 가능한 명령어가 {}개 있습니다.",
        "hist_int_required": "❌ 인덱스는 정수여야 합니다 (예: lumart --replay 1).",
        "hist_replaying": "🚀 재실행 중 [{}]: {}",
        "hist_cleared": "✅ Lumart 명령어 기록이 성공적으로 삭제되었습니다.",
        "hist_already_empty": "ℹ️ 명령어 기록이 이미 비어 있습니다.",
        "desktop_installing": "🖥️  데스크톱 통합 및 파일 관리자 액션을 설치하는 중...",
        "desktop_installed_launcher": "  ✅ 데스크톱 런처가 설치되었습니다: {}",
        "desktop_launcher_error": "  ❌ {} 생성 중 오류 발생: {}",
        "desktop_context_menu": "  ✅ {} 컨텍스트 메뉴 스크립트: {}",
        "desktop_completed": "🎉 데스크톱 통합이 성공적으로 완료되었습니다!\n   이제 파일 관리자에서 이미지를 마우스 오른쪽 버튼으로 클릭하고 'Lumart로 열기'를 선택할 수 있습니다.",
        "spectra_webcam_only": "💡 'Spectra' 엔진은 실시간 비디오 및 웹캠 스트리밍 전용입니다.\n   활성화하려면 다음을 실행하세요:\n   lumart --webcam  (또는 다른 카메라는 lumart -W / lumart -W 1)\n",
        "export_webp_disabled": "❌ WebP 형식(.webp) 내보내기가 영구적으로 비활성화되었습니다. .png 또는 .jpg를 사용해 주세요.",
        "export_sticker_mono_only": "ℹ️  투명 배경 스티커(--transparent)는 Luris Mono(흑백) 전용입니다. 최대 색상 재현을 위해 터미널 배경과 함께 전체 이미지를 내보냅니다.",
        "export_success": "✨ 터미널 아트를 이미지로 성공적으로 내보냈습니다: {}",
        "export_error": "❌ 이미지 내보내기 오류: {}",
        "pillow_not_found": "[luma] Pillow를 찾을 수 없습니다. 종속성을 설치하는 중...",
        "usage": "사용법: lumart [옵션] <이미지_경로>\n\n자세한 옵션은 'lumart --help'를 시도해 보세요.",
        "desc": "Lumart - 터미널 아트 엔진",
        "help_help": "이 도움말 메시지를 표시하고 종료합니다.",
        "help_version": "프로그램의 버전 번호, 시스템 진단 및 엔진 상태를 표시합니다.",
        "help_completions": "셸 자동 완성 스크립트를 생성합니다 (bash, zsh, fish).",
        "help_image_path": "입력 이미지 파일의 경로입니다 (투명한 배경이 가장 좋습니다).",
        "help_width": "출력 ASCII 아트의 너비(문자 수). 기본값: 터미널 창 너비에 자동 맞춤.",
        "help_engine": "렌더링 엔진 선택: 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6) 또는 'spectra' (Spectra Weep 1.4 실시간 웹캠).",
        "help_webcam": "터미널에 라이브 웹캠 영상 스트리밍 (전용 'Spectra' 엔진).",
        "help_instant": "프로그레시브 스캔 효과를 비활성화하고 즉시 출력합니다 (기본값).",
        "help_reveal": "한 줄씩 출력되는 프로그레시브 스캔 애니메이션을 활성화합니다.",
        "help_transparent": "투명 배경으로 PNG 스티커를 내보냅니다 (Luris Mono 전용).",
        "help_history": "Lumart 명령 실행 기록을 표시합니다 (선택 사항: 항목 수).",
        "help_replay": "기록에서 이전 명령을 다시 실행합니다 (기본값: 마지막 명령).",
        "help_clear_history": "저장된 명령 기록을 삭제합니다.",
        "help_paste": "시스템 클립보드에서 직접 이미지를 불러옵니다.",
        "help_install_desktop": "데스크톱 항목 및 파일 관리자 우클릭 통합을 설치합니다.",
        "help_color": "TrueColor 풀 컬러 모드로 출력 강제.",
        "help_no_color": "컬러 출력을 비활성화하고 흑백 엔진 사용.",
        "help_invert": "ASCII 문자를 반전시킵니다(어두운 터미널에 유용).",
        "help_output": "콘솔에 출력하는 대신 ASCII 아트를 파일에 저장합니다.",
        "help_blocks": "고해상도를 위해 하프 블록 또는 2x2 쿼드런트 블록을 사용합니다.",
        "help_quadrants": "초고밀도 서브픽셀 렌더링을 위해 2x2 유니코드 사분면 블록을 사용합니다.",
        "help_sextants": "솔리드 서브픽셀 렌더링을 위해 2x3 유니코드 섹스턴트 블록 사용 (Mary Apex 플래그십).",
        "help_font_ratio": "터미널 폰트 가로/세로 비율 보정 (기본값: 0.5).",
        "help_braille": "부드러운 가장자리와 고해상도 모양을 위해 점자 문자를 사용합니다.",
        "help_boost": "선명한 아케이드 스타일 출력을 위해 향상된 색상 채도, 대비 및 Retinex 처리를 적용합니다.",
        "help_swap": "이름을 사용하여 색상을 교환합니다(예: --swap purple pink blue red). 짝수 개의 인수를 제공해야 합니다.",
        "help_dither": "디더링 알고리즘: 'atkinson' (기본값), 'floyd', 'bayer' 또는 'none'.",
        "help_manga": "정통 만화/애니메이션 스타일 (깔끔한 DoG 라인아트, 8x8 스크린톤).",
        "help_sketch": "순수 선화 스케치 모드 (스크린톤 없는 깔끔한 윤곽선).",
        "help_lang": "특정 언어를 강제 적용합니다(en, es, pt, ru, ja, de, ko, fr).",
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
        "update_already_latest": "✅ Luma가 이미 최신 버전입니다 (v{}). 변경 작업이 수행되지 않았습니다.",
        "already_on_version": "ℹ️ 이미 v{} 버전을 사용 중입니다. 변경 작업이 수행되지 않았습니다.",
        "upgrade_target_older": "⚠️ v{} 버전은 현재 설치된 버전(v{})보다 이전 버전입니다.\n💡 이전 버전으로 롤백하려면 다음을 사용하세요: lumart -dg {}",
        "downgrade_target_newer": "⚠️ v{} 버전은 현재 설치된 버전(v{})보다 최신 버전입니다.\n💡 최신 버전으로 업그레이드하려면 다음을 사용하세요: lumart -uu {}",
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
        "help_loop": "터미널에서 GIF/APNG 애니메이션 반복 재생 (또는 -o <파일.gif> / --save 로 내보내기).",
        "help_fit": "세로 스크롤 없이 터미널 화면에 맞게 맞춤 ( -w/--width 와 함께 사용 불가).",
        "help_save": "렌더링된 애니메이션 GIF 파일 저장.",
        "help_fastfetch": "Fastfetch / Neofetch용 여백 없는 컴팩트 ANSI 로고 출력.",
        "render_anim_export": "{} 개 애니메이션 프레임 렌더링 중",
        "err_conflict_fit_width": "호환되지 않는 옵션: -F/--fit 과 -w/--width 는 함께 사용할 수 없습니다.",
        "err_conflict_instant_reveal": "호환되지 않는 옵션: --instant 과 --reveal 은 상호 배타적입니다.",
        "err_conflict_textures": "호환되지 않는 텍스처: -S, -B, -Q, --blocks 중 하나만 선택하세요.",
        "err_conflict_styles": "호환되지 않는 스타일: -m/--manga 또는 -s/--sketch 중 하나만 선택하세요.",
        "err_conflict_inputs": "입력 충돌: 이미지 파일과 --paste 또는 -W/--webcam 을 동시에 지정할 수 없습니다.",
        "err_conflict_loop_static": "형식 불일치: --loop 모드는 정적 이미지 (.png/.jpg) 로 내보낼 수 없습니다. .gif 를 지정하세요 (예: -o out.gif).",
        "err_conflict_transparent_jpg": "형식 불일치: --transparent 는 .png 형식이 필요합니다 (JPEG는 투명도를 지원하지 않습니다).",
        "help_remove_bg": "품질 저하 없이 이미지 배경을 제거합니다 (-r, --remove-bg). 단독 사용 시 HD 투명 PNG를 저장합니다.",
        "help_theme": "터미널 테마와 색상을 동기화합니다 (catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized).",
        "help_crt": "레트로 CRT 스캔라인 및 인광체 모니터를 시뮬레이션합니다 (--crt [green|amber|color]).",
        "help_matrix": "디지털 가타카나 및 바이너리 녹색 매트릭스 코드로 렌더링합니다 (--matrix).",
        "help_matrix_rain": "이미지로 완성되는 매트릭스 디지털 레인 애니메이션 재생 (--matrix-rain).",
        "help_slideshow": "여러 이미지에 대한 대화형 터미널 슬라이드쇼를 재생합니다.",
        "help_delay": "슬라이드쇼 이미지 간 지연 시간(초, 기본값: 3.0).",
        "help_crop": "이미지 자르기: 'center', 'square' (1:1) 또는 'x,y,w,h'.",
        "help_zoom": "중앙 기준 디지털 줌 배율 (예: --zoom 1.5).",
        "help_interactive": "실시간 대화형 터미널 TUI 조정 모드 (-I, --interactive, --tui).",
        "help_copy": "렌더링된 ANSI 아트를 시스템 클립보드에 복사 (-C, --copy).",
        "help_copy_plain": "Discord/Markdown용 순수 ASCII 텍스트를 클립보드에 복사.",
        "help_diff": "터미널에서 나란히 이미지 시각적 비교 (lumart diff <img1> <img2>).",
        "remove_bg_success": "✅ 품질 손실 없이 배경이 성공적으로 제거되었습니다: {} ({}x{})",
        "clipboard_copied_ansi": "렌더링 결과가 클립보드에 복사되었습니다 (ANSI 트루컬러)!",
        "clipboard_copied_plain": "렌더링 결과가 클립보드에 복사되었습니다 (순수 ASCII)!",
        "diff_delta": "평균 픽셀 색상 차이 (Delta): {:.1f}%",
    },
    "fr": {
        "diag_title_system": "📋 Diagnostics système et environnement d'exécution :",
        "diag_luma_ver": "Version de Luma :",
        "diag_exec_type": "Type d'exécution :",
        "diag_standalone": "Exécutable autonome (PyInstaller)",
        "diag_script": "Script Python",
        "diag_python_env": "Environnement Python :",
        "diag_platform_os": "Plateforme OS :",
        "diag_title_engines": "⚡ Moteurs de rendu :",
        "diag_trumble_desc": "Actif (Par défaut) (Contours anime cel-shading encre, palette Capcom CPS-2 / Neo-Geo, Lanczos, tramage Bayer, TrueColor Braille/Blocks)",
        "diag_mary_desc": "Mary (Couleur perceptive Apex 3.5) :",
        "diag_mary_modes": "Modes Mary pris en charge :",
        "diag_mary_modes_list": "sextants (blocs solides 2x3 HD), braille (2x4 bicolore), quadrants (2x2), blocks, ascii",
        "diag_luris_desc": "Luris (Monochrome Mono 2.6) :",
        "diag_luris_modes": "Modes Luris pris en charge :",
        "diag_luris_modes_list": "braille, manga 2.6 (DoG + Bayer), sketch (DoG pur), blocks (quadrants 2x2 HD), ascii",
        "diag_dither_algos": "Algorithmes de tramage :",
        "diag_dither_list": "atkinson (1984, MacPaint), floyd-steinberg, bayer 8x8",
        "diag_spectra_desc": "Spectra (Webcam en direct Weep 1.4) :",
        "diag_spectra_avail": "Disponible (Flux terminal OpenCV 30-60 FPS avec 5 filtres Weep en direct)",
        "diag_spectra_req": "Nécessite opencv-python",
        "diag_title_terminal": "🖥️  Diagnostics du terminal :",
        "diag_res_label": "Résolution actuelle :",
        "diag_res_format": "{} colonnes × {} lignes",
        "diag_truecolor_label": "TrueColor (24 bits) :",
        "diag_truecolor_supported": "✅ Pris en charge",
        "diag_truecolor_unsupported": "⚠️  Non détecté (les couleurs peuvent être approximées)",
        "diag_title_paths": "📁 Chemins et configuration :",
        "diag_config_label": "Configuration :",
        "diag_config_exists": "Existe",
        "diag_config_default": "Par défaut",
        "diag_backup_label": "Sauvegardes :",
        "diag_backup_count": "{} sauvegardes enregistrées",
        "diag_repo_label": "Dépôt GitHub :",
        "diag_native_active": "Actif ({})",
        "diag_native_active_bin": "Actif via binaire ({})",
        "diag_native_cpp": "C++ natif ({})",
        "diag_native_cpp_bin": "C++ natif via binaire ({})",
        "diag_py_fallback": "Non détecté (utilisation du secours Python)",
        "diag_mary_fallback": "Secours Python",
        "diag_not_available": "Indisponible (utilisation de Trumble)",
        "ver_status_title": "📦 État des versions de Luma :",
        "ver_current_installed": "Version actuellement installée :",
        "ver_latest_github": "Dernière version sur GitHub :",
        "ver_new_available": "💡 Une nouvelle version est disponible !",
        "ver_release_title": "Titre de la version :",
        "ver_install_hint": "Pour télécharger et installer automatiquement, exécutez :",
        "ver_up_to_date": "✅ Votre installation est à jour avec la version la plus récente !",
        "ver_recent_history": "📜 Historique des versions récentes :",
        "ver_useful_commands": "💡 Commandes utiles :",
        "ver_cmd_uu": "Télécharger et appliquer la dernière mise à jour",
        "ver_cmd_dg": "Sélecteur interactif pour revenir à une version précédente",
        "ver_cmd_v": "Afficher le rapport complet de diagnostic système",
        "ver_tag_current": "(actuelle)",
        "upg_avail_title": "🚀 Versions disponibles pour Upgrade :",
        "upg_recommended": "(Dernière version recommandée)",
        "upg_cancel": "Annuler",
        "upg_choose_prompt": "Choisissez une version [1-{}] ou appuyez sur Entrée pour [1] : ",
        "upg_cancelled": "Opération annulée.",
        "upg_invalid_sel": "❌ Sélection invalide.",
        "upg_preparing": "⬇️  Préparation de l'installation de Luma v{}...",
        "upg_title": "Titre :",
        "upg_backup_saved": "🛡️  Sauvegarde de la v{} enregistrée dans : {}",
        "upg_backup_warn": "⚠️  Avertissement : Impossible de créer la sauvegarde ({}).",
        "upg_rollback_hint": "💡 Pour revenir à la version précédente à tout moment, exécutez : lumart -dg",
        "dg_title": "⏪ Versions disponibles pour Restaurer (Downgrade) :",
        "dg_choose_prompt": "Choisissez une version à restaurer [1-{}] ou appuyez sur Entrée pour [1] : ",
        "hist_title": "📜 Historique des commandes Lumart ({} enregistrées) :",
        "hist_empty": "  (Aucune commande enregistrée dans l'historique pour le moment)",
        "hist_header_num": "[#]",
        "hist_header_ver": "Ver",
        "hist_header_date": "Date / Heure",
        "hist_header_cmd": "Commande",
        "hist_replay_hint": "💡 Pour réexécuter une commande : lumart --replay <numéro> (ex : lumart -R 1)",
        "hist_out_of_range": "❌ Indice [{}] hors limites. Il y a {} commandes disponibles.",
        "hist_int_required": "❌ L'indice doit être un nombre entier (ex : lumart --replay 1).",
        "hist_replaying": "🚀 Réexécution de [{}]: {}",
        "hist_cleared": "✅ Historique des commandes Lumart effacé avec succès.",
        "hist_already_empty": "ℹ️ L'historique des commandes était déjà vide.",
        "desktop_installing": "🖥️  Installation de l'intégration au bureau et aux gestionnaires de fichiers...",
        "desktop_installed_launcher": "  ✅ Lanceur de bureau installé : {}",
        "desktop_launcher_error": "  ❌ Erreur lors de la création de {} : {}",
        "desktop_context_menu": "  ✅ Menu contextuel pour {} : {}",
        "desktop_completed": "🎉 Intégration au bureau terminée avec succès !\n   Vous pouvez désormais faire un clic droit sur n'importe quelle image dans votre gestionnaire de fichiers et sélectionner 'Ouvrir avec Lumart'.",
        "spectra_webcam_only": "💡 Le moteur 'Spectra' est exclusivement réservé au streaming vidéo et webcam en temps réel.\n   Pour l'activer, exécutez :\n   lumart --webcam  (ou : lumart -W / lumart -W 1 pour une autre caméra)\n",
        "export_webp_disabled": "❌ L'exportation au format WebP (.webp) a été définitivement désactivée. Veuillez utiliser .png ou .jpg.",
        "export_sticker_mono_only": "ℹ️  Les stickers à fond transparent (--transparent) sont exclusifs à Luris Mono (N&B). Exportation de l'image complète avec arrière-plan de terminal.",
        "export_success": "✨ Art de terminal exporté avec succès vers l'image : {}",
        "export_error": "❌ Erreur lors de l'exportation de l'image : {}",
        "pillow_not_found": "[luma] Pillow introuvable. Installation des dépendances...",
        "usage": "Utilisation : lumart [options] <chemin_image>\n\nEssayez 'lumart --help' si vous avez la flemme de lire la documentation.",
        "desc": "Lumart - Moteur d'art pour terminal fait par et pour les humains",
        "help_help": "Afficher ce message d'aide et quitter.",
        "help_version": "Afficher la version du programme, les diagnostics système et l'état des moteurs.",
        "help_completions": "Générer le script d'auto-complétion pour le shell (bash, zsh, fish).",
        "help_image_path": "Chemin du fichier image d'entrée (fonctionne mieux avec des arrière-plans transparents).",
        "help_width": "Largeur de l'art ASCII en sortie (en caractères). Par défaut : ajustement automatique au terminal.",
        "help_engine": "Sélectionner le moteur de rendu : 'mary' (Mary Apex 3.5), 'trumble' (Trumble Orelx 2.2), 'luris' (Luris Mono 2.6), ou 'spectra' (Spectra Weep 1.4 webcam en direct).",
        "help_webcam": "Diffuser le flux de la webcam en direct dans le terminal (moteur exclusif 'Spectra').",
        "help_instant": "Désactiver l'effet de révélation progressive et afficher immédiatement (par défaut).",
        "help_reveal": "Activer l'animation de balayage progressif ligne par ligne.",
        "help_transparent": "Exporter un sticker PNG avec arrière-plan transparent (exclusif à Luris Mono).",
        "help_history": "Afficher l'historique des commandes Lumart (optionnel : nombre d'entrées).",
        "help_replay": "Réexécuter une commande précédente de l'historique (par défaut : la dernière).",
        "help_clear_history": "Effacer l'historique des commandes enregistrées.",
        "help_paste": "Charger une image directement depuis le presse-papiers système.",
        "help_install_desktop": "Installer l'entrée de bureau Linux et l'intégration au menu contextuel des gestionnaires de fichiers.",
        "help_color": "Forcer la sortie en mode couleur TrueColor.",
        "help_no_color": "Désactiver la sortie couleur et utiliser le moteur monochrome.",
        "help_invert": "Inverser les caractères ASCII (utile pour les terminaux sombres).",
        "help_output": "Enregistrer l'art ASCII dans un fichier au lieu de l'imprimer dans la console.",
        "help_blocks": "Utiliser des demi-blocs (Couleur) ou des blocs quadrants 2x2 HD (N&B) pour une haute résolution.",
        "help_quadrants": "Utiliser des blocs quadrants Unicode 2x2 pour un rendu sous-pixel ultra-dense.",
        "help_sextants": "Utiliser des blocs sextants Unicode 2x3 pour un rendu sous-pixel solide (fleuron Mary Apex).",
        "help_font_ratio": "Calibration du ratio largeur/hauteur de la police du terminal (par défaut : 0.5).",
        "help_braille": "Utiliser des caractères Braille pour des contours lisses et des formes haute résolution.",
        "help_boost": "Appliquer une saturation, un contraste et un traitement Retinex améliorés pour une sortie arcade vibrante.",
        "help_swap": "Échanger des couleurs par leur nom (ex : --swap purple pink blue red). Nombre pair d'arguments requis.",
        "help_dither": "Algorithme de tramage pour le dégradé N&B : 'atkinson' (par défaut), 'floyd', 'bayer' ou 'none'.",
        "help_manga": "Style authentique Manga/Anime (traits DoG nets, trames de points 8x8 Bayer).",
        "help_sketch": "Mode esquisse au trait pur (contours nets sans trame ni bruit d'arrière-plan).",
        "help_lang": "Forcer une langue spécifique (en, es, pt, ru, ja, de, ko, fr).",
        "error_open": "❌ Mais où est passée l'image ? Impossible de l'ouvrir : {}",
        "error_swap": "❌ Veuillez fournir des paires de couleurs à --swap (ex : --swap purple pink). Je ne lis pas dans vos pensées.",
        "saved_to": "Art ASCII enregistré dans {}",
        "error_save": "❌ Échec de l'enregistrement du fichier : {}",
        "lang_success": "Langue modifiée avec succès vers '{}'.",
        "lang_error": "❌ Erreur : La langue '{}' n'est pas prise en charge.",
        "help_update": "Vérifier les mises à jour sans installer (-u, --update, --check-update).",
        "help_upgrade": "Télécharger et installer la dernière mise à jour avec sélecteur interactif (-uu, --upgrade).",
        "help_downgrade": "Revenir à la version précédente ou choisir dans le menu interactif (-dg, --downgrade [VER]).",
        "update_checking": "🔍 Recherche de mises à jour...",
        "update_already_latest": "✅ Luma est déjà à jour (v{}). Aucune action n'a été effectuée.",
        "already_on_version": "ℹ️ Vous êtes déjà sur la version v{}. Aucune action n'a été effectuée.",
        "upgrade_target_older": "⚠️ La version v{} est plus ancienne que la version actuellement installée (v{}).\n💡 Pour revenir à une version antérieure, utilisez : lumart -dg {}",
        "downgrade_target_newer": "⚠️ La version v{} est plus récente que la version actuellement installée (v{}).\n💡 Pour mettre à niveau vers une version plus récente, utilisez : lumart -uu {}",
        "update_available": "💡 Nouvelle version disponible : v{} (actuelle : v{}).\n   Pour l'installer, exécutez : lumart -uu (ou lumart --upgrade)",
        "update_downloading": "⬇️  Téléchargement et installation de Luma v{}...",
        "update_success": "🎉 Luma a été mis à jour avec succès de v{} à v{} !",
        "update_error": "❌ Erreur lors de la vérification ou de l'application des mises à jour : {}",
        "update_permission_error": "⚠️  Permission refusée pour mettre à jour {}. Utilisez sudo : sudo lumart -uu",
        "update_notice": "💡 Une nouvelle version de Luma est disponible : v{} (exécutez 'lumart -uu' pour mettre à niveau)",
        "downgrade_checking": "🔍 Préparation du retour à une version précédente...",
        "downgrade_success": "⏪ Luma a été rétrogradé avec succès vers la v{} !",
        "downgrade_error": "❌ Erreur lors de la rétrogradation : {}",
        "downgrade_no_backup": "❌ Aucune sauvegarde ou version précédente trouvée.",
        "help_loop": "Lire GIF/APNG animé en boucle dans le terminal (ou exporter avec -o <fichier.gif> / --save).",
        "help_fit": "Ajuster l'image à la fenêtre du terminal sans défilement vertical (incompatible avec -w/--width).",
        "help_save": "Enregistrer le GIF animé rendu sur disque.",
        "help_fastfetch": "Générer un logo ANSI compact sans bordures vides pour Fastfetch / Neofetch.",
        "render_anim_export": "Rendu de {} images d'animation",
        "err_conflict_fit_width": "Options incompatibles : -F/--fit et -w/--width ne peuvent pas être utilisés ensemble.",
        "err_conflict_instant_reveal": "Options incompatibles : --instant et --reveal s'excluent mutuellement.",
        "err_conflict_textures": "Textures incompatibles : choisissez une seule option parmi -S, -B, -Q ou --blocks.",
        "err_conflict_styles": "Styles incompatibles : choisissez soit -m/--manga soit -s/--sketch.",
        "err_conflict_inputs": "Sources en conflit : impossible de spécifier un fichier avec --paste ou -W/--webcam.",
        "err_conflict_loop_static": "Format incompatible : --loop ne peut pas être exporté vers une image statique (.png/.jpg). Spécifiez .gif (ex. -o sortie.gif).",
        "err_conflict_transparent_jpg": "Format incompatible : --transparent nécessite le format .png (JPEG ne gère pas la transparence).",
        "help_remove_bg": "Supprimer l'arrière-plan sans perte de qualité (-r, --remove-bg). Enregistre un PNG transparent HD si utilisé seul.",
        "help_theme": "Synchroniser les couleurs avec le thème du terminal (catppuccin, dracula, nord, gruvbox, synthwave, gameboy, solarized).",
        "help_crt": "Simuler un écran cathodique CRT rétro avec lignes de balayage (--crt [green|amber|color]).",
        "help_matrix": "Rendre l'image en code Matrix vert numérique avec Katakana (--matrix).",
        "help_matrix_rain": "Animation de pluie de code Matrix tombant sur l'image (--matrix-rain).",
        "help_slideshow": "Diaporama interactif dans le terminal pour plusieurs images.",
        "help_delay": "Délai en secondes entre les images du diaporama (par défaut : 3.0).",
        "help_crop": "Recadrer l'image : 'center', 'square' (1:1) ou 'x,y,w,h'.",
        "help_zoom": "Facteur de zoom numérique centré sur le sujet (ex : --zoom 1.5).",
        "help_interactive": "Mode TUI interactif en direct dans le terminal (-I, --interactive, --tui).",
        "help_copy": "Copier l'art ANSI rendu dans le presse-papiers système (-C, --copy).",
        "help_copy_plain": "Copier le texte ASCII brut (sans couleurs) pour Discord/Markdown.",
        "help_diff": "Comparaison visuelle d'images côte à côte dans le terminal (lumart diff <img1> <img2>).",
        "remove_bg_success": "✅ Arrière-plan supprimé avec succès sans perte de qualité : {} ({}x{})",
        "clipboard_copied_ansi": "Rendu copié dans le presse-papiers système (ANSI truecolor) !",
        "clipboard_copied_plain": "Rendu copié dans le presse-papiers système (ASCII brut) !",
        "diff_delta": "Variation chromatique moyenne (Delta) : {:.1f}%",
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
    elif lang_code and lang_code.startswith("fr"):
        CURRENT_LANG = "fr"
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

def remove_image_background(pil_img, tolerance=32):
    """
    Remueve inteligentemente el fondo perimetral / conectado a los bordes para salidas transparentes,
    stickers PNG/WebP y celdas sin fondo opaco.
    Utiliza segmentación avanzada GrabCut (Gaussian Mixture Models) de OpenCV para aislar
    figuras complejas, cabellos y degradados sin halos ni recortes prematuros.
    """
    if pil_img is None:
        return pil_img

    img_rgba = pil_img.convert("RGBA")
    
    # Soporte para motor neuronal rembg si está instalado
    try:
        import rembg
        return rembg.remove(pil_img)
    except Exception:
        pass
        
    # 1. Si la imagen ya tiene canal alfa con suficiente transparencia real (>4%), conservarlo intacto
    try:
        import numpy as np
        arr = np.array(img_rgba)
        if np.mean(arr[:, :, 3] < 128) > 0.04:
            return img_rgba
    except Exception:
        pass

    # 2. Segmentación avanzada con OpenCV GrabCut (GMM con 5 componentes gaussianas)
    try:
        import cv2
        import numpy as np

        arr = np.array(img_rgba)
        rgb = arr[:, :, :3]
        h, w = rgb.shape[:2]
        if h <= 4 or w <= 4:
            return img_rgba

        # Bounding box con margen perimetral adaptativo (1% - 3% del tamaño)
        margin_x = max(2, min(20, w // 40))
        margin_y = max(2, min(20, h // 40))
        rect = (margin_x, margin_y, w - 2 * margin_x, h - 2 * margin_y)

        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        mask = np.zeros((h, w), np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # 3 iteraciones de optimización EM para máxima velocidad y nitidez de contorno
        cv2.grabCut(bgr, mask, rect, bgdModel, fgdModel, 3, cv2.GC_INIT_WITH_RECT)
        
        # 0 y 2 son fondo seguro y probable fondo; 1 y 3 son primer plano
        fg_mask = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)

        # Refinamiento morfológico para limpiar islas de ruido perimetral y preservar bordes suaves
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        # Verificar que la segmentación no haya borrado la figura por completo (>5% y <98% transparencia)
        trans_ratio = np.mean(fg_mask == 0)
        if 0.05 <= trans_ratio <= 0.98:
            arr[:, :, 3] = fg_mask
            return Image.fromarray(arr)
    except Exception:
        pass

    # 3. Fallback en OpenCV con Connected Components y FloodFill perimetral
    try:
        import cv2
        import numpy as np

        arr = np.array(img_rgba)
        rgb = arr[:, :, :3]
        h, w = rgb.shape[:2]
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        mask = np.zeros((h + 2, w + 2), np.uint8)
        diff = (tolerance, tolerance, tolerance)
        flags = 4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
        seed_points = [
            (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
            (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)
        ]
        for pt in seed_points:
            cv2.floodFill(bgr, mask, pt, 0, diff, diff, flags)
        bg_mask = mask[1:h+1, 1:w+1] == 255
        arr[bg_mask, 3] = 0
        return Image.fromarray(arr)
    except Exception:
        pass

    # 4. Fallback puro en Python con deque BFS perimetral
    try:
        from collections import deque
        w, h = img_rgba.size
        pixels = img_rgba.load()
        visited = set()
        queue = deque()
        corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
        for cx, cy in corners:
            color = pixels[cx, cy][:3]
            queue.append((cx, cy, color))
            visited.add((cx, cy))
        
        while queue:
            x, y, ref_c = queue.popleft()
            pixels[x, y] = (0, 0, 0, 0)
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    nc = pixels[nx, ny][:3]
                    diff = max(abs(nc[0] - ref_c[0]), abs(nc[1] - ref_c[1]), abs(nc[2] - ref_c[2]))
                    if diff <= tolerance:
                        visited.add((nx, ny))
                        queue.append((nx, ny, ref_c))
        return img_rgba
    except Exception:
        return img_rgba

# -------------------------------------------------------------
# PALETAS DE TEMAS DE TERMINAL (Theme Sync)
# -------------------------------------------------------------
THEME_PALETTES = {
    "catppuccin": [
        (30, 30, 46), (24, 24, 37), (49, 50, 68), (69, 71, 90), (88, 91, 112),
        (205, 214, 244), (245, 224, 220), (242, 205, 205), (203, 166, 247),
        (243, 139, 168), (250, 179, 135), (249, 226, 175), (166, 227, 161),
        (148, 226, 213), (137, 220, 235), (116, 199, 236), (137, 180, 250), (180, 190, 254)
    ],
    "dracula": [
        (40, 42, 54), (68, 71, 90), (248, 248, 242), (98, 114, 164),
        (139, 233, 253), (80, 250, 123), (255, 184, 108), (255, 121, 198),
        (189, 147, 249), (255, 85, 85), (241, 250, 140)
    ],
    "nord": [
        (46, 52, 64), (59, 66, 82), (67, 76, 94), (76, 86, 106),
        (216, 222, 233), (229, 233, 240), (236, 239, 244), (143, 188, 187),
        (136, 192, 208), (129, 161, 193), (94, 129, 172), (191, 97, 106),
        (208, 135, 112), (235, 203, 139), (163, 190, 140), (180, 142, 173)
    ],
    "gruvbox": [
        (40, 40, 40), (146, 131, 116), (251, 73, 52), (184, 187, 38),
        (250, 189, 47), (131, 165, 152), (211, 134, 155), (142, 192, 124),
        (235, 219, 178), (204, 36, 29), (152, 151, 26), (215, 153, 33),
        (69, 133, 136), (177, 98, 134), (104, 157, 106), (168, 153, 132)
    ],
    "synthwave": [
        (38, 20, 71), (46, 33, 87), (253, 58, 105), (254, 205, 81),
        (255, 113, 206), (1, 205, 254), (5, 255, 161), (185, 103, 255), (255, 251, 150)
    ],
    "vaporwave": [
        (38, 20, 71), (46, 33, 87), (253, 58, 105), (254, 205, 81),
        (255, 113, 206), (1, 205, 254), (5, 255, 161), (185, 103, 255), (255, 251, 150)
    ],
    "gameboy": [
        (15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)
    ],
    "solarized": [
        (0, 43, 54), (7, 54, 66), (88, 110, 117), (101, 123, 131),
        (131, 148, 150), (147, 161, 161), (238, 232, 213), (253, 246, 227),
        (181, 137, 0), (203, 75, 22), (220, 50, 47), (211, 54, 130),
        (108, 113, 196), (38, 139, 210), (42, 161, 152), (133, 153, 0)
    ]
}

def apply_theme_palette(image, theme_name):
    """Mapea los colores de la imagen a los colores de la paleta del tema seleccionado."""
    if not theme_name:
        return image
    name_clean = theme_name.lower().strip()
    if name_clean not in THEME_PALETTES:
        return image
    try:
        import numpy as np
        img_rgba = image.convert("RGBA")
        arr = np.array(img_rgba)
        rgb = arr[:, :, :3]
        pal = np.array(THEME_PALETTES[name_clean], dtype=np.int32)
        
        flat_rgb = rgb.reshape(-1, 3).astype(np.int32)
        diff = flat_rgb[:, np.newaxis, :] - pal[np.newaxis, :, :]
        dist_sq = np.sum(diff ** 2, axis=2)
        nearest = np.argmin(dist_sq, axis=1)
        quantized = pal[nearest].astype(np.uint8).reshape(rgb.shape)
        arr[:, :, :3] = quantized
        return Image.fromarray(arr)
    except Exception:
        return image

def apply_crop_and_zoom(image, crop_spec=None, zoom=1.0):
    """Aplica recorte centrado o por coordenadas y zoom digital centrado de alta fidelidad."""
    img = image
    if crop_spec:
        spec = str(crop_spec).lower().strip()
        w, h = img.size
        if spec in ("center", "square", "1:1"):
            min_dim = min(w, h)
            left = (w - min_dim) // 2
            top = (h - min_dim) // 2
            img = img.crop((left, top, left + min_dim, top + min_dim))
        elif "," in spec:
            try:
                coords = [int(v.strip()) for v in spec.split(",")]
                if len(coords) == 4:
                    cx, cy, cw, ch = coords
                    img = img.crop((cx, cy, min(w, cx + cw), min(h, cy + ch)))
            except Exception:
                pass
                
    if zoom and zoom > 1.0:
        w, h = img.size
        new_w = max(4, int(w / zoom))
        new_h = max(4, int(h / zoom))
        left = (w - new_w) // 2
        top = (h - new_h) // 2
        img = img.crop((left, top, left + new_w, top + new_h)).resize((w, h), Image.Resampling.LANCZOS)
        
    return img

def apply_crt_filter(ansi_str, crt_mode="color"):
    """
    Simula un monitor de tubo fósforo CRT con líneas de barrido horizontales alternas (scanlines).
    Modos: 'color' (mantiene RGB con atenuación de líneas), 'green' (fósforo verde P1), 'amber' (fósforo ámbar P3).
    """
    import re
    if not ansi_str or not crt_mode:
        return ansi_str
        
    mode_clean = str(crt_mode).lower().strip() if crt_mode is not True else "color"
    lines = ansi_str.split("\n")
    out_lines = []
    
    fg_pattern = re.compile(r'\x1b\[(38|48);2;(\d+);(\d+);(\d+)m')
    
    for row_idx, line in enumerate(lines):
        is_scanline = (row_idx % 2 == 1)
        factor = 0.60 if is_scanline else 1.0
        
        def repl(match):
            plane = match.group(1)
            r, g, b = int(match.group(2)), int(match.group(3)), int(match.group(4))
            
            if mode_clean in ("green", "p1", "matrix"):
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                nr = 0
                ng = int(min(255, lum * 1.15 * factor))
                nb = int(min(255, lum * 0.15 * factor))
            elif mode_clean in ("amber", "p3", "orange"):
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                nr = int(min(255, lum * factor))
                ng = int(min(255, lum * 0.72 * factor))
                nb = int(min(255, lum * 0.05 * factor))
            else:
                nr = int(r * factor)
                ng = int(g * factor)
                nb = int(b * factor)
                
            return f"\x1b[{plane};2;{nr};{ng};{nb}m"
            
        out_lines.append(fg_pattern.sub(repl, line))
        
    return "\n".join(out_lines)

# Glifos Katakana y código binario para el modo Matrix
MATRIX_RAMP = " ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ10:;."

def render_matrix_art(image, width=80, font_ratio=0.5, animated=False):
    """Renderiza la imagen en glifos Katakana y código binario en verde fósforo Matrix."""
    import time
    aspect = image.height / max(1, image.width)
    target_height = max(5, int(width * aspect * font_ratio))
    
    resized = image.convert("L").resize((width, target_height), Image.Resampling.BILINEAR)
    pixels = resized.load()
    
    ramp_len = len(MATRIX_RAMP)
    lines = []
    
    for y in range(target_height):
        row_str = ""
        for x in range(width):
            lum = pixels[x, y]
            if lum < 15:
                row_str += " "
                continue
            char_idx = int((lum / 255.0) * (ramp_len - 1))
            ch = MATRIX_RAMP[char_idx]
            
            # Verde fósforo con brillo según luminosidad
            if lum > 210:
                fg = "\x1b[38;2;190;255;190m" # resplandor blanco-verde
            elif lum > 140:
                fg = "\x1b[38;2;0;255;65m"   # verde terminal brillante
            elif lum > 70:
                fg = "\x1b[38;2;0;160;30m"   # verde medio
            else:
                fg = "\x1b[38;2;0;70;15m"    # verde oscuro sombra
                
            row_str += f"{fg}{ch}\x1b[0m"
        lines.append(row_str)
        
    full_art = "\n".join(lines)
    
    if animated:
        try:
            import random
            cols = width
            rows = target_height
            drops = [random.randint(-rows, 0) for _ in range(cols)]
            for step in range(25):
                frame_lines = []
                for r in range(rows):
                    frow = ""
                    for c in range(cols):
                        d = drops[c]
                        if d == r:
                            ch = random.choice(MATRIX_RAMP[1:])
                            frow += f"\x1b[1;37m{ch}\x1b[0m"
                        elif d - 6 < r < d:
                            ch = random.choice(MATRIX_RAMP[1:])
                            frow += f"\x1b[38;2;0;255;65m{ch}\x1b[0m"
                        elif r < d - 6:
                            frow += lines[r][c * 19 : (c + 1) * 19] if c * 19 < len(lines[r]) else " "
                        else:
                            frow += " "
                    frame_lines.append(frow)
                drops = [d + 1 if d < rows + 8 else random.randint(-5, 0) for d in drops]
                sys.stdout.write("\033[H" + "\n".join(frame_lines))
                sys.stdout.flush()
                time.sleep(0.04)
        except Exception:
            pass
            
    return full_art

def copy_to_clipboard(text, plain=False):
    """Copia la salida ANSI o texto plano al portapapeles del sistema (Wayland/X11/macOS/WSL)."""
    import subprocess
    import shutil
    import re
    
    payload = re.sub(r'\x1b\[[0-9;]*m', '', text) if plain else text
    
    commands = [
        ["wl-copy"],
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["pbcopy"],
        ["clip.exe"]
    ]
    
    for cmd in commands:
        if shutil.which(cmd[0]):
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                proc.communicate(payload.encode("utf-8"), timeout=2)
                if proc.returncode == 0:
                    mode_str = " (texto plano)" if plain else " (ANSI truecolor)"
                    print(f"\n📋 {_('clipboard_copied_plain') if plain else _('clipboard_copied_ansi')}")
                    return True
            except Exception:
                continue
                
    print(f"\n⚠️ No se detectó ninguna herramienta de portapapeles compatible (wl-copy, xclip, xsel, pbcopy).")
    return False

def render_image_diff(path_a, path_b, width=None):
    """Compara visualmente dos imágenes lado a lado en la terminal con telemetría de diferencias."""
    import math
    import shutil
    try:
        img_a = Image.open(path_a).convert("RGB")
        img_b = Image.open(path_b).convert("RGB")
    except Exception as e:
        print(f"❌ Error al abrir imágenes para diff: {e}")
        return False
        
    term_cols = shutil.get_terminal_size((120, 24)).columns
    total_w = width if width else max(30, min(140, term_cols))
    col_w = max(10, (total_w - 4) // 2)
    
    try:
        import numpy as np
        arr_a = np.array(img_a.resize((100, 100))).astype(np.float32)
        arr_b = np.array(img_b.resize((100, 100))).astype(np.float32)
        rmse = np.sqrt(np.mean((arr_a - arr_b) ** 2))
        delta_pct = min(100.0, (rmse / 255.0) * 100.0)
    except Exception:
        delta_pct = 0.0
        
    print(f"\n\033[1;36m┌─────────────────────────── Lumart Visual Image Diff ───────────────────────────┐\033[0m")
    print(f"\033[1;36m│\033[0m [A] {os.path.basename(path_a)} ({img_a.width}x{img_a.height})")
    print(f"\033[1;36m│\033[0m [B] {os.path.basename(path_b)} ({img_b.width}x{img_b.height})")
    print(f"\033[1;36m│\033[0m {_('diff_delta', delta_pct)}")
    print(f"\033[1;36m└────────────────────────────────────────────────────────────────────────────────┘\033[0m\n")
    
    img_a_res = resize_image(img_a, col_w, is_blocks=True, is_braille=False)
    img_b_res = resize_image(img_b, col_w, is_blocks=True, is_braille=False)
    
    lines_a = convert_image_to_blocks(img_a_res).split("\n")
    lines_b = convert_image_to_blocks(img_b_res).split("\n")
    
    max_h = max(len(lines_a), len(lines_b))
    for r in range(max_h):
        la = lines_a[r] if r < len(lines_a) else " " * col_w
        lb = lines_b[r] if r < len(lines_b) else " " * col_w
        print(f"{la}  \033[1;30m│\033[0m  {lb}")
        
    return True

def run_slideshow(file_list, delay=3.0, width=None, engine=None, theme=None, crt=None):
    """Reproductor de galería interactiva con controles de teclado para la terminal."""
    import glob
    import select
    import termios
    import tty
    import time
    
    expanded = []
    for item in file_list:
        if any(char in item for char in ("*", "?", "[")):
            expanded.extend(sorted(glob.glob(item)))
        elif os.path.isdir(item):
            for ext in ("*.png", "*.jpg", "*.jpeg", "*.gif"):
                expanded.extend(sorted(glob.glob(os.path.join(item, ext))))
        elif os.path.exists(item):
            expanded.append(item)
            
    if not expanded:
        print("❌ No se encontraron imágenes válidas para el pase de diapositivas.")
        return False
        
    print(f"🎬 Iniciando Slideshow ({len(expanded)} imágenes)... Presiona [Espacio] siguiente, [Q] salir.")
    time.sleep(0.8)
    
    idx = 0
    paused = False
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    sys.stdout.write("\033[?25l") # ocultar cursor
    sys.stdout.flush()
    
    try:
        tty.setcbreak(fd)
        last_switch = time.time()
        
        while True:
            cur_path = expanded[idx]
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.write(f"\033[1;30m[{idx+1}/{len(expanded)}] {os.path.basename(cur_path)} (Espacio: sig, Flechas: nav, P: pausa, Q: salir)\033[0m\n\n")
            sys.stdout.flush()
            
            try:
                img = Image.open(cur_path).convert("RGBA")
                if theme:
                    img = apply_theme_palette(img, theme)
                w = width or 80
                art = convert_image_to_blocks(resize_image(img, w, is_blocks=True, is_braille=False))
                if crt:
                    art = apply_crt_filter(art, crt)
                sys.stdout.write(art + "\n")
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f"Error al cargar {cur_path}: {e}\n")
                sys.stdout.flush()
                
            last_switch = time.time()
            
            while True:
                r, _, _ = select.select([sys.stdin], [], [], 0.05)
                if r:
                    ch = sys.stdin.read(1)
                    if ch.lower() == "q" or ch == "\x03":
                        return True
                    elif ch in (" ", "\n") or ch == "n":
                        idx = (idx + 1) % len(expanded)
                        break
                    elif ch.lower() == "p":
                        paused = not paused
                    elif ch.lower() == "r":
                        import random
                        idx = random.randint(0, len(expanded) - 1)
                        break
                    elif ch == "\x1b":
                        seq = sys.stdin.read(2)
                        if seq == "[C":
                            idx = (idx + 1) % len(expanded)
                            break
                        elif seq == "[D":
                            idx = (idx - 1 + len(expanded)) % len(expanded)
                            break
                if not paused and (time.time() - last_switch >= delay):
                    idx = (idx + 1) % len(expanded)
                    break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()
        
    return True

def run_interactive_tui(image_path, initial_width=80):
    """Modo interactivo en vivo en terminal para ajustar parámetros estéticos en tiempo real."""
    import termios
    import tty
    import select
    import time
    
    try:
        base_img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"❌ Error al abrir imagen: {e}")
        return False
        
    cur_width = initial_width or 70
    engines = ["mary", "trumble", "luris"]
    engine_idx = 0
    dithers = ["none", "atkinson", "bayer", "floyd"]
    dither_idx = 0
    themes = [None, "catppuccin", "dracula", "nord", "gruvbox", "synthwave", "gameboy", "solarized"]
    theme_idx = 0
    crts = [None, "color", "green", "amber"]
    crt_idx = 0
    boost = False
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    final_art = ""
    
    try:
        tty.setcbreak(fd)
        while True:
            eng = engines[engine_idx]
            dith = dithers[dither_idx]
            thm = themes[theme_idx]
            crt_val = crts[crt_idx]
            
            work_img = base_img.copy()
            if thm:
                work_img = apply_theme_palette(work_img, thm)
                
            if eng == "luris":
                work_img = resize_image(work_img, cur_width, is_blocks=True, is_braille=False)
                if dith in ("atkinson", "bayer", "floyd"):
                    work_img = apply_bayer_dither(work_img)
                art = convert_image_to_blocks(work_img)
            elif eng == "trumble":
                work_img = resize_image(work_img, cur_width, is_blocks=True, is_braille=False)
                art = convert_image_to_blocks(work_img)
            else:
                if mary is not None:
                    art = mary.render_mary(work_img, cur_width, mode="sextants", raw_colors=not boost)
                else:
                    art = convert_image_to_blocks(resize_image(work_img, cur_width, is_blocks=True, is_braille=False))
                    
            if crt_val:
                art = apply_crt_filter(art, crt_val)
                
            final_art = art
            
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.write(f"\033[1;36m=== Lumart Interactive Live TUI Mode ===\033[0m\n")
            sys.stdout.write(art + "\n")
            sys.stdout.write(f"\033[1;30m─────────────────────────────────────────────────────────────────────────────\033[0m\n")
            sys.stdout.write(f"\033[1;33m[+/- Ancho: {cur_width}]  [M] Motor: {eng}  [T] Tema: {thm or 'ninguno'}  [C] CRT: {crt_val or 'off'}\033[0m\n")
            sys.stdout.write(f"\033[1;33m[D] Dither: {dith}  [B] Boost: {'on' if boost else 'off'}  [S] Guardar  [Enter] Imprimir  [Q] Salir\033[0m\n")
            sys.stdout.flush()
            
            ch = sys.stdin.read(1)
            if ch.lower() == "q" or ch == "\x03":
                return False
            elif ch in ("\r", "\n"):
                sys.stdout.write("\033[H\033[2J")
                sys.stdout.write(art + "\n")
                sys.stdout.flush()
                return True
            elif ch in ("+", "="):
                cur_width = min(200, cur_width + 5)
            elif ch in ("-", "_"):
                cur_width = max(15, cur_width - 5)
            elif ch.lower() == "m":
                engine_idx = (engine_idx + 1) % len(engines)
            elif ch.lower() == "t":
                theme_idx = (theme_idx + 1) % len(themes)
            elif ch.lower() == "c":
                crt_idx = (crt_idx + 1) % len(crts)
            elif ch.lower() == "d":
                dither_idx = (dither_idx + 1) % len(dithers)
            elif ch.lower() == "b":
                boost = not boost
            elif ch.lower() == "s":
                out_name = "lumart_tui_export.ans"
                with open(out_name, "w", encoding="utf-8") as f:
                    f.write(art)
                sys.stdout.write(f"\n💾 Guardado exitosamente en: {out_name}\n")
                sys.stdout.flush()
                time.sleep(1.0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

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

def apply_trumble_cel_shading(image, target_width=None, is_blocks=True, is_braille=False, edge_strength=0.75, saturation=1.30, contrast=1.18):
    """
    Motor Trumble Orelx 2.2: Realce estético Retro-Arcade & Anime Cel-Shading de Alta Fidelidad.
    - Curva de color y contraste arcade estilo Capcom CPS-2 / Neo-Geo (alta vivacidad y pop).
    - Escalado preciso al búfer de subpíxeles antes del entintado.
    - Detección de bordes 1-a-1 subpíxel mediante filtrado bilateral y Canny para trazos anime nítidos.
    """
    # 1. Punch de color arcade y contraste S-curve a resolución completa
    img = image.convert("RGBA")
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))

    # 2. Redimensionar al espacio de subpíxeles antes del entintado para evitar que el remuestreo difumine las líneas
    if target_width is not None:
        scaled = resize_image(img, target_width, is_blocks=is_blocks, is_braille=is_braille)
        was_resized = True
    else:
        scaled = img
        was_resized = False

    try:
        import cv2
        import numpy as np
        rgba = np.array(scaled)
        rgb = rgba[:, :, :3]
        alpha = rgba[:, :, 3]

        # Detección de bordes estructurados en luminancia con filtro bilateral afinado
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        smooth = cv2.bilateralFilter(gray, d=5, sigmaColor=40, sigmaSpace=40)
        canny_edges = cv2.Canny(smooth, 50, 130)

        # Contorno perimetral exterior desde canal alpha
        alpha_edges = cv2.Canny(alpha, 100, 200)
        combined = cv2.bitwise_or(canny_edges, alpha_edges)

        # Entintado subpíxel nítido
        inv_edge = 1.0 - (combined.astype(np.float32) / 255.0 * edge_strength)
        darkened_rgb = (rgb.astype(np.float32) * inv_edge[:, :, None]).clip(0, 255).astype(np.uint8)
        res_pil = Image.fromarray(np.dstack([darkened_rgb, alpha]))
        return res_pil, was_resized
    except Exception:
        return scaled, was_resized

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
            shape_penalty = max(30.0, 900.0 - variance * 0.75)
            
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

def get_lumart_banner():
    """Genera el logotipo oficial de Lumart en arte ANSI con gradiente cromático."""
    c1 = "\033[38;2;64;224;208m"   # Turquesa
    c2 = "\033[38;2;72;191;227m"   # Cyan cielo
    c3 = "\033[38;2;94;142;240m"   # Azul eléctrico
    c4 = "\033[38;2;123;104;238m"  # Púrpura medio
    c5 = "\033[38;2;171;71;238m"   # Magenta brillante
    c6 = "\033[38;2;218;112;214m"  # Orquídea pastel
    rst = "\033[0m"

    return f"""
  {c1}██╗     {c2}██╗   ██╗{c3}███╗   ███╗{c4} █████╗ {c5}██████╗ {c6}████████╗
  {c1}██║     {c2}██║   ██║{c3}████╗ ████║{c4}██╔══██╗{c5}██╔══██╗{c6}╚══██╔══╝
  {c1}██║     {c2}██║   ██║{c3}██╔████╔██║{c4}███████║{c5}██████╔╝{c6}   ██║   
  {c1}██║     {c2}██║   ██║{c3}██║╚██╔╝██║{c4}██╔══██║{c5}██╔══██╗{c6}   ██║   
  {c1}███████╗{c2}╚██████╔╝{c3}██║ ╚═╝ ██║{c4}██║  ██║{c5}██║  ██║{c6}   ██║   
  {c1}╚══════╝{c2} ╚═════╝ {c3}╚═╝     ╚═╝{c4}╚═╝  ╚═╝{c5}╚═╝  ╚═╝{c6}   ╚═╝   {rst}
   \033[1;37mModern Terminal Visual Suite\033[0m \033[38;2;100;149;237m•\033[0m \033[38;2;0;255;200mv{VERSION}\033[0m \033[2m({CODENAME})\033[0m
   \033[2m[ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]\033[0m
"""

def show_version_info():
    """Muestra un informe visual moderno, compacto y minimalista."""
    import platform
    import shutil

    # Colores elegantes estilo Ghostty / Fastfetch
    c_brand = "\033[1;38;2;94;142;240m"   # Azul eléctrico
    c_ver = "\033[1;38;2;0;255;200m"      # Turquesa brillante
    c_dim = "\033[38;2;120;120;140m"      # Gris tenue
    c_ok = "\033[1;38;2;80;250;123m"      # Verde neón
    c_warn = "\033[1;38;2;255;184;108m"   # Naranja suave
    rst = "\033[0m"

    cols, rows = shutil.get_terminal_size((80, 24))
    colorterm = os.environ.get("COLORTERM", "")
    term = os.environ.get("TERM", "")
    has_truecolor = colorterm in ("truecolor", "24bit") or "kitty" in term or "alacritty" in term or "ghostty" in term
    tc_badge = f"{c_ok}TrueColor 24-bit{rst}" if has_truecolor else f"{c_warn}16-Color Banding{rst}"

    # Detección de motores nativos C++
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    base_dir = os.path.dirname(os.path.abspath(__file__))

    has_mary_cpp = any(os.path.exists(os.path.join(d, "libmary.so")) for d in [exe_dir, base_dir, "/usr/local/share/luma", "/usr/share/luma"]) or bool(shutil.which("luma-mary"))
    has_luris_cpp = any(os.path.exists(os.path.join(d, "libmonochrome.so")) for d in [exe_dir, base_dir, "/usr/local/share/luma", "/usr/share/luma"]) or bool(shutil.which("luma-mono"))

    mary_badge = f"{c_ok}C++17 OpenMP{rst}" if has_mary_cpp else f"{c_warn}Python{rst}"
    luris_badge = f"{c_ok}C++17 OpenMP{rst}" if has_luris_cpp else f"{c_warn}Python{rst}"

    has_cv2 = False
    try:
        import cv2
        has_cv2 = True
    except ImportError:
        pass
    spectra_badge = f"{c_ok}Active (30-60 FPS){rst}" if has_cv2 else f"{c_dim}OpenCV required{rst}"

    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    os_info = f"{platform.system()} {platform.machine()}"

    card = f"""
{c_brand}◆ lumart{rst} {c_ver}v{VERSION}{rst} {c_dim}({CODENAME}){rst} {c_dim}•{rst} Modern Terminal Visual Suite
{c_dim}─────────────────────────────────────────────────────────────────{rst}
  {c_dim}Engines:{rst}   Mary Apex 3.5 [{mary_badge}]  •  Trumble Orelx 2.2 [{c_ok}Active{rst}]
             Luris Mono 2.6 [{luris_badge}] •  Spectra Weep 1.4 [{spectra_badge}]
  {c_dim}Terminal:{rst}  {cols}x{rows} cols/lines  •  {tc_badge}
  {c_dim}Runtime:{rst}   Python v{py_ver} ({os_info})
  {c_dim}Source:{rst}    https://github.com/{GITHUB_REPO}
"""
    print(card.strip() + "\n")

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
        print(_("update_error", "GitHub API error"))
        return False
        
    latest_rel = all_releases[0]
    latest_ver = latest_rel["tag_name"]
    cur_tuple = parse_version(VERSION)
    latest_tuple = parse_version(latest_ver)
    
    print(f"\n\033[1m{_('ver_status_title')}\033[0m")
    print(f"   • {_('ver_current_installed')} \033[1;36mv{VERSION}\033[0m")
    print(f"   • {_('ver_latest_github')} \033[1;32mv{latest_ver}\033[0m")
    
    if latest_tuple > cur_tuple:
        print(f"\n\033[1;33m{_('ver_new_available')}\033[0m")
        if latest_rel.get("name"):
            print(f"   {_('ver_release_title')} {latest_rel['name']}")
        print(f"   {_('ver_install_hint')}")
        print(f"   \033[1;32mlumart -uu\033[0m (o \033[1;32mlumart --upgrade\033[0m)")
    else:
        print(f"\n\033[1;32m{_('ver_up_to_date')}\033[0m")
        
    print(f"\n\033[1m{_('ver_recent_history')}\033[0m")
    for r in all_releases[:5]:
        v = r["tag_name"]
        is_cur = f" \033[1;36m{_('ver_tag_current')}\033[0m" if v == VERSION else ""
        date_str = r.get("published_at", "")[:10]
        date_disp = f" [{date_str}]" if date_str else ""
        print(f"   • v{v:<7}{date_disp}{is_cur}")
        
    print(f"\n\033[1m{_('ver_useful_commands')}\033[0m")
    print(f"   • lumart -uu              -> {_('ver_cmd_uu')}")
    print(f"   • lumart -dg              -> {_('ver_cmd_dg')}")
    print(f"   • lumart -v               -> {_('ver_cmd_v')}")
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
    
    cur_tuple = parse_version(VERSION)
    
    # Foolproof guard: si el usuario especifica la versión en la que ya está o una inferior
    if target_ver and target_ver != "latest":
        clean_target = target_ver.lstrip("v").strip()
        target_tuple = parse_version(clean_target)
        if target_tuple == cur_tuple:
            print(_("already_on_version", VERSION))
            return True
        if target_tuple < cur_tuple:
            print(_("upgrade_target_older", clean_target, VERSION, clean_target))
            return False

    print(_("update_checking"))
    all_releases = fetch_all_releases_with_meta()
    if not all_releases:
        print(_("update_error", "No se pudo consultar información de versiones en GitHub."))
        return False
        
    newer = [r for r in all_releases if parse_version(r["tag_name"]) > cur_tuple]
    
    if not newer and (not target_ver or target_ver == "latest"):
        print(_("update_already_latest", VERSION))
        return True
        
    chosen_rel = None
    if target_ver and target_ver != "latest":
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
    if parse_version(dest_ver) == cur_tuple:
        print(_("already_on_version", VERSION))
        return True
        
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
    
    cur_tuple = parse_version(VERSION)
    
    # Foolproof guard: si el usuario especifica la versión en la que ya está o una superior
    if target_ver and target_ver != "prev":
        clean_target = target_ver.lstrip("v").strip()
        target_tuple = parse_version(clean_target)
        if target_tuple == cur_tuple:
            print(_("already_on_version", VERSION))
            return True
        if target_tuple > cur_tuple:
            print(_("downgrade_target_newer", clean_target, VERSION, clean_target))
            return False

    is_frozen = getattr(sys, 'frozen', False)
    target_path = sys.executable if is_frozen else os.path.realpath(__file__)
    target_dir = os.path.dirname(target_path)
    
    if not os.access(target_path, os.W_OK) or not os.access(target_dir, os.W_OK):
        print(_("update_permission_error", target_path))
        return False

    backup_dir = os.path.expanduser("~/.config/luma/backup")
    os.makedirs(backup_dir, exist_ok=True)
    
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
        cand_local = os.path.join(backup_dir, f"lumart-v{chosen_ver}")
        if os.path.exists(cand_local):
            chosen_src = "local"
            chosen_path = cand_local
        else:
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
        for idx, (ver, src, _src_path) in enumerate(options, 1):
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

    if parse_version(chosen_ver) == cur_tuple:
        print(_("already_on_version", VERSION))
        return True

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

def try_render_native_mary(image_path, width, mode="sextants", raw_colors=False, invert=False, font_ratio=0.5):
    """
    Intenta ejecutar el motor nativo Mary en C++ (luma-mary o libmary.so).
    Aceleración C++17 nativa con Guided Filter Oklab O(1), umbral adaptativo Weber-Fechner,
    renderizado multihilo OpenMP y modos subpíxel Sextants/Braille/Quadrants.
    Retorna el string de texto renderizado o None si no se encuentra el binario/librería.
    """
    import ctypes
    import shutil
    import subprocess

    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lib_paths = [
        os.path.join(exe_dir, "libmary.so"),
        os.path.join(base_dir, "libmary.so"),
        os.path.join(exe_dir, "..", "libmary.so"),
        os.path.join(base_dir, "..", "libmary.so"),
        "/usr/local/share/luma/libmary.so",
        "/usr/share/luma/libmary.so",
        "/usr/local/lib/libmary.so",
        "/usr/lib/libmary.so",
        "libmary.so"
    ]
    for lp in lib_paths:
        if os.path.exists(lp):
            try:
                lib = ctypes.CDLL(lp)
                if hasattr(lib, "render_mary_apex_c"):
                    lib.render_mary_apex_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool, ctypes.c_float]
                    lib.render_mary_apex_c.restype = ctypes.c_void_p
                    lib.free_mary_buffer.argtypes = [ctypes.c_void_p]
                    lib.free_mary_buffer.restype = None

                    ptr = lib.render_mary_apex_c(
                        image_path.encode("utf-8"),
                        int(width),
                        mode.encode("utf-8"),
                        bool(raw_colors),
                        bool(invert),
                        float(font_ratio)
                    )
                else:
                    lib.render_mary_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool]
                    lib.render_mary_c.restype = ctypes.c_void_p
                    lib.free_mary_buffer.argtypes = [ctypes.c_void_p]
                    lib.free_mary_buffer.restype = None

                    ptr = lib.render_mary_c(
                        image_path.encode("utf-8"),
                        int(width),
                        mode.encode("utf-8"),
                        bool(raw_colors),
                        bool(invert)
                    )
                if ptr:
                    res_bytes = ctypes.string_at(ptr)
                    lib.free_mary_buffer(ptr)
                    res = res_bytes.decode("utf-8", errors="replace")
                    if res and not res.startswith("❌"):
                        return res
            except Exception:
                pass

    bin_names = [
        os.path.join(exe_dir, "luma-mary"),
        os.path.join(base_dir, "luma-mary"),
        shutil.which("luma-mary")
    ]
    for b in bin_names:
        if b and os.path.exists(b) and os.access(b, os.X_OK):
            try:
                cmd = [b, image_path, "-w", str(width), "-m", mode, "-r", str(font_ratio)]
                if raw_colors:
                    cmd.append("--raw-colors")
                if invert:
                    cmd.append("-i")
                proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
                if proc.stdout and not proc.stdout.startswith("❌"):
                    return proc.stdout
            except Exception:
                pass

    return None

# ==============================================================================
# SEXTANTES, CUADRANTES Y RASTERIZADOR ANSI A IMAGEN (PNG, WEBP, JPG)
# ==============================================================================
SEXTANT_GLYPHS = (
    " ", "🬀", "🬁", "🬂", "🬃", "🬄", "🬅", "🬆",
    "🬇", "🬈", "🬉", "🬊", "🬋", "🬌", "🬍", "🬎",
    "🬏", "🬐", "🬑", "🬒", "🬓", "▌", "🬔", "🬕",
    "🬖", "🬗", "🬘", "🬙", "🬚", "🬛", "🬜", "🬝",
    "🬞", "🬟", "🬠", "🬡", "🬢", "🬣", "🬤", "🬥",
    "🬦", "🬧", "▐", "🬨", "🬩", "🬪", "🬫", "🬬",
    "🬭", "🬮", "🬯", "🬰", "🬱", "🬲", "🬳", "🬴",
    "🬵", "🬶", "🬷", "🬸", "🬹", "🬺", "🬻", "█"
)
SEXTANT_MAP = {ch: idx for idx, ch in enumerate(SEXTANT_GLYPHS) if ch not in (" ", "█")}

QUADRANT_GLYPHS = (
    " ", "▘", "▝", "▀",
    "▖", "▌", "▞", "▛",
    "▗", "▚", "▐", "▜",
    "▄", "▙", "▟", "█"
)
QUADRANT_MAP = {ch: idx for idx, ch in enumerate(QUADRANT_GLYPHS) if ch not in (" ", "▀", "▄", "█")}

def export_ansi_to_image(ansi_text, out_path=None, transparent=False, font_size=16):
    """
    Rasteriza arte ANSI / Unicode a una imagen gráfica de alta definición (.png, .jpg, .gif)
    con geometría subpíxel exacta para bloques y glifos.
    Si out_path es None, retorna el objeto PIL.Image generado en memoria.
    """
    from PIL import ImageDraw, ImageFont

    ext = os.path.splitext(out_path)[1].lower() if out_path else ""
    if ext == ".webp":
        raise ValueError("El formato .webp no está soportado para exportación. Por favor use .png, .jpg o .gif.")
    if out_path and ext not in (".png", ".jpg", ".jpeg", ".gif"):
        raise ValueError(f"Formato no soportado: '{ext}'. Solo se permite exportar a .png, .jpg y .gif.")

    is_alpha_supported = (ext == ".png" or out_path is None)
    use_transparent = transparent and is_alpha_supported

    ansi_pattern = re.compile(r'\033\[([0-9;]+)m')
    raw_lines = ansi_text.split('\n')
    while raw_lines and not raw_lines[-1].strip():
        raw_lines.pop()

    if not raw_lines:
        raise ValueError("El texto ANSI está vacío.")

    # Buscar fuentes monospace comunes del sistema
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf"
    ]
    font = None
    for fc in font_candidates:
        if os.path.exists(fc):
            try:
                font = ImageFont.truetype(fc, font_size)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    cell_w = 9
    cell_h = 18

    parsed_lines = []
    max_cols = 0

    for line in raw_lines:
        parsed_chars = []
        cur_fg = (220, 220, 220)
        cur_bg = None
        pos = 0
        while pos < len(line):
            m = ansi_pattern.match(line, pos)
            if m:
                code_str = m.group(1)
                codes = [int(x) for x in code_str.split(';') if x.isdigit()]
                if not codes or 0 in codes:
                    cur_fg = (220, 220, 220)
                    cur_bg = None
                i = 0
                while i < len(codes):
                    c = codes[i]
                    if c == 0:
                        cur_fg = (220, 220, 220)
                        cur_bg = None
                        i += 1
                    elif c == 39:
                        cur_fg = (220, 220, 220)
                        i += 1
                    elif c == 49:
                        cur_bg = None
                        i += 1
                    elif c == 38 and i + 4 < len(codes) and codes[i + 1] == 2:
                        cur_fg = (codes[i + 2], codes[i + 3], codes[i + 4])
                        i += 5
                    elif c == 48 and i + 4 < len(codes) and codes[i + 1] == 2:
                        cur_bg = (codes[i + 2], codes[i + 3], codes[i + 4])
                        i += 5
                    else:
                        i += 1
                pos = m.end()
            else:
                ch = line[pos]
                if ch != '\r':
                    parsed_chars.append((ch, cur_fg, cur_bg))
                pos += 1
        max_cols = max(max_cols, len(parsed_chars))
        parsed_lines.append(parsed_chars)

    pad_x = 24
    pad_y = 24
    img_w = max_cols * cell_w + pad_x * 2
    img_h = len(parsed_lines) * cell_h + pad_y * 2

    mode = "RGBA" if use_transparent else "RGB"
    bg_color = (0, 0, 0, 0) if use_transparent else (17, 17, 22)

    img = Image.new(mode, (img_w, img_h), color=bg_color)
    draw = ImageDraw.Draw(img)

    y_offset = pad_y
    for row in parsed_lines:
        x_offset = pad_x
        for ch, fg, bg in row:
            if bg is not None:
                bg_rgba = (*bg, 255) if use_transparent else bg
                draw.rectangle([x_offset, y_offset, x_offset + cell_w, y_offset + cell_h], fill=bg_rgba)

            fg_rgba = (*fg, 255) if use_transparent else fg

            # Dibujo geométrico exacto
            if ch == '▀':
                draw.rectangle([x_offset, y_offset, x_offset + cell_w, y_offset + cell_h // 2], fill=fg_rgba)
            elif ch == '▄':
                draw.rectangle([x_offset, y_offset + cell_h // 2, x_offset + cell_w, y_offset + cell_h], fill=fg_rgba)
            elif ch == '█':
                draw.rectangle([x_offset, y_offset, x_offset + cell_w, y_offset + cell_h], fill=fg_rgba)
            elif ch == '▌':
                draw.rectangle([x_offset, y_offset, x_offset + cell_w // 2, y_offset + cell_h], fill=fg_rgba)
            elif ch == '▐':
                draw.rectangle([x_offset + cell_w // 2, y_offset, x_offset + cell_w, y_offset + cell_h], fill=fg_rgba)
            elif ch in SEXTANT_MAP:
                mask = SEXTANT_MAP[ch]
                sw = cell_w / 2.0
                sh = cell_h / 3.0
                for bit in range(6):
                    if mask & (1 << bit):
                        col = bit % 2
                        row_idx = bit // 2
                        x0 = int(x_offset + col * sw)
                        y0 = int(y_offset + row_idx * sh)
                        x1 = int(x_offset + (col + 1) * sw)
                        y1 = int(y_offset + (row_idx + 1) * sh)
                        draw.rectangle([x0, y0, x1, y1], fill=fg_rgba)
            elif ch in QUADRANT_MAP:
                mask = QUADRANT_MAP[ch]
                hw = cell_w // 2
                hh = cell_h // 2
                if mask & 1: draw.rectangle([x_offset, y_offset, x_offset + hw, y_offset + hh], fill=fg_rgba)
                if mask & 2: draw.rectangle([x_offset + hw, y_offset, x_offset + cell_w, y_offset + hh], fill=fg_rgba)
                if mask & 4: draw.rectangle([x_offset, y_offset + hh, x_offset + hw, y_offset + cell_h], fill=fg_rgba)
                if mask & 8: draw.rectangle([x_offset + hw, y_offset + hh, x_offset + cell_w, y_offset + cell_h], fill=fg_rgba)
            elif 0x2800 <= ord(ch) <= 0x28FF:
                val = ord(ch) - 0x2800
                dot_coords = [
                    (0, 0), (0, 1), (0, 2), (1, 0),
                    (1, 1), (1, 2), (0, 3), (1, 3)
                ]
                dw = cell_w / 2.0
                dh = cell_h / 4.0
                r = 1.2
                for bit in range(8):
                    if val & (1 << bit):
                        col, row_idx = dot_coords[bit]
                        cx = x_offset + (col + 0.5) * dw
                        cy = y_offset + (row_idx + 0.5) * dh
                        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fg_rgba)
            elif ch != ' ':
                draw.text((x_offset + 1, y_offset), ch, font=font, fill=fg_rgba)

            x_offset += cell_w
        y_offset += cell_h

    if out_path is None:
        return img

    # Guardar imagen con opciones óptimas
    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    save_kwargs = {}
    if ext in (".jpg", ".jpeg"):
        save_kwargs = {"quality": 95, "optimize": True}
    elif ext == ".png":
        save_kwargs = {"optimize": True}
    elif ext == ".gif":
        save_kwargs = {"optimize": True}

    img.save(out_path, **save_kwargs)
    return True

# ==============================================================================
# EFECTO REVEAL (ESCÁNER LÁSER PROGRESIVO)
# ==============================================================================
def print_with_reveal(ansi_text, instant=True, delay=0.0015):
    """
    Imprime la salida visual con soporte para modo instantáneo o reveal progresivo.
    """
    if instant or not sys.stdout.isatty():
        sys.stdout.write(ansi_text + "\n")
        sys.stdout.flush()
        return
    for line in ansi_text.splitlines():
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)

# ==============================================================================
# ENTRADAS MODERNAS (URLS DIRECTAS, PORTAPAPELES Y STDIN)
# ==============================================================================
def load_image_from_source(source_path, paste=False):
    """
    Carga una imagen desde múltiples orígenes (portapapeles, URL http/https, STDIN o archivo en disco),
    aplicando corrección automática de orientación EXIF para smartphones y cámaras digitales.
    """
    import io
    from PIL import ImageOps

    img = None
    # 1. Portapapeles (--paste o 'clip:')
    if paste or source_path in ("clip:", "clipboard"):
        # Wayland (wl-paste)
        if shutil.which("wl-paste"):
            try:
                proc = subprocess.run(["wl-paste", "--type", "image/png"], capture_output=True, timeout=3)
                if proc.returncode == 0 and len(proc.stdout) > 0:
                    img = Image.open(io.BytesIO(proc.stdout)).convert("RGBA")
            except Exception:
                pass
        # X11 (xclip)
        if img is None and shutil.which("xclip"):
            try:
                proc = subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-o"], capture_output=True, timeout=3)
                if proc.returncode == 0 and len(proc.stdout) > 0:
                    img = Image.open(io.BytesIO(proc.stdout)).convert("RGBA")
            except Exception:
                pass
        # Pillow ImageGrab
        if img is None:
            try:
                from PIL import ImageGrab
                clip_img = ImageGrab.grabclipboard()
                if isinstance(clip_img, Image.Image):
                    img = clip_img.convert("RGBA")
            except Exception:
                pass
        if img is None:
            raise ValueError("No se encontró ninguna imagen en el portapapeles del sistema (o faltan 'wl-paste' / 'xclip').")

    # 2. STDIN Pipe (cat imagen | lumart)
    elif source_path == "-" or (source_path is None and not sys.stdin.isatty()):
        try:
            stdin_data = sys.stdin.buffer.read()
            if len(stdin_data) > 0:
                img = Image.open(io.BytesIO(stdin_data)).convert("RGBA")
            else:
                raise ValueError("Buffer de entrada STDIN vacío.")
        except Exception as e:
            raise ValueError(f"Error al leer imagen desde STDIN: {e}")

    # 3. URL directa (http / https)
    elif source_path and (source_path.startswith("http://") or source_path.startswith("https://")):
        try:
            req = urllib.request.Request(
                source_path,
                headers={"User-Agent": f"Mozilla/5.0 (X11; Linux x86_64) Lumart/{VERSION}"}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                data = response.read()
                img = Image.open(io.BytesIO(data)).convert("RGBA")
        except Exception as e:
            raise ValueError(f"No se pudo descargar la imagen desde la URL: {e}")

    # 4. Archivo local en disco
    else:
        if not source_path:
            raise ValueError("No se especificó ninguna ruta de imagen ni fuente de entrada.")
        img = Image.open(source_path)

    # Auto-orientación según metadatos EXIF
    if img is not None:
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

    return img

# ==============================================================================
# ==============================================================================
# MOTOR SPECTRA WEEP 1.4: CÁMARA WEB EN VIVO EN TIEMPO REAL CON FILTROS
# ==============================================================================
def run_spectra_webcam(cam_index=0, target_width=None, font_ratio=0.5):
    """
    Motor Spectra Weep 1.4: Transmisión de cámara web en vivo y tiempo real en la terminal a 30-60 FPS
    con 5 filtros de gradación cromática interactivos intercambiables al vuelo.
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("\n\033[1;31m❌ [Spectra Weep] Se requiere el paquete 'opencv-python' para usar la cámara web.\033[0m")
        print("   Instálalo fácilmente ejecutando:")
        print("   \033[1;32mpip install opencv-python --user\033[0m\n")
        return False

    print(f"\033[1;35m[Spectra Weep 1.4]\033[0m Conectando con cámara web (índice {cam_index})...")
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"❌ Error: No se pudo conectar a la cámara web en el índice {cam_index}.")
        return False

    term_size = shutil.get_terminal_size((80, 24))
    if target_width is None:
        target_width = min(120, max(30, term_size.columns))

    aspect = 0.75
    target_h_chars = int(target_width * aspect * font_ratio)
    target_h_chars = max(10, min(term_size.lines - 3, target_h_chars))
    frame_h_px = target_h_chars * 2

    # Configuración de entrada no bloqueante en terminal para alternar filtros
    old_term_settings = None
    is_interactive_tty = sys.stdin.isatty() and sys.stdout.isatty()
    if is_interactive_tty:
        try:
            import tty
            import termios
            old_term_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except Exception:
            pass

    sys.stdout.write("\033[?25l\033[2J\033[H")
    sys.stdout.flush()

    fps_count = 0
    fps_start = time.time()
    cur_fps = 30.0
    active_filter = 0

    FILTER_NAMES = [
        "Normal (TrueColor)",
        "Weep Cyberpunk",
        "Matrix Phosphor",
        "Thermal FLIR",
        "Manga Ink (B&W)"
    ]

    try:
        while True:
            # Comprobar si el usuario presionó una tecla (1-5 o q)
            if is_interactive_tty:
                try:
                    import select
                    r, _, _ = select.select([sys.stdin], [], [], 0)
                    if r:
                        ch = sys.stdin.read(1)
                        if ch in ('q', 'Q', '\x03'): # 'q' o Ctrl+C
                            break
                        elif ch == '1': active_filter = 0
                        elif ch == '2': active_filter = 1
                        elif ch == '3': active_filter = 2
                        elif ch == '4': active_filter = 3
                        elif ch == '5': active_filter = 4
                except Exception:
                    pass

            ret, frame = cap.read()
            if not ret:
                break

            frame_resized = cv2.resize(frame, (target_width, frame_h_px), interpolation=cv2.INTER_AREA)

            # Aplicar filtro de imagen en vivo
            if active_filter == 0:
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            elif active_filter == 1:
                # Weep Cyberpunk: Realce de cian, magenta y saturación alta
                rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB).astype(np.float32)
                rgb[:, :, 0] = np.clip(rgb[:, :, 0] * 1.35, 0, 255)
                rgb[:, :, 1] = np.clip(rgb[:, :, 1] * 0.70, 0, 255)
                rgb[:, :, 2] = np.clip(rgb[:, :, 2] * 1.40, 0, 255)
                frame_rgb = rgb.astype(np.uint8)
            elif active_filter == 2:
                # Matrix Phosphor: Monocromático verde fósforo P1
                gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                frame_rgb = np.zeros((frame_h_px, target_width, 3), dtype=np.uint8)
                frame_rgb[:, :, 1] = gray
                frame_rgb[:, :, 0] = (gray * 0.12).astype(np.uint8)
                frame_rgb[:, :, 2] = (gray * 0.15).astype(np.uint8)
            elif active_filter == 3:
                # Thermal FLIR: Espectro térmico infrarrojo
                gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                thermal_bgr = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
                frame_rgb = cv2.cvtColor(thermal_bgr, cv2.COLOR_BGR2RGB)
            elif active_filter == 4:
                # Manga Ink: Alto contraste estilo cómic / tinta
                gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
                frame_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
            else:
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            lines = []
            for y in range(0, frame_h_px, 2):
                row_top = frame_rgb[y]
                row_bot = frame_rgb[y + 1] if y + 1 < frame_h_px else row_top
                line_parts = []
                last_fg = None
                last_bg = None
                for x in range(target_width):
                    r1, g1, b1 = int(row_top[x, 0]), int(row_top[x, 1]), int(row_top[x, 2])
                    r2, g2, b2 = int(row_bot[x, 0]), int(row_bot[x, 1]), int(row_bot[x, 2])
                    color_code = ""
                    if (r1, g1, b1) != last_fg:
                        color_code += f"\033[38;2;{r1};{g1};{b1}m"
                        last_fg = (r1, g1, b1)
                    if (r2, g2, b2) != last_bg:
                        color_code += f"\033[48;2;{r2};{g2};{b2}m"
                        last_bg = (r2, g2, b2)
                    line_parts.append(color_code + "▀")
                line_parts.append("\033[0m")
                lines.append("".join(line_parts))

            fps_count += 1
            if time.time() - fps_start >= 1.0:
                cur_fps = fps_count / (time.time() - fps_start)
                fps_count = 0
                fps_start = time.time()

            filter_tag = FILTER_NAMES[active_filter]
            status_bar = f"\033[1;30;45m SPECTRA WEEP 1.4 \033[0m \033[1;37mCámara: {cam_index} | {target_width}x{target_h_chars} | {cur_fps:.1f} FPS | Filtro: [{filter_tag}] (1-5) | 'q' salir\033[0m"
            sys.stdout.write("\033[H" + "\n".join(lines) + "\n" + status_bar)
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if old_term_settings and is_interactive_tty:
            try:
                import termios
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_term_settings)
            except Exception:
                pass
        sys.stdout.write("\033[?25h\033[0m\n")
        sys.stdout.flush()
        print("✨ Transmisión en vivo de Spectra Weep 1.4 finalizada.")

    return True

# ==============================================================================
# GESTIÓN DE HISTORIAL INTELIGENTE Y REPLAY
# ==============================================================================
def get_history_file():
    config_dir = os.path.expanduser("~/.config/luma")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "history.log")

def record_command_to_history():
    """Registra la invocación de Lumart en ~/.config/luma/history.log"""
    skip_args = {"-H", "--history", "-R", "--replay", "--last", "--clear-history", "-h", "--help", "-v", "--version", "--install-desktop", "--completions"}
    if any(arg in skip_args for arg in sys.argv[1:]):
        return

    if len(sys.argv) < 2:
        return

    hist_file = get_history_file()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cmd_line = "lumart " + " ".join(shlex.quote(a) for a in sys.argv[1:])

    # Evitar duplicados consecutivos
    if os.path.exists(hist_file):
        try:
            with open(hist_file, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                if lines and lines[-1].strip().endswith(cmd_line):
                    return
        except Exception:
            pass

    try:
        with open(hist_file, "a", encoding="utf-8") as f:
            f.write(f"{now_str} | v{VERSION} | {cmd_line}\n")
    except Exception:
        pass

def get_combined_history(limit=None, search=None):
    """Combina ~/.bash_history (antiguos) y ~/.config/luma/history.log (recientes)."""
    entries = []

    # 1. Leer comandos previos de ~/.bash_history primero (son los más antiguos)
    bash_hist = os.path.expanduser("~/.bash_history")
    if os.path.exists(bash_hist):
        try:
            with open(bash_hist, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("lumart ") or line.startswith("luma ") or line.startswith("python3 lumart.py "):
                        if not any(sw in line for sw in ("--history", "-H", "--clear-history", "--replay", "-R", "--last")):
                            entries.append({"timestamp": "(anterior)", "cmd": line})
        except Exception:
            pass

    # 2. Leer history.log de Luma (los más recientes y con timestamp exacto)
    hist_file = get_history_file()
    if os.path.exists(hist_file):
        try:
            with open(hist_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if " | " in line:
                        parts = line.split(" | ")
                        if len(parts) >= 3:
                            ts, ver, cmd = parts[0], parts[1], " | ".join(parts[2:])
                        elif len(parts) == 2:
                            ts, ver, cmd = parts[0], "v2.3.0", parts[1]
                        else:
                            ts, ver, cmd = "----", f"v{VERSION}", line
                    else:
                        ts, ver, cmd = "----", f"v{VERSION}", line
                    entries.append({"timestamp": ts, "version": ver, "cmd": cmd})
        except Exception:
            pass

    if search:
        s_low = search.lower()
        entries = [e for e in entries if s_low in e["cmd"].lower()]

    # Deduplicar preservando los más recientes
    deduped = []
    seen = set()
    for e in reversed(entries):
        cmd_clean = e["cmd"].strip()
        if cmd_clean not in seen:
            seen.add(cmd_clean)
            deduped.append(e)

    if limit and isinstance(limit, int) and limit > 0:
        deduped = deduped[:limit]

    return deduped

def display_command_history(limit=None, search=None):
    entries = get_combined_history(limit=limit, search=search)
    print("\n\033[1;36m █    █ █ █▄ ▄█ ▄▀▄ █▀▄ ▀█▀\033[0m")
    print("\033[1;36m █▄▄▄ ▀▄█ █ ▀ █ █▀█ █▀▄  █\033[0m")
    print(f"\033[1m{_('hist_title', len(entries))}\033[0m\n")

    if not entries:
        print(f"{_('hist_empty')}\n")
        return

    h_num = _("hist_header_num")
    h_ver = _("hist_header_ver")
    h_date = _("hist_header_date")
    h_cmd = _("hist_header_cmd")
    print(f"  \033[1m{h_num:<5} {h_ver:<9} {h_date:<19} {h_cmd}\033[0m")
    print("  " + "─" * 78)

    for i, item in enumerate(entries, 1):
        ts = item["timestamp"]
        ver = item.get("version", "legacy")
        cmd = item["cmd"]
        cmd_h = cmd.replace("lumart", "\033[1;32mlumart\033[0m").replace("luma", "\033[1;32mluma\033[0m")
        print(f"  \033[1;33m[{i:02d}]\033[0m  \033[36m{ver:<9}\033[0m \033[90m{ts:<19}\033[0m {cmd_h}")
    print("  " + "─" * 78)
    print(f"  {_('hist_replay_hint')}\n")

def replay_command(target_idx=1):
    entries = get_combined_history()
    if not entries:
        print(_("hist_empty"))
        return

    try:
        idx = int(target_idx)
        if idx < 1 or idx > len(entries):
            print(_("hist_out_of_range", target_idx, len(entries)))
            return
        selected = entries[idx - 1]["cmd"]
    except ValueError:
        print(_("hist_int_required"))
        return

    print(f"\n{_('hist_replaying', target_idx, selected)}\n")
    args_list = shlex.split(selected)
    if args_list and args_list[0] in ("python", "python3"):
        if len(args_list) > 1 and ("lumart" in args_list[1] or "luma" in args_list[1]):
            args_list = args_list[2:]
        else:
            args_list = args_list[1:]
    elif args_list and args_list[0] in ("lumart", "luma"):
        args_list = args_list[1:]
    elif args_list and ("lumart.py" in args_list[0] or "luma.py" in args_list[0]):
        args_list = args_list[1:]

    sys.argv = [sys.argv[0]] + args_list
    main()

def clear_command_history():
    hist_file = get_history_file()
    if os.path.exists(hist_file):
        try:
            os.remove(hist_file)
            print(_("hist_cleared"))
        except Exception as e:
            print(f"❌ {e}")
    else:
        print(_("hist_already_empty"))

# ==============================================================================
# INTEGRACIÓN CON ESCRITORIO LINUX Y GESTORES DE ARCHIVOS
# ==============================================================================
def install_desktop_integration():
    """Instala el lanzador de escritorio y scripts de clic derecho para gestores de archivos."""
    print("\n🖥️  \033[1mInstalando integración de escritorio y gestores de archivos...\033[0m")
    app_dir = os.path.expanduser("~/.local/share/applications")
    os.makedirs(app_dir, exist_ok=True)

    desktop_file = os.path.join(app_dir, "lumart.desktop")
    desktop_content = """[Desktop Entry]
Type=Application
Name=Lumart Terminal Art
Comment=Render images as high-fidelity terminal art
Exec=lumart %f
Icon=image-x-generic
Terminal=true
Categories=Graphics;Viewer;
MimeType=image/jpeg;image/png;image/webp;image/gif;image/bmp;image/tiff;
NoDisplay=false
"""
    try:
        with open(desktop_file, "w") as f:
            f.write(desktop_content)
        print(f"  ✅ Lanzador de escritorio instalado: {desktop_file}")
    except Exception as e:
        print(f"  ❌ Error creando {desktop_file}: {e}")

    # Scripts de clic derecho para Nautilus y Nemo
    for fm, fm_path in [("Nautilus", "~/.local/share/nautilus/scripts"), ("Nemo", "~/.local/share/nemo/scripts")]:
        s_dir = os.path.expanduser(fm_path)
        os.makedirs(s_dir, exist_ok=True)
        s_file = os.path.join(s_dir, "Abrir con Lumart")
        s_content = """#!/bin/bash
for f in "$@"; do
    if command -v x-terminal-emulator &>/dev/null; then
        x-terminal-emulator -e bash -c "lumart '$f'; echo ''; read -p 'Presiona Enter para cerrar...' key" &
    elif command -v gnome-terminal &>/dev/null; then
        gnome-terminal -- bash -c "lumart '$f'; echo ''; read -p 'Presiona Enter para cerrar...' key" &
    elif command -v kitty &>/dev/null; then
        kitty bash -c "lumart '$f'; echo ''; read -p 'Presiona Enter para cerrar...' key" &
    elif command -v alacritty &>/dev/null; then
        alacritty -e bash -c "lumart '$f'; echo ''; read -p 'Presiona Enter para cerrar...' key" &
    elif command -v konsole &>/dev/null; then
        konsole -e bash -c "lumart '$f'; echo ''; read -p 'Presiona Enter para cerrar...' key" &
    elif command -v xterm &>/dev/null; then
        xterm -e bash -c "lumart '$f'; echo ''; read -p 'Presiona Enter para cerrar...' key" &
    fi
done
"""
        try:
            with open(s_file, "w") as f:
                f.write(s_content)
            os.chmod(s_file, 0o755)
            print(f"  ✅ Menú contextual de {fm}: {s_file}")
        except Exception:
            pass

    if shutil.which("update-desktop-database"):
        try:
            subprocess.run(["update-desktop-database", app_dir], capture_output=True)
        except Exception:
            pass

    print("\n🎉 \033[1;32m¡Integración completada exitosamente!\033[0m")
    print("   Ahora puedes hacer clic derecho sobre cualquier imagen en tu gestor de archivos")
    print("   y seleccionar 'Abrir con Lumart' o 'Scripts > Abrir con Lumart'.\n")

# ==============================================================================
# GENERACIÓN DE AUTOCOMPLETADO DE SHELL (BASH, ZSH, FISH)
# ==============================================================================
def generate_shell_completions(shell_name: str) -> str:
    """Genera el script de autocompletado para Bash, Zsh o Fish."""
    shell = (shell_name or "").strip().lower()
    file_map = {
        "bash": "lumart.bash",
        "zsh": "_lumart",
        "fish": "lumart.fish"
    }
    target_file = file_map.get(shell)
    if not target_file:
        return f"# Error: shell '{shell_name}' no soportado. Disponibles: bash, zsh, fish\n"

    # Buscar en rutas del sistema, paquete y repositorio local
    search_dirs = []
    if hasattr(sys, "_MEIPASS"):
        search_dirs.append(os.path.join(sys._MEIPASS, "completions"))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    search_dirs.append(os.path.join(script_dir, "completions"))
    search_dirs.append(os.path.join(os.path.expanduser("~/.local/share/luma"), "completions"))
    search_dirs.append(os.path.expanduser("~/.local/share/zsh/site-functions"))
    search_dirs.append(os.path.expanduser("~/.local/share/bash-completion/completions"))
    search_dirs.append(os.path.expanduser("~/.local/share/fish/vendor_completions.d"))
    search_dirs.append("/usr/local/share/luma/completions")
    search_dirs.append("/usr/share/luma/completions")
    search_dirs.append("/usr/share/bash-completion/completions" if shell == "bash" else "/usr/share/zsh/site-functions")
    search_dirs.append("/usr/share/fish/vendor_completions.d")

    for d in search_dirs:
        p = os.path.join(d, target_file)
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass

    # Generadores dinámicos de respaldo en caso de que no existan los archivos en disco
    opts_list = (
        "-h --help -v --version -u --update --check-update -uu --upgrade "
        "-dg --downgrade --rollback -w --width -F --fit -E --engine -c --color "
        "--no-color -S --sextants -B --braille -Q --quadrants --blocks -m --manga "
        "-s --sketch --boost --vibrant -i --invert --swap -d --dither --font-ratio "
        "-o -O --output --save --loop --fastfetch --logo -r --remove-bg --transparent "
        "--instant --no-reveal --reveal --paste --lang --theme --palette --crt --scanlines "
        "--matrix --matrix-rain -C --copy --copy-plain --crop --zoom --slideshow --delay "
        "-I --interactive --tui --diff -W --webcam -H --history -R --replay --last "
        "--clear-history --install-desktop --completions"
    )
    if shell == "bash":
        return f"""# Bash completion for lumart and luma
# Generated for Lumart v2.5.0 "Apex Nova"
_lumart_completions() {{
    local cur prev words cword
    _init_completion || return
    local engines="mary trumble luris spectra color mono bw manga sketch"
    local dithers="atkinson floyd bayer none"
    local langs="en es pt fr ru ja de ko"
    local shells="bash zsh fish"
    local themes="catppuccin dracula nord gruvbox synthwave vaporwave gameboy solarized"
    local crts="green amber color scanlines"
    local opts="{opts_list}"
    case "$prev" in
        -E|--engine) COMPREPLY=( $(compgen -W "$engines" -- "$cur") ); return 0 ;;
        -d|--dither) COMPREPLY=( $(compgen -W "$dithers" -- "$cur") ); return 0 ;;
        --lang) COMPREPLY=( $(compgen -W "$langs" -- "$cur") ); return 0 ;;
        --theme|--palette) COMPREPLY=( $(compgen -W "$themes" -- "$cur") ); return 0 ;;
        --crt|--scanlines) COMPREPLY=( $(compgen -W "$crts" -- "$cur") ); return 0 ;;
        --completions) COMPREPLY=( $(compgen -W "$shells" -- "$cur") ); return 0 ;;
        -o|-O|--output|--save) _filedir '@(png|jpg|jpeg|gif|ans|asc|txt)' 2>/dev/null || COMPREPLY=( $(compgen -f -- "$cur") ); return 0 ;;
        --diff) _filedir '@(png|jpg|jpeg|bmp|gif|webp|apng)' 2>/dev/null || COMPREPLY=( $(compgen -f -- "$cur") ); return 0 ;;
    esac
    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
        return 0
    fi
    if [[ "${{words[1]}}" == "diff" ]]; then
        _filedir '@(png|jpg|jpeg|bmp|gif|webp|apng)' 2>/dev/null || COMPREPLY=( $(compgen -f -- "$cur") )
        return 0
    fi
    _filedir '@(png|jpg|jpeg|bmp|gif|webp|apng)' 2>/dev/null || COMPREPLY=( $(compgen -f -- "$cur") )
}}
complete -F _lumart_completions lumart
complete -F _lumart_completions luma
"""
    elif shell == "fish":
        return f"""# Fish completion for lumart and luma
# Generated for Lumart v2.5.0 "Apex Nova"
for c in lumart luma
    complete -c $c -s h -l help -d "Show usage and options help"
    complete -c $c -s v -l version -d "Display hardware and engine status"
    complete -c $c -s u -l update -l check-update -d "Check for latest release"
    complete -c $c -l uu -l upgrade -d "Perform automatic upgrade"
    complete -c $c -l dg -l downgrade -d "Rollback to previous version" -r
    complete -c $c -s w -l width -d "Output width in columns" -r
    complete -c $c -s F -l fit -d "Auto-fit to terminal viewport"
    complete -c $c -l crop -d "Crop image: center, square, or x,y,w,h" -r
    complete -c $c -l zoom -d "Digital zoom factor centered on subject" -r
    complete -c $c -s E -l engine -d "Select rendering engine" -r -a "mary trumble luris spectra color mono bw manga sketch"
    complete -c $c -s c -l color -d "Force TrueColor output"
    complete -c $c -l no-color -d "Disable color output"
    complete -c $c -s S -l sextants -d "Unicode 2x3 sextant blocks (Mary Apex default)"
    complete -c $c -s B -l braille -d "Unicode 2x4 braille characters (8 subpixels)"
    complete -c $c -s Q -l quadrants -d "Unicode 2x2 quadrant blocks (4 subpixels)"
    complete -c $c -l blocks -d "Optimized terminal half-blocks"
    complete -c $c -s m -l manga -d "Manga Screentone 2.0 mode"
    complete -c $c -s s -l sketch -d "Clean line sketch mode"
    complete -c $c -l matrix -d "Render image in digital Katakana and binary green Matrix code"
    complete -c $c -l matrix-rain -d "Falling Katakana digital rain animation"
    complete -c $c -l boost -l vibrant -d "Vibrant arcade Retinex boost"
    complete -c $c -s i -l invert -d "Invert character lightness"
    complete -c $c -s d -l dither -d "Dithering algorithm" -r -a "atkinson floyd bayer none"
    complete -c $c -l font-ratio -d "Calibrate font aspect ratio" -r
    complete -c $c -l theme -l palette -d "Terminal color palette" -r -a "catppuccin dracula nord gruvbox synthwave vaporwave gameboy solarized"
    complete -c $c -l crt -l scanlines -d "Simulate retro CRT scanlines and phosphor monitor" -r -a "green amber color scanlines"
    complete -c $c -s o -s O -l output -l save -d "Export image, GIF, ANS, or TXT" -r
    complete -c $c -l loop -d "Animation mode: smooth terminal loop or animated GIF export"
    complete -c $c -s r -l remove-bg -d "Remove background without quality loss (standalone saves HD PNG)"
    complete -c $c -l transparent -d "Luris Mono transparent sticker"
    complete -c $c -s C -l copy -d "Copy rendered ANSI art to system clipboard"
    complete -c $c -l copy-plain -d "Copy plain ASCII text without escape codes to clipboard"
    complete -c $c -l instant -d "Display output immediately"
    complete -c $c -l reveal -d "Progressive reveal scan animation"
    complete -c $c -l paste -d "Render image from clipboard"
    complete -c $c -s I -l interactive -l tui -d "Interactive live parameter tuning terminal UI"
    complete -c $c -l slideshow -d "Interactive terminal slideshow gallery"
    complete -c $c -l delay -d "Slideshow delay between images in seconds" -r
    complete -c $c -l diff -d "Side-by-side terminal image comparison" -r
    complete -c $c -l lang -d "Set interface language" -r -a "en es pt fr ru ja de ko"
    complete -c $c -s W -l webcam -d "Webcam streaming 30-60 FPS" -r
    complete -c $c -s H -l history -d "Show execution history" -r
    complete -c $c -s R -l replay -d "Re-run command from history" -r
    complete -c $c -l clear-history -d "Wipe command history"
    complete -c $c -l install-desktop -d "Register file manager context menu"
    complete -c $c -l completions -d "Generate shell completion script" -r -a "bash zsh fish"
end
"""
    elif shell == "zsh":
        return f"""#compdef lumart luma
# Generated for Lumart v2.5.0 "Apex Nova"
_lumart() {{
    local context state state_descr line
    typeset -A opt_args
    _arguments -s -S \\
        '(-h --help)'{{-h,--help}}'[Show usage and options help]' \\
        '(-v --version)'{{-v,--version}}'[Display hardware, OS and engine diagnostic card]' \\
        '(-u --update --check-update)'{{-u,--update,--check-update}}'[Check for latest version on GitHub]' \\
        '(-uu --upgrade)'{{-uu,--upgrade}}'[Perform interactive automatic upgrade]' \\
        '(-dg --downgrade --rollback)'{{-dg,--downgrade,--rollback}}'[Rollback to previous version]:version: ' \\
        '(-w --width)'{{-w,--width}}'[Set output width in terminal columns]:columns: ' \\
        '(-F --fit)'{{-F,--fit}}'[Auto-fit to terminal viewport width and height]' \\
        '--fastfetch[Auto-crop empty margins for fastfetch logos]' \\
        '--logo[Alias for --fastfetch]' \\
        '--crop[Crop image: center, square, or x,y,w,h]:crop specification: ' \\
        '--zoom[Digital zoom factor centered on subject]:zoom factor: ' \\
        '(-E --engine)'{{-E,--engine}}'[Select rendering engine explicitly]:engine:(mary trumble luris spectra color mono bw manga sketch)' \\
        '(-c --color --no-color)'{{-c,--color}}'[Force TrueColor output]' \\
        '(-c --color --no-color)'--no-color'[Disable color and use monochrome engine]' \\
        '(-S --sextants)'{{-S,--sextants}}'[Use Unicode 2x3 sextant blocks (Mary default)]' \\
        '(-B --braille)'{{-B,--braille}}'[Use Unicode 2x4 braille characters (8 subpixels)]' \\
        '(-Q --quadrants)'{{-Q,--quadrants}}'[Use Unicode 2x2 quadrant blocks (4 subpixels)]' \\
        '--blocks[Use optimized half-block characters (▀/▄)]' \\
        '(-m --manga)'{{-m,--manga}}'[Manga Screentone 2.0 (Bayer 8x8 + DoG lines)]' \\
        '(-s --sketch)'{{-s,--sketch}}'[Clean pen-and-ink line sketch mode]' \\
        '--matrix[Render in Katakana and binary green Matrix code]' \\
        '--matrix-rain[Falling Katakana digital rain animation]' \\
        '--theme[Synchronize colors with terminal palette]:palette:(catppuccin dracula nord gruvbox synthwave vaporwave gameboy solarized)' \\
        '--palette[Alias for --theme]:palette:(catppuccin dracula nord gruvbox synthwave vaporwave gameboy solarized)' \\
        '--crt[Simulate retro CRT scanlines and phosphor monitor]:mode:(color green amber scanlines)' \\
        '--scanlines[Alias for --crt]:mode:(color green amber scanlines)' \\
        '(--boost --vibrant)'{{--boost,--vibrant}}'[Apply vibrant arcade saturation, contrast and Retinex]' \\
        '(-i --invert)'{{-i,--invert}}'[Invert character lightness]' \\
        '*--swap[Dynamically swap one color for another in 3D RGB space]:color: ' \\
        '(-d --dither)'{{-d,--dither}}'[Select dithering algorithm]:algorithm:(atkinson floyd bayer none)' \\
        '--font-ratio[Font aspect ratio calibration]:ratio: ' \\
        '(-o -O --output --save)'{{-o,-O,--output,--save}}'[Export graphic image, ANS, or TXT]:output file:_files' \\
        '--loop[Animation mode: smooth terminal loop or animated GIF export]' \\
        '(-r --remove-bg)'{{-r,--remove-bg}}'[Remove background without quality loss (standalone saves HD PNG)]' \\
        '--transparent[Luris Mono transparent sticker]' \\
        '(-C --copy)'{{-C,--copy}}'[Copy rendered ANSI art to system clipboard]' \\
        '--copy-plain[Copy plain ASCII text without color codes to clipboard]' \\
        '(--instant --reveal)'{{--instant,--no-reveal}}'[Display output immediately]' \\
        '(--instant --reveal)'--reveal'[Progressive scan animation]' \\
        '--paste[Render clipboard image]' \\
        '(-I --interactive --tui)'{{-I,--interactive,--tui}}'[Interactive live parameter tuning terminal UI]' \\
        '--slideshow[Interactive terminal slideshow gallery]' \\
        '--delay[Slideshow delay between images in seconds]:delay: ' \\
        '--diff[Side-by-side terminal image comparison]:comparison image:_files' \\
        '--lang[Set language]:language:(en es pt fr ru ja de ko)' \\
        '(-W --webcam)'{{-W,--webcam}}'[Webcam streaming]:camera index: ' \\
        '(-H --history)'{{-H,--history}}'[Show execution history]:count: ' \\
        '(-R --replay)'{{-R,--replay}}'[Re-run command from history]:command index: ' \\
        '--clear-history[Wipe command history]' \\
        '--install-desktop[Register file manager context menu]' \\
        '--completions[Generate shell completions]:shell:(bash zsh fish)' \\
        '*:image file:_files'
}}
_lumart "$@"
"""
    return ""

# ==============================================================================
# VALIDACIÓN SEMÁNTICA DE FLAGS CLI
# ==============================================================================
def validate_cli_arguments(args, parser):
    """
    Valida la compatibilidad semántica de flags de la CLI.
    Si se detectan combinaciones incompatibles, imprime un mensaje pedagógico
    y sale con código de error 2.
    """
    # 1. --fit vs --width
    if getattr(args, "fit", False) and args.width is not None:
        print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_fit_width')}", file=sys.stderr)
        sys.exit(2)

    # 2. --instant vs --reveal
    if getattr(args, "instant", False) and getattr(args, "reveal", False):
        print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_instant_reveal')}", file=sys.stderr)
        sys.exit(2)

    # 3. Múltiples texturas (-S, -B, -Q, --blocks)
    textures = [
        opt for cond, opt in [
            (getattr(args, "sextants", False), "-S/--sextants"),
            (getattr(args, "braille", False), "-B/--braille"),
            (getattr(args, "quadrants", False), "-Q/--quadrants"),
            (getattr(args, "blocks", False), "--blocks"),
        ] if cond
    ]
    if len(textures) > 1:
        print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_textures')}", file=sys.stderr)
        sys.exit(2)

    # 4. Múltiples estilos (-m vs -s)
    if getattr(args, "manga", False) and getattr(args, "sketch", False):
        print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_styles')}", file=sys.stderr)
        sys.exit(2)

    # 5. Múltiples fuentes de entrada (image_path vs --paste vs -W)
    if not getattr(args, "diff", None) and not getattr(args, "slideshow", False):
        sources = 0
        if args.image_path and args.image_path != "-":
            sources += 1
        if getattr(args, "paste", False):
            sources += 1
        if getattr(args, "webcam", None) is not None:
            sources += 1
        if sources > 1:
            print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_inputs')}", file=sys.stderr)
            sys.exit(2)

    # 6. --loop vs exportación a imagen estática (-o .png / .jpg / etc.)
    if getattr(args, "loop", False) and getattr(args, "output", None):
        ext = os.path.splitext(args.output)[1].lower()
        if ext in (".png", ".jpg", ".jpeg", ".bmp", ".webp"):
            print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_loop_static')}", file=sys.stderr)
            sys.exit(2)

    # 7. --transparent o -r vs exportación a JPEG (-o .jpg / .jpeg)
    if (getattr(args, "transparent", False) or getattr(args, "remove_bg", False)) and getattr(args, "output", None):
        ext = os.path.splitext(args.output)[1].lower()
        if ext in (".jpg", ".jpeg"):
            print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_transparent_jpg')}", file=sys.stderr)
            sys.exit(2)

    # 8. --zoom <= 0
    if getattr(args, "zoom", 1.0) is not None and getattr(args, "zoom", 1.0) <= 0:
        print(f"\033[1;31m[Lumart Error]\033[0m El factor de zoom debe ser mayor a 0.", file=sys.stderr)
        sys.exit(2)



# ==============================================================================
# UTILIDADES DE RECORTE Y PROCESAMIENTO DE ANIMACIONES
# ==============================================================================
def crop_empty_borders(pil_img, tolerance=10):
    """
    Recorta bordes vacíos o transparentes/monocromáticos de la imagen.
    Ideal para Fastfetch / Neofetch o avatares limpios sin márgenes sobrantes.
    """
    try:
        from PIL import ImageChops
        img_rgba = pil_img.convert("RGBA")
        alpha = img_rgba.split()[3]
        min_a, max_a = alpha.getextrema()
        if min_a < 250:
            alpha_mask = alpha.point(lambda p: 255 if p > 15 else 0)
            alpha_bbox = alpha_mask.getbbox()
            if alpha_bbox:
                return pil_img.crop(alpha_bbox)

        bg = Image.new(img_rgba.mode, img_rgba.size, img_rgba.getpixel((0, 0)))
        diff = ImageChops.difference(img_rgba, bg)
        diff = ImageChops.add(diff, diff, 2.0, -tolerance)
        bbox = diff.getbbox()
        if bbox:
            return pil_img.crop(bbox)
    except Exception:
        pass
    return pil_img


def render_frame_to_art(frame_img, args, engine, mode, is_raw_colors, invert_mode, font_ratio):
    """
    Renderiza un único frame (PIL.Image) a arte ANSI según el motor y modo configurados.
    """
    ascii_art = ""
    if getattr(args, "swap", None):
        frame_img = apply_color_swap(frame_img, args.swap)

    # 1. MOTOR LURIS
    if engine == "luris":
        temp_path = None
        try:
            cur_img = frame_img
            if getattr(args, "transparent", False):
                cur_img = remove_image_background(cur_img)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_path = tmp.name
                cur_img.save(temp_path)

            mono_mode = "braille"
            if getattr(args, "sketch", False):
                mono_mode = "sketch"
            elif getattr(args, "manga", False):
                mono_mode = "manga"
            elif getattr(args, "blocks", False) or getattr(args, "quadrants", False):
                mono_mode = "blocks"

            dither_algo = "none"
            if getattr(args, "dither", None):
                dither_algo = "atkinson" if args.dither is True else str(args.dither).lower()

            native_art = try_render_native_monochrome(temp_path, args.width, mono_mode, dither_algo, invert_mode)
            if native_art is not None:
                ascii_art = native_art
            else:
                if mono_mode == "sketch":
                    ascii_art = render_python_sketch(cur_img, args.width, invert_mode)
                elif mono_mode == "manga":
                    ascii_art = render_python_manga(cur_img, args.width, invert_mode)
                elif mono_mode == "blocks":
                    ascii_art = render_python_bw_quadrants(cur_img, args.width, dither_algo, invert_mode)
                else:
                    resized = resize_image(cur_img, args.width, getattr(args, "blocks", False), getattr(args, "braille", False))
                    if dither_algo in ("atkinson", "bayer", "floyd") or getattr(args, "dither", None):
                        resized = apply_bayer_dither(resized)
                    if getattr(args, "braille", False):
                        ascii_art = convert_image_to_braille(resized, getattr(args, "color", False), invert_mode)
                    else:
                        ascii_art = convert_image_to_blocks(resized)
        finally:
            if temp_path and os.path.exists(temp_path):
                try: os.unlink(temp_path)
                except Exception: pass

    # 2. MOTOR MARY
    elif engine == "mary":
        temp_path = None
        mary_img = frame_img
        try:
            if getattr(args, "transparent", False):
                mary_img = remove_image_background(mary_img)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_path = tmp.name
                mary_img.save(temp_path)

            native_mary = try_render_native_mary(
                temp_path,
                args.width,
                mode=mode,
                raw_colors=is_raw_colors,
                invert=invert_mode,
                font_ratio=font_ratio
            )
            if native_mary is not None:
                ascii_art = native_mary
            elif mary is not None:
                ascii_art = mary.render_mary(
                    mary_img,
                    args.width,
                    mode=mode,
                    raw_colors=is_raw_colors,
                    invert=invert_mode,
                    font_ratio=font_ratio
                )
            else:
                engine = "trumble"
        finally:
            if temp_path and os.path.exists(temp_path):
                try: os.unlink(temp_path)
                except Exception: pass

    # 3. MOTOR TRUMBLE
    if engine == "trumble":
        t_img = frame_img
        if getattr(args, "transparent", False):
            t_img = remove_image_background(t_img)

        is_blocks_mode = not getattr(args, "braille", False)
        if getattr(args, "boost", False):
            t_img, was_resized = apply_trumble_cel_shading(t_img, target_width=args.width, is_blocks=is_blocks_mode, is_braille=getattr(args, "braille", False))
            if not was_resized:
                t_img = resize_image(t_img, args.width, is_blocks=is_blocks_mode, is_braille=getattr(args, "braille", False))
        else:
            t_img = resize_image(t_img, args.width, is_blocks=is_blocks_mode, is_braille=getattr(args, "braille", False))

        if getattr(args, "dither", None):
            t_img = apply_bayer_dither(t_img)

        if getattr(args, "braille", False):
            ascii_art = convert_image_to_braille(t_img, getattr(args, "color", True), invert_mode)
        else:
            ascii_art = convert_image_to_blocks(t_img)

    return ascii_art


def play_or_save_animation(image_path, args, engine, mode, is_raw_colors, invert_mode, font_ratio, out_target=None):
    """
    Maneja la reproducción en bucle (--loop) en terminal o la exportación a GIF animado (-o anim.gif / --save anim.gif).
    """
    try:
        from PIL import ImageSequence
        base_img = Image.open(image_path)
    except Exception as e:
        print(_("error_open", e))
        sys.exit(1)

    is_animated = getattr(base_img, "is_animated", False)
    n_frames = getattr(base_img, "n_frames", 1)
    if not is_animated or n_frames <= 1:
        frame_img = base_img.convert("RGBA" if getattr(args, "transparent", False) else "RGB")
        if getattr(args, "fastfetch", False) or getattr(args, "logo", False):
            frame_img = crop_empty_borders(frame_img)
        art = render_frame_to_art(frame_img, args, engine, mode, is_raw_colors, invert_mode, font_ratio)
        if out_target:
            export_ansi_to_image(art, out_target, transparent=getattr(args, "transparent", False))
            print(_("export_success", out_target))
        else:
            print(art)
        return

    # Si se especificó destino de guardado (-o anim.gif o --save anim.gif)
    if out_target:
        ext = os.path.splitext(out_target)[1].lower()
        if ext != ".gif":
            print(f"\033[1;31m[Lumart Error]\033[0m {_('err_conflict_loop_static')}", file=sys.stderr)
            sys.exit(2)

        rendered_images = []
        durations = []
        for i, frame in enumerate(ImageSequence.Iterator(base_img)):
            dur = frame.info.get("duration", 100) or 100
            durations.append(dur)
            cur = frame.copy().convert("RGBA" if getattr(args, "transparent", False) else "RGB")
            if getattr(args, "fastfetch", False) or getattr(args, "logo", False):
                cur = crop_empty_borders(cur)
            print(_("render_anim_export", i + 1, n_frames), end="\r", flush=True)
            art = render_frame_to_art(cur, args, engine, mode, is_raw_colors, invert_mode, font_ratio)
            frame_render_img = export_ansi_to_image(art, out_path=None, transparent=getattr(args, "transparent", False))
            rendered_images.append(frame_render_img)

        print()
        if rendered_images:
            out_dir = os.path.dirname(os.path.abspath(out_target))
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)
            rendered_images[0].save(
                out_target,
                save_all=True,
                append_images=rendered_images[1:],
                duration=durations,
                loop=0,
                optimize=True
            )
            print(_("export_success", out_target))
        return

    # Reproducción en bucle en tiempo real en la terminal
    frames_data = []
    for frame in ImageSequence.Iterator(base_img):
        dur = (frame.info.get("duration", 100) or 100) / 1000.0
        dur = max(0.02, min(dur, 2.0))
        cur = frame.copy().convert("RGBA" if getattr(args, "transparent", False) else "RGB")
        if getattr(args, "fastfetch", False) or getattr(args, "logo", False):
            cur = crop_empty_borders(cur)
        frames_data.append((cur, dur))

    # Pre-renderizar todos los frames para fluidez a 60fps sin tirones
    cached_arts = []
    for cur, dur in frames_data:
        cached_arts.append((render_frame_to_art(cur, args, engine, mode, is_raw_colors, invert_mode, font_ratio), dur))

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    try:
        while True:
            for art, dur in cached_arts:
                sys.stdout.write(f"\033[H{art}\n")
                sys.stdout.flush()
                time.sleep(dur)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\033[0m\n")
        sys.stdout.flush()

def main():
    import json
    try:
        import signal
        if hasattr(signal, "SIGPIPE"):
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    
    # Inicialización de secuencias de escape ANSI en consolas Windows (cmd / powershell)
    if os.name == "nt":
        os.system("")
    
    # Preprocesamiento de --lang para aplicar la configuración de idioma antes de argparse
    lang_override = None
    for i, a in enumerate(sys.argv):
        if a == "--lang" and i + 1 < len(sys.argv):
            lang_override = sys.argv[i + 1]
            break
        elif a.startswith("--lang="):
            lang_override = a.split("=", 1)[1]
            break

    # Persistir configuración de usuario en ~/.config/luma/config.json
    config_dir = os.path.expanduser("~/.config/luma")
    config_file = os.path.join(config_dir, "config.json")
    
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

    # Si la invocación es solo para cambiar el idioma (ej: lumart --lang es), guardar y salir
    is_lang_only = (len(sys.argv) == 3 and "--lang" in sys.argv) or \
                   (len(sys.argv) == 2 and any(a.startswith("--lang=") for a in sys.argv))
    if is_lang_only:
        if lang_override in TRANSLATIONS:
            os.makedirs(config_dir, exist_ok=True)
            with open(config_file, "w") as f:
                json.dump({"lang": lang_override}, f)
            print(_("lang_success", lang_override))
            sys.exit(0)
        else:
            set_language("en")
            print(_("lang_error", lang_override))
            sys.exit(1)

    banner = get_lumart_banner()
    
    # Intercepción inmediata de -v / --version para mostrar el diagnóstico e info completa
    if "-v" in sys.argv or "--version" in sys.argv:
        show_version_info()
        sys.exit(0)

    # Intercepción inmediata de --completions para scripts de shell
    for i, a in enumerate(sys.argv):
        if a == "--completions" and i + 1 < len(sys.argv):
            out = generate_shell_completions(sys.argv[i + 1])
            print(out, end="" if out.endswith("\n") else "\n")
            sys.exit(0)
        elif a.startswith("--completions="):
            out = generate_shell_completions(a.split("=", 1)[1])
            print(out, end="" if out.endswith("\n") else "\n")
            sys.exit(0)

    # Intercepción inmediata de subcomando 'diff' (ej: lumart diff img1.png img2.png [-w 100])
    if len(sys.argv) >= 2 and sys.argv[1] == "diff":
        diff_parser = argparse.ArgumentParser(prog="lumart diff", description=_("help_diff"))
        diff_parser.add_argument("image_a", help="First image to compare")
        diff_parser.add_argument("image_b", help="Second image to compare")
        diff_parser.add_argument("-w", "--width", type=int, default=None, help=_("help_width"))
        diff_args = diff_parser.parse_args(sys.argv[2:])
        success = render_image_diff(diff_args.image_a, diff_args.image_b, width=diff_args.width)
        record_command_to_history()
        sys.exit(0 if success else 1)

    # Sin argumentos: mostrar banner informativo y ayuda básica de uso
    if len(sys.argv) == 1 and sys.stdin.isatty():
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
    parser.add_argument("-uu", "--upgrade", nargs="?", const="latest", default=None, help=_("help_upgrade"))
    parser.add_argument("-dg", "--downgrade", "--rollback", nargs="?", const="prev", default=None, help=_("help_downgrade"))

    parser.add_argument("image_path", nargs="?", default=None, help=_("help_image_path"))
    parser.add_argument("-w", "--width", type=int, default=None, help=_("help_width"))
    parser.add_argument("-F", "--fit", action="store_true", help=_("help_fit"))
    parser.add_argument("-E", "--engine", choices=["mary", "trumble", "luris", "spectra", "color", "mono", "bw", "manga", "sketch"], default=None, help=_("help_engine"))
    parser.add_argument("-c", "--color", action="store_true", dest="color", default=True, help=_("help_color"))
    parser.add_argument("--no-color", action="store_false", dest="color", help=_("help_no_color"))
    parser.add_argument("-S", "--sextants", action="store_true", help=_("help_sextants"))
    parser.add_argument("-B", "--braille", action="store_true", help=_("help_braille"))
    parser.add_argument("-Q", "--quadrants", action="store_true", help=_("help_quadrants"))
    parser.add_argument("--blocks", action="store_true", help=_("help_blocks"))
    parser.add_argument("-m", "--manga", action="store_true", help=_("help_manga"))
    parser.add_argument("-s", "--sketch", action="store_true", help=_("help_sketch"))
    parser.add_argument("--boost", "--vibrant", action="store_true", default=False, help=_("help_boost"))
    parser.add_argument("-i", "--invert", action="store_true", help=_("help_invert"))
    parser.add_argument("--swap", nargs="+", help=_("help_swap"))
    parser.add_argument("-d", "--dither", nargs="?", const="atkinson", default=None, help=_("help_dither"))
    parser.add_argument("--font-ratio", type=float, default=0.5, help=_("help_font_ratio"))
    parser.add_argument("-o", "-O", "--output", "--save", dest="output", help=_("help_output"))
    parser.add_argument("--loop", action="store_true", help=_("help_loop"))
    parser.add_argument("--fastfetch", "--logo", action="store_true", help=_("help_fastfetch"))
    parser.add_argument("-r", "--remove-bg", action="store_true", help=_("help_remove_bg"))
    parser.add_argument("--transparent", action="store_true", help=_("help_transparent"))
    parser.add_argument("--instant", "--no-reveal", action="store_true", help=_("help_instant"))
    parser.add_argument("--reveal", action="store_true", help=_("help_reveal"))
    parser.add_argument("--paste", action="store_true", help=_("help_paste"))
    parser.add_argument("--lang", help=_("help_lang"))

    # Nuevas funcionalidades avanzadas v2.5.0
    parser.add_argument("--theme", "--palette", choices=list(THEME_PALETTES.keys()), default=None, help=_("help_theme"))
    parser.add_argument("--crt", "--scanlines", choices=["green", "amber", "color", "scanlines"], nargs="?", const="color", default=None, help=_("help_crt"))
    parser.add_argument("--matrix", action="store_true", help=_("help_matrix"))
    parser.add_argument("--matrix-rain", action="store_true", help=_("help_matrix_rain"))
    parser.add_argument("-C", "--copy", action="store_true", help=_("help_copy"))
    parser.add_argument("--copy-plain", action="store_true", help=_("help_copy_plain"))
    parser.add_argument("--crop", default=None, help=_("help_crop"))
    parser.add_argument("--zoom", type=float, default=1.0, help=_("help_zoom"))
    parser.add_argument("--slideshow", action="store_true", help=_("help_slideshow"))
    parser.add_argument("--delay", type=float, default=3.0, help=_("help_delay"))
    parser.add_argument("-I", "--interactive", "--tui", action="store_true", help=_("help_interactive"))
    parser.add_argument("--diff", default=None, help=_("help_diff"))
    parser.add_argument("extra_images", nargs="*", default=[], help=argparse.SUPPRESS)

    # Utilidades del sistema
    parser.add_argument("-W", "--webcam", nargs="?", const=0, default=None, type=int, help=_("help_webcam"))
    parser.add_argument("-H", "--history", nargs="?", const="all", default=None, help=_("help_history"))
    parser.add_argument("-R", "--replay", "--last", nargs="?", const="1", default=None, help=_("help_replay"))
    parser.add_argument("--clear-history", action="store_true", help=_("help_clear_history"))
    parser.add_argument("--install-desktop", action="store_true", help=_("help_install_desktop"))
    parser.add_argument("--completions", choices=["bash", "zsh", "fish"], default=None, help=_("help_completions"))
    
    args = parser.parse_args()
    validate_cli_arguments(args, parser)

    # Si se solicitó versión
    if args.version:
        show_version_info()
        sys.exit(0)

    # Si se solicitó generación de autocompletado
    if getattr(args, "completions", None):
        out = generate_shell_completions(args.completions)
        print(out, end="" if out.endswith("\n") else "\n")
        sys.exit(0)

    # Limpiar historial
    if args.clear_history:
        clear_command_history()
        sys.exit(0)

    # Mostrar historial
    if args.history is not None:
        limit = None
        if args.history != "all":
            try:
                limit = int(args.history)
            except ValueError:
                limit = None
        display_command_history(limit=limit)
        sys.exit(0)

    # Re-ejecutar comando del historial
    if args.replay is not None:
        try:
            target_idx = int(args.replay)
        except ValueError:
            target_idx = 1
        replay_command(target_idx=target_idx)
        sys.exit(0)

    # Instalar integración de escritorio y gestores de archivos
    if args.install_desktop:
        install_desktop_integration()
        sys.exit(0)

    # Motor Spectra exclusivo para webcam
    if args.webcam is not None:
        record_command_to_history()
        success = run_spectra_webcam(cam_index=args.webcam, target_width=args.width, font_ratio=getattr(args, "font_ratio", 0.5) or 0.5)
        sys.exit(0 if success else 1)

    # Comprobar actualizaciones sin instalar (-u / --update / --check-update)
    if args.update:
        print(banner)
        check_for_updates()
        sys.exit(0)

    # Descargar e instalar la actualización más reciente (-uu / --upgrade)
    if args.upgrade is not None:
        print(banner)
        target = None if args.upgrade == "latest" else args.upgrade
        success = perform_upgrade(target)
        sys.exit(0 if success else 1)

    # Volver a la versión anterior o especificada (-dg / --downgrade / --rollback)
    if args.downgrade is not None:
        print(banner)
        target = None if args.downgrade == "prev" else args.downgrade
        success = perform_downgrade(target)
        sys.exit(0 if success else 1)

    # Comparación visual lado a lado con telemetría de diferencias (--diff)
    if getattr(args, "diff", None):
        if not args.image_path:
            print(f"\033[1;31m[Lumart Error]\033[0m Debes proporcionar dos imágenes para comparar.", file=sys.stderr)
            sys.exit(1)
        success = render_image_diff(args.image_path, args.diff, width=args.width)
        record_command_to_history()
        sys.exit(0 if success else 1)

    # Galería interactiva en terminal (--slideshow)
    if getattr(args, "slideshow", False):
        file_candidates = []
        if args.image_path:
            file_candidates.append(args.image_path)
        if getattr(args, "extra_images", None):
            file_candidates.extend(args.extra_images)
        if not file_candidates:
            file_candidates = ["."]
        success = run_slideshow(
            file_candidates,
            delay=getattr(args, "delay", 3.0) or 3.0,
            width=args.width,
            engine=getattr(args, "engine", None),
            theme=getattr(args, "theme", None),
            crt=getattr(args, "crt", None)
        )
        record_command_to_history()
        sys.exit(0 if success else 1)

    # Modo interactivo en vivo (-I / --interactive / --tui)
    if getattr(args, "interactive", False):
        if not args.image_path:
            print(banner)
            print(_("usage"))
            sys.exit(1)
        success = run_interactive_tui(args.image_path, initial_width=args.width or 80)
        record_command_to_history()
        sys.exit(0 if success else 1)

    if not args.image_path and not args.paste and sys.stdin.isatty():
        print(banner)
        print(_("usage"))
        sys.exit(1)

    # Comprobación no invasiva de actualización en segundo plano (aviso a stderr para no contaminar salida)
    has_update, update_ver = check_cached_update()
    if has_update:
        print(f"\033[1;33m{_('update_notice', update_ver)}\033[0m\n", file=sys.stderr)

    # Comprobar si se especificó algún flag de modelo / motor de renderizado
    has_model_flag = any([
        args.engine is not None,
        getattr(args, "manga", False),
        getattr(args, "sketch", False),
        getattr(args, "sextants", False),
        getattr(args, "braille", False),
        getattr(args, "quadrants", False),
        getattr(args, "blocks", False),
        getattr(args, "matrix", False),
        getattr(args, "matrix_rain", False),
        getattr(args, "theme", None) is not None,
        getattr(args, "crt", None) is not None,
        getattr(args, "loop", False),
        getattr(args, "dither", None) is not None,
        getattr(args, "swap", None) is not None,
    ])

    # Manejo de -r / --remove-bg
    if getattr(args, "remove_bg", False):
        if not has_model_flag:
            # Modo Autónomo: Quita fondo al 100% de calidad original y exporta PNG transparente sin aplicar modelos
            try:
                raw_img = load_image_from_source(args.image_path, paste=args.paste)
            except Exception as e:
                print(_("error_open", e))
                sys.exit(1)

            if getattr(args, "crop", None) or (getattr(args, "zoom", 1.0) and args.zoom != 1.0):
                raw_img = apply_crop_and_zoom(raw_img, crop_spec=args.crop, zoom=args.zoom)

            nobg_img = remove_image_background(raw_img)

            if args.output:
                out_target = args.output
            elif args.image_path and args.image_path != "-":
                base_name, _ext = os.path.splitext(args.image_path)
                out_target = f"{base_name}_nobg.png"
            else:
                out_target = "output_nobg.png"

            try:
                nobg_img.save(out_target, format="PNG")
                print(f"\033[1;32m{_('remove_bg_success', out_target, nobg_img.width, nobg_img.height)}\033[0m")
                record_command_to_history()
                sys.exit(0)
            except Exception as e:
                print(f"\033[1;31mError al guardar imagen sin fondo: {e}\033[0m", file=sys.stderr)
                sys.exit(1)
        else:
            # Con flag de modelo: activar transparencia y continuar con el motor elegido
            args.transparent = True

    # Selección y resolución de motor:
    req_engine = getattr(args, "engine", None)
    if req_engine:
        req_engine = req_engine.lower()
        if req_engine in ("color", "mary"):
            engine = "mary"
            args.color = True
        elif req_engine == "trumble":
            engine = "trumble"
            args.color = getattr(args, "color", True)
        elif req_engine in ("mono", "bw", "luris"):
            engine = "luris"
            args.color = False
        elif req_engine in ("manga", "sketch"):
            engine = "luris"
            args.color = False
            if req_engine == "manga":
                args.manga = True
            elif req_engine == "sketch":
                args.sketch = True
        elif req_engine == "spectra":
            engine = "spectra"
        else:
            engine = req_engine
    else:
        # Zero-Flag: Autodetección inteligente (Mary Oklab HD por defecto)
        is_mono = bool(
            not getattr(args, "color", True) or
            getattr(args, "manga", False) or 
            getattr(args, "sketch", False) or 
            getattr(args, "dither", None) is not None or 
            "NO_COLOR" in os.environ
        )
        if is_mono:
            engine = "luris"
            args.color = False
            if getattr(args, "manga", False) or getattr(args, "sketch", False):
                args.braille = True
        else:
            engine = "mary"
            args.color = True

    # Calibración de proporción de caracteres terminal
    font_ratio = getattr(args, "font_ratio", 0.5) or 0.5

    # Si se seleccionó motor spectra explícitamente vía -E spectra:
    if engine == "spectra":
        record_command_to_history()
        cam_idx = args.webcam if args.webcam is not None else 0
        success = run_spectra_webcam(cam_index=cam_idx, target_width=args.width, font_ratio=font_ratio)
        sys.exit(0 if success else 1)

    try:
        image = load_image_from_source(args.image_path, paste=args.paste)
    except Exception as e:
        # Error al abrir la imagen en la ruta especificada
        print(_("error_open", e))
        sys.exit(1)

    # Aplicar recorte y zoom digital
    if getattr(args, "crop", None) or (getattr(args, "zoom", 1.0) and args.zoom != 1.0):
        image = apply_crop_and_zoom(image, crop_spec=args.crop, zoom=args.zoom)

    # Recorte automático de bordes vacíos/transparentes para fastfetch o logos compactos
    if getattr(args, "fastfetch", False) or getattr(args, "logo", False):
        image = crop_empty_borders(image)

    # Aplicar paleta de color temática si fue solicitada
    if getattr(args, "theme", None):
        image = apply_theme_palette(image, args.theme)


    # Autodetección del ancho de la terminal: si se especificó -F/--fit o si no se especificó -w
    if getattr(args, "fit", False):
        try:
            import shutil
            term = shutil.get_terminal_size((120, 24))
            max_cols = max(20, term.columns)
            max_lines = max(10, term.lines - 2)
            aspect = image.height / max(1, image.width)
            width_from_cols = max_cols
            width_from_lines = int(max_lines / max(0.01, (aspect * font_ratio)))
            args.width = max(10, min(width_from_cols, width_from_lines))
        except Exception:
            args.width = 80
    elif args.width is None:
        if args.output and os.path.splitext(args.output)[1].lower() in (".png", ".jpg", ".jpeg"):
            # Para exportación a imagen gráfica / stickers, usar resolución Ultra-HD de estudio (160 cols)
            args.width = 160
        else:
            try:
                import shutil
                term_cols = shutil.get_terminal_size((120, 24)).columns
                # Usar el ancho real de la terminal sin límite artificial.
                # Mínimo de seguridad: 20 columnas para evitar renders rotos.
                args.width = max(20, term_cols)
            except Exception:
                args.width = 120
    elif args.width < 5:
        args.width = 5

    # 3. Autodetección de terminal clara (Light mode) para inversión automática de caracteres
    invert_mode = args.invert or is_light_terminal()

    if args.swap:
        if len(args.swap) % 2 != 0:
            print(_("error_swap"))
            sys.exit(1)
        image = apply_color_swap(image, args.swap)

    # Autodetección de fondo claro/blanco para Luris Mono:
    # Si la imagen tiene fondo predominantemente blanco/claro y el usuario no forzó -i manualmente,
    # invertimos automáticamente para preservar el papel blanco limpio estilo manga.
    if engine == "luris" and not args.invert and "-i" not in sys.argv and "--invert" not in sys.argv:
        try:
            _detect_img = image.convert("RGBA")
            w, h = _detect_img.size
            # Muestrear bordes y esquinas de la imagen para detectar fondo claro
            border_pixels = []
            for x in range(0, w, max(1, w // 20)):
                for y_offset in [0, 1, h - 2, h - 1]:
                    if 0 <= y_offset < h:
                        p = _detect_img.getpixel((x, y_offset))
                        if p[3] > 200:  # Solo píxeles opacos
                            border_pixels.append(p[:3])
            for y in range(0, h, max(1, h // 20)):
                for x_offset in [0, 1, w - 2, w - 1]:
                    if 0 <= x_offset < w:
                        p = _detect_img.getpixel((x_offset, y))
                        if p[3] > 200:
                            border_pixels.append(p[:3])
            if border_pixels:
                avg_lum = sum((0.299 * r + 0.587 * g + 0.114 * b) for r, g, b in border_pixels) / len(border_pixels)
                light_count = sum(1 for r, g, b in border_pixels if (0.299 * r + 0.587 * g + 0.114 * b) > 140)
                if light_count / len(border_pixels) > 0.50 and avg_lum > 150:
                    invert_mode = True
        except Exception:
            pass

    # Determinar modo de representación (sextants, braille, quadrants, blocks)
    if getattr(args, "braille", False):
        mode = "braille"
    elif getattr(args, "quadrants", False):
        mode = "quadrants"
    elif getattr(args, "blocks", False):
        mode = "blocks"
    elif getattr(args, "sextants", False):
        mode = "sextants"
    else:
        mode = "sextants"

    is_raw_colors = not getattr(args, "boost", False)

    # Manejo de animación interactiva o exportación de GIF animado con --loop
    if getattr(args, "loop", False):
        play_or_save_animation(
            args.image_path,
            args,
            engine,
            mode,
            is_raw_colors,
            invert_mode,
            font_ratio,
            out_target=args.output
        )
        record_command_to_history()
        sys.exit(0)

    ascii_art = ""

    # -------------------------------------------------------------
    # 0. MODO MATRIX / DIGITAL RAIN
    # -------------------------------------------------------------
    if getattr(args, "matrix", False) or getattr(args, "matrix_rain", False):
        if getattr(args, "transparent", False):
            image = remove_image_background(image)
        if getattr(args, "matrix_rain", False):
            render_matrix_art(image, width=args.width, font_ratio=font_ratio, animated=True)
            record_command_to_history()
            sys.exit(0)
        else:
            ascii_art = render_matrix_art(image, width=args.width, font_ratio=font_ratio, animated=False)

    # -------------------------------------------------------------
    # 1. MOTOR LURIS: Blanco y Negro (Nativo C++ con fallback Python)
    # -------------------------------------------------------------
    elif engine == "luris":
        # MOTOR EN BLANCO Y NEGRO: Remover fondo ANTES DE EMPEZARLO
        temp_luris_path = None
        luris_input_path = args.image_path
        if getattr(args, "transparent", False):
            image = remove_image_background(image)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_luris_path = tmp.name
                image.save(temp_luris_path)
            luris_input_path = temp_luris_path
        elif not args.image_path or not os.path.exists(args.image_path):
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_luris_path = tmp.name
                image.save(temp_luris_path)
            luris_input_path = temp_luris_path

        try:
            if getattr(args, "sketch", False):
                mono_mode = "sketch"
            elif getattr(args, "manga", False):
                mono_mode = "manga"
            elif getattr(args, "braille", False):
                mono_mode = "braille"
            elif getattr(args, "blocks", False) or getattr(args, "quadrants", False):
                mono_mode = "blocks"
            else:
                mono_mode = "braille"

            dither_algo = "none"
            if args.dither:
                dither_algo = "atkinson" if args.dither is True else str(args.dither).lower()

            native_art = try_render_native_monochrome(luris_input_path, args.width, mono_mode, dither_algo, invert_mode)
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
                    else:
                        ascii_art = convert_image_to_blocks(image)
        finally:
            if temp_luris_path and os.path.exists(temp_luris_path):
                try: os.unlink(temp_luris_path)
                except Exception: pass

    # -------------------------------------------------------------
    # 2. MOTOR MARY: Apex Perceptual Color Engine (Oklab, Fast Guided Filter, Sextants/Braille/Quadrants)
    # -------------------------------------------------------------
    elif engine == "mary":
        if getattr(args, "braille", False):
            mode = "braille"
        elif getattr(args, "quadrants", False):
            mode = "quadrants"
        elif getattr(args, "blocks", False):
            mode = "blocks"
        elif getattr(args, "sextants", False):
            mode = "sextants"
        else:
            # Por defecto en Mary Apex 3.5: Sextantes HD 2x3 (6 subpíxeles por celda, máxima resolución continua)
            mode = "sextants"

        # MOTOR A COLOR: Remover fondo ANTES DE FINALIZAR EL PROCESO
        temp_mary_path = None
        mary_image = image
        mary_input_path = args.image_path
        if getattr(args, "transparent", False):
            mary_image = remove_image_background(image)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_mary_path = tmp.name
                mary_image.save(temp_mary_path)
            mary_input_path = temp_mary_path
        elif not args.image_path or not os.path.exists(args.image_path):
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_mary_path = tmp.name
                mary_image.save(temp_mary_path)
            mary_input_path = temp_mary_path

        try:
            # Colores naturales fieles por defecto. Si se especificó --boost, se desactiva raw_colors.
            is_raw_colors = not args.boost

            # 1. Intentar aceleración nativa C++ (luma-mary / libmary.so)
            native_mary = try_render_native_mary(
                mary_input_path,
                args.width,
                mode=mode,
                raw_colors=is_raw_colors,
                invert=invert_mode,
                font_ratio=font_ratio
            )
            if native_mary is not None:
                ascii_art = native_mary
            elif mary is not None:
                # 2. Fallback al motor Mary en Python puro
                ascii_art = mary.render_mary(
                    mary_image,
                    args.width,
                    mode=mode,
                    raw_colors=is_raw_colors,
                    invert=invert_mode,
                    font_ratio=font_ratio
                )
            else:
                # 3. Fallback seguro al motor clásico Trumble
                engine = "trumble"
        finally:
            if temp_mary_path and os.path.exists(temp_mary_path):
                try: os.unlink(temp_mary_path)
                except Exception: pass

    # -------------------------------------------------------------
    # 3. MOTOR TRUMBLE ORELX 2.2: Retro-Arcade & Anime Cel-Shading
    # -------------------------------------------------------------
    if not ascii_art and engine == "trumble":
        # MOTOR A COLOR: Remover fondo ANTES DE FINALIZAR EL PROCESO
        if getattr(args, "transparent", False):
            image = remove_image_background(image)

        # Trumble por defecto renderiza en Bloques HD TrueColor (medios bloques ▀)
        is_blocks_mode = not getattr(args, "braille", False)

        if args.boost:
            image, was_resized = apply_trumble_cel_shading(image, target_width=args.width, is_blocks=is_blocks_mode, is_braille=args.braille)
            if not was_resized:
                image = resize_image(image, args.width, is_blocks=is_blocks_mode, is_braille=args.braille)
        else:
            image = resize_image(image, args.width, is_blocks=is_blocks_mode, is_braille=args.braille)
        
        # Difuminado ordenado con matriz de Bayer para simular sombreado retro
        if args.dither:
            image = apply_bayer_dither(image)
        
        if args.braille:
            ascii_art = convert_image_to_braille(image, args.color, invert_mode)
        else:
            ascii_art = convert_image_to_blocks(image)

    # 4. Filtro retro CRT / Scanlines
    if getattr(args, "crt", None):
        ascii_art = apply_crt_filter(ascii_art, crt_mode=args.crt)

    # 5. Copiado inteligente al portapapeles (-C / --copy y --copy-plain)
    if getattr(args, "copy", False) or getattr(args, "copy_plain", False):
        plain = getattr(args, "copy_plain", False)
        copy_to_clipboard(ascii_art, plain=plain)
    
    if args.output:
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".webp":
            print(_("export_webp_disabled"))
            return
        if ext in (".png", ".jpg", ".jpeg"):
            # Los stickers con fondo transparente son exclusivos del motor a blanco y negro (Luris Mono)
            is_luris = (engine == "luris" or not args.color or args.manga or args.sketch)
            effective_transparent = args.transparent and is_luris
            if args.transparent and not is_luris:
                print(_("export_sticker_mono_only"))
            try:
                export_ansi_to_image(ascii_art, args.output, transparent=effective_transparent)
                print(_("export_success", args.output))
            except Exception as e:
                print(_("export_error", e))
        elif ext in (".ans", ".asc"):
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(ascii_art)
                print(_("saved_to", args.output))
            except Exception as e:
                print(_("error_save", e))
        elif ext == ".txt":
            try:
                plain_txt = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', ascii_art)
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(plain_txt)
                print(_("saved_to", args.output))
            except Exception as e:
                print(_("error_save", e))
        else:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(ascii_art)
                print(_("saved_to", args.output))
            except Exception as e:
                # Error al guardar el archivo en disco
                print(_("error_save", e))
    else:
        # Imprimir salida instantáneamente (o con reveal progresivo si se especificó --reveal)
        instant_mode = not getattr(args, "reveal", False) or getattr(args, "instant", False)
        print_with_reveal(ascii_art, instant=instant_mode)

    # Registrar el comando en el historial
    record_command_to_history()

if __name__ == "__main__":
    main()
