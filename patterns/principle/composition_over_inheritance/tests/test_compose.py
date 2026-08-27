"""Behavioral tests for the pattern's Pipeline core and the composed Logger."""

from __future__ import annotations

from patterns.principle.composition_over_inheritance import (
    Filter,
    Logger,
    Pipeline,
    identity,
)


def contains(pattern: str) -> Filter[str]:
    def accepts(message: str) -> bool:
        return pattern in message

    return accepts


class Recording:
    """A stateful filter that remembers everything it was asked about."""

    def __init__(self, verdict: bool = True) -> None:
        self.verdict = verdict
        self.asked: list[str] = []

    def __call__(self, message: str) -> bool:
        self.asked.append(message)
        return self.verdict


class TestPipeline:
    def test_delivers_the_transformed_item_when_all_filters_accept(self) -> None:
        out: list[str] = []
        pipe: Pipeline[str, str] = Pipeline(
            filters=(contains("error"),), transform=str.upper, sink=out.append
        )
        assert pipe.process("error: disk full") is True
        assert out == ["ERROR: DISK FULL"]

    def test_one_rejecting_filter_blocks_delivery(self) -> None:
        out: list[str] = []
        pipe: Pipeline[str, str] = Pipeline(
            filters=(contains("error"), contains("disk")), transform=identity, sink=out.append
        )
        assert pipe.process("error: bad password") is False
        assert out == []

    def test_filters_short_circuit_in_declaration_order(self) -> None:
        # Order is behavior: a stateful filter placed after a veto must never
        # even be consulted for the vetoed item.
        recorder = Recording()
        pipe: Pipeline[str, str] = Pipeline(
            filters=(contains("error"), recorder), transform=identity, sink=lambda _line: None
        )
        pipe.process("all fine")
        assert recorder.asked == []  # vetoed before the recorder saw it
        pipe.process("error: disk full")
        assert recorder.asked == ["error: disk full"]

    def test_identity_is_a_real_transform(self) -> None:
        assert identity("unchanged") == "unchanged"


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
        assert logger.sink == ["anything"]  # default transform is identity
