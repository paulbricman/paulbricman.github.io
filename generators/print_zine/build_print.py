#!/usr/bin/env python3
"""
Build a single A5 PDF of the five zine posts (reading order).

System libraries on macOS: WeasyPrint needs Pango and cairo (e.g. brew install pango cairo gdk-pixbuf libffi).
Mosaic covers need rsvg-convert (brew install librsvg).

  generators/print_zine/.venv/bin/python generators/print_zine/build_print.py
  # Site copy (~10MB): raster mosaic covers at 300 DPI; also writes assets/patchwork.pdf.
  # --cover-svg embeds vector covers and roughly triples PDF size; avoid for the public asset.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

_PKG = Path(__file__).resolve().parent
_REPO = _PKG.parent.parent
# Jekyll static asset (no page links); served as /assets/patchwork.pdf on the live site.
_SITE_PDF = _REPO / "assets" / "patchwork.pdf"
# White margin around the 7×7 cover mosaic (same tile matrix, scaled down and centered).
_COVER_MOSAIC_GRID_INSET_FRAC = 0.14
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

_PRINT_MOSAIC = _PKG.parent / "print_mosaic"
if str(_PRINT_MOSAIC) not in sys.path:
    sys.path.insert(0, str(_PRINT_MOSAIC))

import build_mosaic  # noqa: E402
from assets import (  # noqa: E402
    field_pool,
    formulas_strip_pool,
    lattices_pool,
    pick,
    pick_cell,
    roots_pool,
    streams_pool,
)
from jinja2 import Environment, FileSystemLoader  # noqa: E402
from tiles import (  # noqa: E402
    BOOKLET_FIELD_STRIP_GAP_FRAC,
    BOOKLET_FIELD_STRIP_HEIGHT_FRAC,
    BOOKLET_FIELD_STRIP_WIDTH_FRAC,
    BOOKLET_FIELD_VERTICAL_ANCHOR,
    BOOKLET_LATTICES_VIEWBOX_ZOOM,
    build_field_stack_svg,
    build_formulas_stack_svg,
    build_lattices_tile_svg,
    build_roots_tile_svg,
    build_streams_tile_svg,
    render_tile,
)
from zines import generator_for_cell  # noqa: E402
from weasyprint import HTML  # noqa: E402

from parse_posts import image_repo_path, parse_chapter_body, prose_html, validate_image_paths  # noqa: E402
from series_spec import SeparatorKind, ZINE_CHAPTERS, ZineChapterSpec  # noqa: E402
from svg_utils import (  # noqa: E402
    flip_svg_horizontal,
    print_chapter_light_ink,
    recolor_svg_for_print,
)


def _separator_css_class(kind: SeparatorKind) -> str:
    return {
        SeparatorKind.COMPACT: "sep-compact",
        SeparatorKind.DEFAULT: "sep-default",
        SeparatorKind.STREAM_CIRCLE: "sep-stream-circle",
        SeparatorKind.FORMULAS: "sep-formulas",
    }[kind]


def _title_tile_seed(master_seed: int, chapter_index: int) -> int:
    return (master_seed * 100_003 + chapter_index * 17_389) % (2**31 - 1) or 1


def _title_hero_page_class(spec: ZineChapterSpec) -> str:
    """Same layout class string as body image pages (hero CSS parity for title-b)."""
    sk = SeparatorKind.DEFAULT if spec.generator == "streams" else spec.separator_kind
    return _separator_css_class(sk)


def _body_image_page_class(spec: ZineChapterSpec) -> str:
    sk = SeparatorKind.DEFAULT if spec.generator == "streams" else spec.separator_kind
    return _separator_css_class(sk)


def _assign_running_marks(chapters: list[dict]) -> None:
    """Folio 1 = first body text page; section title spreads do not get numbers. Even = verso, odd = recto."""
    n = 1
    for ch in chapters:
        for sp in ch["spreads"]:
            sp["folio_text"] = n
            sp["folio_text_side"] = "verso" if n % 2 == 0 else "recto"
            n += 1
            sp["folio_image"] = n
            sp["folio_image_side"] = "verso" if n % 2 == 0 else "recto"
            n += 1


# Must match tiles._STREAMS_PICK_SALT (seed XOR before pick_cell for non-procedural streams).
_STREAMS_TILE_PICK_SALT = 0x53A3FC51

_ZINE_ROMAN_NUMERALS: tuple[str, ...] = ("I", "II", "III", "IV", "V")


def prelude_series_tokens() -> dict[str, str]:
    """First zine (roots): two-token palette — light paper + dark accent ink; cover bleed stays mosaic accent."""
    accent = ZINE_CHAPTERS[0].background_color
    paper = print_chapter_light_ink(accent)
    ink = accent
    series_bg = paper
    series_ink = ink
    cover_bleed = accent
    return {
        "accent": accent,
        "paper": paper,
        "ink": ink,
        "ink_subtitle": ink,
        "series_bg": series_bg,
        "series_ink": series_ink,
        "cover_bleed": cover_bleed,
    }


def epilogue_blank_paper() -> str:
    """Last zine accent: trailing filler blanks before back cover (same light token weight as chapter interior)."""
    accent = ZINE_CHAPTERS[-1].background_color
    return print_chapter_light_ink(accent)


def _spread_tile_args(master_seed: int, chapter_index: int, spread_index: int) -> tuple[int, int, int]:
    """Stable seed / row / col for field+formulas stack tiles (aligned with pick_cell usage)."""
    seed = (master_seed * 1_000_003 + chapter_index * 50_009 + spread_index * 9973) % (2**31 - 1) or 1
    row = chapter_index * 7 + spread_index
    col = spread_index * 3 + chapter_index * 2
    return seed, row, col


def _composed_figure_key(
    generator: str, seed: int, row: int, col: int, *, streams_procedural: bool
) -> str:
    """Key from the actual picked SVG assets (or procedural streams id).

    ``(seed, row, col)`` alone is insufficient: ``pick_cell`` can map different coordinates to the
    same pool file, so the section opener and a body spread could look identical while keys differed.
    """
    if generator == "streams" and streams_procedural:
        return f"streams::proc::{seed}::{row}::{col}"
    paths: list[Path] = []
    if generator == "roots":
        paths.append(pick_cell(roots_pool(), seed, row, col, 0))
    elif generator == "lattices":
        paths.append(pick_cell(lattices_pool(), seed, row, col, 0))
    elif generator == "field":
        for i in range(3):
            paths.append(pick_cell(field_pool(), seed, row, col, i))
    elif generator == "formulas":
        for i in range(5):
            paths.append(pick_cell(formulas_strip_pool(), seed, row, col, i))
    elif generator == "streams":
        paths.append(
            pick_cell(streams_pool(), seed ^ _STREAMS_TILE_PICK_SALT, row, col, 0)
        )
    else:
        raise ValueError(f"unknown composed generator: {generator}")
    resolved = "|".join(str(p.resolve()) for p in paths)
    return f"{generator}::assets::{resolved}"


def _plan_composed_spread_seeds(
    generator: str,
    master_seed: int,
    chapter_index: int,
    num_spreads: int,
    global_used: set[str],
    *,
    streams_procedural: bool,
) -> tuple[list[tuple[int, int, int]], set[str]]:
    """Pick seeds for every body spread; union is figure-instance keys (for title planning)."""
    spread_seeds: list[tuple[int, int, int]] = []
    union: set[str] = set()
    acc = set(global_used)
    for spread_index in range(num_spreads):
        seed, row, col = _spread_tile_args(master_seed, chapter_index, spread_index)
        seed = _nudge_tile_seed_disjoint(
            generator, seed, row, col, acc, streams_procedural=streams_procedural
        )
        spread_seeds.append((seed, row, col))
        key = _composed_figure_key(generator, seed, row, col, streams_procedural=streams_procedural)
        union.add(key)
        acc.add(key)
    return spread_seeds, union


def _nudge_tile_seed_disjoint(
    generator: str,
    seed: int,
    row: int,
    col: int,
    used_keys: set[str],
    *,
    streams_procedural: bool,
    max_tries: int = 120_000,
) -> int:
    """Adjust seed so this composed tile is not a repeat of any key in ``used_keys``."""
    for k in range(max_tries):
        if k < 80_000:
            s = (seed + k * 97_541) % (2**31 - 1) or 1
        else:
            s = seed ^ ((k - 80_000) * 0xB5297A5D)
        key = _composed_figure_key(generator, s, row, col, streams_procedural=streams_procedural)
        if key not in used_keys:
            return s
    raise SystemExit(
        f"Could not find a unique {generator} figure (row={row}, col={col}); try a different --master-seed."
    )


def _title_tile_pick_seed_from_forbidden(
    generator: str,
    master_seed: int,
    chapter_index: int,
    forbidden: set[str],
    *,
    streams_procedural: bool,
) -> int:
    """Opener hero must not repeat any figure key in ``forbidden``."""
    title_row, title_col = chapter_index, 0
    base = _title_tile_seed(master_seed, chapter_index)
    for attempt in range(80_000):
        s = base ^ (0x14650FB7 if attempt == 0 else attempt * 0xD6E8FEB3)
        key = _composed_figure_key(generator, s, title_row, title_col, streams_procedural=streams_procedural)
        if key not in forbidden:
            return s
    raise SystemExit(
        f"Could not find a unique title hero for {generator} (chapter index {chapter_index}); "
        "try a different --master-seed."
    )


def _series_spread_seed_plans(
    master_seed: int,
) -> tuple[list[list[tuple[int, int, int]]], list[tuple[int, int, int]]]:
    """Body spread picks per chapter + title-hero (seed, chapter_index, 0) each; matches ``_build_chapters``."""
    global_figure_keys: set[str] = set()
    plans: list[list[tuple[int, int, int]]] = []
    title_picks: list[tuple[int, int, int]] = []
    tile_composed = frozenset({"roots", "lattices", "field", "formulas", "streams"})

    for chapter_index, spec in enumerate(ZINE_CHAPTERS):
        pairs = parse_chapter_body(spec)
        errs = validate_image_paths(pairs)
        if errs:
            raise SystemExit(f"{spec.post_filename}: " + "; ".join(errs))

        streams_procedural = spec.generator == "streams"
        spread_seeds: list[tuple[int, int, int]] = []
        chapter_body_keys: set[str] = set()
        if spec.generator in tile_composed:
            spread_seeds, chapter_body_keys = _plan_composed_spread_seeds(
                spec.generator,
                master_seed,
                chapter_index,
                len(pairs),
                global_figure_keys,
                streams_procedural=streams_procedural,
            )
        plans.append(spread_seeds)

        forbidden_title = global_figure_keys | chapter_body_keys
        seed_t = _title_tile_pick_seed_from_forbidden(
            spec.generator,
            master_seed,
            chapter_index,
            forbidden_title,
            streams_procedural=streams_procedural,
        )
        title_picks.append((seed_t, chapter_index, 0))
        if spec.generator in tile_composed:
            global_figure_keys.add(
                _composed_figure_key(
                    spec.generator,
                    seed_t,
                    chapter_index,
                    0,
                    streams_procedural=streams_procedural,
                )
            )
            global_figure_keys.update(chapter_body_keys)

    return plans, title_picks


def _mosaic_cell_pick_series(
    master_seed: int,
    grid_n: int,
    spread_plans: list[list[tuple[int, int, int]]],
    title_picks: list[tuple[int, int, int]],
) -> build_mosaic.SeriesCellPick:
    """Map each mosaic cell to title hero or body spread picks (same seeds/coords as the PDF)."""

    chapter_by_generator = {spec.generator: i for i, spec in enumerate(ZINE_CHAPTERS)}
    n_per_ch = [len(sp) for sp in spread_plans]

    def cell_pick(_face: build_mosaic.Face, row: int, col: int) -> tuple[int, int, int]:
        gen = generator_for_cell(row, col, grid_n)
        ch = chapter_by_generator[gen]
        idx = row * grid_n + col
        occ = 0
        for i in range(idx):
            r, c = divmod(i, grid_n)
            if generator_for_cell(r, c, grid_n) == gen:
                occ += 1
        n = n_per_ch[ch]
        if n <= 0:
            return title_picks[ch]
        cycle_len = n + 1
        k = occ % cycle_len
        if k == 0:
            return title_picks[ch]
        return spread_plans[ch][(k - 1) % n]

    return cell_pick


def _write_mosaic_face_png(
    out_png: Path,
    *,
    face: build_mosaic.Face,
    grid_n: int,
    master_seed: int,
    dpi: int,
    cell_pick: build_mosaic.SeriesCellPick | None = None,
) -> None:
    svg = build_mosaic.build_mosaic_svg(
        grid_n,
        face,
        master_seed,
        cell_pick=cell_pick,
        grid_inset_frac=_COVER_MOSAIC_GRID_INSET_FRAC,
    )
    with tempfile.TemporaryDirectory(prefix="print_zine_mosaic_") as td:
        svg_path = Path(td) / f"mosaic_{face}.svg"
        svg_path.write_text(svg, encoding="utf-8")
        build_mosaic._write_png(svg_path, out_png, dpi)


def _write_mosaic_face_svg(
    out_svg: Path,
    *,
    face: build_mosaic.Face,
    grid_n: int,
    master_seed: int,
    cell_pick: build_mosaic.SeriesCellPick | None = None,
) -> None:
    out_svg.write_text(
        build_mosaic.build_mosaic_svg(
            grid_n,
            face,
            master_seed,
            cell_pick=cell_pick,
            grid_inset_frac=_COVER_MOSAIC_GRID_INSET_FRAC,
        ),
        encoding="utf-8",
    )


def _write_tile_svg(
    path: Path,
    generator: str,
    bg_hex: str,
    seed: int,
    *,
    grid_row: int = 0,
    grid_col: int = 0,
    flip: bool = False,
    opaque_background: bool = True,
) -> None:
    doc = render_tile(
        generator,
        seed,
        tile_background=bg_hex,
        grid_row=grid_row,
        grid_col=grid_col,
        opaque_background=opaque_background,
    )
    if flip:
        doc = flip_svg_horizontal(doc)
    path.write_text(doc, encoding="utf-8")


def _generator_asset_pool(generator: str) -> list[Path]:
    factories = {
        "roots": roots_pool,
        "lattices": lattices_pool,
        "field": field_pool,
        "streams": streams_pool,
        "formulas": formulas_strip_pool,
    }
    fn = factories[generator]
    return fn()


def _prepare_figure_href(
    tmp: Path,
    source: Path | None,
    accent: str,
    dest_stem: str,
    *,
    generator: str,
    ink_on_light: str | None,
    ink_dark: str | None,
    accent_soft: str | None,
    preloaded_svg: str | None = None,
    canonical_two_ink: bool = False,
    treat_white_as_transparent: bool = False,
    grey_fills_transparent: bool = False,
) -> str:
    """Write recolored SVG into tmp, or return file URI for non-SVG figures."""
    if preloaded_svg is not None:
        raw_svg = preloaded_svg
    elif source is not None and source.is_file():
        if source.suffix.lower() != ".svg":
            return source.resolve().as_uri()
        raw_svg = source.read_text(encoding="utf-8")
    else:
        raise ValueError("figure href needs source path or preloaded_svg")
    svg_out = tmp / f"{dest_stem}.svg"
    svg_out.write_text(
        recolor_svg_for_print(
            raw_svg,
            accent,
            generator=generator,
            ink_on_light=ink_on_light,
            ink_dark=ink_dark,
            accent_soft=accent_soft,
            canonical_two_ink=canonical_two_ink,
            treat_white_as_transparent=treat_white_as_transparent,
            grey_fills_transparent=grey_fills_transparent,
        ),
        encoding="utf-8",
    )
    return svg_out.resolve().as_uri()


def _build_chapters(tmp: Path, master_seed: int) -> list[dict]:
    chapters: list[dict] = []
    global_figure_keys: set[str] = set()
    for chapter_index, spec in enumerate(ZINE_CHAPTERS):
        pairs = parse_chapter_body(spec)
        errs = validate_image_paths(pairs)
        if errs:
            raise SystemExit(f"{spec.post_filename}: " + "; ".join(errs))

        accent = spec.background_color
        # Exactly two colors per zine interval: dark = accent, light = blend toward white (no black/white inks).
        chapter_light = print_chapter_light_ink(accent)
        chapter_ink = accent
        accent_light_text = chapter_light
        accent_light_art = chapter_light
        title_ink = chapter_light
        tile_composed = frozenset({"roots", "lattices", "field", "formulas", "streams"})
        extended_ink = spec.generator in frozenset({"roots", "lattices", "formulas", "field", "streams"})
        use_two_ink = spec.generator in tile_composed

        ink_light_arg = accent if extended_ink else None
        ink_dark_arg = accent if extended_ink else None
        accent_soft_arg = accent if extended_ink else None
        streams_procedural = spec.generator == "streams"

        spread_seeds: list[tuple[int, int, int]] = []
        chapter_body_keys: set[str] = set()
        if spec.generator in tile_composed:
            spread_seeds, chapter_body_keys = _plan_composed_spread_seeds(
                spec.generator,
                master_seed,
                chapter_index,
                len(pairs),
                global_figure_keys,
                streams_procedural=streams_procedural,
            )
        forbidden_title = global_figure_keys | chapter_body_keys

        title_path = tmp / f"title_{chapter_index}.svg"
        if spec.generator == "field":
            seed_t = _title_tile_pick_seed_from_forbidden(
                "field",
                master_seed,
                chapter_index,
                forbidden_title,
                streams_procedural=False,
            )
            raw_tile = build_field_stack_svg(
                chapter_light,
                seed_t,
                chapter_index,
                0,
                opaque_background=False,
                strip_width_frac=BOOKLET_FIELD_STRIP_WIDTH_FRAC,
                strip_height_frac=BOOKLET_FIELD_STRIP_HEIGHT_FRAC,
                strip_gap_frac=BOOKLET_FIELD_STRIP_GAP_FRAC,
                inner_preserve_aspect="xMidYMid meet",
                inner_vertical_anchor=BOOKLET_FIELD_VERTICAL_ANCHOR,
                crop_inner_view_to_strip=False,
            )
            title_path.write_text(
                recolor_svg_for_print(
                    raw_tile,
                    accent,
                    generator="field",
                    ink_on_light=chapter_light,
                    ink_dark=chapter_light,
                    accent_soft=chapter_light,
                    canonical_two_ink=False,
                    treat_white_as_transparent=True,
                    grey_fills_transparent=True,
                ),
                encoding="utf-8",
            )
        elif spec.generator == "lattices":
            seed_t = _title_tile_pick_seed_from_forbidden(
                "lattices",
                master_seed,
                chapter_index,
                forbidden_title,
                streams_procedural=False,
            )
            raw_tile = build_lattices_tile_svg(
                spec.background_color,
                seed_t,
                chapter_index,
                0,
                viewbox_zoom=BOOKLET_LATTICES_VIEWBOX_ZOOM,
                opaque_background=False,
            )
            # Transparent tile: HTML owns accent fill; strokes map to light token.
            title_path.write_text(
                recolor_svg_for_print(
                    raw_tile,
                    accent,
                    generator="lattices",
                    ink_on_light=chapter_light,
                    ink_dark=chapter_light,
                    accent_soft=chapter_light,
                    canonical_two_ink=False,
                    treat_white_as_transparent=True,
                    grey_fills_transparent=True,
                ),
                encoding="utf-8",
            )
        elif spec.generator == "streams":
            seed_t = _title_tile_pick_seed_from_forbidden(
                "streams",
                master_seed,
                chapter_index,
                forbidden_title,
                streams_procedural=True,
            )
            raw_tile = build_streams_tile_svg(
                chapter_light,
                seed_t,
                chapter_index,
                0,
                opaque_background=False,
                use_procedural_stream=True,
            )
            title_path.write_text(
                recolor_svg_for_print(
                    raw_tile,
                    accent,
                    generator="streams",
                    ink_on_light=chapter_light,
                    ink_dark=chapter_light,
                    accent_soft=chapter_light,
                    canonical_two_ink=False,
                    treat_white_as_transparent=True,
                    grey_fills_transparent=True,
                ),
                encoding="utf-8",
            )
        else:
            seed_t = _title_tile_pick_seed_from_forbidden(
                spec.generator,
                master_seed,
                chapter_index,
                forbidden_title,
                streams_procedural=False,
            )
            _write_tile_svg(
                title_path,
                spec.generator,
                spec.background_color,
                seed_t,
                grid_row=chapter_index,
                grid_col=0,
                opaque_background=False,
            )
            raw_title = title_path.read_text(encoding="utf-8")
            title_path.write_text(
                recolor_svg_for_print(
                    raw_title,
                    accent,
                    generator=spec.generator,
                    ink_on_light=chapter_light,
                    ink_dark=chapter_light,
                    accent_soft=chapter_light,
                    canonical_two_ink=False,
                    treat_white_as_transparent=True,
                    grey_fills_transparent=True,
                ),
                encoding="utf-8",
            )
        title_right_href = title_path.resolve().as_uri()
        if spec.generator in tile_composed:
            global_figure_keys.add(
                _composed_figure_key(
                    spec.generator,
                    seed_t,
                    chapter_index,
                    0,
                    streams_procedural=streams_procedural,
                )
            )
            global_figure_keys.update(chapter_body_keys)

        spreads: list[dict] = []
        last_repo: Path | None = None

        for spread_index, p in enumerate(pairs):
            base_cls = _body_image_page_class(spec)
            rp = image_repo_path(p)
            image_href = None
            if spec.generator in tile_composed:
                seed, row, col = spread_seeds[spread_index]
                if spec.generator == "field":
                    stacked = build_field_stack_svg(
                        chapter_light,
                        seed,
                        row,
                        col,
                        opaque_background=False,
                        strip_width_frac=BOOKLET_FIELD_STRIP_WIDTH_FRAC,
                        strip_height_frac=BOOKLET_FIELD_STRIP_HEIGHT_FRAC,
                        strip_gap_frac=BOOKLET_FIELD_STRIP_GAP_FRAC,
                        inner_preserve_aspect="xMidYMid meet",
                        inner_vertical_anchor=BOOKLET_FIELD_VERTICAL_ANCHOR,
                        crop_inner_view_to_strip=False,
                    )
                elif spec.generator == "formulas":
                    stacked = build_formulas_stack_svg(
                        chapter_light, seed, row, col, opaque_background=False
                    )
                elif spec.generator == "roots":
                    stacked = build_roots_tile_svg(
                        chapter_light, seed, row, col, opaque_background=False
                    )
                elif spec.generator == "lattices":
                    stacked = build_lattices_tile_svg(
                        chapter_light,
                        seed,
                        row,
                        col,
                        viewbox_zoom=BOOKLET_LATTICES_VIEWBOX_ZOOM,
                        opaque_background=False,
                    )
                else:
                    stacked = build_streams_tile_svg(
                        chapter_light,
                        seed,
                        row,
                        col,
                        opaque_background=False,
                        use_procedural_stream=streams_procedural,
                    )
                image_href = _prepare_figure_href(
                    tmp,
                    None,
                    accent,
                    f"fig_{chapter_index}_{spread_index}",
                    generator=spec.generator,
                    ink_on_light=ink_light_arg,
                    ink_dark=ink_dark_arg,
                    accent_soft=accent_soft_arg,
                    preloaded_svg=stacked,
                    canonical_two_ink=False,
                    treat_white_as_transparent=True,
                )
            elif rp is not None and rp.is_file():
                rp_res = str(rp.resolve())
                ek = f"embed::{rp_res}"
                if ek in global_figure_keys:
                    raise SystemExit(
                        f"{spec.post_filename}: embedded figure {rp_res} already used elsewhere in the booklet."
                    )
                global_figure_keys.add(ek)
                last_repo = rp
                image_href = _prepare_figure_href(
                    tmp,
                    rp,
                    accent,
                    f"fig_{chapter_index}_{spread_index}",
                    generator=spec.generator,
                    ink_on_light=ink_light_arg,
                    ink_dark=ink_dark_arg,
                    accent_soft=accent_soft_arg,
                    canonical_two_ink=use_two_ink,
                    treat_white_as_transparent=True,
                )
            spreads.append(
                {
                    "prose_html": prose_html(p),
                    "image_href": image_href,
                    "image_page_class": base_cls,
                }
            )

        last = spreads[-1]
        if last.get("image_href") is None:
            if spec.generator in tile_composed:
                seed, row, col = _spread_tile_args(master_seed, chapter_index, len(spreads))
                seed = _nudge_tile_seed_disjoint(
                    spec.generator,
                    seed,
                    row,
                    col,
                    global_figure_keys,
                    streams_procedural=streams_procedural,
                )
                if spec.generator == "field":
                    stacked = build_field_stack_svg(
                        chapter_light,
                        seed,
                        row,
                        col,
                        opaque_background=False,
                        strip_width_frac=BOOKLET_FIELD_STRIP_WIDTH_FRAC,
                        strip_height_frac=BOOKLET_FIELD_STRIP_HEIGHT_FRAC,
                        strip_gap_frac=BOOKLET_FIELD_STRIP_GAP_FRAC,
                        inner_preserve_aspect="xMidYMid meet",
                        inner_vertical_anchor=BOOKLET_FIELD_VERTICAL_ANCHOR,
                        crop_inner_view_to_strip=False,
                    )
                elif spec.generator == "formulas":
                    stacked = build_formulas_stack_svg(
                        chapter_light, seed, row, col, opaque_background=False
                    )
                elif spec.generator == "roots":
                    stacked = build_roots_tile_svg(
                        chapter_light, seed, row, col, opaque_background=False
                    )
                elif spec.generator == "lattices":
                    stacked = build_lattices_tile_svg(
                        chapter_light,
                        seed,
                        row,
                        col,
                        viewbox_zoom=BOOKLET_LATTICES_VIEWBOX_ZOOM,
                        opaque_background=False,
                    )
                else:
                    stacked = build_streams_tile_svg(
                        chapter_light,
                        seed,
                        row,
                        col,
                        opaque_background=False,
                        use_procedural_stream=streams_procedural,
                    )
                last["image_href"] = _prepare_figure_href(
                    tmp,
                    None,
                    accent,
                    f"trailing_{chapter_index}",
                    generator=spec.generator,
                    ink_on_light=ink_light_arg,
                    ink_dark=ink_dark_arg,
                    accent_soft=accent_soft_arg,
                    preloaded_svg=stacked,
                    canonical_two_ink=False,
                    treat_white_as_transparent=True,
                )
                global_figure_keys.add(
                    _composed_figure_key(
                        spec.generator, seed, row, col, streams_procedural=streams_procedural
                    )
                )
            else:
                pool = _generator_asset_pool(spec.generator)
                salt = (master_seed * 131_071 + chapter_index * 524_287 + 0x13579BDF) % (2**31 - 1) or 1
                slot = len(spreads)
                chosen = pick(pool, salt, slot)
                if last_repo is not None and chosen.resolve() == last_repo.resolve():
                    chosen = pick(pool, salt, slot + 1)
                chosen_res = str(chosen.resolve())
                pk = f"pool::{chosen_res}"
                if pk in global_figure_keys:
                    for bump in range(1, len(pool) * 3):
                        chosen = pick(pool, salt, slot + bump)
                        chosen_res = str(chosen.resolve())
                        pk = f"pool::{chosen_res}"
                        if pk not in global_figure_keys:
                            break
                    if pk in global_figure_keys:
                        raise SystemExit(
                            f"{spec.post_filename}: could not pick a unique trailing asset for {spec.generator}."
                        )
                global_figure_keys.add(pk)
                last["image_href"] = _prepare_figure_href(
                    tmp,
                    chosen,
                    accent,
                    f"trailing_{chapter_index}",
                    generator=spec.generator,
                    ink_on_light=ink_light_arg,
                    ink_dark=ink_dark_arg,
                    accent_soft=accent_soft_arg,
                    canonical_two_ink=use_two_ink,
                    treat_white_as_transparent=True,
                )
            last["image_page_class"] = _body_image_page_class(spec)

        chapters.append(
            {
                "title": spec.title,
                "generator": spec.generator,
                "background_color": spec.background_color,
                "text_color": spec.text_color,
                "title_right_href": title_right_href,
                "title_hero_class": _title_hero_page_class(spec),
                "accent_light_text": accent_light_text,
                "accent_light_art": accent_light_art,
                "chapter_ink": chapter_ink,
                "title_ink": title_ink,
                "roman_numeral": (
                    _ZINE_ROMAN_NUMERALS[chapter_index]
                    if chapter_index < len(_ZINE_ROMAN_NUMERALS)
                    else str(chapter_index + 1)
                ),
                "spreads": spreads,
            }
        )
    return chapters


def main() -> None:
    p = argparse.ArgumentParser(description="Compose five zine posts into one A5 PDF (WeasyPrint).")
    p.add_argument(
        "--out",
        type=Path,
        default=_PKG / "samples" / "patchwork.pdf",
        help="Output PDF path (default: generators/print_zine/samples/patchwork.pdf).",
    )
    p.add_argument(
        "--blank-start",
        type=int,
        default=0,
        help="Blank pages after front cover (default 0).",
    )
    p.add_argument("--blank-end", type=int, default=0, help="Blank pages before back cover (default 0).")
    p.add_argument(
        "--blank-after-series",
        type=int,
        default=0,
        help="Blank pages after the series title page (default 0).",
    )
    p.add_argument("--no-series-page", action="store_true", help="Omit the series title page.")
    p.add_argument(
        "--series-title",
        default="Patchwork",
        help="HTML document title only (not shown on the series page).",
    )
    p.add_argument(
        "--series-subtitle",
        default="a manifesto on\nthe politics of computing",
        help="Series page text; use embedded newline for a forced line break.",
    )
    p.add_argument("--grid", type=int, default=7, help="Mosaic grid N×N (print_mosaic).")
    p.add_argument("--master-seed", type=int, default=0, help="Mosaic master seed.")
    p.add_argument(
        "--png-dpi",
        type=int,
        default=300,
        help="Mosaic cover PNG DPI when not using --cover-svg (default 300).",
    )
    p.add_argument(
        "--cover-svg",
        action="store_true",
        help="Use vector mosaic SVG for covers (sharp at any zoom); else high-DPI PNG.",
    )
    args = p.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="print_zine_build_") as tmp:
        tmp_path = Path(tmp)
        spread_plans, title_picks = _series_spread_seed_plans(args.master_seed)
        cell_pick = _mosaic_cell_pick_series(
            args.master_seed, args.grid, spread_plans, title_picks
        )
        if args.cover_svg:
            front_cover = tmp_path / "mosaic_front.svg"
            back_cover = tmp_path / "mosaic_back.svg"
            _write_mosaic_face_svg(
                front_cover,
                face="front",
                grid_n=args.grid,
                master_seed=args.master_seed,
                cell_pick=cell_pick,
            )
            _write_mosaic_face_svg(
                back_cover,
                face="back",
                grid_n=args.grid,
                master_seed=args.master_seed,
                cell_pick=cell_pick,
            )
            front_href = front_cover.resolve().as_uri()
            back_href = back_cover.resolve().as_uri()
        else:
            front_png = tmp_path / "mosaic_front.png"
            back_png = tmp_path / "mosaic_back.png"
            _write_mosaic_face_png(
                front_png,
                face="front",
                grid_n=args.grid,
                master_seed=args.master_seed,
                dpi=args.png_dpi,
                cell_pick=cell_pick,
            )
            _write_mosaic_face_png(
                back_png,
                face="back",
                grid_n=args.grid,
                master_seed=args.master_seed,
                dpi=args.png_dpi,
                cell_pick=cell_pick,
            )
            front_href = front_png.resolve().as_uri()
            back_href = back_png.resolve().as_uri()

        chapters = _build_chapters(tmp_path, args.master_seed)
        _assign_running_marks(chapters)
        prelude = prelude_series_tokens()
        epilogue_paper = epilogue_blank_paper()
        epilogue_accent = ZINE_CHAPTERS[-1].background_color

        env = Environment(
            loader=FileSystemLoader(_PKG / "templates"),
            autoescape=False,
        )
        tpl = env.get_template("print_series.html.jinja")
        html = tpl.render(
            stylesheet_href="generators/print_zine/static/print.css",
            front_cover_href=front_href,
            back_cover_href=back_href,
            blank_start=max(0, args.blank_start),
            blank_after_series=max(0, args.blank_after_series),
            blank_end=max(0, args.blank_end),
            include_series_page=not args.no_series_page,
            series_title=args.series_title,
            series_subtitle=args.series_subtitle,
            prelude=prelude,
            epilogue_paper=epilogue_paper,
            epilogue_accent=epilogue_accent,
            chapters=chapters,
        )

        base_url = _REPO.as_uri() + "/"
        HTML(string=html, base_url=base_url).write_pdf(
            args.out,
            presentational_hints=True,
        )

    _SITE_PDF.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.out, _SITE_PDF)

    print(f"Wrote {args.out.resolve()}")
    print(f"Published static copy at {_SITE_PDF.resolve()}")


if __name__ == "__main__":
    main()
