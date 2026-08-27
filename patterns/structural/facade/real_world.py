"""``shutil.make_archive``: one call fronting the zipfile machinery.

Behind the facade: walking the tree, creating the archive, writing entries,
closing handles. The full ``zipfile`` API stays available beside it.
"""

from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path


def archive_directory(source: Path, out_dir: Path) -> Path:
    """The facade in action: an entire directory zipped in one call."""
    return Path(shutil.make_archive(str(out_dir / "backup"), "zip", root_dir=source))


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "src"
        source.mkdir()
        (source / "a.txt").write_text("hello")
        archive = archive_directory(source, Path(tmp))
        with zipfile.ZipFile(archive) as zf:  # the subsystem, still public
            print(f"{archive.name} contains {zf.namelist()}")


if __name__ == "__main__":
    main()
