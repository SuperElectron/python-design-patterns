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
    def test_templates_stamp_out_fresh_equal_jobs(self) -> None:
        a, b = pythonic.schedule("nightly-sales"), pythonic.schedule("nightly-sales")
        assert a is not b and a == b
        assert a.filters == ("exclude-test-accounts",)

    def test_per_run_overrides_leave_the_template_untouched(self) -> None:
        rush = pythonic.schedule("weekly-audit", fmt="csv")
        assert rush.fmt == "csv"
        assert pythonic.schedule("weekly-audit").fmt == "xlsx"

    def test_scheduler_queues_customized_jobs(self) -> None:
        scheduler = pythonic.Scheduler()
        scheduler.enqueue("nightly-sales")
        scheduler.enqueue("weekly-audit", recipients=("audit@x.com",))
        assert [j.name for j in scheduler.queue] == ["nightly-sales", "weekly-audit"]
        assert scheduler.queue[1].recipients == ("audit@x.com",)


class TestRealWorld:
    def test_shallow_copy_shares_nested_state(self) -> None:
        assert real_world.shallow_shares_nested_state(real_world.Board("t"))

    def test_deepcopy_is_independent(self) -> None:
        assert real_world.deep_is_independent(real_world.Board("t"))
