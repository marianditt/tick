from typing import List

from tick.database.migration_service import Migration
from tick.migrations.v0000_create_time_entry_table import V0000CreateTimeEntryTable
from tick.migrations.v0001_create_time_trackers_table import V0001CreateTimeTrackersTable
from tick.migrations.v0002_settings_and_projects import V0002SettingsAndProjects
from tick.migrations.v0003_insert_default_settings_and_project import V0003InsertDefaultSettingsAndProject

MIGRATIONS: List[Migration] = [
    V0000CreateTimeEntryTable(),
    V0001CreateTimeTrackersTable(),
    V0002SettingsAndProjects(),
    V0003InsertDefaultSettingsAndProject()
]
