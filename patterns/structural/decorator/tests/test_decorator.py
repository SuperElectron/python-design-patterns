"""Behavioral tests for all three decorator variants."""

import io

from patterns.structural.decorator import naive, pythonic, real_world


class TestNaive:
    def test_augments_write_and_forwards_content(self) -> None:
        buffer = io.StringIO()
        writer = naive.LoggingWriter(buffer)
        writer.write("a")
        writer.write("b")
        assert writer.writes == 2
        assert buffer.getvalue() == "ab"

    def test_unaugmented_methods_are_forwarded(self) -> None:
        writer = naive.LoggingWriter(io.StringIO())
        writer.write("xyz")
        assert writer.getvalue() == "xyz"  # forwarded via __getattr__

    def test_wrapping_does_not_fool_isinstance(self) -> None:
        assert not isinstance(naive.LoggingWriter(io.StringIO()), io.StringIO)


class TestPythonic:
    def test_count_calls_counts(self) -> None:
        @pythonic.count_calls
        def f() -> int:
            return 1

        f(), f(), f()
        assert f.calls == 3  # type: ignore[attr-defined]

    def test_wraps_preserves_metadata(self) -> None:
        assert pythonic.greet.__name__ == "greet"
        assert pythonic.greet.__doc__ == "Say hello."

    def test_parameterized_decorator(self) -> None:
        assert pythonic.beep() == ["beep", "beep", "beep"]


class TestRealWorld:
    def test_lru_cache_memoizes(self) -> None:
        real_world.fib.cache_clear()
        assert real_world.fib(30) == 832040
        hits_before = real_world.fib.cache_info().hits
        real_world.fib(30)
        assert real_world.fib.cache_info().hits == hits_before + 1
