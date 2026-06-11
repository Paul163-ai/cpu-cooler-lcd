"""Generates assets/icon.png: a simple thermometer icon used for the
config GUI window/taskbar icon and the desktop launchers."""

from pathlib import Path
from PIL import Image, ImageDraw

SIZE = 256
OUT_PATH = Path(__file__).parent / "icon.png"


def generate():
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Dark rounded background
    draw.rounded_rectangle((4, 4, SIZE - 4, SIZE - 4), radius=40, fill=(20, 20, 20, 255))

    # Thermometer bulb and stem
    stem_w = 36
    cx = SIZE // 2
    stem_top = 40
    bulb_r = 46
    bulb_cy = SIZE - 70

    draw.rounded_rectangle(
        (cx - stem_w // 2, stem_top, cx + stem_w // 2, bulb_cy),
        radius=stem_w // 2,
        fill=(60, 60, 60, 255),
    )
    draw.ellipse(
        (cx - bulb_r, bulb_cy - bulb_r, cx + bulb_r, bulb_cy + bulb_r),
        fill=(60, 60, 60, 255),
    )

    # Red mercury fill
    fill_w = 16
    fill_top = 110
    draw.rounded_rectangle(
        (cx - fill_w // 2, fill_top, cx + fill_w // 2, bulb_cy),
        radius=fill_w // 2,
        fill=(220, 40, 40, 255),
    )
    inner_r = bulb_r - 12
    draw.ellipse(
        (cx - inner_r, bulb_cy - inner_r, cx + inner_r, bulb_cy + inner_r),
        fill=(220, 40, 40, 255),
    )

    image.save(OUT_PATH)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    generate()
