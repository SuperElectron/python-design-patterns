"""A text editor's undo/redo built on the Command pattern.

Run it: ``uv run python -m patterns.behavioral.command.examples.editor_undo``
"""

from patterns.behavioral.command.examples.editor_undo.editing import (
    delete_span,
    insert_text,
    replace_span,
)
from patterns.behavioral.command.examples.editor_undo.models import Document

__all__ = ["Document", "delete_span", "insert_text", "replace_span"]
