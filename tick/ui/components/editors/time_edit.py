from enum import Enum

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QIcon, QFocusEvent
from PyQt5.QtWidgets import QLineEdit

from tick.data.timestamp import Timestamp


class TimeEditMode(Enum):
    HMS = 'SECONDS'
    HM = 'MINUTES'


class TimeEdit(QLineEdit):
    HMS_FORMAT = "{h:02}:{m:02}:{s:02}"
    HM_FORMAT = "{h:02}:{m:02}"

    timestamp_changed = pyqtSignal(Timestamp)

    def __init__(self, mode: TimeEditMode):
        super().__init__()
        self.__format = self.HMS_FORMAT if mode == TimeEditMode.HMS else self.HM_FORMAT
        self.__timestamp = Timestamp()
        self.__section_index = 0
        self.__digit_index = 0
        self.__setup_view()

    def update_timestamp(self, timestamp: Timestamp) -> None:
        self.__timestamp = timestamp
        self.setText(self.__timestamp.format(self.__format))

    def set_icon(self, name: str) -> None:
        for action in self.actions():
            self.removeAction(action)
        self.addAction(QIcon.fromTheme(name), TimeEdit.LeadingPosition)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        self.__from_cursor()
        self.__update_selection()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton:
            self.__from_cursor()
            self.__update_selection()

    def focusOutEvent(self, event: QFocusEvent) -> None:
        super().focusOutEvent(event)
        if self.text() != self.__timestamp.format(self.__format):
            self.__on_save()

    def keyPressEvent(self, event: QKeyEvent):
        event.accept()
        if event.key() == Qt.Key_Escape:
            self.update_timestamp(self.__timestamp)
            self.clearFocus()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.clearFocus()
        elif event.key() == Qt.Key_Home:
            self.__move_to(0, 0)
        elif event.key() == Qt.Key_End:
            self.__move_to(self.__num_sections() - 1, 1)
        elif event.key() == Qt.Key_Left:
            self.__move_left()
        elif event.key() == Qt.Key_Right:
            self.__move_right()
        elif event.key() in (Qt.Key_Up, Qt.Key_PageUp):
            self.__move_up()
        elif event.key() in (Qt.Key_Down, Qt.Key_PageDown):
            self.__move_down()
        elif event.key() == Qt.Key_Backspace:
            self.__edit_text(0)
            self.__move_left()
        elif event.key() == Qt.Key_Delete:
            self.__edit_text(0)
        elif Qt.Key_0 <= event.key() <= Qt.Key_9:
            self.__edit_text(event.key() - Qt.Key_0)
            self.__move_right()

    def __move_to(self, section_index: int, digit_index: int) -> None:
        self.__section_index = section_index
        self.__digit_index = digit_index
        self.__update_selection()

    def __from_cursor(self) -> None:
        cursor = self.cursorPosition()
        self.__move_to(cursor // 3, min(cursor % 3, 1))

    def __move_left(self) -> None:
        if self.__digit_index == 0 and self.__section_index > 0:
            self.__move_to(self.__section_index - 1, 1)
        else:
            self.__move_to(self.__section_index, 0)

    def __move_right(self) -> None:
        if self.__digit_index == 1 and self.__section_index < self.__num_sections() - 1:
            self.__move_to(self.__section_index + 1, 0)
        else:
            self.__move_to(self.__section_index, 1)

    def __move_up(self) -> None:
        if self.__digit_index == 1:
            self.__move_to(self.__section_index, 0)
        elif self.__section_index > 0:
            self.__move_to(self.__section_index - 1, 0)

    def __move_down(self) -> None:
        if self.__section_index < self.__num_sections() - 1:
            self.__move_to(self.__section_index + 1, 0)

    def __num_sections(self) -> int:
        return 2 if self.__format == self.HM_FORMAT else 3

    def __update_selection(self) -> None:
        text_index = self.__section_index * 3 + self.__digit_index
        self.setSelection(text_index, 1)

    def __edit_text(self, value: int) -> None:
        edit_index = self.__section_index * 3 + self.__digit_index
        array = list(self.text())
        array[edit_index] = str(value)
        self.setText("".join(array))

    def __on_save(self) -> None:
        if self.text() != self.__timestamp.format(self.__format):
            hms = self.text().split(":")
            if len(hms) == 2:
                self.timestamp_changed.emit(Timestamp.from_hms(int(hms[0]), int(hms[1]), self.__timestamp.seconds_in_minute))
            else:
                self.timestamp_changed.emit(Timestamp.from_hms(int(hms[0]), int(hms[1]), int(hms[2])))

    def __setup_view(self) -> None:
        self.setAlignment(Qt.AlignCenter)
