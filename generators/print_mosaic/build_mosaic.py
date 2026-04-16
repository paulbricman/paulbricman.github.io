#!/usr/bin/env python3
"""
A5 portrait mosaic: N×N grid of A5-aspect cover tiles on an A5 page (rows = cols).

Each tile uses the same portrait aspect as the page (148:210), so the grid must be
square. Zine order matches index.html (site.posts | reverse): roots → lattices →
field → streams → formulas. Tiles use curated / article-referenced SVGs.

  python3 generators/print_mosaic/build_mosaic.py --face front --out /tmp/front.svg
  python3 generators/print_mosaic/build_mosaic.py --grid 26 --both --out /tmp/mosaic --png

Committed sample:

  python3 generators/print_mosaic/build_mosaic.py --grid 10 --both --master-seed 0 \\
    --out generators/print_mosaic/samples/mosaic_sample
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

_pkg = Path(__file__).resolve().parent
if str(_pkg) not in sys.path:
    sys.path.insert(0, str(_pkg))

from tiles import render_tile
from zines import ZINE_BACKGROUND, Face, cell_seed, generator_for_cell

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


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
) -> str:
    if grid_n < 1:
        raise ValueError("grid must be >= 1")

    page_w, page_h = 148.0, 210.0
    cell_w = page_w / grid_n
    cell_h = page_h / grid_n

    root = ET.Element(f"{{{NS}}}svg")
    root.set("width", f"{page_w}mm")
    root.set("height", f"{page_h}mm")
    root.set("viewBox", f"0 0 {page_w} {page_h}")

    for row in range(grid_n):
        for col in range(grid_n):
            gen = generator_for_cell(row, col, grid_n)
            bg = ZINE_BACKGROUND[gen]
            seed = cell_seed(master_seed, face, row, col)
            doc = render_tile(
                gen,
                seed,
                tile_background=bg,
                grid_row=row,
                grid_col=col,
            )
            tile_root = _parse_svg_fragment(doc)
            suffix = f"_{row}_{col}"
            _uniquify_ids(tile_root, suffix)

            vx, vy, vw, vh = _intrinsic_viewbox(tile_root)
            ox = col * cell_w
            oy = row * cell_h

            g = ET.SubElement(root, f"{{{NS}}}g")
            g.set("transform", f"translate({ox:.6f},{oy:.6f})")

            inner = ET.SubElement(g, f"{{{NS}}}svg")
            inner.set("width", f"{cell_w:.6f}")
            inner.set("height", f"{cell_h:.6f}")
            inner.set("viewBox", f"{vx} {vy} {vw} {vh}")
            inner.set("preserveAspectRatio", "xMidYMid slice")
            inner.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

            for child in list(tile_root):
                inner.append(child)

    body = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body


def _write_png(svg_path: Path, png_path: Path) -> None:
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
            "300",
            "-p",
            "300",
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
        default=24,
        help="N×N square grid (default 24). Rows must equal cols so each tile matches A5 aspect.",
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
    p.add_argument("--png", action="store_true", help="Also rasterize at 300 DPI via rsvg-convert.")
    args = p.parse_args()

    def run_face(face: Face, out_svg: Path) -> None:
        svg = build_mosaic_svg(args.grid, face, args.master_seed)
        out_svg.parent.mkdir(parents=True, exist_ok=True)
        out_svg.write_text(svg, encoding="utf-8")
        print(f"Wrote {out_svg}")
        if args.png:
            png = out_svg.with_suffix(".png")
            _write_png(out_svg, png)
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
