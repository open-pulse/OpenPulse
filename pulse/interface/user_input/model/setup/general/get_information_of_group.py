from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

window_title_1 = "Error"
window_title_2 = "Warning"


class GetInformationOfGroup(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        uic.loadUi(UI_DIR / "model/info/get_group_information.ui", self)

        self.values = kwargs.get("values", "")
        self.label = kwargs.get("label", "")

        self.project = app().main_window.project

        self._initialize()
        self._load_icons()
        self._config_windows()
        self._define_qt_variables()
        self._create_connections()
        self.load_group_info()
        self.exec()

    def _initialize(self):
        self.lines_removed = False

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_windows(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):
        # QLineEdit
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')
        self.label_selected_id.setText("Line ID")
        # QPushButton
        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        self.lineEdit_selected_ID.setDisabled(True)
        # QTreeWidget
        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.headerItem().setText(0, self.label)
        self.treeWidget_group_info.headerItem().setText(1, "Capped end")
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_group_info.setColumnWidth(0, 80)
        self.treeWidget_group_info.setColumnWidth(1, 140)
        self.treeWidget_group_info.itemClicked.connect(self.on_click_item_)

    def _create_connections(self):
        self.pushButton_remove.clicked.connect(self.check_remove)
        self.pushButton_close.clicked.connect(self.force_to_close)

    def on_click_item_(self, item):
        text = item.text(0)
        self.lineEdit_selected_ID.setText(text)
        self.lineEdit_selected_ID.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def check_remove(self):
        if self.label == "Lines":
            if self.lineEdit_selected_ID.text() != "":
                line = int(self.lineEdit_selected_ID.text())
                if line in self.values:
                    self.values.remove(line)
                self.project.set_capped_end_by_lines(line, False)
                self.load_group_info()
                self.lines_removed = True
        self.lineEdit_selected_ID.setText("")

    def load_group_info(self):
        self.treeWidget_group_info.clear()
        for value in self.values:
            new = QTreeWidgetItem([str(value), "Enabled"])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)
        self.adjustSize()

    def force_to_close(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Delete:
            self.check_remove()