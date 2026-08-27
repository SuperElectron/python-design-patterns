"""The mediator without a Colleague hierarchy.

Widgets take a ``notify`` callable; the coordinator holds every interaction
rule in one place and the widgets hold none.
"""

from __future__ import annotations

from collections.abc import Callable


class TextField:
    def __init__(self, notify: Callable[[], None]) -> None:
        self.text = ""
        self._notify = notify

    def type_text(self, text: str) -> None:
        self.text = text
        self._notify()


class SignupForm:
    """The mediator: rules in one readable method."""

    def __init__(self) -> None:
        self.username = TextField(self._recheck)
        self.password = TextField(self._recheck)
        self.submit_enabled = False

    def _recheck(self) -> None:
        self.submit_enabled = bool(self.username.text) and len(self.password.text) >= 8


def main() -> None:
    form = SignupForm()
    form.username.type_text("ada")
    form.password.type_text("short")
    print(f"weak password:  {form.submit_enabled}")
    form.password.type_text("correcthorse")
    print(f"valid form:     {form.submit_enabled}")


if __name__ == "__main__":
    main()
