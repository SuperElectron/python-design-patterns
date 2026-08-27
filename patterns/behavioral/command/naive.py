"""The Gang of Four Command: interface, concrete commands, invoker with undo.

A text editor whose operations are objects. The invoker keeps history, so
undo is popping the stack and asking the command to reverse itself.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Document:
    """The receiver: the thing commands operate on."""

    def __init__(self) -> None:
        self.text = ""


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class AppendText(Command):
    def __init__(self, doc: Document, text: str) -> None:
        self.doc = doc
        self.text = text

    def execute(self) -> None:
        self.doc.text += self.text

    def undo(self) -> None:
        self.doc.text = self.doc.text[: -len(self.text)]


class Editor:
    """The invoker: runs commands and remembers them for undo."""

    def __init__(self) -> None:
        self._history: list[Command] = []

    def do(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()


def main() -> None:
    doc = Document()
    editor = Editor()
    editor.do(AppendText(doc, "hello"))
    editor.do(AppendText(doc, " world"))
    print(f"after edits: {doc.text!r}")
    editor.undo()
    print(f"after undo:  {doc.text!r}")


if __name__ == "__main__":
    main()
