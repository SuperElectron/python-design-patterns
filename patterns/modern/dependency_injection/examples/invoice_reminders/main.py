"""Demo: a morning's reminder run with a pinned clock."""

from __future__ import annotations

from datetime import date

from patterns.modern.dependency_injection.examples.invoice_reminders.app import (
    build_service,
    sample_invoices,
)


def main() -> None:
    # The demo pins the clock at the composition root — the same seam a test
    # uses, exercised for reproducibility instead of assertion.
    service = build_service(sample_invoices(), today=lambda: date(2026, 8, 27))
    reminded = service.send_reminders(grace_days=3)
    print(f"reminded: {reminded}")


if __name__ == "__main__":
    main()
