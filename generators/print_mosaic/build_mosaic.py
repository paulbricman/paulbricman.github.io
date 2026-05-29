#!/usr/bin/env python3
"""
A5 portrait mosaic: N×N grid of A5-aspect cover tiles on an A5 page (rows = cols).

Each tile uses the same portrait aspect as the page (148:210), so the grid must be
square. Zine order matches index.html (site.posts | reverse): roots → lattices →
field → streams → formulas. Tiles use curated / article-referenced SVGs. The series PDF builder passes ``cell_pick`` so each
tile reuses the same ``(seed, row, col)`` as the booklet title hero and body spreads; the CLI
defaults to independent ``cell_seed`` picks per cell.

  python3 generators/print_mosaic/build_mosaic.py --face front --out /tmp/front.svg
  python3 generators/print_mosaic/build_mosaic.py --grid 12 --out /tmp/mosaic.svg --png

Default grid is 7×7. Checked-in sample uses the default (PNG):

  python3 generators/print_mosaic/build_mosaic.py --master-seed 0 \\
    --out generators/print_mosaic/samples/mosaic_sample.png

Use ``--out path.png`` to rasterize only (no SVG kept). ``--png-dpi`` applies to that and to ``--png`` (default 300).
"""

from __future__ import annotations

import argparse
import os
import re
from collections.abc import Callable
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

_pkg = Path(__file__).resolve().parent
_print_zine = _pkg.parent / "print_zine"
if str(_pkg) not in sys.path:
    sys.path.insert(0, str(_pkg))
if str(_print_zine) not in sys.path:
    sys.path.append(str(_print_zine))

from tiles import render_tile
from zines import ZINE_BACKGROUND, Face, cell_seed, generator_for_cell
from svg_utils import (
    print_chapter_light_ink,
    recolor_svg_for_print,
    scrub_svg_embedded_style_whites_to_light_ink,
)

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# (face, mosaic_row, mosaic_col) -> (seed, pick_row, pick_col) for render_tile pick_cell coords
SeriesCellPick = Callable[[Face, int, int], tuple[int, int, int]]


def _strip_xml_decl(s: str) -> str:
    s = s.strip()
    if s.startswith("<?xml"):
        _, _, rest = s.partition("?>")
        return rest.strip()
    return s


def _parse_svg_fragment(doc: str) -> ET.Element:
    return ET.fromstring(_strip_xml_decl(doc).encode("utf-8"))


def _uniquify_ids(root: ET.Element, suffix: str) -> None:
    id_map: dict[str, str] = {}
    for el in root.iter():
        old = el.get("id")
        if old:
            id_map[old] = f"{old}{suffix}"
    for el in root.iter():
        old = el.get("id")
        if old and old in id_map:
            el.set("id", id_map[old])
    for el in root.iter():
        for attr, val in list(el.attrib.items()):

            def repl_url(m: re.Match[str]) -> str:
                name = m.group(1)
                return f"url(#{id_map.get(name, name)})"

            if "url(#" in val:
                el.set(attr, re.sub(r"url\(#([^)]+)\)", repl_url, val))


def _intrinsic_viewbox(root: ET.Element) -> tuple[float, float, float, float]:
    vb = root.get("viewBox")
    if vb:
        parts = re.split(r"[,\s]+", vb.strip())
        x, y, w, h = (float(parts[i]) for i in range(4))
        return x, y, w, h
    w = float(root.get("width", "100").replace("mm", "").replace("px", ""))
    h = float(root.get("height", "100").replace("mm", "").replace("px", ""))
    return 0.0, 0.0, w, h


def build_mosaic_svg(
    grid_n: int,
    face: Face,
    master_seed: int,
    *,
    cell_pick: SeriesCellPick | None = None,
    grid_inset_frac: float = 0.0,
    cell_gap_frac: float = 0.0,
) -> str:
    if grid_n < 1:
        raise ValueError("grid must be >= 1")
    if not 0.0 <= grid_inset_frac < 0.5:
        raise ValueError("grid_inset_frac must be in [0, 0.5)")
    if not 0.0 <= cell_gap_frac < 1.0:
        raise ValueError("cell_gap_frac must be in [0, 1)")

    page_w, page_h = 148.0, 210.0
    grid_w = page_w * (1.0 - 2.0 * grid_inset_frac)
    grid_h = page_h * (1.0 - 2.0 * grid_inset_frac)
    offset_x = page_w * grid_inset_frac
    offset_y = page_h * grid_inset_frac
    pitch_w = grid_w / grid_n
    pitch_h = grid_h / grid_n
    gap_w = pitch_w * cell_gap_frac
    gap_h = pitch_h * cell_gap_frac
    tile_w = pitch_w - gap_w
    tile_h = pitch_h - gap_h

    root = ET.Element(f"{{{NS}}}svg")
    root.set("width", f"{page_w}mm")
    root.set("height", f"{page_h}mm")
    root.set("viewBox", f"0 0 {page_w} {page_h}")

    if grid_inset_frac > 0.0 or cell_gap_frac > 0.0:
        bg = ET.SubElement(root, f"{{{NS}}}rect")
        bg.set("x", "0")
        bg.set("y", "0")
        bg.set("width", f"{page_w}")
        bg.set("height", f"{page_h}")
        bg.set("fill", "#ffffff")

    for row in range(grid_n):
        for col in range(grid_n):
            gen = generator_for_cell(row, col, grid_n)
            bg = ZINE_BACKGROUND[gen]
            if cell_pick is not None:
                seed, pick_row, pick_col = cell_pick(face, row, col)
            else:
                seed = cell_seed(master_seed, face, row, col)
                pick_row, pick_col = row, col
            doc = render_tile(
                gen,
                seed,
                tile_background=bg,
                grid_row=pick_row,
                grid_col=pick_col,
                match_print_zine=cell_pick is not None,
                mosaic_field_tile=cell_pick is not None and gen == "field",
            )
            light = print_chapter_light_ink(bg)
            doc = recolor_svg_for_print(
                doc,
                bg,
                generator=gen,
                ink_on_light=light,
                ink_dark=bg,
                accent_soft=light,
                canonical_two_ink=False,
                treat_white_as_transparent=False,
                grey_fills_transparent=False,
            )
            doc = scrub_svg_embedded_style_whites_to_light_ink(doc, light)
            tile_root = _parse_svg_fragment(doc)
            suffix = f"_{row}_{col}"
            _uniquify_ids(tile_root, suffix)

            vx, vy, vw, vh = _intrinsic_viewbox(tile_root)
            ox = offset_x + col * pitch_w + gap_w * 0.5
            oy = offset_y + row * pitch_h + gap_h * 0.5

            g = ET.SubElement(root, f"{{{NS}}}g")
            g.set("transform", f"translate({ox:.6f},{oy:.6f})")

            inner = ET.SubElement(g, f"{{{NS}}}svg")
            inner.set("width", f"{tile_w:.6f}")
            inner.set("height", f"{tile_h:.6f}")
            inner.set("viewBox", f"{vx} {vy} {vw} {vh}")
            inner.set("preserveAspectRatio", "xMidYMid slice")
            inner.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

            for child in list(tile_root):
                inner.append(child)

    body = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body


def _write_png(svg_path: Path, png_path: Path, dpi: int) -> None:
    try:
        subprocess.run(
            ["rsvg-convert", "--version"],
            capture_output=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        raise SystemExit("rsvg-convert not found; install librsvg (e.g. brew install librsvg)") from e
    subprocess.run(
        [
            "rsvg-convert",
            "-d",
            str(dpi),
            "-p",
            str(dpi),
            "-o",
            str(png_path),
            str(svg_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="A5 zine cover mosaic from curated/article SVGs (optional PNG).")
    p.add_argument(
        "--grid",
        type=int,
        default=7,
        help="N×N square grid (default 7). Rows must equal cols so each tile matches A5 aspect.",
    )
    p.add_argument(
        "--face",
        choices=("front", "back"),
        default="front",
        help="Which cover sheet (seeds differ per face).",
    )
    p.add_argument("--both", action="store_true", help="Write front and back using --out as base path.")
    p.add_argument("--master-seed", type=int, default=0, help="Deterministic seed for the whole mosaic.")
    p.add_argument(
        "--out",
        type=Path,
        default=Path("mosaic_front.svg"),
        help="Output .svg path, or directory/base when using --both (front.svg / back.svg).",
    )
    p.add_argument(
        "--png",
        action="store_true",
        help="When --out is .svg, also write a sibling .png via rsvg-convert.",
    )
    p.add_argument(
        "--png-dpi",
        type=int,
        default=300,
        help="PNG raster density (default 300). Use e.g. 150 for smaller files.",
    )
    args = p.parse_args()

    def run_face(face: Face, out_path: Path) -> None:
        svg = build_mosaic_svg(args.grid, face, args.master_seed, cell_pick=None)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_path.suffix.lower() == ".png":
            fd, tmp_name = tempfile.mkstemp(suffix=".svg", prefix="print_mosaic_")
            os.close(fd)
            tmp_svg = Path(tmp_name)
            try:
                tmp_svg.write_text(svg, encoding="utf-8")
                _write_png(tmp_svg, out_path, args.png_dpi)
            finally:
                tmp_svg.unlink(missing_ok=True)
            print(f"Wrote {out_path}")
            return
        out_path.write_text(svg, encoding="utf-8")
        print(f"Wrote {out_path}")
        if args.png:
            png = out_path.with_suffix(".png")
            _write_png(out_path, png, args.png_dpi)
            print(f"Wrote {png}")

    if args.both:
        base = args.out
        if base.suffix.lower() == ".svg":
            base = base.with_suffix("")
        run_face("front", Path(f"{base}_front.svg"))
        run_face("back", Path(f"{base}_back.svg"))
    else:
        run_face(args.face, args.out)


if __name__ == "__main__":
    main()
