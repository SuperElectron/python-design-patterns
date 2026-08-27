# Interpreter — fundamentals

## Intent

Given a small language, represent its grammar and evaluate sentences in it —
user-supplied formulas, filter rules, flag conditions — safely, without ever
handing user input to `eval()`.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Grammar rules | One class per rule (`Number`, `Add`, `Mul`…) | Entries in an operation table — `OPERATIONS["and"] = …` |
| Sentence | A tree of rule instances | Nested tuples: `("*", ("+", 2, 3), 4)` — plain data |
| Evaluator | `interpret()` spread across every class | One recursive walk — [`Interpreter`](../pattern/rules.py) |
| Context | Passed to every `interpret()` | A `resolve` hook that turns leaves into values |

## Mechanism

1. A sentence arrives as data (config, request payload, rule store).
2. The evaluator walks it recursively: leaves resolve to values, tuples
   dispatch on their head through the operation table.
3. Extending the language is one table entry; hostile input hits two guards —
   unknown operations are `ValueError`, and nesting is depth-capped
   (`MAX_DEPTH`) so a bomb fails cleanly instead of overflowing the stack.

## The classic form, and what Python absorbs

The textbook shape defines a class per grammar rule:

```python
class Expression(ABC):
    @abstractmethod
    def interpret(self) -> int: ...


class Number(Expression):
    def __init__(self, value: int) -> None:
        self.value = value

    def interpret(self) -> int:
        return self.value


class Add(Expression):  # ...and Mul, and Sub, and every rule you add
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left, self.right = left, right

    def interpret(self) -> int:
        return self.left.interpret() + self.right.interpret()


tree = Mul(Add(Number(2), Number(3)), Number(4))
```

Python absorbs this twice over. The tree doesn't need classes — tuples and a
dict of operators interpret the same grammar in a screenful. And for many
"little languages" Python *is* the language: `ast.literal_eval` for data
literals, a vetted `ast` walk for arithmetic ([`safe_eval`](../pattern/safe_eval.py),
this module's hardened version), a real parser library beyond that.

## When to use it

- Rules must live in *data* — config files, databases, request payloads —
  and be evaluated repeatedly against different contexts.
- The language is genuinely tiny: boolean combinators, comparisons, a dozen
  operations.

## When not to use it

- The "language" is Python literals → `ast.literal_eval`.
- The language is arithmetic → a restricted `ast` walk (`safe_eval`).
- The language has precedence, bindings, or users who write it by hand →
  a real parser library; hand-rolled grammar code grows without limit.
- **Never** `eval()` on user input — this pattern's safe forms exist
  precisely to avoid that.

## Verdict: prefer an alternative

Check whether Python is already your language's parser before writing one.
When rules truly must be data, the tuple-tree + operation-table form here is
the whole pattern — no class hierarchy required.
