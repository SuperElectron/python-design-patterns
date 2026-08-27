"""Template Method in its Python form: a fixed spine, steps as data.

The classic pattern fixes an algorithm's skeleton in a base class and defers
steps to subclass hooks. Here the skeleton is ``run`` and the steps are
fields — varying a step is constructing (or ``with_steps``-ing) a value,
not declaring a class.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import Generic, TypeVar

Raw = TypeVar("Raw")
Out = TypeVar("Out")


@dataclass(frozen=True)
class Skeleton(Generic[Raw, Out]):
    """A four-step algorithm spine: fetch → transform → render → deliver.

    The spine never varies; every step does. ``run`` is the template method.
    """

    fetch: Callable[[], Raw]
    transform: Callable[[Raw], Raw]
    render: Callable[[Raw], Out]
    deliver: Callable[[Out], None]

    def run(self) -> Out:
        """Execute the fixed skeleton; return what was delivered."""
        document = self.render(self.transform(self.fetch()))
        self.deliver(document)
        return document

    def with_steps(
        self,
        *,
        fetch: Callable[[], Raw] | None = None,
        transform: Callable[[Raw], Raw] | None = None,
        render: Callable[[Raw], Out] | None = None,
        deliver: Callable[[Out], None] | None = None,
    ) -> Skeleton[Raw, Out]:
        """A copy with some steps swapped — variation without subclassing."""
        return replace(
            self,
            fetch=fetch if fetch is not None else self.fetch,
            transform=transform if transform is not None else self.transform,
            render=render if render is not None else self.render,
            deliver=deliver if deliver is not None else self.deliver,
        )


def keep_all(rows: Raw) -> Raw:
    """The identity transform — the explicit 'this step does nothing' hook."""
    return rows


def discard(document: Out) -> None:
    """The no-op delivery — run for the return value alone."""
