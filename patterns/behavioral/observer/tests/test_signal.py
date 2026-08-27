"""Behavioral tests for the Observer pattern's Signal."""

from __future__ import annotations

import pytest

from patterns.behavioral.observer import Signal, Subscriber


class TestBroadcast:
    def test_subscribers_are_notified_in_subscription_order(self) -> None:
        signal: Signal[int] = Signal()
        calls: list[str] = []
        signal.subscribe(lambda e: calls.append(f"first:{e}"))
        signal.subscribe(lambda e: calls.append(f"second:{e}"))
        signal.emit(7)
        assert calls == ["first:7", "second:7"]

    def test_subscribe_works_as_a_decorator(self) -> None:
        signal: Signal[str] = Signal()
        seen: list[str] = []

        @signal.subscribe
        def listener(event: str) -> None:
            seen.append(event)

        signal.emit("hello")
        assert seen == ["hello"]

    def test_unsubscribed_callables_stop_receiving(self) -> None:
        signal: Signal[int] = Signal()
        seen: list[int] = []
        subscriber: Subscriber[int] = seen.append
        signal.subscribe(subscriber)
        signal.emit(1)
        signal.unsubscribe(subscriber)
        signal.emit(2)
        assert seen == [1]

    def test_unsubscribing_a_stranger_raises(self) -> None:
        signal: Signal[int] = Signal()
        with pytest.raises(ValueError):
            signal.unsubscribe(print)

    def test_a_subscriber_may_unsubscribe_itself_mid_broadcast(self) -> None:
        signal: Signal[int] = Signal()
        seen: list[int] = []

        def once(event: int) -> None:
            seen.append(event)
            signal.unsubscribe(once)

        signal.subscribe(once)
        signal.subscribe(seen.append)  # must still run in the same emit
        signal.emit(1)
        signal.emit(2)
        assert seen == [1, 1, 2]


class TestFailurePolicy:
    def test_default_policy_propagates_and_stops_the_broadcast(self) -> None:
        signal: Signal[int] = Signal()
        reached: list[int] = []
        signal.subscribe(lambda e: (_ for _ in ()).throw(RuntimeError("boom")))
        signal.subscribe(reached.append)
        with pytest.raises(RuntimeError, match="boom"):
            signal.emit(1)
        assert reached == []  # fail fast means fail visibly

    def test_on_error_policy_isolates_and_keeps_notifying(self) -> None:
        quarantined: list[str] = []
        signal: Signal[int] = Signal(on_error=lambda err, sub: quarantined.append(str(err)))
        reached: list[int] = []

        def failing(event: int) -> None:
            raise ConnectionError("down")

        signal.subscribe(failing)
        signal.subscribe(reached.append)
        signal.emit(5)
        assert reached == [5]
        assert quarantined == ["down"]

    def test_error_policy_receives_the_offending_subscriber(self) -> None:
        offenders: list[Subscriber[int]] = []
        signal: Signal[int] = Signal(on_error=lambda err, sub: offenders.append(sub))

        def failing(event: int) -> None:
            raise ValueError

        signal.subscribe(failing)
        signal.emit(0)
        assert offenders == [failing]
