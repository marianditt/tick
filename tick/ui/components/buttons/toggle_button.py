from typing import List, TypeVar, Generic, Tuple

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

T = TypeVar("T")


class ToggleButton(QPushButton, Generic[T]):
    mode_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__index = 0
        self.__modes: List[Tuple[str, T]] = []
        self.__setup_view()

    def add_mode(self, mode: T, text: str) -> None:
        self.__modes.append((text, mode))
        self.set_index(self.__index)

    def get_mode(self) -> T:
        return self.__modes[self.__index][1]

    def select_mode(self, mode: T) -> None:
        for index, (_, m) in enumerate(self.__modes):
            if m == mode:
                self.__select_index(index)
                return

    def set_index(self, index: int) -> None:
        self.__select_index(index)
        self.mode_changed.emit()

    def __setup_view(self) -> None:
        self.setIcon(QIcon.fromTheme("arrow_drop_down"))
        self.clicked.connect(self.__switch_mode)

    def __select_index(self, index: int) -> None:
        self.__index = index
        self.setText(self.__modes[self.__index][0])

    def __switch_mode(self) -> None:
        self.set_index((self.__index + 1) % len(self.__modes))
