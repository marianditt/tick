from typing import Dict, TypeVar, Generic, Callable, Any

from PyQt5.QtWidgets import QWidget

from tick.ui.components.lists.abstract_list import AbstractList
from tick.utils.find_first_index import find_first_index

L = TypeVar("L", bound=AbstractList)
T = TypeVar("T", bound=QWidget)


class OrderedList(Generic[L, T]):
    def __init__(self, widget_list: L, id_key: Callable[[T], str], order_key: Callable[[T], Any]):
        super().__init__()
        self.__id_key = id_key
        self.__order_key = order_key

        self.__widget_map: Dict[str, T] = {}
        self.__widget_list = widget_list

    def get_list_view(self) -> L:
        return self.__widget_list

    def insert_widget(self, widget: T) -> None:
        widget_id = self.__id_key(widget)
        widget_key = self.__order_key(widget)
        if widget_id not in self.__widget_map:
            self.__widget_map[widget_id] = widget
            index = find_first_index(
                self.__widget_list.get_widgets(),
                condition=lambda x: widget_key > self.__order_key(x)
            )
            self.__widget_list.insert_widget(index, widget)
        else:
            raise ValueError(f"Failed to insert widget. Widget with id {widget_id} already exists.")

    def get_widget(self, widget_id: str) -> T:
        try:
            return self.__widget_map[widget_id]
        except KeyError:
            raise ValueError(f"Failed to get widget. Widget with id {widget_id} does not exist.")

    def delete_widget(self, widget_id: str) -> None:
        if widget_id in self.__widget_map:
            del self.__widget_map[widget_id]
            index = find_first_index(
                self.__widget_list.get_widgets(),
                condition=lambda x: widget_id == self.__id_key(x)
            )
            self.__widget_list.delete_widget(index)
        else:
            raise ValueError(f"Failed to delete widget. Widget with id {widget_id} does not exist.")
