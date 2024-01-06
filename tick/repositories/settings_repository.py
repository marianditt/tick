import logging
from typing import Optional, Tuple

from tick.data.settings import Settings
from tick.database.database_client import DatabaseClient, DatabaseError


def convert_row_to_entity(row: Tuple) -> Settings:
    return Settings(session_id=row[0], theme=row[1])


class SettingsRepository(object):
    def __init__(self, database: DatabaseClient):
        self.__database = database

    def find_settings(self) -> Optional[Settings]:
        try:
            rows = self.__database.find_many(
                """
                SELECT * FROM settings
                """
            )
            if len(rows) == 1:
                return convert_row_to_entity(rows[0])
            else:
                logging.error(f"Expected 1 settings, found {len(rows)}.")
                return None
        except DatabaseError:
            logging.exception("Failed to find settings.")
            return None

    def update_settings(self, settings: Settings) -> None:
        try:
            self.__database.mutate(
                """
                UPDATE settings
                    SET theme = :theme
                    WHERE session_id = :session_id
                """,
                session_id=settings.session_id, theme=settings.theme
            )
        except DatabaseError:
            logging.exception("Failed to update settings.")
