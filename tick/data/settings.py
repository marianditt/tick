from dataclasses import dataclass


@dataclass(frozen=True)
class Settings(object):
    session_id: str
    theme: str

    @staticmethod
    def default() -> 'Settings':
        return Settings(session_id="default", theme="dark")
