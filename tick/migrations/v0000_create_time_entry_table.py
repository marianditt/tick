from tick.database.database_client import DatabaseClient
from tick.database.migration_service import Migration


class V0000CreateTimeEntryTable(Migration):
    def up(self, database: DatabaseClient):
        database.mutate(
            """
            CREATE TABLE IF NOT EXISTS time_entries (
                entry_id TEXT PRIMARY KEY,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL
            )
            """
        )
        database.mutate("CREATE INDEX start_time_idx ON time_entries (start_time)")
