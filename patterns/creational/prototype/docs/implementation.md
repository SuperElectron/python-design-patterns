# Prototype — putting it into a system

## The smell it fixes

Construction calls repeating the same configuration, or a "template" object
that everyone mutates before use:

```python
# The pre-pattern shape: a plain mutable class, before anyone froze it.
job = MutableReportJob(
    name="nightly-sales",
    query="SELECT * FROM sales WHERE day = today()",  # copied everywhere
    recipients=("sales-leads@example.com",),
    filters=("exclude-test-accounts",),
)
job.fmt = "csv"  # ...and sometimes someone edits the shared one. Which one?
```

Named starting points want to live in exactly one place, and "start from X,
tweak Y" must never mutate X.

## Steps

1. **Freeze the product.** Make it a frozen dataclass; per-use variation then
   *has* to build a new object, which is the safety the pattern promises.
2. **Turn each named configuration into a template callable** —
   `functools.partial(ReportJob, name=..., query=...)`. The recipe is data;
   nothing is instantiated until asked.
3. **Put templates in a registry** keyed by name
   (`TemplateRegistry[ReportJob]`), so the menu is one readable structure and
   unknown names fail with the menu attached.
4. **Route per-use tweaks through `create(name, **overrides)`** — which is
   `dataclasses.replace` under the hood: a new product each time, template
   untouched.
5. **Reach for `copy.deepcopy` only if construction is the expensive part** —
   then the template really is an instance, and the `__deepcopy__` hook is the
   place to control what copying means.

```python
from patterns.creational.prototype import TemplateRegistry

menu: TemplateRegistry[ReportJob] = TemplateRegistry()
menu.register("nightly-sales", partial(ReportJob, name="nightly-sales", ...))
rush = menu.create("nightly-sales", fmt="csv")   # fresh, tweaked, template safe
```

## Python idioms that keep it small

- **`functools.partial` is a pre-configured constructor** — the exemplar
  without the copying.
- **`dataclasses.replace` is copy-with-changes** as a single expression; on a
  frozen dataclass it is also the *only* way, which is the point.
- **`register` returns its argument**, so a zero-argument factory function can
  be registered where a `partial` is too cramped.

## Pitfalls

- **Know your copy depth** if you do copy: `copy.copy` shares nested mutable
  state between "independent" clones — the classic aliasing bug.
- **Mutable defaults inside templates** (a list shared by every product)
  reintroduce aliasing through the back door; freeze collections into tuples.
- **A registry of live instances handed out un-copied** is the worst of both
  worlds — every caller edits the menu.
- **Overrides on a non-dataclass product** have no general safe form;
  `TemplateRegistry.create` refuses rather than guessing.

## Worked example

[`examples/report_job_templates/`](../examples/report_job_templates/) is the
scheduler shape above, end to end — run it with:

```bash
uv run python -m patterns.creational.prototype.examples.report_job_templates.main
```
