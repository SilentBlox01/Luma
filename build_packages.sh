#!/bin/bash
set -e

VERSION="2.0.0"

echo "=== Building lumart v$VERSION ==="
echo "Compiling with PyInstaller..."
pyinstaller --onefile --name lumart lumart.py

echo "=== Creating DEB package ==="
mkdir -p build/deb/lumart-$VERSION/usr/bin
cp dist/lumart build/deb/lumart-$VERSION/usr/bin/
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

echo "=== Creating RPM package ==="
mkdir -p build/rpm/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cat << EOF > build/rpm/rpmbuild/SPECS/lumart.spec
Name:           lumart
Version:        $VERSION
Release:        1
Summary:        Epic Terminal Art Engine
License:        MIT
%description
Epic Terminal Art Engine (Color Swap & Neofetch OS Style)
%install
mkdir -p %{buildroot}/usr/bin
cp %{_sourcedir}/lumart %{buildroot}/usr/bin/
%files
/usr/bin/lumart
EOF
cp dist/lumart build/rpm/rpmbuild/SOURCES/
rpmbuild --define "_topdir $(pwd)/build/rpm/rpmbuild" -bb build/rpm/rpmbuild/SPECS/lumart.spec
find build/rpm/rpmbuild/RPMS -name "*.rpm" -exec cp {} dist/ \;

echo "=== Creating Arch Linux PKGBUILD ==="
mkdir -p dist/arch
cat << EOF > dist/arch/PKGBUILD
pkgname=lumart-bin
pkgver=$VERSION
pkgrel=1
pkgdesc="Epic Terminal Art Engine (Color Swap & Neofetch OS Style)"
arch=('x86_64')
license=('MIT')
source=("lumart")
sha256sums=('SKIP')
package() {
    install -Dm755 "\$srcdir/lumart" "\$pkgdir/usr/bin/lumart"
}
EOF
cp dist/lumart dist/arch/

echo "=== DONE! ==="
echo "All packages are ready in the 'dist' folder:"
ls -lh dist/
