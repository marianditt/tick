import logging
import sqlite3
from datetime import datetime
from typing import Tuple, List, Optional
from zoneinfo import ZoneInfo

from tick.database.database_client import DatabaseClient, DatabaseError


def adapt_datetime(dt: datetime) -> str:
    return dt.astimezone(ZoneInfo("UTC")).isoformat()


def convert_datetime(dt: bytes) -> datetime:
    return datetime.fromisoformat(dt.decode()).astimezone()


class SqliteDatabase(DatabaseClient):
    def __init__(self, database_path: str):
        self.__database_path = database_path
        self.__connection: Optional[sqlite3.Connection] = None
        self.__cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self):
        try:
            sqlite3.register_adapter(datetime, adapt_datetime)
            sqlite3.register_converter("datetime", convert_datetime)

            self.__connection = sqlite3.connect(self.__database_path, detect_types=sqlite3.PARSE_DECLTYPES)
            self.__cursor = self.__connection.cursor()
            return self
        except sqlite3.Error:
            logging.exception(f"Failed to connect to database at {self.__database_path}.")
            raise DatabaseError("Failed to connect to database.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__connection.close()
        except sqlite3.Error:
            logging.exception("Failed to close database connection.")

    def find_one(self, query: str, **kwargs) -> Optional[Tuple]:
        try:
            self.__cursor.execute(query, kwargs)
            return self.__cursor.fetchone()
        except sqlite3.Error:
            logging.exception(f"Failed to execute find one query: {query}, args: {kwargs}")
            raise DatabaseError("Failed to execute find one query.")

    def find_many(self, query: str, **kwargs) -> List[Tuple]:
        try:
            self.__cursor.execute(query, kwargs)
            return self.__cursor.fetchall()
        except sqlite3.Error:
            logging.exception(f"Failed to execute find all query: {query}, args: {kwargs}")
            raise DatabaseError("Failed to execute find all query.")

    def mutate(self, query: str, **kwargs):
        try:
            self.__cursor.execute(query, kwargs)
            self.__connection.commit()
        except sqlite3.Error:
            logging.exception(f"Failed to execute mutation: {query}, args: {kwargs}")
            raise DatabaseError("Failed to execute mutation.")
