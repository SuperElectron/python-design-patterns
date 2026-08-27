---
id: structural/proxy
name: Proxy
aliases: [surrogate, virtual-proxy, protection-proxy]
guide_url: null
problem: "Stand in for another object to control access to it — deferring, guarding, or instrumenting the real thing."
symptoms: ["lazy expensive construction", "access control around an object", "remote object stand-in", "count or log attribute access"]
verdict: use-with-care
caveats:
  - "A proxy is not the object: isinstance checks, identity comparisons, and dunder lookups (which bypass __getattr__) all see through the disguise."
  - "For 'compute this attribute lazily once', functools.cached_property is the pattern at the right size — no proxy class needed."
stdlib_sightings: [weakref.proxy, functools.cached_property, unittest.mock.Mock]
---

# Proxy

Stand between callers and an object to mediate access — lazily building it,
guarding it, observing it. **Verdict: use with care** — the mediation is real
power, the disguise is skin-deep.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `LazyProxy`, `ProtectionProxy`, `MeteringProxy` — stackable |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/db_gateway/`](examples/db_gateway/) | Mini-project: an expensive warehouse connection behind all three proxies |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.structural.proxy.examples.db_gateway
```
