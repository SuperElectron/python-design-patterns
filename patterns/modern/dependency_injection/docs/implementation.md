# Dependency Injection — putting it into a system

## The smell it fixes

A test that cannot run without the real world:

```python
def test_greeting() -> None:
    service = GreetingService()
    assert service.greet("ada").startswith("good morning")  # fails after noon
```

Whatever the class constructs for itself — `datetime.now`, `sqlite3.connect`,
`requests.Session()` — its tests drag along. The fix is to move construction
out of the class and pass the result in.

## Steps

1. **Find the seams.** List what the class reaches out to that varies by
   environment: time, randomness, storage, network, transport. Those — and
   only those — become parameters.
2. **Type each seam as a `Protocol`** (or a callable alias like
   `Clock = Callable[[], date]`). Structural typing means adapters need no
   base class: any object with a matching `send` method is a `MailTransport`.
3. **Take collaborators in the constructor.** Keep a default argument where
   one implementation is right nearly always (`today: Clock = date.today`);
   require the argument where the choice deserves to be visible.
4. **Build one composition root.** A single ordinary function at the program's
   edge constructs adapters and assembles the graph
   (`build_service(...)` in the mini-project). If wiring appears in more than
   one place, it has leaked.
5. **Write the tests the seams were made for.** Freeze the clock with a
   lambda, capture mail in a list; assert on behavior, not on mocks' innards.

```python
from datetime import date

from patterns.modern.dependency_injection import Invoice, ReminderService
from patterns.modern.dependency_injection.examples.invoice_reminders import (
    ConsoleMail,
    InMemoryInvoices,
)

source = InMemoryInvoices(
    [
        Invoice("INV-1", "ada@example.com", 120_00, date(2026, 8, 1)),
        Invoice("INV-3", "sam@example.com", 60_00, date(2026, 7, 20)),
    ]
)
outbox = ConsoleMail()
service = ReminderService(invoices=source, mail=outbox, today=lambda: date(2026, 8, 27))
assert service.send_reminders() == ["INV-1", "INV-3"]
```

## Python idioms that keep it small

- **A lambda is a fine adapter** for one-method seams; `Protocol` earns its
  keep from two methods up.
- **`functools.partial`** turns a configured function into an injectable
  collaborator without a class.
- **No container.** When the graph grows past what one composition-root
  function can hold readably, split the function — reach for a DI framework
  only when you can name what the function can no longer do.

## Pitfalls

- **Injecting everything.** A constructor with ten parameters is a wiring
  diagram; inject what varies, construct the rest.
- **Patching instead of injecting.** `unittest.mock.patch` reaches through
  module internals to do what a seam would have offered openly — needing it
  is the signal the seam is missing.
- **Wiring scattered through the code.** Construction belongs at the
  composition root; a class that builds one collaborator and injects two
  others has both problems.
- **Seams without contracts.** An untyped `mail=None` parameter accepts
  anything and promises nothing; the `Protocol` is what makes the fake and
  the real thing provably interchangeable.

## Worked example

[`examples/invoice_reminders/`](../examples/invoice_reminders/) wires the
service at a real composition root, with the demo pinning the clock through
the same seam the tests use:

```bash
uv run python -m patterns.modern.dependency_injection.examples.invoice_reminders.main
```
