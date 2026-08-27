---
id: creational/prototype
name: Prototype
aliases: [clone]
guide_url: https://python-patterns.guide/gang-of-four/prototype/
problem: "Create new objects by copying a pre-configured exemplar instead of constructing from scratch."
symptoms: ["expensive construction", "objects that start from a template", "registry of preconfigured instances", "clone this object"]
verdict: prefer-alternative
caveats:
  - "The pattern targets a 1990s problem: languages where classes weren't first-class values. In Python you just pass the class, or a functools.partial, or a bound copy call."
  - "If you do copy, know your depth: copy.copy shares nested mutable state; copy.deepcopy does not."
stdlib_sightings: [copy.copy, copy.deepcopy, functools.partial]
---

# Prototype

Stamp out new objects from named, pre-configured starting points. **Verdict:
prefer an alternative** — store callables (`functools.partial`), not exemplars
with a `clone()` protocol; tweak frozen products with `dataclasses.replace`.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `TemplateRegistry`, `Template` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/report_job_templates/`](examples/report_job_templates/) | Mini-project: a report scheduler stamping jobs from a template menu |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.creational.prototype.examples.report_job_templates.main
```
