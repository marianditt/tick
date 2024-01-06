from PyQt5.QtWidgets import QLabel


class Header(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
