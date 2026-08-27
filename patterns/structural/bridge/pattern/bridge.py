"""The Bridge without ceremony: composition plus an injected implementor.

Two independent axes — what to say (alert, digest) and how to deliver it
(email, Slack, SMS). The transport is a ``Protocol`` injected into dataclass
notifiers: M notifiers + N transports cover M x N combinations, and "outage
alert to Slack" is a constructor call, not a class.
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
    """A second abstraction on the same bridge — no transport changes needed."""

    transport: Transport
    recipient: str

    def digest(self, items: list[str]) -> None:
        summary = f"{len(items)} updates: " + "; ".join(items)
        self.transport.deliver(self.recipient, summary)
