from datetime import date, timedelta
from typing import Optional, Dict
from uuid import uuid5, UUID

from PyQt5.QtCore import QObject, pyqtSignal

from tick.data.time_entry import TimeEntry
from tick.data.work_day import WorkDay
from tick.repositories.time_entry_repository import TimeEntryRepository


class TimeEntryModel(QObject):
    WORK_DAY_ID_NAMESPACE = UUID("b338e886-61f5-4609-b907-a50f53a0cabe")
    PAGE_LIMIT = 30

    work_day_inserted = pyqtSignal(WorkDay)
    work_day_updated = pyqtSignal(WorkDay)
    work_day_deleted = pyqtSignal(str)

    time_entry_inserted = pyqtSignal(str, TimeEntry)
    time_entry_updated = pyqtSignal(str, TimeEntry)
    time_entry_deleted = pyqtSignal(str, str)

    def __init__(self, repository: TimeEntryRepository):
        super().__init__()
        self.__repository = repository

        self.__work_days: Dict[str, Dict[str, TimeEntry]] = {}
        self.__cursor: Optional[bytes] = None
        self.__has_more = True

    def load_more(self) -> None:
        if not self.__has_more:
            return

        page = self.__repository.find_entry_page(self.PAGE_LIMIT, self.__cursor)
        self.__cursor = page.cursor
        self.__has_more = page.has_more

        for time_entry in page.values:
            self.cache_time_entry(time_entry)

    def insert_time_entry(self, time_entry: TimeEntry) -> None:
        time_entry = self.__validate_time_entry(time_entry)
        self.__repository.create_entry(time_entry)
        self.cache_time_entry(time_entry)

    def cache_time_entry(self, time_entry: TimeEntry) -> None:
        work_day_id = self.__create_work_day_id(time_entry.start_time.date())
        if work_day_id in self.__work_days:
            self.__work_days[work_day_id][time_entry.entry_id] = time_entry
            self.update_work_day(work_day_id)
        else:
            self.__work_days[work_day_id] = {time_entry.entry_id: time_entry}
            self.work_day_inserted.emit(WorkDay(work_day_id, time_entry.start_time.date(), time_entry.duration))
        self.time_entry_inserted.emit(work_day_id, time_entry)

    def update_time_entry(self, time_entry: TimeEntry) -> None:
        # Correct time entry if necessary
        time_entry = self.__validate_time_entry(time_entry)

        # Update time entry
        previous_time_entry = self.__repository.find_one_entry(time_entry.entry_id)
        self.__repository.update_entry(time_entry)

        # Emit signals
        work_day_id = self.__create_work_day_id(time_entry.start_time.date())
        time_entry_id = time_entry.entry_id
        if previous_time_entry.start_time != time_entry.start_time:
            self.time_entry_deleted.emit(work_day_id, time_entry_id)
            self.time_entry_inserted.emit(work_day_id, time_entry)
        else:
            self.time_entry_updated.emit(work_day_id, time_entry)
        self.update_work_day(work_day_id)

    def delete_time_entry(self, entry_id: str) -> None:
        # Delete time entry
        time_entry = self.__repository.find_one_entry(entry_id)
        self.__repository.delete_entry(entry_id)

        # Emit signals
        work_day_id = self.__create_work_day_id(time_entry.start_time.date())
        work_day_entries = self.__work_days[work_day_id]
        if len(work_day_entries) == 1:
            del self.__work_days[work_day_id]
            self.work_day_deleted.emit(work_day_id)
        else:
            del work_day_entries[entry_id]
            self.time_entry_deleted.emit(work_day_id, entry_id)
            self.update_work_day(work_day_id)

    def update_work_day(self, work_day_id: str) -> None:
        time_entries = list(self.__work_days[work_day_id].values())
        work_day_date = time_entries[0].start_time.date()
        total_time = sum((time_entry.duration for time_entry in time_entries), start=timedelta())
        work_day = WorkDay(work_day_id, work_day_date, total_time)
        self.work_day_updated.emit(work_day)

    @staticmethod
    def __validate_time_entry(time_entry: TimeEntry) -> TimeEntry:
        if time_entry.start_time > time_entry.end_time:
            time_entry = TimeEntry(time_entry.entry_id, time_entry.start_time, time_entry.start_time)
        return time_entry

    @staticmethod
    def __create_work_day_id(work_day_date: date) -> str:
        return str(uuid5(TimeEntryModel.WORK_DAY_ID_NAMESPACE, work_day_date.isoformat()))
