"""Behavioral tests for all three iterator variants."""

import pytest

from patterns.behavioral.iterator import naive, pythonic, real_world


class TestNaive:
    def test_yields_odds_up_to_maximum(self) -> None:
        assert list(naive.OddNumbers(7)) == [1, 3, 5, 7]

    def test_iterable_restarts_iterator_does_not(self) -> None:
        numbers = naive.OddNumbers(5)
        assert list(numbers) == list(numbers) == [1, 3, 5]
        it = iter(numbers)
        assert list(it) == [1, 3, 5]
        assert list(it) == []  # the iterator itself is exhausted

    def test_next_raises_stop_iteration_when_done(self) -> None:
        it = iter(naive.OddNumbers(1))
        assert next(it) == 1
        with pytest.raises(StopIteration):
            next(it)


class TestPythonic:
    def test_generator_function_matches_naive(self) -> None:
        assert list(pythonic.odd_numbers(7)) == [1, 3, 5, 7]

    def test_generator_dunder_iter_makes_class_iterable(self) -> None:
        assert list(pythonic.OddNumbers(9)) == [1, 3, 5, 7, 9]

    def test_generators_are_lazy(self) -> None:
        gen = pythonic.odd_numbers(10**12)  # instant: nothing computed yet
        assert next(gen) == 1


class TestRealWorld:
    def test_bounded_pipeline_over_infinite_source(self) -> None:
        assert list(real_world.first_n_odd_squares(4)) == [1, 9, 25, 49]
