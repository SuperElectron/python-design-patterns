---
id: behavioral/template_method
name: Template Method
aliases: [hook-methods, skeleton-algorithm]
guide_url: null
problem: "Fix an algorithm's skeleton while letting callers vary individual steps."
symptoms: ["same steps, different details", "framework calls your overrides", "setUp/tearDown-style hooks"]
verdict: prefer-alternative
caveats:
  - "Passing step callables as keyword arguments with defaults does the same job without inheritance, and composes better."
  - "Subclass hooks make sense at framework boundaries (unittest, socketserver) where the framework owns the loop and you own the steps."
stdlib_sightings: [json.JSONEncoder.default, unittest.TestCase.setUp, socketserver.BaseRequestHandler.handle]
---

# Template Method

Fix the algorithm's spine, vary its steps. **Verdict: prefer an alternative**
— pass the steps as callables; subclass hooks belong at framework boundaries
that hand them to you.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Skeleton`, `keep_all`, `discard` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/report_pipeline/`](examples/report_pipeline/) | Mini-project: sales reports built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.template_method.examples.report_pipeline
```
