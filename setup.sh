#!/usr/bin/env bash
# RBR desktop: install the RBR look on KDE Plasma 6.
#
# WARNING: largely AI-generated ("vibe coded"). Read it before you run it.
# No support, no warranty — see README.md.
#
#   ./setup.sh              interactive (asks before changing anything)
#   ./setup.sh --yes        no questions
#   ./setup.sh --dry-run    show what would happen, change nothing
#
# Run it as your normal user inside a Plasma 6 Wayland session. It never uses
# sudo: everything goes into your home folder. Missing system packages are only
# listed (see Requirements in README.md); you install those yourself.
set -euo pipefail

KIT="$(cd "$(dirname "$0")" && pwd)"
PAYLOAD="$KIT/payload"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

YES=false
DRY=false
for arg in "$@"; do
    case "$arg" in
        --yes|-y) YES=true ;;
        --dry-run|-n) DRY=true ;;
        -h|--help) sed -n '2,/^set -euo/{/^#/p}' "$0"; exit 0 ;;
        *) echo "Unknown option: $arg" >&2; exit 1 ;;
    esac
done

orange=$'\e[38;2;219;10;64m'; lilac=$'\e[38;2;143;174;245m'; red=$'\e[38;2;255;90;95m'; off=$'\e[0m'
step() { printf '\n%s▌ %s%s\n' "$orange" "$*" "$off"; }
info() { printf '  %s\n' "$*"; }
warn() { printf '  %s! %s%s\n' "$red" "$*" "$off"; }
run() { if $DRY; then printf '  %s[dry-run]%s %s\n' "$lilac" "$off" "$*"; else "$@"; fi; }

# ── Preflight ───────────────────────────────────────────────────────
step "RBR desktop — preflight"
[[ -d "$PAYLOAD" ]] || { warn "payload/ is missing next to setup.sh"; exit 1; }
[[ "${XDG_CURRENT_DESKTOP:-}" == *KDE* ]] || warn "This doesn't look like a KDE session (XDG_CURRENT_DESKTOP=${XDG_CURRENT_DESKTOP:-unset})."
[[ "${XDG_SESSION_TYPE:-}" == "wayland" ]] || warn "Not a Wayland session: the audio overlay and RBR popups need Wayland."
command -v plasmashell >/dev/null || { warn "plasmashell not found: install KDE Plasma first."; exit 1; }
info "Plasma: $(plasmashell --version 2>/dev/null)"
. /etc/os-release 2>/dev/null || true
info "System: ${PRETTY_NAME:-unknown}"

cat <<EOF

  This will:
   1. check the required packages (it lists missing ones, it never installs them)
   2. install the Barlow Condensed font, the RBR icon theme and the RBR global theme
      (kora icons / WhiteSur cursors are used if you already have them)
   3. detect this machine's hardware and set up the RBR widgets for it
   4. install the RBR widgets, audio overlay (Meta+G), RBR fastfetch and helper commands
   5. apply the RBR theme, and REPLACE the panels on the primary screen
      with the RBR panels, widgets and hotkeys
   6. make GTK and Flatpak apps follow the theme

  Your current settings are backed up first.
EOF
if ! $YES && ! $DRY; then
    read -r -p "  Continue? [y/N] " answer
    [[ "$answer" =~ ^[Yy] ]] || { echo "  Cancelled."; exit 0; }
fi

# ── 0. Backup ───────────────────────────────────────────────────────
step "Backing up current settings"
BACKUP="$CONF/rbr-kit-backup-$(date +%Y%m%d-%H%M%S)"
run mkdir -p "$BACKUP"
for f in kdeglobals kwinrc plasmarc ksplashrc kcminputrc plasmashellrc kglobalshortcutsrc \
         plasma-org.kde.plasma.desktop-appletsrc plasmanotifyrc gtk-3.0/settings.ini gtk-4.0/gtk.css \
         fastfetch/config.jsonc; do
    if [[ -f "$CONF/$f" ]]; then run install -D -m600 "$CONF/$f" "$BACKUP/$f"; fi
done
info "Backup: $BACKUP"

# ── 1. Requirements (checked only, never installed) ─────────────────
step "Checking requirements"
MISSING=()
if command -v pacman >/dev/null; then
    wanted=(qt6-declarative layer-shell-qt plasma-pa kirigami kitemmodels bluez-qt bluedevil plasma-nm
            powerdevil libksysguard ksystemstats libarchive fastfetch libnotify)
    for p in "${wanted[@]}"; do pacman -Q "$p" >/dev/null 2>&1 || MISSING+=("$p"); done
    pacman -Q power-profiles-daemon >/dev/null 2>&1 || pacman -Q tuned-ppd >/dev/null 2>&1 || MISSING+=(power-profiles-daemon)
    INSTALL_CMD="sudo pacman -S --needed"
elif command -v rpm >/dev/null; then
    wanted=(qt6-qtdeclarative layer-shell-qt plasma-pa kf6-kirigami kf6-kitemmodels kf6-bluez-qt bluedevil
            plasma-nm powerdevil libksysguard ksystemstats bsdtar power-profiles-daemon fastfetch libnotify)
    for p in "${wanted[@]}"; do rpm -q "$p" >/dev/null 2>&1 || MISSING+=("$p"); done
    INSTALL_CMD="sudo dnf install"
else
    warn "Unknown distro: check the requirements list in README.md yourself."
fi
if (( ${#MISSING[@]} )); then
    warn "Missing (this script does not install packages): ${MISSING[*]}"
    info "Install them yourself if you want the parts that need them (see README.md):"
    info "  $INSTALL_CMD ${MISSING[*]}"
    if ! $YES && ! $DRY; then
        read -r -p "  Continue without them? [y/N] " answer
        [[ "$answer" =~ ^[Yy] ]] || { echo "  Cancelled. Install them, then run setup.sh again."; exit 0; }
    fi
else
    info "All requirements present."
fi
command -v qml6 >/dev/null || command -v qml-qt6 >/dev/null || [[ -x /usr/lib64/qt6/bin/qml ]] || \
    warn "Qt 6 QML runtime not found: the audio overlay needs it (see README)."

# ── 2. Fonts, icons, theme ──────────────────────────────────────────
step "Fonts, icons and theme"
run install -Dm644 "$PAYLOAD/projects/rbr-monitor/package/contents/fonts/BarlowCondensed-SemiBoldItalic.ttf" "$DATA/fonts/BarlowCondensed-SemiBoldItalic.ttf"
run fc-cache -f "$DATA/fonts"
run mkdir -p "$DATA/icons"
for theme in kora WhiteSur-cursors; do
    if [[ -d "$PAYLOAD/icons/$theme" ]]; then
        run rm -rf "$DATA/icons/$theme"
        run cp -a "$PAYLOAD/icons/$theme" "$DATA/icons/"
        info "icons: $theme"
    fi
done
icons_found() { [[ -d "$DATA/icons/$1" || -d "$HOME/.icons/$1" || -d "/usr/share/icons/$1" ]]; }
icons_found kora || warn "kora icons not found (optional): https://github.com/bikass/kora"
icons_found WhiteSur-cursors || warn "WhiteSur cursors not found (optional): https://github.com/vinceliuice/WhiteSur-cursors"
run "$PAYLOAD/projects/rbr-icons/install.sh"
run "$PAYLOAD/projects/rbr-theme/install.sh"
run install -Dm755 "$PAYLOAD/bin/panel-opacity" "$HOME/.local/bin/panel-opacity"

# RBR fastfetch (shown on every new terminal by CachyOS's fish greeting) and fish helpers
if [[ -d "$PAYLOAD/fastfetch" ]]; then
    for f in "$PAYLOAD"/fastfetch/*; do run install -Dm644 "$f" "$CONF/fastfetch/$(basename "$f")"; done
    info "fastfetch: RBR config"
fi
if [[ -d "$PAYLOAD/fish" ]]; then
    for f in "$PAYLOAD"/fish/*.fish; do run install -Dm644 "$f" "$CONF/fish/functions/$(basename "$f")"; done
    info "fish: rbr-test, rbr-fetch"
fi

# ── 3. Hardware ─────────────────────────────────────────────────────
step "Detecting hardware"
if $DRY; then
    python3 "$KIT/lib/detect-hardware.py" "$PAYLOAD" --dry-run
else
    # Work on a copy so the kit itself stays generic.
    cp -a "$PAYLOAD/projects" "$WORK/projects"
    cp "$PAYLOAD/layout.json" "$WORK/layout.json"
    python3 "$KIT/lib/detect-hardware.py" "$WORK"
fi
SRC="$([[ $DRY == true ]] && echo "$PAYLOAD" || echo "$WORK")/projects"

# ── 4. Widgets and overlay ──────────────────────────────────────────
step "RBR widgets and audio overlay"
install_plasmoid() {
    local src="$1" id
    id=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["KPlugin"]["Id"])' "$src/metadata.json")
    run rm -rf "$DATA/plasma/plasmoids/$id"
    run kpackagetool6 -t Plasma/Applet -i "$src" >/dev/null
    info "widget: $id"
}
if ! $DRY; then
    (cd "$SRC/rbr-control" && ./build.sh >/dev/null)
fi
install_plasmoid "$SRC/rbr-monitor/package"
install_plasmoid "$SRC/rbr-control/control"
install_plasmoid "$SRC/rbr-control/notify"
[[ -d "$SRC/rbr-audio/plasmoid" ]] && install_plasmoid "$SRC/rbr-audio/plasmoid"
if [[ -d "$PAYLOAD/plasmoids" ]]; then  # optional extra widgets, if you add any
    for w in "$PAYLOAD"/plasmoids/*/; do install_plasmoid "${w%/}"; done
fi
run "$SRC/rbr-audio/install.sh"

# Meta+G for the audio overlay (taken from KWin's Grid View)
run kwriteconfig6 --file kglobalshortcutsrc --group kwin --key "Grid View" "none,Meta+G,Toggle Grid View"
run kwriteconfig6 --file kglobalshortcutsrc --group services --group rbr-audio.desktop --key _launch "Meta+G"

# ── 5. Theme and layout ─────────────────────────────────────────────
step "Applying the RBR theme and panel layout"
run plasma-apply-lookandfeel -a RBR
icons_found WhiteSur-cursors && { run plasma-apply-cursortheme WhiteSur-cursors >/dev/null 2>&1 || true; }
run plasma-apply-colorscheme RBR >/dev/null 2>&1 || true
icons_found kora && run kwriteconfig6 --file kdeglobals --group Icons --key Theme kora

WALL=""
wall_name=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["desktop"].get("wallpaperFile",""))' "$PAYLOAD/layout.json")
if [[ -n "$wall_name" && -f "$PAYLOAD/wallpaper/$wall_name" ]]; then
    WALL="$DATA/wallpapers/rbr-kit/$wall_name"
    run install -Dm644 "$PAYLOAD/wallpaper/$wall_name" "$WALL"
fi
python3 "$KIT/lib/make-layout.py" "$PAYLOAD/layout.json" "$WALL" > "$WORK/layout.js"
if $DRY; then
    info "[dry-run] would run a $(wc -l < "$WORK/layout.js")-line Plasma layout script"
else
    qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "$(cat "$WORK/layout.js")" | sed 's/^/  /'
fi

# ── 6. GTK and Flatpak ──────────────────────────────────────────────
step "GTK and Flatpak apps"
if [[ -f "$PAYLOAD/gtk4-rbr.css" ]]; then
    css="$CONF/gtk-4.0/gtk.css"
    if ! grep -q "RBR-BEGIN" "$css" 2>/dev/null; then
        run mkdir -p "$CONF/gtk-4.0"
        if ! $DRY; then { [[ -f "$css" ]] && cat "$css"; echo; cat "$PAYLOAD/gtk4-rbr.css"; } > "$WORK/gtk.css" && cp "$WORK/gtk.css" "$css"; fi
        info "GTK 4 RBR colours added (remove the RBR-BEGIN…RBR-END block to undo)"
    fi
fi
if command -v flatpak >/dev/null; then
    run flatpak override --user --filesystem=xdg-config/gtk-3.0:ro --filesystem=xdg-config/gtk-4.0:ro \
        --filesystem=xdg-config/kdeglobals:ro --filesystem=xdg-data/icons:ro --filesystem=xdg-data/fonts:ro
    info "Flatpak apps may read the theme"
fi

# ── Done ────────────────────────────────────────────────────────────
step "Restarting Plasma"
run systemctl --user restart plasma-plasmashell
opacity=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("panelOpacity",100))' "$PAYLOAD/settings.json" 2>/dev/null || echo 100)
if [[ "$opacity" != "100" ]]; then
    run sleep 8
    run "$HOME/.local/bin/panel-opacity" "$opacity"
fi

(( ${#MISSING[@]} )) && warn "Still missing: ${MISSING[*]} — the parts that need them won't work until you install them."
cat <<EOF

${orange}▌ RBR setup complete.${off}
  • Log out and back in once so Meta+G and the widget hotkeys are active.
  • Hide the crossed-out bell in the system tray (Configure → Entries →
    Notifications → Always hidden). Don't disable it.
  • The RBR icons are installed but not active: System Settings → Icons → RBR.
  • Guide: $PAYLOAD/RBR-HOWTO.md
  • Settings backup: $BACKUP
EOF
