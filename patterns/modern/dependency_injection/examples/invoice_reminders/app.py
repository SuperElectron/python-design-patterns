"""The composition root: the one place that knows every concrete choice.

The service stays ignorant of these decisions; swapping SMTP for console
mail, or a database for a fixture list, edits only this file.
"""

from __future__ import annotations

from datetime import date

from patterns.modern.dependency_injection.examples.invoice_reminders.adapters import (
    ConsoleMail,
    InMemoryInvoices,
)
from patterns.modern.dependency_injection.pattern import (
    Clock,
    Invoice,
    MailTransport,
    ReminderService,
)


def sample_invoices() -> list[Invoice]:
    return [
        Invoice("INV-1", "ada@example.com", 120_00, date(2026, 8, 1)),
        Invoice("INV-2", "grace@example.com", 80_00, date(2026, 8, 25)),
        Invoice("INV-3", "linus@example.com", 45_50, date(2026, 7, 15)),
    ]


def build_service(
    invoices: list[Invoice],
    mail: MailTransport | None = None,
    today: Clock = date.today,
) -> ReminderService:
    """Assemble the production object graph; every seam overridable for tests."""
    return ReminderService(
        invoices=InMemoryInvoices(invoices),
        mail=mail if mail is not None else ConsoleMail(),
        today=today,
    )
