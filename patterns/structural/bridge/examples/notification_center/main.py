"""Demo: one incident and one digest, three teams, three transports."""

from __future__ import annotations

from patterns.structural.bridge.examples.notification_center.center import (
    NotificationCenter,
    TeamChannel,
)
from patterns.structural.bridge.pattern import EmailTransport, SlackTransport, SmsTransport


def main() -> None:
    slack, email, sms = SlackTransport(), EmailTransport(), SmsTransport()

    center = NotificationCenter()
    center.register(TeamChannel("platform", slack, "#platform-ops"))
    center.register(TeamChannel("payments", sms, "+1-555-0100"))
    center.register(TeamChannel("support", email, "support@example.com"))

    center.alert(["platform", "payments"], "critical", "db connection pool exhausted")
    center.broadcast_digest(["3 deploys", "1 rollback", "error budget at 92%"])

    for line in (*slack.posts, *sms.messages, *email.outbox):
        print(line)


if __name__ == "__main__":
    main()
