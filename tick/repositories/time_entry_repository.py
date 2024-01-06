import logging
from datetime import datetime
from typing import Optional, List, Tuple

from tick.data.time_entry import TimeEntry
from tick.database.database_client import DatabaseClient, DatabaseError
from tick.database.pagination import parse_cursor, Page, create_cursor


def convert_row_to_entity(row: Tuple) -> TimeEntry:
    return TimeEntry(entry_id=row[0], start_time=row[1], end_time=row[2])


def create_page(entries: List[TimeEntry], limit: int) -> Page[TimeEntry]:
    has_more = len(entries) == limit + 1
    cursor = None if not has_more else create_cursor("start_time", entries[-1].start_time, convert_datetime_to_str)
    return Page(
        values=entries[:limit],
        cursor=cursor,
        has_more=has_more
    )


def convert_datetime_to_str(dt: datetime) -> str:
    return dt.isoformat()


def convert_str_to_datetime(s: str) -> datetime:
    return datetime.fromisoformat(s)


class TimeEntryRepository(object):
    def __init__(self, database: DatabaseClient):
        self.__database = database

    def create_entry(self, entry: TimeEntry) -> None:
        try:
            self.__database.mutate(
                """
                INSERT INTO time_entries (entry_id, start_time, end_time)
                    VALUES (:id, :start, :end)
                """,
                id=entry.entry_id, start=entry.start_time, end=entry.end_time
            )
        except DatabaseError:
            logging.exception("Failed to create time entry.")

    def find_one_entry(self, entry_id: str) -> Optional[TimeEntry]:
        try:
            row = self.__database.find_one(
                """
                SELECT * FROM time_entries
                    WHERE entry_id = :id
                """,
                id=entry_id
            )
            return None if row is None else convert_row_to_entity(row)
        except DatabaseError:
            logging.exception("Failed to find time entry.")
            return None

    def find_entry_page(self, limit: int, cursor: Optional[bytes] = None) -> Page[TimeEntry]:
        try:
            if cursor is None:
                return self.find_first_entry_page(limit)
            else:
                return self.find_next_entry_page(limit, cursor)
        except DatabaseError:
            logging.exception("Failed to find time entry page.")
            return Page()

    def find_first_entry_page(self, limit: int) -> Page[TimeEntry]:
        try:
            rows = self.__database.find_many(
                """
                SELECT * FROM time_entries
                    ORDER BY start_time DESC
                    LIMIT :limit
                """,
                limit=limit + 1
            )
            entities = [convert_row_to_entity(row) for row in rows]
            return create_page(entities, limit)
        except DatabaseError:
            logging.exception("Failed to find first time entry page.")
            return Page()

    def find_next_entry_page(self, limit: int, cursor: bytes) -> Page[TimeEntry]:
        try:
            field, parameter = parse_cursor(cursor, convert_str_to_datetime)
            if field != "start_time" or parameter is None:
                return Page()

            rows = self.__database.find_many(
                """
                SELECT * FROM time_entries
                    WHERE start_time <= :cursor
                    ORDER BY start_time DESC
                    LIMIT :limit
                """,
                cursor=parameter, limit=limit + 1
            )
            entities = [convert_row_to_entity(row) for row in rows]
            return create_page(entities, limit)
        except DatabaseError:
            logging.exception("Failed to find next time entry page.")
            return Page()

    def find_entries_between(self, min_dt: datetime, max_dt: datetime) -> List[TimeEntry]:
        try:
            rows = self.__database.find_many(
                """
                SELECT * FROM time_entries
                    WHERE start_time >= :min AND start_time <= :max
                    ORDER BY start_time DESC
                """,
                min=min_dt, max=max_dt
            )
            return [convert_row_to_entity(row) for row in rows]
        except DatabaseError:
            logging.exception("Failed to find time entries between dates.")
            return []

    def update_entry(self, entry: TimeEntry):
        try:
            self.__database.mutate(
                """
                UPDATE time_entries
                    SET start_time = :start, end_time = :end
                    WHERE entry_id = :id
                """,
                id=entry.entry_id, start=entry.start_time, end=entry.end_time
            )
        except DatabaseError:
            logging.exception("Failed to update time entry.")

    def delete_entry(self, entry_id: str):
        try:
            self.__database.mutate(
                """
                DELETE FROM time_entries
                    WHERE entry_id = :id
                """,
                id=entry_id
            )
        except DatabaseError:
            logging.exception("Failed to delete time entry.")
