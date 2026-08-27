"""Behavioral tests for the invoice-reminders mini-project."""

from __future__ import annotations

from datetime import date

import pytest

from patterns.modern.dependency_injection.examples.invoice_reminders.adapters import (
    ConsoleMail,
    InMemoryInvoices,
)
from patterns.modern.dependency_injection.examples.invoice_reminders.app import (
    build_service,
    sample_invoices,
)
from patterns.modern.dependency_injection.examples.invoice_reminders.main import main
from patterns.modern.dependency_injection.pattern import Invoice


class TestAdapters:
    def test_in_memory_source_returns_a_copy(self) -> None:
        inv = Invoice("INV-1", "ada@example.com", 100, date(2026, 8, 1))
        source = InMemoryInvoices([inv])
        source.unpaid().clear()
        assert source.unpaid() == [inv]

    def test_console_mail_prints_and_counts(self, capsys: pytest.CaptureFixture[str]) -> None:
        mail = ConsoleMail()
        mail.send("ada@example.com", "Invoice INV-1 is 5 days overdue", "Please pay.")
        assert mail.sent_count == 1
        assert "ada@example.com" in capsys.readouterr().out


class TestCompositionRoot:
    def test_build_service_defaults_to_production_adapters(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        service = build_service(sample_invoices(), today=lambda: date(2026, 8, 27))
        reminded = service.send_reminders()
        assert reminded == ["INV-1", "INV-3"]  # INV-2 is inside the grace period
        assert capsys.readouterr().out.count("MAIL") == 2

    def test_every_seam_is_overridable_from_the_root(self) -> None:
        captured: list[str] = []

        class Outbox:
            def send(self, to: str, subject: str, body: str) -> None:
                captured.append(to)

        service = build_service(sample_invoices(), mail=Outbox(), today=lambda: date(2026, 8, 27))
        service.send_reminders()
        assert captured == ["ada@example.com", "linus@example.com"]


class TestDemo:
    def test_main_reports_the_pinned_day_reminders(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "reminded: ['INV-1', 'INV-3']" in out
