"""Immutable state makes mementos free.

The state is a frozen dataclass; a snapshot IS the state object, history is
a list of them, and undo is pop. No Memento class, no copying.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class EditorState:
    text: str = ""
    cursor: int = 0


class Editor:
    def __init__(self) -> None:
        self.state = EditorState()
        self._history: list[EditorState] = []

    def type_text(self, text: str) -> None:
        self._history.append(self.state)  # the old state object is the memento
        new_text = self.state.text + text
        self.state = replace(self.state, text=new_text, cursor=len(new_text))

    def undo(self) -> None:
        if self._history:
            self.state = self._history.pop()


def main() -> None:
    editor = Editor()
    editor.type_text("hello")
    editor.type_text(" world")
    print(f"before undo: {editor.state.text!r}")
    editor.undo()
    print(f"after undo:  {editor.state.text!r}")


if __name__ == "__main__":
    main()
