"""BM25 search over the pattern catalog. Pure stdlib, no network."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from design_patterns.catalog import Catalog, Pattern

_TOKEN = re.compile(r"[a-z0-9']+")

# Field weights: a hit in the problem statement or symptoms should count
# for more than a hit deep in the prose.
_WEIGHTS = {"name": 4.0, "aliases": 4.0, "problem": 3.0, "symptoms": 3.0, "prose": 1.0}


def _tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _document(pattern: Pattern) -> list[str]:
    tokens: list[str] = []
    fields = {
        "name": pattern.name,
        "aliases": " ".join(pattern.aliases),
        "problem": pattern.problem,
        "symptoms": " ".join(pattern.symptoms),
        "prose": pattern.prose,
    }
    for field, text in fields.items():
        weight = int(_WEIGHTS[field])
        tokens.extend(_tokenize(text) * weight)
    return tokens


@dataclass(frozen=True)
class Hit:
    pattern: Pattern
    score: float


class SearchIndex:
    """A small BM25 index over every unit's frontmatter and prose."""

    K1 = 1.5
    B = 0.75

    def __init__(self, catalog: Catalog) -> None:
        self._patterns = catalog.patterns
        self._docs = [_document(p) for p in self._patterns]
        self._doc_lens = [len(d) for d in self._docs]
        self._avg_len = sum(self._doc_lens) / len(self._docs)
        self._freqs = [{t: doc.count(t) for t in set(doc)} for doc in self._docs]
        self._df: dict[str, int] = {}
        for freq in self._freqs:
            for term in freq:
                self._df[term] = self._df.get(term, 0) + 1

    def _idf(self, term: str) -> float:
        n, df = len(self._docs), self._df.get(term, 0)
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def search(self, query: str, limit: int = 5) -> list[Hit]:
        terms = _tokenize(query)
        hits: list[Hit] = []
        for i, pattern in enumerate(self._patterns):
            score = 0.0
            for term in terms:
                tf = self._freqs[i].get(term, 0)
                if tf == 0:
                    continue
                norm = self.K1 * (1 - self.B + self.B * self._doc_lens[i] / self._avg_len)
                score += self._idf(term) * tf * (self.K1 + 1) / (tf + norm)
            if score > 0:
                hits.append(Hit(pattern, round(score, 3)))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:limit]
