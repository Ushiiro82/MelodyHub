from PyQt6.QtCore import Qt, QPropertyAnimation, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem

from utils import str_or_path, set_font, FONT_BOLD_PATH, start_backward_animation


class MenuButton(QPushButton):
    def __init__(self, text: str, icon_path: str_or_path, image_path: str_or_path):
        super().__init__(text)
        self._size = QSize(180, 180)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setMinimumSize(self._size)
        self.setStyleSheet("""
            MenuButton {
                border: 2px solid black;
                border-radius: 20px;
                background-color: white; border-radius: 20px;
            }
        """)

        self.init_layout(text, icon_path, image_path)

        self.hover_animation = QPropertyAnimation(self, b"size")
        self.press_animation = QPropertyAnimation(self, b"size")

        self.init_animations()

    def init_animations(self):
        size_offset = QSize(10, 10)

        self.hover_animation.setDuration(200)
        self.hover_animation.setStartValue(self._size)
        self.hover_animation.setEndValue(self._size + size_offset)

        # self.press_animation.setDuration(100)
        # self.press_animation.setStartValue(self._size)
        # self.press_animation.setEndValue(self._size + size_offset)

    def init_layout(self, text: str, icon_path: str_or_path, image_path: str_or_path):
        if type(icon_path) is not str:
            icon_path = str(icon_path)

        if type(image_path) is not str:
            image_path = str(image_path)

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
        # image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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
        text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        text_label.setContentsMargins(5, 0, 0, 0)
        set_font(text_label, FONT_BOLD_PATH, weight=700, pointSize=10)

        label_layout.addWidget(icon_label)
        label_layout.addWidget(text_label)

        return label_layout

    def enterEvent(self, event):
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        start_backward_animation(self.hover_animation)
        super().leaveEvent(event)

    # def mousePressEvent(self, event):
    #     self.press_animation.start()
    #     super().mousePressEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     self.press_animation.setDirection(QPropertyAnimation.Direction.Backward)
    #     self.press_animation.start()
    #     super().mouseReleaseEvent(event)
