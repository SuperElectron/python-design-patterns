"""``io.TextIOWrapper``: the stdlib's flagship adapter.

It wraps a binary stream and exposes the text-file interface -- your code
reads ``str`` while bytes flow underneath.
"""

from __future__ import annotations

import io


def read_as_text(binary_stream: io.BytesIO) -> str:
    """Adapt any binary stream to the text interface."""
    return io.TextIOWrapper(binary_stream, encoding="utf-8").read()


def main() -> None:
    binary = io.BytesIO("héllo bytes\n".encode())
    text = read_as_text(binary)
    print(f"adapted read -> {type(text).__name__}: {text!r}")


if __name__ == "__main__":
    main()
