"""The Gang of Four Decorator: wrap an *object*, forward the rest.

A write-logging wrapper around a file-like object. ``__getattr__`` handles
wholesale forwarding so only the augmented method is written by hand -- the
Python mitigation of the book's forward-every-method tax.
"""

from __future__ import annotations

from typing import Any, TextIO


class LoggingWriter:
    """Wraps a file-like object; counts and logs writes, forwards the rest."""

    def __init__(self, wrapped: TextIO) -> None:
        self._wrapped = wrapped
        self.writes: int = 0

    def write(self, text: str) -> int:
        self.writes += 1
        return self._wrapped.write(text)

    def __getattr__(self, name: str) -> Any:
        # Everything we don't augment is forwarded untouched.
        return getattr(self._wrapped, name)


def main() -> None:
    import io

    buffer = io.StringIO()
    writer = LoggingWriter(buffer)
    writer.write("hello ")
    writer.write("world")
    print(f"writes seen: {writer.writes}")
    print(f"content:     {buffer.getvalue()!r}")
    print(f"isinstance survives wrapping: {isinstance(writer, io.StringIO)}")  # False!


if __name__ == "__main__":
    main()
