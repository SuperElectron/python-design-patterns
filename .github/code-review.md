# Code review standards

The reviewer's contract for this repo — and a reusable checklist for any
Python team.

## Layer 0: machines argue about style, humans argue about design

These run in CI; a human review comment about anything they cover is wasted:

| Tool | Standard it enforces |
|---|---|
| `ruff check` + `ruff format` | PEP 8, import order, bugbear/simplify/pyupgrade rule packs — each rule documented at [docs.astral.sh/ruff/rules](https://docs.astral.sh/ruff/rules/) |
| `mypy --strict` | PEP 484 typing, no untyped defs, no implicit Any |
| `pytest` + coverage | behavior, not just "it imports" |
| `python -m design_patterns.readme_table --check` | docs can't drift from code |

Worth adding for security-sensitive work: `bandit` (SAST) and `pip-audit`
(dependency CVEs). Note: bandit flags every `assert` (B101) — in pytest
tests that's idiomatic, not a finding.

## Layer 1: the written standards behind the tools

- **PEP 8** (style) · **PEP 257** (docstrings) · **PEP 20** (design sensibility)
- **Google Python Style Guide** — the most common team-level extension
- This repo's own bar: [CLAUDE.md](../CLAUDE.md) (unit template, frontmatter
  schema) and [docs/verdicts.md](../docs/verdicts.md)

## Layer 2: what human reviewers actually check

Severity-ordered — block on CRITICAL/HIGH, note MEDIUM:

**CRITICAL**
- Injection: user input reaching `eval`/`exec`, SQL strings, `subprocess` with `shell=True`
- Unsafe deserialization: `pickle.loads`/`yaml.load` on data crossing a trust boundary
- Secrets in code

**HIGH**
- `assert` as a runtime guard (vanishes under `python -O`)
- Mutable default arguments; shared mutable module state
- Swallowed exceptions (`except: pass`), or `except Exception` hiding real errors
- Resources without context managers; missing cleanup on the error path
- Thread-safety claims the code doesn't earn (unguarded lazy init, shared caches)
- Unbounded recursion/loops on user-controlled input

**MEDIUM**
- Work at import time (I/O, big computation) — see `patterns/python/global_object`
- `isinstance` traps (`bool` passes `int` checks), `is` vs `==` on sentinels
- API honesty: docstrings/comments that promise more than the code delivers
- A design pattern where a language feature suffices — check the catalog's verdict first

## Reference sources for reviewers (MCP)

- **This repo's own MCP server** — `claude mcp add design-patterns -- uv run --directory <repo> python-design-patterns-mcp`. `recommend_pattern` answers "should this be a Singleton?" with python-patterns.guide's verdicts and caveats; `get_pattern` serves the reference implementation to compare against.
- **Context7 MCP** — current library/framework docs, for "is this the right API usage?" questions.
- **python-patterns.guide** — the prose authority behind this catalog's verdicts.

## House rules (settled during the v2 migration, enforced in review)

- Name-keyed registries and caretakers refuse silent duplicates: `ValueError`
  unless `replace=True`. Ordered collections where repeats are meaningful —
  chains, signals — append freely; `functools.singledispatch`'s own overwrite
  behavior is inherited, noted not fought.
- `ParamSpec` typing only where a wrapper callable is returned
  (`structural/decorator` is the precedent); registries that return callables
  unchanged use plain identity typing.
- Never use `None` as a cache sentinel — a factory may legitimately return
  `None` and it must still cache once (`LazyProxy._MISSING` precedent).
  Immutability guards recurse into containers: a tuple holding a list is
  mutable where it counts (`InternPool` precedent).
- Every unit's `examples/` must genuinely build on its `pattern/` package —
  an AST import check enforces the import; reviewers judge token imports
  (an annotation-only import that vanishes at runtime does not count).
- Frontmatter stays stable; deliberate caveat improvements are allowed and
  called out in review.

## Mutation discipline

Reading a diff is not verification. For any load-bearing claim — a shutdown
discipline, a durability promise, a security guard, an "import does no work"
assertion — apply the mutation that would falsify it (swap the operator,
collapse the branch, make the write non-atomic) and confirm the suite fails.
During the v2 migration this caught four real defects that reading alone did
not: an untestable shutdown switch, a sqlite adapter that never committed, a
fixture that erased its own evidence, and a runtime-erased annotation import.
If the mutant survives, the finding is the missing test, not the mutation.

## Review etiquette

- Cite the rule or the file, not taste ("B008: mutable default" beats "I don't like this").
- One approval pass = one severity sweep top-down; don't drip-feed.
- The author of a change never approves it.
