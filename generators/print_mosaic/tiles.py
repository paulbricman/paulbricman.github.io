"""Homepage-faithful cover tiles (layout + typography) with procedural art inside."""

from __future__ import annotations

import random
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

from zines import ZineSpec, ZINES

_ROOT = Path(__file__).resolve().parent.parent
for _subdir in ("streams", "field", "lattices", "roots", "formulas"):
    _p = str(_ROOT / _subdir)
    if _p not in sys.path:
        sys.path.insert(0, _p)

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# Portrait module matching streams curated cover and homepage tile aspect
COVER_W = 350.0
COVER_H = 495.0


def _strip_xml_decl(s: str) -> str:
    s = s.strip()
    if s.startswith("<?xml"):
        _, _, rest = s.partition("?>")
        return rest.strip()
    return s


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


def _parse_root(svg_doc: str) -> ET.Element:
    return ET.fromstring(_strip_xml_decl(svg_doc).encode("utf-8"))


def _intrinsic_viewbox(root: ET.Element) -> tuple[float, float, float, float]:
    vb = root.get("viewBox")
    if vb:
        parts = re.split(r"[,\s]+", vb.strip())
        x, y, w, h = (float(parts[i]) for i in range(4))
        return x, y, w, h
    w = float(root.get("width", "100").replace("mm", "").replace("px", ""))
    h = float(root.get("height", "100").replace("mm", "").replace("px", ""))
    return 0.0, 0.0, w, h


def _clone_children_of_svg(svg_doc: str, id_suffix: str) -> tuple[list[ET.Element], tuple[float, float, float, float]]:
    r = _parse_root(svg_doc)
    _uniquify_ids(r, id_suffix)
    vx, vy, vw, vh = _intrinsic_viewbox(r)
    kids: list[ET.Element] = []
    for c in list(r):
        kids.append(ET.fromstring(ET.tostring(c, encoding="unicode")))
    return kids, (vx, vy, vw, vh)


def _title_block(root: ET.Element, spec: ZineSpec) -> None:
    """Uppercase wide-tracked title like .grid-item h3 (approximate in SVG)."""
    fs = 11.0
    ls = spec.title_letter_spacing_em * fs
    t = ET.SubElement(root, f"{{{NS}}}text")
    t.set("x", str(COVER_W / 2))
    t.set("y", "22")
    t.set("text-anchor", "middle")
    t.set("fill", "#ffffff")
    t.set("font-family", "Palatino, 'Palatino Linotype', Georgia, 'Times New Roman', serif")
    t.set("font-size", str(fs))
    t.set("font-weight", "normal")
    t.set("letter-spacing", f"{ls:.3f}")
    t.text = escape(spec.title.upper())


def _svg_root_open(spec: ZineSpec) -> ET.Element:
    root = ET.Element(f"{{{NS}}}svg")
    root.set("width", str(COVER_W))
    root.set("height", str(COVER_H))
    root.set("viewBox", f"0 0 {COVER_W:.0f} {COVER_H:.0f}")
    root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    bg = ET.SubElement(root, f"{{{NS}}}rect")
    bg.set("width", "100%")
    bg.set("height", "100%")
    bg.set("fill", spec.background)
    _title_block(root, spec)
    return root


def _to_doc(root: ET.Element) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        + ET.tostring(root, encoding="unicode")
    )


def render_tile(
    generator_id: str,
    seed: int,
    *,
    tile_background: str,
    icons_root: Path | None = None,
) -> str:
    spec = next(z for z in ZINES if z.key == generator_id)
    if spec.background.lower() != tile_background.lower():
        raise ValueError(f"background mismatch for {generator_id}")
    if generator_id == "field":
        return _cover_field(spec, seed)
    if generator_id == "streams":
        return _cover_streams(spec, seed)
    if generator_id == "formulas":
        if icons_root is None or not icons_root.is_dir():
            raise SystemExit(
                "formulas tiles need --icons-root or PIXELARTICONS_SVG_DIR pointing at "
                "Pixelarticons base SVGs (see generators/formulas/generate.py)."
            )
        return _cover_formulas(spec, seed, icons_root)
    if generator_id == "lattices":
        return _cover_lattices(spec, seed)
    if generator_id == "roots":
        return _cover_roots(spec, seed)
    raise ValueError(f"unknown generator: {generator_id}")


def _field_strip_svg(seed: int) -> str:
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
        background="transparent",
        padding=40,
    )
    gen.generate(seed=seed)
    return gen.to_svg()


def _cover_field(spec: ZineSpec, seed: int) -> str:
    root = _svg_root_open(spec)
    strip_w = COVER_W * 0.75
    x0 = (COVER_W - strip_w) / 2
    strip_h = COVER_H * 0.22
    centers = (0.26, 0.51, 0.76)
    for i, cy in enumerate(centers):
        y = cy * COVER_H - strip_h / 2
        kids, (vx, vy, vw, vh) = _clone_children_of_svg(
            _field_strip_svg(seed + i * 10_007 + 3),
            f"_f{seed}_{i}",
        )
        inner = ET.SubElement(root, f"{{{NS}}}svg")
        inner.set("x", f"{x0:.2f}")
        inner.set("y", f"{y:.2f}")
        inner.set("width", f"{strip_w:.2f}")
        inner.set("height", f"{strip_h:.2f}")
        inner.set("viewBox", f"{vx} {vy} {vw} {vh}")
        inner.set("preserveAspectRatio", "xMidYMid slice")
        for ch in kids:
            inner.append(ch)
    return _to_doc(root)


def _streams_square_svg(seed: int, side: int) -> str:
    from streams import StreamsGenerator

    gen = StreamsGenerator(
        width=side,
        height=side,
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


def _cover_streams(spec: ZineSpec, seed: int) -> str:
    root = _svg_root_open(spec)
    defs = ET.SubElement(root, f"{{{NS}}}defs")
    clip_id = f"streamclip_{seed}"
    cp = ET.SubElement(defs, f"{{{NS}}}clipPath")
    cp.set("id", clip_id)
    frame = COVER_W * 0.78
    cx = COVER_W / 2
    cy = COVER_H * 0.51
    r = frame / 2
    circ = ET.SubElement(cp, f"{{{NS}}}circle")
    circ.set("cx", f"{cx:.3f}")
    circ.set("cy", f"{cy:.3f}")
    circ.set("r", f"{r:.3f}")

    g = ET.SubElement(root, f"{{{NS}}}g")
    g.set("clip-path", f"url(#{clip_id})")
    side = 520
    kids, (vx, vy, vw, vh) = _clone_children_of_svg(_streams_square_svg(seed, side), f"_s{seed}")
    inner = ET.SubElement(g, f"{{{NS}}}svg")
    inner.set("x", f"{cx - r:.3f}")
    inner.set("y", f"{cy - r:.3f}")
    inner.set("width", f"{frame:.3f}")
    inner.set("height", f"{frame:.3f}")
    inner.set("viewBox", f"{vx} {vy} {vw} {vh}")
    inner.set("preserveAspectRatio", "xMidYMid slice")
    for ch in kids:
        inner.append(ch)

    ring = ET.SubElement(root, f"{{{NS}}}circle")
    ring.set("cx", f"{cx:.3f}")
    ring.set("cy", f"{cy:.3f}")
    ring.set("r", f"{r:.3f}")
    ring.set("fill", "none")
    ring.set("stroke", "#ffffff")
    ring.set("stroke-width", "2")
    return _to_doc(root)


def _formula_strip_svg(seed: int, icons_root: Path, bg: str) -> str:
    from expression_ast import load_shortlist, random_formula
    from render_svg import expr_scaled_bounds, expr_to_svg

    names = load_shortlist(None)
    rng = random.Random(seed)
    cw, ch = 720.0, 280.0
    pad = 32.0
    fg = "#ffffff"
    expr = random_formula(names, rng, 4, 5)
    avail_w = cw - 2 * pad
    avail_h = ch - 2 * pad
    bw, bh = expr_scaled_bounds(expr, icons_root, fg=fg, max_content_width=880.0)
    canvas_scale = min(avail_w / bw, avail_h / bh) if bw > 0 and bh > 0 else 1.0
    return expr_to_svg(
        expr,
        icons_root,
        padding=pad,
        fg=fg,
        bg=bg,
        max_content_width=880.0,
        canvas_width=cw,
        canvas_height=ch,
        canvas_content_scale=canvas_scale,
    )


def _cover_formulas(spec: ZineSpec, seed: int, icons_root: Path) -> str:
    root = _svg_root_open(spec)
    strip_h = COVER_H * 0.14
    tops = (0.26, 0.38, 0.50, 0.62, 0.74)
    for i, top in enumerate(tops):
        y = top * COVER_H - strip_h / 2
        kids, (vx, vy, vw, vh) = _clone_children_of_svg(
            _formula_strip_svg(seed + i * 50_003, icons_root, spec.background),
            f"_m{seed}_{i}",
        )
        inner = ET.SubElement(root, f"{{{NS}}}svg")
        inner.set("x", "0")
        inner.set("y", f"{y:.2f}")
        inner.set("width", str(COVER_W))
        inner.set("height", f"{strip_h:.2f}")
        inner.set("viewBox", f"{vx} {vy} {vw} {vh}")
        inner.set("preserveAspectRatio", "xMidYMid meet")
        for ch in kids:
            inner.append(ch)
    return _to_doc(root)


def _lattice_body_svg(seed: int, background: str) -> str:
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


def _cover_lattices(spec: ZineSpec, seed: int) -> str:
    root = _svg_root_open(spec)
    kids, (vx, vy, vw, vh) = _clone_children_of_svg(
        _lattice_body_svg(seed, spec.background),
        f"_l{seed}",
    )
    art_w = COVER_W * 0.92
    art_h = COVER_H * 0.62
    cx = COVER_W / 2
    cy = COVER_H * 0.56
    g = ET.SubElement(root, f"{{{NS}}}g")
    g.set(
        "transform",
        f"translate({cx:.2f},{cy:.2f}) rotate(90) scale(1.18)",
    )
    inner = ET.SubElement(g, f"{{{NS}}}svg")
    inner.set("x", f"{-art_w / 2:.2f}")
    inner.set("y", f"{-art_h / 2:.2f}")
    inner.set("width", f"{art_w:.2f}")
    inner.set("height", f"{art_h:.2f}")
    inner.set("viewBox", f"{vx} {vy} {vw} {vh}")
    inner.set("preserveAspectRatio", "xMidYMid meet")
    for ch in kids:
        inner.append(ch)
    return _to_doc(root)


def _roots_body_svg(seed: int) -> str:
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


def _cover_roots(spec: ZineSpec, seed: int) -> str:
    root = _svg_root_open(spec)
    kids, (vx, vy, vw, vh) = _clone_children_of_svg(_roots_body_svg(seed), f"_r{seed}")
    art_w = COVER_W * 0.90
    art_h = COVER_H * 0.58
    x0 = (COVER_W - art_w) / 2
    y0 = COVER_H * 0.34
    inner = ET.SubElement(root, f"{{{NS}}}svg")
    inner.set("x", f"{x0:.2f}")
    inner.set("y", f"{y0:.2f}")
    inner.set("width", f"{art_w:.2f}")
    inner.set("height", f"{art_h:.2f}")
    inner.set("viewBox", f"{vx} {vy} {vw} {vh}")
    inner.set("preserveAspectRatio", "xMidYMid meet")
    for ch in kids:
        inner.append(ch)
    return _to_doc(root)
