#!/bin/bash
set -e

# Detect version dynamically from lumart.py
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"
LUMA_VERSION=$(grep -m1 -oP 'VERSION\s*=\s*"\K[^"]+' "$SCRIPT_DIR/lumart.py" 2>/dev/null || echo "2.1.2")

TARGET="auto"
for arg in "$@"; do
    case "$arg" in
        --all) TARGET="all" ;;
        --deb) TARGET="deb" ;;
        --rpm) TARGET="rpm" ;;
        --arch) TARGET="arch" ;;
        --help|-h)
            echo "Usage: ./build_packages.sh [OPTIONS]"
            echo "Options:"
            echo "  (no args)  Auto-detect host Linux distribution and build only the matching package"
            echo "  --deb      Build only Debian/Ubuntu (.deb) package"
            echo "  --rpm      Build only Fedora/RHEL/openSUSE (.rpm) package"
            echo "  --arch     Build only Arch Linux PKGBUILD"
            echo "  --all      Build all packages (for release maintainers)"
            exit 0
            ;;
    esac
done

# Distro Auto-Detection
if [ "$TARGET" = "auto" ]; then
    OS_ID=""
    OS_LIKE=""
    if [ -f /etc/os-release ]; then
        # Subshell to prevent polluting our own script variables (like VERSION)
        eval "$(grep -E '^(ID|ID_LIKE)=' /etc/os-release)"
        OS_ID="${ID:-}"
        OS_LIKE="${ID_LIKE:-}"
    fi

    if [[ "$OS_ID" =~ ^(debian|ubuntu|linuxmint|pop|kali|elementary)$ ]] || [[ "$OS_LIKE" =~ (debian|ubuntu) ]] || command -v dpkg-deb &>/dev/null; then
        TARGET="deb"
        echo "🔍 Detected Debian/Ubuntu ecosystem ($OS_ID). Building only .deb package."
    elif [[ "$OS_ID" =~ ^(fedora|rhel|centos|rocky|almalinux|opensuse.*|suse)$ ]] || [[ "$OS_LIKE" =~ (fedora|rhel|suse) ]]; then
        TARGET="rpm"
        echo "🔍 Detected Fedora/RHEL/openSUSE ecosystem ($OS_ID). Building only .rpm package."
    elif [[ "$OS_ID" =~ ^(arch|manjaro|endeavouros|artix)$ ]] || [[ "$OS_LIKE" =~ arch ]] || command -v pacman &>/dev/null; then
        TARGET="arch"
        echo "🔍 Detected Arch Linux ecosystem ($OS_ID). Building only Arch PKGBUILD."
    else
        TARGET="binary"
        echo "🔍 Unknown Linux distribution. Building standalone binary only."
    fi
fi

echo "=== Building lumart v$LUMA_VERSION ==="
echo "Compiling standalone binary with PyInstaller..."
pyinstaller --clean --onefile --name lumart "$SCRIPT_DIR/lumart.py"

mkdir -p dist

if command -v g++ &>/dev/null && [ -f "$SCRIPT_DIR/monochrome.cpp" ]; then
    echo "Compiling native C++ monochrome engine (luma-mono)..."
    g++ -O3 -std=c++17 -I"$SCRIPT_DIR" "$SCRIPT_DIR/monochrome.cpp" -o dist/luma-mono
    g++ -O3 -std=c++17 -fPIC -shared -I"$SCRIPT_DIR" "$SCRIPT_DIR/monochrome.cpp" -o dist/libmonochrome.so
fi

# 1. DEB Package
if [ "$TARGET" = "deb" ] || [ "$TARGET" = "all" ]; then
    echo "=== Creating DEB package ==="
    rm -rf "build/deb/lumart-$LUMA_VERSION"
    mkdir -p "build/deb/lumart-$LUMA_VERSION/usr/bin"
    cp dist/lumart "build/deb/lumart-$LUMA_VERSION/usr/bin/"
    ln -sf lumart "build/deb/lumart-$LUMA_VERSION/usr/bin/luma"
    if [ -f "dist/luma-mono" ]; then
        cp dist/luma-mono "build/deb/lumart-$LUMA_VERSION/usr/bin/"
    fi
    if [ -f "dist/libmonochrome.so" ]; then
        mkdir -p "build/deb/lumart-$LUMA_VERSION/usr/lib"
        cp dist/libmonochrome.so "build/deb/lumart-$LUMA_VERSION/usr/lib/"
    fi
    mkdir -p "build/deb/lumart-$LUMA_VERSION/DEBIAN"
    cat << EOF > "build/deb/lumart-$LUMA_VERSION/DEBIAN/control"
Package: lumart
Version: $LUMA_VERSION
Architecture: amd64
Maintainer: SilentBlox_01
Description: High-Fidelity Terminal Art Engine (Color Swap, Neofetch OS Style & Native C++ B&W Engine)
EOF
    # Use --root-owner-group to prevent owner warning
    dpkg-deb --root-owner-group --build "build/deb/lumart-$LUMA_VERSION"
    mv "build/deb/lumart-$LUMA_VERSION.deb" dist/
    ln -sf "lumart-$LUMA_VERSION.deb" "dist/lumart.deb"
fi

# 2. RPM Package
if [ "$TARGET" = "rpm" ] || [ "$TARGET" = "all" ]; then
    echo "=== Creating RPM package ==="
    if command -v rpmbuild &>/dev/null; then
        mkdir -p build/rpm/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
        
        EXTRA_FILES=""
        if [ -f "dist/luma-mono" ]; then
            cp dist/luma-mono build/rpm/rpmbuild/SOURCES/
            EXTRA_FILES="${EXTRA_FILES}\n/usr/bin/luma-mono"
        fi
        if [ -f "dist/libmonochrome.so" ]; then
            cp dist/libmonochrome.so build/rpm/rpmbuild/SOURCES/
            EXTRA_FILES="${EXTRA_FILES}\n/usr/lib/libmonochrome.so"
        fi

        cat << EOF > build/rpm/rpmbuild/SPECS/lumart.spec
Name:           lumart
Version:        $LUMA_VERSION
Release:        1
Summary:        High-Fidelity Terminal Art Engine
License:        AGPL-3.0
%description
High-Fidelity Terminal Art Engine (Dual-Engine, Manga 2.0 & Color Swap)
%install
mkdir -p %{buildroot}/usr/bin
cp %{_sourcedir}/lumart %{buildroot}/usr/bin/
ln -sf lumart %{buildroot}/usr/bin/luma
if [ -f "%{_sourcedir}/luma-mono" ]; then
    cp %{_sourcedir}/luma-mono %{buildroot}/usr/bin/
fi
if [ -f "%{_sourcedir}/libmonochrome.so" ]; then
    mkdir -p %{buildroot}/usr/lib
    cp %{_sourcedir}/libmonochrome.so %{buildroot}/usr/lib/
fi
%files
/usr/bin/lumart
/usr/bin/luma
$(echo -e "$EXTRA_FILES")
EOF
        cp dist/lumart build/rpm/rpmbuild/SOURCES/
        rpmbuild --define "_topdir $(pwd)/build/rpm/rpmbuild" -bb build/rpm/rpmbuild/SPECS/lumart.spec
        find build/rpm/rpmbuild/RPMS -name "*.rpm" -exec cp {} dist/ \;
        RPM_FILE=$(find dist -maxdepth 1 -name "lumart-$LUMA_VERSION-*.rpm" | head -n 1)
        [ -n "$RPM_FILE" ] && ln -sf "$(basename "$RPM_FILE")" "dist/lumart.rpm"
    else
        echo "⚠️  'rpmbuild' not found. (Install 'rpm-build' on Fedora/RHEL to build RPMs)."
    fi
fi

# 3. Arch Linux PKGBUILD
if [ "$TARGET" = "arch" ] || [ "$TARGET" = "all" ]; then
    echo "=== Creating Arch Linux PKGBUILD ==="
    mkdir -p dist/arch
    cat << EOF > dist/arch/PKGBUILD
# Maintainer: SilentBlox_01
pkgname=lumart-bin
pkgver=$LUMA_VERSION
pkgrel=1
pkgdesc="High-Fidelity Terminal Art Engine (Dual-Engine, Manga 2.0 & Color Swap)"
arch=('x86_64')
url="https://github.com/SilentBlox01/Luma"
license=('AGPL-3.0')
source=("lumart")
sha256sums=('SKIP')
package() {
    install -Dm755 "\$srcdir/lumart" "\$pkgdir/usr/bin/lumart"
    ln -sf lumart "\$pkgdir/usr/bin/luma"
    if [ -f "\$srcdir/luma-mono" ]; then
        install -Dm755 "\$srcdir/luma-mono" "\$pkgdir/usr/bin/luma-mono"
    fi
    if [ -f "\$srcdir/libmonochrome.so" ]; then
        install -Dm755 "\$srcdir/libmonochrome.so" "\$pkgdir/usr/lib/libmonochrome.so"
    fi
}
EOF
    cp dist/lumart dist/arch/
    [ -f "dist/luma-mono" ] && cp dist/luma-mono dist/arch/
    [ -f "dist/libmonochrome.so" ] && cp dist/libmonochrome.so dist/arch/
fi

# 4. Universal Linux Portable Archive (.tar.gz)
echo "=== Creating Universal Linux Tarball ==="
TAR_NAME="lumart-$LUMA_VERSION-linux-x86_64"
rm -rf "build/$TAR_NAME"
mkdir -p "build/$TAR_NAME"
cp dist/lumart "build/$TAR_NAME/"
ln -sf lumart "build/$TAR_NAME/luma"
[ -f "dist/luma-mono" ] && cp dist/luma-mono "build/$TAR_NAME/"
[ -f "dist/libmonochrome.so" ] && cp dist/libmonochrome.so "build/$TAR_NAME/"
[ -f "install.sh" ] && cp install.sh "build/$TAR_NAME/"
[ -f "README.md" ] && cp README.md "build/$TAR_NAME/"
[ -f "LICENSE" ] && cp LICENSE "build/$TAR_NAME/"
tar -czf "dist/$TAR_NAME.tar.gz" -C build "$TAR_NAME"
ln -sf "$TAR_NAME.tar.gz" "dist/lumart-linux-x86_64.tar.gz"

echo -e "\n=== DONE! ==="
echo "Artifacts ready in 'dist/':"
ls -lh dist/

echo -e "\n💡 How to install on this system:"
if [ "$TARGET" = "deb" ]; then
    echo "  sudo apt install ./dist/lumart-$LUMA_VERSION.deb"
    echo "  (or: sudo apt install ./dist/lumart.deb)"
elif [ "$TARGET" = "rpm" ]; then
    echo "  sudo dnf install ./dist/lumart-$LUMA_VERSION-*.rpm"
elif [ "$TARGET" = "arch" ]; then
    echo "  cd dist/arch && makepkg -si"
else
    echo "  sudo cp dist/lumart /usr/local/bin/"
    echo "  sudo ln -sf /usr/local/bin/lumart /usr/local/bin/luma"
fi
