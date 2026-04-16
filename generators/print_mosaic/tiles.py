"""Render one procedural SVG tile per generator (full <svg> document string)."""

from __future__ import annotations

import random
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
for _subdir in ("streams", "field", "lattices", "roots", "formulas"):
    _p = str(_ROOT / _subdir)
    if _p not in sys.path:
        sys.path.insert(0, _p)


def render_tile(
    generator_id: str,
    seed: int,
    *,
    tile_background: str,
    icons_root: Path | None = None,
) -> str:
    if generator_id == "streams":
        return _tile_streams(seed, tile_background)
    if generator_id == "field":
        return _tile_field(seed, tile_background)
    if generator_id == "lattices":
        return _tile_lattices(seed, tile_background)
    if generator_id == "roots":
        return _tile_roots(seed, tile_background)
    if generator_id == "formulas":
        if icons_root is None or not icons_root.is_dir():
            raise SystemExit(
                "formulas tiles need --icons-root or PIXELARTICONS_SVG_DIR pointing at "
                "Pixelarticons base SVGs (see generators/formulas/generate.py)."
            )
        return _tile_formulas(seed, tile_background, icons_root)
    raise ValueError(f"unknown generator: {generator_id}")


def _tile_streams(seed: int, _bg: str) -> str:
    from streams import StreamsGenerator

    gen = StreamsGenerator(
        width=350,
        height=495,
        num_lines=1200,
        steps=55,
        step_size=4.5,
        noise_scale=0.0035,
        stroke_width=0.22,
        stroke_color="white",
        background="transparent",
        padding=0,
    )
    gen.generate(seed=seed)
    return gen.to_svg()


def _tile_field(seed: int, background: str) -> str:
    from field import FieldGenerator

    gen = FieldGenerator(
        width=100,
        height=25,
        scale=0.08,
        octaves=3,
        persistence=0.5,
        threshold=0.5,
        char_size=12,
        stroke_color="white",
        background=background,
        padding=40,
    )
    gen.generate(seed=seed)
    return gen.to_svg()


def _tile_lattices(seed: int, background: str) -> str:
    from lattices import LatticeGenerator

    random.seed(seed * 1000)
    rand_val = random.random()
    if rand_val < 0.25:
        num_hexagons = 0
    elif rand_val < 0.55:
        num_hexagons = 1
    elif rand_val < 0.75:
        num_hexagons = 2
    elif rand_val < 0.9:
        num_hexagons = 3
    else:
        num_hexagons = 4
    num_chains = random.randint(0, 2)

    gen = LatticeGenerator(
        grid_rows=6,
        grid_cols=8,
        hex_size=50,
        stroke_width=16,
        stroke_color="white",
        fill_color="white",
        background=background,
        padding=40,
        show_debug=False,
        num_hexagons=num_hexagons,
        num_chains=num_chains,
    )
    gen.generate(seed=seed)
    return gen.to_svg()


def _tile_roots(seed: int, _bg: str) -> str:
    from roots import RootSystemGenerator

    gen = RootSystemGenerator(
        grid_width=20,
        grid_height=15,
        block_size=60,
        max_terminals=120,
        branch_probability=0.7,
        termination_probability=0.08,
        vertical_line_penalty=0.7,
        horizontal_line_penalty=0.7,
        stroke_width=8,
        stroke_color="white",
        padding=40,
    )
    gen.generate(seed=seed)
    return gen.to_svg(background="transparent")


def _tile_formulas(seed: int, background: str, icons_root: Path) -> str:
    from expression_ast import load_shortlist, random_formula
    from render_svg import expr_scaled_bounds, expr_to_svg

    names = load_shortlist(None)
    rng = random.Random(seed)
    depth = 4
    row_budget = 5
    max_width = 880.0
    cw, ch = 350.0, 495.0
    pad = 32.0
    fg = "#ffffff"
    expr = random_formula(names, rng, depth, row_budget)
    avail_w = cw - 2 * pad
    avail_h = ch - 2 * pad
    bw, bh = expr_scaled_bounds(expr, icons_root, fg=fg, max_content_width=max_width)
    canvas_scale = min(avail_w / bw, avail_h / bh) if bw > 0 and bh > 0 else 1.0
    return expr_to_svg(
        expr,
        icons_root,
        padding=pad,
        fg=fg,
        bg=background,
        max_content_width=max_width,
        canvas_width=cw,
        canvas_height=ch,
        canvas_content_scale=canvas_scale,
    )
