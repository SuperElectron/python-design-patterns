# Chain of Responsibility — putting it into a system

## The smell it fixes

An `if/elif` ladder that keeps growing, where each arm is really a policy
owned by a different concern:

```python
def route(ticket):
    if is_faq(ticket):
        ...
    elif ticket.severity >= 5:
        ...
    elif ticket.severity <= 2:
        ...
    else:
        ...
```

Every new policy edits this one function. The chain inverts that: each policy
becomes a handler that owns its own "is this mine?" test, and the router
becomes data — an ordered list you configure.

## Steps

1. **Define the request and answer types.** Small frozen dataclasses work
   well; the types make `mypy` police the handler contract for you.
2. **Extract each ladder arm into a handler** `(request) -> answer | None`.
   The arm's condition becomes the handler's decline test (`return None`).
3. **Choose the order deliberately.** Order is policy: put short-circuiting
   handlers (cache hits, emergencies) before general ones. Write a test that
   pins the order's observable behavior.
4. **Decide the unhandled policy at the call site.** `chain.handle(req)`
   raises `UnhandledRequestError`; `chain.handle_or(req, default)` substitutes
   a fallback. Never let "no handler" pass silently.
5. **Assemble the chain in one place** (a `build_*_chain()` factory), so the
   whole routing policy is readable — and swappable in tests.

```python
from patterns.behavioral.chain_of_responsibility import Chain

chain: Chain[Ticket, Resolution] = Chain([auto_responder, incident_commander, helpdesk])
chain.register(on_call)  # or grow it later / use as decorator
resolution = chain.handle_or(ticket, triage(ticket))
```

## Python idioms that keep it small

- Handlers are **plain functions** until they need state; then any callable
  object or `functools.partial(handler, config)` slots in unchanged.
- `chain.register` as a **decorator** turns registration into a one-liner at
  definition site — the same move `singledispatch` and Flask routes use.
- Parameterize, don't subclass: `partial(severity_gate, max_severity=2)`
  replaces a class hierarchy of near-identical handlers.

## Pitfalls

- **Silent fall-off-the-end** — the GoF form's biggest trap; the unhandled
  case must be a visible decision (step 4).
- **`None` as a real answer.** The decline convention reserves `None`; if your
  domain needs "the answer is nothing", wrap answers or use a sentinel.
- **Order coupling nobody wrote down.** If swapping two handlers changes
  behavior, a test must fail. Test the chain's routing table, not just each
  handler.
- **Handlers that mutate the request** turn a dispatch chain into a pipeline —
  a different pattern with different guarantees. Keep requests immutable.
- **Overlapping predicates** make the first match arbitrary; keep each
  handler's claim test exclusive enough that order expresses priority, not
  accident.

## Worked example

[`examples/ticket_escalation/`](../examples/ticket_escalation/) applies every
step above to support-ticket routing — run it with:

```bash
uv run python -m patterns.behavioral.chain_of_responsibility.examples.ticket_escalation
```
