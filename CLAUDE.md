# python-design-patterns

Companion catalog to [python-patterns.guide](https://python-patterns.guide/): every design
pattern as runnable, tested, typed Python — plus an MCP server (`src/design_patterns_mcp/`)
that serves the catalog to agents.

## Layout

- `patterns/<group>/<slug>/` — one directory per pattern ("unit"). Groups:
  `principle`, `python`, `creational`, `structural`, `behavioral`, `modern`.
- `src/design_patterns/` — catalog loader (frontmatter → typed `Pattern` objects).
- `src/design_patterns_mcp/` — FastMCP server (tools, resources, prompts, sandbox).
- Legacy flat dirs (`behavioral/`, `combos/`, `creational/`, `structural/`) are
  pre-migration code: excluded from lint, deleted as units absorb them. Do not add to them.

## Pattern unit template

Every unit has exactly this shape (scaffold one with `/new-pattern`):

```
patterns/<group>/<slug>/
├── README.md          # YAML frontmatter + prose
├── __init__.py
├── naive.py           # the literal 1994/Java-style translation
├── pythonic.py        # what you actually write in Python
├── real_world.py      # the pattern as it appears in the stdlib
└── tests/test_<slug>.py
```

- Each `.py` variant is import-safe (no side effects at import) and has a
  `main() -> None` demo runnable as a script (`if __name__ == "__main__": main()`).
- Tests import the variants and assert behavior — never just "it runs".
- Full type hints; `mypy --strict` must pass.

## Frontmatter schema (the MCP server indexes this — keep it valid)

```yaml
id: structural/decorator        # must equal <group>/<slug>
name: Decorator
aliases: [wrapper]              # alternate names searchers might use
guide_url: https://python-patterns.guide/gang-of-four/decorator-pattern/  # or null
problem: "One sentence: the problem this pattern solves."
symptoms: ["logging every call", "caching results"]   # phrases a user might say
verdict: pythonic               # pythonic | use-with-care | prefer-alternative
caveats: ["Always use functools.wraps."]
stdlib_sightings: [functools.wraps, contextlib.contextmanager]
```

Verdicts: `pythonic` = use it as shown; `use-with-care` = valid but has sharp edges
(caveats say which); `prefer-alternative` = the naive form exists for study, the
pythonic file shows what to write instead (e.g. Singleton → module global,
Visitor → singledispatch). See `docs/verdicts.md`.

## Workflow

- Branches: `main ← staging ← feat/<slug>`. PRs target `staging`. Never push to `main`.
- Gate before any PR: `make check` (ruff lint+format, mypy --strict, pytest+cov) green.
- Commit style: `<type>: <summary>` (`feat`, `fix`, `chore`, `docs`, `refactor`).
- Toolchain is uv only — no pip/poetry. `make install` to set up.

## Writing style for pattern prose

- Lead with the problem, not the pattern name's history.
- Say plainly when Python makes the pattern unnecessary — that honesty is the
  point of the repo. Cite the guide chapter when one exists.
- naive.py mirrors the GoF book faithfully, even when un-Pythonic (that's its job);
  pythonic.py is idiomatic; real_world.py points at real stdlib usage.
