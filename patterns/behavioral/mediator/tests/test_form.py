"""Behavioral tests for the Mediator pattern's library code."""

from __future__ import annotations

from patterns.behavioral.mediator.pattern import Field


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
