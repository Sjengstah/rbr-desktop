#!/usr/bin/env bash
# Install the RBR icon theme for the current user (no root needed).
# Select it in System Settings > Colors & Themes > Icons.
set -euo pipefail
cd "$(dirname "$0")"
dest="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
mkdir -p "$dest"
rm -rf "$dest/RBR"
cp -r RBR "$dest/"
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -f -t "$dest/RBR" >/dev/null 2>&1 || true
echo "RBR icons installed to $dest/RBR"
