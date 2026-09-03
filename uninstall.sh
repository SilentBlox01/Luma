#!/bin/bash
# Luma Uninstaller Script
# This script removes Luma if it was installed manually (outside of a package manager).

echo "Uninstalling Luma..."

# Remove global binaries
if [ -f "/usr/local/bin/lumart" ]; then
    sudo rm -f /usr/local/bin/lumart
    sudo rm -f /usr/local/bin/luma
    echo "Removed from /usr/local/bin"
fi

if [ -f "/usr/bin/lumart" ]; then
    echo "Luma was installed via a package manager (apt/dnf)."
    echo "Please use your package manager to remove it:"
    echo "  Debian/Ubuntu: sudo apt remove lumart"
    echo "  Fedora/RHEL:   sudo dnf remove lumart"
    echo "  Arch Linux:    sudo pacman -Rns lumart"
fi

# Remove local binaries
if [ -f "$HOME/.local/bin/lumart" ] || [ -f "$HOME/.local/bin/luma" ]; then
    rm -f "$HOME/.local/bin/lumart"
    rm -f "$HOME/.local/bin/luma"
    echo "Removed from ~/.local/bin"
fi

echo "Done!"
