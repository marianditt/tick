from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QMainWindow, QLabel, QSizePolicy

from tick.data.project import Project
from tick.data.settings import Settings
from tick.data.timestamp import Timestamp
from tick.ui.components.buttons.toggle_button import ToggleButton
from tick.ui.components.editors.time_edit import TimeEdit, TimeEditMode
from tick.ui.models.project_model import ProjectModel
from tick.ui.models.settings_model import SettingsModel
from tick.ui.models.time_entry_model import TimeEntryModel
from tick.ui.models.time_tracker_model import TimeTrackerModel
from tick.ui.themes.layout_factory import LayoutFactory
from tick.ui.views.time_tracking_view import TimeTrackingView


class AppWindow(QMainWindow):
    theme_changed = pyqtSignal(str)

    def __init__(
            self,
            settings_model: SettingsModel,
            project_model: ProjectModel,
            time_tracker_model: TimeTrackerModel,
            time_entry_model: TimeEntryModel
    ):
        super().__init__()
        self.__settings_model = settings_model
        self.__project_model = project_model
        self.__time_tracker_model = time_tracker_model
        self.__time_entry_model = time_entry_model

        self.__theme_button = ToggleButton[str]()
        self.__working_time_edit = TimeEdit(TimeEditMode.HM)
        self.__time_tracking_view = TimeTrackingView()
        self.__setup_view()

    @property
    def theme(self) -> str:
        return self.__theme_button.get_mode()

    def update_settings(self, settings: Settings) -> None:
        self.__theme_button.select_mode(settings.theme)
        self.theme_changed.emit(settings.theme)

    def __setup_view(self) -> None:
        self.setWindowTitle("Time Tracker")
        self.setWindowIcon(QIcon.fromTheme("timer"))
        self.setMinimumSize(QSize(400, 600))

        self.__theme_button.setFixedWidth(75)
        self.__theme_button.add_mode("dark", "Dark")
        self.__theme_button.add_mode("light", "Light")

        self.__working_time_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.__working_time_edit.setFixedWidth(55)

        settings_bar_layout = LayoutFactory.horizontal(gap=4)
        settings_bar_layout.addWidget(self.__theme_button)
        settings_bar_layout.addStretch()
        settings_bar_layout.addWidget(QLabel("Working Time"))
        settings_bar_layout.addWidget(self.__working_time_edit)
        settings_bar_layout.addStretch()
        settings_bar = QFrame()
        settings_bar.setObjectName("level1")
        settings_bar.setLayout(settings_bar_layout)

        central_layout = LayoutFactory.vertical()
        central_layout.addWidget(settings_bar)
        central_layout.addWidget(self.__time_tracking_view)

        central_widget = QFrame()
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        self.__connect_settings_model()
        self.__connect_project_model()
        self.__connect_time_tracker_model()
        self.__connect_time_entry_model()

    def __connect_settings_model(self) -> None:
        self.__settings_model.settings_updated.connect(self.update_settings)
        self.__theme_button.mode_changed.connect(self.__on_theme_changed)

    def __connect_project_model(self) -> None:
        self.__project_model.project_updated.connect(self.__on_project_updated)
        self.__working_time_edit.timestamp_changed.connect(self.__on_working_time_changed)

    def __connect_time_tracker_model(self) -> None:
        self.__time_tracker_model.started.connect(self.__time_tracking_view.create_time_tracker)
        self.__time_tracker_model.tracker_updated.connect(self.__time_tracking_view.update_time_tracker)
        self.__time_tracker_model.stopped.connect(self.__time_tracking_view.delete_time_tracker)
        self.__time_tracker_model.create_time_entry_requested.connect(self.__time_entry_model.insert_time_entry)

        self.__time_tracking_view.start_tracker_requested.connect(self.__time_tracker_model.start)
        self.__time_tracking_view.update_tracker_requested.connect(self.__time_tracker_model.update_tracker)
        self.__time_tracking_view.stop_tracker_requested.connect(self.__time_tracker_model.stop)

    def __connect_time_entry_model(self) -> None:
        self.__time_entry_model.work_day_inserted.connect(self.__time_tracking_view.insert_work_day)
        self.__time_entry_model.work_day_updated.connect(self.__time_tracking_view.update_work_day)
        self.__time_entry_model.work_day_deleted.connect(self.__time_tracking_view.delete_work_day)
        self.__time_entry_model.time_entry_inserted.connect(self.__time_tracking_view.insert_time_entry)
        self.__time_entry_model.time_entry_updated.connect(self.__time_tracking_view.update_time_entry)
        self.__time_entry_model.time_entry_deleted.connect(self.__time_tracking_view.delete_time_entry)

        self.__time_tracking_view.end_of_work_day_list_reached.connect(self.__time_entry_model.load_more)
        self.__time_tracking_view.update_time_entry_requested.connect(self.__time_entry_model.update_time_entry)
        self.__time_tracking_view.delete_time_entry_requested.connect(self.__time_entry_model.delete_time_entry)

    def __on_theme_changed(self) -> None:
        settings = Settings.default()
        theme = self.__theme_button.get_mode()
        self.__settings_model.update_settings(Settings(session_id=settings.session_id, theme=theme))

    def __on_project_updated(self, project: Project) -> None:
        self.__working_time_edit.update_timestamp(Timestamp(project.working_time))
        self.__time_tracking_view.update_project(project)

    def __on_working_time_changed(self, timestamp: Timestamp) -> None:
        project = Project.default()
        self.__project_model.update_project(
            Project(project_id=project.project_id, working_time=timestamp.total_seconds)
        )
