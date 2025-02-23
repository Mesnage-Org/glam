from collections.abc import Iterator
from typing import Pattern

def isoforms(
    sequence: str,
    variable_mods: dict[str, list[str]] = {},
    max_mods: int | None = None,
    **kwargs,
) -> Iterator[str]: ...
def cleave(
    sequence: str,
    rule: str | Pattern[str],
    missed_cleavages: int,
    min_length: int | None,
    max_length: int | None,
    semi: bool,
    exception: str | Pattern[str] | None,
    regex: bool,
) -> set[str]: ...
