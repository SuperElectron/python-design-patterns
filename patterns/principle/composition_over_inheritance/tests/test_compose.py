"""Behavioral tests for the pattern's composed Logger and axis aliases."""

from __future__ import annotations

from patterns.principle.composition_over_inheritance import Filter, Logger


def contains(pattern: str) -> Filter[str]:
    def accepts(message: str) -> bool:
        return pattern in message

    return accepts


class TestComposedLogger:
    def test_behavior_comes_from_the_composed_pieces(self) -> None:
        loud_errors = Logger(filters=(contains("error"),), transform=str.upper)
        loud_errors.log("error: disk full")
        loud_errors.log("all fine")
        assert loud_errors.sink == ["ERROR: DISK FULL"]

    def test_a_new_combination_is_a_constructor_call_not_a_class(self) -> None:
        quiet = Logger(filters=(contains("error"), contains("disk")))
        quiet.log("error: disk full")
        quiet.log("error: bad password")  # fails the second filter
        assert quiet.sink == ["error: disk full"]
        assert type(quiet) is Logger  # same one class covers every combination

    def test_no_filters_means_everything_passes(self) -> None:
        logger = Logger()
        logger.log("anything")
        assert logger.sink == ["anything"]
