from datetime import datetime
from typing import List
from uuid import UUID, uuid5

from tick.database.database_client import DatabaseClient


class Migration(object):
    def up(self, database: DatabaseClient):
        raise NotImplementedError()


class MigrationService(object):
    MIGRATION_NAMESPACE = UUID("ee7c50ba-af47-44d7-8437-e33ef510c0cb")

    @staticmethod
    def create_migration_id(migration: Migration):
        return str(uuid5(MigrationService.MIGRATION_NAMESPACE, migration.__class__.__name__))

    def __init__(self, database: DatabaseClient):
        self.__database = database

    def run(self, migrations: List[Migration]):
        self.__initialize_database()
        for migration in migrations:
            if not self.__has_migration(migration):
                self.__run_migration(migration)

    def __initialize_database(self):
        self.__database.mutate(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                migration_id TEXT PRIMARY KEY,
                created_at DATETIME NOT NULL,
                migration_name TEXT NOT NULL
            )
            """
        )

    def __has_migration(self, migration: Migration) -> bool:
        migration_id = self.create_migration_id(migration)
        row = self.__database.find_one(
            "SELECT migration_id FROM migrations WHERE migration_id = :id",
            id=migration_id
        )
        return row is not None

    def __run_migration(self, migration: Migration):
        migration_id = self.create_migration_id(migration)
        migration_name = migration.__class__.__name__
        migration.up(self.__database)
        self.__database.mutate(
            "INSERT INTO migrations (migration_id, created_at, migration_name) VALUES (:id, :stamp, :name)",
            id=migration_id, stamp=datetime.now(), name=migration_name
        )
