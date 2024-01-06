from datetime import date

from PyQt5.QtWidgets import QLabel


def format_date(d: date):
    day_digit = (d.day - 1) % 10
    suffix = "th" if day_digit > 2 else ["st", "nd", "rd"][day_digit]
    return d.strftime(f"%a, %b {d.day}{suffix}")


class DateLabel(QLabel):
    def __init__(self, d: date):
        super().__init__()
        self.__date = d
        self.__on_update()

    def set_date(self, d: date):
        self.__date = d
        self.__on_update()

    def __on_update(self):
        self.setText(format_date(self.__date))
