from typing import Generic, TypeVar, Iterable

T = TypeVar("T")


class AbstractList(Generic[T]):
    def insert_widget(self, index: int, widget: T) -> None:
        raise NotImplementedError()

    def get_widgets(self) -> Iterable[T]:
        raise NotImplementedError()

    def delete_widget(self, index: int) -> None:
        raise NotImplementedError()
