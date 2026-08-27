# How to read this repo

Every pattern lives in `patterns/<group>/<slug>/` with the same five parts:

| File | Job |
|---|---|
| `README.md` | YAML frontmatter (machine-readable metadata) + one page of prose: problem → naive → pythonic → in the wild → verdict |
| `naive.py` | The Gang-of-Four/Java translation, faithfully — even where it looks silly in Python. It exists so you can diff it against `pythonic.py` and *see* what the language absorbs. |
| `pythonic.py` | What a fluent Python developer writes for the same problem. When the pattern collapses into a language feature, this file shows the collapse and names it. |
| `real_world.py` | A small program using the stdlib's own embodiment of the pattern. |
| `tests/` | Behavioral tests for all three variants. |

## Where to start

- Reading for education: start with `principle/composition_over_inheritance`,
  then any pattern whose *symptom* you recognize (the frontmatter lists them).
- Solving a problem now: search the catalog through the [MCP server](mcp.md)
  (`recommend_pattern`) or skim the README table's "problem it solves" column.
- Every example runs: `uv run python -m patterns.<group>.<slug>.<variant>`.

## Groups

`principle` · `python` (patterns native to the language, from
[python-patterns.guide](https://python-patterns.guide/)) · `creational` /
`structural` / `behavioral` (the GoF 23) · `modern` (post-GoF additions:
DI, Repository, Context Manager, Registry, async producer/consumer).
