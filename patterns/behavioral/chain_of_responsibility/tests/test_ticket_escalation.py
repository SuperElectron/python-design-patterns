"""Behavioral tests for the ticket-escalation mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.__main__ import main
from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.handlers import (
    build_escalation_chain,
    route,
)
from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.models import Ticket


def ticket(severity: int, tags: frozenset[str] = frozenset(), id_: str = "T-1") -> Ticket:
    return Ticket(id_, "subject", severity, tags)


class TestRouting:
    def test_faq_topics_are_answered_by_the_bot(self) -> None:
        resolution = route(ticket(1, frozenset({"password-reset"})))
        assert resolution.team == "bot"
        assert "KB-101" in resolution.action

    def test_routine_tickets_go_to_helpdesk(self) -> None:
        assert route(ticket(2)).team == "helpdesk"

    def test_defects_page_engineering(self) -> None:
        assert route(ticket(4, frozenset({"bug"}))).team == "on-call"

    def test_outages_jump_the_queue_regardless_of_severity(self) -> None:
        low_severity_outage = ticket(2, frozenset({"outage"}))
        assert route(low_severity_outage).team == "incident"

    def test_severity_five_is_an_incident_without_any_tag(self) -> None:
        assert route(ticket(5)).team == "incident"

    def test_unclaimed_tickets_fall_back_to_human_triage(self) -> None:
        feature_idea = ticket(0)
        resolution = route(feature_idea)
        assert resolution.team == "triage"
        assert resolution.ticket_id == feature_idea.id

    def test_faq_beats_outage_because_the_bot_is_first(self) -> None:
        both = ticket(5, frozenset({"password-reset", "outage"}))
        assert route(both).team == "bot"


class TestChainShape:
    def test_the_policy_is_four_handlers_in_documented_order(self) -> None:
        chain = build_escalation_chain()
        assert [h.__name__ for h in chain] == [
            "auto_responder",
            "incident_commander",
            "helpdesk",
            "engineering_on_call",
        ]


class TestDemo:
    def test_main_routes_the_sample_inbox(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "T-1" in out and "bot" in out
        assert "T-4" in out and "incident" in out
        assert "T-5" in out and "triage" in out
