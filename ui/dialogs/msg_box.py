from typing import Literal
from PySide6.QtWidgets import QDialog, QWidget, QGridLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt
from config.config import AppConfig


class MessageBox(QDialog):
    def __init__(
        self,
        parent: QWidget,
        configs: AppConfig,
        message: Literal["error", "warning", "information"],
        informative_text: str,
    ):
        super().__init__(parent)

        self.configs: AppConfig = configs

        self.icon: QLabel = QLabel("", self)
        self.message: QLabel = QLabel(f"<h1>{message.capitalize()}</h1>", self)
        self.informative_text: QLabel = QLabel(f"<center>{informative_text}</center>", self)
        self.ok_button: QPushButton = QPushButton("Ok", self)
        self.reject_button: QPushButton = QPushButton("Cancel", self)

        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(self.configs.app.icon_path))
        self.setWindowTitle(self.configs.app.name)
        self.setFixedSize(*self.configs.app.dialog.size)

        self.icon.setPixmap(QPixmap(self.search_image_by_message()))
        self.informative_text.setFont(QFont("Arial", 10, 2))
        self.informative_text.setWordWrap(True)
        self.informative_text.setTextFormat(Qt.TextFormat.AutoText)
        self.ok_button.setMinimumWidth(110)
        self.ok_button.clicked.connect(self.accept)
        self.reject_button.setMinimumWidth(110)
        self.reject_button.clicked.connect(self.reject)

        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(self.icon, 0, 0, 3, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message, 0, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.informative_text, 1, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.reject_button, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.ok_button, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def search_image_by_message(self) -> str:
        match self.message.text():
            case "<h1>Error</h1>":
                return self.configs.app.dialog.error_image_path
            case "<h1>Warning</h1>":
                return self.configs.app.dialog.warning_image_path
            case "<h1>Information</h1>":
                return self.configs.app.dialog.info_image_path
