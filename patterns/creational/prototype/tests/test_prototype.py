"""Behavioral tests for all three prototype variants."""

from patterns.creational.prototype import naive, pythonic, real_world


class TestNaive:
    def test_registry_clones_are_independent(self) -> None:
        registry = naive.PrototypeRegistry()
        registry.register("c", naive.Circle(radius=2, color="green"))
        a, b = registry.create("c"), registry.create("c")
        assert a is not b
        assert isinstance(a, naive.Circle)
        assert (a.radius, a.color) == (2, "green")

    def test_mutating_a_clone_leaves_the_exemplar_alone(self) -> None:
        registry = naive.PrototypeRegistry()
        exemplar = naive.Circle(radius=2, color="green")
        registry.register("c", exemplar)
        clone = registry.create("c")
        assert isinstance(clone, naive.Circle)
        clone.radius = 99
        assert exemplar.radius == 2


class TestPythonic:
    def test_factory_menu_produces_fresh_equal_instances(self) -> None:
        a, b = pythonic.create("small-red"), pythonic.create("small-red")
        assert a is not b
        assert a == b == pythonic.Circle(radius=1, color="red")

    def test_distinct_entries_differ(self) -> None:
        assert pythonic.create("big-blue") == pythonic.Circle(radius=10, color="blue")


class TestRealWorld:
    def test_shallow_copy_shares_nested_state(self) -> None:
        assert real_world.shallow_shares_nested_state(real_world.Board("t"))

    def test_deepcopy_is_independent(self) -> None:
        assert real_world.deep_is_independent(real_world.Board("t"))
