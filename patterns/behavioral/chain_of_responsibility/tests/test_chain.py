"""Behavioral tests for the Chain building block."""

from __future__ import annotations

import pytest

from patterns.behavioral.chain_of_responsibility import (
    Chain,
    Handler,
    UnhandledRequestError,
)


def helpdesk(severity: int) -> str | None:
    return "helpdesk" if severity <= 1 else None


def engineer(severity: int) -> str | None:
    return "engineer" if severity <= 3 else None


def management(severity: int) -> str | None:
    return "management" if severity <= 5 else None


class TestDispatch:
    def test_first_capable_handler_wins(self) -> None:
        chain: Chain[int, str] = Chain([helpdesk, engineer, management])
        assert chain.handle(1) == "helpdesk"
        assert chain.handle(3) == "engineer"
        assert chain.handle(5) == "management"

    def test_order_is_policy(self) -> None:
        reordered: Chain[int, str] = Chain([management, helpdesk])
        assert reordered.handle(1) == "management"

    def test_declining_handlers_are_skipped_not_consulted_again(self) -> None:
        calls: list[str] = []

        def declines(severity: int) -> str | None:
            calls.append("declines")
            return None

        def answers(severity: int) -> str | None:
            calls.append("answers")
            return "ok"

        def never_reached(severity: int) -> str | None:  # pragma: no cover
            calls.append("never")
            return "late"

        chain: Chain[int, str] = Chain([declines, answers, never_reached])
        assert chain.handle(1) == "ok"
        assert calls == ["declines", "answers"]


class TestUnhandledPolicy:
    def test_handle_raises_with_the_request_in_the_message(self) -> None:
        chain: Chain[int, str] = Chain([helpdesk])
        with pytest.raises(UnhandledRequestError, match="9"):
            chain.handle(9)

    def test_handle_or_falls_back_to_default(self) -> None:
        chain: Chain[int, str] = Chain([helpdesk])
        assert chain.handle_or(9, "triage") == "triage"

    def test_empty_chain_is_explicitly_unhandled(self) -> None:
        empty: Chain[int, str] = Chain()
        with pytest.raises(UnhandledRequestError):
            empty.handle(1)


class TestRegistration:
    def test_register_appends_and_returns_the_handler(self) -> None:
        chain: Chain[int, str] = Chain([helpdesk])
        returned = chain.register(engineer)
        assert returned is engineer
        assert list(chain) == [helpdesk, engineer]
        assert chain.handle(3) == "engineer"

    def test_register_works_as_a_decorator(self) -> None:
        chain: Chain[int, str] = Chain()

        @chain.register
        def catch_all(severity: int) -> str | None:
            return "caught"

        handler: Handler[int, str] = catch_all
        assert handler(0) == "caught"
        assert len(chain) == 1
        assert chain.handle(99) == "caught"
