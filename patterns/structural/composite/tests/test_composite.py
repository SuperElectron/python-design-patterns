"""Behavioral tests for all three composite variants."""

import pytest

from patterns.structural.composite import naive, pythonic, real_world


class TestNaive:
    def test_nested_render_recurses(self) -> None:
        scene = naive.Group("scene")
        scene.add(naive.Circle("sun"))
        inner = naive.Group("g")
        inner.add(naive.Circle("a"))
        scene.add(inner)
        assert scene.render() == "group(scene)\n  circle(sun)\n  group(g)\n    circle(a)"

    def test_leaf_refuses_children(self) -> None:
        with pytest.raises(TypeError):
            naive.Circle("sun").add(naive.Circle("moon"))


class TestPythonic:
    def test_totals_recurse_through_nesting(self) -> None:
        root = pythonic.Directory("root")
        root.add(pythonic.File("a", 100))
        sub = pythonic.Directory("sub")
        sub.add(pythonic.File("b", 400))
        root.add(sub)
        assert root.total_bytes() == 500

    def test_leaf_has_no_child_management(self) -> None:
        assert not hasattr(pythonic.File("a", 1), "add")

    def test_empty_directory_totals_zero(self) -> None:
        assert pythonic.Directory("empty").total_bytes() == 0


class TestRealWorld:
    def test_uniform_traversal_counts_all_depths(self) -> None:
        assert real_world.count_circles(real_world.build_scene()) == 3
