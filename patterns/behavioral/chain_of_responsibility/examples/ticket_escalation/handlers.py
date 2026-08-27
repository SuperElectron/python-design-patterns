"""Escalation policies as handlers, and the chain that orders them.

Each handler claims a ticket by returning a ``Resolution`` or declines with
``None``. The chain's order *is* the escalation policy: knowledge-base
auto-replies first, outages jump every queue, then the human tiers.
"""

from __future__ import annotations

from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.models import (
    Resolution,
    Ticket,
)
from patterns.behavioral.chain_of_responsibility.pattern import Chain

KNOWLEDGE_BASE = {
    "password-reset": "KB-101: resetting your password",
    "invoice-copy": "KB-204: downloading past invoices",
}


def auto_responder(ticket: Ticket) -> Resolution | None:
    """Answer known FAQ topics instantly, without a human."""
    for tag in ticket.tags:
        if tag in KNOWLEDGE_BASE:
            return Resolution(ticket.id, "bot", f"sent {KNOWLEDGE_BASE[tag]}")
    return None


def incident_commander(ticket: Ticket) -> Resolution | None:
    """Outages and severity-5 tickets bypass every queue."""
    if ticket.severity >= 5 or "outage" in ticket.tags:
        return Resolution(ticket.id, "incident", "declared incident, paged commander")
    return None


def helpdesk(ticket: Ticket) -> Resolution | None:
    """First human tier: routine tickets."""
    if 1 <= ticket.severity <= 2:
        return Resolution(ticket.id, "helpdesk", "assigned to helpdesk queue")
    return None


def engineering_on_call(ticket: Ticket) -> Resolution | None:
    """Second human tier: defects and anything the helpdesk can't take."""
    if 3 <= ticket.severity <= 4:
        return Resolution(ticket.id, "on-call", "paged engineering on-call")
    return None


def build_escalation_chain() -> Chain[Ticket, Resolution]:
    return Chain(
        [
            auto_responder,
            incident_commander,  # before the human tiers: outages jump the queue
            helpdesk,
            engineering_on_call,
        ]
    )


def route(ticket: Ticket, chain: Chain[Ticket, Resolution] | None = None) -> Resolution:
    """Route one ticket; anything no policy claims goes to human triage."""
    escalation = chain if chain is not None else build_escalation_chain()
    return escalation.handle_or(ticket, Resolution(ticket.id, "triage", "queued for human triage"))
