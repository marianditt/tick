import logging
import sys
from typing import Dict

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from tick.ui.themes.app_themes import light_theme, dark_theme
from tick.ui.themes.style_factory import create_style


class StyledApplication(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.__styles: Dict[str, str] = {}
        self.__setup_app()

    def __setup_app(self) -> None:
        QIcon.setThemeSearchPaths(["assets/icons"])
        self.__styles["light"] = create_style(light_theme)
        self.__styles["dark"] = create_style(dark_theme)

    def set_theme(self, theme: str) -> None:
        QIcon.setThemeName(theme)
        self.setStyleSheet(self.__styles[theme])


def load_style(path: str) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        logging.exception(f"Could not load style from {path}.")
        return ""
