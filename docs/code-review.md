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
  schema) and [verdicts.md](verdicts.md)

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

## Review etiquette

- Cite the rule or the file, not taste ("B008: mutable default" beats "I don't like this").
- One approval pass = one severity sweep top-down; don't drip-feed.
- The author of a change never approves it.
