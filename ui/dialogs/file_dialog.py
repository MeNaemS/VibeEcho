from PySide6.QtWidgets import QFileDialog, QWidget
from PySide6.QtGui import QIcon
from config.config import AppConfig


class FileDialog(QFileDialog):
    def __init__(
        self,
        parent: QWidget,
        configs: AppConfig,
        title: str,
        mode: QFileDialog.FileMode,
        filter: str
    ):
        super().__init__(parent)
        self.setWindowIcon(QIcon(configs.app.icon_path))
        self.setWindowTitle(title)
        self.setFileMode(mode)
        self.setNameFilter(filter)
