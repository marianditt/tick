from datetime import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QSizePolicy, QLabel

from tick.data.time_entry import TimeEntry
from tick.data.timestamp import Timestamp
from tick.ui.components.buttons.long_press_button import LongPressButton
from tick.ui.components.editors.time_edit import TimeEdit, TimeEditMode
from tick.ui.components.labels.badge import Badge
from tick.ui.themes.layout_factory import LayoutFactory


class TimeEntryView(QFrame):
    update_time_entry_requested = pyqtSignal(TimeEntry)
    delete_time_entry_requested = pyqtSignal(str)

    def __init__(self, time_entry: TimeEntry):
        super().__init__()
        self.__time_entry = time_entry

        self.__start_time_edit = TimeEdit(TimeEditMode.HM)
        self.__end_time_edit = TimeEdit(TimeEditMode.HM)
        self.__badge = Badge()
        self.__duration_edit = TimeEdit(TimeEditMode.HMS)
        self.__delete_button = LongPressButton(1)

        self.__setup_view()
        self.update_time_entry(time_entry)

    def get_time_entry(self) -> TimeEntry:
        return self.__time_entry

    def update_time_entry(self, time_entry: TimeEntry) -> None:
        self.__time_entry = time_entry
        self.__start_time_edit.update_timestamp(Timestamp.from_datetime(time_entry.start_time))
        self.__end_time_edit.update_timestamp(Timestamp.from_datetime(time_entry.end_time))
        self.__duration_edit.update_timestamp(Timestamp.from_timedelta(time_entry.duration))

        date_difference = time_entry.end_time.date() - time_entry.start_time.date()
        self.__badge.setVisible(date_difference.days > 0)
        self.__badge.setText(f"{date_difference.days:+}d")

    def __setup_view(self) -> None:
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.__start_time_edit.setFixedWidth(55)
        self.__start_time_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.__end_time_edit.setFixedWidth(55)
        self.__end_time_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.__duration_edit.set_icon("timer")
        self.__duration_edit.setFixedWidth(100)
        self.__duration_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.__delete_button.setIcon(QIcon.fromTheme("delete"))

        layout = LayoutFactory.horizontal()
        layout.addWidget(self.__start_time_edit)
        layout.addWidget(QLabel("-"))
        layout.addWidget(self.__end_time_edit)
        layout.addWidget(self.__badge)
        layout.addStretch()
        layout.addWidget(self.__duration_edit)
        layout.addWidget(self.__delete_button)
        self.setLayout(layout)

        self.__start_time_edit.timestamp_changed.connect(self.__on_start_time_changed)
        self.__end_time_edit.timestamp_changed.connect(self.__on_end_time_changed)
        self.__duration_edit.timestamp_changed.connect(self.__on_duration_changed)
        self.__delete_button.long_pressed.connect(self.__on_delete_clicked)

    def __on_start_time_changed(self, timestamp: Timestamp) -> None:
        new_start_time = timestamp.replace_hms(self.__time_entry.start_time)
        self.__on_time_entry_changed(new_start_time, self.__time_entry.end_time)

    def __on_end_time_changed(self, timestamp: Timestamp) -> None:
        new_end_time = timestamp.replace_hms(self.__time_entry.end_time)
        self.__on_time_entry_changed(self.__time_entry.start_time, new_end_time)

    def __on_duration_changed(self, timestamp: Timestamp) -> None:
        new_end_time = self.__time_entry.start_time + timestamp.to_timedelta()
        self.__on_time_entry_changed(self.__time_entry.start_time, new_end_time)

    def __on_time_entry_changed(self, start_time: datetime, end_time: datetime) -> None:
        new_time_entry = TimeEntry(self.__time_entry.entry_id, start_time, end_time)
        self.update_time_entry_requested.emit(new_time_entry)

    def __on_delete_clicked(self) -> None:
        self.delete_time_entry_requested.emit(self.__time_entry.entry_id)
