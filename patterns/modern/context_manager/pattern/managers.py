"""Context managers as importable, typed building blocks.

Two general-purpose managers, one per construction form the pattern offers:
``AtomicWrite`` implements the protocol (``__enter__``/``__exit__``) because
its exit logic branches on the exception; ``temporarily`` uses the generator
form because its cleanup is one unconditional restore. Choosing the form to
fit the cleanup is itself part of the pattern.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import TracebackType
from typing import IO, Any


class AtomicWrite:
    """Write a file so readers see the old content or the new — never half.

    Text is written to a temp file beside ``path``; a clean exit renames it
    over ``path`` (atomic on POSIX), an exception discards it and leaves any
    previous content untouched.
    """

    def __init__(self, path: Path, *, encoding: str = "utf-8") -> None:
        self._path = path
        self._encoding = encoding
        self._handle: IO[str] | None = None
        self._tmp_name = ""

    def __enter__(self) -> IO[str]:
        fd, self._tmp_name = tempfile.mkstemp(dir=self._path.parent, prefix=f".{self._path.name}.")
        self._handle = os.fdopen(fd, "w", encoding=self._encoding)
        return self._handle

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        # Returning None (falsy): never swallow the body's exception.
        if self._handle is not None:
            self._handle.close()
        if exc_type is None:
            os.replace(self._tmp_name, self._path)  # the atomic commit
        else:
            os.unlink(self._tmp_name)  # discard; the old file stays intact


@contextmanager
def temporarily(obj: Any, attribute: str, value: object) -> Iterator[None]:
    """Set ``obj.attribute = value`` for the block; restore on any exit.

    The ``yield`` sits inside ``try/finally`` — without that, an exception
    in the body would skip the restore (the unit's first caveat).
    """
    previous = getattr(obj, attribute)
    setattr(obj, attribute, value)
    try:
        yield
    finally:
        setattr(obj, attribute, previous)
