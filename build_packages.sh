#!/bin/bash
set -e

VERSION="2.1.0"

echo "=== Building lumart v$VERSION ==="
# Generación del binario autónomo con PyInstaller
echo "Compiling with PyInstaller..."
pyinstaller --onefile --name lumart lumart.py

# DEB: para sistemas basados en Debian / Ubuntu
echo "=== Creating DEB package ==="
mkdir -p build/deb/lumart-$VERSION/usr/bin
cp dist/lumart build/deb/lumart-$VERSION/usr/bin/
ln -sf lumart build/deb/lumart-$VERSION/usr/bin/luma
mkdir -p build/deb/lumart-$VERSION/DEBIAN
cat << EOF > build/deb/lumart-$VERSION/DEBIAN/control
Package: lumart
Version: $VERSION
Architecture: amd64
Maintainer: Trixie
Description: Epic Terminal Art Engine (Color Swap & Neofetch OS Style)
EOF
dpkg-deb --build build/deb/lumart-$VERSION
mv build/deb/lumart-$VERSION.deb dist/

# RPM: para distribuciones Fedora / RHEL / openSUSE
echo "=== Creating RPM package ==="
if command -v rpmbuild &>/dev/null; then
    mkdir -p build/rpm/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    cat << EOF > build/rpm/rpmbuild/SPECS/lumart.spec
Name:           lumart
Version:        $VERSION
Release:        1
Summary:        Epic Terminal Art Engine
License:        AGPL
%description
Epic Terminal Art Engine (Color Swap & Neofetch OS Style)
%install
mkdir -p %{buildroot}/usr/bin
cp %{_sourcedir}/lumart %{buildroot}/usr/bin/
ln -sf lumart %{buildroot}/usr/bin/luma
%files
/usr/bin/lumart
/usr/bin/luma
EOF
    cp dist/lumart build/rpm/rpmbuild/SOURCES/
    rpmbuild --define "_topdir $(pwd)/build/rpm/rpmbuild" -bb build/rpm/rpmbuild/SPECS/lumart.spec
    find build/rpm/rpmbuild/RPMS -name "*.rpm" -exec cp {} dist/ \;
else
    echo "⚠️  'rpmbuild' not found. Skipping RPM package generation. (Install 'rpm-build' on Fedora/RHEL to build RPMs)."
fi

# Arch Linux: (por cierto, uso Arch)
echo "=== Creating Arch Linux PKGBUILD ==="
mkdir -p dist/arch
cat << EOF > dist/arch/PKGBUILD
pkgname=lumart-bin
pkgver=$VERSION
pkgrel=1
pkgdesc="Epic Terminal Art Engine (Color Swap & Neofetch OS Style)"
arch=('x86_64')
license=('AGPL')
source=("lumart")
sha256sums=('SKIP')
package() {
    install -Dm755 "\$srcdir/lumart" "\$pkgdir/usr/bin/lumart"
    ln -sf lumart "\$pkgdir/usr/bin/luma"
}
EOF
cp dist/lumart dist/arch/

echo "=== DONE! ==="
echo "All packages are ready in the 'dist' folder:"
ls -lh dist/
