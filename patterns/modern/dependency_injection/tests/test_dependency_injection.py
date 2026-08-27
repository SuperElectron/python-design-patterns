"""Behavioral tests for all three dependency-injection variants."""

from datetime import date

from patterns.modern.dependency_injection import naive, pythonic, real_world


class TestNaive:
    def test_works_but_depends_on_the_real_clock(self) -> None:
        message = naive.GreetingService().greet("ada")
        assert message.endswith(", ada")
        assert message.startswith(("good morning", "good day"))


class CapturingMail:
    def __init__(self) -> None:
        self.outbox: list[tuple[str, str]] = []

    def send(self, to: str, subject: str, body: str) -> None:
        self.outbox.append((to, subject))


def _service(mail: CapturingMail, today: date) -> pythonic.ReminderService:
    source = pythonic.InMemoryInvoices(
        [
            pythonic.Invoice("INV-1", "ada@example.com", 120_00, date(2026, 8, 1)),
            pythonic.Invoice("INV-2", "grace@example.com", 80_00, date(2026, 8, 25)),
        ]
    )
    return pythonic.ReminderService(source, mail=mail, today=lambda: today)


class TestPythonic:
    def test_frozen_clock_makes_reminders_deterministic(self) -> None:
        mail = CapturingMail()
        reminded = _service(mail, date(2026, 8, 26)).send_reminders(grace_days=3)
        assert reminded == ["INV-1"]  # 25 days overdue; INV-2 inside grace
        assert mail.outbox == [("ada@example.com", "Invoice INV-1 is 25 days overdue")]

    def test_grace_period_is_respected(self) -> None:
        mail = CapturingMail()
        reminded = _service(mail, date(2026, 8, 26)).send_reminders(grace_days=30)
        assert reminded == [] and mail.outbox == []

    def test_every_seam_is_swappable(self) -> None:
        # A different source, transport, and clock -- no monkeypatching anywhere.
        source = pythonic.InMemoryInvoices([])
        mail = CapturingMail()
        service = pythonic.ReminderService(source, mail=mail, today=lambda: date(2026, 1, 1))
        assert service.send_reminders() == []

    def test_production_defaults_exist(self) -> None:
        service = pythonic.ReminderService(pythonic.InMemoryInvoices([]))
        assert isinstance(service.mail, pythonic.ConsoleMail)


class TestRealWorld:
    def test_injected_sort_policy(self) -> None:
        assert real_world.sort_by_injected_policy(["b", "A", "c"]) == ["A", "b", "c"]

    def test_injected_encoder(self) -> None:
        assert real_world.dump_with_injected_encoder({"k": "v"}) == '{"K": "V"}'
