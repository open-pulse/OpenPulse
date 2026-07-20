import os
from pathlib import Path

import numpy as np
from PIL import Image

from pulse import DARK_ICON_COLOR, ICON_DIR, LIGHT_ICON_COLOR

DARK_ICONS_DIR = ICON_DIR / "dark_theme"
LIGHT_ICONS_DIR = ICON_DIR / "light_theme"  
ICONS_DIRS = [DARK_ICONS_DIR, LIGHT_ICONS_DIR]
COLORS = [DARK_ICON_COLOR, LIGHT_ICON_COLOR]


def get_icons_to_paint(dir: Path) -> list[Path]:
    icons_to_paint = list()

    for path in dir.rglob("*.png"):
        icons_to_paint.append(path)

    return icons_to_paint


def save_icon(icon_path: Path, icon_image: Image) -> None:
    icon_path.parent.mkdir(parents=True, exist_ok=True)
    icon_image.save(icon_path)


def paint_icons():
    for dir, color in zip(ICONS_DIRS, COLORS):
        icons_to_paint = get_icons_to_paint(dir)

        for icon in icons_to_paint:
            img = Image.open(icon).convert("RGBA")
            img_data = np.array(img)

            mask = img_data[:, :, 3] != 0
            img_data[mask] = color.to_rgba()

            painted_icon = Image.fromarray(img_data)
            save_icon(icon, painted_icon)
            
    
def main():
    paint_icons()

    if os.system("uv --version") != 0:
        return
    
    os.system("uv run invoke ui-compile")


if __name__ == "__main__":
    main()