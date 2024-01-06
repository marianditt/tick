from typing import Optional, Iterable

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame

from tick.data.time_mode import TimeMode
from tick.ui.components.buttons.toggle_button import ToggleButton
from tick.ui.components.lists.ordered_list import OrderedList
from tick.ui.components.lists.scrollable_list import ScrollableList
from tick.ui.themes.layout_factory import LayoutFactory
from tick.ui.views.work_days.work_day_view import WorkDayView


class WorkDayListView(QWidget):
    end_of_work_day_list_reached = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__time_mode_button = ToggleButton[TimeMode]()
        self.__ordered_list = OrderedList[ScrollableList[WorkDayView], WorkDayView](
            ScrollableList[WorkDayView](),
            id_key=lambda x: x.get_work_day().work_day_id,
            order_key=lambda x: x.get_work_day().date
        )
        self.__setup_view()

    def insert_work_day_view(self, work_day_view: WorkDayView) -> None:
        work_day_view.update_time_mode(self.__time_mode_button.get_mode())
        self.__ordered_list.insert_widget(work_day_view)

    def get_work_day_view(self, work_day_id: str) -> Optional[WorkDayView]:
        return self.__ordered_list.get_widget(work_day_id)

    def get_work_day_views(self) -> Iterable[WorkDayView]:
        return self.__ordered_list.get_list_view().get_widgets()

    def delete_work_day(self, work_day_id: str) -> None:
        self.__ordered_list.delete_widget(work_day_id)

    def __on_time_mode_changed(self) -> None:
        for work_day_view in self.__ordered_list.get_list_view().get_widgets():
            work_day_view.update_time_mode(self.__time_mode_button.get_mode())

    def __setup_view(self) -> None:
        self.__time_mode_button.setFixedWidth(75)
        self.__time_mode_button.add_mode(TimeMode.CLOCK, "h:m:s")
        self.__time_mode_button.add_mode(TimeMode.DECIMAL, "#.##")

        time_mode_layout = LayoutFactory.horizontal()
        time_mode_layout.addStretch()
        time_mode_layout.addWidget(self.__time_mode_button)

        time_mode_widget = QFrame()
        time_mode_widget.setObjectName("time-mode-controls")
        time_mode_widget.setLayout(time_mode_layout)

        work_day_list = self.__ordered_list.get_list_view()

        layout = LayoutFactory.vertical(gap=8)
        layout.addWidget(time_mode_widget)
        layout.addWidget(work_day_list)
        self.setLayout(layout)

        work_day_list.end_of_list_reached.connect(self.end_of_work_day_list_reached.emit)
        self.__time_mode_button.mode_changed.connect(self.__on_time_mode_changed)
