from typing import Optional

from PyQt5.QtWidgets import QFrame, QSizePolicy

from tick.data.time_mode import TimeMode
from tick.data.timestamp import Timestamp
from tick.data.work_day import WorkDay
from tick.ui.components.lists.ordered_list import OrderedList
from tick.ui.components.lists.widget_list import WidgetList
from tick.ui.themes.layout_factory import LayoutFactory
from tick.ui.views.time_entries.time_entry_view import TimeEntryView
from tick.ui.views.work_days.work_day_title import WorkDayTitle


class WorkDayView(QFrame):
    def __init__(self, work_day: WorkDay):
        super().__init__()

        # Data
        self.__work_day = work_day

        # View
        self.__work_day_title = WorkDayTitle(work_day)
        self.__ordered_list = OrderedList[WidgetList[TimeEntryView], TimeEntryView](
            WidgetList[TimeEntryView](),
            id_key=lambda x: x.get_time_entry().entry_id,
            order_key=lambda x: x.get_time_entry().start_time
        )

        self.__setup_view()

    def get_work_day(self) -> WorkDay:
        return self.__work_day

    def update_work_day(self, work_day: WorkDay) -> None:
        self.__work_day = work_day
        self.__work_day_title.update_work_day(work_day)

    def update_working_time(self, working_time: Timestamp) -> None:
        self.__work_day_title.update_working_time(working_time)

    def update_time_mode(self, time_mode: TimeMode) -> None:
        self.__work_day_title.update_time_mode(time_mode)

    def insert_time_entry_view(self, time_entry_view: TimeEntryView) -> None:
        self.__ordered_list.insert_widget(time_entry_view)

    def get_time_entry_view(self, entry_id: str) -> Optional[TimeEntryView]:
        return self.__ordered_list.get_widget(entry_id)

    def delete_time_entry(self, entry_id: str) -> None:
        self.__ordered_list.delete_widget(entry_id)

    def __setup_view(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        layout = LayoutFactory.vertical()
        layout.addWidget(self.__work_day_title)
        layout.addWidget(self.__ordered_list.get_list_view())
        self.setLayout(layout)
