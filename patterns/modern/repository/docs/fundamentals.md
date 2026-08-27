# Repository — fundamentals

## Intent

Keep domain logic ignorant of how objects are stored by mediating through a
collection-like interface. Named in Fowler's
[Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/repository.html);
given its canonical modern-Python treatment in
[Architecture Patterns with Python, ch. 2](https://www.cosmicpython.com/book/chapter_02_repository.html).

## Participants

| Role | Enterprise form | Python form |
|---|---|---|
| Domain objects | Mapped entities | Frozen dataclasses — `Invoice` in [`pattern/ledger.py`](../pattern/ledger.py) |
| The port | A repository interface | A `Protocol` naming only the operations the domain needs (`Invoices`) |
| Real adapter | ORM-backed repository class | Any class with the same methods (the mini-project's `SqliteInvoices`) |
| The fake | A mocking framework's job | `InMemoryInvoices` — a list with the port's methods, shipped *with* the pattern |
| Domain services | Methods on entities/services | Plain functions taking the port (`total_owed`, `overdue`) |

## Mechanism

1. The domain names its storage needs as a small `Protocol` — the operations
   it actually uses, not a generic CRUD surface.
2. Domain logic takes the port as a parameter and never imports a driver.
3. Two adapters satisfy the port: an in-memory fake for tests and a real one
   for production. Structural typing means neither declares anything.
4. One shared contract test suite runs against **both** adapters — that suite
   is what makes "the fake behaves like production" a checked fact instead of
   a hope.

## The welded-shut form, and what Python absorbs

The pre-pattern shape inlines storage into the domain question:

```python
def total_owed(conn: sqlite3.Connection, customer: str) -> int:
    rows = conn.execute("SELECT amount FROM invoices WHERE customer = ?", (customer,)).fetchall()
    return sum(amount for (amount,) in rows)  # domain math, welded to SQL
```

Compact — and every test of the *math* now drags a database, and every
storage change touches domain files. Enterprise stacks answered with
repository interfaces, unit-of-work classes, and ORMs. Python absorbs the
ceremony: `Protocol` gives the interface without inheritance, a list gives
the fake without a mocking framework. What survives is the discipline —
**the domain speaks only in its own types, through a port it owns**.

## When to use it

- Domain logic worth testing at speed, uncoupled from storage.
- A genuine second backend (and the in-memory fake counts as one).

## When not to use it

- Scripts that just need a query — the pattern's indirection buys nothing.
- One entity, one backend, no tests that hurt — wait for the pain.
- An ORM you're happy to couple to everywhere is itself a repository-shaped
  boundary; wrapping it again adds a layer with no new seam.

## Verdict: use with care

Earn it with a real second implementation and shared contract tests; if your
tests still hit a database, the repository isn't earning its keep.
