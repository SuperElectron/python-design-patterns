"""Behavioral tests for the feed-client mini-project."""

from patterns.creational.factory_method.examples.feed_client import (
    DigestClient,
    DigestResponse,
    FeedClient,
    FeedResponse,
)

FEED = "Storm warning|Heavy rain expected tonight\nNew library opens|Doors open at nine"


def canned(url: str) -> str:
    return FEED


class TestFrameworkSlot:
    def test_stock_client_builds_stock_responses(self) -> None:
        response = FeedClient(canned).fetch("news://x")
        assert type(response) is FeedResponse
        assert response.titles() == ["Storm warning", "New library opens"]

    def test_subclass_swaps_the_response_type(self) -> None:
        response = DigestClient(canned).fetch("news://x")
        assert isinstance(response, DigestResponse)
        assert response.digest() == "Storm warning (4w); New library opens (4w)"

    def test_instance_override_without_subclassing(self) -> None:
        class Canary(FeedResponse):
            pass

        client = FeedClient(canned, response_class=Canary)
        assert isinstance(client.fetch("news://x"), Canary)
        # ...and the framework default is untouched.
        assert type(FeedClient(canned).fetch("news://x")) is FeedResponse

    def test_transport_is_injected_not_built(self) -> None:
        calls: list[str] = []

        def spying(url: str) -> str:
            calls.append(url)
            return "A|b"

        FeedClient(spying).fetch("news://spied")
        assert calls == ["news://spied"]
