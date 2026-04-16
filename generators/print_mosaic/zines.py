"""Zine order 1..5 matches index.html post loop (site.posts | reverse): oldest → newest."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ZineSpec:
    key: str
    background: str


# 1 = The Technical Is Political (roots) … 5 = Stories We Tell (formulas), same as {% for post in site.posts | reverse limit:5 %}
ZINES: tuple[ZineSpec, ...] = (
    ZineSpec("roots", "#228B22"),
    ZineSpec("lattices", "#0D47A1"),
    ZineSpec("field", "#FF8C00"),
    ZineSpec("streams", "#B71C1C"),
    ZineSpec("formulas", "#0D7377"),
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
    h = hashlib.sha256(
        f"{master_seed}:{face}:{row}:{col}".encode("utf-8")
    ).digest()
    return int.from_bytes(h[:8], "big") % (2**31 - 1) or 1
