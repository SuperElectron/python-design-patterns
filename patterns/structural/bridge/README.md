---
id: structural/bridge
name: Bridge
aliases: [abstraction-implementor]
guide_url: null
problem: "Let an abstraction and its implementation vary independently, instead of multiplying subclasses across both axes."
symptoms: ["two hierarchies multiplying", "shapes times renderers", "device times remote", "backend swappable under a stable front"]
verdict: prefer-alternative
caveats:
  - "In Python the Bridge collapses into ordinary composition with dependency injection — hold the implementor as an attribute, pass it in."
  - "The pattern's real lesson survives: name the two axes, give each its own small hierarchy (or set of callables), and connect them with one reference."
stdlib_sightings: [logging.Logger with logging.Handler]
---

# Bridge

Two independent axes (what to do × how to carry it out) joined by one injected
reference, instead of a subclass per combination. **Verdict: prefer an
alternative** — composition with dependency injection *is* the bridge.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Transport` protocol, transports, `AlertNotifier`, `DigestNotifier` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/notification_center/`](examples/notification_center/) | Mini-project: team alert/digest routing over per-team transports |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.structural.bridge.examples.notification_center
```
