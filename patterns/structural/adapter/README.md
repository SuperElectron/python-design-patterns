---
id: structural/adapter
name: Adapter
aliases: [wrapper, translator]
guide_url: null
problem: "Make an existing class usable through the interface your code expects, without editing either side."
symptoms: ["third-party API has the wrong shape", "legacy interface mismatch", "make X look like Y", "can't edit the class I'm given"]
verdict: pythonic
caveats:
  - "When the target interface is a single method, the adapter is just a function — don't build a class to hold one translation."
  - "Duck typing means the adapter only needs the methods your code actually calls, not the adaptee's whole surface."
stdlib_sightings: [io.TextIOWrapper, socket.makefile, functools.cmp_to_key]
---

# Adapter

Make a class you can't edit speak the interface your code expects — translate
what differs, forward the rest. **Verdict: pythonic** — the honest way to
reconcile interfaces you don't control.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `DelegatingAdapter` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/payment_gateways/`](examples/payment_gateways/) | Mini-project: one checkout over two mismatched vendor SDKs |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.structural.adapter.examples.payment_gateways.main
```
