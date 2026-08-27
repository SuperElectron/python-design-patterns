"""Behavioral tests for the Skeleton building block."""

from __future__ import annotations

from patterns.behavioral.template_method import Skeleton, discard, keep_all


def recording_skeleton(trace: list[str]) -> Skeleton[str, str]:
    def fetch() -> str:
        trace.append("fetch")
        return "raw"

    def transform(data: str) -> str:
        trace.append("transform")
        return f"{data}+clean"

    def render(data: str) -> str:
        trace.append("render")
        return f"[{data}]"

    def deliver(document: str) -> None:
        trace.append(f"deliver:{document}")

    return Skeleton(fetch=fetch, transform=transform, render=render, deliver=deliver)


class TestSpine:
    def test_run_executes_the_four_steps_in_fixed_order(self) -> None:
        trace: list[str] = []
        result = recording_skeleton(trace).run()
        assert result == "[raw+clean]"
        assert trace == ["fetch", "transform", "render", "deliver:[raw+clean]"]

    def test_the_delivered_document_is_the_rendered_one(self) -> None:
        trace: list[str] = []
        recording_skeleton(trace).run()
        assert trace[-1] == "deliver:[raw+clean]"


class TestVariation:
    def test_with_steps_swaps_one_step_and_keeps_the_rest(self) -> None:
        trace: list[str] = []
        variant = recording_skeleton(trace).with_steps(render=lambda data: data.upper())
        assert variant.run() == "RAW+CLEAN"
        assert "fetch" in trace  # untouched steps still ran

    def test_with_steps_returns_a_new_skeleton_leaving_the_original_alone(self) -> None:
        trace: list[str] = []
        base = recording_skeleton(trace)
        base.with_steps(render=lambda data: "other")
        assert base.run() == "[raw+clean]"  # original unchanged


class TestExplicitNoOps:
    def test_keep_all_is_the_identity_transform(self) -> None:
        assert keep_all((1, 2)) == (1, 2)

    def test_discard_delivers_nowhere(self) -> None:
        discard("document")  # accepts any document, produces no side effect
