"""The pythonic facade: a module-level function with good defaults.

The subsystem (tokenize / count / rank) stays public for callers who need
the controls; ``top_words`` is the one-call common case.
"""

from __future__ import annotations

import re
from collections import Counter

STOPWORDS = frozenset({"the", "a", "an", "and", "of", "to", "in"})


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def count(words: list[str], *, drop_stopwords: bool = True) -> Counter[str]:
    kept = [w for w in words if not (drop_stopwords and w in STOPWORDS)]
    return Counter(kept)


def rank(counts: Counter[str], n: int) -> list[tuple[str, int]]:
    return counts.most_common(n)


def top_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    """The facade: the whole pipeline, one call, sensible defaults."""
    return rank(count(tokenize(text)), n)


def main() -> None:
    text = "the cat and the hat and the cat in the hat"
    print(f"facade:        {top_words(text, 2)}")
    print(f"full controls: {rank(count(tokenize(text), drop_stopwords=False), 1)}")


if __name__ == "__main__":
    main()
