"""Behavioral tests for all three facade variants."""

import tempfile
import zipfile
from pathlib import Path

from patterns.structural.facade import naive, pythonic, real_world


class TestNaive:
    def test_one_call_runs_the_whole_sequence(self) -> None:
        steps = naive.HomeTheaterFacade().watch_movie()
        assert steps == ["lights 10%", "projector on", "16:9", "amp on", "volume 5"]


class TestPythonic:
    def test_facade_covers_the_common_case(self) -> None:
        text = "the cat and the hat and the cat in the hat"
        assert pythonic.top_words(text, 2) == [("cat", 2), ("hat", 2)]

    def test_subsystem_stays_available_for_full_control(self) -> None:
        counts = pythonic.count(["the", "cat"], drop_stopwords=False)
        assert counts["the"] == 1


class TestRealWorld:
    def test_make_archive_facade(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "src"
            source.mkdir()
            (source / "a.txt").write_text("hello")
            archive = real_world.archive_directory(source, Path(tmp))
            assert archive.exists()
            with zipfile.ZipFile(archive) as zf:
                assert zf.namelist() == ["a.txt"]
