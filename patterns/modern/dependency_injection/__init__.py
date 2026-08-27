"""Dependency Injection — public API.

>>> from patterns.modern.dependency_injection import ReminderService
"""

from patterns.modern.dependency_injection.pattern import (
    Clock,
    Invoice,
    InvoiceSource,
    MailTransport,
    ReminderService,
)

__all__ = ["Clock", "Invoice", "InvoiceSource", "MailTransport", "ReminderService"]
