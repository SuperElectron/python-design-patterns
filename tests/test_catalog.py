"""Catalog loader: round-trips the real catalog and fails loudly on bad units."""

import json
from pathlib import Path

import pytest

from design_patterns.catalog import (
    VERDICTS,
    CatalogError,
    find_patterns_root,
    load_catalog,
)


class TestRealCatalog:
    def test_loads_all_units(self) -> None:
        catalog = load_catalog()
        assert len(catalog.patterns) == 32
        assert "structural/decorator" in catalog.ids()

    def test_every_module_example_builds_on_its_own_pattern_package(self) -> None:
        # The mini-projects exist to show the pattern in practice: each one
        # must import its unit's pattern/ package, not reimplement the idea.
        # AST walk, not text search — a docstring mentioning the path is not
        # an import.
        import ast

        for pattern in load_catalog().patterns:
            group, slug = pattern.id.split("/")
            absolute = f"patterns.{group}.{slug}.pattern"
            for name, path in pattern.examples().items():
                imports_pattern = False
                for source_file in sorted(path.rglob("*.py")):
                    tree = ast.parse(source_file.read_text(), filename=str(source_file))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ImportFrom):
                            module = node.module or ""
                            if module == absolute or module.startswith(f"{absolute}."):
                                imports_pattern = True
                            # Relative: from ..pattern import X / from ...pattern.chain import X
                            if node.level > 0 and (
                                module == "pattern" or module.startswith("pattern.")
                            ):
                                imports_pattern = True
                        elif isinstance(node, ast.Import):
                            for alias in node.names:
                                if alias.name == absolute or alias.name.startswith(f"{absolute}."):
                                    imports_pattern = True
                assert imports_pattern, (
                    f"{pattern.id} example {name!r} never imports its own pattern package"
                )

    def test_every_unit_ships_the_full_module_shape(self) -> None:
        for pattern in load_catalog().patterns:
            assert sorted(pattern.docs()) == ["examples", "fundamentals", "implementation"], (
                pattern.id
            )
            assert pattern.examples(), pattern.id
            assert pattern.sources(), pattern.id

    def test_verdicts_are_from_the_vocabulary(self) -> None:
        for pattern in load_catalog().patterns:
            assert pattern.verdict in VERDICTS

    def test_get_and_group_slug(self) -> None:
        pattern = load_catalog().get("creational/singleton")
        assert (pattern.group, pattern.slug) == ("creational", "singleton")
        assert pattern.guide_url is not None and pattern.guide_url.startswith("https://")

    def test_get_unknown_id_raises(self) -> None:
        with pytest.raises(KeyError):
            load_catalog().get("nope/nothing")

    def test_index_json_round_trips(self) -> None:
        entries = json.loads(load_catalog().to_json())
        assert len(entries) == 32
        keys = {"id", "name", "problem", "verdict", "docs", "examples"}
        assert all(keys <= e.keys() for e in entries)
        assert not any("prose" in e or "path" in e for e in entries)


GOOD = """\
id: creational/thing
name: Thing
guide_url: null
problem: "Build a thing."
symptoms: ["thing needed"]
verdict: pythonic
caveats: []"""


class TestValidation:
    def test_minimal_valid_unit_loads(self, tmp_path: Path) -> None:
        _write_module_unit(tmp_path, "creational", "thing", GOOD)
        catalog = load_catalog(tmp_path)
        assert catalog.get("creational/thing").verdict == "pythonic"

    def test_missing_key_fails(self, tmp_path: Path) -> None:
        _write_module_unit(
            tmp_path, "creational", "thing", GOOD.replace('problem: "Build a thing."', "")
        )
        with pytest.raises(CatalogError, match="missing frontmatter keys"):
            load_catalog(tmp_path)

    def test_id_directory_mismatch_fails(self, tmp_path: Path) -> None:
        _write_module_unit(tmp_path, "creational", "other", GOOD)
        with pytest.raises(CatalogError, match="!= directory"):
            load_catalog(tmp_path)

    def test_unknown_verdict_fails(self, tmp_path: Path) -> None:
        _write_module_unit(tmp_path, "creational", "thing", GOOD.replace("pythonic", "amazing"))
        with pytest.raises(CatalogError, match="verdict"):
            load_catalog(tmp_path)

    def test_no_frontmatter_fails(self, tmp_path: Path) -> None:
        unit = tmp_path / "creational" / "thing"
        unit.mkdir(parents=True)
        (unit / "README.md").write_text("# just prose\n")
        with pytest.raises(CatalogError, match="frontmatter"):
            load_catalog(tmp_path)

    def test_empty_tree_fails(self, tmp_path: Path) -> None:
        with pytest.raises(CatalogError, match="no pattern units"):
            load_catalog(tmp_path)


def _write_module_unit(root: Path, group: str, slug: str, frontmatter: str) -> Path:
    """A minimal valid module-shape unit: pattern/ + docs/ + examples/ + tests/."""
    unit = root / group / slug
    (unit / "pattern").mkdir(parents=True)
    (unit / "README.md").write_text(f"---\n{frontmatter}\n---\n\n# x\n")
    # Only load-bearing __init__.py exist (house rule): the two API files.
    (unit / "__init__.py").write_text("from .pattern.thing import build as build\n")
    (unit / "pattern" / "__init__.py").write_text("from .thing import build as build\n")
    (unit / "pattern" / "thing.py").write_text("def build() -> str:\n    return 'thing'\n")
    docs = unit / "docs"
    docs.mkdir()
    for name in ("fundamentals", "implementation", "examples"):
        (docs / f"{name}.md").write_text(f"# {name}\n")
    project = unit / "examples" / "demo"
    project.mkdir(parents=True)
    (project / "main.py").write_text("print('demo ran')\n")
    tests = unit / "tests"
    tests.mkdir()
    (tests / "test_thing.py").write_text("def test_ok() -> None:\n    assert True\n")
    return unit


class TestModuleShapeValidation:
    def test_valid_module_unit_loads_with_shape_fields(self, tmp_path: Path) -> None:
        _write_module_unit(tmp_path, "creational", "thing", GOOD)
        pattern = load_catalog(tmp_path).get("creational/thing")
        assert sorted(pattern.docs()) == ["examples", "fundamentals", "implementation"]
        assert sorted(pattern.examples()) == ["demo"]
        assert sorted(pattern.sources()) == ["__init__.py", "thing.py"]

    def test_missing_doc_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "docs" / "implementation.md").unlink()
        with pytest.raises(CatalogError, match=r"missing docs.*implementation"):
            load_catalog(tmp_path)

    def test_no_example_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "demo" / "main.py").unlink()
        with pytest.raises(CatalogError, match="no runnable examples"):
            load_catalog(tmp_path)

    def test_empty_init_in_example_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "demo" / "__init__.py").write_text("")
        with pytest.raises(CatalogError, match=r"delete empty __init__\.py"):
            load_catalog(tmp_path)

    def test_dunder_main_is_banned(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "demo" / "__main__.py").write_text("print('old style')\n")
        with pytest.raises(CatalogError, match=r"__main__\.py is banned"):
            load_catalog(tmp_path)

    def test_empty_tests_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "tests" / "test_thing.py").unlink()
        with pytest.raises(CatalogError, match="no tests"):
            load_catalog(tmp_path)

    def test_pattern_package_needs_init(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "pattern" / "__init__.py").unlink()
        with pytest.raises(CatalogError, match=r"no __init__\.py"):
            load_catalog(tmp_path)

    def test_stale_legacy_variant_files_fail(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "pythonic.py").write_text("def main() -> None: ...\n")
        with pytest.raises(CatalogError, match="legacy variant files"):
            load_catalog(tmp_path)

    def test_partial_unit_fails_loudly(self, tmp_path: Path) -> None:
        # A unit with only some of the template present must fail validation.
        unit = tmp_path / "creational" / "thing"
        (unit / "docs").mkdir(parents=True)
        (unit / "README.md").write_text(f"---\n{GOOD}\n---\n\n# x\n")
        with pytest.raises(CatalogError, match="module unit missing docs"):
            load_catalog(tmp_path)

    def test_empty_init_in_examples_dir_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "__init__.py").write_text("")
        with pytest.raises(CatalogError, match=r"delete empty __init__\.py"):
            load_catalog(tmp_path)

    def test_loadbearing_example_init_is_allowed(self, tmp_path: Path) -> None:
        # A NON-empty example __init__.py (e.g. plugin self-registration) is fine.
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "demo" / "__init__.py").write_text(
            "# load-bearing: demo of import-time registration\n"
        )
        assert load_catalog(tmp_path).get("creational/thing").examples()

    def test_index_json_carries_docs_and_examples(self, tmp_path: Path) -> None:
        _write_module_unit(tmp_path, "creational", "thing", GOOD)
        entries = json.loads(load_catalog(tmp_path).to_json())
        assert entries[0]["examples"] == ["demo"]
        assert entries[0]["docs"] == ["examples", "fundamentals", "implementation"]


def test_find_patterns_root_from_repo() -> None:
    assert find_patterns_root().name == "patterns"
