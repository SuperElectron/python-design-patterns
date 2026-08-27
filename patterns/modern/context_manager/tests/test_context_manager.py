"""Behavioral tests for all three context-manager variants."""

import tempfile
from pathlib import Path

import pytest

from patterns.modern.context_manager import naive, pythonic, real_world


class TestNaive:
    def test_finally_cleans_up_on_exception(self) -> None:
        log: list[str] = []
        with pytest.raises(RuntimeError):
            naive.use_one(log, explode=True)
        assert log == ["open a", "work", "close a"]

    def test_nested_resources_close_in_reverse(self) -> None:
        log: list[str] = []
        naive.use_two(log)
        assert log == ["open a", "open b", "work", "close b", "close a"]


class TestPythonic:
    def test_class_form_pairs_enter_and_exit(self) -> None:
        log: list[str] = []
        with pythonic.Managed("a", log):
            log.append("work")
        assert log == ["open a", "work", "close a"]

    def test_class_form_cleans_up_on_exception(self) -> None:
        log: list[str] = []
        with pytest.raises(ValueError, match="boom"), pythonic.Managed("a", log):
            raise ValueError("boom")
        assert log == ["open a", "close a"]

    def test_generator_form_cleans_up_on_exception(self) -> None:
        log: list[str] = []
        with pytest.raises(ValueError), pythonic.managed("g", log):
            raise ValueError
        assert log == ["open g", "close g"]


class TestRealWorld:
    def test_exit_stack_handles_a_runtime_number_of_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for i, text in enumerate(["x", "y"]):
                p = Path(tmp) / f"{i}.txt"
                p.write_text(text)
                paths.append(p)
            assert real_world.concatenate(paths) == "xy"

    def test_empty_stack_is_fine(self) -> None:
        assert real_world.concatenate([]) == ""
