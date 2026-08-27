"""A tiny feed-client framework whose response type is a class-attribute factory.

The framework (``FeedClient``) must build a response object mid-work, exactly
like ``http.client.HTTPConnection`` building its ``HTTPResponse``. Instead of
an abstract ``factory_method()`` and a subclass per choice, the factory is the
class attribute ``response_class`` — apps override it by subclass or
assignment, tests override it per instance, and the transport is injected
outright (the best dodge of all: pass the object).
"""

from __future__ import annotations

from collections.abc import Callable

from patterns.creational.factory_method.examples.feed_client.models import Article

#: A transport fetches raw feed text for a URL — injected, so no real network.
Transport = Callable[[str], str]


class FeedResponse:
    """Parses the wire format (title|body lines) into articles."""

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
