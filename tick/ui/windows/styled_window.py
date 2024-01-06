from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame

from tick.data.settings import Settings
from tick.ui.themes.layout_factory import LayoutFactory


class StyledWindow(QMainWindow):
    update_settings_requested = pyqtSignal(Settings)
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__settings = Settings.default()
        self.__setup_view()

    @property
    def settings(self) -> Settings:
        return self.__settings

    def add_widget(self, widget: QWidget) -> None:
        self.centralWidget().layout().addWidget(widget)

    def add_stretch(self) -> None:
        self.centralWidget().layout().addStretch()

    def update_settings(self, settings: Settings) -> None:
        self.__settings = settings
        self.theme_changed.emit(settings.theme)

    def __setup_view(self) -> None:
        self.setCentralWidget(QFrame())
        self.centralWidget().setLayout(LayoutFactory.vertical(gap=0))
