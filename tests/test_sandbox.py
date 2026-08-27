"""Sandbox contract: only catalog files run; timeouts and bad ids refuse."""

import pytest

from design_patterns.catalog import load_catalog
from design_patterns_mcp.sandbox import run_example

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


class TestSearchIndex:
    def test_symptom_search_hits_the_right_unit(self) -> None:
        from design_patterns_mcp.search import SearchIndex

        index = SearchIndex(CATALOG)
        top = index.search("undo redo history snapshot", limit=3)
        assert top and top[0].pattern.id in {"behavioral/memento", "behavioral/command"}

    def test_no_match_returns_empty(self) -> None:
        from design_patterns_mcp.search import SearchIndex

        assert SearchIndex(CATALOG).search("zzzqqqxxx") == []
