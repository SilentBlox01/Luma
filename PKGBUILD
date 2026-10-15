# Maintainer: SilentBlox_01 <silentblox@users.noreply.github.com>
pkgname=lumart
pkgver=2.5.1
pkgrel=1
pkgdesc="Modern Terminal Visual Suite (Mary Apex 3.5, Trumble Orelx 2.2, Luris Mono 2.6, Spectra Weep 2.0)"
arch=('x86_64' 'aarch64')
url="https://github.com/SilentBlox01/Luma"
license=('AGPL-3.0-or-later')
depends=('python' 'python-pillow')
optdepends=(
    'opencv: Real-time video and webcam streaming (Spectra Weep 2.0)'
    'gcc: Native C++17 OpenMP SIMD acceleration'
    'wl-clipboard: Clipboard support on Wayland (-C / --copy)'
    'xclip: Clipboard support on X11 (-C / --copy)'
)
provides=('lumart' 'luma')
conflicts=('lumart-bin' 'luma')

build() {
    cd "$startdir" || cd "$srcdir"
    if command -v g++ &>/dev/null; then
        g++ -O3 -march=native -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so 2>/dev/null ||         g++ -O3 -std=c++17 -fopenmp -fPIC -shared mary.cpp -o libmary.so 2>/dev/null || true

        g++ -O3 -march=native -std=c++17 -fopenmp -fPIC -shared monochrome.cpp -o libmonochrome.so 2>/dev/null ||         g++ -O3 -std=c++17 -fopenmp -fPIC -shared monochrome.cpp -o libmonochrome.so 2>/dev/null || true

        g++ -O3 -march=native -std=c++17 -fopenmp mary.cpp -o luma-mary 2>/dev/null || true
        g++ -O3 -march=native -std=c++17 -fopenmp monochrome.cpp -o luma-mono 2>/dev/null || true
    fi
}

package() {
    cd "$startdir" || cd "$srcdir"
    install -d "$pkgdir/usr/share/luma"
    install -Dm755 lumart.py "$pkgdir/usr/share/luma/lumart.py"
    [ -f mary.py ] && install -Dm644 mary.py "$pkgdir/usr/share/luma/mary.py"
    [ -f trumble.py ] && install -Dm644 trumble.py "$pkgdir/usr/share/luma/trumble.py"
    [ -f VERSION ] && install -Dm644 VERSION "$pkgdir/usr/share/luma/VERSION"
    [ -d locales ] && cp -r locales "$pkgdir/usr/share/luma/"

    install -d "$pkgdir/usr/bin"
    cat << 'EOF_WRAPPER' > "$pkgdir/usr/bin/lumart"
#!/bin/bash
exec /usr/bin/python3 /usr/share/luma/lumart.py "$@"
EOF_WRAPPER
    chmod +x "$pkgdir/usr/bin/lumart"
    ln -sf lumart "$pkgdir/usr/bin/luma"

    if [ -f luma-mono ]; then
        install -Dm755 luma-mono "$pkgdir/usr/bin/luma-mono"
    fi
    if [ -f luma-mary ]; then
        install -Dm755 luma-mary "$pkgdir/usr/bin/luma-mary"
    fi
    if [ -f libmonochrome.so ]; then
        install -Dm755 libmonochrome.so "$pkgdir/usr/lib/libmonochrome.so"
        install -Dm755 libmonochrome.so "$pkgdir/usr/share/luma/libmonochrome.so"
    fi
    if [ -f libmary.so ]; then
        install -Dm755 libmary.so "$pkgdir/usr/lib/libmary.so"
        install -Dm755 libmary.so "$pkgdir/usr/share/luma/libmary.so"
    fi

    # Shell Completions
    install -Dm644 completions/lumart.bash "$pkgdir/usr/share/bash-completion/completions/lumart"
    ln -sf lumart "$pkgdir/usr/share/bash-completion/completions/luma"
    install -Dm644 completions/_lumart "$pkgdir/usr/share/zsh/site-functions/_lumart"
    ln -sf _lumart "$pkgdir/usr/share/zsh/site-functions/_luma"
    install -Dm644 completions/lumart.fish "$pkgdir/usr/share/fish/vendor_completions.d/lumart.fish"
    ln -sf lumart.fish "$pkgdir/usr/share/fish/vendor_completions.d/luma.fish"

    # UNIX Man page
    install -Dm644 man/lumart.1 "$pkgdir/usr/share/man/man1/lumart.1"
    ln -sf lumart.1 "$pkgdir/usr/share/man/man1/luma.1"
}
