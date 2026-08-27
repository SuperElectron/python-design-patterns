# MCP server

The catalog ships as an MCP server so agents can search the docs, read the
reference code, execute the examples, and get pattern recommendations with
honest verdicts attached.

## Connect

From a checkout:

```bash
claude mcp add design-patterns -- uv run --directory /path/to/python-design-patterns python-design-patterns-mcp
```

Once published to PyPI:

```bash
claude mcp add design-patterns -- uvx python-design-patterns-mcp
```

Remote/HTTP (Streamable HTTP on `/mcp`):

```bash
python-design-patterns-mcp --http --host 127.0.0.1 --port 8734
```

## Tools

| Tool | What it does |
|---|---|
| `list_patterns(group?, verdict?)` | Catalog listing, filterable |
| `get_pattern(pattern_id, variant?)` | Full prose (+ legacy variant source files: `naive.py` / `pythonic.py` / `real_world.py`, or `all`) |
| `search_patterns(query, limit?)` | BM25 full-text search over names, aliases, problems, symptoms, prose |
| `get_pattern_docs(pattern_id, doc)` | A migrated pattern's teaching doc: `fundamentals`, `implementation`, or `examples` |
| `list_examples(pattern_id)` | A migrated pattern's runnable mini-projects |
| `run_example(pattern_id, variant?/example?)` | Executes a vendored example (legacy `variant` or migrated `example`) in a sandboxed subprocess; returns real stdout |
| `read_source(pattern_id)` | A migrated pattern's own implementation (`pattern/` package) |
| `recommend_pattern(problem_statement, limit?)` | Ranked candidates with caveats; `prefer-alternative` verdicts tell you what to write instead |

Migrated (module-shape) patterns follow three access levels: scan docs
(`get_pattern_docs`) → run a use case (`list_examples` + `run_example`) →
read the source (`read_source`).

## Resources

- `catalog://index` — the whole catalog as JSON
- `pattern://<group>/<slug>` — one pattern's prose
- `pattern://<group>/<slug>/<variant>` — one legacy example's source
- `pattern://<group>/<slug>/docs/<doc>` — one migrated pattern's teaching doc

## Prompts

`refactor_toward(pattern_id, code)` · `explain_pattern(pattern_id, audience?)` · `choose_pattern(problem)`

## Sandbox contract

`run_example` executes only files resolved from the catalog index — the
`(id, variant)` / `(id, example)` pair is a dictionary lookup, never joined
into a path. The
subprocess runs `python -I` in a temp cwd with a scrubbed environment, a 10s
timeout, and 64KB output caps. There is no arbitrary-code-execution tool.
