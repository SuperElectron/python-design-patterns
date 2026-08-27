"""Behavioral tests for the shared-instance accessor."""

from patterns.creational.singleton.pattern import Shared


class Counter:
    built = 0

    def __init__(self) -> None:
        type(self).built += 1


class TestShared:
    def setup_method(self) -> None:
        Counter.built = 0

    def test_same_instance_every_get(self) -> None:
        shared = Shared(Counter)
        assert shared.get() is shared.get()

    def test_factory_runs_once(self) -> None:
        shared = Shared(Counter)
        shared.get()
        shared.get()
        assert Counter.built == 1

    def test_build_is_lazy(self) -> None:
        shared = Shared(Counter)
        assert not shared.built
        assert Counter.built == 0
        shared.get()
        assert shared.built

    def test_reset_builds_fresh_next_time(self) -> None:
        shared = Shared(Counter)
        first = shared.get()
        shared.reset()
        assert not shared.built
        assert shared.get() is not first
        assert Counter.built == 2
