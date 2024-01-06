import math
from datetime import timedelta, datetime


class Timestamp(object):
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
    SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR

    @staticmethod
    def from_datetime(dt: datetime) -> 'Timestamp':
        total_seconds = dt.hour * Timestamp.SECONDS_PER_HOUR + dt.minute * Timestamp.SECONDS_PER_MINUTE + dt.second
        return Timestamp(total_seconds)

    @staticmethod
    def from_timedelta(td: timedelta) -> 'Timestamp':
        total_seconds = td.days * Timestamp.SECONDS_PER_DAY + td.seconds
        return Timestamp(total_seconds)

    @staticmethod
    def from_hms(hours: int = 0, minutes: int = 0, seconds: int = 0) -> 'Timestamp':
        total_seconds = hours * Timestamp.SECONDS_PER_HOUR + minutes * Timestamp.SECONDS_PER_MINUTE + seconds
        return Timestamp(total_seconds)

    def __init__(self, seconds: int = 0):
        self.__seconds = seconds

    def __add__(self, other: 'Timestamp') -> 'Timestamp':
        return Timestamp(self.__seconds + other.__seconds)

    def __sub__(self, other: 'Timestamp') -> 'Timestamp':
        return Timestamp(self.__seconds - other.__seconds)

    @property
    def sign(self) -> str:
        return "-" if math.copysign(1.0, self.__seconds) < 0 else "+"

    @property
    def days(self) -> int:
        return abs(self.__seconds) // self.SECONDS_PER_DAY

    @property
    def hours_in_day(self) -> int:
        return (abs(self.__seconds) % self.SECONDS_PER_DAY) // self.SECONDS_PER_HOUR

    @property
    def total_hours(self) -> int:
        return abs(self.__seconds) // self.SECONDS_PER_HOUR

    @property
    def minutes(self) -> int:
        return (abs(self.__seconds) % self.SECONDS_PER_HOUR) // self.SECONDS_PER_MINUTE

    @property
    def seconds_in_minute(self) -> int:
        return abs(self.__seconds) % self.SECONDS_PER_MINUTE

    @property
    def total_seconds(self) -> int:
        return self.__seconds

    def replace_hm(self, base: datetime) -> datetime:
        return base.replace(hour=self.hours_in_day, minute=self.minutes) + timedelta(days=self.days)

    def replace_hms(self, base: datetime) -> datetime:
        return (base.replace(hour=self.hours_in_day, minute=self.minutes, second=self.seconds_in_minute) +
                timedelta(days=self.days))

    def to_timedelta(self) -> timedelta:
        return timedelta(days=self.days, hours=self.hours_in_day, minutes=self.minutes, seconds=self.seconds_in_minute)

    def format(self, fmt: str) -> str:
        hours_dec = self.__seconds / self.SECONDS_PER_HOUR
        return fmt.format(sign=self.sign, h=self.total_hours, m=self.minutes, s=self.seconds_in_minute, d=hours_dec)
