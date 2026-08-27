"""Overdue-invoice reminders wired at a real composition root.

Run it: ``uv run python -m patterns.modern.dependency_injection.examples.invoice_reminders``
"""

from patterns.modern.dependency_injection.examples.invoice_reminders.adapters import (
    ConsoleMail,
    InMemoryInvoices,
)
from patterns.modern.dependency_injection.examples.invoice_reminders.app import (
    build_service,
    sample_invoices,
)

__all__ = ["ConsoleMail", "InMemoryInvoices", "build_service", "sample_invoices"]
