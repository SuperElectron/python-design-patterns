# Template Method — putting it into a system

## The smell it fixes

Two (then three, then five) near-identical procedures, copy-pasted and
drifting:

```python
def daily_csv_report(): ...  # fetch, clean, format csv, print
def daily_markdown_report(): ...  # fetch, clean, format md, print — 90% the same
def weekly_csv_report(): ...  # subtle drift: forgot the clean step
```

The duplicated spine is where bugs breed — the fix is one spine, many steps.

## Steps

1. **Write out the spine once** and name its stages. Four is typical:
   acquire, normalize, produce, ship (`Skeleton`'s fetch/transform/render/
   deliver).
2. **Type each seam.** `Callable[[Sales], str]` per step; `mypy` then rejects
   a step wired into the wrong slot.
3. **Extract the variants' differing code into step functions** matching the
   seams. Identical code stays in the spine.
4. **Assemble variants as values**, deriving from a baseline instead of
   repeating yourself:

   ```python
   from patterns.behavioral.template_method import Skeleton

   csv_report = Skeleton(fetch=pull, transform=drop_refunds, render=csv_rows, deliver=print_delivery)
   md_report = csv_report.with_steps(render=markdown_table)
   ```

5. **Test the spine's order once, each step alone, and each variant's
   output.** The spine test uses recording steps; step tests are plain
   function tests — no fixtures, no subclass scaffolding.

## Python idioms that keep it small

- **`with_steps` (or `dataclasses.replace`) is the variant factory** — a new
  report is a diff against the baseline, so what varies is visible at a
  glance.
- **`functools.partial` configures a step** (`partial(top_n, n=10)`) without
  widening the seam's signature.
- **Explicit no-op steps** (`keep_all`, `discard`) beat `if step is not None`
  branches in the spine — the spine stays a straight line.
- At a **framework boundary**, take the hook the framework gives you
  (`JSONEncoder.default`, `setUp`) — wrapping a framework's template in your
  own adds a layer for nothing.

## Pitfalls

- **The spine growing conditionals.** An `if kind == "csv"` inside `run`
  means a step leaked into the skeleton; push it back out into a step.
- **Steps calling each other.** Seams talk only through the spine's data;
  a step reaching into another step re-couples what you separated.
- **Hook explosion.** Ten seams make every call site a wall of keywords —
  group related steps into one object, or accept that these are two
  different templates.
- **Mutable data flowing between steps** hides ordering dependencies; pass
  immutable snapshots (tuples, frozen dataclasses) so a reordered spine
  fails loudly in tests.

## Worked example

[`examples/report_pipeline/`](../examples/report_pipeline/) applies every
step above to sales reporting — one spine, CSV and Markdown variants derived
from a baseline:

```bash
uv run python -m patterns.behavioral.template_method.examples.report_pipeline.main
```
