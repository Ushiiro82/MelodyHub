from pathlib import Path
from typing import Union, Optional
from dataclasses import dataclass, field

from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QWidget

import os
from spleeter.separator import Separator


# Укажите путь к локальному FFmpeg
ffmpeg_path = r'D:\python projects\MelodyHub\ui\ffmpeg\ffmpeg-2024-12-19-git-494c961379-essentials_build\bin'
os.environ["PATH"] += os.pathsep + ffmpeg_path  # Добавляем путь к FFmpeg в PATH


FONT_DIRECTORY_PATH = "fonts"
FONT_BOLD_PATH = FONT_DIRECTORY_PATH / Path("Fira_Sans/FiraSans-Bold.ttf")
FONT_REGULAR_PATH = FONT_DIRECTORY_PATH / Path("Fira_Sans/FiraSans-Regular.ttf")

str_or_path = Union[Path, str]
direction = QPropertyAnimation.Direction


@dataclass
class TrackInfo:
    name: str
    artist: Optional[str] = field(default=None)
    time: Optional[str] = field(default=None)
    image_url: Optional[str] = field(default=None)
    download_link: Optional[str] = field(default=None)


def set_font(
        widget: QWidget,
        font_path: str_or_path = FONT_REGULAR_PATH,
        **q_font_kwargs
):
    if type(font_path) is not str:
        font_path = str(font_path)

    font_id = QFontDatabase.addApplicationFont(font_path)
    # Получаем имя шрифта
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    font = QFont(font_family, **q_font_kwargs)

    widget.setFont(font)


def start_backward_animation(animation: QPropertyAnimation):
    def finished():
        animation.setDirection(direction.Forward)
        animation.finished.disconnect(finished)

    animation.setDirection(direction.Backward)
    animation.finished.connect(finished)
    animation.start()


def separate_audio(file_path, output_dir='output'):
    """
    Загружает MP3 файл и разделяет его на дорожки.

    :param file_path: Путь к загружаемому MP3 файлу.
    :param output_dir: Папка для сохранения разделенных дорожек.
    """
    # Проверяем, существует ли файл
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    # Создаем выходную папку, если она не существует
    os.makedirs(output_dir, exist_ok=True)

    # Разделяем дорожки
    separator = Separator('spleeter:4stems')  # 4 дорожки: вокал, ударные, бас, другие
    separator.separate_to_file(file_path, output_dir)

    print(f"Файл {file_path} успешно разделен. Результаты сохранены в {output_dir}.")