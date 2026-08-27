"""Behavioral tests for the pattern's service — every seam exercised."""

from __future__ import annotations

from datetime import date

from patterns.modern.dependency_injection import Invoice, ReminderService


class FixedInvoices:
    def __init__(self, invoices: list[Invoice]) -> None:
        self._invoices = invoices

    def unpaid(self) -> list[Invoice]:
        return list(self._invoices)


class CapturingMail:
    def __init__(self) -> None:
        self.outbox: list[tuple[str, str]] = []

    def send(self, to: str, subject: str, body: str) -> None:
        self.outbox.append((to, subject))


def invoice(number: str, due: date, email: str = "ada@example.com") -> Invoice:
    return Invoice(number, email, 100_00, due)


class TestReminderPolicy:
    today = date(2026, 8, 27)

    def service(self, invoices: list[Invoice], mail: CapturingMail) -> ReminderService:
        return ReminderService(FixedInvoices(invoices), mail, today=lambda: self.today)

    def test_overdue_past_grace_is_reminded(self) -> None:
        mail = CapturingMail()
        reminded = self.service([invoice("INV-1", date(2026, 8, 1))], mail).send_reminders()
        assert reminded == ["INV-1"]
        assert mail.outbox == [("ada@example.com", "Invoice INV-1 is 26 days overdue")]

    def test_exactly_at_grace_is_not_reminded(self) -> None:
        mail = CapturingMail()
        at_grace = invoice("INV-2", date(2026, 8, 24))  # 3 days overdue == grace
        assert self.service([at_grace], mail).send_reminders(grace_days=3) == []
        assert mail.outbox == []

    def test_not_yet_due_is_not_reminded(self) -> None:
        mail = CapturingMail()
        future = invoice("INV-3", date(2026, 9, 1))
        assert self.service([future], mail).send_reminders() == []

    def test_the_clock_seam_controls_the_outcome(self) -> None:
        """The same invoice flips from quiet to reminded by injecting a later day."""
        inv = invoice("INV-4", date(2026, 8, 25))

        def at(day: date) -> ReminderService:
            return ReminderService(FixedInvoices([inv]), CapturingMail(), today=lambda: day)

        early = at(date(2026, 8, 26))
        late = at(date(2026, 9, 26))
        assert early.send_reminders() == []
        assert late.send_reminders() == ["INV-4"]
