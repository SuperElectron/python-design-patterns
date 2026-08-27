# Decorator — putting it into a system

## The smell it fixes

The same guard-and-report scaffolding pasted around every meaningful call:

```python
def charge(card, amount):
    log.info("charging...")
    for attempt in range(3):
        try:
            result = api.charge(card, amount)
            break
        except ConnectionError:
            if attempt == 2:
                raise
    log.info("charged")
    return result
```

Business logic is one line; the other nine are concerns that belong to
everyone and therefore to no one. Each becomes a decorator written once.

## Steps

1. **Name each concern** hiding in the scaffolding: retry, log, time, limit.
2. **Write each as a decorator factory** `(config) -> (func) -> wrapper`, with
   `functools.wraps` on every wrapper. Type with `ParamSpec` so the wrapped
   signature survives type checking.
3. **Inject effects** (clock, sleep, log sink) as factory parameters with real
   defaults — the decorators stay deterministic under test.
4. **Choose the stacking order deliberately**, and write it down where you
   compose: retry innermost (each attempt hugs the call), observability
   outside it (one line per *operation*), admission control outermost
   (rejected calls cost nothing). A different policy is legitimate — but it
   should be a decision, not an accident of paste order.
5. **Pin the order with a test.** Stacks are policy; swapping two layers must
   fail a test, not a production incident.

## Python idioms that keep it small

- `@decorator` syntax at definition site when a function is always wrapped;
  explicit `wrapped = deco(func)` at composition site when the policy varies
  per use — [`examples/resilient_client/`](../examples/resilient_client/)
  uses the second form.
- Parameterized decorators are three nested functions; that's the ceiling.
  If you're four deep, refactor to a class with `__call__`.
- `functools.wraps` is non-negotiable — it is itself a decorator fixing
  decorators, and every tool that inspects signatures depends on it.

## Pitfalls

- **Forgetting `functools.wraps`** — the wrapped function's name, docstring,
  and signature vanish; stack traces and debuggers lie.
- **Order accidents.** These are decorator *factories* — call them first.
  `retry(3)(logged(log)(f))` logs once per attempt;
  `logged(log)(retry(3)(f))` logs once per operation. Both are useful; only
  one is what you meant.
- **Decorators that swallow exceptions** turn control flow invisible; add
  behavior around the call, don't change its contract.
- **Hidden effects** (module-level clocks, global sleeps) make wrapped code
  untestable; inject them.
- **State on the wrapper** (`wrapper.calls += 1`) needs a `type: ignore` under
  strict typing — prefer a sink/callback the caller owns.

## Worked example

[`examples/resilient_client/`](../examples/resilient_client/) hardens a flaky
payments client with the retry/logging/rate-limit stack and pins the ordering
policy in tests. `timed` is deliberately left out of that stack: latency is
measured around the whole hardened call at the edge, not baked between the
layers — slot it outermost when you want it:

```bash
uv run python -m patterns.structural.decorator.examples.resilient_client
```
