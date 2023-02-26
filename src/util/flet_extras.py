import flet as ft
from flet import ButtonStyle, ControlEvent


class WindowEventType:
    CLOSE = "close"
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"
    RESTORE = "restore"
    MOVE = "move"
    BLUR = "blur"


class THEME:

    PRIMARY = "#f28c18"
    PRIMARY_CONTENT = "#131616"
    SECONDARY = "#6d3a9c"
    ACCENT = "#51a800"
    NEUTRAL = "#1b1d1d"
    BASE_100 = "#212121"
    INFO = "#2563eb"
    SUCCESS = "#16a34a"
    WARNING = "#d97706"
    ERROR = "#dc2626"
    


class STYLES:

    PRIMARY = ButtonStyle(
        color={
            ft.MaterialState.DEFAULT: THEME.PRIMARY
        }
    )

class GenericEvent(ControlEvent):
    
    def __init__(self, target: str = None, name: str = None, data: str = None, control= None, page = None):
        super().__init__(target, name, data, control, page)

