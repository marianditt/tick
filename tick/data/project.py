from dataclasses import dataclass


@dataclass(frozen=True)
class Project(object):
    project_id: str
    working_time: int

    @staticmethod
    def default() -> 'Project':
        return Project(project_id="default", working_time=8 * 60 * 60)
