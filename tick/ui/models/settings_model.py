from PyQt5.QtCore import QObject, pyqtSignal

from tick.data.settings import Settings
from tick.repositories.settings_repository import SettingsRepository


class SettingsModel(QObject):
    settings_updated = pyqtSignal(Settings)

    def __init__(self, repository: SettingsRepository):
        super().__init__()
        self.__repository = repository

    def load(self) -> None:
        settings = self.__repository.find_settings()
        self.settings_updated.emit(settings or Settings.default())

    def update_settings(self, settings: Settings) -> None:
        self.__repository.update_settings(settings)
        self.settings_updated.emit(settings)
