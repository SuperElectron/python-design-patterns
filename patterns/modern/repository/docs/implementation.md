# Repository — putting it into a system

## The smell it fixes

Domain tests that need infrastructure:

```python
def test_total_owed() -> None:
    conn = sqlite3.connect(TEST_DB)  # schema setup, fixtures, teardown...
    assert total_owed(conn, "ada") == 150
```

SQL scattered through business logic means the business rules can't be
tested — or changed — without dragging storage along.

## Steps

1. **Write the domain type first.** A frozen dataclass in domain vocabulary
   (`Invoice(number, customer, amount_cents, due)`) — no ORM base, no row
   shapes.
2. **Name the port from the domain's demand side.** List the storage
   operations domain code *actually performs* and put exactly those in a
   `Protocol`. Three methods is a normal size; ten is a warning.
3. **Build the fake in the same module as the port.** A list with the port's
   methods. It ships with the pattern, not buried in test helpers, because
   it *is* the deliverable that makes domain tests instant.
4. **Move the SQL into a real adapter** that satisfies the same `Protocol`
   (structurally — no base class), owning all row↔dataclass conversion.
5. **Write one contract test suite, parametrized over both adapters.** Same
   assertions, both backends. This is the step most implementations skip,
   and it is what keeps the fake honest.
6. **Pass the port into domain functions** — plain functions taking
   `repo: Invoices` stay importable, testable, and driver-free.

```python
from patterns.modern.repository import InMemoryInvoices, total_owed

repo = InMemoryInvoices()
repo.add(Invoice("INV-1", "ada", 120_00, date(2026, 8, 1)))
assert total_owed(repo, "ada") == 120_00
```

## Python idioms that keep it small

- **`Protocol` over ABC**: adapters stay dependency-free; sqlite3's and the
  fake's only relationship is behavioral.
- **Frozen dataclasses** make identity questions explicit and rows
  hashable-by-value in tests.
- **Keep queries as methods, not a query language.** `for_customer(name)`
  beats `find(spec)` until you have evidence otherwise (the caveat about
  generic `Repository[T]` in this unit's frontmatter).

## Pitfalls

- **The port grows to mirror SQL.** If a method exists because a screen
  needed a `JOIN`, the domain is no longer defining the port. Split read
  models out rather than widening the port.
- **The fake drifts from production.** Without shared contract tests, the
  fake quietly diverges (ordering, duplicates, missing rows) and domain
  tests pass against behavior production doesn't have.
- **Leaking storage types** — returning rows, cursors, or ORM instances
  through the port re-couples everything the pattern decoupled.
- **A repository per table** instead of per domain concept: the port serves
  an aggregate, not a schema.
- **Transactions smeared across repositories.** Commit/rollback is its own
  seam (unit of work); bolting `commit()` onto each repository hides it.

## Worked example

[`examples/invoice_ledger/`](../examples/invoice_ledger/) adds the sqlite
adapter and prints identical domain answers from both backends; the shared
contract tests live in [`tests/test_invoice_ledger.py`](../tests/test_invoice_ledger.py):

```bash
uv run python -m patterns.modern.repository.examples.invoice_ledger
```
