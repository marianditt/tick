import logging
from typing import List, Optional

from tick.data.time_tracker import TimeTracker
from tick.database.database_client import DatabaseClient, DatabaseError


def convert_row_to_entity(row: tuple) -> TimeTracker:
    return TimeTracker(tracker_id=row[0], start_time=row[1])


class TimeTrackerRepository(object):
    def __init__(self, database: DatabaseClient):
        self.__database = database

    def start_tracker(self, tracker: TimeTracker):
        try:
            self.__database.mutate(
                """
                INSERT INTO time_trackers (tracker_id, start_time)
                    VALUES (:id, :start)
                """,
                id=tracker.tracker_id, start=tracker.start_time
            )
        except DatabaseError:
            logging.exception("Failed to start time tracker.")

    def find_running_trackers(self) -> List[TimeTracker]:
        try:
            rows = self.__database.find_many("SELECT * FROM time_trackers")
            return [convert_row_to_entity(row) for row in rows]
        except DatabaseError:
            logging.exception("Failed to find running time tracker.")
            return []

    def find_one_tracker(self, tracker_id: str) -> Optional[TimeTracker]:
        try:
            row = self.__database.find_one(
                """
                SELECT * FROM time_trackers
                    WHERE tracker_id = :id
                """,
                id=tracker_id
            )
            return None if row is None else convert_row_to_entity(row)
        except DatabaseError:
            logging.exception("Failed to find time tracker.")
            return None

    def update_tracker(self, tracker: TimeTracker):
        try:
            self.__database.mutate(
                """
                UPDATE time_trackers
                    SET start_time = :start
                    WHERE tracker_id = :id
                """,
                id=tracker.tracker_id, start=tracker.start_time
            )
        except DatabaseError:
            logging.exception("Failed to update time tracker.")

    def stop_tracker(self, tracker_id: str):
        try:
            self.__database.mutate(
                """
                DELETE FROM time_trackers
                    WHERE tracker_id = :id
                """,
                id=tracker_id
            )
        except DatabaseError:
            logging.exception("Failed to stop time tracker.")
