---
id: modern/dependency_injection
name: Dependency Injection
aliases: [DI, constructor-injection, inversion-of-control]
guide_url: null
problem: "Hand an object its collaborators instead of letting it construct them, so they can be swapped — above all in tests."
symptoms: ["can't test without the real database", "class news up its own client", "mock the clock", "swap implementation per environment"]
verdict: pythonic
caveats:
  - "In Python DI needs no framework: a keyword argument with a production default is the entire mechanism."
  - "Inject at the boundary that varies (clock, storage, transport) — injecting everything turns constructors into wiring diagrams."
stdlib_sightings: [json.dumps cls=, sorted key=, unittest.mock]
---

# Dependency Injection

Hand an object its collaborators — clock, storage, transport — instead of
letting it construct them, so tests can swap in fakes. **Verdict: pythonic** —
a keyword argument with a production default is the whole mechanism.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `ReminderService`, `InvoiceSource`, `MailTransport`, `Clock` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/invoice_reminders/`](examples/invoice_reminders/) | Mini-project: adapters + a real composition root over `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.modern.dependency_injection.examples.invoice_reminders.main
```
