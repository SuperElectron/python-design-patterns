"""``sorted(key=...)``: the Strategy pattern as an argument.

The key function is an interchangeable ordering algorithm; swapping
strategies is passing a different callable.
"""

from __future__ import annotations


def by_length(words: list[str]) -> list[str]:
    return sorted(words, key=len)


def by_last_letter(words: list[str]) -> list[str]:
    return sorted(words, key=lambda w: w[-1])


def case_insensitive(words: list[str]) -> list[str]:
    return sorted(words, key=str.casefold)


def main() -> None:
    words = ["banana", "Fig", "cherry"]
    print(f"by length:        {by_length(words)}")
    print(f"by last letter:   {by_last_letter(words)}")
    print(f"case-insensitive: {case_insensitive(words)}")


if __name__ == "__main__":
    main()
