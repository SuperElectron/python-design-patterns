"""The Bridge without ceremony: composition plus an injected dependency.

The two real axes: what to say (alert severities, digest summaries) and how
to deliver it (email, Slack, SMS). M notifiers + N transports cover M x N
combinations, and "send the outage alert to Slack" is a constructor call.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Protocol


class Transport(Protocol):
    """The implementor side of the bridge."""

    def deliver(self, recipient: str, text: str) -> None: ...


@dataclass
class EmailTransport:
    outbox: list[str] = field(default_factory=list)

    def deliver(self, recipient: str, text: str) -> None:
        self.outbox.append(f"email to {recipient}: {text}")


@dataclass
class SlackTransport:
    posts: list[str] = field(default_factory=list)

    def deliver(self, recipient: str, text: str) -> None:
        self.posts.append(f"slack {recipient}: {text}")


@dataclass
class SmsTransport:
    MAX_LEN: ClassVar[int] = 80
    messages: list[str] = field(default_factory=list)

    def deliver(self, recipient: str, text: str) -> None:
        self.messages.append(f"sms {recipient}: {text[: self.MAX_LEN]}")


@dataclass(frozen=True)
class AlertNotifier:
    """One abstraction; the transport is the bridged-out detail."""

    transport: Transport
    recipient: str

    def alert(self, severity: str, message: str) -> None:
        self.transport.deliver(self.recipient, f"[{severity.upper()}] {message}")


@dataclass(frozen=True)
class DigestNotifier:
    """A second abstraction on the same bridge -- no transport changes needed."""

    transport: Transport
    recipient: str

    def digest(self, items: list[str]) -> None:
        summary = f"{len(items)} updates: " + "; ".join(items)
        self.transport.deliver(self.recipient, summary)


def main() -> None:
    slack = SlackTransport()
    email = EmailTransport()
    AlertNotifier(slack, "#ops").alert("critical", "db connection pool exhausted")
    DigestNotifier(email, "team@example.com").digest(["3 deploys", "1 rollback"])
    print(slack.posts)
    print(email.outbox)


if __name__ == "__main__":
    main()
