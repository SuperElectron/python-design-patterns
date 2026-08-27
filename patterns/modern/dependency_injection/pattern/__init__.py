"""Dependency Injection as importable, typed building blocks."""

from patterns.modern.dependency_injection.pattern.service import (
    Clock,
    Invoice,
    InvoiceSource,
    MailTransport,
    ReminderService,
)

__all__ = ["Clock", "Invoice", "InvoiceSource", "MailTransport", "ReminderService"]
