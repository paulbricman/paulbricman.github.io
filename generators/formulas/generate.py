#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import random
from pathlib import Path

from expression_ast import expr_to_placeholder, load_shortlist, random_formula
from render_svg import expr_scaled_bounds, expr_to_svg

_DEFAULT_ICONS = Path.home() / "Projects/cloud/_icons/svg"


def _assert_base_icon_name(name: str) -> None:
    lower = name.lower()
    if not lower.endswith(".svg"):
        raise ValueError(f"Expected .svg icon: {name}")
    if lower.endswith("-sharp.svg") or lower.endswith("-sharpsolid.svg"):
        raise ValueError(f"Use base Pixelarticons only (not sharp): {name}")
    if lower.endswith("-solid.svg") or lower.endswith("-filled.svg"):
        raise ValueError(f"Use outline icons only (not solid/filled): {name}")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Figurative formula patterns: LaTeX-style math typography + inlined Pixelarticons (base only).",
    )
    p.add_argument(
        "--icons-root",
        type=Path,
        default=Path(os.environ.get("PIXELARTICONS_SVG_DIR", _DEFAULT_ICONS)),
        help="Directory of base (non-sharp) SVGs from Pixelarticons",
    )
    p.add_argument("--shortlist", type=Path, default=None, help="Override icon_shortlist.txt path")
    p.add_argument("--out-dir", type=Path, default=Path("outputs"), help="Output directory (relative to formulas/)")
    p.add_argument("--count", type=int, default=50)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--depth", type=int, default=4, help="Max recursion depth for expressions")
    p.add_argument(
        "--row-budget",
        type=int,
        default=5,
        help="Max icon count on one horizontal row (fraction numerator/denominator each get this budget).",
    )
    p.add_argument(
        "--max-width",
        type=float,
        default=880.0,
        help="Scale down if formula is wider than this (px). Use 0 to disable.",
    )
    p.add_argument("--fg", type=str, default="#111111", help="Foreground (icons, operators, text).")
    p.add_argument(
        "--bg",
        type=str,
        default="#faf8f5",
        help="Background fill, or 'transparent' / 'none' for no backdrop rect.",
    )
    p.add_argument(
        "--basename",
        type=str,
        default="formula_",
        help="Output filename prefix (files are {basename}00.svg, …).",
    )
    p.add_argument(
        "--canvas-width",
        type=float,
        default=0.0,
        help="If > 0 and --canvas-height > 0, fix SVG viewBox to this size and scale+center content.",
    )
    p.add_argument(
        "--canvas-height",
        type=float,
        default=0.0,
        help="Paired with --canvas-width for uniform formula frames (e.g. article / cover assets).",
    )
    args = p.parse_args()
    if args.depth < 1:
        raise SystemExit("--depth must be at least 1 (use 2–4 for readable compound formulas).")
    if args.row_budget < 1:
        raise SystemExit("--row-budget must be at least 1.")

    base = Path(__file__).resolve().parent
    out_dir = (base / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    icons_root = args.icons_root.expanduser().resolve()
    if not icons_root.is_dir():
        raise SystemExit(f"Icons directory not found: {icons_root}")

    names = load_shortlist(args.shortlist)
    for n in names:
        try:
            _assert_base_icon_name(n)
        except ValueError as e:
            raise SystemExit(str(e)) from e
        if not (icons_root / n).is_file():
            raise SystemExit(f"Shortlist icon missing on disk: {n} (under {icons_root})")

    cw = args.canvas_width if args.canvas_width > 0 else None
    ch = args.canvas_height if args.canvas_height > 0 else None
    if (cw is None) ^ (ch is None):
        raise SystemExit("Use both --canvas-width and --canvas-height together, or neither.")

    rng = random.Random(args.seed)
    mw = None if args.max_width <= 0 else args.max_width
    exprs = [
        random_formula(names, rng, args.depth, args.row_budget) for _ in range(args.count)
    ]

    canvas_scale: float | None = None
    if cw is not None and ch is not None:
        pad = 32.0
        avail_w = cw - 2 * pad
        avail_h = ch - 2 * pad
        scales = []
        for e in exprs:
            bw, bh = expr_scaled_bounds(e, icons_root, fg=args.fg, max_content_width=mw)
            scales.append(min(avail_w / bw, avail_h / bh))
        canvas_scale = min(scales)

    for i, expr in enumerate(exprs):
        path = out_dir / f"{args.basename}{i:02d}.svg"
        svg = expr_to_svg(
            expr,
            icons_root,
            max_content_width=mw,
            fg=args.fg,
            bg=args.bg,
            canvas_width=cw,
            canvas_height=ch,
            canvas_content_scale=canvas_scale,
        )
        path.write_text(svg, encoding="utf-8")
        print(path.name, expr_to_placeholder(expr))


if __name__ == "__main__":
    main()
