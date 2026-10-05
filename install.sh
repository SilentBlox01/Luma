#!/bin/bash
# ==============================================================================
#  Luma / Lumart Universal Installer / Instalador Universal
#  Compatible: Fedora, RHEL, Ubuntu, Debian, Arch Linux, openSUSE, macOS
#  "Si esto no funciona a la primera, el problema suele estar entre la silla y el teclado"
# ==============================================================================
set -e

VERSION="2.5.0"

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

WITH_DESKTOP=0

for arg in "$@"; do
    case "$arg" in
        --lang=es|--es) LANG_MODE="es" ;;
        --lang=en|--en) LANG_MODE="en" ;;
        --update|-u|--check-update) CHECK_MODE=1 ;;
        --upgrade|-uu) UPGRADE_MODE=1 ;;
        --downgrade|-dg|--rollback) DOWNGRADE_MODE=1 ;;
        --desktop|--with-desktop) WITH_DESKTOP=1 ;;
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
    MSG_NO_PYTHON="❌ Error: No tienes Python 3 instalado en tu sistema."
    MSG_INSTALL_PY="Por favor instala Python 3 con el gestor de paquetes de tu distribución:"
    MSG_COPY_LOCAL="📦 Copiando el motor de Luma desde fuente local a"
    MSG_DOWNLOAD="⬇️  Descargando la versión más reciente de Luma v${VERSION} desde GitHub..."
    MSG_CHECK_DEPS="🔍 Verificando dependencias necesarias (Pillow)..."
    MSG_RESOLVING="⚙️  Pillow no detectado. Resolviendo dependencias automáticamente..."
    MSG_FEDORA="📦 Detectado Fedora/RHEL. Instalando python3-pillow vía dnf..."
    MSG_DEBIAN="📦 Detectado Debian/Ubuntu/derivadas. Instalando python3-pil vía apt..."
    MSG_ARCH="📦 Detectado Arch Linux. Instalando python-pillow vía pacman..."
    MSG_SUSE="📦 Detectado openSUSE. Instalando python3-Pillow vía zypper..."
    MSG_PIP="🐍 Instalando Pillow con pip de usuario (--break-system-packages)..."
    MSG_VENV="🛡️  Creando entorno virtual aislado en"
    MSG_FAIL="⚠️  Nota: No se pudo instalar Pillow automáticamente."
    MSG_FAIL_HINT="Por favor, instálalo manualmente con:"
    MSG_FORGING="🔗 Creando los binarios ejecutables (luma y lumart)..."
    MSG_SUCCESS="✅ ¡Luma v${VERSION} instalado exitosamente!"
    MSG_READY="Ya puedes usar luma y lumart desde cualquier directorio."
    MSG_PATH_WARN="⚠️  Aviso: INSTALL_DIR no está en tu \$PATH."
    MSG_PATH_HINT="Agrégalo a tu ~/.bashrc o ~/.zshrc:"
    MSG_UPDATE_HINT="💡 Comprueba actualizaciones con: luma -u (o actualiza con: luma -uu, rollback: luma -dg)"
    MSG_TEST="Prueba rápida para verificar el funcionamiento:"
else
    MSG_TAGLINE="Terminal Art Engine"
    MSG_START="Starting installation... (buckle up, magic is about to happen)\n"
    MSG_NO_PYTHON="❌ Error: Python 3 was not found."
    MSG_INSTALL_PY="Please install Python 3 using your system package manager and try again:"
    MSG_COPY_LOCAL="📦 Copying Luma engine from local source to"
    MSG_DOWNLOAD="⬇️  Downloading latest Luma v${VERSION} from GitHub..."
    MSG_CHECK_DEPS="🔍 Checking dependencies (Pillow)..."
    MSG_RESOLVING="⚙️  Pillow not detected. Resolving dependencies automatically..."
    MSG_FEDORA="📦 Detected Fedora/RHEL. Installing python3-pillow via dnf..."
    MSG_DEBIAN="📦 Detected Debian/Ubuntu/derivatives. Installing python3-pil via apt..."
    MSG_ARCH="📦 Detected Arch Linux. Installing python-pillow via pacman..."
    MSG_SUSE="📦 Detected openSUSE. Installing python3-Pillow via zypper..."
    MSG_PIP="🐍 Installing Pillow with user pip (--break-system-packages)..."
    MSG_VENV="🛡️  Setting up isolated virtual environment in"
    MSG_FAIL="⚠️  Note: Could not auto-install Pillow automatically."
    MSG_FAIL_HINT="Please install it manually:"
    MSG_FORGING="🔗 Linking executable commands (luma and lumart)..."
    MSG_SUCCESS="✅ Luma v${VERSION} installed successfully!"
    MSG_READY="You can now use luma and lumart from anywhere."
    MSG_PATH_WARN="⚠️  Notice: INSTALL_DIR is not yet in your PATH."
    MSG_PATH_HINT="Add this line to your ~/.bashrc or ~/.zshrc:"
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
    echo "  • Fedora/RHEL:   sudo dnf install python3"
    echo "  • Ubuntu/Debian: sudo apt install python3"
    echo "  • Arch Linux:    sudo pacman -S python"
    echo "  • openSUSE:      sudo zypper install python3"
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
    [ -L "$SHARE_DIR/lumart.py" ] && rm -f "$SHARE_DIR/lumart.py"
    cp "$SCRIPT_DIR/lumart.py" "$SHARE_DIR/lumart.py"
else
    echo -e "${MSG_DOWNLOAD}"
    curl -fsSL "https://raw.githubusercontent.com/SilentBlox01/Luma/main/lumart.py" -o "$SHARE_DIR/lumart.py"
fi
chmod +x "$SHARE_DIR/lumart.py"

if [ -f "$SCRIPT_DIR/mary.py" ]; then
    [ -L "$SHARE_DIR/mary.py" ] && rm -f "$SHARE_DIR/mary.py"
    cp "$SCRIPT_DIR/mary.py" "$SHARE_DIR/mary.py"
else
    curl -fsSL "https://raw.githubusercontent.com/SilentBlox01/Luma/main/mary.py" -o "$SHARE_DIR/mary.py" 2>/dev/null || true
fi
chmod +x "$SHARE_DIR/mary.py" 2>/dev/null || true

if [ -d "$SCRIPT_DIR/completions" ]; then
    mkdir -p "$SHARE_DIR/completions" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/completions/"* "$SHARE_DIR/completions/" 2>/dev/null || true
fi

# 3b. C++ Monochrome Engine (standalone binary and shared library)
if [ -f "$SCRIPT_DIR/monochrome.cpp" ]; then
    cp "$SCRIPT_DIR/monochrome.cpp" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image.h" ] && cp "$SCRIPT_DIR/stb_image.h" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image_resize2.h" ] && cp "$SCRIPT_DIR/stb_image_resize2.h" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/libmonochrome.so" ] && cp "$SCRIPT_DIR/libmonochrome.so" "$SHARE_DIR/" 2>/dev/null || true
    [ -f "$SCRIPT_DIR/luma-mono" ] && cp "$SCRIPT_DIR/luma-mono" "$INSTALL_DIR/" 2>/dev/null || true
    if command -v g++ &>/dev/null; then
        echo "⚡ Compiling native C++ monochrome engine (luma-mono)..."
        g++ -O3 -march=native -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$INSTALL_DIR/luma-mono" 2>/dev/null || \
        g++ -O3 -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$INSTALL_DIR/luma-mono" 2>/dev/null || \
        g++ -O3 -std=c++17 -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$INSTALL_DIR/luma-mono" 2>/dev/null || true

        g++ -O3 -march=native -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$SHARE_DIR/libmonochrome.so" 2>/dev/null || \
        g++ -O3 -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$SHARE_DIR/libmonochrome.so" 2>/dev/null || \
        g++ -O3 -std=c++17 -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$SHARE_DIR/libmonochrome.so" 2>/dev/null || true
    else
        echo -e "${YELLOW}ℹ️  g++ no detectado. Para soporte C++ de máxima aceleración:${NC}"
        echo "  • Fedora/RHEL:   sudo dnf install gcc-c++ libgomp"
        echo "  • Debian/Ubuntu: sudo apt install g++"
        echo "  • Arch Linux:    sudo pacman -S gcc"
    fi
fi

# 3c. C++ Mary Color Super-Engine (standalone binary and shared library)
if [ -f "$SCRIPT_DIR/mary.cpp" ]; then
    cp "$SCRIPT_DIR/mary.cpp" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image.h" ] && cp "$SCRIPT_DIR/stb_image.h" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/stb_image_resize2.h" ] && cp "$SCRIPT_DIR/stb_image_resize2.h" "$SHARE_DIR/"
    [ -f "$SCRIPT_DIR/libmary.so" ] && cp "$SCRIPT_DIR/libmary.so" "$SHARE_DIR/" 2>/dev/null || true
    [ -f "$SCRIPT_DIR/luma-mary" ] && cp "$SCRIPT_DIR/luma-mary" "$INSTALL_DIR/" 2>/dev/null || true
    if command -v g++ &>/dev/null; then
        echo "⚡ Compiling native C++ Mary color super-engine (luma-mary)..."
        g++ -O3 -march=native -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || \
        g++ -O3 -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || \
        g++ -O3 -std=c++17 -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || true

        g++ -O3 -march=native -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || \
        g++ -O3 -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || \
        g++ -O3 -std=c++17 -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || true
    fi
fi

# 4. Resolve Pillow dependency (auto-resolution)
echo -e "${MSG_CHECK_DEPS}"
if ! python3 -c "from PIL import Image" &>/dev/null; then
    echo -e "${YELLOW}${MSG_RESOLVING}${NC}"
    INSTALLED=0

    # Opción A: Modo administrador / root
    if [ "$EUID" -eq 0 ]; then
        if command -v dnf5 &>/dev/null; then
            echo "${MSG_FEDORA}"
            dnf5 install -y python3-pillow && INSTALLED=1 || true
        elif command -v dnf &>/dev/null; then
            echo "${MSG_FEDORA}"
            dnf install -y python3-pillow && INSTALLED=1 || true
        elif command -v apt-get &>/dev/null; then
            echo "${MSG_DEBIAN}"
            (apt-get update -qq && (apt-get install -y -qq python3-pil || apt-get install -y -qq python3-pillow)) && INSTALLED=1 || true
        elif command -v pacman &>/dev/null; then
            echo "${MSG_ARCH}"
            pacman -S --noconfirm python-pillow && INSTALLED=1 || true
        elif command -v zypper &>/dev/null; then
            echo "${MSG_SUSE}"
            zypper --non-interactive install python3-Pillow && INSTALLED=1 || true
        fi
    else
        # Opción B: Modo usuario regular (sin sudo invasivo que bloquee)
        echo "${MSG_PIP}"
        python3 -m pip install Pillow --user --break-system-packages -q &>/dev/null && INSTALLED=1 || true

        # Opción C: Entorno virtual aislado en ~/.local/share/luma/venv
        if [ "$INSTALLED" -eq 0 ]; then
            echo "${MSG_VENV} $SHARE_DIR/venv..."
            python3 -m venv "$SHARE_DIR/venv" &>/dev/null || true
            if [ -f "$SHARE_DIR/venv/bin/pip" ]; then
                "$SHARE_DIR/venv/bin/pip" install Pillow -q &>/dev/null && INSTALLED=2 || true
            fi
        fi

        # Opción D: Si las opciones de usuario fallaron y sudo está disponible
        if [ "$INSTALLED" -eq 0 ] && command -v sudo &>/dev/null; then
            if command -v dnf5 &>/dev/null; then
                echo "${MSG_FEDORA}"
                sudo dnf5 install -y python3-pillow && INSTALLED=1 || true
            elif command -v dnf &>/dev/null; then
                echo "${MSG_FEDORA}"
                sudo dnf install -y python3-pillow && INSTALLED=1 || true
            elif command -v apt-get &>/dev/null; then
                echo "${MSG_DEBIAN}"
                (sudo apt-get update -qq && (sudo apt-get install -y -qq python3-pil || sudo apt-get install -y -qq python3-pillow)) && INSTALLED=1 || true
            elif command -v pacman &>/dev/null; then
                echo "${MSG_ARCH}"
                sudo pacman -S --noconfirm python-pillow && INSTALLED=1 || true
            elif command -v zypper &>/dev/null; then
                echo "${MSG_SUSE}"
                sudo zypper --non-interactive install python3-Pillow && INSTALLED=1 || true
            fi
        fi
    fi

    if [ "$INSTALLED" -eq 0 ]; then
        echo -e "${YELLOW}${MSG_FAIL}${NC}"
        echo "${MSG_FAIL_HINT}"
        echo "  • Fedora/RHEL:   sudo dnf install python3-pillow"
        echo "  • Debian/Ubuntu: sudo apt install python3-pil"
        echo "  • Arch Linux:    sudo pacman -S python-pillow"
        echo "  • openSUSE:      sudo zypper install python3-Pillow"
    fi
fi

# 5. Create launcher wrappers in INSTALL_DIR
echo -e "${MSG_FORGING}"

PY_EXEC="python3"
if [ -f "$SHARE_DIR/venv/bin/python" ]; then
    PY_EXEC="$SHARE_DIR/venv/bin/python"
fi

rm -f "$INSTALL_DIR/lumart" "$INSTALL_DIR/luma"
cat << EOF_WRAPPER > "$INSTALL_DIR/lumart"
#!/bin/bash
exec "$PY_EXEC" "$SHARE_DIR/lumart.py" "\$@"
EOF_WRAPPER

chmod +x "$INSTALL_DIR/lumart"
ln -sf "$INSTALL_DIR/lumart" "$INSTALL_DIR/luma"

# 5b. Manejo de icono de escritorio: CLI limpia por defecto, opcional con --desktop
if [ "$WITH_DESKTOP" -eq 1 ]; then
    "$INSTALL_DIR/lumart" --install-desktop &>/dev/null || true
else
    # Limpieza proactiva: Eliminar cualquier lanzador .desktop residual previo
    rm -f "$HOME/.local/share/applications/lumart.desktop" "$HOME/Desktop/lumart.desktop" 2>/dev/null || true
    if command -v update-desktop-database &>/dev/null; then
        update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    fi
fi

# 5c. Shell Completions & UNIX Man Page
if [ "$EUID" -eq 0 ]; then
    BASH_COMP_DIR="/usr/share/bash-completion/completions"
    ZSH_COMP_DIR="/usr/share/zsh/site-functions"
    FISH_COMP_DIR="/usr/share/fish/vendor_completions.d"
    MAN_DIR="/usr/local/share/man/man1"
else
    BASH_COMP_DIR="$HOME/.local/share/bash-completion/completions"
    ZSH_COMP_DIR="$HOME/.local/share/zsh/site-functions"
    FISH_COMP_DIR="$HOME/.local/share/fish/vendor_completions.d"
    MAN_DIR="$HOME/.local/share/man/man1"
fi

if [ -f "$SCRIPT_DIR/completions/lumart.bash" ]; then
    mkdir -p "$BASH_COMP_DIR" 2>/dev/null || true
    cp "$SCRIPT_DIR/completions/lumart.bash" "$BASH_COMP_DIR/lumart" 2>/dev/null || true
    ln -sf lumart "$BASH_COMP_DIR/luma" 2>/dev/null || true
fi
if [ -f "$SCRIPT_DIR/completions/_lumart" ]; then
    mkdir -p "$ZSH_COMP_DIR" 2>/dev/null || true
    cp "$SCRIPT_DIR/completions/_lumart" "$ZSH_COMP_DIR/_lumart" 2>/dev/null || true
    ln -sf _lumart "$ZSH_COMP_DIR/_luma" 2>/dev/null || true
    if [ "$EUID" -ne 0 ]; then
        mkdir -p "$HOME/.zsh/completion" 2>/dev/null || true
        cp "$SCRIPT_DIR/completions/_lumart" "$HOME/.zsh/completion/_lumart" 2>/dev/null || true
        ln -sf _lumart "$HOME/.zsh/completion/_luma" 2>/dev/null || true
    fi
fi
if [ -f "$SCRIPT_DIR/completions/lumart.fish" ]; then
    mkdir -p "$FISH_COMP_DIR" 2>/dev/null || true
    cp "$SCRIPT_DIR/completions/lumart.fish" "$FISH_COMP_DIR/lumart.fish" 2>/dev/null || true
    ln -sf lumart.fish "$FISH_COMP_DIR/luma.fish" 2>/dev/null || true
fi
if [ -f "$SCRIPT_DIR/man/lumart.1" ]; then
    mkdir -p "$MAN_DIR" 2>/dev/null || true
    cp "$SCRIPT_DIR/man/lumart.1" "$MAN_DIR/lumart.1" 2>/dev/null || true
    ln -sf lumart.1 "$MAN_DIR/luma.1" 2>/dev/null || true
    if command -v mandb &>/dev/null; then
        mandb -q "$MAN_DIR/.." 2>/dev/null || true
    fi
fi

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
echo "  luma /path/to/image.png"
