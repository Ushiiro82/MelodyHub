from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel

from utils import str_or_path, set_font, FONT_REGULAR_PATH, FONT_BOLD_PATH


class MenuButton(QPushButton):
    def __init__(self, text: str, icon_path: str_or_path, image_path: str_or_path):
        super().__init__(text)

        if type(icon_path) is not str:
            icon_path = str(icon_path)

        if type(image_path) is not str:
            image_path = str(image_path)

        self.setFixedSize(180, 180)
        self.setStyleSheet("""
            MenuButton {
                border: 2px solid black;
                border-radius: 20px;
                background-color: white; border-radius: 20px;
            }
        """)

        label_layout = self.get_label_layout(text, icon_path)
        image = self.get_image(image_path)

        # Создаем вертикальный layout
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        layout.addLayout(label_layout)
        layout.addWidget(image)

        self.setLayout(layout)

    @staticmethod
    def get_image(image_path: str):
        image_label = QLabel()
        image_label.setPixmap(QPixmap(image_path))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return image_label

    @staticmethod
    def get_label_layout(text: str, icon_path: str):
        # Создаем общий layout для иконки и текстовой метки
        label_layout = QHBoxLayout()
        label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создаем иконку
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создаем текстовую метку
        text_label = QLabel(text)
        set_font(text_label, FONT_BOLD_PATH, weight=700, pointSize=10)
        text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        text_label.setContentsMargins(5, 0, 0, 0)

        label_layout.addWidget(icon_label)
        label_layout.addWidget(text_label)

        return label_layout
