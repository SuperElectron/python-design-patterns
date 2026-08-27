"""Generate the README catalog table from frontmatter -- and keep it honest.

``python -m design_patterns.readme_table`` rewrites the block between the
markers in README.md; ``--check`` exits non-zero if the block has drifted,
which CI runs so the table can never rot.
"""

from __future__ import annotations

import sys
from pathlib import Path

from design_patterns.catalog import find_patterns_root, load_catalog

BEGIN = "<!-- catalog:begin (generated: make readme) -->"
END = "<!-- catalog:end -->"

_GROUP_ORDER = ["principle", "python", "creational", "structural", "behavioral", "modern"]
_GROUP_TITLES = {
    "principle": "Principles",
    "python": "Python-native",
    "creational": "Creational (GoF)",
    "structural": "Structural (GoF)",
    "behavioral": "Behavioral (GoF)",
    "modern": "Modern Python",
}
_VERDICT_BADGES = {
    "pythonic": "✅ pythonic",
    "use-with-care": "⚠️ use with care",
    "prefer-alternative": "🔄 prefer alternative",
}


def render_table() -> str:
    catalog = load_catalog()
    lines: list[str] = []
    for group in _GROUP_ORDER:
        members = [p for p in catalog.patterns if p.group == group]
        if not members:
            continue
        lines.append(f"\n### {_GROUP_TITLES[group]}\n")
        lines.append("| Pattern | Verdict | Problem it solves |")
        lines.append("|---|---|---|")
        for p in sorted(members, key=lambda p: p.slug):
            link = f"[{p.name}](patterns/{p.id}/)"
            lines.append(f"| {link} | {_VERDICT_BADGES[p.verdict]} | {p.problem} |")
    return "\n".join(lines) + "\n"


def apply(readme: Path) -> str:
    text = readme.read_text()
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n{render_table()}{END}{tail}"


def main() -> None:
    readme = find_patterns_root().parent / "README.md"
    fresh = apply(readme)
    if "--check" in sys.argv:
        if fresh != readme.read_text():
            print("README catalog table is stale: run `make readme`", file=sys.stderr)
            raise SystemExit(1)
        print("README catalog table is current")
        return
    readme.write_text(fresh)
    print(f"wrote {readme}")


if __name__ == "__main__":
    main()
