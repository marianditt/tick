import logging

from tick.data.time_entry import TimeEntry
from tick.database.database_client import DatabaseError
from tick.database.sqlite_database import SqliteDatabase
from tick.prod_application import ProdApplication
from tick.repositories.time_entry_repository import TimeEntryRepository


class TestApplication(ProdApplication):
    def exec(self) -> int:
        db_file_name = './db/test.sqlite'

        try:
            with SqliteDatabase(db_file_name) as database:
                entry_repository = TimeEntryRepository(database)
                create_fake_data(entry_repository)
        except DatabaseError:
            logging.exception("Failed to access database.")
        return super().exec(db_file_name=db_file_name)


def create_fake_data(repository: TimeEntryRepository):
    from datetime import datetime

    def generate_id():
        from uuid import uuid5, UUID
        seed = 0
        while True:
            yield str(uuid5(UUID("0f816fc6-b609-43fd-ae8c-97e33bc5d4cf"), str(seed)))
            seed += 1

    def create_entry(entry_id: str) -> TimeEntry:
        import random
        now = datetime.now()
        start_time = now.replace(
            month=random.randint(1, now.month),
            day=random.randint(1, now.day),
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        end_time = start_time.replace(
            hour=random.randint(start_time.hour, 23),
            minute=random.randint(start_time.minute, 59),
            second=random.randint(start_time.second, 59)
        )
        return TimeEntry(entry_id=entry_id, start_time=start_time, end_time=end_time)

    def run():
        if repository.find_one_entry(next(generate_id())) is not None:
            return

        generator = generate_id()
        for _ in range(200):
            entry_id = next(generator)
            repository.create_entry(create_entry(entry_id))

    run()
