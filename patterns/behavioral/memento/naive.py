"""The Gang of Four Memento: originator, opaque memento, caretaker."""

from __future__ import annotations


class Memento:
    """Opaque by convention: only the originator reads its fields."""

    def __init__(self, text: str, cursor: int) -> None:
        self._text = text
        self._cursor = cursor


class Editor:
    """The originator."""

    def __init__(self) -> None:
        self.text = ""
        self.cursor = 0

    def type_text(self, text: str) -> None:
        self.text += text
        self.cursor = len(self.text)

    def save(self) -> Memento:
        return Memento(self.text, self.cursor)

    def restore(self, memento: Memento) -> None:
        self.text = memento._text
        self.cursor = memento._cursor


class History:
    """The caretaker: stores mementos, never looks inside."""

    def __init__(self) -> None:
        self._stack: list[Memento] = []

    def push(self, memento: Memento) -> None:
        self._stack.append(memento)

    def pop(self) -> Memento:
        return self._stack.pop()


def main() -> None:
    editor, history = Editor(), History()
    editor.type_text("hello")
    history.push(editor.save())
    editor.type_text(" world")
    print(f"before undo: {editor.text!r}")
    editor.restore(history.pop())
    print(f"after undo:  {editor.text!r}")


if __name__ == "__main__":
    main()
