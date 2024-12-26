from PyQt6 import QtCore, QtGui, QtWidgets, QtMultimedia
import os
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from utils import separate_audio
import shutil

class AudioSeparatorThread(QtCore.QThread):
    progress_updated = QtCore.pyqtSignal(int)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            # Пример разделения процесса на несколько этапов
            total_steps = 100  # Количество этапов
            for step in range(total_steps):
                # Имитация выполнения этапа
                self.msleep(15)  # Имитация задержки для демонстрации
                progress = int((step + 1) / total_steps * 100)
                self.progress_updated.emit(progress)  # Отправляем сигнал о прогрессе
                print(f"Progress updated to {progress}%")  # Логирование для отладки

            # Вызов функции для разделения аудио
            separate_audio(self.file_path)
            self.progress_updated.emit(100)  # Указываем, что процесс завершен
            print("Audio separation completed")  # Логирование для отладки
        except Exception as e:
            print(f"Ошибка при разделении аудио: {e}")
            self.progress_updated.emit(-1)  # Указываем, что произошла ошибка

class UiForm(object):
    # Константы для путей и стилей
    icons_path = os.path.join(os.path.dirname(__file__), '../icons')
    font_path = os.path.join(os.path.dirname(__file__), '../fonts/Fira_Sans/FiraSans-Bold.ttf')
    styles = {
        'button': """
            QPushButton {
                padding: 10px 37px 10px 40px;
                color: #333333;
                background: #D9D9D9;
                border: 1px solid #000000;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #C9C9C9;
            }
        """,
        'label': """
            QLabel {
                color: #333333;
                background: transparent;
            }
        """,
        'progress_bar': """
            QProgressBar {
                background: #D9D9D9;
                border: 1px solid #000000;
                border-radius: 10px;
            }
            QProgressBar::chunk {
                background: #767676;
                border-radius: 10px;
            }
        """,
        'wave_widget': """
            QWidget {
                background: #D9D9D9;
                border: 1px solid #000000;
                border-radius: 10px;
            }
        """,
        'play_button': """
            QPushButton {
                background: #D9D9D9;
                border: 1px solid #000000;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #C9C9C9;
            }
        """,
        'download_button': """
            QPushButton {
                background: #D9D9D9;
                border: 1px solid #000000;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #C9C9C9;
            }
        """
    }

    def __init__(self):
        self.player = QtMultimedia.QMediaPlayer()
        self.audioOutput = QtMultimedia.QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)

    def setup_ui(self, form):
        # Загрузка шрифта
        font_id = QtGui.QFontDatabase.addApplicationFont(self.font_path)
        if font_id == -1:
            print("Failed to load font")
            return
        font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        if not font_families:
            print("No font families found")
            return
        font_family = font_families[0]

        # Настройка основных параметров формы
        form.setObjectName("form")
        form.resize(904, 670)
        form.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(40)
        form.setFont(font)
        form.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        form.setWindowTitle("Spleeter")

        # Установка иконки окна
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.icons_path, 'music_note.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        form.setWindowIcon(icon)

        # Установка стиля фона
        form.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
                          "stop: 0 rgba(167, 198, 237, 255),\n"
                          "stop: 1 rgba(111, 163, 239, 255));")

        # Создание вертикального layout для формы
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(form)
        self.vertical_layout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.vertical_layout_2.setObjectName("vertical_layout_2")

        # Создание горизонтального layout для верхней части формы
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2.setContentsMargins(30, -1, -1, -1)
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")

        # Создание кнопки загрузки файлов
        self.create_upload_button(self.horizontal_layout_2)
        # Создание заголовка
        self.create_title_label(self.horizontal_layout_2)
        # Добавление горизонтального layout в вертикальный layout
        self.vertical_layout_2.addLayout(self.horizontal_layout_2)

        # Добавление промежутка между элементами
        self.vertical_layout_2.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed))

        # Создание горизонтального layout для центральной части формы
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setContentsMargins(30, 0, 30, -1)
        self.horizontal_layout.setSpacing(20)
        self.horizontal_layout.setObjectName("horizontal_layout")

        # Создание метки ожидания результата
        self.create_waiting_label(self.horizontal_layout)
        # Создание progress bar
        self.create_progress_bar(self.horizontal_layout)
        # Добавление горизонтального layout в вертикальный layout
        self.vertical_layout_2.addLayout(self.horizontal_layout)

        # Добавление промежутка между элементами
        self.vertical_layout_2.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed))

        # Создание вертикального layout для нижней части формы
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setContentsMargins(30, -1, 30, 0)
        self.vertical_layout.setSpacing(30)
        self.vertical_layout.setObjectName("vertical_layout")

        # Создание layout для волновых виджетов
        self.create_wave_layouts(self.vertical_layout)
        # Добавление вертикального layout в основной вертикальный layout
        self.vertical_layout_2.addLayout(self.vertical_layout)

        # Перевод текста на форме
        self.retranslate_ui(form)
        # Подключение слотов к сигналам
        QtCore.QMetaObject.connectSlotsByName(form)

    def open_file_dialog(self):
        # Открытие файлового менеджера и выбор MP3 файла
        file_dialog = QtWidgets.QFileDialog(form)
        file_dialog.setNameFilter("MP3 Files (*.mp3)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                # Обработка выбранного файла
                print(f"Выбран файл: {selected_files[0]}")
                # Создание и запуск потока для разделения аудио
                self.audio_separator_thread = AudioSeparatorThread(selected_files[0])
                self.audio_separator_thread.progress_updated.connect(self.update_progress)
                self.audio_separator_thread.finished.connect(lambda: self.load_audio_waves(selected_files[0]))
                self.audio_separator_thread.start()

    def load_audio_waves(self, file_path):
        # Загрузка и отображение аудио волн
        base_name = os.path.basename(file_path).split('.')[0]
        output_dir = os.path.join(os.path.dirname(__file__), 'output', base_name)
        tracks = ['vocals.wav', 'drums.wav', 'bass.wav', 'other.wav']

        for i, track in enumerate(tracks):
            track_path = os.path.join(output_dir, track)
            if os.path.exists(track_path):
                print(f"Loading track: {track_path}")  # Логирование для отладки
                audio = AudioSegment.from_wav(track_path)
                samples = audio.get_array_of_samples()
                self.plot_waveform(samples, self.wave_widgets[i])
                self.wave_widgets[i].samples = samples  # Сохраняем образцы для воспроизведения
                self.wave_widgets[i].track_path = track_path  # Сохраняем путь к треку для воспроизведения
            else:
                print(f"Track not found: {track_path}")  # Логирование для отладки

    def plot_waveform(self, samples, widget):
        # Отображение аудио волны на виджете
        plt.figure(figsize=(widget.width() / 100, widget.height() / 100), dpi=100)
        plt.plot(samples)
        plt.axis('off')
        plt.savefig('temp_wave.png')
        plt.close()

        pixmap = QtGui.QPixmap('../img/temp_wave.png')
        label = QtWidgets.QLabel(widget)
        label.setPixmap(pixmap)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(label)
        widget.setLayout(layout)

    def play_audio(self, track_path):
        # Воспроизведение аудио
        self.player.stop()
        self.player.setSource(QtCore.QUrl.fromLocalFile(track_path))
        self.player.play()

    def download_audio(self, track_path):
        # Открытие файлового менеджера для сохранения файла
        file_dialog = QtWidgets.QFileDialog(form)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("WAV Files (*.wav)")
        file_dialog.setDefaultSuffix("wav")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            if selected_file:
                # Копирование файла в выбранное место
                shutil.copyfile(track_path, selected_file)
                print(f"Файл сохранен: {selected_file}")

    def update_progress(self, value):
        if value == 100:
            self.waiting_res.setText("Разделение завершено!")
        elif value == -1:
            self.waiting_res.setText("Ошибка при разделении аудио.")
        else:
            self.progress_bar.setValue(value)
            self.waiting_res.setText(f"Разделение завершено на {value}%")

    def create_upload_button(self, layout):
        # Создание кнопки загрузки файлов
        self.drug_files = QtWidgets.QPushButton(parent=form)
        self.drug_files.setEnabled(True)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        self.drug_files.setSizePolicy(size_policy)
        font = QtGui.QFont(self.drug_files.font())
        font.setPointSize(20)
        font.setBold(True)
        self.drug_files.setFont(font)
        self.drug_files.setStyleSheet(self.styles['button'])
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(self.icons_path, 'folder_open.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.drug_files.setIcon(icon1)
        self.drug_files.setIconSize(QtCore.QSize(40, 40))
        self.drug_files.setObjectName("drug_files")
        self.drug_files.clicked.connect(self.open_file_dialog)  # Подключение слота к сигналу
        layout.addWidget(self.drug_files)

    def create_title_label(self, layout):
        # Создание заголовка
        self.title = QtWidgets.QLabel(parent=form)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.title.setSizePolicy(size_policy)
        font = QtGui.QFont(self.title.font())
        font.setFamily("Fira Sans")
        font.setPointSize(64)
        font.setBold(True)
        font.setItalic(False)
        self.title.setFont(font)
        self.title.setStyleSheet(self.styles['label'])
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")

        # Добавление тени к заголовку
        shadow = QtWidgets.QGraphicsDropShadowEffect(self.title)
        shadow.setBlurRadius(10)
        shadow.setOffset(5, 5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 128))
        self.title.setGraphicsEffect(shadow)

        layout.addWidget(self.title)

    def create_waiting_label(self, layout):
        # Создание метки ожидания результата
        self.waiting_res = QtWidgets.QLabel(parent=form)
        font = QtGui.QFont(self.waiting_res.font())
        font.setFamily("Fira Sans")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        self.waiting_res.setFont(font)
        self.waiting_res.setStyleSheet(self.styles['label'])
        self.waiting_res.setObjectName("waiting_res")
        layout.addWidget(self.waiting_res)

    def create_progress_bar(self, layout):
        # Создание progress bar
        self.progress_bar = QtWidgets.QProgressBar(parent=form)
        self.progress_bar.setStyleSheet(self.styles['progress_bar'])
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        layout.addWidget(self.progress_bar)

    def create_wave_layouts(self, parent_layout):
        # Создание layout для волновых виджетов
        self.wave_widgets = []
        wave_names = ["wave1", "wave2", "wave3", "wave4"]
        play_names = ["play1", "play2", "play3", "play4"]
        download_names = ["download1", "download2", "download3", "pushButton_9"]

        for wave_name, play_name, download_name in zip(wave_names, play_names, download_names):
            wave_widget = self.create_wave_layout(parent_layout, wave_name, play_name, download_name)
            self.wave_widgets.append(wave_widget)

    def create_wave_layout(self, parent_layout, wave_name, play_name, download_name):
        # Создание горизонтального layout для волнового виджета
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setContentsMargins(-1, -1, -1, 0)
        horizontal_layout.setSpacing(10)
        horizontal_layout.setObjectName(f"horizontal_layout_{wave_name}")

        # Создание волнового виджета
        wave = QtWidgets.QWidget(parent=form)
        wave.setMinimumSize(QtCore.QSize(0, 43))
        wave.setStyleSheet(self.styles['wave_widget'])
        wave.setObjectName(wave_name)
        horizontal_layout.addWidget(wave)

        # Создание кнопки воспроизведения
        play = QtWidgets.QPushButton(parent=form)
        play.setMinimumSize(QtCore.QSize(0, 43))
        play.setStyleSheet(self.styles['play_button'])
        play.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(self.icons_path, 'play.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        play.setIcon(icon2)
        play.setIconSize(QtCore.QSize(50, 50))
        play.setObjectName(play_name)
        play.clicked.connect(lambda: self.play_audio(wave.track_path))  # Подключение слота к сигналу
        horizontal_layout.addWidget(play)

        # Создание кнопки загрузки
        download = QtWidgets.QPushButton(parent=form)
        download.setMinimumSize(QtCore.QSize(0, 43))
        download.setStyleSheet(self.styles['download_button'])
        download.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(self.icons_path, 'download.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        download.setIcon(icon3)
        download.setIconSize(QtCore.QSize(50, 50))
        download.setObjectName(download_name)
        download.clicked.connect(lambda: self.download_audio(wave.track_path))  # Подключение слота к сигналу
        horizontal_layout.addWidget(download)

        # Установка растяжения для волнового виджета
        horizontal_layout.setStretch(0, 4)
        # Добавление горизонтального layout в родительский layout
        parent_layout.addLayout(horizontal_layout)

        return wave

    def retranslate_ui(self, form):
        # Перевод текста на форме
        _translate = QtCore.QCoreApplication.translate
        self.drug_files.setText(_translate("form", "Upload Files"))
        self.title.setText(_translate("form", "Spleeter"))
        self.waiting_res.setText(_translate("form", "Ожидание результата..."))

    def clean_output_directory(self):
        # Очистка папки output
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            print(f"Output directory cleaned: {output_dir}")
        else:
            print(f"Output directory not found: {output_dir}")

    def resize_wave_widget(self, widget):
        # Обновление отображения аудио волны при изменении размера виджета
        if hasattr(widget, 'samples'):
            self.plot_waveform(widget.samples, widget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = UiForm()
    ui.setup_ui(form)
    form.show()

    # Подключение функции очистки к сигналу aboutToQuit
    app.aboutToQuit.connect(ui.clean_output_directory)

    # Подключение функции resize_wave_widget к сигналу resize для каждого волнового виджета
    for wave_widget in ui.wave_widgets:
        wave_widget.resizeEvent = lambda event, widget=wave_widget: ui.resize_wave_widget(widget)

    sys.exit(app.exec())
