"""Document exporters built on the Visitor pattern.

Run it: ``uv run python -m patterns.behavioral.visitor.examples.doc_exporters``
"""

from patterns.behavioral.visitor.examples.doc_exporters.exporters import (
    markdown,
    plain_text,
    word_count,
)
from patterns.behavioral.visitor.examples.doc_exporters.nodes import (
    Block,
    BulletList,
    CodeBlock,
    Document,
    Paragraph,
    Section,
)

__all__ = [
    "Block",
    "BulletList",
    "CodeBlock",
    "Document",
    "Paragraph",
    "Section",
    "markdown",
    "plain_text",
    "word_count",
]
