from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from expression_ast import BinOp, Eq, Expr, Frac, IconAtom

ICON_SZ = 17.5
OP_SIZE = 17.0
FRAC_PAD = 6.0
FRAC_EXTRA_W = 18.0
LINE_H = 1.5

SPACE_BINOP = OP_SIZE * 0.62
SPACE_MUL = OP_SIZE * 0.55
MUL_DOT_LEAD = 2.0

_FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?family=STIX+Two+Math&amp;display=swap');"
)


def _svg_defs_style() -> str:
    return (
        f"<defs><style type=\"text/css\">{_FONT_IMPORT}"
        "text.math { font-family: 'STIX Two Math', 'STIX Two Text', 'Times New Roman', serif; "
        "text-rendering: geometricPrecision; shape-rendering: geometricPrecision; } "
        "text.mop { font-style: normal; font-weight: 400; } "
        "text.mit { font-style: italic; font-weight: 400; } "
        "text.mbin { font-style: normal; font-weight: 400; letter-spacing: 0.02em; } "
        "</style></defs>"
    )


def _tint_icon_markup(markup: str) -> str:
    m = markup
    m = m.replace('fill="black"', 'fill="currentColor"')
    m = m.replace("fill='black'", "fill='currentColor'")
    m = m.replace('stroke="black"', 'stroke="currentColor"')
    m = m.replace("stroke='black'", "stroke='currentColor'")
    m = re.sub(r'fill\s*=\s*["\']#000000?["\']', 'fill="currentColor"', m, flags=re.I)
    m = re.sub(r'stroke\s*=\s*["\']#000000?["\']', 'stroke="currentColor"', m, flags=re.I)
    return m


def _parse_icon_inner(svg_path: Path) -> tuple[str, float, float]:
    text = svg_path.read_text(encoding="utf-8")
    vb_m = re.search(r"viewBox\s*=\s*[\"']([^\"']+)[\"']", text, re.I)
    if vb_m:
        parts = re.sub(r"[,\s]+", " ", vb_m.group(1).strip()).split()
        vw, vh = float(parts[2]), float(parts[3])
    else:
        w_m = re.search(r"width\s*=\s*[\"']?(\d+)", text, re.I)
        h_m = re.search(r"height\s*=\s*[\"']?(\d+)", text, re.I)
        vw = float(w_m.group(1)) if w_m else 24.0
        vh = float(h_m.group(1)) if h_m else 24.0
    inner_m = re.search(r"<svg[^>]*>(.*)</svg>", text, re.I | re.S)
    if not inner_m:
        raise ValueError(f"Unparseable SVG: {svg_path}")
    inner = _tint_icon_markup(inner_m.group(1).strip())
    return inner, vw, vh


def _icon_group(svg_path: Path, box: float) -> str:
    inner, vw, vh = _parse_icon_inner(svg_path)
    scale = min(box / vw, box / vh)
    tw, th = vw * scale, vh * scale
    tx = (box - tw) / 2
    ty = (box - th) / 2
    return (
        f'<g transform="translate({tx:.3f},{ty:.3f}) scale({scale:.6f})">{inner}</g>'
    )


@dataclass
class Box:
    w: float
    h: float
    mid: float
    g: str

    def shift(self, dx: float, dy: float) -> str:
        if dx == 0 and dy == 0:
            return self.g
        return f'<g transform="translate({dx:.2f},{dy:.2f})">{self.g}</g>'


def _text_row(
    s: str,
    size: float,
    fg: str,
    wmul: float,
    cls: str,
    extra_w: float = 0.0,
    *,
    center_x: bool = False,
) -> Box:
    ef = escape(fg)
    w = max(size * wmul * max(len(s), 1), size * 0.35) + extra_w
    h = size * 1.3
    ym = h / 2
    if center_x:
        xa = w / 2
        ta = "middle"
    else:
        xa = 0.0
        ta = "start"
    g = (
        f'<text class="math {cls}" x="{xa:.2f}" y="{ym:.2f}" '
        f'text-anchor="{ta}" font-size="{size:.1f}" fill="{ef}" stroke="none" '
        f'dominant-baseline="middle">{escape(s)}</text>'
    )
    return Box(w, h, h / 2, g)


def layout_icon(name: str, icons_dir: Path, fg: str) -> Box:
    p = icons_dir / name
    inner = _icon_group(p, ICON_SZ)
    ef = escape(fg)
    g = f'<g fill="{ef}" color="{ef}">{inner}</g>'
    return Box(ICON_SZ, ICON_SZ, ICON_SZ / 2, g)


def hconcat(parts: list[Box], gaps: list[float] | float) -> Box:
    if not parts:
        return Box(0, 0, 0, "")
    if isinstance(gaps, (int, float)):
        gap_list = [float(gaps)] * max(0, len(parts) - 1)
    else:
        gap_list = gaps
        if len(gap_list) != len(parts) - 1:
            raise ValueError("gaps must have len(parts)-1 entries")
    axis_ref = max(b.mid for b in parts)
    x = 0.0
    placements: list[tuple[float, float, Box]] = []
    for i, b in enumerate(parts):
        if i:
            x += gap_list[i - 1]
        dy = axis_ref - b.mid
        placements.append((x, dy, b))
        x += b.w
    top = min(dy for x, dy, b in placements)
    bot = max(dy + b.h for x, dy, b in placements)
    H = bot - top
    mid = axis_ref - top
    chunks = [b.shift(px, dy - top) for px, dy, b in placements]
    return Box(x, H, mid, "".join(chunks))


def layout_expr(expr: Expr, icons_dir: Path, fg: str) -> Box:
    ef = escape(fg)

    match expr:
        case IconAtom(name):
            return layout_icon(name, icons_dir, fg)
        case BinOp(left, op, right):
            lb = layout_expr(left, icons_dir, fg)
            sym = {"+": "+", "-": "−", "*": "·", "/": "/"}.get(op, op)
            if op == "*":
                inner = _text_row("·", OP_SIZE, fg, 0.52, "mbin", center_x=True)
                mid = Box(
                    inner.w + MUL_DOT_LEAD,
                    inner.h,
                    inner.mid,
                    f'<g transform="translate({MUL_DOT_LEAD:.2f},0)">{inner.g}</g>',
                )
            else:
                mid = _text_row(sym, OP_SIZE, fg, 0.42, "mbin")
            rb = layout_expr(right, icons_dir, fg)
            if op == "*":
                gap_before = SPACE_MUL * 0.80
                gap_after = SPACE_MUL * 0.82
            else:
                gap_before = SPACE_BINOP * 0.58
                gap_after = SPACE_BINOP * 0.92
            return hconcat([lb, mid, rb], [gap_before, gap_after])
        case Frac(num, den):
            nb = layout_expr(num, icons_dir, fg)
            db = layout_expr(den, icons_dir, fg)
            w = max(nb.w, db.w) + FRAC_EXTRA_W
            nx = (w - nb.w) / 2
            dx = (w - db.w) / 2
            y_line = nb.h + FRAC_PAD
            y_den = y_line + LINE_H + FRAC_PAD
            total_h = y_den + db.h
            mid = y_line
            frag = (
                f"<g>"
                f"{nb.shift(nx, 0)}"
                f'<line x1="0" y1="{y_line:.2f}" x2="{w:.2f}" y2="{y_line:.2f}" '
                f'stroke="{ef}" stroke-width="{LINE_H:.2f}"/>'
                f"{db.shift(dx, y_den)}"
                f"</g>"
            )
            return Box(w, total_h, mid, frag)
        case Eq(left, right):
            lb = layout_expr(left, icons_dir, fg)
            mb = _text_row("=", OP_SIZE, fg, 0.42, "mbin", center_x=True)
            rb = layout_expr(right, icons_dir, fg)
            gap_eq = SPACE_BINOP * 0.88
            return hconcat([lb, mb, rb], [gap_eq, gap_eq])
        case _:
            raise TypeError(type(expr))


def expr_scaled_bounds(
    expr: Expr,
    icons_dir: Path,
    *,
    fg: str,
    max_content_width: float | None,
) -> tuple[float, float]:
    box = layout_expr(expr, icons_dir, fg)
    s = 1.0
    if max_content_width is not None and box.w > max_content_width:
        s = max_content_width / box.w
    return box.w * s, box.h * s


def expr_to_svg(
    expr: Expr,
    icons_dir: Path,
    *,
    padding: float = 32.0,
    fg: str = "#111111",
    bg: str = "#faf8f5",
    max_content_width: float | None = 900.0,
    canvas_width: float | None = None,
    canvas_height: float | None = None,
    canvas_content_scale: float | None = None,
) -> str:
    box = layout_expr(expr, icons_dir, fg)
    s = 1.0
    if max_content_width is not None and box.w > max_content_width:
        s = max_content_width / box.w
    inner = box.g if s >= 1.0 else f'<g transform="scale({s:.6f})">{box.g}</g>'
    bw = box.w * s
    bh = box.h * s

    if (
        canvas_width is not None
        and canvas_height is not None
        and canvas_width > 2 * padding
        and canvas_height > 2 * padding
    ):
        avail_w = canvas_width - 2 * padding
        avail_h = canvas_height - 2 * padding
        s_fit = (
            canvas_content_scale
            if canvas_content_scale is not None
            else min(avail_w / bw, avail_h / bh)
        )
        inner = f'<g transform="scale({s_fit:.6f})">{inner}</g>'
        bw *= s_fit
        bh *= s_fit
        x0 = padding + (avail_w - bw) / 2
        y0 = padding + (avail_h - bh) / 2
        placed = f'<g transform="translate({x0:.2f},{y0:.2f})">{inner}</g>'
        w = canvas_width
        h = canvas_height
    else:
        w = bw + 2 * padding
        h = bh + 2 * padding
        placed = f'<g transform="translate({padding:.2f},{padding:.2f})">{inner}</g>'
    bg_lower = bg.strip().lower()
    if bg_lower in ("transparent", "none"):
        bg_markup = ""
    else:
        bg_markup = f'<rect width="100%" height="100%" fill="{escape(bg)}"/>'
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w:.1f}" height="{h:.1f}" viewBox="0 0 {w:.1f} {h:.1f}" overflow="visible">'
        f"{_svg_defs_style()}"
        f"{bg_markup}"
        f'<g fill="{escape(fg)}" color="{escape(fg)}">{placed}</g>'
        "</svg>"
    )
