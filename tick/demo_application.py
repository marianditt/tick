from tick.styled_application import StyledApplication
from tick.ui.windows.demo_window import DemoWindow


class DemoApplication(StyledApplication):
    def exec(self) -> int:
        window = DemoWindow()
        window.theme_changed.connect(self.set_theme)
        self.set_theme(window.theme)
        window.show()
        return super().exec()
