"""Behavioral tests for the template-registry pattern code."""

from dataclasses import dataclass
from functools import partial

import pytest

from patterns.creational.prototype.pattern import TemplateRegistry


@dataclass(frozen=True)
class Widget:
    label: str
    size: int = 1


class TestTemplateRegistry:
    def test_every_create_builds_a_fresh_product(self) -> None:
        menu: TemplateRegistry[Widget] = TemplateRegistry()
        menu.register("small", partial(Widget, label="small"))
        a, b = menu.create("small"), menu.create("small")
        assert a is not b
        assert a == b

    def test_overrides_customize_one_product_only(self) -> None:
        menu: TemplateRegistry[Widget] = TemplateRegistry()
        menu.register("small", partial(Widget, label="small"))
        big = menu.create("small", size=9)
        assert big.size == 9
        assert menu.create("small").size == 1  # template untouched

    def test_unknown_template_names_the_menu(self) -> None:
        menu: TemplateRegistry[Widget] = TemplateRegistry()
        menu.register("small", partial(Widget, label="small"))
        with pytest.raises(ValueError, match=r"unknown template 'huge' \(has: \['small'\]\)"):
            menu.create("huge")

    def test_register_returns_the_template(self) -> None:
        menu: TemplateRegistry[Widget] = TemplateRegistry()

        def blank() -> Widget:
            return Widget(label="blank")

        assert menu.register("blank", blank) is blank
        assert menu.names() == ["blank"]

    def test_overrides_refuse_non_dataclass_products(self) -> None:
        menu: TemplateRegistry[str] = TemplateRegistry()
        menu.register("greeting", lambda: "hello")
        assert menu.create("greeting") == "hello"
        with pytest.raises(TypeError, match="dataclass"):
            menu.create("greeting", tone="loud")
