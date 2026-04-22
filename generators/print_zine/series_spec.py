"""Zine series chapter order matches homepage / print_mosaic (oldest → newest)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class SeparatorKind(Enum):
    COMPACT = "compact"
    DEFAULT = "default"
    STREAM_CIRCLE = "stream_circle"
    FORMULAS = "formulas"


@dataclass(frozen=True)
class ZineChapterSpec:
    post_filename: str
    title: str
    generator: str
    background_color: str
    text_color: str
    separator_kind: SeparatorKind


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def posts_dir() -> Path:
    return repo_root() / "_posts"


# Order: roots → lattices → field → streams → formulas (same as generators/print_mosaic/zines.py)
ZINE_CHAPTERS: tuple[ZineChapterSpec, ...] = (
    ZineChapterSpec(
        post_filename="2025-12-10-the-technical-is-political.md",
        title="The Technical Is Political",
        generator="roots",
        background_color="#228B22",
        text_color="#ffffff",
        separator_kind=SeparatorKind.COMPACT,
    ),
    ZineChapterSpec(
        post_filename="2025-12-17-design-for-democracy.md",
        title="Design for Democracy",
        generator="lattices",
        background_color="#0D47A1",
        text_color="#ffffff",
        separator_kind=SeparatorKind.DEFAULT,
    ),
    ZineChapterSpec(
        post_filename="2026-01-12-apologists-of-the-artificial.md",
        title="Apologists of the Artificial",
        generator="field",
        background_color="#FA8900",
        text_color="#ffffff",
        separator_kind=SeparatorKind.DEFAULT,
    ),
    ZineChapterSpec(
        post_filename="2026-03-10-experience-as-material.md",
        title="Experience as Material",
        generator="streams",
        background_color="#B71C1C",
        text_color="#ffffff",
        separator_kind=SeparatorKind.STREAM_CIRCLE,
    ),
    ZineChapterSpec(
        post_filename="2026-04-08-stories-we-tell.md",
        title="Stories We Tell",
        generator="formulas",
        background_color="#0D7377",
        text_color="#ffffff",
        separator_kind=SeparatorKind.FORMULAS,
    ),
)
