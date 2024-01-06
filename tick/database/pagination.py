import base64
import binascii
import logging
from dataclasses import dataclass, field as dataclass_field
from typing import TypeVar, Generic, Optional, Callable, Any, Tuple, List

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    values: List[T] = dataclass_field(default_factory=list)
    cursor: Optional[bytes] = None
    has_more: bool = False


def create_cursor(field: str, parameter: Any, converter: Optional[Callable[[Any], str]] = None) -> bytes:
    converter = converter or (lambda x: x)
    return base64.urlsafe_b64encode(f"{field}:{converter(parameter)}".encode())


def parse_cursor(cursor: bytes, converter: Optional[Callable[[str], Any]] = None) -> Tuple[str, Optional[Any]]:
    try:
        converter = converter or (lambda x: x)
        cursor_value = base64.urlsafe_b64decode(cursor).decode()
        field, parameter = cursor_value.split(":", maxsplit=1)
        return field, converter(parameter)
    except binascii.Error | ValueError:
        logging.exception(f"Failed to parse cursor: {cursor}")
        return "", None
