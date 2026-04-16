"""Homepage-faithful cover tiles: curated/article SVGs only, no titles, art vertically centered."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from assets import (
    field_pool,
    formula_cover_paths,
    lattices_pool,
    pick,
    roots_pool,
    streams_pool,
)
from zines import ZINES, ZineSpec

_ROOT = Path(__file__).resolve().parent.parent
for _subdir in ("streams", "field", "lattices", "roots", "formulas"):
    _p = str(_ROOT / _subdir)
    if _p not in sys.path:
        sys.path.insert(0, _p)

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

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


def _clone_file(path: Path, id_suffix: str) -> tuple[list[ET.Element], tuple[float, float, float, float]]:
    return _clone_children_of_svg(path.read_text(encoding="utf-8"), id_suffix)


def _svg_open(spec: ZineSpec) -> ET.Element:
    root = ET.Element(f"{{{NS}}}svg")
    root.set("width", str(COVER_W))
    root.set("height", str(COVER_H))
    root.set("viewBox", f"0 0 {COVER_W:.0f} {COVER_H:.0f}")
    root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    bg = ET.SubElement(root, f"{{{NS}}}rect")
    bg.set("width", "100%")
    bg.set("height", "100%")
    bg.set("fill", spec.background)
    return root


def _to_doc(root: ET.Element) -> str:
    return '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root, encoding="unicode")


def render_tile(
    generator_id: str,
    seed: int,
    *,
    tile_background: str,
    icons_root: Path | None = None,
) -> str:
    _ = icons_root  # retained for API compatibility; tiles use on-disk SVGs only
    spec = next(z for z in ZINES if z.key == generator_id)
    if spec.background.lower() != tile_background.lower():
        raise ValueError(f"background mismatch for {generator_id}")
    if generator_id == "field":
        return _cover_field(spec, seed)
    if generator_id == "streams":
        return _cover_streams(spec, seed)
    if generator_id == "formulas":
        return _cover_formulas(spec, seed)
    if generator_id == "lattices":
        return _cover_lattices(spec, seed)
    if generator_id == "roots":
        return _cover_roots(spec, seed)
    raise ValueError(f"unknown generator: {generator_id}")


def _cover_field(spec: ZineSpec, seed: int) -> str:
    root = _svg_open(spec)
    pool = field_pool()
    strip_w = COVER_W * 0.75
    x0 = (COVER_W - strip_w) / 2
    strip_h = COVER_H * 0.21
    gap = COVER_H * 0.03
    stack_h = 3 * strip_h + 2 * gap
    y0 = (COVER_H - stack_h) / 2
    for i in range(3):
        path = pick(pool, seed, i + 2)
        kids, vb = _clone_file(path, f"_f{seed}_{i}_{path.stem}")
        y = y0 + i * (strip_h + gap)
        inner = ET.SubElement(root, f"{{{NS}}}svg")
        inner.set("x", f"{x0:.2f}")
        inner.set("y", f"{y:.2f}")
        inner.set("width", f"{strip_w:.2f}")
        inner.set("height", f"{strip_h:.2f}")
        inner.set("viewBox", f"{vb[0]} {vb[1]} {vb[2]} {vb[3]}")
        inner.set("preserveAspectRatio", "xMidYMid slice")
        for ch in kids:
            inner.append(ch)
    return _to_doc(root)


def _cover_streams(spec: ZineSpec, seed: int) -> str:
    root = _svg_open(spec)
    pool = streams_pool()
    path = pick(pool, seed, 0)
    kids, vb = _clone_file(path, f"_s{seed}_{path.stem}")

    defs = ET.SubElement(root, f"{{{NS}}}defs")
    clip_id = f"sc_{seed}"
    cp = ET.SubElement(defs, f"{{{NS}}}clipPath")
    cp.set("id", clip_id)
    frame = COVER_W * 0.78
    cx = COVER_W / 2
    cy = COVER_H / 2
    r = frame / 2
    circ = ET.SubElement(cp, f"{{{NS}}}circle")
    circ.set("cx", f"{cx:.3f}")
    circ.set("cy", f"{cy:.3f}")
    circ.set("r", f"{r:.3f}")

    g = ET.SubElement(root, f"{{{NS}}}g")
    g.set("clip-path", f"url(#{clip_id})")
    inner = ET.SubElement(g, f"{{{NS}}}svg")
    inner.set("x", f"{cx - r:.3f}")
    inner.set("y", f"{cy - r:.3f}")
    inner.set("width", f"{frame:.3f}")
    inner.set("height", f"{frame:.3f}")
    inner.set("viewBox", f"{vb[0]} {vb[1]} {vb[2]} {vb[3]}")
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


def _cover_formulas(spec: ZineSpec, seed: int) -> str:
    root = _svg_open(spec)
    paths = formula_cover_paths()
    strip_h = COVER_H * 0.125
    gap = COVER_H * 0.012
    stack_h = 5 * strip_h + 4 * gap
    y0 = (COVER_H - stack_h) / 2
    for i, path in enumerate(paths):
        if not path.is_file():
            continue
        kids, vb = _clone_file(path, f"_m{seed}_{i}_{path.stem}")
        y = y0 + i * (strip_h + gap)
        inner = ET.SubElement(root, f"{{{NS}}}svg")
        inner.set("x", "0")
        inner.set("y", f"{y:.2f}")
        inner.set("width", str(COVER_W))
        inner.set("height", f"{strip_h:.2f}")
        inner.set("viewBox", f"{vb[0]} {vb[1]} {vb[2]} {vb[3]}")
        inner.set("preserveAspectRatio", "xMidYMid meet")
        for ch in kids:
            inner.append(ch)
    return _to_doc(root)


def _cover_lattices(spec: ZineSpec, seed: int) -> str:
    root = _svg_open(spec)
    pool = lattices_pool()
    path = pick(pool, seed, 0)
    kids, vb = _clone_file(path, f"_l{seed}_{path.stem}")
    art_w = COVER_W * 0.92
    art_h = COVER_H * 0.68
    cx = COVER_W / 2
    cy = COVER_H / 2
    g = ET.SubElement(root, f"{{{NS}}}g")
    g.set("transform", f"translate({cx:.2f},{cy:.2f}) rotate(90) scale(1.16)")
    inner = ET.SubElement(g, f"{{{NS}}}svg")
    inner.set("x", f"{-art_w / 2:.2f}")
    inner.set("y", f"{-art_h / 2:.2f}")
    inner.set("width", f"{art_w:.2f}")
    inner.set("height", f"{art_h:.2f}")
    inner.set("viewBox", f"{vb[0]} {vb[1]} {vb[2]} {vb[3]}")
    inner.set("preserveAspectRatio", "xMidYMid meet")
    for ch in kids:
        inner.append(ch)
    return _to_doc(root)


def _cover_roots(spec: ZineSpec, seed: int) -> str:
    root = _svg_open(spec)
    pool = roots_pool()
    path = pick(pool, seed, 0)
    kids, vb = _clone_file(path, f"_r{seed}_{path.stem}")
    art_w = COVER_W * 0.90
    art_h = COVER_H * 0.66
    x0 = (COVER_W - art_w) / 2
    y0 = (COVER_H - art_h) / 2
    inner = ET.SubElement(root, f"{{{NS}}}svg")
    inner.set("x", f"{x0:.2f}")
    inner.set("y", f"{y0:.2f}")
    inner.set("width", f"{art_w:.2f}")
    inner.set("height", f"{art_h:.2f}")
    inner.set("viewBox", f"{vb[0]} {vb[1]} {vb[2]} {vb[3]}")
    inner.set("preserveAspectRatio", "xMidYMid meet")
    for ch in kids:
        inner.append(ch)
    return _to_doc(root)
