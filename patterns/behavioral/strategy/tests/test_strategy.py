"""Behavioral tests for all three strategy variants."""

from patterns.behavioral.strategy import naive, pythonic, real_world


def _cart() -> list[naive.LineItem]:
    return [naive.LineItem("banana", 30, 0.5), naive.LineItem("apple", 10, 1.5)]


class TestNaive:
    def test_bulk_promo_discounts_every_qualifying_line(self) -> None:
        # 30 bananas -> 15.00 total -> 1.50 off; apples don't qualify.
        order = naive.Order(_cart(), naive.BulkItemPromo())
        assert order.due() == 30.0 - 1.5

    def test_swapping_strategy_changes_result(self) -> None:
        cart = _cart()
        assert naive.Order(cart, naive.LargeOrderPromo()).due() == 30.0  # <10 products
        assert naive.Order(cart).due() == 30.0

    def test_regression_all_lines_counted(self) -> None:
        # The legacy repo returned inside the loop, scoring only the first line.
        cart = [naive.LineItem("a", 20, 1.0), naive.LineItem("b", 20, 2.0)]
        assert naive.BulkItemPromo().discount(naive.Order(cart)) == 2.0 + 4.0


class TestPythonic:
    def _order(self) -> pythonic.Order:
        return pythonic.Order(
            (pythonic.LineItem("banana", 30, 0.5), pythonic.LineItem("apple", 10, 1.5))
        )

    def test_function_is_the_strategy(self) -> None:
        assert pythonic.due(self._order(), pythonic.bulk_item) == 30.0 - 1.5

    def test_decorator_registered_all_strategies(self) -> None:
        assert pythonic.bulk_item in pythonic.promos
        assert pythonic.large_order in pythonic.promos

    def test_best_promo_picks_the_maximum(self) -> None:
        assert pythonic.best_promo(self._order()) == 1.5


class TestRealWorld:
    def test_key_functions_are_swappable_strategies(self) -> None:
        words = ["banana", "Fig", "cherry"]
        assert real_world.by_length(words) == ["Fig", "banana", "cherry"]
        assert real_world.case_insensitive(words) == ["banana", "cherry", "Fig"]
