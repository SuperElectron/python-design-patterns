"""Behavioral tests for all three sentinel-object variants."""

from patterns.python.sentinel_object import naive, pythonic, real_world


class TestNaive:
    def test_in_band_sentinel_produces_plausible_garbage(self) -> None:
        # The bug on display: absent needle silently indexes text[-2].
        assert naive.last_char_before("hello", "z") == "l"

    def test_none_cache_cannot_hold_none(self) -> None:
        cache = naive.NoneCache()
        calls: list[str] = []
        cache.put("k", None)
        cache.get_or_compute("k", calls)
        cache.get_or_compute("k", calls)
        assert calls == ["k", "k"]  # recomputed on every access


class TestPythonic:
    def test_cache_distinguishes_stored_none_from_miss(self) -> None:
        cache = pythonic.Cache()
        cache.put("k", None)
        calls: list[str] = []
        assert cache.get_or_compute("k", lambda: calls.append("x")) is None
        assert calls == []

    def test_miss_computes_once(self) -> None:
        cache = pythonic.Cache()
        calls: list[str] = []

        def compute() -> object:
            calls.append("x")
            return 42

        assert cache.get_or_compute("k", compute) == 42
        assert cache.get_or_compute("k", compute) == 42
        assert calls == ["x"]

    def test_default_argument_three_ways(self) -> None:
        assert pythonic.greet("ada") == "hello ada"
        assert pythonic.greet("ada", None) == "ada"
        assert pythonic.greet("ada", "yo") == "yo ada"

    def test_null_object_never_raises(self) -> None:
        pythonic.NullLogger().log("anything")


class TestRealWorld:
    def test_missing_separates_no_default_from_none_default(self) -> None:
        assert not real_world.has_default("name")
        assert real_world.has_default("retries")
        assert real_world.has_default("tags")

    def test_iter_with_sentinel_stops_at_blank(self) -> None:
        assert real_world.read_until_blank(["a", "b", "", "c"]) == ["a", "b"]
