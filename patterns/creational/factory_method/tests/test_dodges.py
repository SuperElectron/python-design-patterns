"""Behavioral tests for the pattern's three dodges."""

from patterns.creational.factory_method.pattern import (
    ExpressStore,
    InjectedStore,
    Shipment,
    Store,
    express,
)


class TestDependencyInjection:
    def test_receives_the_object_instead_of_building_it(self) -> None:
        assert InjectedStore(express()).ship() == "shipping via express"


class TestClassAttributeFactory:
    def test_default_factory(self) -> None:
        assert Store().ship() == "shipping via standard"

    def test_subclass_overrides_the_factory(self) -> None:
        assert ExpressStore().ship() == "shipping via express"

    def test_any_callable_is_accepted(self) -> None:
        assert Store(shipment_factory=lambda: Shipment("drone")).ship() == "shipping via drone"


class TestInstanceAttributeFactory:
    def test_instance_override_beats_class_attribute(self) -> None:
        assert Store(shipment_factory=express).ship() == "shipping via express"

    def test_instance_override_leaves_the_class_alone(self) -> None:
        Store(shipment_factory=express)
        assert Store().ship() == "shipping via standard"
