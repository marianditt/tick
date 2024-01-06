import logging

from tick.database.database_client import DatabaseError
from tick.database.migration_service import MigrationService
from tick.database.sqlite_database import SqliteDatabase
from tick.migrations.migrations import MIGRATIONS
from tick.repositories.project_repository import ProjectRepository
from tick.repositories.settings_repository import SettingsRepository
from tick.repositories.time_entry_repository import TimeEntryRepository
from tick.repositories.time_tracker_repository import TimeTrackerRepository
from tick.styled_application import StyledApplication
from tick.ui.models.project_model import ProjectModel
from tick.ui.models.settings_model import SettingsModel
from tick.ui.models.time_entry_model import TimeEntryModel
from tick.ui.models.time_tracker_model import TimeTrackerModel
from tick.ui.windows.app_window import AppWindow


class ProdApplication(StyledApplication):
    def exec(self, **kwargs) -> int:
        logging.basicConfig(level=logging.DEBUG)
        db_file_name = kwargs.get('db_file_name', './db/prod.sqlite')

        try:
            with SqliteDatabase(db_file_name) as database:
                migration_service = MigrationService(database)
                migration_service.run(MIGRATIONS)

                settings_repository = SettingsRepository(database)
                settings_model = SettingsModel(settings_repository)

                project_repository = ProjectRepository(database)
                project_model = ProjectModel(project_repository)

                time_entry_repository = TimeEntryRepository(database)
                time_entry_model = TimeEntryModel(time_entry_repository)

                tracker_repository = TimeTrackerRepository(database)
                tracker_model = TimeTrackerModel(tracker_repository)

                window = AppWindow(settings_model, project_model, tracker_model, time_entry_model)
                window.theme_changed.connect(self.set_theme)
                self.set_theme(window.theme)
                window.show()

                settings_model.load()
                project_model.load()
                tracker_model.load()
                time_entry_model.load_more()
                return super().exec()
        except DatabaseError:
            logging.exception("Failed to access database.")
            return 1
