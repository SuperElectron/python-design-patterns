"""Constructor injection with ``Protocol`` seams.

The service names the collaborators that must vary — the invoice source, the
mail transport, the clock — as constructor parameters typed by ``Protocol``
(or a plain callable). The composition root passes real adapters; tests pass
fakes. Where one implementation is right nearly always, a default argument
makes injection invisible until the day it is needed (``today=date.today``).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Protocol

Clock = Callable[[], date]


@dataclass(frozen=True)
class Invoice:
    """One unpaid invoice, as the reminder policy sees it."""

    number: str
    customer_email: str
    amount_cents: int
    due: date


class InvoiceSource(Protocol):
    """Where unpaid invoices come from — a database in production."""

    def unpaid(self) -> list[Invoice]: ...


class MailTransport(Protocol):
    """How reminders leave the system — SMTP in production."""

    def send(self, to: str, subject: str, body: str) -> None: ...


class ReminderService:
    """Remind customers about overdue invoices.

    Every collaborator arrives through the constructor; the service builds
    nothing it depends on. The clock keeps a production default because
    ``date.today`` is right everywhere except in a test.
    """

    def __init__(
        self,
        invoices: InvoiceSource,
        mail: MailTransport,
        today: Clock = date.today,
    ) -> None:
        self._invoices = invoices
        self._mail = mail
        self._today = today

    def send_reminders(self, grace_days: int = 3) -> list[str]:
        """Mail every invoice more than ``grace_days`` overdue; return its numbers."""
        reminded: list[str] = []
        for invoice in self._invoices.unpaid():
            overdue = (self._today() - invoice.due).days
            if overdue > grace_days:
                self._mail.send(
                    to=invoice.customer_email,
                    subject=f"Invoice {invoice.number} is {overdue} days overdue",
                    body=f"Please pay {invoice.amount_cents / 100:.2f}.",
                )
                reminded.append(invoice.number)
        return reminded
