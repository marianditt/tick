from dataclasses import dataclass
from datetime import datetime, timedelta, date


@dataclass(frozen=True)
class TimeEntry(object):
    entry_id: str
    start_time: datetime
    end_time: datetime

    @property
    def start_date(self) -> date:
        return self.start_time.date()

    @property
    def end_date(self) -> date:
        return self.end_time.date()

    @property
    def duration(self) -> timedelta:
        return self.end_time - self.start_time
