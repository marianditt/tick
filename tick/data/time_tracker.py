from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimeTracker(object):
    tracker_id: str
    start_time: datetime
