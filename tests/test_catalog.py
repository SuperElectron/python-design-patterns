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
        assert len(catalog.patterns) == 27
        assert "structural/decorator" in catalog.ids()

    def test_every_unit_ships_all_three_variants(self) -> None:
        for pattern in load_catalog().patterns:
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
        assert len(entries) == 27
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


def test_find_patterns_root_from_repo() -> None:
    assert find_patterns_root().name == "patterns"
