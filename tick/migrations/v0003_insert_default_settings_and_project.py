from tick.data.project import Project
from tick.data.settings import Settings
from tick.database.migration_service import Migration


class V0003InsertDefaultSettingsAndProject(Migration):
    def up(self, database):
        settings = Settings.default()
        project = Project.default()

        database.mutate(
            """
            INSERT INTO settings (session_id, theme)
                VALUES (:session_id, :theme)
            """,
            session_id=settings.session_id, theme=settings.theme
        )

        database.mutate(
            """
            INSERT INTO projects (project_id, working_time)
                VALUES (:project_id, :working_time)
            """,
            project_id=project.project_id, working_time=project.working_time
        )
