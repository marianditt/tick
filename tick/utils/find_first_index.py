from collections.abc import Iterable
from typing import TypeVar, Callable

T = TypeVar('T')


def find_first_index(values: Iterable[T], condition: Callable[[T], bool]) -> int:
    index = 0
    for value in values:
        if condition(value):
            return index
        else:
            index += 1
    return index
