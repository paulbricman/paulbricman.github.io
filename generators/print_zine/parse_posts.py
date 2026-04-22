"""Load zine post bodies and split into prose segments + illustration paths."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import markdown

from series_spec import ZineChapterSpec, posts_dir, repo_root

# Separator div with optional classes/inline style; img may have extra attributes.
_SEPARATOR_BLOCK = re.compile(
    r"<div\s+class=\"separator[^\"]*\"[^>]*>\s*<img\s+[^>]*src=\"([^\"]+)\"[^>]*>\s*</div>",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class TextImagePair:
    prose_markdown: str
    """Web path starting with / or site-relative generators/..."""

    image_src: str | None
    """None => second page of spread is blank (e.g. closing prose only)."""


def _strip_yaml_front_matter(raw: str) -> str:
    if not raw.startswith("---"):
        return raw
    rest = raw[3:].lstrip("\n")
    end = rest.find("\n---")
    if end == -1:
        return raw
    after = rest[end + 4 :]
    if after.startswith("\n"):
        after = after[1:]
    elif after.startswith("\r\n"):
        after = after[2:]
    return after.lstrip()


def _md_to_html_fragment(md: str) -> str:
    md = md.strip()
    if not md:
        return ""
    return markdown.markdown(
        md,
        extensions=["extra", "smarty"],
        output_format="html5",
    )


def _web_src_to_repo_path(src: str) -> Path:
    s = src.strip()
    if s.startswith("/"):
        s = s[1:]
    return repo_root() / s


def parse_chapter_body(spec: ZineChapterSpec) -> list[TextImagePair]:
    path = posts_dir() / spec.post_filename
    raw = path.read_text(encoding="utf-8")
    body = _strip_yaml_front_matter(raw)

    pairs: list[TextImagePair] = []
    pos = 0
    for m in _SEPARATOR_BLOCK.finditer(body):
        chunk = body[pos : m.start()]
        src = m.group(1).strip()
        pairs.append(TextImagePair(prose_markdown=chunk, image_src=src))
        pos = m.end()

    tail = body[pos:]
    if tail.strip():
        pairs.append(TextImagePair(prose_markdown=tail, image_src=None))

    return pairs


def _unwrap_links(html: str) -> str:
    """Print: keep anchor text only, no link styling or URLs."""
    if not html or "<a" not in html.lower():
        return html
    return re.sub(
        r"<a\s[^>]*>(.*?)</a>",
        r"\1",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def prose_html(pair: TextImagePair) -> str:
    return _unwrap_links(_md_to_html_fragment(pair.prose_markdown))


def image_repo_path(pair: TextImagePair) -> Path | None:
    if not pair.image_src:
        return None
    return _web_src_to_repo_path(pair.image_src)


def validate_image_paths(pairs: list[TextImagePair]) -> list[str]:
    errors: list[str] = []
    for i, p in enumerate(pairs):
        if p.image_src:
            rp = image_repo_path(p)
            if rp is None or not rp.is_file():
                errors.append(f"missing image segment {i}: {p.image_src}")
    return errors
