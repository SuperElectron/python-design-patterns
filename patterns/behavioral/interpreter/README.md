---
id: behavioral/interpreter
name: Interpreter
aliases: [little-language, expression-tree]
guide_url: null
problem: "Represent a small language's grammar as data and evaluate sentences in it."
symptoms: ["mini query language", "user-supplied formulas", "rules engine", "evaluate expressions safely"]
verdict: prefer-alternative
caveats:
  - "Before inventing a language, check whether Python is the language: ast.literal_eval for data, a vetted ast walk for arithmetic, a real parser library beyond that."
  - "Never eval() user input — the safe version of this pattern exists precisely to avoid that."
stdlib_sightings: [ast.literal_eval, ast.NodeVisitor, re]
---

# Interpreter

## Problem

Users need to supply small formulas — spreadsheet expressions, feature-flag
rules — that your program must evaluate, safely, without shipping them to
`eval()`.

## Naive solution

`naive.py` is the GoF class-per-grammar-rule form: `Number`, `Add`, `Mul`
nodes each carrying `interpret()`, composed into an expression tree.

## Pythonic solution

The tree doesn't need a class per rule: nested tuples plus one recursive
function interpret the same grammar in a screenful. Adding an operation to
the language is one dict entry, not a class.

## In the wild

The `re` module is a full Interpreter-pattern implementation you use daily
(pattern → compiled program → evaluated against strings). `ast.literal_eval`
safely interprets Python's own literal grammar, and `real_world.py` builds
the classic safe arithmetic evaluator from a restricted `ast` walk.

## Verdict

**Prefer an alternative.** Python's own parsers (`ast`, `re`) cover most
"little language" needs; write a grammar only when you truly have a language.
