"""Behavioral tests for the composition-over-inheritance unit."""

from patterns.principle.composition_over_inheritance import naive, pythonic, real_world


class TestNaive:
    def test_combination_class_works_but_had_to_exist(self) -> None:
        sink: list[str] = []
        logger = naive.FilteredUppercaseLogger("error", sink)
        logger.log("error: disk full")
        logger.log("all fine")
        assert sink == ["ERROR: DISK FULL"]

    def test_the_explosion_is_real(self) -> None:
        # Four classes for two axes -- the M x N cost, in the flesh.
        assert issubclass(naive.FilteredUppercaseLogger, naive.FilteredLogger)
        assert issubclass(naive.FilteredLogger, naive.Logger)


class TestPythonic:
    def test_composed_behavior_matches_the_combination_class(self) -> None:
        logger = pythonic.Logger(filters=(pythonic.contains("error"),), transform=str.upper)
        logger.log("error: disk full")
        logger.log("all fine")
        assert logger.sink == ["ERROR: DISK FULL"]

    def test_new_combination_is_a_constructor_call(self) -> None:
        plain = pythonic.Logger(filters=(pythonic.contains("warn"),))
        plain.log("warn: low disk")
        plain.log("error: ignored here")
        assert plain.sink == ["warn: low disk"]

    def test_no_filters_means_log_everything(self) -> None:
        logger = pythonic.Logger()
        logger.log("anything")
        assert logger.sink == ["anything"]


class TestRealWorld:
    def test_stdlib_logging_composes_filter_and_handler(self) -> None:
        sink: list[str] = []
        logger = real_world.build_error_logger("pdp-test", sink)
        logger.info("error: disk full")
        logger.info("all fine")
        assert sink == ["error: disk full"]
