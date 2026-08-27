"""Behavioral tests for all three dependency-injection variants."""

from patterns.modern.dependency_injection import naive, pythonic, real_world


class TestNaive:
    def test_works_but_depends_on_the_real_clock(self) -> None:
        message = naive.GreetingService().greet("ada")
        # The strongest assertion possible without controlling the clock:
        assert message.endswith(", ada")
        assert message.startswith(("good morning", "good day"))


class TestPythonic:
    def test_injected_clock_makes_behavior_deterministic(self) -> None:
        morning = pythonic.GreetingService(hour_now=lambda: 9)
        evening = pythonic.GreetingService(hour_now=lambda: 20)
        assert morning.greet("ada") == "good morning, ada"
        assert evening.greet("ada") == "good day, ada"

    def test_injected_store_observes_writes(self) -> None:
        store: list[str] = []
        pythonic.GreetingService(store=store, hour_now=lambda: 9).greet("ada")
        assert store == ["good morning, ada"]

    def test_production_defaults_still_work(self) -> None:
        assert pythonic.GreetingService().greet("ada").endswith(", ada")


class TestRealWorld:
    def test_injected_sort_policy(self) -> None:
        assert real_world.sort_by_injected_policy(["b", "A", "c"]) == ["A", "b", "c"]

    def test_injected_encoder(self) -> None:
        assert real_world.dump_with_injected_encoder({"k": "v"}) == '{"K": "V"}'
