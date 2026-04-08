from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Union

Expr = Union["IconAtom", "BinOp", "Frac", "Eq"]


@dataclass
class IconAtom:
    name: str

    def leaves(self) -> list[IconAtom]:
        return [self]


@dataclass
class BinOp:
    left: Expr
    op: str
    right: Expr

    def leaves(self) -> list[IconAtom]:
        return self.left.leaves() + self.right.leaves()


@dataclass
class Frac:
    num: Expr
    den: Expr

    def leaves(self) -> list[IconAtom]:
        return self.num.leaves() + self.den.leaves()


@dataclass
class Eq:
    left: Expr
    right: Expr

    def leaves(self) -> list[IconAtom]:
        return self.left.leaves() + self.right.leaves()


def load_shortlist(path: Path | None = None) -> list[str]:
    base = Path(__file__).resolve().parent
    p = path or base / "icon_shortlist.txt"
    lines = [ln.strip() for ln in p.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    return lines


_MAX_FRAC_NEST = 2


def random_expr(
    icons: list[str],
    rng: random.Random,
    depth: int,
    p_frac: float = 0.18,
    row_budget: int = 5,
    frac_nest: int = 0,
) -> Expr:
    if row_budget <= 1 or depth <= 0:
        return IconAtom(rng.choice(icons))

    allow_frac = frac_nest < _MAX_FRAC_NEST

    if allow_frac and depth >= 2 and rng.random() < p_frac:
        return Frac(
            num=random_expr(icons, rng, depth - 1, p_frac * 0.6, row_budget, frac_nest + 1),
            den=random_expr(icons, rng, depth - 1, p_frac * 0.6, row_budget, frac_nest + 1),
        )

    ops = ["+", "-", "*"]
    if depth >= 2 and allow_frac:
        ops += ["/"]
    op = rng.choice(ops)
    if op == "/":
        return Frac(
            num=random_expr(icons, rng, depth - 1, p_frac * 0.5, row_budget, frac_nest + 1),
            den=random_expr(icons, rng, depth - 1, p_frac * 0.5, row_budget, frac_nest + 1),
        )

    lo = 1
    hi = row_budget - 1
    if hi < lo:
        return IconAtom(rng.choice(icons))
    left_budget = rng.randint(lo, hi)
    right_budget = row_budget - left_budget
    left = random_expr(icons, rng, depth - 1, p_frac, left_budget, frac_nest)
    right = random_expr(icons, rng, depth - 1, p_frac, right_budget, frac_nest)
    return BinOp(left, op, right)


def random_formula(
    icons: list[str],
    rng: random.Random,
    depth: int,
    row_budget: int,
    p_frac: float = 0.18,
) -> Eq:
    return Eq(
        random_expr(icons, rng, depth, p_frac, row_budget),
        random_expr(icons, rng, depth, p_frac, row_budget),
    )


def expr_to_placeholder(expr: Expr) -> str:
    def stem(s: str) -> str:
        return Path(s).stem

    match expr:
        case IconAtom(name):
            return f"⟨{stem(name)}⟩"
        case BinOp(left, op, right):
            return f"{expr_to_placeholder(left)} {op} {expr_to_placeholder(right)}"
        case Frac(num, den):
            return f"{expr_to_placeholder(num)} / {expr_to_placeholder(den)}"
        case Eq(left, right):
            return f"{expr_to_placeholder(left)} = {expr_to_placeholder(right)}"
        case _:
            raise TypeError(type(expr))
