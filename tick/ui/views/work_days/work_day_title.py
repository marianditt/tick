import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame

from tick.data.time_mode import TimeMode
from tick.data.timestamp import Timestamp
from tick.data.work_day import WorkDay
from tick.ui.components.labels.date_label import DateLabel
from tick.ui.themes.layout_factory import LayoutFactory


class WorkDayTitle(QFrame):
    def __init__(self, work_day: WorkDay):
        super().__init__()

        # Data
        self.__work_day = work_day
        self.__working_time = Timestamp()
        self.__time_mode = TimeMode.CLOCK

        # View
        self.__date_label = DateLabel(self.__work_day.date)
        self.__total_time_label = QLabel()
        self.__overtime_label = QLabel()

        self.__setup_view()
        self.__update_view()

    def update_work_day(self, work_day: WorkDay):
        self.__work_day = work_day
        self.__update_view()

    def update_working_time(self, working_time: Timestamp):
        self.__working_time = working_time
        self.__update_view()

    def update_time_mode(self, time_mode: TimeMode):
        self.__time_mode = time_mode
        self.__update_view()

    def __setup_view(self):
        self.setObjectName("work-day-title")

        self.__date_label.setObjectName("work-day-title-label")

        total_label = QLabel("Total (Overtime)")
        total_label.setObjectName("work-day-title-label")

        self.__total_time_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.__overtime_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout = LayoutFactory.horizontal(gap=4)
        layout.addWidget(self.__date_label)
        layout.addStretch()
        layout.addWidget(total_label)
        layout.addWidget(self.__total_time_label)
        layout.addWidget(self.__overtime_label)
        self.setLayout(layout)

    def __update_view(self):
        self.__date_label.set_date(self.__work_day.date)

        total_time = Timestamp.from_timedelta(self.__work_day.total_time)
        overtime = total_time - self.__working_time
        if self.__time_mode == TimeMode.CLOCK:
            self.__total_time_label.setText(total_time.format("{h}:{m:02}"))
            self.__overtime_label.setText(overtime.format("({sign}{h}:{m:02})"))
        elif self.__time_mode == TimeMode.DECIMAL:
            self.__total_time_label.setText(total_time.format("{d:.2f}"))
            self.__overtime_label.setText(overtime.format("({d:+.2f})"))
        else:
            logging.error(f"Failed to update work day title. Unknown time mode: {self.__time_mode}")
