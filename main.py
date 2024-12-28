import sys
from pprint import pprint
from typing import Callable

from PyQt6.QtCore import QPropertyAnimation, QSize, QObject, pyqtSlot, pyqtSignal, QThread
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor

from pathlib import Path

from ui.menu_button import MenuButton
from ui.track_button import TrackButton
from ui.main_window import Ui_MainWindow
from ui.search_result_window import Ui_SearchResultWindow
from utils import set_font, FONT_REGULAR_PATH, FONT_BOLD_PATH, start_backward_animation, TrackInfo

import parsing.hitmo_parser as hitmo_parser


class ParserThread(QThread):
    finished = pyqtSignal()
    found = pyqtSignal(TrackInfo)

    def run(self):
        query = self.parent().search_line.text()

        for music in hitmo_parser.search(query):
            self.found.emit(music)

        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_window = Ui_MainWindow()
        self.window_search_result = Ui_SearchResultWindow()

        self.main_window.setupUi(self)

        self.search_line = self.main_window.search_line

        self.parser_thread = ParserThread(self)

        self.setMinimumSize(500, 500)

        self.search_line_focus_animation = QPropertyAnimation(self.main_window.search_line, b"size")

        self.add_shadow_to_title(self.main_window.title)

        self.init_fonts()
        self.init_buttons()
        # self.init_animations()
        self.init_events()
        self.init_parser_signals()

    def init_parser_signals(self):
        self.parser_thread.finished.connect(self._finished_parser)
        self.parser_thread.found.connect(self.add_track_to_results)

    def add_track_to_results(self, music: TrackInfo):
        track_button = TrackButton(music.image_url, music.artist, music.name, music.download_link)
        self.window_search_result.list_search_result.widget().layout().addWidget(track_button)

    def _finished_parser(self):
        self.search_line.setDisabled(False)
        self.search_line.returnPressed.connect(self.open_search_result_window)

    def _open(self):
        self.show()

    def open_search_result_window(self):
        query = self.search_line.text()

        self.window_search_result.setupUi(self)

        self.search_line = self.window_search_result.search_line

        self.search_line.setText(query)
        self.search_line.setDisabled(True)

        self.parser_thread.start()

        self._open()

    def init_events(self):
        self.search_line.returnPressed.connect(self.open_search_result_window)

    def init_animations(self):
        self.main_window.search_line.focusInEvent = lambda _: self.search_line_focus_animation.start()
        self.main_window.search_line.focusOutEvent = lambda _: start_backward_animation(self.search_line_focus_animation)

        self.search_line_focus_animation.setDuration(200)
        self.search_line_focus_animation.setStartValue(self.main_window.search_line.size())
        self.search_line_focus_animation.setEndValue(self.main_window.search_line.size() + QSize(10, 10))

    def init_buttons(self):
        layout = self.main_window.horizontalLayout
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
        font_title = self.main_window.title.font()
        font_search_line = self.main_window.search_line.font()

        set_font(self.main_window.title, font_path=FONT_BOLD_PATH, pointSize=font_title.pointSize(), weight=font_title.weight())
        set_font(self.main_window.search_line, font_path=FONT_REGULAR_PATH, pointSize=font_search_line.pointSize())

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
