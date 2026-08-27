"""Behavioral tests for the feed_fetcher mini-project."""

from __future__ import annotations

import pytest

from patterns.modern.async_producer_consumer.examples.feed_fetcher.fetcher import (
    fetch_all,
    summarize,
)
from patterns.modern.async_producer_consumer.examples.feed_fetcher.main import main
from patterns.modern.async_producer_consumer.examples.feed_fetcher.models import Feed
from patterns.modern.async_producer_consumer.pattern import Shutdown

FEEDS = [
    Feed("alpha", "https://feeds.example/alpha"),
    Feed("beta", "https://feeds.example/beta"),
    Feed("dead", "https://unreachable.example/rss"),
]


class TestFetchAll:
    @pytest.mark.parametrize("shutdown", list(Shutdown))
    async def test_failures_are_captured_not_raised(self, shutdown: Shutdown) -> None:
        outcomes = {o.feed.name: o for o in await fetch_all(FEEDS, shutdown=shutdown)}
        assert len(outcomes) == 3
        assert outcomes["alpha"].ok and outcomes["alpha"].entries == len("alpha")
        assert not outcomes["dead"].ok
        assert outcomes["dead"].error is not None
        assert "unreachable" in outcomes["dead"].error

    async def test_both_disciplines_agree_on_outcomes(self) -> None:
        by_discipline = [
            sorted((o.feed.name, o.ok) for o in await fetch_all(FEEDS, shutdown=s))
            for s in Shutdown
        ]
        assert by_discipline[0] == by_discipline[1]


class TestSummarize:
    async def test_reports_totals_and_failures(self) -> None:
        line = summarize(await fetch_all(FEEDS))
        assert "2 feeds" in line
        assert f"{len('alpha') + len('beta')} entries" in line
        assert "failed: dead" in line


class TestDemo:
    def test_demo_prints_one_line_per_discipline(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out.strip().splitlines()
        assert len(out) == len(Shutdown)
        assert any(line.startswith("sentinel:") for line in out)
        assert all("failed: dead-blog" in line for line in out)
