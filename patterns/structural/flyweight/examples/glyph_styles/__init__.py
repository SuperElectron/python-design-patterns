"""A text buffer sharing character styles through an intern pool.

Run it: ``uv run python -m patterns.structural.flyweight.examples.glyph_styles``
"""

from patterns.structural.flyweight.examples.glyph_styles.document import (
    Document,
    Style,
    StyleBook,
)

__all__ = ["Document", "Style", "StyleBook"]
