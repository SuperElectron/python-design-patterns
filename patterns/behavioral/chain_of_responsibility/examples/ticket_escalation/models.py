"""Domain types for the ticket-escalation mini-project."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Ticket:
    """A customer support ticket. Severity: 1 (question) .. 5 (outage)."""

    id: str
    subject: str
    severity: int
    tags: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class Resolution:
    """Where a ticket ended up and why."""

    ticket_id: str
    team: str
    action: str
