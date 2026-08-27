"""Behavioral tests for all three chain-of-responsibility variants."""

from patterns.behavioral.chain_of_responsibility import naive, pythonic, real_world


class TestNaive:
    def test_first_capable_handler_wins(self) -> None:
        chain = naive.build_chain()
        assert chain.handle(1) == "helpdesk resolves it"
        assert chain.handle(3) == "engineer resolves it"
        assert chain.handle(5) == "management escalation"

    def test_falling_off_the_end(self) -> None:
        assert naive.build_chain().handle(9) == "unhandled"


class TestPythonic:
    def test_list_chain_matches_naive(self) -> None:
        assert pythonic.handle(1) == "helpdesk resolves it"
        assert pythonic.handle(3) == "engineer resolves it"
        assert pythonic.handle(9) == "unhandled"

    def test_reordering_is_list_surgery(self) -> None:
        reordered: list[pythonic.Handler] = [pythonic.management, pythonic.helpdesk]
        assert pythonic.handle(1, reordered) == "management escalation"

    def test_empty_chain_is_explicitly_unhandled(self) -> None:
        assert pythonic.handle(1, []) == "unhandled"


class TestRealWorld:
    def test_record_propagates_to_ancestor_handler(self) -> None:
        sink: list[str] = []
        real_world.chain_delivery(sink)
        assert sink == ["cor_demo.web.requests: timeout on /api"]
