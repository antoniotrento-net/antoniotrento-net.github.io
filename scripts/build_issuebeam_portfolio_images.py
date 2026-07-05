#!/usr/bin/env python3
"""Portfolio JPG/PNG da SVG ufficiali Issuebeam."""

from __future__ import annotations

import tempfile
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ISSUEBEAM_LOGO = (
    Path(__file__).resolve().parents[2]
    / "issuebeam.github.io"
    / "assets"
    / "images"
    / "logo"
)
OUT = ROOT / "assets" / "images" / "portfolio" / "issuebeam"

BG = "#0a0a0a"
TEXT = "#94a3b8"
ACCENT = "#a78bfa"

INDEX_SIZE = (1280, 720)
COVER_SIZE = (1536, 1024)
ICON_SIZE = 1024

TAGLINE_IT = "GitHub Issues dagli agenti AI · CLI Python · vibe coding"


def load_svg(name: str, *, replace_current_color: str | None = None) -> str:
    text = (ISSUEBEAM_LOGO / name).read_text(encoding="utf-8")
    if replace_current_color:
        text = text.replace("currentColor", replace_current_color)
    return text


def render_html(html: str, width: int, height: int, out_png: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "render.html"
        html_path.write_text(html, encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge")
            page = browser.new_page(
                viewport={"width": width, "height": height, "device_scale_factor": 2}
            )
            page.goto(html_path.as_uri())
            page.locator("body").screenshot(path=str(out_png), type="png")
            browser.close()


def png_to_jpg(png: Path, jpg: Path, *, quality: int = 92) -> None:
    Image.open(png).convert("RGB").save(jpg, quality=quality, optimize=True)


def build_index() -> None:
    mark = load_svg("logo-mark.svg")
    w, h = INDEX_SIZE
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {w}px; height: {h}px;
    background: {BG};
    background-image:
      linear-gradient(rgba(124,58,237,0.06) 1px, transparent 1px),
      linear-gradient(90deg, rgba(124,58,237,0.06) 1px, transparent 1px);
    background-size: 48px 48px;
    display: flex; align-items: center; justify-content: center;
  }}
  .mark svg {{ width: 280px; height: 280px; display: block; }}
</style></head><body>
  <div class="mark">{mark}</div>
</body></html>"""
    png = OUT / "_index.png"
    render_html(html, w, h, png)
    png_to_jpg(png, OUT / "issuebeam-index.jpg")
    png.unlink(missing_ok=True)


def build_cover() -> None:
    logo = load_svg("logo-horizontal-dark.svg")
    w, h = COVER_SIZE
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {w}px; height: {h}px;
    background: {BG};
    background-image:
      linear-gradient(rgba(124,58,237,0.06) 1px, transparent 1px),
      linear-gradient(90deg, rgba(124,58,237,0.06) 1px, transparent 1px);
    background-size: 48px 48px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 28px;
  }}
  .logo svg {{ width: 520px; height: auto; display: block; }}
  .tagline {{
    font-family: Inter, system-ui, sans-serif;
    font-size: 22px; font-weight: 500;
    letter-spacing: 0.02em;
    color: {TEXT};
  }}
</style></head><body>
  <div class="logo">{logo}</div>
  <p class="tagline">{TAGLINE_IT}</p>
</body></html>"""
    png = OUT / "_cover.png"
    render_html(html, w, h, png)
    png_to_jpg(png, OUT / "issuebeam-cover.jpg")
    png.unlink(missing_ok=True)


def build_icon() -> None:
    mark = load_svg("logo-mark.svg")
    size = ICON_SIZE
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {size}px; height: {size}px;
    background: {BG};
    display: flex; align-items: center; justify-content: center;
  }}
  .mark svg {{ width: 560px; height: 560px; display: block; }}
</style></head><body>
  <div class="mark">{mark}</div>
</body></html>"""
    out = OUT / "issuebeam-logo-1024x1024.png"
    render_html(html, size, size, out)


def main() -> int:
    if not ISSUEBEAM_LOGO.is_dir():
        raise SystemExit(f"SVG Issuebeam non trovati: {ISSUEBEAM_LOGO}")
    OUT.mkdir(parents=True, exist_ok=True)
    build_index()
    build_cover()
    build_icon()
    print("OK", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
