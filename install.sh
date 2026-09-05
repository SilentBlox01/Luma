#!/bin/bash
# ==============================================================================
#  Luma / Lumart Universal Installer / Instalador Universal
#  Compatible: Fedora, RHEL, Ubuntu, Debian, Arch Linux, openSUSE, macOS
#  "Si esto no funciona a la primera, el problema suele estar entre la silla y el teclado"
# ==============================================================================
set -e

VERSION="2.2.0"

# Color helpers
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

# --- Language Autodetection ---
SYS_LOCALE="${LC_ALL:-${LC_MESSAGES:-${LANG:-}}}"
LANG_MODE="en"
if [[ "$SYS_LOCALE" =~ ^es ]]; then
    LANG_MODE="es"
fi

for arg in "$@"; do
    case "$arg" in
        --lang=es|--es) LANG_MODE="es" ;;
        --lang=en|--en) LANG_MODE="en" ;;
        --update|-u|--check-update) CHECK_MODE=1 ;;
        --upgrade|-uu) UPGRADE_MODE=1 ;;
        --downgrade|-dg|--rollback) DOWNGRADE_MODE=1 ;;
    esac
done
if [ "$1" = "--lang" ] && [ -n "$2" ]; then
    LANG_MODE="$2"
fi

if [ "${CHECK_MODE:-0}" -eq 1 ]; then
    if command -v luma &>/dev/null; then
        exec luma -u
    elif command -v lumart &>/dev/null; then
        exec lumart -u
    fi
fi
if [ "${UPGRADE_MODE:-0}" -eq 1 ]; then
    if command -v luma &>/dev/null; then
        exec luma -uu
    elif command -v lumart &>/dev/null; then
        exec lumart -uu
    fi
fi
if [ "${DOWNGRADE_MODE:-0}" -eq 1 ]; then
    if command -v luma &>/dev/null; then
        exec luma -dg
    elif command -v lumart &>/dev/null; then
        exec lumart -dg
    fi
fi

if [ "$LANG_MODE" = "es" ]; then
    MSG_TAGLINE="Motor de Arte para Terminal"
    MSG_START="Iniciando instalación... (abróchense los cinturones)\n"
    MSG_NO_PYTHON="❌ Error: No tienes Python 3 instalado en tu sistema. ¿En qué cueva vives bro?"
    MSG_INSTALL_PY="Por favor instala Python 3 con el gestor de paquetes de tu distribución antes de llorar:"
    MSG_COPY_LOCAL="📦 Copiando el motor de Luma desde fuente local a"
    MSG_DOWNLOAD="⬇️  Descargando la versión más reciente de Luma v${VERSION} desde GitHub..."
    MSG_CHECK_DEPS="🔍 Verificando dependencias necesarias (Pillow)..."
    MSG_RESOLVING="⚙️  Pillow no detectado. Resolviendo dependencias automáticamente..."
    MSG_FEDORA="📦 Detectado Fedora/RHEL. Instalando python3-pillow vía dnf (mandando al carajo las restricciones de Red Hat)..."
    MSG_DEBIAN="📦 Detectado Debian/Ubuntu. Instalando python3-pil vía apt (el confiable que nunca te abandona)..."
    MSG_ARCH="📦 Detectado Arch Linux. Sí, ya sabemos que usas Arch btw... instalando con pacman a la velocidad de la luz..."
    MSG_SUSE="📦 Detectado openSUSE. Saludos cordiales a los 3 geckos que usan zypper en este planeta..."
    MSG_PIP="🐍 Intentando instalar con pip de usuario (--break-system-packages) para ignorar restricciones..."
    MSG_VENV="🛡️  Creando entorno virtual aislado en"
    MSG_FAIL="⚠️  Nota: No se pudo instalar Pillow automáticamente."
    MSG_FAIL_HINT="Por favor, instálalo manualmente con:"
    MSG_FORGING="🔗 Creando los binarios ejecutables (luma y lumart)..."
    MSG_SUCCESS="✅ ¡Luma v${VERSION} instalado exitosamente!"
    MSG_READY="Ya puedes usar luma y lumart desde cualquier directorio."
    MSG_PATH_WARN="⚠️  Aviso: INSTALL_DIR no está en tu \$PATH."
    MSG_PATH_HINT="Agrégalo a tu ~/.bashrc o ~/.zshrc antes de abrir un issue llorando 'command not found':"
    MSG_UPDATE_HINT="💡 Comprueba actualizaciones con: luma -u (o actualiza con: luma -uu, rollback: luma -dg)"
    MSG_TEST="Prueba rápida para verificar el funcionamiento:"
else
    MSG_TAGLINE="Terminal Art Engine"
    MSG_START="Starting installation... (buckle up, magic is about to happen)\n"
    MSG_NO_PYTHON="❌ Error: Python 3 was not found. What cave have you been living in?"
    MSG_INSTALL_PY="Please install Python 3 using your system package manager and try again:"
    MSG_COPY_LOCAL="📦 Copying Luma engine from local source to"
    MSG_DOWNLOAD="⬇️  Downloading latest Luma v${VERSION} from GitHub..."
    MSG_CHECK_DEPS="🔍 Checking dependencies (Pillow)..."
    MSG_RESOLVING="⚙️  Pillow not detected. Resolving dependencies automatically..."
    MSG_FEDORA="📦 Detected Fedora/RHEL. Installing python3-pillow via dnf (bypassing Red Hat PEP 668 restrictions)..."
    MSG_DEBIAN="📦 Detected Debian/Ubuntu. Installing python3-pil via apt..."
    MSG_ARCH="📦 Detected Arch Linux. Yes, we know you use Arch btw... installing with pacman at lightspeed..."
    MSG_SUSE="📦 Detected openSUSE. Greetings to the 3 geckos currently using zypper on Earth..."
    MSG_PIP="🐍 Trying pip user install (--break-system-packages) to bypass restrictions..."
    MSG_VENV="🛡️  Setting up isolated virtual environment in"
    MSG_FAIL="⚠️  Note: Could not auto-install Pillow automatically."
    MSG_FAIL_HINT="Please install it manually:"
    MSG_FORGING="🔗 Linking executable commands (luma and lumart)..."
    MSG_SUCCESS="✅ Luma v${VERSION} installed successfully!"
    MSG_READY="You can now use luma and lumart from anywhere."
    MSG_PATH_WARN="⚠️  Notice: INSTALL_DIR is not yet in your PATH."
    MSG_PATH_HINT="Add this line to your ~/.bashrc or ~/.zshrc before opening an issue crying 'command not found':"
    MSG_UPDATE_HINT="💡 Check for updates with: luma -u (or upgrade with: luma -uu, rollback: luma -dg)"
    MSG_TEST="Quick test:"
fi

echo -e "${CYAN}"
echo " █    █ █ █▄ ▄█ ▄▀▄ █▀▄ ▀█▀"
echo " █▄▄▄ ▀▄█ █ ▀ █ █▀█ █▀▄  █"
echo " v${VERSION} - ${MSG_TAGLINE}"
echo -e "${NC}"
echo -e "${MSG_START}"

# 1. Check Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}${MSG_NO_PYTHON}${NC}"
    echo "${MSG_INSTALL_PY}"
    echo "  • Fedora:   sudo dnf install python3"
    echo "  • Ubuntu:   sudo apt install python3"
    echo "  • Arch:     sudo pacman -S python"
    exit 1
fi

# 2. Determine target install directory
if [ "$EUID" -eq 0 ]; then
    INSTALL_DIR="/usr/local/bin"
    SHARE_DIR="/usr/local/share/luma"
else
    INSTALL_DIR="$HOME/.local/bin"
    SHARE_DIR="$HOME/.local/share/luma"
fi

mkdir -p "$INSTALL_DIR"
mkdir -p "$SHARE_DIR"

# 3. Locate or download lumart.py and mary.py
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"
if [ -f "$SCRIPT_DIR/lumart.py" ]; then
    echo -e "${MSG_COPY_LOCAL} ${SHARE_DIR}..."
    cp "$SCRIPT_DIR/lumart.py" "$SHARE_DIR/lumart.py"
else
    echo -e "${MSG_DOWNLOAD}"
    curl -fsSL "https://raw.githubusercontent.com/SilentBlox01/Luma/main/lumart.py" -o "$SHARE_DIR/lumart.py"
fi
chmod +x "$SHARE_DIR/lumart.py"

if [ -f "$SCRIPT_DIR/mary.py" ]; then
    cp "$SCRIPT_DIR/mary.py" "$SHARE_DIR/mary.py"
else
    curl -fsSL "https://raw.githubusercontent.com/SilentBlox01/Luma/main/mary.py" -o "$SHARE_DIR/mary.py" 2>/dev/null || true
fi
chmod +x "$SHARE_DIR/mary.py" 2>/dev/null || true

# 3b. C++ Monochrome Engine (standalone binary and shared library)
if [ -f "$SCRIPT_DIR/monochrome.cpp" ]; then
    cp "$SCRIPT_DIR/monochrome.cpp" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image.h" ] && cp "$SCRIPT_DIR/stb_image.h" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image_resize2.h" ] && cp "$SCRIPT_DIR/stb_image_resize2.h" "$SHARE_DIR/"
    if command -v g++ &>/dev/null; then
        echo "⚡ Compiling native C++ monochrome engine (luma-mono)..."
        g++ -O3 -std=c++17 -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$INSTALL_DIR/luma-mono" 2>/dev/null || true
        g++ -O3 -std=c++17 -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$SHARE_DIR/libmonochrome.so" 2>/dev/null || true
    fi
fi

# 3c. C++ Mary Color Super-Engine (standalone binary and shared library)
if [ -f "$SCRIPT_DIR/mary.cpp" ]; then
    cp "$SCRIPT_DIR/mary.cpp" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image.h" ] && cp "$SCRIPT_DIR/stb_image.h" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image_resize2.h" ] && cp "$SCRIPT_DIR/stb_image_resize2.h" "$SHARE_DIR/"
    if command -v g++ &>/dev/null; then
        echo "⚡ Compiling native C++ Mary color super-engine (luma-mary)..."
        g++ -O3 -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || \
        g++ -O3 -std=c++17 -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || true

        g++ -O3 -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || \
        g++ -O3 -std=c++17 -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || true
    fi
fi

# 4. Resolve Pillow dependency (auto-resolution)
echo -e "${MSG_CHECK_DEPS}"
if ! python3 -c "from PIL import Image" &>/dev/null; then
    echo -e "${YELLOW}${MSG_RESOLVING}${NC}"
    INSTALLED=0

    # Option A: Check for distro native package managers
    if [ "$EUID" -eq 0 ] || command -v sudo &>/dev/null; then
        SUDO_CMD=""
        [ "$EUID" -ne 0 ] && SUDO_CMD="sudo"

        if command -v dnf &>/dev/null; then
            echo "${MSG_FEDORA}"
            $SUDO_CMD dnf install -y python3-pillow &>/dev/null && INSTALLED=1 || true
        elif command -v apt-get &>/dev/null; then
            echo "${MSG_DEBIAN}"
            $SUDO_CMD apt-get update -qq && $SUDO_CMD apt-get install -y -qq python3-pil &>/dev/null && INSTALLED=1 || true
        elif command -v pacman &>/dev/null; then
            echo "${MSG_ARCH}"
            $SUDO_CMD pacman -S --noconfirm python-pillow &>/dev/null && INSTALLED=1 || true
        elif command -v zypper &>/dev/null; then
            echo "${MSG_SUSE}"
            $SUDO_CMD zypper --non-interactive install python3-Pillow &>/dev/null && INSTALLED=1 || true
        fi

    fi

    # Option B: Pip user install with PEP 668 bypass
    if [ "$INSTALLED" -eq 0 ]; then
        echo "${MSG_PIP}"
        python3 -m pip install Pillow --user --break-system-packages -q &>/dev/null && INSTALLED=1 || true
    fi

    # Option C: Dedicated isolated virtual environment
    if [ "$INSTALLED" -eq 0 ]; then
        echo "${MSG_VENV} $SHARE_DIR/venv..."
        python3 -m venv "$SHARE_DIR/venv" &>/dev/null || true
        if [ -f "$SHARE_DIR/venv/bin/pip" ]; then
            "$SHARE_DIR/venv/bin/pip" install Pillow -q &>/dev/null && INSTALLED=2 || true
        fi
    fi

    if [ "$INSTALLED" -eq 0 ]; then
        echo -e "${YELLOW}${MSG_FAIL}${NC}"
        echo "${MSG_FAIL_HINT}"
        echo "  • Fedora:       sudo dnf install python3-pillow"
        echo "  • Ubuntu/Debian: sudo apt install python3-pil"
        echo "  • Arch Linux:    sudo pacman -S python-pillow"
    fi
fi

# 5. Create launcher wrappers in INSTALL_DIR
echo -e "${MSG_FORGING}"

PY_EXEC="python3"
if [ -f "$SHARE_DIR/venv/bin/python" ]; then
    PY_EXEC="$SHARE_DIR/venv/bin/python"
fi

rm -f "$INSTALL_DIR/lumart" "$INSTALL_DIR/luma"
cat << EOF > "$INSTALL_DIR/lumart"
#!/bin/bash
exec "$PY_EXEC" "$SHARE_DIR/lumart.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/lumart"
ln -sf "$INSTALL_DIR/lumart" "$INSTALL_DIR/luma"

# 6. Verify PATH
IN_PATH=0
case ":$PATH:" in
    *":$INSTALL_DIR:"*) IN_PATH=1 ;;
esac

echo -e "\n${GREEN}${MSG_SUCCESS}${NC}"
echo -e "${MSG_READY}\n"

if [ "$IN_PATH" -eq 0 ]; then
    echo -e "${YELLOW}${MSG_PATH_WARN/INSTALL_DIR/$INSTALL_DIR}${NC}"
    echo "${MSG_PATH_HINT}"
    echo -e "  ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}\n"
fi

echo -e "${MSG_UPDATE_HINT}\n"
echo "${MSG_TEST}"
echo "  luma --help"
echo "  luma -u"
echo "  luma -uu"
echo "  luma -dg"
echo "  luma /path/to/image.png --braille"

