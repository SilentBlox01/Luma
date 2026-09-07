#!/bin/bash
# ==============================================================================
# Luma / Lumart Uninstaller Script / Desinstalador Completo
# ==============================================================================

echo "🧹 Uninstalling Luma..."

# 1. Remove global binaries and share dir (if installed with sudo / root)
if [ -f "/usr/local/bin/lumart" ] || [ -d "/usr/local/share/luma" ]; then
    echo "Removing global files from /usr/local..."
    sudo rm -f /usr/local/bin/lumart /usr/local/bin/luma /usr/local/bin/luma-mono /usr/local/bin/luma-mary
    sudo rm -rf /usr/local/share/luma
    echo "  ✅ Removed global installation in /usr/local"
fi

if [ -f "/usr/bin/lumart" ]; then
    echo "ℹ️ Luma was detected in /usr/bin (installed via package manager)."
    echo "To remove it via your distribution package manager, run:"
    echo "  • Debian/Ubuntu: sudo apt remove lumart"
    echo "  • Fedora/RHEL:   sudo dnf remove lumart"
    echo "  • Arch Linux:    sudo pacman -Rns lumart"
fi

# 2. Remove user local binaries and shared data
if [ -f "$HOME/.local/bin/lumart" ] || [ -f "$HOME/.local/bin/luma" ] || [ -d "$HOME/.local/share/luma" ]; then
    rm -f "$HOME/.local/bin/lumart" "$HOME/.local/bin/luma" "$HOME/.local/bin/luma-mono" "$HOME/.local/bin/luma-mary"
    rm -rf "$HOME/.local/share/luma"
    echo "  ✅ Removed user binaries and engines from ~/.local"
fi

# 3. Remove desktop launcher and file manager scripts
DESKTOP_ENTRY="$HOME/.local/share/applications/lumart.desktop"
if [ -f "$DESKTOP_ENTRY" ]; then
    rm -f "$DESKTOP_ENTRY"
    if command -v update-desktop-database &>/dev/null; then
        update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    fi
    echo "  ✅ Removed desktop launcher"
fi

rm -f "$HOME/.local/share/nautilus/scripts/Abrir con Lumart"
rm -f "$HOME/.local/share/nemo/scripts/Abrir con Lumart"
echo "  ✅ Removed file manager context scripts"

echo "✨ Luma has been completely uninstalled from your system."
