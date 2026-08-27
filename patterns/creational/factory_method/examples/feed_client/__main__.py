"""Demo: one client framework, three ways to swap what it builds."""

from __future__ import annotations

from patterns.creational.factory_method.examples.feed_client.client import (
    DigestClient,
    FeedClient,
    FeedResponse,
    StrictClient,
)

FEED = "Storm warning|Heavy rain expected tonight\nNew library opens|Doors open at nine"


def canned_transport(url: str) -> str:
    return FEED


def main() -> None:
    stock = FeedClient(canned_transport)
    print(f"stock response:    {stock.fetch('news://local').titles()}")

    digest = DigestClient(canned_transport)
    response = digest.fetch("news://local")
    print(f"subclass override: {type(response).__name__}")

    class UpperResponse(FeedResponse):
        def titles(self) -> list[str]:
            return [t.upper() for t in super().titles()]

    per_instance = FeedClient(canned_transport, response_class=UpperResponse)
    print(f"instance override: {per_instance.fetch('news://local').titles()}")

    strict = StrictClient(canned_transport)
    count = len(strict.fetch("news://local").articles)
    print(f"function slot:     {count} articles parsed strictly")


if __name__ == "__main__":
    main()
