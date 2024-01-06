from datetime import datetime
from typing import Optional

from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QLabel, QFrame

from tick.data.time_tracker import TimeTracker
from tick.data.timestamp import Timestamp
from tick.ui.components.buttons.hover_button import HoverButton
from tick.ui.components.editors.time_edit import TimeEdit, TimeEditMode
from tick.ui.themes.layout_factory import LayoutFactory


class TimeTrackerControls(QFrame):
    start_tracker_requested = pyqtSignal()
    update_tracker_requested = pyqtSignal(TimeTracker)
    stop_tracker_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.__time_tracker: Optional[TimeTracker] = None
        self.__timer = QTimer()

        self.__stack_layout = LayoutFactory.stacked()
        self.__start_button = QPushButton("Start")
        self.__start_edit = TimeEdit(TimeEditMode.HM)
        self.__stop_button = HoverButton("", "Stop")
        self.__setup_layout()

    def create_time_tracker(self, time_tracker: TimeTracker) -> None:
        self.__time_tracker = time_tracker
        self.__start_edit.update_timestamp(Timestamp.from_datetime(self.__time_tracker.start_time))
        self.__on_time_update()
        self.__timer.start(1000)
        self.__stack_layout.setCurrentIndex(1)

    def update_time_tracker(self, time_tracker: TimeTracker) -> None:
        self.__time_tracker = time_tracker
        self.__start_edit.update_timestamp(Timestamp.from_datetime(self.__time_tracker.start_time))
        self.__on_time_update()

    def delete_time_tracker(self) -> None:
        self.__timer.stop()
        self.__time_tracker = None
        self.__stack_layout.setCurrentIndex(0)

    def __on_time_update(self) -> None:
        if self.__time_tracker is None:
            return

        timestamp = Timestamp.from_timedelta(datetime.now().astimezone() - self.__time_tracker.start_time)
        self.__stop_button.set_text(timestamp.format("{h}:{m:02}:{s:02}"))

    def __on_tracker_time_changed(self, timestamp: Timestamp) -> None:
        start_time = timestamp.replace_hm(self.__time_tracker.start_time)
        self.update_tracker_requested.emit(TimeTracker(self.__time_tracker.tracker_id, start_time))

    def __on_stop_button_clicked(self) -> None:
        self.stop_tracker_requested.emit(self.__time_tracker.tracker_id)

    def __setup_layout(self) -> None:
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.__start_button.setObjectName("start-button")
        self.__start_button.setFixedWidth(90)

        start_layout = LayoutFactory.horizontal()
        start_layout.addWidget(QLabel(u"Time to change the  🌍"))
        start_layout.addStretch()
        start_layout.addWidget(self.__start_button)

        start_widget = QWidget()
        start_widget.setLayout(start_layout)

        self.__start_edit.setFixedWidth(55)
        self.__start_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.__stop_button.setObjectName("stop-button")
        self.__stop_button.setFixedWidth(90)

        stop_layout = LayoutFactory.horizontal(gap=4)
        stop_layout.addWidget(QLabel(u"🌍  changing since"))
        stop_layout.addWidget(self.__start_edit)
        stop_layout.addStretch()
        stop_layout.addWidget(self.__stop_button)

        stop_widget = QWidget()
        stop_widget.setLayout(stop_layout)

        self.__stack_layout.addWidget(start_widget)
        self.__stack_layout.addWidget(stop_widget)
        self.setLayout(self.__stack_layout)

        self.__start_button.clicked.connect(self.start_tracker_requested.emit)
        self.__start_edit.timestamp_changed.connect(self.__on_tracker_time_changed)
        self.__stop_button.clicked.connect(self.__on_stop_button_clicked)
        self.__timer.timeout.connect(self.__on_time_update)
