"""Behavioral tests for all three global-object variants."""

import math
import os

from patterns.python.global_object import naive, pythonic, real_world


class TestNaive:
    def test_mutable_global_couples_callers(self) -> None:
        naive._counts.clear()
        naive.tally("x")
        # A "different caller" is affected by the first one's state:
        assert naive.tally("x") == 2

    def test_import_time_work_already_happened(self) -> None:
        assert len(naive.IMPORT_TIME_WORK) == 1000


class TestPythonic:
    def test_constants_are_immutable_types(self) -> None:
        assert isinstance(pythonic.VOWELS, frozenset)
        assert pythonic.count_vowels("aeiou xyz") == 5

    def test_compiled_regex_global(self) -> None:
        assert pythonic.IDENTIFIER.fullmatch("valid_name")
        assert not pythonic.IDENTIFIER.fullmatch("1bad")

    def test_lazy_table_builds_once(self) -> None:
        assert pythonic.big_table() is pythonic.big_table()
        assert pythonic.big_table()[99] == 9801


class TestRealWorld:
    def test_stdlib_globals(self) -> None:
        assert real_world.midweek_day() == "Wednesday"
        assert real_world.circle_area(1.0) == math.pi

    def test_environ_mutation_cleans_up(self) -> None:
        assert real_world.with_temp_env("PDP_TEST_KEY", "v") == "v"
        assert "PDP_TEST_KEY" not in os.environ
