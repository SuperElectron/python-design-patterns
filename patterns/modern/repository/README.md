---
id: modern/repository
name: Repository
aliases: [data-access-layer, persistence-port]
guide_url: null
problem: "Keep domain logic ignorant of how objects are stored, behind a collection-like interface."
symptoms: ["SQL scattered through business logic", "tests need a database", "swap sqlite for postgres", "collection-like storage API"]
verdict: use-with-care
caveats:
  - "The payoff is the in-memory fake: if your tests still hit a database, the repository isn't earning its keep."
  - "Don't build a generic Repository[T] for one entity — write the three methods you need and stop."
stdlib_sightings: [sqlite3, shelve]
---

# Repository

Domain logic speaks to storage through a small `Protocol` port; a fake and a
real adapter both satisfy it, held together by shared contract tests.
**Verdict: use with care** — earn it with a genuine second implementation.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Invoice`, `Invoices` (port), `InMemoryInvoices` (fake), `total_owed`, `overdue` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/invoice_ledger/`](examples/invoice_ledger/) | Mini-project: sqlite adapter + identical answers from both backends |
| [`tests/`](tests/) | Domain tests on the fake; one contract suite parametrized over both adapters |

```bash
uv run python -m patterns.modern.repository.examples.invoice_ledger
```
