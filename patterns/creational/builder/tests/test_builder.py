"""Behavioral tests for all three builder variants."""

from patterns.creational.builder import naive, pythonic, real_world


class TestNaive:
    def test_director_reuses_steps_across_representations(self) -> None:
        director = naive.Director()
        stone = director.construct(naive.StoneHouseBuilder())
        wood = director.construct(naive.WoodHouseBuilder())
        assert stone.describe() == "stone walls + slate roof"
        assert wood.describe() == "timber walls + shingle roof"

    def test_each_construct_yields_a_fresh_product(self) -> None:
        director = naive.Director()
        assert director.construct(naive.StoneHouseBuilder()) is not director.construct(
            naive.StoneHouseBuilder()
        )


class TestPythonic:
    def test_kwargs_builder(self) -> None:
        pizza = pythonic.order_pizza("large", "basil")
        assert (pizza.size, pizza.toppings) == ("large", ("basil",))

    def test_staged_builder_chains_and_freezes(self) -> None:
        pizza = pythonic.PizzaBuilder(size="small").topped_with("olive", "caper").build()
        assert pizza == pythonic.Pizza(size="small", toppings=("olive", "caper"))

    def test_product_is_immutable(self) -> None:
        import dataclasses

        import pytest

        with pytest.raises(dataclasses.FrozenInstanceError):
            pythonic.Pizza("medium").size = "large"  # type: ignore[misc]


class TestRealWorld:
    def test_email_assembles_headers_and_body(self) -> None:
        msg = real_world.build_email("a@x.com", "b@x.com", "s", "body\n")
        assert msg["To"] == "b@x.com"
        assert msg.get_content() == "body\n"
