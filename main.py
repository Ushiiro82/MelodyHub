import sys

from typing import Union

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QFontDatabase, QColor

from pathlib import Path
from ui.main_window import Ui_MainWindow


FONT_DIRECTORY_PATH = "fonts"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = Ui_MainWindow()
        self.window.setupUi(self)

        self.init_fonts()
        self.add_shadow_to_title(self.window.title)

    def init_fonts(self):
        font_bold_path = FONT_DIRECTORY_PATH / Path("Fira_Sans/FiraSans-Bold.ttf")
        font_regular_path = FONT_DIRECTORY_PATH / Path("Fira_Sans/FiraSans-Regular.ttf")

        font_title = self.window.title.font()
        font_search_line = self.window.search_line.font()

        self.set_font(self.window.title, font_path=font_bold_path, pointSize=font_title.pointSize(), weight=font_title.weight())
        self.set_font(self.window.search_line, font_path=font_regular_path, pointSize=font_search_line.pointSize())

        print(self.window.search_line.font().family())

    @staticmethod
    def add_shadow_to_title(title: QLabel):
        shadow = QGraphicsDropShadowEffect()

        shadow.setXOffset(0)
        shadow.setYOffset(4)

        shadow.setBlurRadius(4)
        shadow.setColor(QColor(0, 0, 0, 64))

        title.setGraphicsEffect(shadow)

    @staticmethod
    def set_font(
            widget: QWidget,
            font_path: Union[Path, str],
            **q_font_kwargs
    ):
        if type(font_path) is not str:
            font_path = str(font_path)

        font_id = QFontDatabase.addApplicationFont(font_path)
        # Получаем имя шрифта
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, **q_font_kwargs)

        widget.setFont(font)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
