"""All-or-nothing config deployment, composed from context managers.

Each file is written with ``AtomicWrite`` (old-or-new, never half). The
release as a whole is made transactional with ``ExitStack``: every written
file pushes a rollback callback, and only a fully validated release pops
them off uncalled — the commit *is* ``pop_all()``. Any exception on the way
unwinds the stack, restoring every file already touched.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from contextlib import ExitStack
from pathlib import Path

from patterns.modern.context_manager.pattern import AtomicWrite

Validator = Callable[[str, str], None]


class ReleaseError(RuntimeError):
    """A file in the release failed validation; nothing was deployed."""


def _restore(path: Path, previous: str | None) -> None:
    if previous is None:
        path.unlink()  # the file did not exist before this release
    else:
        path.write_text(previous, encoding="utf-8")


def no_validation(name: str, content: str) -> None:
    """The default validator: accept everything."""


def require_nonempty(name: str, content: str) -> None:
    """A realistic validator: an empty config file is a broken release."""
    if not content.strip():
        raise ReleaseError(f"{name} is empty")


def deploy(
    release: Mapping[str, str],
    target: Path,
    *,
    validate: Validator = no_validation,
) -> list[Path]:
    """Write every file in ``release`` into ``target``, or none of them."""
    written: list[Path] = []
    with ExitStack() as rollback:
        for name, content in sorted(release.items()):
            validate(name, content)
            path = target / name
            previous = path.read_text(encoding="utf-8") if path.exists() else None
            with AtomicWrite(path) as handle:
                handle.write(content)
            rollback.callback(_restore, path, previous)  # undo, if we unwind
            written.append(path)
        rollback.pop_all()  # every file landed: cancel the rollbacks
    return written
