"""Behavioral tests for all three visitor variants."""

import pytest

from patterns.behavioral.visitor import naive, pythonic, real_world


class TestNaive:
    def test_double_dispatch_renders_the_tree(self) -> None:
        tree = naive.Add(naive.Number(1), naive.Add(naive.Number(2), naive.Number(3)))
        assert tree.accept(naive.Renderer()) == "(1 + (2 + 3))"


class TestPythonic:
    def test_two_operations_no_node_changes(self) -> None:
        tree = pythonic.Add(
            pythonic.Number(1), pythonic.Add(pythonic.Number(2), pythonic.Number(3))
        )
        assert pythonic.render(tree) == "(1 + (2 + 3))"
        assert pythonic.evaluate(tree) == 6

    def test_unknown_node_type_fails_loudly(self) -> None:
        with pytest.raises(TypeError, match="no renderer"):
            pythonic.render("not a node")


class TestRealWorld:
    def test_ast_census(self) -> None:
        source = "def greet():\n    print('hi')\n\ndef leave():\n    print(exit())\n"
        census = real_world.census_of(source)
        assert census.functions == ["greet", "leave"]
        assert census.calls == 3
