"""Behavioral tests for the bridge building block: axes compose freely."""

from __future__ import annotations

from patterns.structural.bridge import (
    AlertNotifier,
    DigestNotifier,
    EmailTransport,
    SlackTransport,
    SmsTransport,
    Transport,
)


class TestAxesCompose:
    def test_any_notifier_works_over_any_transport(self) -> None:
        # 2 notifiers x 3 transports: every combination must actually deliver.
        email, slack, sms = EmailTransport(), SlackTransport(), SmsTransport()
        channels: list[tuple[Transport, list[str]]] = [
            (email, email.outbox),
            (slack, slack.posts),
            (sms, sms.messages),
        ]
        for transport, delivered in channels:
            AlertNotifier(transport, "ops").alert("critical", "disk full")
            DigestNotifier(transport, "ops").digest(["a", "b"])
            assert len(delivered) == 2
            assert "[CRITICAL] disk full" in delivered[0]
            assert "2 updates" in delivered[1]

    def test_alert_formats_severity_upfront(self) -> None:
        slack = SlackTransport()
        AlertNotifier(slack, "#ops").alert("critical", "db pool exhausted")
        assert slack.posts == ["slack #ops: [CRITICAL] db pool exhausted"]

    def test_digest_summarizes_item_count(self) -> None:
        email = EmailTransport()
        DigestNotifier(email, "team@example.com").digest(["3 deploys", "1 rollback"])
        assert email.outbox == ["email to team@example.com: 2 updates: 3 deploys; 1 rollback"]

    def test_sms_transport_truncates_long_texts(self) -> None:
        sms = SmsTransport()
        AlertNotifier(sms, "+15550100").alert("info", "x" * 200)
        (message,) = sms.messages
        assert len(message) <= len("sms +15550100: ") + SmsTransport.MAX_LEN


class TestBridgeIsOneReference:
    def test_a_new_transport_needs_no_notifier_changes(self) -> None:
        received: list[tuple[str, str]] = []

        class PagerTransport:
            def deliver(self, recipient: str, text: str) -> None:
                received.append((recipient, text))

        AlertNotifier(PagerTransport(), "oncall").alert("critical", "it's down")
        assert received == [("oncall", "[CRITICAL] it's down")]
