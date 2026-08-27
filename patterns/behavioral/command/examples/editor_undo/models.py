"""Domain type for the editor-undo mini-project: a mutable text buffer."""

from __future__ import annotations


class Document:
    """The receiver: commands operate on this buffer, it knows no history."""

    def __init__(self, text: str = "") -> None:
        self.text = text

    def insert(self, position: int, chunk: str) -> None:
        self.text = self.text[:position] + chunk + self.text[position:]

    def delete(self, position: int, length: int) -> str:
        """Remove and return ``length`` characters at ``position``."""
        removed = self.text[position : position + length]
        self.text = self.text[:position] + self.text[position + length :]
        return removed
