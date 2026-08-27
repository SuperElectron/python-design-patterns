"""An invoice ledger over two interchangeable repositories.

Run it: ``uv run python -m patterns.modern.repository.examples.invoice_ledger``
"""

from patterns.modern.repository.examples.invoice_ledger.sqlite_repo import SqliteInvoices

__all__ = ["SqliteInvoices"]
