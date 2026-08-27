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
| `get_pattern(pattern_id, variant?)` | Full prose + example source (`naive`/`pythonic`/`real_world`/`all`) |
| `search_patterns(query, limit?)` | BM25 full-text search over names, aliases, problems, symptoms, prose |
| `run_example(pattern_id, variant)` | Executes the vendored example in a sandboxed subprocess; returns real stdout |
| `recommend_pattern(problem_statement, limit?)` | Ranked candidates with caveats; `prefer-alternative` verdicts tell you what to write instead |

## Resources

- `catalog://index` — the whole catalog as JSON
- `pattern://<group>/<slug>` — one pattern's prose
- `pattern://<group>/<slug>/<variant>` — one example's source

## Prompts

`refactor_toward(pattern_id, code)` · `explain_pattern(pattern_id, audience?)` · `choose_pattern(problem)`

## Sandbox contract

`run_example` executes only files resolved from the catalog index — the
`(id, variant)` pair is a dictionary lookup, never joined into a path. The
subprocess runs `python -I` in a temp cwd with a scrubbed environment, a 10s
timeout, and 64KB output caps. There is no arbitrary-code-execution tool.
