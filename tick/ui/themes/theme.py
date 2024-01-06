from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ThemeColors(object):
    surface: str
    on_surface: str
    hover: Optional[str] = None


@dataclass(frozen=True)
class ColorTheme(object):
    primary: ThemeColors
    secondary: ThemeColors
    badge: ThemeColors
    level0: ThemeColors
    level1: ThemeColors
    level2: ThemeColors
    level3: ThemeColors


@dataclass(frozen=True)
class SpacingTheme(object):
    small: int
    medium: int
    large: int
    extra_large: int
    radius: int
    scrollbar_size: int


@dataclass(frozen=True)
class Theme(object):
    spacing: SpacingTheme
    color: ColorTheme
