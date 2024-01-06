from datetime import date, datetime, timedelta
from uuid import uuid4

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon

from tick.data.time_entry import TimeEntry
from tick.data.timestamp import Timestamp
from tick.data.work_day import WorkDay
from tick.ui.components.buttons.hover_button import HoverButton
from tick.ui.components.buttons.long_press_button import LongPressButton
from tick.ui.components.buttons.toggle_button import ToggleButton
from tick.ui.components.editors.time_edit import TimeEdit, TimeEditMode
from tick.ui.components.labels.badge import Badge
from tick.ui.components.labels.date_label import DateLabel
from tick.ui.components.labels.header import Header
from tick.ui.views.time_entries.time_entry_view import TimeEntryView
from tick.ui.views.work_days.work_day_view import WorkDayView
from tick.ui.windows.styled_window import StyledWindow


class DemoWindow(StyledWindow):
    def __init__(self):
        super().__init__()

        self.__button_label = Header("Buttons")
        self.__theme_button = ToggleButton()
        self.__primary_hover_button = HoverButton("Primary", "Hovering")
        self.__secondary_hover_button = HoverButton("Secondary", "Hovering")
        self.__long_press_button = LongPressButton(1)

        self.__badge_label = Header("Labels")
        self.__badge = Badge()
        self.__date_label = DateLabel(date.today())

        self.__editor_label = Header("Editors")
        self.__minutes_editor = TimeEdit(TimeEditMode.HM)
        self.__seconds_editor = TimeEdit(TimeEditMode.HMS)

        self.__view_label = Header("Views")
        self.__time_entry_view = TimeEntryView(TimeEntry(str(uuid4()), datetime.now(), datetime.now()))
        self.__time_entry_model = TimeEntryModelMock()
        self.__work_day_view = WorkDayView(
            WorkDay(str(uuid4()), date.today(), timedelta(hours=8, minutes=30, seconds=12))
        )

        self.__setup_view()

    @property
    def theme(self) -> str:
        return self.__theme_button.get_mode()

    def __setup_view(self) -> None:
        self.__setup_buttons()
        self.__setup_labels()
        self.__setup_editors()
        self.__setup_child_views()
        self.add_stretch()

        self.__theme_button.mode_changed.connect(self.__on_theme_changed)
        self.__theme_button.add_mode("light", "Light")
        self.__theme_button.add_mode("dark", "Dark")

    def __setup_buttons(self) -> None:
        self.add_widget(self.__button_label)

        self.__theme_button.setFixedWidth(120)
        self.add_widget(self.__theme_button)

        self.__primary_hover_button.setFixedWidth(120)
        self.add_widget(self.__primary_hover_button)

        self.__secondary_hover_button.setFixedWidth(120)
        self.add_widget(self.__secondary_hover_button)

        self.__long_press_button.setIcon(QIcon.fromTheme("delete"))
        self.add_widget(self.__long_press_button)

    def __setup_labels(self) -> None:
        self.add_widget(self.__badge_label)

        self.__badge.setText("badge text")
        self.add_widget(self.__badge)
        self.add_widget(self.__date_label)

    def __setup_editors(self) -> None:
        self.add_widget(self.__editor_label)

        self.__minutes_editor.update_timestamp(Timestamp.from_datetime(datetime.now()))
        self.__minutes_editor.setFixedWidth(90)
        self.add_widget(self.__minutes_editor)

        self.__seconds_editor.update_timestamp(Timestamp.from_datetime(datetime.now()))
        self.__seconds_editor.setFixedWidth(90)
        self.add_widget(self.__seconds_editor)

    def __setup_child_views(self) -> None:
        self.add_widget(self.__view_label)

        self.__time_entry_view.update_time_entry_requested.connect(self.__time_entry_model.time_entry_changed.emit)
        self.__time_entry_model.time_entry_changed.connect(self.__time_entry_view.update_time_entry)
        self.add_widget(self.__time_entry_view)

        self.__work_day_view.update_working_time(Timestamp.from_hms(hours=8))
        self.add_widget(self.__work_day_view)

    def __on_theme_changed(self) -> None:
        self.theme_changed.emit(self.__theme_button.get_mode())


class TimeEntryModelMock(QObject):
    time_entry_changed = pyqtSignal(TimeEntry)

    def __init__(self):
        super().__init__()
