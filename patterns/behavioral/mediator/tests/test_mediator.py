"""Behavioral tests for all three mediator variants."""

from patterns.behavioral.mediator import naive, pythonic, real_world


class TestNaive:
    def test_rules_live_in_the_mediator(self) -> None:
        dialog = naive.SignupDialog()
        dialog.username.type_text("ada")
        assert not dialog.submit.enabled
        dialog.password.type_text("correcthorse")
        assert dialog.submit.enabled

    def test_weak_password_keeps_submit_disabled(self) -> None:
        dialog = naive.SignupDialog()
        dialog.username.type_text("ada")
        dialog.password.type_text("short")
        assert not dialog.submit.enabled


class TestPythonic:
    def test_form_coordination(self) -> None:
        form = pythonic.SignupForm()
        form.username.type_text("ada")
        form.password.type_text("correcthorse")
        assert form.submit_enabled

    def test_widgets_know_no_rules(self) -> None:
        # A TextField is reusable with any notify callable -- no form coupling.
        pings: list[str] = []
        field = pythonic.TextField(lambda: pings.append("changed"))
        field.type_text("x")
        assert pings == ["changed"]


class TestRealWorld:
    def test_queue_mediates_producer_and_consumer(self) -> None:
        assert real_world.pipeline(["a", "b", "c"]) == ["A", "B", "C"]

    def test_empty_stream(self) -> None:
        assert real_world.pipeline([]) == []
