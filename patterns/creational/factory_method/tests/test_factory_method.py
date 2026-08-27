"""Behavioral tests for all three factory-method variants."""

from http.client import HTTPConnection, HTTPResponse

from patterns.creational.factory_method import naive, pythonic, real_world


class TestNaive:
    def test_each_subclass_builds_its_helper(self) -> None:
        assert naive.ExpressStore().ship() == "shipping via express"
        assert naive.StandardStore().ship() == "shipping via standard"


class TestPythonic:
    def test_dependency_injection(self) -> None:
        assert pythonic.InjectedStore(pythonic.express()).ship() == "shipping via express"

    def test_class_attribute_default(self) -> None:
        assert pythonic.Store().ship() == "shipping via standard"

    def test_subclass_overrides_class_attribute(self) -> None:
        assert pythonic.ExpressStore().ship() == "shipping via express"

    def test_instance_attribute_beats_class_attribute(self) -> None:
        assert pythonic.Store(shipment_factory=pythonic.express).ship() == "shipping via express"


class TestRealWorld:
    def test_stock_connection_builds_httpresponse(self) -> None:
        assert real_world.factory_of(HTTPConnection) is HTTPResponse

    def test_subclass_swaps_the_response_factory(self) -> None:
        assert real_world.factory_of(real_world.LoggedConnection) is real_world.LoggedResponse
