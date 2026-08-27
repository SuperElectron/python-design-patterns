# Dependency Injection — fundamentals

## Intent

Hand an object its collaborators instead of letting it construct them, so the
things that vary — the clock, the storage, the transport — can be swapped
without touching the object. Named and taxonomized by Fowler in
[Inversion of Control Containers and the Dependency Injection pattern](https://martinfowler.com/articles/injection.html) (2004).

## Participants

| Role | Framework-era form | Python form |
|---|---|---|
| Service | A class resolved from a container | A plain class taking collaborators as constructor arguments — `ReminderService` in [`pattern/service.py`](../pattern/service.py) |
| Seam contract | An interface registered with the container | A `Protocol` (or a bare callable type like `Clock`) |
| Adapters | Container-managed beans | Any object with the right methods — no base class, no registration |
| Composition root | XML / container configuration | The one ordinary function that builds the object graph ([`examples/invoice_reminders/app.py`](../examples/invoice_reminders/app.py)) |

## Mechanism

1. The service names what it needs as constructor parameters, typed by
   `Protocol` so `mypy` checks any adapter structurally.
2. The composition root — one function, at the edge of the program — builds
   the real collaborators and passes them in.
3. Tests build the same service with fakes: a frozen clock, a capturing
   mailbox. No patching, no framework, no container.
4. A collaborator with one nearly-universal right answer keeps a **production
   default** (`today: Clock = date.today`) — the seam is invisible until the
   day a test needs it.

## The hard-wired form, and what Python absorbs

There is no GoF chapter for DI; the classic form here is the code you write
*before* the pattern — the service that builds its own collaborators:

```python
class GreetingService:
    def __init__(self) -> None:
        self.sent: list[str] = []  # the "store", welded in

    def greet(self, name: str) -> str:
        hour = datetime.now().hour  # the clock, welded in
        prefix = "good morning" if hour < 12 else "good day"
        ...
```

This class can only be tested against the real wall clock; the hidden
construction *is* the coupling. Java grew containers, XML wiring, and
`@Autowired` to break it. Python absorbs all of that: keyword arguments are
the injection mechanism, defaults are the production wiring, `Protocol` is
the interface. What survives of the pattern is one design habit — **name your
seams, and construct nothing you might need to swap**.

## When to use it

- A collaborator must differ between production and tests (clock, randomness,
  network, storage, transport).
- The same logic must run against interchangeable backends.

## When not to use it

- The collaborator never varies — `math.sqrt` needs no seam.
- Everything is injected on principle and constructors become wiring diagrams;
  inject at the boundary that varies, not everywhere.

## Verdict: pythonic

A keyword argument with a production default is the entire mechanism; the
stdlib itself does DI this way (`sorted(key=...)`, `json.dumps(cls=...)`).
