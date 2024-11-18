import sys

from PyQt6.QtCore import Qt, QPropertyAnimation, QSize, pyqtSlot
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor

from pathlib import Path

from menu_button import MenuButton
from ui.main_window import Ui_MainWindow
from utils import set_font, FONT_REGULAR_PATH, FONT_BOLD_PATH, start_backward_animation

import parsing.hitmo_parser_with_search as hitmo_parser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = Ui_MainWindow()
        self.window.setupUi(self)

        self.search_line_focus_animation = QPropertyAnimation(self.window.search_line, b"size")

        self.add_shadow_to_title(self.window.title)

        self.init_fonts()
        self.init_buttons()
        # self.init_animations()
        self.init_events()

    def init_events(self):
        self.window.search_line.returnPressed.connect(self.search)

    def init_animations(self):
        self.window.search_line.focusInEvent = lambda _: self.search_line_focus_animation.start()
        self.window.search_line.focusOutEvent = lambda _: start_backward_animation(self.search_line_focus_animation)

        self.search_line_focus_animation.setDuration(200)
        self.search_line_focus_animation.setStartValue(self.window.search_line.size())
        self.search_line_focus_animation.setEndValue(self.window.search_line.size() + QSize(10, 10))

    def init_buttons(self):
        layout = self.window.horizontalLayout
        path_icons = Path("icons")
        path_img = Path("img")

        for button_info in [
            ("Актуальные жанры", path_icons / "album.svg", path_img / "actual_genres.png"),
            ("Актуальные плагины", path_icons / "graphic_eq.svg", path_img / "actual_plugins.png"),
            ("Сплиттер mp3", path_icons / "splitscreen.svg", path_img / "splitter.png")
        ]:
            button = MenuButton(button_info[0], button_info[1], button_info[2])
            button.clicked.connect(lambda: print("click"))

            layout.addWidget(button)

    def init_fonts(self):
        font_title = self.window.title.font()
        font_search_line = self.window.search_line.font()

        set_font(self.window.title, font_path=FONT_BOLD_PATH, pointSize=font_title.pointSize(), weight=font_title.weight())
        set_font(self.window.search_line, font_path=FONT_REGULAR_PATH, pointSize=font_search_line.pointSize())

    @pyqtSlot()
    def search(self):
        query = self.window.search_line.text()
        for track_info in hitmo_parser.search(query):
            print(track_info)

    @staticmethod
    def add_shadow_to_title(title: QLabel):
        shadow = QGraphicsDropShadowEffect()

        shadow.setXOffset(0)
        shadow.setYOffset(4)

        shadow.setBlurRadius(4)
        shadow.setColor(QColor(0, 0, 0, 64))

        title.setGraphicsEffect(shadow)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
