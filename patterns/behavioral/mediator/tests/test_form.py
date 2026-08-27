"""Behavioral tests for the Mediator pattern's library code."""

from __future__ import annotations

import pytest

from patterns.behavioral.mediator.pattern import Field, Form


class TestForm:
    class _Doubler(Form):
        """Minimal mediator: derived state re-computed on every change."""

        def __init__(self) -> None:
            super().__init__()
            self.rechecks = 0
            self.left = self.add_field("left")
            self.right = self.add_field("right")
            self.combined = ""
            self.recheck()

        def recheck(self) -> None:
            self.rechecks += 1
            self.combined = f"{self.left.value}+{self.right.value}"

    def test_fields_notify_their_mediator(self) -> None:
        form = self._Doubler()
        form.left.set("a")
        form.right.set("b")
        assert form.combined == "a+b"
        assert form.rechecks == 3  # construction + two sets

    def test_add_field_refuses_duplicate_names(self) -> None:
        form = self._Doubler()
        with pytest.raises(ValueError, match="already registered"):
            form.add_field("left")

    def test_field_names_keep_registration_order(self) -> None:
        form = self._Doubler()
        assert form.field_names() == ["left", "right"]

    def test_recheck_is_the_subclass_contract(self) -> None:
        with pytest.raises(NotImplementedError):
            Form().recheck()


class TestField:
    def test_set_updates_value_then_notifies(self) -> None:
        seen: list[str] = []
        field = Field(notify=lambda: seen.append(field.value))
        field.set("hello")
        assert field.value == "hello"
        assert seen == ["hello"]  # notify observed the *new* value

    def test_every_set_notifies(self) -> None:
        count = 0

        def bump() -> None:
            nonlocal count
            count += 1

        field = Field(notify=bump)
        field.set("a")
        field.set("a")  # even an unchanged value reports; dedup is the mediator's call
        assert count == 2

    def test_direct_write_does_not_notify(self) -> None:
        """Mediators write .value directly to avoid re-entering themselves."""
        count = 0

        def bump() -> None:
            nonlocal count
            count += 1

        field = Field(notify=bump)
        field.value = "silent"
        assert count == 0
