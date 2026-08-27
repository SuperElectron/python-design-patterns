"""The python-design-patterns MCP server.

Tools, resources, and prompts over the pattern catalog. Run over stdio by
default (``python-design-patterns-mcp``) or streamable HTTP (``--http``).
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ResourceError, ToolError

from design_patterns.catalog import DOC_NAMES, Catalog, Pattern, load_catalog
from design_patterns.mcp.sandbox import run_example as _run_example
from design_patterns.mcp.sandbox import run_example_package as _run_example_package
from design_patterns.mcp.search import SearchIndex


# Lazy initialization (see patterns/python/global_object): importing this
# module must not do disk I/O; the catalog loads on first use, once.
@lru_cache(maxsize=1)
def get_catalog() -> Catalog:
    return load_catalog()


@lru_cache(maxsize=1)
def get_index() -> SearchIndex:
    return SearchIndex(get_catalog())


mcp = MCPServer(
    "python-design-patterns",
    instructions=(
        "Design patterns in Python: 32 units covering all 23 GoF patterns, "
        "Python-native patterns, and modern additions, each with an honest "
        "verdict. Start with search_patterns or recommend_pattern; verdicts of "
        "'prefer-alternative' tell you what to write instead. Migrated "
        "(module-shape) units offer three access levels: get_pattern_docs "
        "(fundamentals/implementation/examples), then list_examples + "
        "run_example(example=...) for runnable mini-projects, then read_source "
        "(the pattern/ package). Legacy (not yet migrated) units instead ship "
        "flat variant files, served via get_pattern(variant=...) and "
        "run_example(variant=...) with variant one of 'naive', 'pythonic', "
        "'real_world' (their literal filenames)."
    ),
)


def _summary(pattern: Pattern) -> dict[str, Any]:
    return {
        "id": pattern.id,
        "name": pattern.name,
        "problem": pattern.problem,
        "verdict": pattern.verdict,
    }


def _detail(pattern: Pattern, include_source: str | None) -> dict[str, Any]:
    detail: dict[str, Any] = {
        **_summary(pattern),
        "shape": pattern.shape,
        "aliases": list(pattern.aliases),
        "guide_url": pattern.guide_url,
        "symptoms": list(pattern.symptoms),
        "caveats": list(pattern.caveats),
        "stdlib_sightings": list(pattern.stdlib_sightings),
        "variants": sorted(pattern.variants()),
        "prose": pattern.prose,
    }
    if pattern.shape == "module":
        detail["docs"] = sorted(pattern.docs())
        detail["examples"] = sorted(pattern.examples())
        detail["note"] = (
            "module-shape unit: variants are legacy-only. Read docs via "
            "get_pattern_docs, run mini-projects via list_examples + "
            "run_example(example=...), read code via read_source."
        )
        return detail
    if include_source:
        variants = pattern.variants()
        wanted = sorted(variants) if include_source == "all" else [include_source]
        detail["source"] = {name: variants[name].read_text() for name in wanted if name in variants}
    return detail


@mcp.tool()
def list_patterns(group: str | None = None, verdict: str | None = None) -> list[dict[str, Any]]:
    """List catalog patterns, optionally filtered by group (creational,
    structural, behavioral, python, principle, modern) or verdict
    (pythonic, use-with-care, prefer-alternative)."""
    patterns = get_catalog().patterns
    if group is not None:
        patterns = tuple(p for p in patterns if p.group == group)
    if verdict is not None:
        patterns = tuple(p for p in patterns if p.verdict == verdict)
    return [_summary(p) for p in patterns]


@mcp.tool()
def get_pattern(pattern_id: str, variant: str | None = None) -> dict[str, Any]:
    """Fetch one pattern's full documentation. pattern_id is '<group>/<slug>'
    (e.g. 'structural/decorator'). For legacy units, variant ('naive',
    'pythonic', 'real_world', or 'all') includes that flat file's source;
    module-shape units serve code via read_source instead."""
    return _detail(_get(pattern_id), variant)


@mcp.tool()
def search_patterns(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Full-text search across pattern names, aliases, problems, symptoms,
    and prose. Returns the best matches with scores."""
    return [{**_summary(h.pattern), "score": h.score} for h in get_index().search(query, limit)]


def _get(pattern_id: str) -> Pattern:
    try:
        return get_catalog().get(pattern_id)
    except KeyError:
        known = ", ".join(get_catalog().ids())
        raise ValueError(f"unknown pattern {pattern_id!r}; known ids: {known}") from None


def _require_module_shape(pattern: Pattern) -> Pattern:
    if pattern.shape != "module":
        raise ToolError(
            f"{pattern.id} is not yet migrated to the module shape "
            "(no pattern/, docs/, examples/); use get_pattern with a variant instead"
        )
    return pattern


@mcp.tool()
def run_example(
    pattern_id: str, variant: str | None = None, example: str | None = None
) -> dict[str, Any]:
    """Execute one of a pattern's vendored examples in a sandboxed subprocess
    and return its real output. For migrated (module-shape) patterns pass
    example=<mini-project name from list_examples>; for legacy patterns pass
    variant='naive'|'pythonic'|'real_world'. Exactly one of the two."""
    if (variant is None) == (example is None):
        raise ValueError("pass exactly one of 'variant' (legacy) or 'example' (module-shape)")
    if example is not None:
        result = _run_example_package(get_catalog(), pattern_id, example)
    else:
        assert variant is not None
        result = _run_example(get_catalog(), pattern_id, variant)
    return {
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "timed_out": result.timed_out,
    }


@mcp.tool()
def get_pattern_docs(pattern_id: str, doc: str) -> str:
    """Read one of a migrated pattern's teaching docs: 'fundamentals' (intent,
    participants, mechanism, classic-form contrast), 'implementation' (how to
    introduce it into a real system), or 'examples' (cited external usages)."""
    pattern = _require_module_shape(_get(pattern_id))
    docs = pattern.docs()
    if doc not in docs:
        raise ValueError(f"doc must be one of {sorted(DOC_NAMES)}; {pattern_id} has {sorted(docs)}")
    return docs[doc].read_text(encoding="utf-8")


@mcp.tool()
def list_examples(pattern_id: str) -> list[dict[str, Any]]:
    """List a migrated pattern's runnable mini-projects (examples/<project>);
    run one with run_example(pattern_id, example=<name>)."""
    pattern = _require_module_shape(_get(pattern_id))
    return [
        {
            "name": name,
            "modules": sorted(p.name for p in path.glob("*.py")),
            "run": f"run_example(pattern_id={pattern.id!r}, example={name!r})",
        }
        for name, path in pattern.examples().items()
    ]


@mcp.tool()
def read_source(pattern_id: str) -> dict[str, str]:
    """Read a migrated pattern's own implementation: every file in its
    pattern/ package, keyed by filename."""
    pattern = _require_module_shape(_get(pattern_id))
    return {name: path.read_text(encoding="utf-8") for name, path in pattern.sources().items()}


@mcp.tool()
def recommend_pattern(problem_statement: str, limit: int = 3) -> list[dict[str, Any]]:
    """Describe a design problem in plain words; get ranked candidate patterns,
    each with its caveats and verdict attached. A 'prefer-alternative' verdict
    means the pythonic variant shows what to write instead."""
    recommendations = []
    for hit in get_index().search(problem_statement, limit):
        p = hit.pattern
        rec = {
            **_summary(p),
            "score": hit.score,
            "caveats": list(p.caveats),
            "stdlib_sightings": list(p.stdlib_sightings),
        }
        if p.verdict == "prefer-alternative":
            where = (
                f"read get_pattern_docs({p.id!r}, 'fundamentals') and read_source({p.id!r})"
                if p.shape == "module"
                else "see this unit's pythonic.py"
            )
            rec["note"] = (
                f"The guide's honest answer is usually not {p.name}: "
                f"{where} for what to write instead."
            )
        recommendations.append(rec)
    return recommendations


@mcp.resource("catalog://index")
def catalog_index() -> str:
    """The whole catalog as JSON: every pattern's metadata and variants."""
    return get_catalog().to_json()


@mcp.resource("pattern://{group}/{slug}")
def pattern_doc(group: str, slug: str) -> str:
    """One pattern's README prose."""
    return _get(f"{group}/{slug}").prose


@mcp.resource("pattern://{group}/{slug}/{variant}")
def pattern_source(group: str, slug: str, variant: str) -> str:
    """One legacy pattern's example source (naive | pythonic | real_world)."""
    pattern = _get(f"{group}/{slug}")
    variants = pattern.variants()
    if variant not in variants:
        hint = (
            "module-shape unit: use pattern://<id>/docs/<doc> or the read_source tool"
            if pattern.shape == "module"
            else f"has: {sorted(variants)}"
        )
        raise ResourceError(f"{pattern.id} has no variant {variant!r} ({hint})")
    return variants[variant].read_text()


@mcp.resource("pattern://{group}/{slug}/docs/{doc}")
def pattern_docs_resource(group: str, slug: str, doc: str) -> str:
    """One migrated pattern's teaching doc (fundamentals | implementation | examples)."""
    pattern = _get(f"{group}/{slug}")
    docs = pattern.docs()
    if doc not in docs:
        hint = (
            f"has: {sorted(docs)}"
            if pattern.shape == "module"
            else "unit not yet migrated to the module shape; use get_pattern instead"
        )
        raise ResourceError(f"{pattern.id} has no doc {doc!r} ({hint})")
    return docs[doc].read_text(encoding="utf-8")


@mcp.prompt()
def refactor_toward(pattern_id: str, code: str) -> str:
    """Ask for a refactor of the given code toward one catalog pattern."""
    pattern = _get(pattern_id)
    caveats = "\n".join(f"- {c}" for c in pattern.caveats)
    reference = (
        f"read_source({pattern.id!r}) and get_pattern_docs({pattern.id!r}, 'implementation')"
        if pattern.shape == "module"
        else "this unit's pythonic.py file"
    )
    return (
        f"Refactor the following code toward the {pattern.name} pattern "
        f"({pattern.id}), as shown by {reference}.\n"
        f"Verdict for this pattern: {pattern.verdict}. Honor these caveats:\n"
        f"{caveats}\n\nCode:\n```python\n{code}\n```"
    )


@mcp.prompt()
def explain_pattern(pattern_id: str, audience: str = "an intermediate Python developer") -> str:
    """Ask for an explanation of one pattern, tuned to an audience."""
    pattern = _get(pattern_id)
    contrast = (
        f"the classic-form vs Python contrast in get_pattern_docs({pattern.id!r}, 'fundamentals')"
        if pattern.shape == "module"
        else "the contrast between this unit's classic-form and pythonic example files"
    )
    return (
        f"Explain the {pattern.name} pattern to {audience}. Problem it solves: "
        f"{pattern.problem} Use {contrast}, state "
        f"the verdict ({pattern.verdict}) plainly, and show where the stdlib "
        f"already uses it ({', '.join(pattern.stdlib_sightings)})."
    )


@mcp.prompt()
def choose_pattern(problem: str) -> str:
    """Ask which pattern (if any!) fits a described problem."""
    return (
        f"A developer describes this problem:\n\n{problem}\n\n"
        "Using the python-design-patterns catalog (search_patterns / "
        "recommend_pattern), name the best-fitting pattern or say plainly that "
        "no pattern is needed. If the top candidate's verdict is "
        "'prefer-alternative', recommend the alternative the unit itself "
        "documents instead."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="python-design-patterns MCP server")
    parser.add_argument(
        "--http", action="store_true", help="serve streamable HTTP instead of stdio"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8734)
    args = parser.parse_args()
    if args.http:
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
