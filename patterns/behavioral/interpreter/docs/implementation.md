# Interpreter — putting it into a system

## The smell it fixes

Business rules hard-coded as Python conditionals that non-developers keep
asking to change ("enable this for Canadian pro users over 18"), or —
worse — a deployed `eval()` call "temporarily" evaluating user formulas.

## Steps

1. **Design the sentence shape first.** Nested tuples with a string head are
   ideal: JSON-serializable, diffable, storable in config or a database:

   ```python
   rule = ("and", (">=", "age", 18), ("==", "country", "CA"))
   ```

2. **Write the operation table.** Each operation takes its already-evaluated
   operands. Keep operations total: validate operand types and raise
   `ValueError` on nonsense (comparing booleans, wrong arity).
3. **Decide leaf resolution.** The `resolve` hook is where `"age"` becomes
   *this user's* age. Be explicit about the ambiguity it creates: a string
   is a field when the context has it, a literal otherwise — write that rule
   down and test it.
4. **Guard the edges.** Unknown operation → `ValueError` naming the options;
   nesting beyond `MAX_DEPTH` → `ValueError`, not `RecursionError`. Both are
   attacker-facing surfaces if rules come from users.
5. **Wrap it in a domain API.** Callers should see
   `engine.is_enabled("beta", user)`, never the interpreter.

```python
from patterns.behavioral.interpreter import Interpreter

interpreter = Interpreter(OPERATIONS, resolve=lookup)
verdict = bool(interpreter.evaluate(rule))
```

## Python idioms that keep it small

- Operations are **dict entries, not classes** — `operator.add`,
  lambdas, or named functions all slot in.
- For arithmetic-on-strings needs, **reuse [`safe_eval`](../pattern/safe_eval.py)**
  instead of extending the grammar — Python's parser already did the work.
- Sentences being plain tuples means **tests are literals** — no builders.

## Pitfalls

- **`eval()` creep.** The moment someone proposes `eval` "because the rules
  are trusted", the rules stop being trusted. The safe evaluator exists;
  there is no acceptable shortcut.
- **Unbounded recursion.** Rules from outside are attacker input; the depth
  cap is a security control, not a nicety (it was added in a security
  review — keep it).
- **Boolean/int confusion.** `bool` subclasses `int`; ordered comparisons on
  booleans and `True + 1` arithmetic should be rejected explicitly (both
  `safe_eval` and the flag engine do).
- **Grammar sprawl.** Every operation added is language surface to document,
  test, and secure. If the table keeps growing, you need a parser library,
  not a bigger dict.

## Worked example

[`examples/flag_rules/`](../examples/flag_rules/) applies every step to a
feature-flag engine — rules as data, per-user evaluation, hostile input
rejected:

```bash
uv run python -m patterns.behavioral.interpreter.examples.flag_rules.main
```
