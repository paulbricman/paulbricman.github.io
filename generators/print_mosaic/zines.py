"""Zine order matches homepage: site.posts reversed (newest first)."""

from __future__ import annotations

import hashlib
from typing import Literal

# generator keys in display order 1..5
ZINE_GENERATORS: tuple[str, ...] = ("formulas", "streams", "field", "lattices", "roots")

# background colors from post frontmatter (covers use white/light art on these)
ZINE_BACKGROUND: dict[str, str] = {
    "formulas": "#0D7377",
    "streams": "#B71C1C",
    "field": "#FF8C00",
    "lattices": "#0D47A1",
    "roots": "#228B22",
}

Face = Literal["front", "back"]


def zine_index_for_cell(row: int, col: int, grid_n: int) -> int:
    """0..4 cycling left-to-right, top-to-bottom (zine 1 == index 0)."""
    i = row * grid_n + col
    return i % len(ZINE_GENERATORS)


def generator_for_cell(row: int, col: int, grid_n: int) -> str:
    return ZINE_GENERATORS[zine_index_for_cell(row, col, grid_n)]


def cell_seed(master_seed: int, face: Face, row: int, col: int) -> int:
    """Stable 32-bit-ish positive seed per cell; front and back differ."""
    h = hashlib.sha256(
        f"{master_seed}:{face}:{row}:{col}".encode("utf-8")
    ).digest()
    return int.from_bytes(h[:8], "big") % (2**31 - 1) or 1
