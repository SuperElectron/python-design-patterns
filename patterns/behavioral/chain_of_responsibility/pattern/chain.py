"""Chain of Responsibility as an importable, typed building block.

A handler is any callable that returns an answer or ``None`` to decline.
``Chain`` tries its handlers in order; the first non-``None`` answer wins.
What an unhandled request means is the caller's decision: ``handle`` raises,
``handle_or`` falls back to a default.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, TypeVar

Req = TypeVar("Req")
Res = TypeVar("Res")

Handler = Callable[[Req], "Res | None"]


class UnhandledRequestError(LookupError):
    """No handler in the chain accepted the request."""


class Chain(Generic[Req, Res]):
    """An ordered chain of handlers; the first non-``None`` answer wins."""

    def __init__(self, handlers: Iterable[Handler[Req, Res]] = ()) -> None:
        self._handlers: list[Handler[Req, Res]] = list(handlers)

    def register(self, handler: Handler[Req, Res]) -> Handler[Req, Res]:
        """Append a handler to the end of the chain; usable as a decorator."""
        self._handlers.append(handler)
        return handler

    def handle(self, request: Req) -> Res:
        """Return the first handler's answer; raise if every handler declines."""
        for handler in self._handlers:
            answer = handler(request)
            if answer is not None:
                return answer
        raise UnhandledRequestError(f"no handler accepted {request!r}")

    def handle_or(self, request: Req, default: Res) -> Res:
        """Like ``handle``, but fall back to ``default`` instead of raising."""
        try:
            return self.handle(request)
        except UnhandledRequestError:
            return default

    def __iter__(self) -> Iterator[Handler[Req, Res]]:
        return iter(self._handlers)

    def __len__(self) -> int:
        return len(self._handlers)
