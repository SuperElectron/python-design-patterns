---
id: behavioral/observer
name: Observer
aliases: [publish-subscribe, listener, event-handler]
guide_url: null
problem: "Notify interested parties when something changes, without the subject knowing who they are."
symptoms: ["react to changes", "event listeners", "pub/sub", "on_change callbacks", "model updates views"]
verdict: pythonic
caveats:
  - "Observers are callables — an Observer ABC with one update() method is a function with extra steps."
  - "Decide the failure policy: one raising observer can silence the rest. Notify inside try/except or document that observers must not raise."
stdlib_sightings: [concurrent.futures.Future.add_done_callback, asyncio.Future]
---

# Observer

Broadcast a change to whoever subscribed, in order, without the subject
knowing its audience. **Verdict: pythonic** — observers are callables in a
list; the only real design decisions are order and failure policy.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Signal`, `Subscriber`, `ErrorPolicy` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/order_events/`](examples/order_events/) | Mini-project: order pipeline with independent subscribers built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.observer.examples.order_events.main
```
