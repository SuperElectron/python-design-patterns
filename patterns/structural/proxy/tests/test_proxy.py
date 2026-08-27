"""Behavioral tests for all three proxy variants."""

from patterns.structural.proxy import naive, pythonic, real_world


class TestNaive:
    def test_construction_is_deferred_until_first_use(self) -> None:
        before = naive.ExpensiveReport.instances_built
        proxy = naive.ReportProxy()
        assert naive.ExpensiveReport.instances_built == before
        assert proxy.summary() == "42 pages of insight"
        assert naive.ExpensiveReport.instances_built == before + 1

    def test_repeat_calls_reuse_the_subject(self) -> None:
        before = naive.ExpensiveReport.instances_built
        proxy = naive.ReportProxy()
        proxy.summary()
        proxy.summary()
        assert naive.ExpensiveReport.instances_built == before + 1


class TestPythonic:
    def test_lazy_proxy_defers_then_forwards(self) -> None:
        built: list[str] = []

        def factory() -> object:
            built.append("x")
            return "abc"

        proxy = pythonic.LazyProxy(factory)
        assert built == []
        assert proxy.upper() == "ABC"
        assert proxy.startswith("a")
        assert built == ["x"]  # built exactly once

    def test_cached_property_computes_once(self) -> None:
        data = pythonic.Dataset([3, 1, 4])
        assert data.stats == (1, 4)
        assert data.stats == (1, 4)
        assert data.computations == 1


class TestRealWorld:
    def test_live_weakref_proxy_forwards(self) -> None:
        assert real_world.live_proxy_forwards() == "pong"

    def test_dead_weakref_proxy_raises(self) -> None:
        assert real_world.dead_proxy_raises()
