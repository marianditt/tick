import logging
from typing import TypeVar, Iterable

from PyQt5.QtWidgets import QWidget

from tick.ui.components.lists.abstract_list import AbstractList
from tick.ui.themes.layout_factory import LayoutFactory

T = TypeVar("T", bound=QWidget)


class WidgetList(QWidget, AbstractList[T]):
    def __init__(self):
        super().__init__()
        self.__content_layout = LayoutFactory.vertical(gap=4)
        self.setLayout(self.__content_layout)

    def insert_widget(self, index: int, widget: T) -> None:
        if 0 <= index <= self.__content_layout.count():
            self.__content_layout.insertWidget(index, widget)
        else:
            logging.error(f"Failed to insert widget at index {index}. Index out of bounds.")

    def get_widgets(self) -> Iterable[T]:
        for index in range(self.__content_layout.count()):
            try:
                yield self.__content_layout.itemAt(index).widget()
            except AttributeError:
                logging.error(f"Failed to get widget at index {index}. Iteration aborted!")
                return

    def delete_widget(self, index: int) -> None:
        if 0 <= index < self.__content_layout.count():
            try:
                self.__content_layout.takeAt(index).widget().deleteLater()
            except AttributeError:
                logging.error(f"Failed to delete widget at index {index}.")
        else:
            logging.error(f"Failed to delete widget at index {index}. Index out of bounds.")
