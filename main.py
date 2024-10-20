import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QIcon, QFont, QFontDatabase


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MelodyHub")  # Устанавливаем заголовок окна
        self.setFixedSize(1000, 600)
        # self.setGeometry(100, 100, 700, 400)  # Устанавливаем размеры и позицию окна (x, y, width, height)
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
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]  # Получаем имя шрифта

        # Создаем центральный виджет и компоновщик
        # central_widget = QWidget()
        # main_layout = QVBoxLayout(central_widget)
        # center_layout = QHBoxLayout()

        '''Добавление текста 'MelodyHub'''
        self.label = QLabel('MelodyHub', self)
        self.label.setFont(QFont(font_family, 20, QFont.Weight.Bold))
        self.label.setStyleSheet("""
            color: #333333;
        """)
        self.label.setGeometry(430, 52, 140, 30)

        # # Устанавливаем отступы, чтобы переместить текст вверх
        # main_layout.addWidget(self.label,
        #                  alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)  # Выравнивание по верху и по центру
        # # Устанавливаем вертикальные отступы
        # main_layout.setContentsMargins(0, 20, 10, 0)  # (left, top, right, bottom)
        #
        # # Устанавливаем центральный виджет
        # self.setCentralWidget(central_widget)

        '''Добавление поисковой строки'''
        # Создание иконки поиска
        self.search_icon = QSvgWidget('icons/search.svg')  # Замените на путь к вашему файлу SVG
        self.search_icon.setFixedSize(25, 25)  # Установите размер иконки
        # self.search_icon.setStyleSheet("margin-right: 10px;")  # Отступ справа от иконки

        # Создание поисковой строки
        self.search_line = QLineEdit()
        self.search_line.setAlignment(Qt.AlignmentFlag.AlignCenter) # Установка выравнивания текста по центру
        self.search_line.setPlaceholderText("Поиск...")
        self.search_line.setStyleSheet("""
            QLineEdit {
                background-color: #E6E6FA;  /* Цвет фона */
                border: 2px solid #D3D3D3;   /* Цвет границы */
                border-radius: 10px;          /* Закругленные углы */
                padding: 10px;                /* Отступы */
                color: black;                  /* Цвет текста */
            }
            QLineEdit:focus {
                border: 2px solid #A0A0FF;    /* Цвет границы при фокусе */
            }
            QLineEdit::placeholder {
                color: #A0A0A0;                /* Цвет текста подсказки */
                font-style: italic;            /* Курсив для подсказки */
            }
        """)
        # Установка политики фокуса, чтобы строка поиска не была активной при старте
        self.search_line.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        # Установка политики размеров
        self.search_line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Добавление строки поиска в центральный layout
        # center_layout.addStretch()  # Добавление растягивающего пространства слева
        # center_layout.addWidget(self.search_icon)  # Добавление иконки поиска
        # center_layout.addWidget(self.search_line)  # Добавление поисковой строки
        # center_layout.addStretch()  # Добавление растягивающего пространства справа
        #
        # # Добавление центрального layout в основной
        # main_layout.addLayout(center_layout)  # Центрируем строку поиска
        # main_layout.addStretch()  # Добавление растягивающего пространства снизу, чтобы центровать по вертикали
        # # self.setLayout(main_layout) # (Просто ненужная строка)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем экземпляр приложения
    window = MainWindow()  # Создаем экземпляр главного окна
    window.show()  # Показываем главное окно
    sys.exit(app.exec())  # Запускаем главный цикл приложения
