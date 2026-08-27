---
id: structural/facade
name: Facade
aliases: [front-door, simplified-interface]
guide_url: null
problem: "Give a complicated subsystem one simple entry point for the common case."
symptoms: ["five-step setup for one common task", "callers copy-paste the same subsystem dance", "wrap this messy API"]
verdict: pythonic
caveats:
  - "In Python a facade is usually a module-level function — a class with one method is a function wearing a costume."
  - "A facade simplifies; it must not imprison. Leave the subsystem importable for callers who need the full controls."
stdlib_sightings: [subprocess.run, shutil.make_archive, urllib.request.urlopen]
---

# Facade

One entry point for the subsystem dance every caller used to copy-paste —
ordering, rollback and all. **Verdict: pythonic** — the natural Python facade
is a module-level function, and the subsystem stays public beside it.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `place_order` fronting `Warehouse`/`PaymentGateway`/`Shipping`/`Notifier` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/order_checkout/`](examples/order_checkout/) | Mini-project: a storefront batch-processing orders through the one door |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.structural.facade.examples.order_checkout.main
```
