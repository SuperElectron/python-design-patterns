---
id: behavioral/visitor
name: Visitor
aliases: [double-dispatch]
guide_url: null
problem: "Run a new operation over every node of an object structure without adding a method to every node class."
symptoms: ["walk an AST", "operation per node type", "double dispatch", "add behavior across a class family"]
verdict: prefer-alternative
caveats:
  - "functools.singledispatch dispatches on type without touching the node classes — the visitor with the accept() plumbing deleted."
  - "The subclass form survives where the stdlib hands it to you: ast.NodeVisitor is the right tool for walking Python source."
stdlib_sightings: [functools.singledispatch, ast.NodeVisitor]
---

# Visitor

## Problem

An expression tree (or document tree, or AST) needs new operations — render,
optimize, measure — and you'd rather not add a method to every node class for
every new operation.

## Naive solution

`naive.py` is the full GoF double dispatch: every node implements
`accept(visitor)`, every visitor implements one `visit_X` per node type.

## Pythonic solution

`functools.singledispatch` dispatches on the node's type directly — the
`accept()` plumbing evaporates, node classes stay untouched, and a new
operation is one decorated function per node type.

## In the wild

`ast.NodeVisitor` walks Python source with a `visit_ClassName` method per
node — the Visitor pattern as a supported stdlib API.

## Verdict

**Prefer an alternative:** `singledispatch`. Use `ast.NodeVisitor` when the
tree is Python itself.
