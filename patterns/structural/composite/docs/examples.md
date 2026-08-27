# Composite — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing composite-shaped code.

## Python standard library

- **`pathlib.Path`** — files and directories behind one interface;
  `iterdir()` walks one level, `rglob()` recurses the whole composite. The
  operations every node answers (`exists()`, `stat()`, `name`) coexist with
  directory-only ones (`iterdir()`), an interface-honesty compromise worth
  studying. [docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)
- **`xml.etree.ElementTree.Element`** — elements holding child elements, one
  API all the way down; `iter()` is the uniform deep traversal.
  [docs.python.org/3/library/xml.etree.elementtree.html](https://docs.python.org/3/library/xml.etree.elementtree.html)
- **`ast`** — Python source as a uniform node tree; `ast.walk` and
  `NodeVisitor` traverse without asking node kinds for structure.
  [docs.python.org/3/library/ast.html](https://docs.python.org/3/library/ast.html)

## Major ecosystems

- **Qt object trees (PyQt/PySide).** Every `QObject` may parent children;
  ownership, event propagation, and deletion all recurse the tree — a
  composite carrying lifecycle semantics, not just totals.
  [doc.qt.io/qt-6/objecttrees.html](https://doc.qt.io/qt-6/objecttrees.html)

## Design discussion

- **python-patterns.guide, Composite chapter** — the argument this unit's
  caveat encodes: side with interface honesty (child management on
  containers only) over the classic form's uniform-but-lying component.
  [python-patterns.guide/gang-of-four/composite/](https://python-patterns.guide/gang-of-four/composite/)

## What to notice across all of them

None of the production composites make leaves carry child management:
`ElementTree` leaves are just elements with no children, `ast` leaves are
nodes whose fields hold no lists, and Qt children live on the parent. The
uniformity that matters to callers is the *operation* (walk, size, iterate),
not the mutation API — which is exactly the guide's honesty argument.
