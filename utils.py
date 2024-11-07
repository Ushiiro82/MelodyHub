from pathlib import Path
from typing import Union

from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QWidget


FONT_DIRECTORY_PATH = "fonts"
FONT_BOLD_PATH = FONT_DIRECTORY_PATH / Path("Fira_Sans/FiraSans-Bold.ttf")
FONT_REGULAR_PATH = FONT_DIRECTORY_PATH / Path("Fira_Sans/FiraSans-Regular.ttf")

str_or_path = Union[Path, str]


def set_font(
        widget: QWidget,
        font_path: str_or_path,
        **q_font_kwargs
):
    if type(font_path) is not str:
        font_path = str(font_path)

    font_id = QFontDatabase.addApplicationFont(font_path)
    # Получаем имя шрифта
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    font = QFont(font_family, **q_font_kwargs)

    widget.setFont(font)


