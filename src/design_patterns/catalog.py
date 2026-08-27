"""Load the pattern catalog from ``patterns/<group>/<slug>/README.md`` frontmatter.

Each unit's README carries a YAML frontmatter block; this module parses and
validates it into typed :class:`Pattern` objects. The MCP server, the
generated README table, and CI's schema check all consume this loader, so a
schema violation here fails loudly rather than propagating bad data.
"""

from __future__ import annotations

import importlib.util
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal, get_args

Verdict = Literal["pythonic", "use-with-care", "prefer-alternative"]
VariantName = Literal["naive", "pythonic", "real_world"]

VERDICTS: tuple[str, ...] = get_args(Verdict)
VARIANTS: tuple[str, ...] = get_args(VariantName)

_REQUIRED_KEYS = frozenset({"id", "name", "guide_url", "problem", "symptoms", "verdict", "caveats"})


class CatalogError(ValueError):
    """A pattern unit violates the catalog schema."""


@dataclass(frozen=True)
class Pattern:
    """One validated pattern unit."""

    id: str
    name: str
    problem: str
    verdict: Verdict
    aliases: tuple[str, ...] = ()
    guide_url: str | None = None
    symptoms: tuple[str, ...] = ()
    caveats: tuple[str, ...] = ()
    stdlib_sightings: tuple[str, ...] = ()
    prose: str = field(default="", repr=False, compare=False)
    path: Path = field(default_factory=Path, repr=False, compare=False)

    @property
    def group(self) -> str:
        return self.id.split("/", 1)[0]

    @property
    def slug(self) -> str:
        return self.id.split("/", 1)[1]

    def variants(self) -> dict[str, Path]:
        """The example files this unit actually ships."""
        return {v: self.path / f"{v}.py" for v in VARIANTS if (self.path / f"{v}.py").is_file()}


def _split_frontmatter(text: str, readme: Path) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise CatalogError(f"{readme}: README must start with a '---' frontmatter block")
    try:
        frontmatter, prose = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise CatalogError(f"{readme}: unterminated frontmatter block") from exc
    return frontmatter, prose.strip()


def _str_tuple(raw: object, key: str, readme: Path) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise CatalogError(f"{readme}: '{key}' must be a list")
    return tuple(str(item) for item in raw)


def _parse_pattern(readme: Path, root: Path) -> Pattern:
    import yaml

    frontmatter, prose = _split_frontmatter(readme.read_text(encoding="utf-8"), readme)
    try:
        data = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        raise CatalogError(f"{readme}: invalid YAML frontmatter: {exc}") from exc
    if not isinstance(data, dict):
        raise CatalogError(f"{readme}: frontmatter must be a mapping")

    missing = _REQUIRED_KEYS - data.keys()
    if missing:
        raise CatalogError(f"{readme}: missing frontmatter keys: {sorted(missing)}")

    unit_dir = readme.parent
    expected_id = f"{unit_dir.parent.name}/{unit_dir.name}"
    if data["id"] != expected_id:
        raise CatalogError(f"{readme}: id {data['id']!r} != directory {expected_id!r}")

    verdict = data["verdict"]
    if verdict not in VERDICTS:
        raise CatalogError(f"{readme}: verdict {verdict!r} not one of {VERDICTS}")

    guide_url = data["guide_url"]
    if guide_url is not None and not str(guide_url).startswith("https://"):
        raise CatalogError(f"{readme}: guide_url must be https or null")

    problem = str(data["problem"]).strip()
    if not problem:
        raise CatalogError(f"{readme}: 'problem' must be a non-empty sentence")

    pattern = Pattern(
        id=str(data["id"]),
        name=str(data["name"]),
        problem=problem,
        verdict=verdict,
        aliases=_str_tuple(data.get("aliases"), "aliases", readme),
        guide_url=None if guide_url is None else str(guide_url),
        symptoms=_str_tuple(data["symptoms"], "symptoms", readme),
        caveats=_str_tuple(data["caveats"], "caveats", readme),
        stdlib_sightings=_str_tuple(data.get("stdlib_sightings"), "stdlib_sightings", readme),
        prose=prose,
        path=unit_dir,
    )
    if not pattern.variants():
        raise CatalogError(f"{readme}: unit ships no naive/pythonic/real_world example")
    return pattern


@dataclass(frozen=True)
class Catalog:
    """All validated pattern units, ordered by id."""

    patterns: tuple[Pattern, ...]

    def get(self, pattern_id: str) -> Pattern:
        for pattern in self.patterns:
            if pattern.id == pattern_id:
                return pattern
        raise KeyError(pattern_id)

    def ids(self) -> tuple[str, ...]:
        return tuple(p.id for p in self.patterns)

    def to_json(self) -> str:
        """The ``catalog://index`` payload: everything except prose and paths."""
        entries = []
        for p in self.patterns:
            entry = asdict(p)
            del entry["prose"], entry["path"]
            entry["variants"] = sorted(p.variants())
            entries.append(entry)
        return json.dumps(entries, indent=2)


def find_patterns_root(start: Path | None = None) -> Path:
    """Locate the ``patterns/`` directory.

    Works both from a repo checkout (walk upward from this file) and from an
    installed wheel (the ``patterns`` package ships inside the distribution).
    """
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        candidate = parent / "patterns"
        if candidate.is_dir():
            return candidate
    spec = importlib.util.find_spec("patterns")
    if spec is not None and spec.origin is not None:
        return Path(spec.origin).parent
    raise CatalogError(f"no patterns/ directory above {here} and no installed patterns package")


def load_catalog(root: Path | None = None) -> Catalog:
    """Parse and validate every unit under ``root`` (default: the repo's patterns/)."""
    patterns_root = root if root is not None else find_patterns_root()
    readmes = sorted(patterns_root.glob("*/*/README.md"))
    if not readmes:
        raise CatalogError(f"no pattern units found under {patterns_root}")
    return Catalog(patterns=tuple(_parse_pattern(r, patterns_root) for r in readmes))
