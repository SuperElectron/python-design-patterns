# Verdicts

Every unit's frontmatter carries one verdict — the catalog's honest answer to
"should I write this in Python?"

| Verdict | Meaning |
|---|---|
| ✅ `pythonic` | Use it as shown in the unit's `pattern/` package; the pattern (in its Python form) is what we'd genuinely recommend. |
| ⚠️ `use-with-care` | Legitimate uses exist, but each caveat in the frontmatter names a concrete failure mode. Read them first. |
| 🔄 `prefer-alternative` | The honest answer is usually "don't". The classic form appears in `docs/fundamentals.md` for study; the unit's `pattern/` package exports the alternative to write instead (e.g. Singleton → module global, Visitor → `functools.singledispatch`). |

Where [python-patterns.guide](https://python-patterns.guide/) has a chapter,
its verdict wins and the unit links it. Where it doesn't, we reason from the
same principles: composition over inheritance, callables over class
hierarchies, the language's own features over ceremony.
