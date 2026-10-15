#!/usr/bin/env bash
# ==============================================================================
#  Luma / Lumart Universal Installer / Instalador Universal
#  Compatible: Fedora, RHEL, Ubuntu, Debian, Arch Linux, openSUSE, Void, Alpine,
#              Gentoo, NixOS, macOS, Android (Termux)
# ==============================================================================
set -e

VERSION="2.5.1"
RAW_BASE="https://raw.githubusercontent.com/SilentBlox01/Luma/main"

# Color helpers
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

# --- Environment & OS Autodetection ---
IS_TERMUX=0
if [ -n "${TERMUX_VERSION:-}" ] || [ -d "/data/data/com.termux" ] || [[ "${PREFIX:-}" == *"com.termux"* ]] || ([ -n "${PREFIX:-}" ] && [ -d "$PREFIX/bin" ] && [ -w "$PREFIX/bin" ] && ! [ -d "/usr/bin" ]); then
    IS_TERMUX=1
fi

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
    MSG_TERMUX="📦 Detectado Termux (Android). Instalando python-pillow vía pkg..."
    MSG_VOID="📦 Detectado Void Linux. Instalando python3-Pillow vía xbps-install..."
    MSG_ALPINE="📦 Detectado Alpine Linux. Instalando py3-pillow vía apk..."
    MSG_GENTOO="📦 Detectado Gentoo Linux. Instalando dev-python/pillow vía emerge..."
    MSG_NIX="📦 Detectado Nix/NixOS. Instalando python3Packages.pillow vía nix-env..."
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
    MSG_TERMUX="📦 Detected Termux (Android). Installing python-pillow via pkg..."
    MSG_VOID="📦 Detected Void Linux. Installing python3-Pillow via xbps-install..."
    MSG_ALPINE="📦 Detected Alpine Linux. Installing py3-pillow via apk..."
    MSG_GENTOO="📦 Detected Gentoo Linux. Installing dev-python/pillow via emerge..."
    MSG_NIX="📦 Detected Nix/NixOS. Installing python3Packages.pillow via nix-env..."
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

# 1. Android Termux Auto-Bootstrap & Python 3 Check
if [ "$IS_TERMUX" -eq 1 ] && command -v pkg &>/dev/null; then
    NEEDED_PKGS=()
    command -v python3 &>/dev/null || NEEDED_PKGS+=("python")
    python3 -c "from PIL import Image" &>/dev/null 2>&1 || NEEDED_PKGS+=("python-pillow")
    command -v clang++ &>/dev/null || NEEDED_PKGS+=("clang" "make" "libomp")
    if [ ${#NEEDED_PKGS[@]} -gt 0 ]; then
        if [ "$LANG_MODE" = "es" ]; then
            echo -e "${YELLOW}📦 Detectado Termux (Android). Instalando paquetes esenciales: ${NEEDED_PKGS[*]}...${NC}"
        else
            echo -e "${YELLOW}📦 Detected Termux (Android). Installing essential packages: ${NEEDED_PKGS[*]}...${NC}"
        fi
        pkg install -y "${NEEDED_PKGS[@]}" || true
    fi
fi

if ! command -v python3 &>/dev/null; then
    echo -e "${RED}${MSG_NO_PYTHON}${NC}"
    echo "${MSG_INSTALL_PY}"
    echo "  • Android (Termux): pkg install python python-pillow"
    echo "  • Fedora/RHEL:      sudo dnf install python3"
    echo "  • Ubuntu/Debian:    sudo apt install python3"
    echo "  • Arch Linux:       sudo pacman -S python"
    echo "  • openSUSE:         sudo zypper install python3"
    echo "  • Void Linux:       sudo xbps-install -S python3"
    echo "  • Alpine Linux:     sudo apk add python3"
    echo "  • Gentoo Linux:     sudo emerge --ask dev-lang/python"
    echo "  • NixOS / Nix:      nix-shell -p python3"
    exit 1
fi

# 2. Determine target install directory
if [ "$IS_TERMUX" -eq 1 ] && [ -n "${PREFIX:-}" ] && [ -d "$PREFIX/bin" ] && [ -w "$PREFIX/bin" ]; then
    # Termux / Android environment: standard prefix
    INSTALL_DIR="$PREFIX/bin"
    SHARE_DIR="$PREFIX/share/luma"
elif [ "$EUID" -eq 0 ]; then
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
    curl -fsSL "$RAW_BASE/lumart.py" -o "$SHARE_DIR/lumart.py"
fi
chmod +x "$SHARE_DIR/lumart.py"

if [ -f "$SCRIPT_DIR/mary.py" ]; then
    [ -L "$SHARE_DIR/mary.py" ] && rm -f "$SHARE_DIR/mary.py"
    cp "$SCRIPT_DIR/mary.py" "$SHARE_DIR/mary.py"
else
    curl -fsSL "$RAW_BASE/mary.py" -o "$SHARE_DIR/mary.py" 2>/dev/null || true
fi
chmod +x "$SHARE_DIR/mary.py" 2>/dev/null || true

# 3b. Locate or download C++ engine sources and headers
for src_file in monochrome.cpp mary.cpp stb_image.h stb_image_resize2.h; do
    if [ -f "$SCRIPT_DIR/$src_file" ]; then
        cp "$SCRIPT_DIR/$src_file" "$SHARE_DIR/$src_file"
    elif [ ! -f "$SHARE_DIR/$src_file" ]; then
        curl -fsSL "$RAW_BASE/$src_file" -o "$SHARE_DIR/$src_file" 2>/dev/null || true
    fi
done

# If prebuilt binaries exist locally (e.g. from local git clone), copy them
[ -f "$SCRIPT_DIR/libmonochrome.so" ] && cp "$SCRIPT_DIR/libmonochrome.so" "$SHARE_DIR/" 2>/dev/null || true
[ -f "$SCRIPT_DIR/luma-mono" ] && cp "$SCRIPT_DIR/luma-mono" "$INSTALL_DIR/" 2>/dev/null || true
[ -f "$SCRIPT_DIR/libmary.so" ] && cp "$SCRIPT_DIR/libmary.so" "$SHARE_DIR/" 2>/dev/null || true
[ -f "$SCRIPT_DIR/luma-mary" ] && cp "$SCRIPT_DIR/luma-mary" "$INSTALL_DIR/" 2>/dev/null || true

# 3c. Compile native C++ engines if compiler is available
CXX_BIN=""
if command -v g++ &>/dev/null; then
    CXX_BIN="g++"
elif command -v clang++ &>/dev/null; then
    CXX_BIN="clang++"
fi

if [ -n "$CXX_BIN" ]; then
    if [ -f "$SHARE_DIR/monochrome.cpp" ]; then
        echo "⚡ Compiling native C++ monochrome engine (luma-mono) with $CXX_BIN..."
        "$CXX_BIN" -O3 -march=native -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$INSTALL_DIR/luma-mono" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$INSTALL_DIR/luma-mono" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$INSTALL_DIR/luma-mono" 2>/dev/null || true

        "$CXX_BIN" -O3 -march=native -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$SHARE_DIR/libmonochrome.so" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$SHARE_DIR/libmonochrome.so" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/monochrome.cpp" -o "$SHARE_DIR/libmonochrome.so" 2>/dev/null || true
    fi

    if [ -f "$SHARE_DIR/mary.cpp" ]; then
        echo "⚡ Compiling native C++ Mary color super-engine (luma-mary) with $CXX_BIN..."
        "$CXX_BIN" -O3 -march=native -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -fopenmp -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$INSTALL_DIR/luma-mary" 2>/dev/null || true

        "$CXX_BIN" -O3 -march=native -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -fopenmp -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || \
        "$CXX_BIN" -O3 -std=c++17 -fPIC -shared -I"$SHARE_DIR" "$SHARE_DIR/mary.cpp" -o "$SHARE_DIR/libmary.so" 2>/dev/null || true
    fi
else
    if [ "$LANG_MODE" = "es" ]; then
        echo -e "${YELLOW}ℹ️  Compilador C++ (g++/clang++) no detectado. Para soporte C++ de máxima aceleración:${NC}"
        echo "  • Android (Termux): pkg install clang make libomp"
        echo "  • Fedora/RHEL:      sudo dnf install gcc-c++ libgomp"
        echo "  • Debian/Ubuntu:    sudo apt install g++"
        echo "  • Arch Linux:       yay -S gcc (o: sudo pacman -S gcc)"
        echo "  • Void Linux:       sudo xbps-install -S gcc make"
        echo "  • Alpine Linux:     sudo apk add g++ openmp-dev make"
        echo "  • Gentoo Linux:     sudo emerge --ask sys-devel/gcc"
        echo "  • NixOS / Nix:      nix-shell -p gcc openmp"
    else
        echo -e "${YELLOW}ℹ️  C++ compiler (g++/clang++) not found. For maximum native C++ speed:${NC}"
        echo "  • Android (Termux): pkg install clang make libomp"
        echo "  • Fedora/RHEL:      sudo dnf install gcc-c++ libgomp"
        echo "  • Debian/Ubuntu:    sudo apt install g++"
        echo "  • Arch Linux:       sudo pacman -S gcc"
        echo "  • Void Linux:       sudo xbps-install -S gcc make"
        echo "  • Alpine Linux:     sudo apk add g++ openmp-dev make"
        echo "  • Gentoo Linux:     sudo emerge --ask sys-devel/gcc"
        echo "  • NixOS / Nix:      nix-shell -p gcc openmp"
    fi
fi

# 4. Resolve Pillow dependency (auto-resolution)
echo -e "${MSG_CHECK_DEPS}"
if ! python3 -c "from PIL import Image" &>/dev/null; then
    echo -e "${YELLOW}${MSG_RESOLVING}${NC}"
    INSTALLED=0

    # Opción macOS (Homebrew)
    if [ "$INSTALLED" -eq 0 ] && ([ "$(uname -s 2>/dev/null)" = "Darwin" ] || [[ "${OSTYPE:-}" == "darwin"* ]]); then
        if command -v brew &>/dev/null; then
            echo "📦 Detectado macOS. Instalando Pillow y dependencias vía Homebrew..."
            brew install pillow libomp && INSTALLED=1 || true
        fi
    fi

    # Opción Termux (Android)
    if [ "$IS_TERMUX" -eq 1 ] && command -v pkg &>/dev/null; then
        echo "${MSG_TERMUX}"
        pkg install -y python-pillow clang make libomp && INSTALLED=1 || true
    fi

    # Opción A: Modo administrador / root
    if [ "$INSTALLED" -eq 0 ] && [ "$EUID" -eq 0 ]; then
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
        elif command -v xbps-install &>/dev/null; then
            echo "${MSG_VOID}"
            xbps-install -Sy python3-Pillow && INSTALLED=1 || true
        elif command -v apk &>/dev/null; then
            echo "${MSG_ALPINE}"
            apk add --no-cache py3-pillow && INSTALLED=1 || true
        elif command -v emerge &>/dev/null; then
            echo "${MSG_GENTOO}"
            emerge --ask=n dev-python/pillow && INSTALLED=1 || true
        elif command -v nix-env &>/dev/null; then
            echo "${MSG_NIX}"
            nix-env -iA nixpkgs.python3Packages.pillow && INSTALLED=1 || true
        fi
    fi

    # Opción B: Modo usuario regular
    if [ "$INSTALLED" -eq 0 ]; then
        if command -v yay &>/dev/null; then
            echo "📦 Detectado yay (Arch Linux / AUR). Instalando dependencias de Pillow..."
            yay -S --noconfirm --needed python-pillow && INSTALLED=1 || true
        fi

        if [ "$INSTALLED" -eq 0 ]; then
            echo "${MSG_PIP}"
            python3 -m pip install Pillow --user --break-system-packages -q &>/dev/null && INSTALLED=1 || true
        fi

        # Opción C: Entorno virtual aislado en SHARE_DIR/venv
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
            elif command -v xbps-install &>/dev/null; then
                echo "${MSG_VOID}"
                sudo xbps-install -Sy python3-Pillow && INSTALLED=1 || true
            elif command -v apk &>/dev/null; then
                echo "${MSG_ALPINE}"
                sudo apk add --no-cache py3-pillow && INSTALLED=1 || true
            elif command -v emerge &>/dev/null; then
                echo "${MSG_GENTOO}"
                sudo emerge --ask=n dev-python/pillow && INSTALLED=1 || true
            elif command -v nix-env &>/dev/null; then
                echo "${MSG_NIX}"
                nix-env -iA nixpkgs.python3Packages.pillow && INSTALLED=1 || true
            fi
        fi
    fi

    if [ "$INSTALLED" -eq 0 ]; then
        echo -e "${YELLOW}${MSG_FAIL}${NC}"
        echo "${MSG_FAIL_HINT}"
        echo "  • Android (Termux): pkg install python-pillow"
        echo "  • Fedora/RHEL:      sudo dnf install python3-pillow"
        echo "  • Debian/Ubuntu:    sudo apt install python3-pil"
        echo "  • Arch Linux:       yay -S python-pillow (o: sudo pacman -S python-pillow)"
        echo "  • openSUSE:         sudo zypper install python3-Pillow"
        echo "  • Void Linux:       sudo xbps-install -S python3-Pillow"
        echo "  • Alpine Linux:     sudo apk add py3-pillow"
        echo "  • Gentoo Linux:     sudo emerge --ask dev-python/pillow"
        echo "  • NixOS / Nix:      nix-env -iA nixpkgs.python3Packages.pillow"
    fi
fi

# 5. Create launcher wrappers in INSTALL_DIR
echo -e "${MSG_FORGING}"

PY_EXEC="python3"
if [ -f "$SHARE_DIR/venv/bin/python" ]; then
    PY_EXEC="$SHARE_DIR/venv/bin/python"
fi

rm -f "$INSTALL_DIR/lumart" "$INSTALL_DIR/luma"
BASH_BIN="$(command -v bash 2>/dev/null || command -v sh 2>/dev/null || echo "/bin/sh")"
cat << EOF_WRAPPER > "$INSTALL_DIR/lumart"
#!$BASH_BIN
exec "$PY_EXEC" "$SHARE_DIR/lumart.py" "\$@"
EOF_WRAPPER

chmod +x "$INSTALL_DIR/lumart"
ln -sf "$INSTALL_DIR/lumart" "$INSTALL_DIR/luma"

if command -v termux-fix-shebang &>/dev/null; then
    termux-fix-shebang "$INSTALL_DIR/lumart" 2>/dev/null || true
fi

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
if [ -d "$SCRIPT_DIR/completions" ]; then
    mkdir -p "$SHARE_DIR/completions" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/completions/"* "$SHARE_DIR/completions/" 2>/dev/null || true
else
    mkdir -p "$SHARE_DIR/completions" 2>/dev/null || true
    curl -fsSL "$RAW_BASE/completions/lumart.bash" -o "$SHARE_DIR/completions/lumart.bash" 2>/dev/null || true
    curl -fsSL "$RAW_BASE/completions/_lumart" -o "$SHARE_DIR/completions/_lumart" 2>/dev/null || true
    curl -fsSL "$RAW_BASE/completions/lumart.fish" -o "$SHARE_DIR/completions/lumart.fish" 2>/dev/null || true
fi

if [ -f "$SCRIPT_DIR/man/lumart.1" ]; then
    mkdir -p "$SHARE_DIR/man" 2>/dev/null || true
    cp "$SCRIPT_DIR/man/lumart.1" "$SHARE_DIR/man/lumart.1" 2>/dev/null || true
else
    mkdir -p "$SHARE_DIR/man" 2>/dev/null || true
    curl -fsSL "$RAW_BASE/man/lumart.1" -o "$SHARE_DIR/man/lumart.1" 2>/dev/null || true
fi

if [ "$IS_TERMUX" -eq 1 ] && [ -n "${PREFIX:-}" ] && [ -d "$PREFIX/share" ]; then
    BASH_COMP_DIR="$PREFIX/share/bash-completion/completions"
    ZSH_COMP_DIR="$PREFIX/share/zsh/site-functions"
    FISH_COMP_DIR="$PREFIX/share/fish/vendor_completions.d"
    MAN_DIR="$PREFIX/share/man/man1"
elif [ "$EUID" -eq 0 ]; then
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

if [ -f "$SHARE_DIR/completions/lumart.bash" ]; then
    mkdir -p "$BASH_COMP_DIR" 2>/dev/null || true
    cp "$SHARE_DIR/completions/lumart.bash" "$BASH_COMP_DIR/lumart" 2>/dev/null || true
    ln -sf lumart "$BASH_COMP_DIR/luma" 2>/dev/null || true
fi
if [ -f "$SHARE_DIR/completions/_lumart" ]; then
    mkdir -p "$ZSH_COMP_DIR" 2>/dev/null || true
    cp "$SHARE_DIR/completions/_lumart" "$ZSH_COMP_DIR/_lumart" 2>/dev/null || true
    ln -sf _lumart "$ZSH_COMP_DIR/_luma" 2>/dev/null || true
    if [ "$EUID" -ne 0 ] && [ "$IS_TERMUX" -ne 1 ]; then
        mkdir -p "$HOME/.zsh/completion" 2>/dev/null || true
        cp "$SHARE_DIR/completions/_lumart" "$HOME/.zsh/completion/_lumart" 2>/dev/null || true
        ln -sf _lumart "$HOME/.zsh/completion/_luma" 2>/dev/null || true
    fi
fi
if [ -f "$SHARE_DIR/completions/lumart.fish" ]; then
    mkdir -p "$FISH_COMP_DIR" 2>/dev/null || true
    cp "$SHARE_DIR/completions/lumart.fish" "$FISH_COMP_DIR/lumart.fish" 2>/dev/null || true
    ln -sf lumart.fish "$FISH_COMP_DIR/luma.fish" 2>/dev/null || true
fi
if [ -f "$SHARE_DIR/man/lumart.1" ]; then
    mkdir -p "$MAN_DIR" 2>/dev/null || true
    cp "$SHARE_DIR/man/lumart.1" "$MAN_DIR/lumart.1" 2>/dev/null || true
    ln -sf lumart.1 "$MAN_DIR/luma.1" 2>/dev/null || true
    if command -v mandb &>/dev/null; then
        mandb -q "$MAN_DIR/.." 2>/dev/null || true
    fi
fi

# 6. Verify installation execution & PATH
INSTALL_VERIFIED=0
if [ -x "$INSTALL_DIR/lumart" ]; then
    if "$INSTALL_DIR/lumart" --version &>/dev/null; then
        INSTALL_VERIFIED=1
    fi
fi

if [ "$INSTALL_VERIFIED" -eq 1 ]; then
    echo -e "\n${GREEN}${MSG_SUCCESS}${NC}"
    echo -e "${MSG_READY}\n"
else
    if [ "$LANG_MODE" = "es" ]; then
        echo -e "\n${YELLOW}⚠️  Luma se instaló pero la verificación de ejecución reportó un aviso.${NC}"
        echo "Prueba ejecutar directamente: $INSTALL_DIR/lumart --version"
    else
        echo -e "\n${YELLOW}⚠️  Luma was installed but execution verification reported a warning.${NC}"
        echo "Try executing directly: $INSTALL_DIR/lumart --version"
    fi
fi

IN_PATH=0
case ":$PATH:" in
    *":$INSTALL_DIR:"*) IN_PATH=1 ;;
esac

if [ "$IN_PATH" -eq 0 ]; then
    echo -e "${YELLOW}${MSG_PATH_WARN/INSTALL_DIR/$INSTALL_DIR}${NC}"
    echo "${MSG_PATH_HINT}"
    echo -e "  ${CYAN}export PATH=\"$INSTALL_DIR:\$PATH\"${NC}\n"
    for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
        if [ -f "$rc" ] && ! grep -q "$INSTALL_DIR" "$rc"; then
            echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$rc"
            if [ "$LANG_MODE" = "es" ]; then
                echo -e "${GREEN}✓ Se ha agregado $INSTALL_DIR a $rc${NC}"
            else
                echo -e "${GREEN}✓ Added $INSTALL_DIR to $rc${NC}"
            fi
        fi
    done
fi

echo -e "${MSG_UPDATE_HINT}\n"
echo "${MSG_TEST}"
echo "  luma --help"
echo "  luma -u"
echo "  luma -uu"
echo "  luma -dg"
echo "  luma /path/to/image.png"
