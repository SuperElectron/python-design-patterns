"""Behavioral tests for all three flyweight variants."""

from patterns.structural.flyweight import naive, pythonic, real_world


class TestNaive:
    def test_same_request_returns_shared_instance(self) -> None:
        factory = naive.CardFactory()
        assert factory.get("9", "♥") is factory.get("9", "♥")

    def test_pool_counts_distinct_only(self) -> None:
        factory = naive.CardFactory()
        for _ in range(10):
            factory.get("9", "♥")
        factory.get("A", "♠")
        assert factory.distinct_cards == 2


class TestPythonic:
    def test_lru_cache_factory_shares(self) -> None:
        assert pythonic.get_card("2", "♦") is pythonic.get_card("2", "♦")

    def test_dunder_new_shares_on_plain_construction(self) -> None:
        assert pythonic.Card("9", "♥") is pythonic.Card("9", "♥")

    def test_distinct_values_stay_distinct(self) -> None:
        assert pythonic.Card("9", "♥") is not pythonic.Card("A", "♠")


class TestRealWorld:
    def test_small_int_interning(self) -> None:
        assert real_world.small_ints_are_interned()

    def test_sys_intern(self) -> None:
        assert real_world.interned_strings_share_identity()
