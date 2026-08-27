"""The mini-project: a document where every character carries a style.

The GoF book's own motivating example, made measurable. Intrinsic state
(font, size, weight) is interned in a ``StyleBook``; extrinsic state (the
character, its position) stays with each occurrence. A million-character
document holds a handful of ``Style`` objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from patterns.structural.flyweight.pattern import InternPool

StyleKey = tuple[str, int, str]  # (font, size, weight)


@dataclass(frozen=True)
class Style:
    """Intrinsic, shared, immutable — the flyweight."""

    font: str
    size: int
    weight: str


@dataclass(frozen=True)
class Glyph:
    """One occurrence: extrinsic state plus a reference to the shared style."""

    char: str
    style: Style


class StyleBook:
    """The intern pool with a domain face: ask for a style, share the object."""

    def __init__(self) -> None:
        self._pool: InternPool[StyleKey, Style] = InternPool(lambda key: Style(*key), strict=True)

    def get(self, font: str, size: int, weight: str = "regular") -> Style:
        return self._pool.get((font, size, weight))

    @property
    def distinct_styles(self) -> int:
        return len(self._pool)


class Document:
    """A text buffer whose glyphs share their styles."""

    def __init__(self, styles: StyleBook | None = None) -> None:
        self.styles = styles if styles is not None else StyleBook()
        self.glyphs: list[Glyph] = []

    def write(self, text: str, *, font: str, size: int, weight: str = "regular") -> None:
        style = self.styles.get(font, size, weight)  # one lookup per run of text
        self.glyphs.extend(Glyph(char, style) for char in text)

    def __len__(self) -> int:
        return len(self.glyphs)
