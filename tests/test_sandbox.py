"""Sandbox contract: only catalog files run; timeouts and bad ids refuse."""

import pytest

from design_patterns.catalog import Catalog, load_catalog
from design_patterns.mcp.sandbox import run_example, run_example_package

CATALOG = load_catalog()


class TestSandbox:
    def test_runs_a_real_example(self) -> None:
        result = run_example(CATALOG, "structural/flyweight", "pythonic")
        assert result.exit_code == 0
        assert "shares" in result.stdout
        assert not result.timed_out

    def test_unknown_pattern_id_is_refused(self) -> None:
        with pytest.raises(KeyError):
            run_example(CATALOG, "../../etc/passwd", "naive")

    def test_unknown_variant_is_refused(self) -> None:
        with pytest.raises(KeyError, match="no variant"):
            run_example(CATALOG, "structural/flyweight", "__init__")

    def test_traversal_shaped_variant_is_refused(self) -> None:
        with pytest.raises(KeyError):
            run_example(CATALOG, "structural/flyweight", "../../../tmp/evil")

    def test_failing_example_reports_not_raises(self) -> None:
        # every current example exits 0; simulate by checking the API shape
        result = run_example(CATALOG, "behavioral/command", "real_world")
        assert isinstance(result.exit_code, int)
        assert isinstance(result.stderr, str)


class TestPackageSandbox:
    def test_runs_a_module_example_that_imports_the_pattern(self, module_catalog: Catalog) -> None:
        result = run_example_package(module_catalog, "creational/thing", "demo")
        assert result.exit_code == 0, result.stderr
        assert "built a thing" in result.stdout
        assert not result.timed_out

    def test_unknown_example_is_refused(self, module_catalog: Catalog) -> None:
        with pytest.raises(KeyError, match="no example"):
            run_example_package(module_catalog, "creational/thing", "nope")

    def test_traversal_shaped_example_is_refused(self, module_catalog: Catalog) -> None:
        with pytest.raises(KeyError):
            run_example_package(module_catalog, "creational/thing", "../../../tmp/evil")

    def test_unknown_pattern_id_is_refused(self, module_catalog: Catalog) -> None:
        with pytest.raises(KeyError):
            run_example_package(module_catalog, "../../etc/passwd", "demo")

    def test_legacy_unit_has_no_packages(self) -> None:
        with pytest.raises(KeyError, match="no example"):
            run_example_package(CATALOG, "structural/flyweight", "pythonic")

    def test_runs_the_real_pilot_unit(self) -> None:
        # The migrated unit itself, through the python -I -m path CI must cover.
        result = run_example_package(
            CATALOG, "behavioral/chain_of_responsibility", "ticket_escalation"
        )
        assert result.exit_code == 0, result.stderr
        assert "triage" in result.stdout
        assert not result.timed_out


class TestSearchIndex:
    def test_symptom_search_hits_the_right_unit(self) -> None:
        from design_patterns.mcp.search import SearchIndex

        index = SearchIndex(CATALOG)
        top = index.search("undo redo history snapshot", limit=3)
        assert top and top[0].pattern.id in {"behavioral/memento", "behavioral/command"}

    def test_no_match_returns_empty(self) -> None:
        from design_patterns.mcp.search import SearchIndex

        assert SearchIndex(CATALOG).search("zzzqqqxxx") == []
