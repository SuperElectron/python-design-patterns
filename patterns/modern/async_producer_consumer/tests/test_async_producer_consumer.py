"""Behavioral tests for all three producer/consumer variants."""

from patterns.modern.async_producer_consumer import naive, pythonic, real_world


class TestNaive:
    def test_thread_pool_processes_everything(self) -> None:
        assert naive.process_all(["a", "b", "c", "d"]) == ["A", "B", "C", "D"]

    def test_zero_items(self) -> None:
        assert naive.process_all([]) == []


class TestPythonic:
    async def test_all_items_processed_despite_backpressure(self) -> None:
        items = [chr(ord("a") + n) for n in range(10)]  # more items than maxsize
        assert await pythonic.process_all(items) == [c.upper() for c in items]

    async def test_more_workers_than_items(self) -> None:
        assert await pythonic.process_all(["x"], worker_count=5) == ["X"]

    async def test_zero_items_shuts_down_cleanly(self) -> None:
        assert await pythonic.process_all([]) == []


class TestRealWorld:
    async def test_crawl_collects_every_url(self) -> None:
        urls = [f"u{n}" for n in range(9)]
        pages = await real_world.crawl(urls, workers=3)
        assert pages == {u: f"body-of-{u}" for u in urls}

    async def test_injected_fetcher(self) -> None:
        async def fetch(url: str) -> str:
            return url[::-1]

        assert await real_world.crawl(["abc"], fetch=fetch) == {"abc": "cba"}
