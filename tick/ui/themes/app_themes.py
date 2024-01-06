from tick.ui.themes.theme import ColorTheme, ThemeColors, SpacingTheme, Theme

spacing = SpacingTheme(
    small=2,
    medium=4,
    large=8,
    extra_large=16,
    radius=6,
    scrollbar_size=6
)

dark_theme = Theme(
    spacing=spacing,
    color=ColorTheme(
        primary=ThemeColors(
            surface="#2fbdfc",
            hover="#039add",
            on_surface="#ffffff"
        ),

        secondary=ThemeColors(
            surface="#f44336",
            hover="#f6695e",
            on_surface="#ffffff"
        ),

        badge=ThemeColors(
            surface="#ffffff",
            on_surface="#000000"
        ),

        level0=ThemeColors(
            surface="#474747",
            on_surface="#ffffff"
        ),

        level1=ThemeColors(
            surface="#191919",
            on_surface="#ffffff"
        ),

        level2=ThemeColors(
            surface="#272727",
            on_surface="#ffffff"
        ),

        level3=ThemeColors(
            surface="#191919",
            on_surface="#888888"
        )
    )
)

light_theme = Theme(
    spacing=spacing,
    color=ColorTheme(
        primary=ThemeColors(
            surface="#2fbdfc",
            hover="#039add",
            on_surface="#ffffff"
        ),

        secondary=ThemeColors(
            surface="#f44336",
            hover="#f6695e",
            on_surface="#ffffff"
        ),

        badge=ThemeColors(
            surface="#000000",
            on_surface="#ffffff"
        ),

        level0=ThemeColors(
            surface="#efefef",
            on_surface="#000000"
        ),

        level1=ThemeColors(
            surface="#d4d4d4",
            on_surface="#000000"
        ),

        level2=ThemeColors(
            surface="#ffffff",
            on_surface="#000000"
        ),

        level3=ThemeColors(
            surface="#d4d4d4",
            on_surface="#555555"
        )
    )
)
