"""Shared fixtures: a synthetic pattern unit for engine tests.

Engine tests use a self-contained synthetic unit instead of assuming any real
unit's API, so unit-level refactors never ripple into the engine suite.
"""

from pathlib import Path

import pytest

from design_patterns.catalog import Catalog, load_catalog


def write_module_unit(root: Path) -> Path:
    """Build ``<root>/creational/thing`` as a complete, runnable module-shape unit."""
    unit = root / "creational" / "thing"
    (unit / "pattern").mkdir(parents=True)
    # No empty __init__.py anywhere — namespace packages (PEP 420) carry the
    # structure. The two API files model the house style: bare as-alias re-exports.
    (unit / "__init__.py").write_text("from .pattern.thing import build as build\n")
    (unit / "pattern" / "__init__.py").write_text("from .thing import build as build\n")
    (unit / "README.md").write_text(
        "---\n"
        "id: creational/thing\nname: Thing\nguide_url: null\n"
        'problem: "Build a thing."\nsymptoms: ["thing needed"]\n'
        "verdict: prefer-alternative\ncaveats: []\n"
        "---\n\n# Thing\n"
    )
    (unit / "pattern" / "thing.py").write_text("def build() -> str:\n    return 'built a thing'\n")
    docs = unit / "docs"
    docs.mkdir()
    for name in ("fundamentals", "implementation", "examples"):
        (docs / f"{name}.md").write_text(f"# {name} of Thing\n")
    project = unit / "examples" / "demo"
    project.mkdir(parents=True)
    (project / "__main__.py").write_text(
        "from patterns.creational.thing.pattern.thing import build\n\nprint(build())\n"
    )
    tests = unit / "tests"
    tests.mkdir()
    (tests / "test_thing.py").write_text("def test_ok() -> None:\n    assert True\n")
    return unit


@pytest.fixture
def module_catalog(tmp_path: Path) -> Catalog:
    """A catalog whose ``patterns/`` root holds one synthetic module-shape unit."""
    root = tmp_path / "patterns"
    write_module_unit(root)
    return load_catalog(root)
