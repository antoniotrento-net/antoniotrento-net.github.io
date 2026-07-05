#!/usr/bin/env python3
"""Portfolio JPG/PNG da brand Qwibo — simbolo e testo separati (no overlap)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "portfolio" / "qwibo"

BG = (15, 23, 42)
TEXT = (240, 244, 255)
ACCENT = (56, 189, 248)
FONT = Path(r"C:\Windows\Fonts\segoeuib.ttf")


def draw_mark(size: int) -> Image.Image:
    """Bobina + righe di testo (solo simbolo, senza wordmark)."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size / 64.0

    cx, cy = 22 * s, 25 * s
    r = 13 * s
    sw = max(3, int(5 * s))

    draw.ellipse(
        (cx - r, cy - r, cx + r, cy + r),
        outline=ACCENT,
        width=sw,
    )
    dot = max(2, int(3 * s))
    draw.ellipse((cx - dot, cy - dot, cx + dot, cy + dot), fill=ACCENT)

    def line(y: float, x2: float, color: tuple[int, int, int]) -> None:
        draw.line((cx, y * s, x2 * s, y * s), fill=color, width=sw)

    line(38, 57, ACCENT)
    line(48, 57, TEXT)
    line(58, 44, TEXT)

    return img


def compose_card(width: int, height: int, *, subtitle: str | None = None) -> Image.Image:
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    mark_h = int(height * 0.42)
    mark = draw_mark(mark_h)

    title_font = ImageFont.truetype(str(FONT), int(height * 0.11))
    sub_font = ImageFont.truetype(str(FONT), int(height * 0.035)) if subtitle else None

    title = "Qwibo"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]

    gap = int(width * 0.04)
    block_w = mark.width + gap + title_w
    start_x = (width - block_w) // 2
    mark_y = (height - mark.height) // 2 - (20 if subtitle else 0)
    mark_x = start_x

    img.paste(mark, (mark_x, mark_y), mark)

    text_x = mark_x + mark.width + gap
    text_y = mark_y + (mark.height - title_h) // 2
    draw.text((text_x, text_y), title, font=title_font, fill=TEXT)

    if subtitle and sub_font:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = text_x + max(0, (title_w - sub_w) // 2)
        sub_y = text_y + title_h + int(height * 0.03)
        draw.text((sub_x, sub_y), subtitle, font=sub_font, fill=ACCENT)

    return img


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    compose_card(1600, 600, subtitle="App desktop · Electron + Python embedded").save(
        OUT / "qwibo-cover.jpg", quality=92
    )

    icon = Image.new("RGB", (1024, 1024), BG)
    mark = draw_mark(520)
    icon.paste(mark, ((1024 - mark.width) // 2, (1024 - mark.height) // 2 - 40), mark)
    draw = ImageDraw.Draw(icon)
    font = ImageFont.truetype(str(FONT), 96)
    title = "Qwibo"
    bbox = draw.textbbox((0, 0), title, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((1024 - tw) // 2, 700), title, font=font, fill=TEXT)
    icon.save(OUT / "qwibo-logo-1024x1024.png", optimize=True)

    print("OK", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
