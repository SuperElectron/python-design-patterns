"""A tiny feed-client framework whose response type is a class-attribute factory.

The framework (``FeedClient``) must build a response object mid-work, exactly
like ``http.client.HTTPConnection`` building its ``HTTPResponse``. Instead of
an abstract ``factory_method()`` and a subclass per choice, the factory is the
class attribute ``response_class`` — apps override it with their own class in
a subclass, tests override it per instance, and the transport is injected
outright (the best dodge of all: pass the object).

Built on this unit's ``pattern`` package: ``factory_slot`` guards the one trap
(a plain *function* in a class body binds ``self``; classes are safe bare).
"""

from __future__ import annotations

from collections.abc import Callable

from patterns.creational.factory_method.examples.feed_client.models import Article
from patterns.creational.factory_method.pattern import factory_slot

#: A transport fetches raw feed text for a URL — injected, so no real network.
Transport = Callable[[str], str]


class FeedResponse:
    """Parses the wire format (``title|body`` lines) into articles.

    Lenient by policy: a line with no ``|`` becomes an ``Article`` with an
    empty body (feeds in the wild often carry title-only entries). Use
    ``StrictClient`` when malformed lines should fail loudly instead.
    """

    def __init__(self, raw: str) -> None:
        self.articles = [
            Article(title, body)
            for line in raw.splitlines()
            if line.strip()
            for title, _, body in [line.partition("|")]
        ]

    def titles(self) -> list[str]:
        return [a.title for a in self.articles]


class DigestResponse(FeedResponse):
    """An app's own response type: same parse, plus a one-line digest."""

    def digest(self) -> str:
        return "; ".join(f"{a.title} ({len(a.body.split())}w)" for a in self.articles)


def parse_strictly(raw: str) -> FeedResponse:
    """A plain-function factory: rejects any line missing the ``|`` separator."""
    for line in raw.splitlines():
        if line.strip() and "|" not in line:
            raise ValueError(f"malformed feed line (no '|'): {line!r}")
    return FeedResponse(raw)


class FeedClient:
    """The framework class. ``response_class`` is the factory-method slot."""

    response_class: Callable[[str], FeedResponse] = FeedResponse

    def __init__(
        self,
        transport: Transport,
        response_class: Callable[[str], FeedResponse] | None = None,
    ) -> None:
        self._transport = transport
        # Per-instance override — no subclass needed (e.g. a test double).
        if response_class is not None:
            self.response_class = response_class

    def fetch(self, url: str) -> FeedResponse:
        return self.response_class(self._transport(url))


class DigestClient(FeedClient):
    """An app subclass: one line swaps what the framework builds."""

    response_class = DigestResponse


class StrictClient(FeedClient):
    """A subclass slotting in a plain *function* — hence ``factory_slot``.

    Bare assignment here would bind the function as a method and every fetch
    would raise ``TypeError``; the wrapper from ``pattern/`` prevents that.
    """

    response_class = factory_slot(parse_strictly)
