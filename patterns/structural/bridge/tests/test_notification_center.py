"""Behavioral tests for the notification-center mini-project."""

from __future__ import annotations

import pytest

from patterns.structural.bridge.examples.notification_center.center import (
    NotificationCenter,
    TeamChannel,
)
from patterns.structural.bridge.examples.notification_center.main import main
from patterns.structural.bridge.pattern import EmailTransport, SlackTransport, SmsTransport


def build_center() -> tuple[NotificationCenter, SlackTransport, SmsTransport, EmailTransport]:
    slack, sms, email = SlackTransport(), SmsTransport(), EmailTransport()
    center = NotificationCenter()
    center.register(TeamChannel("platform", slack, "#platform-ops"))
    center.register(TeamChannel("payments", sms, "+1-555-0100"))
    center.register(TeamChannel("support", email, "support@example.com"))
    return center, slack, sms, email


class TestRouting:
    def test_alerts_reach_only_the_paged_teams(self) -> None:
        center, slack, sms, email = build_center()
        center.alert(["platform"], "critical", "db pool exhausted")
        assert len(slack.posts) == 1
        assert sms.messages == []
        assert email.outbox == []

    def test_each_team_hears_through_its_own_transport(self) -> None:
        center, slack, sms, _ = build_center()
        center.alert(["platform", "payments"], "critical", "db pool exhausted")
        assert "slack #platform-ops" in slack.posts[0]
        assert "sms +1-555-0100" in sms.messages[0]

    def test_digest_broadcasts_to_every_registered_team(self) -> None:
        center, slack, sms, email = build_center()
        center.broadcast_digest(["3 deploys"])
        assert len(slack.posts) == len(sms.messages) == len(email.outbox) == 1

    def test_reregistering_a_team_requires_explicit_replace(self) -> None:
        center, slack, _, email = build_center()
        with pytest.raises(ValueError, match="platform"):
            center.register(TeamChannel("platform", email, "platform@example.com"))
        center.register(TeamChannel("platform", email, "platform@example.com"), replace=True)
        center.alert(["platform"], "warn", "retrying")
        assert slack.posts == []
        assert "platform@example.com" in email.outbox[0]

    def test_alerting_an_unregistered_team_names_the_known_ones(self) -> None:
        center, *_ = build_center()
        with pytest.raises(KeyError, match="payments"):
            center.alert(["nope"], "critical", "who hears this?")

    def test_teams_lists_registrations(self) -> None:
        center, *_ = build_center()
        assert center.teams == ["payments", "platform", "support"]


class TestDemo:
    def test_main_prints_all_three_transports(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "slack #platform-ops" in out
        assert "sms +1-555-0100" in out
        assert "email to support@example.com" in out
