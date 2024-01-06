from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class WorkDay(object):
    work_day_id: str
    date: date
    total_time: timedelta
