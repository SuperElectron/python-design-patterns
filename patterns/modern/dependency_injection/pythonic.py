"""Constructor injection with Protocol seams and production defaults.

A real service shape: overdue-invoice reminders. Three collaborators that
must be swappable in tests -- the clock, the invoice source, the mail
transport -- each behind a seam. Production passes nothing; tests pass
fakes and get deterministic behavior.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class Invoice:
    number: str
    customer_email: str
    amount_cents: int
    due: date


class InvoiceSource(Protocol):
    def unpaid(self) -> list[Invoice]: ...


class MailTransport(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...


class InMemoryInvoices:
    """Production would wrap a database; the seam doesn't care."""

    def __init__(self, invoices: list[Invoice] | None = None) -> None:
        self._invoices = invoices or []

    def unpaid(self) -> list[Invoice]:
        return list(self._invoices)


class ConsoleMail:
    """The production default transport (stand-in for SMTP)."""

    def send(self, to: str, subject: str, body: str) -> None:
        print(f"MAIL to={to} subject={subject!r}")


class ReminderService:
    def __init__(
        self,
        invoices: InvoiceSource,
        mail: MailTransport | None = None,
        today: Callable[[], date] = date.today,
    ) -> None:
        self.invoices = invoices
        self.mail: MailTransport = mail if mail is not None else ConsoleMail()
        self.today = today

    def send_reminders(self, grace_days: int = 3) -> list[str]:
        """Remind every invoice more than grace_days overdue; return numbers."""
        reminded: list[str] = []
        for invoice in self.invoices.unpaid():
            overdue = (self.today() - invoice.due).days
            if overdue > grace_days:
                self.mail.send(
                    to=invoice.customer_email,
                    subject=f"Invoice {invoice.number} is {overdue} days overdue",
                    body=f"Please pay {invoice.amount_cents / 100:.2f}.",
                )
                reminded.append(invoice.number)
        return reminded


def main() -> None:
    source = InMemoryInvoices(
        [
            Invoice("INV-1", "ada@example.com", 120_00, date(2026, 8, 1)),
            Invoice("INV-2", "grace@example.com", 80_00, date(2026, 8, 25)),
        ]
    )
    # Test wiring: frozen clock, captured mail -- fully deterministic.
    outbox: list[str] = []

    class CapturingMail:
        def send(self, to: str, subject: str, body: str) -> None:
            outbox.append(f"{to}: {subject}")

    service = ReminderService(source, mail=CapturingMail(), today=lambda: date(2026, 8, 26))
    print(f"reminded: {service.send_reminders()}")
    print(f"outbox:   {outbox}")


if __name__ == "__main__":
    main()
