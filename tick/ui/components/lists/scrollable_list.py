from typing import Iterable, TypeVar

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QFrame, QWidget

from tick.ui.components.lists.abstract_list import AbstractList
from tick.ui.components.lists.widget_list import WidgetList
from tick.ui.themes.layout_factory import LayoutFactory

T = TypeVar("T", bound=QWidget)


class ScrollableList(QScrollArea, AbstractList[T]):
    end_of_list_reached = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__widget_list = WidgetList[T]()
        self.__setup_view()

    def insert_widget(self, index: int, widget: T) -> None:
        self.__widget_list.insert_widget(index, widget)

    def get_widgets(self) -> Iterable[T]:
        return self.__widget_list.get_widgets()

    def delete_widget(self, index: int) -> None:
        self.__widget_list.delete_widget(index)

    def __setup_view(self) -> None:
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        layout = LayoutFactory.vertical()
        layout.addWidget(self.__widget_list)
        layout.addStretch()

        content = ScrollableContent()
        content.setLayout(layout)

        self.setWidget(content)

        self.verticalScrollBar().valueChanged.connect(self.__on_scroll_value_changed)

    def __on_scroll_value_changed(self, value: int) -> None:
        if value == self.verticalScrollBar().maximum():
            self.end_of_list_reached.emit()


class ScrollableContent(QFrame):
    pass
