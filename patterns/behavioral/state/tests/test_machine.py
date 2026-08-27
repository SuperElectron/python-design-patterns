"""Behavioral tests for the State pattern's StateMachine."""

from __future__ import annotations

from enum import Enum, auto

import pytest

from patterns.behavioral.state import IllegalTransitionError, StateMachine, Step


class Phase(Enum):
    IDLE = auto()
    RUNNING = auto()
    DONE = auto()


TABLE = {
    (Phase.IDLE, "start"): Phase.RUNNING,
    (Phase.RUNNING, "finish"): Phase.DONE,
    (Phase.RUNNING, "abort"): Phase.IDLE,
}


class TestTransitions:
    def test_a_listed_event_moves_the_machine_and_returns_the_target(self) -> None:
        machine = StateMachine(Phase.IDLE, TABLE)
        assert machine.trigger("start") is Phase.RUNNING
        assert machine.state is Phase.RUNNING

    def test_an_unlisted_event_raises_and_names_the_allowed_ones(self) -> None:
        machine = StateMachine(Phase.IDLE, TABLE)
        with pytest.raises(IllegalTransitionError, match="start"):
            machine.trigger("finish")
        assert machine.state is Phase.IDLE  # never half-moves

    def test_can_reports_the_table_without_moving(self) -> None:
        machine = StateMachine(Phase.RUNNING, TABLE)
        assert machine.can("finish")
        assert machine.can("abort")
        assert not machine.can("start")
        assert machine.state is Phase.RUNNING


class TestGuards:
    def test_a_failing_guard_vetoes_a_listed_transition(self) -> None:
        armed = False
        machine = StateMachine(Phase.IDLE, TABLE, guards={(Phase.IDLE, "start"): lambda: armed})
        with pytest.raises(IllegalTransitionError, match="guard"):
            machine.trigger("start")

    def test_a_passing_guard_lets_the_transition_through(self) -> None:
        machine = StateMachine(Phase.IDLE, TABLE, guards={(Phase.IDLE, "start"): lambda: True})
        assert machine.trigger("start") is Phase.RUNNING

    def test_can_consults_the_guard_too(self) -> None:
        machine = StateMachine(Phase.IDLE, TABLE, guards={(Phase.IDLE, "start"): lambda: False})
        assert not machine.can("start")


class TestLog:
    def test_every_transition_is_recorded_in_order(self) -> None:
        machine = StateMachine(Phase.IDLE, TABLE)
        machine.trigger("start")
        machine.trigger("abort")
        machine.trigger("start")
        assert machine.log == [
            Step(Phase.IDLE, "start", Phase.RUNNING),
            Step(Phase.RUNNING, "abort", Phase.IDLE),
            Step(Phase.IDLE, "start", Phase.RUNNING),
        ]

    def test_refused_transitions_leave_no_log_entry(self) -> None:
        machine = StateMachine(Phase.IDLE, TABLE)
        with pytest.raises(IllegalTransitionError):
            machine.trigger("finish")
        assert machine.log == []
