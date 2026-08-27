"""The stdlib's composite: ``xml.etree.ElementTree``.

An ``Element`` holds child ``Element`` objects; ``iter()`` walks the whole
tree through one interface, never asking a node whether it is a leaf.
(``pathlib.Path`` is the same idea over the file system.)
"""

from __future__ import annotations

import xml.etree.ElementTree as ET


def build_scene() -> ET.Element:
    scene = ET.Element("scene")
    ET.SubElement(scene, "circle", name="sun")
    cluster = ET.SubElement(scene, "group", name="cluster")
    ET.SubElement(cluster, "circle", name="a")
    ET.SubElement(cluster, "circle", name="b")
    return scene


def count_circles(root: ET.Element) -> int:
    """One recursive traversal, uniform over leaves and containers."""
    return sum(1 for _ in root.iter("circle"))


def main() -> None:
    scene = build_scene()
    print(ET.tostring(scene, encoding="unicode"))
    print(f"circles in tree: {count_circles(scene)}")


if __name__ == "__main__":
    main()
