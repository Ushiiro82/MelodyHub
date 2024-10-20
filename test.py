import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt6.QtGui import QFont, QIcon, QFontDatabase
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MelodyHub")
        self.setFixedSize(1000, 600)
        self.setWindowIcon(QIcon("icons/music_note.svg"))
        # Установка градиентного фона
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(167, 198, 237, 255), 
                    stop: 1 rgba(111, 163, 239, 255));
            }
        """)

        ''' Загрузка пользовательского шрифта'''
        font_id = QFontDatabase.addApplicationFont(
            "Fonts/Fira_Sans/FiraSans-Bold.ttf"
        )
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # Установка основного виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Заголовок
        title_label = QLabel("MelodyHub")
        title_label.setFont(QFont(font_family, 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            color: #333333;
        """)
        # title_label.setGeometry(430, 52, 140, 30)

        # Поле поиска
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Поиск...")

        # Горизонтальный Layout для кнопок
        button_layout = QHBoxLayout()

        # Кнопка "Актуальные жанры"
        genres_button = QPushButton("Актуальные жанры")
        genres_button.setIcon(QIcon("path/to/genres_icon.png"))  # Укажите путь к иконке
        button_layout.addWidget(genres_button)

        # Кнопка "Актуальные плагины"
        plugins_button = QPushButton("Актуальные плагины")
        plugins_button.setIcon(QIcon("path/to/plugins_icon.png"))  # Укажите путь к иконке
        button_layout.addWidget(plugins_button)

        # Кнопка "Сплиттер mp3"
        splitter_button = QPushButton("Сплиттер mp3")
        splitter_button.setIcon(QIcon("path/to/splitter_icon.png"))  # Укажите путь к иконке
        button_layout.addWidget(splitter_button)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())