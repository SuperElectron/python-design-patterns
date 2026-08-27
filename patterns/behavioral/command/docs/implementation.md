# Command — putting it into a system

## The smell it fixes

Undo implemented by snapshotting entire state ("save a copy of the document
before every change"), or an event log reverse-engineered from side effects.
Both grow unbounded and neither can answer "what exactly did the user do?".

## Steps

1. **Identify the operations** users trigger that must be reversible or
   auditable. Each becomes a command factory, not a subclass.
2. **Write each factory to capture its own inverse.** The critical rule:
   capture undo state *at execution time*. Deleting text must remember what
   it deleted — that memory is the command's whole reason to be an object:

   ```python
   def delete_span(doc: Document, position: int, length: int) -> Undoable:
       removed: list[str] = []  # filled by do, consumed by undo

       def do() -> None:
           removed.append(doc.delete(position, length))

       def undo() -> None:
           doc.insert(position, removed.pop())

       return Undoable(do=do, undo=undo, label=f"delete {length}@{position}")
   ```

3. **Route every mutation through one invoker.** `UndoStack.push` is the
   single door: nothing edits the receiver directly, or history lies.
4. **Give commands labels.** `stack.log()` is your audit trail and your
   macro recording for free.
5. **Test the round-trip property**: for any command, `do(); undo()` must
   restore the receiver exactly. Property-style tests catch asymmetric pairs.

## Python idioms that keep it small

- Command factories are **plain functions returning `Undoable`** — closures
  capture receiver and arguments; no Receiver/ConcreteCommand classes.
- Execute-only queues are **lists of callables**; `functools.partial`
  packages arguments without ceremony.
- A macro is `[stack.push(cmd) for cmd in recorded]` — replay is iteration.

## Pitfalls

- **Undo state captured too early.** Computing the inverse when the command
  is *built* (not executed) breaks as soon as commands run against a state
  that changed since construction.
- **Bypassing the invoker.** One direct mutation makes every later undo
  corrupt the receiver. The receiver's mutators should be package-private by
  convention.
- **Non-invertible operations** (send email, charge card) don't belong on an
  undo stack — model them as compensations (a *new* command), not undos.
- **Forgetting to clear redo on new pushes** — replaying a stale future
  corrupts state; `UndoStack` does this for you, keep the contract if you
  write your own.

## Worked example

[`examples/editor_undo/`](../examples/editor_undo/) applies every step to a
text editor — insert/delete/replace with undo, redo, and a session log:

```bash
uv run python -m patterns.behavioral.command.examples.editor_undo
```
