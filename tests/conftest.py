"""Shared fixtures: a synthetic module-shape unit for engine tests.

The real catalog's module-shape pilot is being built alongside this code, so
engine tests use a self-contained synthetic unit instead of assuming any real
unit's API.
"""

from pathlib import Path

import pytest

from design_patterns.catalog import Catalog, load_catalog


def write_module_unit(root: Path) -> Path:
    """Build ``<root>/creational/thing`` as a complete, runnable module-shape unit."""
    unit = root / "creational" / "thing"
    (unit / "pattern").mkdir(parents=True)
    for pkg in (root, root / "creational", unit, unit / "pattern"):
        (pkg / "__init__.py").write_text("")
    (unit / "README.md").write_text(
        "---\n"
        "id: creational/thing\nname: Thing\nguide_url: null\n"
        'problem: "Build a thing."\nsymptoms: ["thing needed"]\nverdict: pythonic\ncaveats: []\n'
        "---\n\n# Thing\n"
    )
    (unit / "pattern" / "thing.py").write_text("def build() -> str:\n    return 'built a thing'\n")
    docs = unit / "docs"
    docs.mkdir()
    for name in ("fundamentals", "implementation", "examples"):
        (docs / f"{name}.md").write_text(f"# {name} of Thing\n")
    project = unit / "examples" / "demo"
    project.mkdir(parents=True)
    (unit / "examples" / "__init__.py").write_text("")
    (project / "__init__.py").write_text("")
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
