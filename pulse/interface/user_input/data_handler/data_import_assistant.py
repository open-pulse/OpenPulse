from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QTreeWidgetItem, QWidget
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.data_handler.data_import_assistant_ui import DataImportAssistant_UI
from pulse.interface.user_input.data_handler.file_dialog_service import FileDialogService
from pulse.interface.user_input.data_handler.imported_data import ImportedData, SpreadsheetData, SpreadsheetSheet
from pulse.interface.user_input.data_handler.file_handlers.file_handler import FileHandler

import numpy as np


class DataImportAssistant(DataImportAssistant_UI):
    
    def __init__(self, plotter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plotter = plotter

        self.main_window = app().main_window

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        
    def _config_window(self):    
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True
        self.imported_data = None
        self.imported_paths: list = list()

        self.imported_results: dict[int, ImportedData] = dict()
        self.ids_to_checkBox = dict()
        self.checkButtons_state = dict()

        self.colors = [ [0,0,0],
                        [1,0,0],
                        [1,0,1],
                        [0,1,1],
                        [0.75,0.75,0.75],
                        [0.5, 0.5, 0.5],
                        [0.25, 0.25, 0.25] ]

    def _define_qt_variables(self):
        self.lineEdit_import_results_path.setDisabled(True)

    def _create_connections(self):
        #
        self.checkBox_skiprows.clicked.connect(self.update_skiprows_visibility)
        #
        self.pushButton_search_file_to_import.clicked.connect(self.import_results)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_reset_imported_data.clicked.connect(self.reset_imported_data)
        self.pushButton_add_imported_data_to_plot.clicked.connect(self.add_imported_data_to_plot)
        #
        self.update_skiprows_visibility()
        
    def _config_widgets(self):

        widths_1 = [320, 60]
        for i, width in enumerate(widths_1):
            self.treeWidget_import_text_files.setColumnWidth(i, width)

        widths_2 = [180, 180, 60]
        for i, width in enumerate(widths_2):
            self.treeWidget_import_sheet_files.setColumnWidth(i, width)

    def update_skiprows_visibility(self):
        self.spinBox_skiprows.setDisabled(not self.checkBox_skiprows.isChecked())

    def import_results(self):
        last_folder = app().config.get_last_folder_for("imported_data_folder")
        file_extensions = ["csv", "dat", "txt", "xlsx", "xls"]

        new_paths = FileDialogService.open_multiple_files(file_extensions, last_folder=last_folder)

        if not new_paths:
            return

        self.imported_paths += new_paths

        if len(self.imported_paths) == 1:
            imported_text = str(self.imported_paths[0])
        else:
            imported_text = f"{self.imported_paths[0].name} (+{len(self.imported_paths) - 1} more)"

        tooltip_text = "Imported files:\n" + "\n".join(map(str, self.imported_paths))
        last_imported_file = str(self.imported_paths[-1])

        self.lineEdit_import_results_path.setText(imported_text)
        self.lineEdit_import_results_path.setToolTip(tooltip_text)

        for imported_path in new_paths:
            file = FileHandler().read(imported_path)

            if isinstance(file, SpreadsheetData):
                for sheet in file.sheets:
                    sheet.source_file = file.filename
                    key = self.get_data_index()
                    self.imported_results[key] = sheet
            else:
                key = self.get_data_index()
                self.imported_results[key] = file

        app().config.write_last_folder_path_in_file("imported_data_folder", last_imported_file)
        self.update_treeWidget_info()

    def update_treeWidget_info(self):
        self.cache_checkButtons_state()
        self.treeWidget_import_text_files.clear()
        self.treeWidget_import_sheet_files.clear()
        #
        if len(self.imported_results) > 0:
            for i, (id, file) in enumerate(self.imported_results.items()):

                # Creates the QCheckButtons to control data to be plotted
                self.ids_to_checkBox[id] = QCheckBox()

                checkbox_container = QWidget()
                cointeiner_layout = QHBoxLayout(checkbox_container)
                cointeiner_layout.addStretch()
                cointeiner_layout.addWidget(self.ids_to_checkBox[id])
                cointeiner_layout.addStretch()
                cointeiner_layout.setContentsMargins(0, 0, 0, 0)

                if id in self.checkButtons_state.keys():
                    self.ids_to_checkBox[id].setChecked(self.checkButtons_state[id])

                if isinstance(file, SpreadsheetSheet):
                    _item = QTreeWidgetItem([file.source_file, file.name])
                    self.treeWidget_import_sheet_files.addTopLevelItem(_item)
                    self.treeWidget_import_sheet_files.setItemWidget(_item, 2, checkbox_container)

                else:
                    _item = QTreeWidgetItem([file.filename])
                    self.treeWidget_import_text_files.addTopLevelItem(_item)
                    self.treeWidget_import_text_files.setItemWidget(_item, 1, checkbox_container)                  

                for i in range(5):
                    _item.setTextAlignment(i, Qt.AlignCenter)

    def get_data_index(self):
        return len(self.imported_results) + 1
    
    def join_imported_data(self):
        j = 0
        imported_results_data = dict()
        for id, checkBox in self.ids_to_checkBox.items():
            temp_dict = dict()
            if checkBox.isChecked():

                if id < len(self.colors):
                    color = self.colors[j]
                    j += 1
                else:
                    color = np.random.randint(0,255,3)/255

                file = self.imported_results[id]
                key = (id)

                if isinstance(file, SpreadsheetSheet):
                    temp_dict = self.generate_temp_dict(file.name, file.data, color)
                else:
                    temp_dict = self.generate_temp_dict(file.filename, file.data, color)

                imported_results_data[key] = temp_dict

        self.plotter._set_imported_results_data_to_plot(imported_results_data)
    
    def generate_temp_dict(self, name: str, data: np.ndarray, color) -> dict:
        cols = data.shape[1]
        x_values = data[:, 0]
        if cols == 2:
            y_values = data[:, 1]
        else:
            y_values = data[:, 1] + 1j*data[:, 2]

        return {   "type" : "imported_data",
                        "x_data" : x_values,
                        "y_data" : y_values,
                        "x_label" : "Frequency [Hz]",
                        "y_label" : "Nodal response",
                        "legend" : name,
                        "unit" : "",
                        "title" : "",
                        "color" : color,
                        "linestyle" : "--"   }

    def cache_checkButtons_state(self):
        self.checkButtons_state = dict()
        for key, check in self.ids_to_checkBox.items():
            self.checkButtons_state[key] = check.isChecked()

    def reset_imported_data(self):
        self.lineEdit_import_results_path.clear()
        self.treeWidget_import_sheet_files.clear()
        self.treeWidget_import_text_files.clear()

        self.plotter.reset_imported_results_data_to_plot()

        self._initialize()

    def add_imported_data_to_plot(self):
        self.join_imported_data()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.add_imported_data_to_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        # if self.exporter is not None:
        #     self.exporter.close()

        # if self.importer is not None:
        #     self.importer.close()

        self.keep_window_open = False
        return super().closeEvent(a0)