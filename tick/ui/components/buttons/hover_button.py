from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QPushButton


class HoverButton(QPushButton):
    def __init__(self, text: str, hover_text: str):
        super().__init__()
        self.__text = text
        self.__hover_text = hover_text
        self.__hovering = False
        self.__on_update()

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.__hovering = True
        self.__on_update()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.__hovering = False
        self.__on_update()

    def setText(self, text: str) -> None:
        self.set_text(text)

    def set_text(self, text: str) -> None:
        self.__text = text
        self.__on_update()

    def set_hover_text(self, hover_text: str) -> None:
        self.__hover_text = hover_text
        self.__on_update()

    def __on_update(self) -> None:
        if self.__hovering:
            super().setText(self.__hover_text)
        else:
            super().setText(self.__text)
