"""
Curated / article-referenced SVG pools per zine (index.html + _posts), then ranked files.

Roots and field/lattice batch scripts rank candidates; on-disk filenames preserve rank order.
We prefer explicit homepage + in-article references first, then fill from curated/outputs.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

GENERATORS = Path(__file__).resolve().parent.parent


def _field_landscape_strip(path: Path) -> bool:
    """Keep only wide strip-style field SVGs (homepage rows); skip tall portrait pages."""
    try:
        r = ET.parse(path).getroot()
        w = float(str(r.get("width", "0")).replace("px", ""))
        h = float(str(r.get("height", "0")).replace("px", ""))
    except (ET.ParseError, OSError, ValueError, TypeError):
        return False
    if h <= 0 or w <= 0:
        return False
    return (w / h) >= 1.5


def _stem_num(p: Path) -> int:
    m = re.search(r"_(\d+)\.svg$", p.name, re.I)
    if m:
        return int(m.group(1))
    m2 = re.search(r"(\d+)", p.name)
    return int(m2.group(1)) if m2 else -1


def _dedupe_extend(ordered: list[Path], more: list[Path]) -> None:
    seen = {p.resolve() for p in ordered}
    for p in more:
        r = p.resolve()
        if r not in seen and p.is_file():
            seen.add(r)
            ordered.append(p)


def field_pool() -> list[Path]:
    """Homepage field_0/5/10, article field outputs, then remaining curated + outputs."""
    base = GENERATORS / "field"
    out: list[Path] = []
    for n in (0, 5, 10):
        p = base / "curated" / f"field_{n}.svg"
        if p.is_file() and _field_landscape_strip(p):
            out.append(p)
    for n in (5, 10, 15, 20, 25, 30, 31):
        p = base / "outputs" / f"field_{n}.svg"
        if p.is_file() and _field_landscape_strip(p):
            _dedupe_extend(out, [p])
    curated = sorted((base / "curated").glob("field_*.svg"), key=_stem_num)
    outputs = sorted((base / "outputs").glob("field_*.svg"), key=_stem_num)
    for p in curated + outputs:
        if _field_landscape_strip(p):
            _dedupe_extend(out, [p])
    return out or [base / "curated" / "field_0.svg"]


def streams_pool() -> list[Path]:
    """Article figures first, then homepage tile, then remaining curated/outputs.

    Order matches _posts/2026-03-10-experience-as-material.md (stream_0, 8, 3, 4, 5, 6),
    then index.html stream_cover.svg, then other files for variety.
    """
    base = GENERATORS / "streams"
    out: list[Path] = []
    for n in (0, 8, 3, 4, 5, 6):
        p = base / "outputs" / f"stream_{n}.svg"
        if p.is_file():
            out.append(p)
    cover = base / "curated" / "stream_cover.svg"
    if cover.is_file():
        _dedupe_extend(out, [cover])
    curated_streams = sorted((base / "curated").glob("stream_*.svg"), key=_stem_num)
    _dedupe_extend(out, curated_streams)
    outputs = sorted((base / "outputs").glob("stream_*.svg"), key=_stem_num)
    _dedupe_extend(out, outputs)
    return out or [base / "curated" / "stream_cover.svg"]


def formula_cover_paths() -> list[Path]:
    """Five strips exactly like index.html (cover_00 … cover_04)."""
    base = GENERATORS / "formulas" / "curated"
    return [base / f"cover_{i:02d}.svg" for i in range(5)]


def formulas_strip_pool() -> list[Path]:
    """Curated covers + inline strips (white art); each mosaic strip picks independently."""
    base = GENERATORS / "formulas" / "curated"
    out: list[Path] = []
    for p in formula_cover_paths():
        if p.is_file():
            out.append(p)
    inlines = sorted(base.glob("inline_*.svg"), key=_stem_num)
    _dedupe_extend(out, inlines)
    return out or [base / "cover_00.svg"]


def lattices_pool() -> list[Path]:
    base = GENERATORS / "lattices"
    out: list[Path] = []
    p0 = base / "curated" / "lattice_0.svg"
    if p0.is_file():
        out.append(p0)
    for n in (0, 1, 3, 4, 5, 8, 9, 11, 10):
        p = base / "outputs" / f"lattice_{n}.svg"
        if p.is_file():
            _dedupe_extend(out, [p])
    outputs = sorted((base / "outputs").glob("lattice_*.svg"), key=_stem_num)
    _dedupe_extend(out, outputs)
    return out or [p0]


def roots_pool() -> list[Path]:
    """Index root_system_4, article picks, then remaining ranked curated."""
    base = GENERATORS / "roots" / "curated"
    out: list[Path] = []
    for n in (4, 5, 6, 9, 10, 12, 15, 22, 25):
        p = base / f"root_system_{n}.svg"
        if p.is_file():
            _dedupe_extend(out, [p])
    ranked = sorted(base.glob("root_system_*.svg"), key=_stem_num)
    _dedupe_extend(out, ranked)
    return out or [base / "root_system_4.svg"]


def pick(pool: list[Path], salt: int, slot: int) -> Path:
    if not pool:
        raise ValueError("empty asset pool")
    i = (salt * 1103515245 + slot * 7919) % len(pool)
    return pool[i]


def pick_cell(pool: list[Path], seed: int, row: int, col: int, slot: int = 0) -> Path:
    """Stable pick that varies with grid position (avoids repeated art across tiles)."""
    if not pool:
        raise ValueError("empty asset pool")
    mixed = (
        int(seed)
        ^ ((row + 1) * 0x9E3779B9)
        ^ ((col + 1) * 0x85EBCA6B)
        ^ (slot * 0xC2B2AE35)
    ) & 0xFFFFFFFFFFFFFFFF
    return pool[mixed % len(pool)]
