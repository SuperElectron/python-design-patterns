"""Sandbox contract: only catalog example packages run; bad ids and names refuse."""

from pathlib import Path

import pytest
from tests.conftest import write_module_unit

from design_patterns.catalog import Catalog, load_catalog
from design_patterns.mcp.sandbox import run_example_package

CATALOG = load_catalog()


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

    def test_failing_example_reports_not_raises(self, tmp_path: Path) -> None:
        # A crashing demo must come back as a RunResult, not an exception.
        root = tmp_path / "patterns"
        unit = write_module_unit(root)
        (unit / "examples" / "demo" / "main.py").write_text(
            "import sys\n\nprint('about to fail')\nsys.exit(3)\n"
        )
        result = run_example_package(load_catalog(root), "creational/thing", "demo")
        assert result.exit_code == 3
        assert "about to fail" in result.stdout
        assert not result.timed_out

    def test_runs_the_real_pilot_unit(self) -> None:
        # The migrated unit itself, through the python -I -m path CI must cover.
        result = run_example_package(
            CATALOG, "behavioral/chain_of_responsibility", "ticket_escalation"
        )
        assert result.exit_code == 0, result.stderr
        assert "triage" in result.stdout
        assert not result.timed_out


def _every_example() -> list[tuple[str, str]]:
    return [
        (pattern.id, example)
        for pattern in CATALOG.patterns
        for example in sorted(pattern.examples())
    ]


class TestEveryExampleRuns:
    """Demo rot check: every unit's every example runs in the sandbox."""

    @pytest.mark.parametrize(("pattern_id", "example"), _every_example())
    def test_example_exits_cleanly(self, pattern_id: str, example: str) -> None:
        result = run_example_package(CATALOG, pattern_id, example)
        assert result.exit_code == 0, f"{pattern_id}/{example}: {result.stderr}"
        assert not result.timed_out
        assert result.stdout.strip(), f"{pattern_id}/{example} printed nothing"


class TestSearchIndex:
    def test_symptom_search_hits_the_right_unit(self) -> None:
        from design_patterns.mcp.search import SearchIndex

        index = SearchIndex(CATALOG)
        top = index.search("undo redo history snapshot", limit=3)
        assert top and top[0].pattern.id in {"behavioral/memento", "behavioral/command"}

    def test_no_match_returns_empty(self) -> None:
        from design_patterns.mcp.search import SearchIndex

        assert SearchIndex(CATALOG).search("zzzqqqxxx") == []
