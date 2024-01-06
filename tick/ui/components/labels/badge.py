from PyQt5.QtWidgets import QLabel, QSizePolicy


class Badge(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(24)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
