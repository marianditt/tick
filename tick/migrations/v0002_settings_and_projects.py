from tick.database.migration_service import Migration


class V0002SettingsAndProjects(Migration):
    def up(self, database):
        database.mutate(
            """
            CREATE TABLE IF NOT EXISTS settings (
                session_id TEXT PRIMARY KEY,
                theme TEXT
            )
            """
        )

        database.mutate(
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                working_time INTEGER
            )
            """
        )
