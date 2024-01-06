from tick.ui.themes.theme import Theme


def create_style(theme: Theme) -> str:
    return f"""
        {create_base_style(theme)}
        {create_level1_style(theme)}
        {create_button_style(theme)}
        {create_toggle_button_style()}
        {create_time_tracker_controls_style(theme)}
        {create_start_button_style(theme)}
        {create_stop_button_style(theme)}
        {create_line_edit_style(theme)}
        {create_badge_style(theme)}
        {create_header_style(theme)}
        {create_scrollable_list_style(theme)}
        {create_time_mode_controls_style(theme)}
        {create_work_day_view_style(theme)}
        {create_work_day_title_style(theme)}
        {create_time_entry_view_style(theme)}
        """


def create_debug_style() -> str:
    return f"""
        *:hover {{
            border: 1px solid magenta;
        }}
        """


def create_base_style(theme: Theme) -> str:
    return f"""
        * {{
            background-color: {theme.color.level0.surface};
            color: {theme.color.level0.on_surface};
            margin: 0;
            border: none;
            border-radius: 0;
            padding: 0;
            selection-background-color: {theme.color.primary.surface};
            selection-color: {theme.color.primary.on_surface};
        }}
        """


def create_level1_style(theme: Theme) -> str:
    return f"""
        #level1, #level1 * {{
            background-color: {theme.color.level1.surface};
            color: {theme.color.level1.on_surface};
        }}
        """


def create_button_style(theme: Theme) -> str:
    return f"""
        QPushButton {{
            border-radius: {theme.spacing.radius}px;
            padding: {theme.spacing.large}px;
        }}
        """


def create_toggle_button_style() -> str:
    return f"""
        ToggleButton {{
            text-align: left;
        }}
        """


def create_time_tracker_controls_style(theme: Theme) -> str:
    return f"""
        TimeTrackerControls, TimeTrackerControls * {{
            background-color: {theme.color.level1.surface};
            color: {theme.color.level1.on_surface};
        }}
        TimeTrackerControls {{
            padding: {theme.spacing.extra_large}px;
        }}
        """


def create_start_button_style(theme: Theme) -> str:
    return f"""
        QPushButton#start-button {{
            background-color: {theme.color.primary.surface};
            color: {theme.color.primary.on_surface};
        }}
        QPushButton#start-button:hover {{
            background-color: {theme.color.primary.hover};
        }}
        """


def create_stop_button_style(theme: Theme) -> str:
    return f"""
        HoverButton#stop-button {{
            background-color: {theme.color.secondary.surface};
            color: {theme.color.secondary.on_surface};
        }}
        HoverButton#stop-button:hover {{
            background-color: {theme.color.secondary.hover};
        }}
        """


def create_line_edit_style(theme: Theme) -> str:
    return f"""
        QLineEdit {{
            border-radius: {theme.spacing.radius}px;
            padding: {theme.spacing.small}px;
        }}
        QLineEdit:hover, QLineEdit:focus {{
            border: 1px solid {theme.color.primary.surface};
        }}
        """


def create_badge_style(theme: Theme) -> str:
    return f"""
        Badge {{
            background-color: {theme.color.badge.surface};
            color: {theme.color.badge.on_surface};
            font-size: 12px;
            border-radius: 12px;
            padding: {theme.spacing.medium}px;
        }}
        """


def create_header_style(theme: Theme) -> str:
    return f"""
        Header {{
            font-size: 20px;
            font-weight: bold;
            margin-top: {theme.spacing.extra_large}px;
            margin-bottom: {theme.spacing.medium}px;
        }}
        """


def create_scrollable_list_style(theme: Theme) -> str:
    return f"""
        ScrollableContent {{
            padding-left: {theme.spacing.extra_large}px;
            padding-right: {theme.spacing.extra_large - theme.spacing.scrollbar_size}px;
        }}
        QScrollBar {{
            width: {theme.spacing.scrollbar_size}px;
            height: {theme.spacing.scrollbar_size}px;
        }}
        QScrollBar::handle {{
            background-color: {theme.color.primary.surface};
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            height: 0;
        }}
        """


def create_time_mode_controls_style(theme: Theme) -> str:
    return f"""
        QFrame#time-mode-controls, QFrame#time-mode-controls * {{
            background-color: {theme.color.level1.surface};
        }}
        QFrame#time-mode-controls {{
            padding-left: {theme.spacing.extra_large}px;
            padding-right: {theme.spacing.extra_large}px;
        }}
        """


def create_time_entry_view_style(theme: Theme) -> str:
    return f"""
        TimeEntryView, TimeEntryView * {{
            background-color: {theme.color.level2.surface};
            color: {theme.color.level2.on_surface};
        }}
        TimeEntryView {{
            border-radius: {theme.spacing.radius}px;
            padding: {theme.spacing.medium}px;
        }}
        """


def create_work_day_view_style(theme: Theme) -> str:
    return f"""
        WorkDayView, WorkDayView * {{
            background-color: {theme.color.level1.surface};
            color: {theme.color.level1.on_surface};
        }}
        WorkDayView {{
            border-radius: {theme.spacing.radius}px;
            margin-bottom: {theme.spacing.extra_large}px;
            padding: {theme.spacing.medium}px;
        }}
        """


def create_work_day_title_style(theme: Theme) -> str:
    return f"""
        WorkDayTitle, WorkDayTitle * {{
            font-size: 12px;
        }}
        WorkDayTitle {{
            padding: {theme.spacing.large}px;
        }}
        #work-day-title-label {{
            font-weight: bold;
            color: {theme.color.level3.on_surface};
        }}
        """
