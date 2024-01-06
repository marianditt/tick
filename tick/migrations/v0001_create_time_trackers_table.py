from tick.database.migration_service import Migration


class V0001CreateTimeTrackersTable(Migration):
    def up(self, database):
        database.mutate(
            """
            CREATE TABLE IF NOT EXISTS time_trackers (
                tracker_id TEXT PRIMARY KEY,
                start_time DATETIME NOT NULL
            )
            """
        )
