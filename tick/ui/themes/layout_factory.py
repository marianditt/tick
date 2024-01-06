from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLayout, QStackedLayout


class LayoutFactory(object):

    @staticmethod
    def horizontal(gap: int = 0) -> QHBoxLayout:
        layout = QHBoxLayout()
        configure_layout(layout, gap)
        return layout

    @staticmethod
    def vertical(gap: int = 0) -> QVBoxLayout:
        layout = QVBoxLayout()
        configure_layout(layout, gap)
        return layout

    @staticmethod
    def stacked() -> QStackedLayout:
        layout = QStackedLayout()
        configure_layout(layout, 0)
        return layout


def configure_layout(layout: QLayout, gap: int) -> None:
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(gap)
