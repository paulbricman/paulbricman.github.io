"""Zine order 1..5 matches homepage cover numbering (left-to-right among the five tiles)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ZineSpec:
    """One homepage zine tile (same order as reading the five covers 1→5)."""

    key: str
    title: str
    background: str
    title_letter_spacing_em: float  # homepage uses 0.5em except field 0.35em


# 1 = Apologists (field), 2 = Experience (streams), 3 = Stories (formulas),
# 4 = Design for Democracy (lattices), 5 = Technical Is Political (roots)
ZINES: tuple[ZineSpec, ...] = (
    ZineSpec("field", "Apologists of the Artificial", "#FF8C00", 0.35),
    ZineSpec("streams", "Experience as Material", "#B71C1C", 0.5),
    ZineSpec("formulas", "Stories We Tell", "#0D7377", 0.5),
    ZineSpec("lattices", "Design for Democracy", "#0D47A1", 0.5),
    ZineSpec("roots", "The Technical Is Political", "#228B22", 0.5),
)

ZINE_GENERATORS: tuple[str, ...] = tuple(z.key for z in ZINES)
ZINE_BACKGROUND: dict[str, str] = {z.key: z.background for z in ZINES}

Face = Literal["front", "back"]


def zine_spec_for_cell(row: int, col: int, grid_n: int) -> ZineSpec:
    i = row * grid_n + col
    return ZINES[i % len(ZINES)]


def generator_for_cell(row: int, col: int, grid_n: int) -> str:
    return zine_spec_for_cell(row, col, grid_n).key


def cell_seed(master_seed: int, face: Face, row: int, col: int) -> int:
    """Stable positive seed per cell; front and back differ."""
    h = hashlib.sha256(
        f"{master_seed}:{face}:{row}:{col}".encode("utf-8")
    ).digest()
    return int.from_bytes(h[:8], "big") % (2**31 - 1) or 1
