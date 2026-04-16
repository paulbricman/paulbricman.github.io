"""
Curated / article-referenced SVG pools per zine (index.html + _posts), then ranked files.

Roots and field/lattice batch scripts rank candidates; on-disk filenames preserve rank order.
We prefer explicit homepage + in-article references first, then fill from curated/outputs.
"""

from __future__ import annotations

import re
from pathlib import Path

GENERATORS = Path(__file__).resolve().parent.parent


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
        if p.is_file():
            out.append(p)
    for n in (5, 10, 15, 20, 25, 30, 31):
        p = base / "outputs" / f"field_{n}.svg"
        if p.is_file():
            _dedupe_extend(out, [p])
    curated = sorted((base / "curated").glob("field_*.svg"), key=_stem_num)
    outputs = sorted((base / "outputs").glob("field_*.svg"), key=_stem_num)
    _dedupe_extend(out, curated)
    _dedupe_extend(out, outputs)
    return out or [base / "curated" / "field_0.svg"]


def streams_pool() -> list[Path]:
    """stream_cover + article streams + curated picks + ranked outputs."""
    base = GENERATORS / "streams"
    out: list[Path] = []
    for rel in ("curated/stream_cover.svg",):
        p = base / rel
        if p.is_file():
            out.append(p)
    for n in (0, 8, 3, 4, 5, 6):
        p = base / "outputs" / f"stream_{n}.svg"
        if p.is_file():
            _dedupe_extend(out, [p])
    curated_streams = sorted((base / "curated").glob("stream_*.svg"), key=_stem_num)
    _dedupe_extend(out, curated_streams)
    outputs = sorted((base / "outputs").glob("stream_*.svg"), key=_stem_num)
    _dedupe_extend(out, outputs)
    return out or [base / "curated" / "stream_cover.svg"]


def formula_cover_paths() -> list[Path]:
    """Five strips exactly like index.html (cover_00 … cover_04)."""
    base = GENERATORS / "formulas" / "curated"
    return [base / f"cover_{i:02d}.svg" for i in range(5)]


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
