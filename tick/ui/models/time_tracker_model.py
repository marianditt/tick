import logging
from datetime import datetime
from uuid import uuid4

from PyQt5.QtCore import QObject, pyqtSignal

from tick.data.time_entry import TimeEntry
from tick.data.time_tracker import TimeTracker
from tick.repositories.time_tracker_repository import TimeTrackerRepository


class TimeTrackerModel(QObject):
    started = pyqtSignal(TimeTracker)
    tracker_updated = pyqtSignal(TimeTracker)
    stopped = pyqtSignal()
    create_time_entry_requested = pyqtSignal(TimeEntry)

    def __init__(self, repository: TimeTrackerRepository):
        super().__init__()
        self.__repository = repository

    def load(self) -> None:
        trackers = self.__repository.find_running_trackers()
        if len(trackers) > 1:
            logging.error("Found more than one running tracker. All of them will be stopped.")
            for tracker in trackers:
                self.stop(tracker.tracker_id)
        elif len(trackers) == 1:
            self.started.emit(trackers[0])

    def start(self) -> None:
        tracker = TimeTracker(str(uuid4()), datetime.now().astimezone())
        self.__repository.start_tracker(tracker)
        self.started.emit(tracker)

    def update_tracker(self, tracker: TimeTracker) -> None:
        self.__repository.update_tracker(tracker)
        self.tracker_updated.emit(tracker)

    def stop(self, tracker_id: str) -> None:
        tracker = self.__repository.find_one_tracker(tracker_id)
        if tracker is None:
            return

        self.__repository.stop_tracker(tracker_id)
        self.stopped.emit()

        time_entry = TimeEntry(str(uuid4()), tracker.start_time, datetime.now().astimezone())
        self.create_time_entry_requested.emit(time_entry)
