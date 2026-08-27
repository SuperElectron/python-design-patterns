# Visitor — putting it into a system

## The smell it fixes

Either a growing `isinstance` ladder duplicated in every operation:

```python
def to_markdown(node):
    if isinstance(node, Paragraph):
        ...
    elif isinstance(node, Section):
        ...
    elif isinstance(node, CodeBlock):
        ...  # copy-pasted into to_html,
    ...  # word_count, lint, ...
```

…or its mirror image: node classes accreting one method per operation
(`to_markdown`, `to_html`, `word_count`, …) until every new operation is a
cross-cutting edit of the whole file.

## Steps

1. **Make the nodes plain data.** Frozen dataclasses; a union alias
   (`Block = Paragraph | CodeBlock | ...`) names the family. No `accept`,
   no base class needed.
2. **One `Operation` per operation**, typed by its result:

   ```python
   from patterns.behavioral.visitor import Operation

   markdown: Operation[str] = Operation("markdown")


   @markdown.register
   def _(node: Paragraph) -> str:
       return node.text
   ```

3. **One case per node type**, dispatched by the annotation. Composite nodes
   recurse by calling the operation on their children — recursion lives in
   the cases, not in a walker.
4. **Keep the default strict.** `Operation` raises `UnhandledNodeError`
   (naming the handled types) for an unregistered node — a new node type
   then fails the first test that touches it, instead of being silently
   skipped.
5. **Test the promise.** One test should add a brand-new operation without
   editing `nodes.py` — that is the property the pattern exists to provide.

## Python idioms that keep it small

- **Dispatch on annotations** (`def _(node: Section) -> str`) keeps each
  case self-documenting; `singledispatch` keys on the annotated type, so
  the function names don't matter — every case can be named `_`.
- **Same-module registration** keeps an operation reviewable as one unit —
  a dispatch family scattered across files is the ladder again, hidden.
- **`ast.NodeVisitor` at the boundary:** when the tree is Python source,
  subclass the stdlib visitor rather than rebuilding dispatch over `ast`
  nodes.

## Pitfalls

- **A permissive default** (`return ""` / `pass` for unknown nodes) turns
  new node types into silent data loss. Strictness is the safety net.
- **Growing the node family is expensive by design** — every operation needs
  a new case. If node types churn, the pattern is working against you;
  prefer methods on the nodes.
- **Inheritance surprises:** `singledispatch` matches subclasses; a case for
  a base dataclass will absorb its subclasses unless more-specific cases are
  registered.
- **State in the operation.** Cases should be pure node → result; an
  operation needing traversal state (numbering, indentation depth) should
  pass it explicitly or wrap results, not stash it in globals.

## Worked example

[`examples/doc_exporters/`](../examples/doc_exporters/) applies every step
above to a document tree — Markdown, plain-text, and word-count operations
over five node types the operations never edit:

```bash
uv run python -m patterns.behavioral.visitor.examples.doc_exporters.main
```
