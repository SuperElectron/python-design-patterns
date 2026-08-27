"""Behavioral tests for all three state variants."""

from patterns.behavioral.state import naive, pythonic, real_world


class TestNaive:
    def test_full_cycle(self) -> None:
        turnstile = naive.Turnstile()
        assert turnstile.push() == "locked: push refused"
        assert turnstile.coin() == "unlocked"
        assert turnstile.coin() == "already unlocked: coin returned"
        assert turnstile.push() == "pushed through, locking"
        assert turnstile.push() == "locked: push refused"


class TestPythonic:
    def test_table_machine_matches_naive(self) -> None:
        machine = pythonic.Turnstile()
        outputs = [machine.handle(e) for e in ("push", "coin", "coin", "push", "push")]
        assert outputs == [
            "locked: push refused",
            "unlocked",
            "already unlocked: coin returned",
            "pushed through, locking",
            "locked: push refused",
        ]

    def test_generator_machine(self) -> None:
        gen = pythonic.turnstile_machine()
        assert next(gen) == "ready"
        assert gen.send("push") == "locked: push refused"
        assert gen.send("coin") == "unlocked"
        assert gen.send("coin") == "already unlocked: coin returned"
        assert gen.send("push") == "pushed through, locking"


class TestRealWorld:
    def test_scanner_extracts_blocks(self) -> None:
        text = ["x", "BEGIN", "a", "b", "END", "y", "BEGIN", "c", "END"]
        assert list(real_world.blocks(text)) == [["a", "b"], ["c"]]

    def test_unterminated_block_yields_partial(self) -> None:
        assert list(real_world.blocks(["BEGIN", "a"])) == [["a"]]
