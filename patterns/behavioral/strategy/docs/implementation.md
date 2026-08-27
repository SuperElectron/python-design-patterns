# Strategy — putting it into a system

## The smell it fixes

An `if/elif` ladder choosing *behavior*, or a flag argument that swaps
algorithm mid-function:

```python
def price(order, promo_kind):
    if promo_kind == "bulk":
        ...
    elif promo_kind == "large_order":
        ...
    elif promo_kind == "loyalty":
        ...
```

Every new algorithm edits this function, and nothing stops the branches from
drifting apart in signature or behavior.

## Steps

1. **Name the signature.** One type alias — e.g. `PromoRule = Callable[[Order], float]`
   — is the whole "strategy interface"; `mypy` enforces it from then on.
2. **Extract each branch into a function** with that signature. The branch
   condition usually becomes the function's early `return 0.0` (or equivalent
   "not applicable" value).
3. **Pass the strategy where the work happens.** For a closed set, a plain
   parameter (`sorted(key=...)` style) is finished — stop here.
4. **Register open families.** When rules arrive over time (plugins, pricing,
   policies), a `StrategyRegistry` makes joining the family a decorator:

   ```python
   from patterns.behavioral.strategy import StrategyRegistry

   promotion: StrategyRegistry[Order, float] = StrategyRegistry()


   @promotion.register
   def loyalty(order: Order) -> float: ...


   promotion.results(order)  # every rule's answer, keyed by name
   promotion.get("loyalty")  # or one by name — UnknownStrategyError otherwise
   ```

5. **Make the selection policy explicit and tested.** "Best discount wins"
   (`max` over `results()`) is a business rule — pin it with a test, next to
   tests for each individual strategy.

## Python idioms that keep it small

- **`functools.partial` parameterizes a strategy** without a class:
  `partial(percent_off, rate=0.05)` is a new family member from an old recipe.
- **Registration by decoration** puts a rule's membership at its definition
  site — the same move Flask routes and `singledispatch` use.
- **A strategy needing state** graduates to a callable object (`__call__`)
  and slots into the same registry unchanged.

## Pitfalls

- **Module-level registries are import-order state.** A rule registers when
  its module is imported; a rule nobody imports silently does not exist.
  Import the rules module somewhere deliberate (the package `__init__`).
- **Registries are shared across tests.** Registering test-only strategies
  mutates global state — register into a fresh `StrategyRegistry` in tests,
  or clean up.
- **Signature drift.** The alias only protects call sites that use it;
  annotate every strategy with the alias's exact shape.
- **Comparing incomparable results.** `best`-style selection needs an
  ordering; keep strategy outputs plain (floats, tuples) or supply a key.

## Worked example

[`examples/promotions/`](../examples/promotions/) applies every step above to
checkout pricing — three registered rules, a best-rule engine, and a
comparison report:

```bash
uv run python -m patterns.behavioral.strategy.examples.promotions
```
