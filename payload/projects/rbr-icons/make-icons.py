#!/usr/bin/env python3
"""Generate the RBR icon theme.

Each icon is an RBR elbow frame (thick top and left bar with a 45° cut corner
and segment cuts) around a navy panel holding a line glyph. Glyphs are drawn on a 24-unit grid.
Icons not defined here are inherited from the themes listed in index.theme.
"""
from pathlib import Path

OUT = Path(__file__).parent / "RBR"

ORANGE, GOLD, TAN, PEACH = "#DB0A40", "#FFC906", "#E8EDF7", "#A9B4CC"
VIOLET, LILAC, BLUE, SKY, RED = "#3671C6", "#8FAEF5", "#6C7FA8", "#C6D6F7", "#FF5A5F"
NAVY = "#050A1E"

# ── Glyphs (24×24 grid, stroked unless noted) ───────────────────────────────
G = {
    "folder": '<path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1Z"/>',
    "home": '<path d="M3 11 12 4l9 7M5.5 9.5V20h4.5v-6h4v6h4.5V9.5"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>',
    "document": '<path d="M6 3h8l4 4v14H6ZM14 3v4h4M9 12h6M9 16h6"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    "music": '<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',
    "picture": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m3 16 5-5 4 4 3-3 6 6"/><circle cx="16" cy="9" r="1.6"/>',
    "video": '<rect x="3" y="6" width="13" height="12" rx="1.5"/><path d="m16 10 5-3v10l-5-3"/>',
    "template": '<path d="M6 3h8l4 4v14H6ZM14 3v4h4M12 11v6M9 14h6"/>',
    "people": '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>',
    "trash": '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 11v6M14 11v6"/>',
    "trash-full": '<path d="M6 7l1 13h10l1-13Z" fill="currentColor" fill-opacity="0.35"/><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 11v6M14 11v6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "star": '<path d="M12 2l2.2 7.8L22 12l-7.8 2.2L12 22l-2.2-7.8L2 12l7.8-2.2Z" fill="currentColor"/>',
    "harddisk": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M6.5 14h6"/><circle cx="17" cy="14" r="1.2" fill="currentColor"/>',
    "ssd": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h10M7 14h6"/>',
    "usb": '<path d="M9 3h6v5H9ZM7 8h10v11a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2Z"/>',
    "headset": '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1"/><rect x="17" y="14" width="4" height="6" rx="1"/>',
    "gamepad": '<path d="M6.5 8h11a4.5 4.5 0 0 1 4.5 4.5V15a3 3 0 0 1-5.2 2L15 15H9l-1.8 2A3 3 0 0 1 2 15v-2.5A4.5 4.5 0 0 1 6.5 8ZM7 10.5v4M5 12.5h4"/><circle cx="16" cy="11.5" r="0.9" fill="currentColor"/><circle cx="18.2" cy="13.5" r="0.9" fill="currentColor"/>',
    "mouse": '<rect x="7" y="3" width="10" height="18" rx="5"/><path d="M12 3v6"/>',
    "keyboard": '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
    "webcam": '<circle cx="12" cy="10" r="6"/><circle cx="12" cy="10" r="2"/><path d="M8 20h8M12 16v4"/>',
    "speaker": '<path d="M4 9h4l5-4v14l-5-4H4ZM16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/>',
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3M12 15h5"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="6.5"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "bars": '<path d="M3 20h18M6 17v-5M10 17V8M14 17v-3M18 17V6"/>',
    "pencil": '<path d="M4 20l1-5L16 4l4 4L9 19ZM14 6l4 4"/>',
    "calculator": '<rect x="5" y="3" width="14" height="18" rx="2"/><rect x="8" y="6" width="8" height="3"/><path d="M9 13h.01M12 13h.01M15 13h.01M9 17h.01M12 17h.01M15 17h.01"/>',
    "screenshot": '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3"/><circle cx="12" cy="12" r="3"/>',
    "bag": '<path d="M5 8h14l-1 12H6ZM9 8a3 3 0 0 1 6 0"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 2-2s-1-2 0-3h3a4 4 0 0 0 4-4c0-5-4-9-9-9Z"/><circle cx="7.5" cy="11" r="1.2" fill="currentColor"/><circle cx="10" cy="7" r="1.2" fill="currentColor"/><circle cx="15" cy="7" r="1.2" fill="currentColor"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4Z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "search": '<circle cx="11" cy="11" r="6"/><path d="m16 16 5 5"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "power": '<path d="M12 3v8M7 6a8 8 0 1 0 10 0"/>',
    "reboot": '<path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5"/>',
    "logout": '<path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h10"/>',
    "moon": '<path d="M20 14A8 8 0 1 1 10 4a6 6 0 0 0 10 10Z"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8l6 4-6 4Z" fill="currentColor"/>',
    "code": '<path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "wrench": '<path d="M14.5 5.5a4 4 0 0 0 4.9 4.9l-9 9a2 2 0 0 1-2.8-2.8l9-9a4 4 0 0 0-2.1-2.1Z"/>',
    "atom": '<circle cx="12" cy="12" r="1.5" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="3.5"/><ellipse cx="12" cy="12" rx="9" ry="3.5" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="3.5" transform="rotate(-60 12 12)"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5ZM6 11v5c3 3 9 3 12 0v-5"/>',
    "grid": '<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><rect x="14" y="14" width="6" height="6" rx="1"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4ZM3 7l9 4 9-4M12 11v10"/>',
}

# ── Icon name → (glyph, colour), per context directory ──────────────────────
ICONS = {
    "places": {
        "folder": ("folder", ORANGE), "inode-directory": ("folder", ORANGE),
        "user-home": ("home", GOLD), "folder-home": ("home", GOLD),
        "user-desktop": ("monitor", VIOLET), "folder-desktop": ("monitor", VIOLET),
        "folder-documents": ("document", TAN), "folder-download": ("download", SKY),
        "folder-downloads": ("download", SKY), "folder-music": ("music", PEACH),
        "folder-pictures": ("picture", LILAC), "folder-images": ("picture", LILAC),
        "folder-videos": ("video", RED), "folder-templates": ("template", TAN),
        "folder-publicshare": ("people", BLUE), "folder-public": ("people", BLUE),
        "folder-games": ("gamepad", ORANGE), "folder-remote": ("globe", BLUE),
        "network-workgroup": ("globe", BLUE), "network-server": ("harddisk", BLUE),
        "user-trash": ("trash", RED), "user-trash-full": ("trash-full", RED),
        "start-here": ("star", ORANGE), "start-here-kde": ("star", ORANGE),
        "start-here-kde-plasma": ("star", ORANGE),
    },
    "devices": {
        "drive-harddisk": ("harddisk", BLUE), "drive-harddisk-solidstate": ("ssd", BLUE),
        "drive-removable-media": ("usb", SKY), "drive-removable-media-usb": ("usb", SKY),
        "media-flash": ("usb", SKY), "computer": ("monitor", LILAC),
        "video-display": ("monitor", LILAC), "audio-headset": ("headset", PEACH),
        "audio-headphones": ("headset", PEACH), "audio-card": ("speaker", ORANGE),
        "input-gaming": ("gamepad", ORANGE), "input-mouse": ("mouse", TAN),
        "input-keyboard": ("keyboard", TAN), "camera-web": ("webcam", VIOLET),
    },
    "apps": {
        "utilities-terminal": ("terminal", GOLD), "org.kde.konsole": ("terminal", GOLD),
        "konsole": ("terminal", GOLD), "system-file-manager": ("folder", ORANGE),
        "org.kde.dolphin": ("folder", ORANGE), "preferences-system": ("gear", LILAC),
        "systemsettings": ("gear", LILAC), "org.kde.systemsettings": ("gear", LILAC),
        "utilities-system-monitor": ("bars", ORANGE), "org.kde.plasma-systemmonitor": ("bars", ORANGE),
        "accessories-text-editor": ("pencil", TAN), "org.kde.kate": ("pencil", TAN),
        "org.kde.kwrite": ("pencil", TAN), "accessories-calculator": ("calculator", PEACH),
        "org.kde.kcalc": ("calculator", PEACH), "internet-web-browser": ("globe", SKY),
        "org.kde.spectacle": ("screenshot", VIOLET), "applets-screenshooter": ("screenshot", VIOLET),
        "system-software-install": ("bag", PEACH), "plasmadiscover": ("bag", PEACH),
        "org.kde.discover": ("bag", PEACH), "multimedia-volume-control": ("speaker", ORANGE),
        "preferences-desktop-theme": ("palette", VIOLET), "preferences-desktop-color": ("palette", VIOLET),
        "internet-mail": ("mail", SKY), "internet-chat": ("chat", LILAC),
        "office-calendar": ("calendar", GOLD), "preferences-system-time": ("clock", GOLD),
        "system-search": ("search", SKY), "org.kde.krunner": ("search", SKY),
    },
    "categories": {
        "applications-games": ("gamepad", ORANGE), "applications-multimedia": ("play", PEACH),
        "applications-internet": ("globe", SKY), "applications-office": ("document", TAN),
        "applications-graphics": ("palette", VIOLET), "applications-development": ("code", GOLD),
        "applications-system": ("gear", LILAC), "applications-utilities": ("wrench", BLUE),
        "applications-science": ("atom", SKY), "applications-education": ("cap", GOLD),
        "applications-other": ("grid", TAN), "preferences-desktop": ("gear", LILAC),
        "applications-accessories": ("wrench", BLUE),
    },
    "mimetypes": {
        "text-plain": ("document", TAN), "text-x-generic": ("document", TAN),
        "application-pdf": ("document", RED), "image-x-generic": ("picture", LILAC),
        "audio-x-generic": ("music", PEACH), "video-x-generic": ("video", RED),
        "application-x-executable": ("terminal", GOLD), "application-x-shellscript": ("terminal", GOLD),
        "text-x-script": ("terminal", GOLD), "text-html": ("code", SKY),
        "package-x-generic": ("box", ORANGE), "application-x-archive": ("box", ORANGE),
        "application-zip": ("box", ORANGE), "application-x-compressed-tar": ("box", ORANGE),
    },
    "actions": {
        "system-shutdown": ("power", RED), "system-reboot": ("reboot", GOLD),
        "system-log-out": ("logout", PEACH), "system-suspend": ("moon", LILAC),
        "system-lock-screen": ("lock", SKY), "system-switch-user": ("people", BLUE),
    },
}


def icon_svg(glyph: str, color: str) -> str:
    # 64×64 tile: coloured elbow frame (thick top/left) with a 45° cut corner,
    # navy panel with a chamfered inner corner, glyph.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <path d="M14 2H62V62H2V14Z" fill="{color}"/>
  <path d="M17 12H60V60H12V17Z" fill="{NAVY}"/>
  <path d="M2 42H12V44.5H2Z" fill="{NAVY}"/>
  <path d="M42 2H44.5V12H42Z" fill="{NAVY}"/>
  <g transform="translate(18 18) scale(1.5)" fill="none" stroke="{color}" color="{color}"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{G[glyph]}</g>
</svg>
'''


def main():
    dirs = []
    for context, icons in ICONS.items():
        d = OUT / "scalable" / context
        d.mkdir(parents=True, exist_ok=True)
        dirs.append(f"scalable/{context}")
        for name, (glyph, color) in icons.items():
            (d / f"{name}.svg").write_text(icon_svg(glyph, color))

    contexts = {"places": "Places", "devices": "Devices", "apps": "Applications",
                "categories": "Categories", "mimetypes": "MimeTypes", "actions": "Actions"}
    index = [
        "[Icon Theme]",
        "Name=RBR",
        "Comment=F1 RBR-style icons; everything else comes from kora and Breeze",
        "Inherits=kora,breeze-dark,breeze,hicolor",
        "Example=folder",
        "DisplayDepth=32",
        "Directories=" + ",".join(dirs),
        "",
    ]
    for d in dirs:
        index += [f"[{d}]", "Size=64", "MinSize=8", "MaxSize=512", "Type=Scalable",
                  f"Context={contexts[d.split('/')[1]]}", ""]
    (OUT / "index.theme").write_text("\n".join(index))
    print(f"{sum(len(v) for v in ICONS.values())} icons written to {OUT}")


if __name__ == "__main__":
    main()
