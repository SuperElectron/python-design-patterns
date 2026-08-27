"""Behavioral tests for the decorator building blocks."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from patterns.structural.decorator.pattern import (
    RateLimitExceededError,
    logged,
    rate_limited,
    retry,
    timed,
)


def test_logged_reports_call_and_return() -> None:
    lines: list[str] = []

    @logged(lines.append)
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5
    assert lines == ["-> add", "<- add"]


def test_logged_reports_raise_and_reraises() -> None:
    lines: list[str] = []

    @logged(lines.append)
    def boom() -> None:
        raise ValueError("no")

    with pytest.raises(ValueError):
        boom()
    assert lines == ["-> boom", "!! boom raised ValueError"]


def test_timed_feeds_sink_with_injected_clock() -> None:
    ticks = iter([10.0, 10.25])
    seen: list[tuple[str, float]] = []

    @timed(lambda name, secs: seen.append((name, secs)), clock=lambda: next(ticks))
    def work() -> str:
        return "done"

    assert work() == "done"
    assert seen == [("work", 0.25)]


def test_retry_retries_then_succeeds() -> None:
    outcomes: Iterator[ConnectionError | str] = iter(
        [ConnectionError("x"), ConnectionError("y"), "ok"]
    )

    @retry(3, on=(ConnectionError,))
    def flaky() -> str:
        result = next(outcomes)
        if isinstance(result, Exception):
            raise result
        return result

    assert flaky() == "ok"


def test_retry_exhaustion_raises_last_error_after_exact_attempts() -> None:
    calls: list[int] = []

    @retry(3, on=(ConnectionError,))
    def always_down() -> None:
        calls.append(1)
        raise ConnectionError("still down")

    with pytest.raises(ConnectionError):
        always_down()
    assert len(calls) == 3


def test_retry_backoff_doubles_and_uses_injected_sleep() -> None:
    pauses: list[float] = []

    @retry(3, on=(ConnectionError,), wait=1.0, sleep=pauses.append)
    def always_down() -> None:
        raise ConnectionError("down")

    with pytest.raises(ConnectionError):
        always_down()
    assert pauses == [1.0, 2.0]


def test_retry_does_not_catch_unlisted_exceptions() -> None:
    @retry(3, on=(ConnectionError,))
    def wrong_kind() -> None:
        raise ValueError("not transient")

    with pytest.raises(ValueError):
        wrong_kind()


def test_rate_limited_allows_within_window_then_raises() -> None:
    now = [0.0]

    @rate_limited(2, window=10.0, clock=lambda: now[0])
    def ping() -> str:
        return "pong"

    assert ping() == "pong"
    assert ping() == "pong"
    with pytest.raises(RateLimitExceededError):
        ping()
    now[0] = 11.0  # window slides; capacity returns
    assert ping() == "pong"


def test_wraps_preserves_identity_through_a_stack() -> None:
    @logged(lambda _: None)
    @retry(2)
    def documented() -> None:
        """The docstring survives the stack."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "The docstring survives the stack."


def test_retry_refuses_a_nonsensical_attempt_count() -> None:
    with pytest.raises(ValueError, match="attempts"):
        retry(0)
