"""Lightweight SVG transforms for print assets."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"


def _local_tag(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _relative_luminance_srgb(r: int, g: int, b: int) -> float:
    def lin(u: float) -> float:
        u = u / 255.0
        return u / 12.92 if u <= 0.03928 else ((u + 0.055) / 1.055) ** 2.4

    R, G, B = lin(float(r)), lin(float(g)), lin(float(b))
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def _hsl_to_rgb(h: float, s: float, l_pct: float) -> tuple[int, int, int]:
    h = (h % 360.0) / 360.0
    s = max(0.0, min(1.0, s / 100.0))
    l = max(0.0, min(1.0, l_pct / 100.0))

    def hue2rgb(p: float, q: float, t: float) -> float:
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    if s == 0:
        v = int(round(l * 255))
        return v, v, v
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    r = hue2rgb(p, q, h + 1 / 3)
    g = hue2rgb(p, q, h)
    b = hue2rgb(p, q, h - 1 / 3)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))


def _hex_to_rgb_alpha(val: str) -> tuple[int, int, int, float] | None:
    s = val.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8}", s):
        return None
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    a = 1.0
    if len(s) == 8:
        a = int(s[6:8], 16) / 255.0
    return r, g, b, a


def _parse_any_color_to_rgb(val: str) -> tuple[int, int, int, float] | None:
    v = val.strip()
    low = v.lower()
    if low in ("white", "#fff"):
        return 255, 255, 255, 1.0
    if low in ("black", "#000"):
        return 0, 0, 0, 1.0
    if low.startswith("#"):
        t = _hex_to_rgb_alpha(v)
        return t
    m = re.match(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+)\s*)?\)",
        v,
        flags=re.IGNORECASE,
    )
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return r, g, b, a
    m2 = re.match(
        r"hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%(?:\s*,\s*([\d.]+)\s*)?\)",
        v,
        flags=re.IGNORECASE,
    )
    if m2:
        h_f, s_f, l_f = float(m2.group(1)), float(m2.group(2)), float(m2.group(3))
        a = 1.0
        if m2.group(4) is not None:
            a = float(m2.group(4))
        r, g, b = _hsl_to_rgb(h_f, s_f, l_f)
        return r, g, b, a
    return None


def _two_ink_pick(L: float, ink_dark: str, ink_mid: str, *, mode: str) -> str:
    """Map luminance to two inks + transparency; mode tunes per-generator behavior."""
    if mode in ("lattices_mono", "formulas_flat", "streams_flat"):
        return ink_dark
    # field_stack: push near-white and near-black to dark ink; mid greys to ink_mid
    if mode == "field_stack":
        if L >= 0.34 or L <= 0.12:
            return ink_dark
        return ink_mid
    if L >= 0.34 or L <= 0.12:
        return ink_dark
    return ink_mid


def _is_top_cover_rect(root: ET.Element, el: ET.Element) -> bool:
    if _local_tag(el.tag) != "rect":
        return False
    if el.get("width") != "100%" or el.get("height") != "100%":
        return False
    for c in root:
        if c is el:
            return True
    return False


def _remap_paint_two_ink(val: str, ink_dark: str, ink_mid: str, *, mode: str) -> str | None:
    low = val.strip().lower()
    if low in ("none", "transparent", "inherit"):
        return None
    if low.startswith("url("):
        return ink_dark
    if low == "currentcolor":
        if mode in ("formulas_flat", "streams_flat", "lattices_mono"):
            return ink_dark
        return ink_mid
    parsed = _parse_any_color_to_rgb(val)
    if parsed is None:
        return None
    r, g, b, a = parsed
    if a < 0.04:
        return "none"
    L = _relative_luminance_srgb(r, g, b)
    return _two_ink_pick(L, ink_dark, ink_mid, mode=mode)


def _rewrite_style_two_ink(style: str, ink_dark: str, ink_mid: str, *, mode: str) -> str:
    out: list[str] = []
    for raw in style.split(";"):
        piece = raw.strip()
        if not piece:
            continue
        if ":" not in piece:
            out.append(piece)
            continue
        k, _, v = piece.partition(":")
        key = k.strip().lower()
        val = v.strip()
        if key in ("fill", "stroke", "stop-color", "color"):
            repl = _remap_paint_two_ink(val, ink_dark, ink_mid, mode=mode)
            if repl is not None:
                val = repl
        out.append(f"{k.strip()}: {val}")
    return "; ".join(out)


def _scrub_style_element_text_two_ink(css: str, ink_dark: str, ink_mid: str, *, mode: str) -> str:
    def repl_hex(m: re.Match[str]) -> str:
        raw = m.group(0)
        t = _hex_to_rgb_alpha(raw)
        if t is None:
            return raw
        r, g, b, a = t
        if a < 0.04:
            return "none"
        L = _relative_luminance_srgb(r, g, b)
        return _two_ink_pick(L, ink_dark, ink_mid, mode=mode)

    out = re.sub(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b", repl_hex, css)

    def repl_named_white(m: re.Match[str]) -> str:
        prop = m.group(1)
        repl = _remap_paint_two_ink("white", ink_dark, ink_mid, mode=mode)
        return f"{prop}: {repl}" if repl is not None else m.group(0)

    out = re.sub(
        r"(?i)(fill|stroke|color|stop-color)\s*:\s*white\b",
        repl_named_white,
        out,
    )

    def repl_rgb_white(m: re.Match[str]) -> str:
        prop = m.group(1)
        color_val = m.group(2)
        repl = _remap_paint_two_ink(color_val, ink_dark, ink_mid, mode=mode)
        return f"{prop}: {repl}" if repl is not None else m.group(0)

    out = re.sub(
        r"(?i)(fill|stroke|color|stop-color)\s*:\s*(rgba?\(\s*255\s*,\s*255\s*,\s*255(?:\s*,\s*[\d.]+\s*)?\))",
        repl_rgb_white,
        out,
    )
    return out


def _two_ink_canonicalize_tree(root: ET.Element, ink_dark: str, ink_mid: str, *, mode: str) -> None:
    for el in root.iter():
        if _is_top_cover_rect(root, el):
            continue
        for attr in ("fill", "stroke", "color", "stop-color"):
            v = el.get(attr)
            if not v:
                continue
            repl = _remap_paint_two_ink(v, ink_dark, ink_mid, mode=mode)
            if repl is not None:
                el.set(attr, repl)
        st = el.get("style")
        if st:
            el.set("style", _rewrite_style_two_ink(st, ink_dark, ink_mid, mode=mode))
    for el in root.iter():
        if _local_tag(el.tag) != "style" or not el.text:
            continue
        el.text = _scrub_style_element_text_two_ink(el.text, ink_dark, ink_mid, mode=mode)


def _rewrite_style_force_single_ink(style: str, ink: str) -> str:
    out: list[str] = []
    for raw in style.split(";"):
        piece = raw.strip()
        if not piece:
            continue
        if ":" not in piece:
            out.append(piece)
            continue
        k, _, v = piece.partition(":")
        key = k.strip().lower()
        val = v.strip()
        if key in ("fill", "stroke", "color", "stop-color"):
            low = val.lower()
            if low in ("none", "transparent", "inherit"):
                out.append(f"{k.strip()}: {val}")
            else:
                out.append(f"{k.strip()}: {ink}")
        else:
            out.append(f"{k.strip()}: {val}")
    return "; ".join(out)


def _flatten_lattices_residual_to_ink(root: ET.Element, ink: str) -> None:
    """After lattices_mono, force remaining solid paints to one ink (removes stray mid-grey)."""
    for el in root.iter():
        if _is_top_cover_rect(root, el):
            continue
        if _local_tag(el.tag) == "style":
            continue
        for attr in ("fill", "stroke", "color", "stop-color"):
            v = el.get(attr)
            if not v:
                continue
            low = v.strip().lower()
            if low in ("none", "transparent", "inherit"):
                continue
            el.set(attr, ink)
        st = el.get("style")
        if st:
            el.set("style", _rewrite_style_force_single_ink(st, ink))


def _scrub_style_paint_declarations(css: str, ink: str) -> str:
    """Rewrite fill/stroke/color/stop-color inside <style> text (semicolon-terminated or brace-closed)."""

    def repl_decl(m: re.Match[str]) -> str:
        prop = m.group(1)
        val = m.group(2).strip()
        low = val.lower()
        if low.split()[0] in ("none", "transparent", "inherit"):
            return m.group(0)
        # Always terminate with `;` so the next declaration is not parsed as part of the paint value.
        return f"{prop}: {ink};"

    out = re.sub(
        r"(?i)\b(fill|stroke|color|stop-color)\s*:\s*([^;]+);",
        repl_decl,
        css,
    )
    return re.sub(
        r"(?i)\b(fill|stroke|color|stop-color)\s*:\s*([^;}]+?)(?=\s*\})",
        repl_decl,
        out,
    )


def _scrub_style_paint_blocks(root: ET.Element, ink: str) -> None:
    for el in root.iter():
        if _local_tag(el.tag) != "style" or not el.text:
            continue
        el.text = _scrub_style_paint_declarations(el.text, ink)


def _luminance_of_paint_value(val: str) -> float | None:
    t = _parse_any_color_to_rgb(val)
    if t is None:
        return None
    r, g, b, a = t
    if a < 0.08:
        return None
    return _relative_luminance_srgb(r, g, b)


def _rewrite_style_light_fill_none(style: str, *, luminance_above: float, el_tag: str) -> str:
    if (el_tag or "").lower() in ("text", "tspan"):
        return style
    out: list[str] = []
    for raw in style.split(";"):
        piece = raw.strip()
        if not piece:
            continue
        if ":" not in piece:
            out.append(piece)
            continue
        k, _, v = piece.partition(":")
        key = k.strip().lower()
        val = v.strip()
        if key == "fill":
            low = val.lower()
            if low not in ("none", "transparent", "inherit") and not val.strip().startswith("url("):
                L = _luminance_of_paint_value(val)
                if L is not None and L > luminance_above:
                    val = "none"
        out.append(f"{k.strip()}: {val}")
    return "; ".join(out)


def _scrub_high_luminance_fills_to_transparent(root: ET.Element, *, luminance_above: float = 0.72) -> None:
    """Remove residual light fills on full-width rects only (never circles/paths used as marks)."""
    for el in root.iter():
        el_tag = _local_tag(el.tag)
        if el_tag.lower() != "rect":
            continue
        v = el.get("fill")
        if v:
            low = v.strip().lower()
            if low not in ("none", "transparent", "inherit") and not v.strip().startswith("url("):
                L = _luminance_of_paint_value(v)
                if L is not None and L > luminance_above:
                    el.set("fill", "none")
        st = el.get("style")
        if st:
            el.set(
                "style",
                _rewrite_style_light_fill_none(st, luminance_above=luminance_above, el_tag=el_tag),
            )


def _remove_light_full_viewport_rects(root: ET.Element, *, luminance_above: float = 0.5) -> None:
    """Drop embedded 'paper' plates that would hide the chapter accent on opener tiles."""
    for c in list(root):
        if _local_tag(c.tag) != "rect":
            continue
        if c.get("width") != "100%" or c.get("height") != "100%":
            continue
        fv = c.get("fill")
        if not fv:
            continue
        low = fv.strip().lower()
        if low in ("none", "transparent") or fv.strip().startswith("url("):
            continue
        L = _luminance_of_paint_value(fv)
        if L is not None and L > luminance_above:
            root.remove(c)


def _ensure_accent_plate_under_opener(root: ET.Element, accent_css: str) -> None:
    """Full-bleed accent behind diagram so PDF renderers still show dark under partially opaque art."""
    if _local_tag(root.tag) != "svg":
        return
    want = accent_css.strip().lstrip("#").lower()
    if len(want) == 3:
        want = "".join(ch * 2 for ch in want)
    for c in list(root):
        if _local_tag(c.tag) != "rect":
            continue
        if c.get("width") == "100%" and c.get("height") == "100%":
            fh = (c.get("fill") or "").strip().lstrip("#").lower()
            if len(fh) == 3:
                fh = "".join(ch * 2 for ch in fh)
            if fh[:6] == want[:6]:
                return
    plate = ET.Element(f"{{{SVG_NS}}}rect")
    plate.set("x", "0")
    plate.set("y", "0")
    plate.set("width", "100%")
    plate.set("height", "100%")
    plate.set("fill", accent_css)
    root.insert(0, plate)


def _lift_dark_paint_declarations_in_css(css: str, ink: str, *, max_luminance: float) -> str:
    """Like _scrub_style_paint_declarations but only replaces paints at or below max_luminance."""

    def repl_decl(m: re.Match[str]) -> str:
        prop = m.group(1)
        val = m.group(2).strip()
        low = val.lower()
        if low.split()[0] in ("none", "transparent", "inherit") or val.startswith("url("):
            return m.group(0)
        L = _luminance_of_paint_value(val)
        if L is not None and L <= max_luminance:
            return f"{prop}: {ink};"
        return m.group(0)

    out = re.sub(
        r"(?i)\b(fill|stroke|color)\s*:\s*([^;]+);",
        repl_decl,
        css,
    )
    return re.sub(
        r"(?i)\b(fill|stroke|color)\s*:\s*([^;}]+?)(?=\s*\})",
        repl_decl,
        out,
    )


def _rewrite_style_lift_dark_paints(style: str, ink: str, *, max_luminance: float) -> str:
    out: list[str] = []
    for raw in style.split(";"):
        piece = raw.strip()
        if not piece:
            continue
        if ":" not in piece:
            out.append(piece)
            continue
        k, _, v = piece.partition(":")
        key = k.strip().lower()
        val = v.strip()
        if key in ("fill", "stroke", "color"):
            low = val.lower()
            if low in ("none", "transparent", "inherit") or val.startswith("url("):
                out.append(f"{k.strip()}: {val}")
            else:
                L = _luminance_of_paint_value(val)
                if L is not None and L <= max_luminance:
                    out.append(f"{k.strip()}: {ink}")
                else:
                    out.append(f"{k.strip()}: {val}")
        else:
            out.append(f"{k.strip()}: {val}")
    return "; ".join(out)


def _append_field_opener_light_ink_cascade(root: ET.Element, ink: str) -> None:
    """Append author stylesheet last so !important beats embedded .cls rules (dark 0/1 on accent)."""
    if _local_tag(root.tag) != "svg":
        return
    ink_css = ink.strip()
    if not ink_css.startswith("#"):
        ink_css = f"#{_hex_norm_6(ink)}"
    # Group color fixes currentColor descendants; path/text/tspan get explicit fill.
    css = (
        f"g{{color:{ink_css}!important;}}"
        f"text,tspan{{fill:{ink_css}!important;color:{ink_css}!important;stroke:none!important;}}"
        f"path{{fill:{ink_css}!important;color:{ink_css}!important;}}"
        f"polygon,circle,ellipse{{fill:{ink_css}!important;}}"
        f"line,polyline{{stroke:{ink_css}!important;fill:none!important;}}"
    )
    st = ET.Element(f"{{{SVG_NS}}}style")
    st.set("type", "text/css")
    st.text = css
    root.append(st)


def _field_opener_lift_dark_marker_paint(
    root: ET.Element,
    ink: str,
    accent_css: str,
    *,
    max_luminance: float = 0.52,
) -> None:
    """Binary glyphs and rules often keep dark fills; push them to title ink (not chapter accent)."""
    want = _hex_norm_6(accent_css)

    def _is_chapter_accent_paint(val: str) -> bool:
        t = _parse_any_color_to_rgb(val)
        if t is None:
            return False
        r, g, b, _a = t
        return f"{r:02x}{g:02x}{b:02x}".lower() == want

    def _maybe_lift(val: str) -> str | None:
        low = val.strip().lower()
        if low in ("none", "transparent", "inherit") or val.strip().startswith("url("):
            return None
        if _is_chapter_accent_paint(val):
            return None
        L = _luminance_of_paint_value(val)
        if L is not None and L <= max_luminance:
            return ink
        return None

    shape_tags = frozenset(
        {"path", "text", "tspan", "circle", "ellipse", "line", "polyline", "polygon", "rect"}
    )

    for el in root.iter():
        if _is_top_cover_rect(root, el):
            continue
        st = el.get("style")
        if st:
            el.set("style", _rewrite_style_lift_dark_paints(st, ink, max_luminance=max_luminance))
        if _local_tag(el.tag) == "style" and el.text:
            el.text = _lift_dark_paint_declarations_in_css(el.text, ink, max_luminance=max_luminance)

        tag = _local_tag(el.tag).lower()
        if tag not in shape_tags:
            continue
        for attr in ("fill", "stroke"):
            v = el.get(attr)
            if not v:
                continue
            repl = _maybe_lift(v)
            if repl is not None:
                el.set(attr, repl)
        if tag == "path":
            fa = (el.get("fill") or "").strip().lower()
            if fa == "none":
                continue
            if fa:
                continue
            stn = el.get("style") or ""
            if re.search(r"(?i)\bfill\s*:", stn):
                continue
            el.set("fill", ink)


def _force_single_chapter_ink_tree(root: ET.Element, ink: str) -> None:
    """Collapse diagram paints to a single ink (body: dark on paper; opener: light on accent)."""
    for el in root.iter():
        if _is_top_cover_rect(root, el):
            continue
        if _local_tag(el.tag) == "style":
            continue
        for attr in ("fill", "stroke", "color", "stop-color"):
            v = el.get(attr)
            if not v:
                continue
            low = v.strip().lower()
            if low in ("none", "transparent", "inherit") or v.strip().startswith("url("):
                continue
            el.set(attr, ink)
        st = el.get("style")
        if st:
            el.set("style", _rewrite_style_force_single_ink(st, ink))
    _scrub_style_paint_blocks(root, ink)


def _normalize_opacity_in_style_blocks(root: ET.Element) -> None:
    """Set opacity / stroke-opacity / fill-opacity in <style> text to 1 when they were < 1."""

    def repl(m: re.Match[str]) -> str:
        prop = m.group(1)
        val = m.group(2).strip()
        try:
            if float(val) < 1.0:
                return f"{prop}: 1"
        except ValueError:
            pass
        return m.group(0)

    pat = r"(?i)\b(opacity|stroke-opacity|fill-opacity)\s*:\s*([\d.]+(?:\.\d+)?)"
    for el in root.iter():
        if _local_tag(el.tag) != "style" or not el.text:
            continue
        el.text = re.sub(pat, repl, el.text)


_PRINT_OPACITY_SHAPE_TAGS = frozenset(
    {"path", "line", "circle", "polyline", "polygon", "rect", "ellipse"}
)


def _normalize_print_diagram_opacity(root: ET.Element) -> None:
    """Lattices/field art often uses stroke/fill with opacity<1; after ink remap it reads as grey mist."""
    for el in root.iter():
        if _local_tag(el.tag) not in _PRINT_OPACITY_SHAPE_TAGS:
            continue
        for attr in ("opacity", "stroke-opacity", "fill-opacity"):
            raw = el.get(attr)
            if raw is None:
                continue
            try:
                o = float(str(raw).strip())
            except ValueError:
                continue
            if o < 1.0:
                el.set(attr, "1")


def _accent_css_hex(accent_hex: str) -> str:
    s = accent_hex.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) not in (6, 8):
        raise ValueError(f"bad accent hex for print recolor: {accent_hex!r}")
    return f"#{s[:6].lower()}"


def _hex_norm_6(h: str) -> str:
    s = h.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) >= 6:
        return s[:6].lower()
    raise ValueError(f"bad hex: {h!r}")


def _blend_hex(fg: str, bg: str, t: float) -> str:
    """Linear blend: t=0 → bg, t=1 → fg."""
    fg = _hex_norm_6(fg)
    bg = _hex_norm_6(bg)
    rf, gf, bf = (int(fg[i : i + 2], 16) for i in (0, 2, 4))
    rb, gb, bb = (int(bg[i : i + 2], 16) for i in (0, 2, 4))
    r = max(0, min(255, round(rb + t * (rf - rb))))
    g = max(0, min(255, round(gb + t * (gf - gb))))
    b = max(0, min(255, round(bb + t * (bf - bb))))
    return f"#{r:02x}{g:02x}{b:02x}"


def _parse_rgb_channels(val: str) -> tuple[int, int, int] | None:
    v = val.strip()
    vl = v.lower()
    if vl.startswith("#"):
        h = _hex_norm_6(vl)
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    m = re.match(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)",
        v,
        flags=re.IGNORECASE,
    )
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None


def _is_explicit_white_paint(value: str) -> bool:
    """True only for literal white paints (not none / currentColor / gradients)."""
    v = value.strip()
    vl = v.lower()
    if vl in ("none", "transparent", "currentcolor"):
        return False
    if vl.startswith("url("):
        return False
    if vl in ("white", "#fff", "#ffffff"):
        return True
    if re.fullmatch(r"#[0-9a-f]{3}", vl) and vl[1] == vl[2] == vl[3] == "f":
        return True
    if re.fullmatch(r"#[0-9a-f]{6}", vl) and vl.lower() == "#ffffff":
        return True
    if re.fullmatch(r"#[0-9a-f]{8}", vl) and vl[1:7].lower() == "ffffff":
        return True
    return bool(
        re.fullmatch(
            r"rgba?\(\s*255\s*,\s*255\s*,\s*255(?:\s*,\s*[\d.]+\s*)?\)",
            vl,
            flags=re.IGNORECASE,
        )
    )


def _is_explicit_black_paint(value: str) -> bool:
    v = value.strip().lower()
    if v in ("black", "#000", "#000000"):
        return True
    if re.fullmatch(r"#[0-9a-f]{3}", v) and v[1] == v[2] == v[3] == "0":
        return True
    return bool(
        re.fullmatch(
            r"rgba?\(\s*0\s*,\s*0\s*,\s*0(?:\s*,\s*[\d.]+\s*)?\)",
            v,
            flags=re.IGNORECASE,
        )
    )


def _is_neutral_grey_paint(value: str) -> bool:
    """Near-neutral strokes/fills (not white/black) for accent substitution."""
    if value.strip().lower() in ("none", "transparent", "currentcolor"):
        return False
    if value.strip().startswith("url("):
        return False
    ch = _parse_rgb_channels(value)
    if ch is None:
        return False
    r, g, b = ch
    if max(r, g, b) - min(r, g, b) > 22:
        return False
    avg = (r + g + b) / 3.0
    return 38.0 < avg < 248.0 and not _is_explicit_white_paint(value) and not _is_explicit_black_paint(value)


def _is_soft_greyish_for_transparent_print(value: str) -> bool:
    """Slightly chromatic mid-tones still read as 'grey diagram' on paper; map to ink_dark."""
    if value.strip().lower() in ("none", "transparent", "currentcolor"):
        return False
    if value.strip().startswith("url("):
        return False
    ch = _parse_rgb_channels(value)
    if ch is None:
        return False
    r, g, b = ch
    if max(r, g, b) - min(r, g, b) > 55:
        return False
    avg = (r + g + b) / 3.0
    return 28.0 < avg < 252.0 and not _is_explicit_white_paint(value) and not _is_explicit_black_paint(value)


def _map_print_paint(
    value: str,
    *,
    generator: str | None,
    accent: str,
    ink_on_light: str | None,
    ink_dark: str | None,
    accent_soft: str | None,
    treat_white_as_transparent: bool = False,
    grey_fills_transparent: bool = False,
    paint_key: str | None = None,
    element_tag: str | None = None,
) -> str | None:
    """Return replacement color, or None to keep value."""
    if treat_white_as_transparent and ink_dark is not None:
        if _is_explicit_white_paint(value):
            pk = (paint_key or "").strip().lower()
            if pk == "fill":
                if (element_tag or "").lower() in ("text", "tspan"):
                    return ink_dark
                # Opener on accent: keep white fills as light ink (lattice dots, marks), not holes.
                if grey_fills_transparent:
                    return ink_dark
                return "none"
            return ink_dark
        if _is_explicit_black_paint(value):
            return ink_dark
        if _is_neutral_grey_paint(value) or _is_soft_greyish_for_transparent_print(value):
            if grey_fills_transparent and (paint_key or "").strip().lower() == "fill":
                et = (element_tag or "").lower()
                if et not in ("text", "tspan") and et == "rect":
                    return "none"
            return ink_dark
        return None

    if ink_on_light is None:
        if _is_explicit_white_paint(value):
            return accent
        return None

    # Print pipeline always passes ink_on_light = chapter_ink (or title_ink on openers): never map
    # white to raw accent for streams/roots/etc., or figure strokes read as "cover colour" vs body text.
    if _is_explicit_white_paint(value):
        return ink_on_light
    if _is_explicit_black_paint(value):
        return ink_dark or ink_on_light
    if _is_neutral_grey_paint(value):
        return accent_soft or ink_on_light
    return None


def _rewrite_style_paints(
    style: str,
    *,
    generator: str | None,
    accent: str,
    ink_on_light: str | None,
    ink_dark: str | None,
    accent_soft: str | None,
    treat_white_as_transparent: bool = False,
    grey_fills_transparent: bool = False,
    element_tag: str | None = None,
) -> str:
    out: list[str] = []
    for raw in style.split(";"):
        piece = raw.strip()
        if not piece:
            continue
        if ":" not in piece:
            out.append(piece)
            continue
        k, _, v = piece.partition(":")
        key = k.strip().lower()
        val = v.strip()
        if key in ("opacity", "stroke-opacity", "fill-opacity"):
            if treat_white_as_transparent and generator in ("lattices", "field"):
                try:
                    if float(val) < 1.0:
                        val = "1"
                except ValueError:
                    pass
        elif key in ("fill", "stroke", "stop-color", "color"):
            repl = _map_print_paint(
                val,
                generator=generator,
                accent=accent,
                ink_on_light=ink_on_light,
                ink_dark=ink_dark,
                accent_soft=accent_soft,
                treat_white_as_transparent=treat_white_as_transparent,
                grey_fills_transparent=grey_fills_transparent,
                paint_key=key,
                element_tag=element_tag,
            )
            if repl is not None:
                val = repl
        out.append(f"{k.strip()}: {val}")
    return "; ".join(out)


def recolor_svg_for_print(
    svg: str,
    accent_hex: str,
    *,
    generator: str | None = None,
    ink_on_light: str | None = None,
    ink_dark: str | None = None,
    accent_soft: str | None = None,
    canonical_two_ink: bool = False,
    treat_white_as_transparent: bool = False,
    grey_fills_transparent: bool = False,
) -> str:
    """
    Map whites (and optional greys/blacks for stacked zines) to accent-family inks.

    When ``canonical_two_ink`` is True for ``lattices`` / ``field`` / ``formulas``, collapse
    paints to two accent inks plus transparency (luminance split).

    When ``ink_on_light`` is set (print pipeline), whites map to ``ink_on_light`` and blacks to
    ``ink_dark`` for every generator; neutral greys map to ``accent_soft`` or ``ink_on_light``.
    When ``ink_on_light`` is unset, only explicit white is replaced with ``accent_hex``.

    When ``treat_white_as_transparent`` is True (print figures on HTML backgrounds), explicit
    white fills on shapes map to ``none`` (paper); ``text`` / ``tspan`` white fills map to
    ``ink_dark`` so formula operators stay visible. Strokes / greys / blacks map to ``ink_dark``;
    canonical two-ink flattening is skipped.

    When ``grey_fills_transparent`` is True (section title tiles: light ink on HTML accent),
    neutral / soft grey *fills* on non-text elements map to ``none`` so mid-tones do not paint a
    second “paper” layer over the accent.
    """
    accent = _accent_css_hex(accent_hex)
    root = ET.fromstring(_strip_xml_decl(svg).encode("utf-8"))
    use_canonical = (
        canonical_two_ink
        and not treat_white_as_transparent
        and generator in ("lattices", "field", "formulas", "streams")
        and ink_dark
    )
    if use_canonical:
        ink_mid = accent_soft or ink_on_light or ink_dark
        two_mode = {
            "lattices": "lattices_mono",
            "formulas": "formulas_flat",
            "field": "field_stack",
            "streams": "streams_flat",
        }[generator or ""]
        _two_ink_canonicalize_tree(root, ink_dark, ink_mid, mode=two_mode)
        if generator == "lattices":
            _flatten_lattices_residual_to_ink(root, ink_dark)
            _scrub_style_paint_blocks(root, ink_dark)
        elif generator == "field":
            _scrub_style_paint_blocks(root, ink_dark)
        body = ET.tostring(root, encoding="unicode")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + body

    for el in root.iter():
        el_tag = _local_tag(el.tag)
        for attr in ("fill", "stroke", "color", "stop-color"):
            v = el.get(attr)
            if not v:
                continue
            repl = _map_print_paint(
                v,
                generator=generator,
                accent=accent,
                ink_on_light=ink_on_light,
                ink_dark=ink_dark,
                accent_soft=accent_soft,
                treat_white_as_transparent=treat_white_as_transparent,
                grey_fills_transparent=grey_fills_transparent,
                paint_key=attr,
                element_tag=el_tag,
            )
            if repl is not None:
                el.set(attr, repl)
        st = el.get("style")
        if st:
            el.set(
                "style",
                _rewrite_style_paints(
                    st,
                    generator=generator,
                    accent=accent,
                    ink_on_light=ink_on_light,
                    ink_dark=ink_dark,
                    accent_soft=accent_soft,
                    treat_white_as_transparent=treat_white_as_transparent,
                    grey_fills_transparent=grey_fills_transparent,
                    element_tag=el_tag,
                ),
            )
    if grey_fills_transparent:
        _remove_light_full_viewport_rects(root, luminance_above=0.5)
        _scrub_high_luminance_fills_to_transparent(root, luminance_above=0.72)
        _ensure_accent_plate_under_opener(root, accent)
        if ink_dark:
            _force_single_chapter_ink_tree(root, ink_dark)
            # Embedded <img> SVG does not inherit HTML parent color; fix fill:currentColor for marks/digits.
            root.set("color", ink_dark)

    mono_body = (
        treat_white_as_transparent
        and not grey_fills_transparent
        and ink_on_light
        and ink_dark
        and ink_on_light == ink_dark
        and (accent_soft is None or accent_soft == ink_on_light)
    )
    if mono_body:
        _force_single_chapter_ink_tree(root, ink_on_light)

    if treat_white_as_transparent and ink_dark and generator in ("lattices", "field"):
        _normalize_print_diagram_opacity(root)
        _normalize_opacity_in_style_blocks(root)
        _scrub_style_paint_blocks(root, ink_dark)

    if grey_fills_transparent and generator == "field" and ink_dark:
        _field_opener_lift_dark_marker_paint(root, ink_dark, accent)
        _append_field_opener_light_ink_cascade(root, ink_dark)

    body = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body


def _strip_xml_decl(s: str) -> str:
    s = s.strip()
    if s.startswith("<?xml"):
        _, _, rest = s.partition("?>")
        return rest.strip()
    return s


def flip_svg_horizontal(svg_text: str) -> str:
    """Wrap root SVG contents in a group with scale(-1,1) about the horizontal center."""
    root = ET.fromstring(_strip_xml_decl(svg_text).encode("utf-8"))
    vb = root.get("viewBox")
    if vb:
        parts = re.split(r"[,\s]+", vb.strip())
        w = float(parts[2])
        cx = float(parts[0]) + w / 2.0
    else:
        w_str = root.get("width", "100").replace("mm", "").replace("px", "")
        w = float(re.sub(r"[^\d.]", "", w_str) or 100.0)
        cx = w / 2.0

    g = ET.Element(f"{{{SVG_NS}}}g")
    g.set("transform", f"translate({cx:.6f},0) scale(-1,1) translate({-cx:.6f},0)")
    for child in list(root):
        root.remove(child)
        g.append(child)
    root.append(g)
    body = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body


def flip_svg_file(path: Path, out: Path) -> None:
    out.write_text(flip_svg_horizontal(path.read_text(encoding="utf-8")), encoding="utf-8")


# Expose blend for build_print chapter colors (single source for accent ladders in print).
blend_hex_for_print = _blend_hex
