"""Concrete collaborators satisfying the pattern's seams.

Nothing here is imported by ``ReminderService`` — the service knows only the
protocols. These are what the composition root chooses to plug in.
"""

from __future__ import annotations

from patterns.modern.dependency_injection.pattern import Invoice


class InMemoryInvoices:
    """An invoice source backed by a list; production would wrap a database."""

    def __init__(self, invoices: list[Invoice] | None = None) -> None:
        self._invoices = list(invoices or [])

    def unpaid(self) -> list[Invoice]:
        return list(self._invoices)


class ConsoleMail:
    """A mail transport that prints; production would speak SMTP."""

    def __init__(self) -> None:
        self.sent_count = 0

    def send(self, to: str, subject: str, body: str) -> None:
        self.sent_count += 1
        print(f"MAIL to={to} subject={subject!r}")
