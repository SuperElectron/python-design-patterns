# Builder — putting it into a system

## The smell it fixes

A constructor call that keeps growing conditionals around it:

```python
conditions, params = [], []
if region:
    conditions.append("region = ?")
    params.append(region)
if product:
    conditions.append("product = ?")
    params.append(product)
sql = "SELECT ... " + (" AND ".join(conditions) if conditions else "")  # and so on
```

Every call site re-implements the assembly rules — clause ordering, the
conditions/params zip, edge cases — and any of them can drift. The builder
owns those rules once.

## Steps

1. **Define the product as a frozen dataclass.** Immutability is the payoff:
   a finished product cannot be half-edited later, and it is safely shareable.
2. **Give the builder the product's invariants as constructor arguments** —
   what every product must have (the table). Everything optional becomes a
   step.
3. **Write each step to validate, accumulate, and `return self`.** Validate
   *in* the step, so an error points at the faulty call, not at `build()`.
4. **Make `build()` a snapshot**, converting accumulated lists to tuples.
   The builder stays usable; products built earlier stay untouched.
5. **Keep the builder dumb about execution.** It emits a product; running it
   (here: handing `sql()`/`params` to sqlite) is someone else's job.

```python
from patterns.creational.builder import SelectBuilder

builder = SelectBuilder("orders").columns("id", "amount")
if minimum is not None:
    builder.where("amount >= ?", minimum)  # staged: only when asked for
query = builder.order_by("id").build()
rows = conn.execute(query.sql(), query.params)
```

## Python idioms that keep it small

- **Try keyword arguments first.** If every caller can supply everything in
  one call, `Query(table=..., columns=...)` needs no builder at all.
- **`return self` chaining** reads fluently, but each step working as a
  statement too (`builder.where(...)` on its own line) keeps conditional
  assembly natural.
- **Frozen product, plain-list builder** — the two-type split is the whole
  discipline; resist a `mutable=False` flag on one class.
- **Parameters ride with the query.** Bundling `sql()` and `params` in the
  product keeps values out of the SQL text — injection discipline for free.

## Pitfalls

- **The half-built object escaping.** If code can grab the builder's state
  before `build()`, the "finished" guarantee is gone — keep accumulators
  private.
- **Validation hoarded in `build()`.** Failing there points at the wrong
  line; validate in the step that received the bad input.
- **A Director class.** The caller's own code walking the steps *is* the
  director; a class for it is imported ceremony.
- **Builder reuse surprises.** Decide whether the builder may keep growing
  after `build()` (this one may) and pin it in a test either way.

## Worked example

[`examples/sql_select_builder/`](../examples/sql_select_builder/) stages
three analytics queries — including a conditionally-narrowed one — and runs
them against a real in-memory sqlite database:

```bash
uv run python -m patterns.creational.builder.examples.sql_select_builder.main
```
