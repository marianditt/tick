from datetime import datetime
from typing import Optional

from PyQt5.QtCore import QTimer, QEvent, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPaintEvent, QPainter, QPen
from PyQt5.QtWidgets import QPushButton


class LongPressButton(QPushButton):
    long_pressed = pyqtSignal()

    def __init__(self, min_press_seconds: int):
        super().__init__()
        self.__min_press_seconds = min_press_seconds
        self.__press_start_time: Optional[datetime] = None

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.update)

        self.setFixedSize(QSize(32, 32))

    def mousePressEvent(self, event: QEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.__press_start_time = datetime.now()
            self.__timer.start(10)
        else:
            self.__press_start_time = None
            self.__timer.stop()

    def mouseReleaseEvent(self, event: QEvent):
        super().mouseReleaseEvent(event)
        self.__timer.stop()

        if self.progress == 100:
            self.long_pressed.emit()
        self.__press_start_time = None
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        pen_size = 4

        pen = QPen(self.palette().highlight().color())
        pen.setWidth(pen_size)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(pen)

        # Draw arc for progress
        rect = self.rect()
        rect.adjust(pen_size, pen_size, -pen_size, -pen_size)

        start_angle = 90 * 16  # Starting point is at 12 o'clock
        span_angle = int(-16 * 3.6 * self.progress)  # -360 degrees for complete circle
        painter.drawArc(rect, start_angle, span_angle)

    @property
    def progress(self) -> int:
        end_time = datetime.now()
        start_time = self.__press_start_time or end_time
        press_seconds = (end_time - start_time).total_seconds()
        progress = press_seconds / self.__min_press_seconds
        return min(int(100.0 * progress), 100)
