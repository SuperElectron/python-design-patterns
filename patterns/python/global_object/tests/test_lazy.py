"""Behavioral tests for the pattern's Lazy global."""

from __future__ import annotations

from patterns.python.global_object import Lazy


class TestLazy:
    def test_construction_does_not_run_the_factory(self) -> None:
        runs: list[int] = []

        def factory() -> str:
            runs.append(1)
            return "value"

        lazy = Lazy(factory)
        assert runs == []
        assert lazy.initialized is False

    def test_first_get_builds_exactly_once(self) -> None:
        runs: list[int] = []

        def factory() -> str:
            runs.append(1)
            return "value"

        lazy = Lazy(factory)
        assert lazy.get() == "value"
        assert lazy.get() == "value"
        assert runs == [1]
        assert lazy.initialized is True

    def test_reset_forces_a_rebuild(self) -> None:
        counter = iter(range(100))
        lazy = Lazy(lambda: next(counter))
        assert lazy.get() == 0
        lazy.reset()
        assert lazy.initialized is False
        assert lazy.get() == 1

    def test_none_is_a_legitimate_lazy_value(self) -> None:
        runs: list[int] = []

        def factory() -> None:
            runs.append(1)

        lazy: Lazy[None] = Lazy(factory)
        assert lazy.get() is None
        assert lazy.get() is None
        assert runs == [1]  # a stored None is not mistaken for "unbuilt"
