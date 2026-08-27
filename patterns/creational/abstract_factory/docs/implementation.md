# Abstract Factory — putting it into a system

## The smell it fixes

Client code that branches on a format or backend every time it builds
something:

```python
def render_report(report, fmt):
    if fmt == "html":
        out.append(f"<h2>{report.title}</h2>")
    elif fmt == "md":
        out.append(f"## {report.title}")
    ...  # repeated for every element, in every function
```

Every new format edits every branch, and nothing stops one function emitting
HTML headings above Markdown tables. The family bundle inverts it: the format
decision is made once, at the edge, and travels as a value.

## Steps

1. **List the products that must stay consistent.** If there is only one,
   stop here and pass a single callable.
2. **Define the family as a frozen dataclass of callables**, one field per
   product kind, precisely typed. Frozen matters: a family that can be
   mutated field-by-field can drift into a mixed family.
3. **Make client code accept the family as a parameter.** The client builds
   everything through it and never names a concrete class, format, or
   backend.
4. **Create one family instance per variant** (`HTML`, `MARKDOWN`, a stub
   family in tests) at module level — instances, not subclasses.
5. **Choose the family at the edge** (CLI flag, request content-type, config)
   and hand it down. Inner code stays format-blind.

```python
from patterns.creational.abstract_factory import HTML, MARKDOWN, DocumentFamily


def render(family: DocumentFamily, report: Report) -> str:
    parts = [family.heading(report.title)]
    ...


render(MARKDOWN if args.cli else HTML, report)
```

## Python idioms that keep it small

- **Families are instances, not classes.** A new family is a new
  `DocumentFamily(...)` literal — no subclass, no registration.
- **Test doubles are just another family**: builders that record calls or
  return markers, swapped in with zero patching.
- **Derive variants with `dataclasses.replace`**: a family that only changes
  one builder shares the rest — `replace(HTML, callout=plain_callout)`.
- **Lambdas are fine for one-liner builders**; promote to named functions
  when a builder grows logic worth testing alone.

## Pitfalls

- **Bundling factories that never vary together.** If callers always override
  members individually, the bundle is friction — pass callables separately
  (the `json.load(parse_float=...)` shape).
- **Letting the client peek at the concrete family** (`if family is HTML`).
  One branch reintroduces everything the pattern removed.
- **Mutable families.** Without `frozen=True` a family can be half-edited at
  runtime into a mix no one designed.
- **Growing the family for one client's needs.** Every field must be used by
  every client; optional products belong in a different bundle.

## Worked example

[`examples/report_renderer/`](../examples/report_renderer/) renders one
quarterly report through the `MARKDOWN` and `HTML` families — same client
code, both outputs:

```bash
uv run python -m patterns.creational.abstract_factory.examples.report_renderer
```
