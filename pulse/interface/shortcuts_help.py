from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from pulse import app
from pulse.interface.shortcuts import SHORTCUTS


class ShortcutsHelp(QDialog):
    """Modal dialog listing every key sequence of the SHORTCUTS registry."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._config_window()
        self._create_widgets()
        self._create_layout()
        self._config_widgets()

        self.exec()

    def _config_window(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Keyboard Shortcuts")

    def _create_widgets(self):
        self.label = QLabel("Shortcuts List")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.table = QTableWidget(len(SHORTCUTS), 2, self)
        self.table.setHorizontalHeaderLabels(["Shortcut", "Description"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        for row, (keys, (target, description)) in enumerate(SHORTCUTS.items()):
            self.table.setItem(row, 0, QTableWidgetItem(keys))
            self.table.setItem(row, 1, QTableWidgetItem(description))

        self.pushButton_close = QPushButton("Close")
        self.pushButton_close.clicked.connect(self.close)

    def _create_layout(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.pushButton_close)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)

    def _config_widgets(self):
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        vertical_header = self.table.verticalHeader()
        vertical_header.setDefaultSectionSize(26)
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.adjustSize()
        self.resize(max(self.width(), 500), max(self.height(), 700))
