import os
import webbrowser

from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QWidget

from utils import set_font, FONT_REGULAR_PATH


class TrackButton(QPushButton):
    def __init__(self, album_image: str, artist: str, track_name: str, download_url: str):
        super().__init__()

        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_image_load)

        # Установка стиля кнопки
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(60)

        # Создание виджетов для информации о треке
        self.album_image_label = QLabel()

        self.artist_label = QLabel(artist)
        self.track_name_label = QLabel(track_name)

        set_font(self.artist_label, pointSize=8)
        set_font(self.track_name_label, pointSize=12)

        # Создание кнопки для скачивания
        self.download_button = QPushButton("")
        icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", 'download.svg')
        icon = QIcon()
        icon.addPixmap(
            QPixmap(icon_path),
            QIcon.Mode.Normal,
            QIcon.State.Off
        )
        self.download_button.setIcon(icon)
        self.download_button.setStyleSheet("""
            QPushButton {
                background: #D9D9D9;
                border: 1px solid #000000;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #C9C9C9;
            }
        """)
        self.download_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.download_button.clicked.connect(lambda: webbrowser.open(download_url))
        self.download_button.setIconSize(QSize(50, 50))
        # Создание компоновки для размещения элементов
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.track_name_label)
        info_layout.addWidget(self.artist_label)

        left_layout = QHBoxLayout()
        left_layout.addWidget(self.album_image_label)
        left_layout.addLayout(info_layout)
        # left_layout.setSpacing(0)
        # left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.download_button)

        self.setStyleSheet("""
            TrackButton {
                border: 1px solid black;
                border-radius: 10px;
                background-color: white; 
            }
        """)

        # Установка компоновки в кнопку
        self.setLayout(main_layout)

        request = QNetworkRequest(QUrl(album_image))
        self.network_manager.get(request)

    def on_image_load(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            image_data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.album_image_label.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            print("Ошибка загрузки изображения:", reply.errorString())
