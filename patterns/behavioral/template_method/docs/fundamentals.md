# Template Method — fundamentals

## Intent

Fix an algorithm's skeleton — the order and number of its steps — while
letting individual steps vary. Report generation always goes fetch →
transform → render → deliver; only the details of each step change per
report.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Skeleton owner | Abstract base class; the template method is concrete | A function or a frozen dataclass's `run` — `Skeleton` in [`pattern/skeleton.py`](../pattern/skeleton.py) |
| Variable steps | Abstract "primitive operations" overridden in subclasses | Callable parameters / fields with sensible defaults |
| Variants | One subclass per combination of steps | One *value* per combination — steps compose at call time |

## Mechanism

1. The skeleton calls its steps in a fixed order; nobody overrides the spine.
2. Each step is a hook: the classic form binds hooks by inheritance, the
   Python form binds them by passing callables.
3. A new variant is a new combination of steps — `with_steps(render=...)` —
   not a new class.

## The classic form, and what Python absorbs

The textbook implementation puts the spine in a base class and each variable
step behind an abstract method:

```python
class Report(ABC):
    def render(self, data: dict[str, int]) -> str:
        """The template method: the skeleton nobody overrides."""
        rows = self.format_rows(data)
        return f"{self.header()}\n{rows}"

    @abstractmethod
    def header(self) -> str: ...

    @abstractmethod
    def format_rows(self, data: dict[str, int]) -> str: ...


class TextReport(Report): ...  # one subclass


class CsvReport(Report): ...  # per combination of steps
```

Inheritance is doing one job here: passing functions to a function. Python
passes functions directly, so the same design collapses to callable
parameters — and combinations that would each need a subclass become call
sites. What survives is the discipline: **the spine is fixed and owns the
order; the steps are named, typed seams.**

The subclass form is not dead — it survives at *framework boundaries*, where
the framework owns the loop and hands you the hook: `unittest.TestCase.setUp`,
`socketserver.BaseRequestHandler.handle`, `json.JSONEncoder.default`.
Recognize it there; don't build it for your own code.

## When to use it

- Several procedures share an invariant step order but differ in step details
  (ETL jobs, report generation, request pipelines).
- You want the *spine* to be the single audited place where ordering,
  error-handling, and logging live.

## When not to use it

- Steps don't share a fixed order → that's composition of functions, not a
  template.
- Only one variant exists → write the plain function; extract seams when the
  second variant arrives.
- Variants need to change the *spine* → the skeleton is the wrong boundary;
  split it.

## Verdict: prefer an alternative

Pass the steps as callables (what `Skeleton` packages); subclass hooks only
at framework boundaries that hand them to you.
