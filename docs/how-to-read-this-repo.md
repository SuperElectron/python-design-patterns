# How to read this repo

Every pattern is a self-contained module in `patterns/<group>/<slug>/`:

| Part | Job |
|---|---|
| `README.md` | YAML frontmatter (machine-readable metadata) + a ten-line front door: problem, verdict, map of the folders below |
| `pattern/` | The pattern itself as importable, typed library code — what you `from patterns.<group>.<slug> import` |
| `docs/fundamentals.md` | What the pattern *is*: intent, participants, mechanism, when/when-not — including the classic (GoF/Java) form as an annotated listing, diffed against the Python form |
| `docs/implementation.md` | How to introduce the pattern into a real system: the smell, the steps, the idioms, the pitfalls |
| `docs/examples.md` | Cited external usages — stdlib, major OSS, articles — the extra resources to pull during design and review |
| `examples/<project>/` | A runnable mini-project that imports `pattern/` and puts it to work in a realistic domain (more can be added over time) |
| `tests/` | Behavioral tests for the pattern code and each mini-project |

## Usage contract

```python
from patterns.behavioral.chain_of_responsibility import Chain
```

```bash
uv run python -m patterns.behavioral.chain_of_responsibility.examples.ticket_escalation
```

## Where to start

- Reading for education: start with `principle/composition_over_inheritance`,
  then any pattern whose *symptom* you recognize (the frontmatter lists them);
  read `docs/fundamentals.md` first, the code second.
- Solving a problem now: search the catalog through the [MCP server](mcp.md)
  (`recommend_pattern`) or skim the README table's "problem it solves" column,
  then go straight to that unit's `docs/implementation.md`.

## Groups

`principle` · `python` (patterns native to the language, from
[python-patterns.guide](https://python-patterns.guide/)) · `creational` /
`structural` / `behavioral` (the GoF 23) · `modern` (post-GoF additions:
DI, Repository, Context Manager, Registry, async producer/consumer).
