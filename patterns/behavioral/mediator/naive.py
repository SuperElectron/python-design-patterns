"""The Gang of Four Mediator: colleagues talk only to the dialog."""

from __future__ import annotations


class Widget:
    def __init__(self, mediator: SignupDialog, name: str) -> None:
        self.mediator = mediator
        self.name = name

    def changed(self) -> None:
        self.mediator.widget_changed(self)


class TextField(Widget):
    def __init__(self, mediator: SignupDialog, name: str) -> None:
        super().__init__(mediator, name)
        self.text = ""

    def type_text(self, text: str) -> None:
        self.text = text
        self.changed()


class Button(Widget):
    def __init__(self, mediator: SignupDialog, name: str) -> None:
        super().__init__(mediator, name)
        self.enabled = False


class SignupDialog:
    """All interaction rules live here; widgets know none of them."""

    def __init__(self) -> None:
        self.username = TextField(self, "username")
        self.password = TextField(self, "password")
        self.submit = Button(self, "submit")

    def widget_changed(self, _widget: Widget) -> None:
        self.submit.enabled = bool(self.username.text) and len(self.password.text) >= 8


def main() -> None:
    dialog = SignupDialog()
    dialog.username.type_text("ada")
    print(f"after username: submit enabled = {dialog.submit.enabled}")
    dialog.password.type_text("correcthorse")
    print(f"after password: submit enabled = {dialog.submit.enabled}")


if __name__ == "__main__":
    main()
