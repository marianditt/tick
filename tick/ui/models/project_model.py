from PyQt5.QtCore import QObject, pyqtSignal

from tick.data.project import Project
from tick.repositories.project_repository import ProjectRepository


class ProjectModel(QObject):
    project_updated = pyqtSignal(Project)

    def __init__(self, repository: ProjectRepository):
        super().__init__()
        self.__repository = repository

    def load(self) -> None:
        project = self.__repository.get_project()
        self.project_updated.emit(project or Project.default())

    def update_project(self, project: Project) -> None:
        self.__repository.update_project(project)
        self.project_updated.emit(project)
