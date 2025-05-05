from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from pulse import app, UI_DIR

from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"


class GetInformationOfGroup(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/info/get_group_information.ui"
        load_ui(ui_path, self, UI_DIR)

        self.group_label = kwargs.get("group_label", "")
        self.selection_label = kwargs.get("selection_label", "")
        self.header_labels = kwargs.get("header_labels", list())
        self.column_widths = kwargs.get("column_widths", list())
        self.remove_button = kwargs.get("remove_button", False)
        self.data = kwargs.get("data", dict())

        self.values = kwargs.get("values", "")

        self.project = app().main_window.project

        self._initialize()
        self._config_windows()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_group_info()
        self.exec()

    def _initialize(self):
        self.lines_removed = False

    def _config_windows(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLabel
        self.label_selected_id : QLabel

        # QLineEdit
        self.lineEdit_selected_id : QLineEdit

        # QPushButton
        self.pushButton_close : QPushButton
        self.pushButton_remove : QPushButton

        # QTreeWidget
        self.treeWidget_group_info : QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_remove.clicked.connect(self.check_remove)
        self.pushButton_close.clicked.connect(self.close)
        #
        self.treeWidget_group_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_group_info.itemDoubleClicked.connect(self.on_double_click_item)

    def _config_widgets(self):

        self.label_selected_id.setText(self.selection_label)
        self.lineEdit_selected_id.setDisabled(True)

        if not self.remove_button:
            self.pushButton_remove.setDisabled(True)

        for col, label in enumerate(self.header_labels):
            self.treeWidget_group_info.headerItem().setText(col, label)
            self.treeWidget_group_info.headerItem().setTextAlignment(col, Qt.AlignCenter)
            if len(self.column_widths):
                self.treeWidget_group_info.setColumnWidth(col, self.column_widths[col])

    def on_click_item(self, item):
        text = item.text(0)
        if text != "":
            self.lineEdit_selected_id.setText(text)
            self.lineEdit_selected_id.setDisabled(True)
            if self.remove_button:
                self.pushButton_remove.setDisabled(False)
            else:
                self.pushButton_remove.setDisabled(True)

    def on_double_click_item(self, item):
        text = item.text(0)
        if text != "":
            try:
                self.process_highlights(selection=[int(text)])
                self.lineEdit_selected_id.setText(text)
                self.lineEdit_selected_id.setDisabled(True)
                if self.remove_button:
                    self.pushButton_remove.setDisabled(False)
                else:
                    self.pushButton_remove.setDisabled(True)
            except:
                pass

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
        for keys, values in self.data.items():

            if isinstance(keys, (int, float, complex)):
                keys = [keys]

            if isinstance(values, (int, float, complex)):
                values = [values]

            item_info = list()
            for key in keys:
                item_info.append(str(key))

            if isinstance(values, str):
                item_info.append(values)
            else:
                for value in values:
                    item_info.append(str(value))

            new = QTreeWidgetItem(item_info)
            for col in range(len(item_info)):
                new.setTextAlignment(col, Qt.AlignCenter)

            self.treeWidget_group_info.addTopLevelItem(new)

        self.process_highlights()
        self.adjustSize()

    def process_highlights(self, selection=None):
        
        if selection is None:
            selection = list()
            for key in self.data.keys():
                if key not in selection:
                    if isinstance(key, int):
                        selection.append(key)
                    else:
                        selection.append(key[0])

        if isinstance(selection, list):
            if "Line" in self.selection_label:
                app().main_window.set_selection(lines = selection)

            elif "Element" in self.selection_label:
                app().main_window.set_selection(elements = selection)

            elif "Node" in self.selection_label:
                app().main_window.set_selection(nodes = selection)

            else:
                return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Delete:
            self.check_remove()