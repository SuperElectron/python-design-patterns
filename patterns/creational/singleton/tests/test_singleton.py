"""Behavioral tests for all three singleton variants."""

from patterns.creational.singleton import naive, pythonic, real_world


class TestNaive:
    def test_identity(self) -> None:
        assert naive.Logger() is naive.Logger()

    def test_state_is_shared(self) -> None:
        a = naive.Logger()
        a.lines.clear()
        naive.Logger().log("hi")
        assert a.lines == ["hi"]

    def test_reinit_does_not_wipe_state(self) -> None:
        a = naive.Logger()
        a.lines.clear()
        a.log("kept")
        naive.Logger()  # __init__ runs again; the guard must preserve state
        assert a.lines == ["kept"]


class TestPythonic:
    def test_module_global_is_stable(self) -> None:
        assert pythonic.logger is pythonic.logger

    def test_lazy_accessor_returns_same_instance(self) -> None:
        assert pythonic.get_logger() is pythonic.get_logger()

    def test_lazy_accessor_builds_a_real_logger(self) -> None:
        log = pythonic.get_logger()
        log.lines.clear()
        log.log("x")
        assert pythonic.get_logger().lines == ["x"]


class TestRealWorld:
    def test_none_identity(self) -> None:
        assert real_world.none_is_a_singleton()

    def test_module_identity(self) -> None:
        assert real_world.modules_are_singletons()
