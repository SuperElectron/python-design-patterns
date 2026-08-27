"""Behavioral tests for all three bridge variants."""

from patterns.structural.bridge import naive, pythonic, real_world


class TestNaive:
    def test_same_abstraction_different_implementations(self) -> None:
        assert naive.Circle(naive.VectorRenderer(), 2.0).draw() == "<circle r=2.0/>"
        assert "pixels" in naive.Circle(naive.RasterRenderer(), 2.0).draw()


class TestPythonic:
    def test_injected_renderer_decides_output(self) -> None:
        assert pythonic.Circle(2.0, pythonic.Vector()).draw() == "<circle r=2.0/>"
        assert "pixels" in pythonic.Circle(2.0, pythonic.Raster()).draw()

    def test_any_duck_typed_implementor_works(self) -> None:
        class Ascii:
            def circle(self, radius: float) -> str:
                return "o" * int(radius)

        assert pythonic.Circle(3.0, Ascii()).draw() == "ooo"


class TestRealWorld:
    def test_one_logger_call_reaches_both_implementations(self) -> None:
        a: list[str] = []
        b: list[str] = []
        real_world.logger_with_two_backends("bridge-test", a, b).info("msg")
        assert a == ["msg"] and b == ["msg"]
