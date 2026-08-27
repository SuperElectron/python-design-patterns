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

    def test_catalog_contains_both_shapes_during_migration(self) -> None:
        # The pilot migrated at least one unit; a silent regression of a
        # module unit back to legacy shape must fail here, not skip a branch.
        shapes = {p.shape for p in load_catalog().patterns}
        assert "module" in shapes
        module_ids = {p.id for p in load_catalog().patterns if p.shape == "module"}
        assert "behavioral/chain_of_responsibility" in module_ids

    def test_every_unit_ships_its_shape_completely(self) -> None:
        for pattern in load_catalog().patterns:
            if pattern.shape == "module":
                assert sorted(pattern.docs()) == ["examples", "fundamentals", "implementation"], (
                    pattern.id
                )
                assert pattern.examples(), pattern.id
                assert pattern.sources(), pattern.id
            else:
                assert sorted(pattern.variants()) == ["naive", "pythonic", "real_world"], pattern.id

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
        assert all({"id", "name", "problem", "verdict", "variants"} <= e.keys() for e in entries)
        assert not any("prose" in e or "path" in e for e in entries)


def _write_unit(root: Path, group: str, slug: str, frontmatter: str, body: str = "# x") -> None:
    unit = root / group / slug
    unit.mkdir(parents=True)
    (unit / "README.md").write_text(f"---\n{frontmatter}\n---\n\n{body}\n")
    (unit / "pythonic.py").write_text("def main() -> None: ...\n")


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
        _write_unit(tmp_path, "creational", "thing", GOOD)
        catalog = load_catalog(tmp_path)
        assert catalog.get("creational/thing").verdict == "pythonic"

    def test_missing_key_fails(self, tmp_path: Path) -> None:
        _write_unit(tmp_path, "creational", "thing", GOOD.replace('problem: "Build a thing."', ""))
        with pytest.raises(CatalogError, match="missing frontmatter keys"):
            load_catalog(tmp_path)

    def test_id_directory_mismatch_fails(self, tmp_path: Path) -> None:
        _write_unit(tmp_path, "creational", "other", GOOD)
        with pytest.raises(CatalogError, match="!= directory"):
            load_catalog(tmp_path)

    def test_unknown_verdict_fails(self, tmp_path: Path) -> None:
        _write_unit(tmp_path, "creational", "thing", GOOD.replace("pythonic", "amazing"))
        with pytest.raises(CatalogError, match="verdict"):
            load_catalog(tmp_path)

    def test_no_frontmatter_fails(self, tmp_path: Path) -> None:
        unit = tmp_path / "creational" / "thing"
        unit.mkdir(parents=True)
        (unit / "README.md").write_text("# just prose\n")
        with pytest.raises(CatalogError, match="frontmatter"):
            load_catalog(tmp_path)

    def test_unit_without_examples_fails(self, tmp_path: Path) -> None:
        _write_unit(tmp_path, "creational", "thing", GOOD)
        (tmp_path / "creational" / "thing" / "pythonic.py").unlink()
        with pytest.raises(CatalogError, match="ships no"):
            load_catalog(tmp_path)

    def test_empty_tree_fails(self, tmp_path: Path) -> None:
        with pytest.raises(CatalogError, match="no pattern units"):
            load_catalog(tmp_path)


def _write_module_unit(root: Path, group: str, slug: str, frontmatter: str) -> Path:
    """A minimal valid module-shape unit: pattern/ + docs/ + examples/ + tests/."""
    unit = root / group / slug
    (unit / "pattern").mkdir(parents=True)
    (unit / "README.md").write_text(f"---\n{frontmatter}\n---\n\n# x\n")
    (unit / "__init__.py").write_text("")
    (unit / "pattern" / "__init__.py").write_text("")
    (unit / "pattern" / "thing.py").write_text("def build() -> str:\n    return 'thing'\n")
    docs = unit / "docs"
    docs.mkdir()
    for name in ("fundamentals", "implementation", "examples"):
        (docs / f"{name}.md").write_text(f"# {name}\n")
    project = unit / "examples" / "demo"
    project.mkdir(parents=True)
    (unit / "examples" / "__init__.py").write_text("")
    (project / "__init__.py").write_text("")
    (project / "__main__.py").write_text("print('demo ran')\n")
    tests = unit / "tests"
    tests.mkdir()
    (tests / "test_thing.py").write_text("def test_ok() -> None:\n    assert True\n")
    return unit


class TestModuleShapeValidation:
    def test_valid_module_unit_loads_with_shape_fields(self, tmp_path: Path) -> None:
        _write_module_unit(tmp_path, "creational", "thing", GOOD)
        pattern = load_catalog(tmp_path).get("creational/thing")
        assert pattern.shape == "module"
        assert sorted(pattern.docs()) == ["examples", "fundamentals", "implementation"]
        assert sorted(pattern.examples()) == ["demo"]
        assert sorted(pattern.sources()) == ["__init__.py", "thing.py"]
        assert pattern.variants() == {}

    def test_missing_doc_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "docs" / "implementation.md").unlink()
        with pytest.raises(CatalogError, match=r"missing docs.*implementation"):
            load_catalog(tmp_path)

    def test_no_example_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "demo" / "__main__.py").unlink()
        with pytest.raises(CatalogError, match="no runnable examples"):
            load_catalog(tmp_path)

    def test_example_not_a_package_fails(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "demo" / "__init__.py").unlink()
        with pytest.raises(CatalogError, match="not a package"):
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

    def test_half_migration_is_claimed_and_fails_loudly(self, tmp_path: Path) -> None:
        # docs/ alone marks the unit module-shape; strict validation then
        # demands the rest instead of silently classifying it legacy.
        unit = tmp_path / "creational" / "thing"
        (unit / "docs").mkdir(parents=True)
        (unit / "README.md").write_text(f"---\n{GOOD}\n---\n\n# x\n")
        with pytest.raises(CatalogError, match="module unit missing docs"):
            load_catalog(tmp_path)

    def test_examples_dir_needs_init(self, tmp_path: Path) -> None:
        unit = _write_module_unit(tmp_path, "creational", "thing", GOOD)
        (unit / "examples" / "__init__.py").unlink()
        with pytest.raises(CatalogError, match=r"examples/ is not a package"):
            load_catalog(tmp_path)

    def test_index_json_carries_shape(self, tmp_path: Path) -> None:
        _write_module_unit(tmp_path, "creational", "thing", GOOD)
        entries = json.loads(load_catalog(tmp_path).to_json())
        assert entries[0]["shape"] == "module"
        assert entries[0]["examples"] == ["demo"]
        assert entries[0]["docs"] == ["examples", "fundamentals", "implementation"]


def test_find_patterns_root_from_repo() -> None:
    assert find_patterns_root().name == "patterns"
