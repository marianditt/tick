import logging
from typing import Optional, Tuple

from tick.data.project import Project
from tick.database.database_client import DatabaseClient, DatabaseError


def convert_row_to_entity(row: Tuple) -> Project:
    return Project(project_id=row[0], working_time=row[1])


class ProjectRepository(object):
    def __init__(self, database: DatabaseClient):
        self.__database = database

    def get_project(self) -> Optional[Project]:
        try:
            rows = self.__database.find_many(
                """
                SELECT * FROM projects
                """
            )
            if len(rows) == 1:
                return convert_row_to_entity(rows[0])
            else:
                logging.error(f"Expected 1 project, found {len(rows)}.")
                return None
        except DatabaseError:
            logging.exception("Failed to find project.")
            return None

    def update_project(self, project: Project) -> None:
        try:
            self.__database.mutate(
                """
                UPDATE projects
                    SET working_time = :working_time
                    WHERE project_id = :id
                """,
                id=project.project_id, working_time=project.working_time
            )
        except DatabaseError:
            logging.exception("Failed to update project.")
