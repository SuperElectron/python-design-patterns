"""Demo: a morning's tickets through the escalation chain."""

from __future__ import annotations

from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.handlers import route
from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.models import Ticket


def main() -> None:
    inbox = [
        Ticket("T-1", "Can't log in", 1, frozenset({"password-reset"})),
        Ticket("T-2", "Wrong charge on invoice", 2, frozenset({"billing"})),
        Ticket("T-3", "Export breaks on large files", 4, frozenset({"bug"})),
        Ticket("T-4", "API returning 500s for everyone", 3, frozenset({"outage"})),
        Ticket("T-5", "Feature idea: dark mode", 0, frozenset()),
    ]
    for ticket in inbox:
        resolution = route(ticket)
        print(f"{ticket.id} [{ticket.subject}] -> {resolution.team}: {resolution.action}")


if __name__ == "__main__":
    main()
