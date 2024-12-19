import webbrowser

from PyQt6.QtCore import Qt, QPropertyAnimation, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy

from utils import set_font, FONT_REGULAR_PATH


class TrackButton(QPushButton):
    def __init__(self, album_image: str, artist: str, track_name: str, download_url: str):
        super().__init__()

        # Установка стиля кнопки
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setMinimumSize(QSize(200, 50))
        self.setStyleSheet("""
            TrackButton {
                border: 1px solid black;
                border-radius: 10px;
                background-color: white; 
            }
        """)

        # Создание виджетов для информации о треке
        # self.album_image_label = QLabel()
        # self.album_image_label.setPixmap(QPixmap(album_image).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))

        self.artist_label = QLabel(artist)
        self.track_name_label = QLabel(track_name)

        set_font(self.artist_label, pointSize=8)
        set_font(self.track_name_label, pointSize=12)

        # Создание кнопки для скачивания
        self.download_button = QPushButton("Скачать")
        self.download_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.download_button.clicked.connect(lambda: webbrowser.open(download_url))

        # Создание компоновки для размещения элементов
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.track_name_label)
        info_layout.addWidget(self.artist_label)

        main_layout = QHBoxLayout()
        # main_layout.addWidget(self.album_image_label)
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.download_button)

        # Установка компоновки в кнопку
        self.setLayout(main_layout)