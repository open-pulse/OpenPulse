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

        self.group_label = kwargs.get("group_label", "")
        self.selection_label = kwargs.get("selection_label", "")
        self.header_label_left = kwargs.get("header_label_left", "")
        self.header_label_right = kwargs.get("header_label_right", "")
        self.remove_button = kwargs.get("remove_button", False)
        self.data = kwargs.get("data", dict())
        self.values = kwargs.get("values", "")

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
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        # QLabel
        self.label_selected_id : QLabel
        self.label_selected_id.setText(self.selection_label)
        # QLineEdit
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_selected_id.setDisabled(True)
        # QPushButton
        self.pushButton_close : QPushButton
        self.pushButton_remove : QPushButton
        if not self.remove_button:
            self.pushButton_remove.setDisabled(True)
        # QTreeWidget
        self.treeWidget_group_info : QTreeWidget
        self._config_treeWidget()        

    def _config_treeWidget(self):
        self.treeWidget_group_info.headerItem().setText(0, self.header_label_left)
        self.treeWidget_group_info.headerItem().setText(1, self.header_label_right)
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_group_info.setColumnWidth(0, 80)
        self.treeWidget_group_info.setColumnWidth(1, 140)

    def _create_connections(self):
        self.pushButton_remove.clicked.connect(self.check_remove)
        self.pushButton_close.clicked.connect(self.close)
        self.treeWidget_group_info.itemClicked.connect(self.on_click_item_)

    def on_click_item_(self, item):
        text = item.text(0)
        self.lineEdit_selected_id.setText(text)
        self.lineEdit_selected_id.setDisabled(True)
        if self.remove_button:
            self.pushButton_remove.setDisabled(False)
        else:
            self.pushButton_remove.setDisabled(True)

    def check_remove(self):
        if self.group_label == "Capped end":
            if self.lineEdit_selected_id.text() != "":
                line = int(self.lineEdit_selected_id.text())
                if line in self.values:
                    self.values.remove(line)
                self.project.set_capped_end_by_lines(line, False)
                self.load_group_info()
                self.lines_removed = True
        self.lineEdit_selected_id.setText("")

    def load_group_info(self):
        self.treeWidget_group_info.clear()
        for key, value in self.data.items():
            new = QTreeWidgetItem([str(key), str(value)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)
        self.adjustSize()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Delete:
            self.check_remove()