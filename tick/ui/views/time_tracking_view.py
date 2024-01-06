from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from tick.data.time_entry import TimeEntry
from tick.data.time_tracker import TimeTracker
from tick.data.timestamp import Timestamp
from tick.data.work_day import WorkDay
from tick.ui.themes.layout_factory import LayoutFactory
from tick.ui.views.time_entries.time_entry_view import TimeEntryView
from tick.ui.views.time_trackers.time_tracker_controls import TimeTrackerControls
from tick.ui.views.work_days.work_day_list_view import WorkDayListView
from tick.ui.views.work_days.work_day_view import WorkDayView


class TimeTrackingView(QWidget):
    start_tracker_requested = pyqtSignal()
    update_tracker_requested = pyqtSignal(TimeTracker)
    stop_tracker_requested = pyqtSignal(str)

    end_of_work_day_list_reached = pyqtSignal()

    update_time_entry_requested = pyqtSignal(TimeEntry)
    delete_time_entry_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__working_time = Timestamp.from_hms(hours=8)

        self.__time_tracker_controls = TimeTrackerControls()
        self.__work_day_list_view = WorkDayListView()
        self.__setup_view()

    def update_project(self, project) -> None:
        self.__working_time = Timestamp(project.working_time)
        for work_day_view in self.__work_day_list_view.get_work_day_views():
            work_day_view.update_working_time(self.__working_time)

    def create_time_tracker(self, time_tracker: TimeTracker) -> None:
        self.__time_tracker_controls.create_time_tracker(time_tracker)

    def update_time_tracker(self, time_tracker: TimeTracker) -> None:
        self.__time_tracker_controls.update_time_tracker(time_tracker)

    def delete_time_tracker(self) -> None:
        self.__time_tracker_controls.delete_time_tracker()

    def insert_work_day(self, work_day: WorkDay) -> None:
        work_day_view = WorkDayView(work_day)
        work_day_view.update_working_time(self.__working_time)
        self.__work_day_list_view.insert_work_day_view(work_day_view)

    def update_work_day(self, work_day: WorkDay) -> None:
        work_day_view = self.__work_day_list_view.get_work_day_view(work_day.work_day_id)
        if work_day_view is not None:
            work_day_view.update_work_day(work_day)

    def delete_work_day(self, work_day_id: str) -> None:
        self.__work_day_list_view.delete_work_day(work_day_id)

    def insert_time_entry(self, work_day_id: str, time_entry: TimeEntry) -> None:
        work_day_view = self.__work_day_list_view.get_work_day_view(work_day_id)
        if work_day_view is not None:
            time_entry_view = TimeEntryView(time_entry)
            time_entry_view.update_time_entry_requested.connect(self.update_time_entry_requested.emit)
            time_entry_view.delete_time_entry_requested.connect(self.delete_time_entry_requested.emit)
            work_day_view.insert_time_entry_view(time_entry_view)

    def update_time_entry(self, work_day_id: str, time_entry: TimeEntry) -> None:
        work_day_view = self.__work_day_list_view.get_work_day_view(work_day_id)
        time_entry_view = None if work_day_view is None else work_day_view.get_time_entry_view(time_entry.entry_id)
        if time_entry_view is not None:
            time_entry_view.update_time_entry(time_entry)

    def delete_time_entry(self, work_day_id: str, entry_id: str) -> None:
        work_day_view = self.__work_day_list_view.get_work_day_view(work_day_id)
        if work_day_view is not None:
            work_day_view.delete_time_entry(entry_id)

    def __setup_view(self) -> None:
        layout = LayoutFactory.vertical()
        layout.addWidget(self.__time_tracker_controls)
        layout.addWidget(self.__work_day_list_view)
        self.setLayout(layout)

        self.__time_tracker_controls.start_tracker_requested.connect(self.start_tracker_requested.emit)
        self.__time_tracker_controls.update_tracker_requested.connect(self.update_tracker_requested.emit)
        self.__time_tracker_controls.stop_tracker_requested.connect(self.stop_tracker_requested.emit)
        self.__work_day_list_view.end_of_work_day_list_reached.connect(self.end_of_work_day_list_reached.emit)
