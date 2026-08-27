"""Function decorators as importable, composable building blocks.

Each factory returns a decorator that wraps a callable with one cross-cutting
concern -- logging, timing, retry, rate limiting -- and every wrapper applies
``functools.wraps`` so the wrapped function keeps its identity. Effects
(clocks, sleeping, log sinks) are injected, so the decorators stay
deterministic under test.
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import ParamSpec, Protocol, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class Decorator(Protocol):
    """A signature-preserving wrapper: takes a callable, returns its like.

    The type variables live on ``__call__``, so one ``Decorator`` value can
    wrap functions of any signature — they bind per decoration, not when the
    factory runs.
    """

    def __call__(self, func: Callable[P, R], /) -> Callable[P, R]: ...


class RateLimitExceededError(RuntimeError):
    """The wrapped callable was invoked more often than its window allows."""


def logged(log: Callable[[str], None]) -> Decorator:
    """Report every call and its outcome to ``log``."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            log(f"-> {func.__name__}")
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                log(f"!! {func.__name__} raised {type(exc).__name__}")
                raise
            log(f"<- {func.__name__}")
            return result

        return wrapper

    return decorator


def timed(
    sink: Callable[[str, float], None],
    clock: Callable[[], float] = time.perf_counter,
) -> Decorator:
    """Report each call's duration (seconds) to ``sink`` as ``(name, elapsed)``."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            started = clock()
            try:
                return func(*args, **kwargs)
            finally:
                sink(func.__name__, clock() - started)

        return wrapper

    return decorator


def retry(
    attempts: int,
    *,
    on: tuple[type[Exception], ...] = (Exception,),
    wait: float = 0.0,
    sleep: Callable[[float], None] = time.sleep,
) -> Decorator:
    """Retry up to ``attempts`` times on the listed exceptions.

    The wait doubles after each failure (``wait``, ``2*wait``, ...); the last
    failure propagates. Inject ``sleep`` in tests to keep them instant.
    """
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            pause = wait
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except on:
                    if attempt == attempts:
                        raise
                    if pause:
                        sleep(pause)
                        pause *= 2
            raise AssertionError("unreachable")  # pragma: no cover

        return wrapper

    return decorator


def rate_limited(
    max_calls: int,
    window: float,
    clock: Callable[[], float] = time.monotonic,
) -> Decorator:
    """Allow ``max_calls`` per sliding ``window`` seconds; then raise.

    Raises :class:`RateLimitExceededError` instead of blocking -- the caller
    decides whether to queue, drop, or surface the pressure.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        calls: list[float] = []

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            now = clock()
            while calls and now - calls[0] >= window:
                calls.pop(0)
            if len(calls) >= max_calls:
                raise RateLimitExceededError(
                    f"{func.__name__}: {max_calls} calls per {window}s exceeded"
                )
            calls.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator
