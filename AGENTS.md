# Agent instructions — python-design-patterns

Companion catalog to [python-patterns.guide](https://python-patterns.guide/): every design
pattern as a self-contained, tested, typed Python module — plus an MCP server
(`src/design_patterns/mcp/`) that serves the catalog to agents.

## Layout

- `patterns/<group>/<slug>/` — one module per pattern ("unit"). Groups:
  `principle`, `python`, `creational`, `structural`, `behavioral`, `modern`.
- `src/design_patterns/` — catalog loader (frontmatter → typed `Pattern` objects,
  strict structure validation in CI).
- `src/design_patterns/mcp/` — MCP server on the mcp 2.x SDK (`MCPServer`, not
  FastMCP): tools, resources, prompts, sandbox.

## Pattern unit template

Every unit has exactly this shape (scaffold one with `/new-pattern`):

```
patterns/<group>/<slug>/
├── README.md            # YAML frontmatter + ~10-line front door: problem, verdict, folder map
├── __init__.py          # public API — re-exports from pattern/
├── pattern/             # the pattern as importable, typed library code
│   ├── __init__.py
│   └── <named>.py       # named for what it provides (chain.py, decorators.py, …)
├── docs/
│   ├── fundamentals.md  # intent, participants, mechanism, when/when-not,
│   │                    #   the classic (GoF) form as an annotated listing — never call it "naive"
│   ├── implementation.md# introducing it into a real system: smell, steps, idioms, pitfalls
│   └── examples.md      # cited EXTERNAL usages: stdlib, OSS, articles
├── examples/            # runnable mini-projects that import pattern/
│   └── <project>/       # realistic domain, no Foo/Bar; main.py + modules
└── tests/               # isolated: test_<named>.py + test_<project>.py
```

No other `__init__.py` exist — namespace packages (PEP 420) carry the rest;
the loader rejects empty ones.

- Everything import-safe (no side effects at import); mini-projects run via
  `uv run python -m patterns.<group>.<slug>.examples.<project>.main`.
- Tests assert behavior, never just "it runs"; load-bearing claims get the
  mutation treatment (mutate the code, prove the suite fails, revert).
- Examples must genuinely build on `pattern/` — the loader and a catalog test
  enforce the structure and the import; reviewers reject token imports.
- Full type hints; `mypy --strict` must pass.

## House rules

- Name-keyed registries refuse silent duplicates (`ValueError` unless
  `replace=True`); ordered collections append freely.
- `ParamSpec` only where a wrapper callable is returned; identity typing otherwise.
- Never `None` as a cache sentinel; immutability guards recurse into containers.
- No empty `__init__.py` — delete them (PEP 420 namespace packages). One exists
  only when load-bearing: the unit's public-API re-exports
  (`from .pattern.x import Y as Y` — the as-alias form) or an import-time
  effect the unit teaches. Never `__all__`.

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
(caveats say which); `prefer-alternative` = the classic form exists for study in
docs/fundamentals.md, `pattern/` exports the alternative to write instead
(e.g. Singleton → module global, Visitor → singledispatch). See `docs/verdicts.md`.

## Workflow

- Branches: `main ← staging ← feat/<slug>`. PRs target `staging`. Never push to `main`.
- Gate before any PR: `make check` (ruff lint+format, mypy --strict, pytest+cov,
  readme-table drift) green.
- Commit style: `<type>: <summary>` (`feat`, `fix`, `chore`, `docs`, `refactor`).
- Toolchain is uv only — no pip/poetry. `make install` to set up.

## Writing style for pattern prose

- Lead with the problem, not the pattern name's history.
- Say plainly when Python makes the pattern unnecessary — that honesty is the
  point of the repo. Cite the guide chapter when one exists.
- The classic form in fundamentals.md mirrors the GoF book faithfully, even when
  un-Pythonic (that's its job); `pattern/` is idiomatic; examples.md points at
  real external usage.
