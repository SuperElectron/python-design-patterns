"""Behavioral tests for all three adapter variants."""

import io

from patterns.structural.adapter import naive, pythonic, real_world


class TestNaive:
    def test_adapter_translates_the_interface(self) -> None:
        adapter = naive.SensorAdapter(naive.FahrenheitSensor())
        assert adapter.celsius() == 20.0

    def test_client_code_sees_only_the_target_interface(self) -> None:
        assert naive.describe(naive.SensorAdapter(naive.FahrenheitSensor())) == "20.0 °C"


class TestPythonic:
    def test_function_adapter(self) -> None:
        read = pythonic.celsius_reader(pythonic.FahrenheitSensor())
        assert read() == 20.0

    def test_class_adapter_translates_and_forwards(self) -> None:
        adapter = pythonic.CelsiusAdapter(pythonic.FahrenheitSensor())
        assert adapter.celsius() == 20.0
        assert adapter.vendor_id() == "acme-42"  # forwarded untouched


class TestRealWorld:
    def test_textiowrapper_adapts_bytes_to_str(self) -> None:
        text = real_world.read_as_text(io.BytesIO("héllo\n".encode()))
        assert text == "héllo\n"
        assert isinstance(text, str)
