from PySide6.QtWidgets import QMainWindow, QGridLayout, QLabel, QPushButton, QSlider, QFileDialog, QWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon
from adaptix import Retort
from logging import Logger
from sys import exit
from config.config import AppConfig
from services.song import SongService
from ui.dialogs.msg_box import MessageBox
from ui.dialogs.file_dialog import FileDialog
from core.domain.song import Song


class MainWindow(QMainWindow):
    def __init__(
        self,
        configs: AppConfig,
        retort: Retort,
        logger: Logger,
        song_service: SongService
    ):
        super().__init__()

        self.configs: AppConfig = configs
        self.retort: Retort = retort
        self.logger: Logger = logger
        self.music_file_path: str = self.get_music_path()

        self.choose_file: QPushButton = QPushButton("Choose music file", self)
        self.audio_output: QMediaPlayer = QMediaPlayer(self)
        self.audio_device: QAudioOutput = QAudioOutput(self)
        self.slider: QSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.controle: QPushButton = QPushButton("▶️", self)
        self.image: QLabel = QLabel("", self)

        song_data: Song = song_service.load_song(self.music_file_path)
        self.name: QLabel = QLabel(song_data.title, self)
        self.duration: QLabel = QLabel(str(song_data.duration), self)

        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowIcon(QIcon(self.configs.app.icon_path))
        self.setWindowTitle(self.configs.app.name)
        self.setFixedSize(*self.configs.app.size)

        self.audio_output.setAudioOutput(self.audio_device)
        self.audio_output.setSource(QUrl.fromLocalFile(self.music_file_path))

        self.choose_file.clicked.connect(self.set_music)
        self.controle.clicked.connect(self.play_audio)
        self.slider.setMinimumWidth(300)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.seek_position)
        self.audio_output.positionChanged.connect(self.update_slider)
        self.audio_output.durationChanged.connect(self.set_duration)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout: QGridLayout = QGridLayout(central_widget)
        layout.addWidget(self.choose_file, 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.image, 1, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        controller_layout: QGridLayout = QGridLayout()
        controller_layout.addWidget(self.name, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        controller_layout.addWidget(self.duration, 1, 0, 1, 3, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        controller_layout.addWidget(self.slider, 2, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        controller_layout.addWidget(self.controle, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(controller_layout, 2, 0, 1, 3)
        self.setLayout(layout)


    def show_error_dialog(self):
        msg_box: MessageBox = MessageBox(
            self,
            self.configs,
            "warning",
            "You have not selected a file with music"
        )
        return msg_box.exec()


    def get_music_path(self) -> str:
        result: FileDialog = FileDialog(
            self,
            self.configs,
            "Select a file with music: ",
            QFileDialog.FileMode.ExistingFile,
            "Audio Files (*.mp3 *.wav *.ogg)"
        )
        if not result.exec():
            if not self.show_error_dialog():
                exit(0)
            return self.get_music_path()
        return result.selectedFiles()[0]

    def set_music(self) -> None:
        self.music_file_path = self.get_music_path()
        self.audio_output.setSource(QUrl.fromLocalFile(self.music_file_path))

    def seek_position(self, value):
        if self.audio_output.duration() > 0:
            new_position = int((value / 100) * self.audio_output.duration())
            self.audio_output.setPosition(new_position)

    def play_audio(self):
        if self.audio_output.isPlaying():
            self.audio_output.stop()
        else:
            self.audio_output.play()

    def update_slider(self, position):
        if self.audio_output.duration() > 0:
            value = (position / self.audio_output.duration()) * 100
            self.slider.setValue(int(value))

    def set_duration(self, duration):
        self.duration = duration
