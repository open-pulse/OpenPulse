from PySide6.QtCore import Qt
from pathlib import Path

from pulse import app
from pulse.interface.ui_generated.model.setup.fluid.load_fluid_composition_ui import LoadFluidComposition_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput



class LoadFluidCompositionInput(LoadFluidComposition_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        app().main_window.set_input_widget(self)

        self.file_path = kwargs.get("file_path", "")
       
        self._initialize()
        self._config_window()
        self._create_connections()
        self._config_widgets()
        self._load_file()
        self.exec()

    def _initialize(self):

        self.complete = False
        self.fluid_composition_data = None

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _create_connections(self):
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.confirm_button_callback)
        self.pushButton_search.clicked.connect(self.search_button_callback)

    def _config_widgets(self):
        self.lineEdit_file_path.setDisabled(True)
        self.comboBox_sheet_names.setDisabled(True)

    def _load_file(self):
        if self.file_path != "":
            self.lineEdit_file_path.setText(self.file_path)
            self.load_composition_data_from_file()

    def search_button_callback(self):

        last_path = app().config.get_last_folder_for("fluid_composition_folder")
        if last_path is None:
            last_path = str(Path().home())

        caption = "Open the fluid composition file"
        self.file_path, check = app().main_window.file_dialog.get_open_file_name(
                                                                                    caption,
                                                                                    last_path,
                                                                                    'Files (*.xlsx *.xls)'
                                                                                 )

        if not check:
            return
        
        app().config.write_last_folder_path_in_file("fluid_composition_folder", self.file_path)
                                                    

        self.lineEdit_file_path.setText(self.file_path)

        if self.load_composition_data_from_file():
            return True

    def load_composition_data_from_file(self):

        if self.lineEdit_file_path.text() == "":
            if self.search_button_callback():
                return True

        self.imported_data = dict()
        self.comboBox_sheet_names.clear()

        from polars import read_excel
        from openpyxl import load_workbook

        wb = load_workbook(self.file_path)
        sheetnames = wb.sheetnames
        for sheetname in sheetnames:

            try:

                sheet_data = read_excel(self.file_path, 
                                        sheet_name = sheetname, 
                                        columns = [0,1,2,3]).to_numpy()

                self.imported_data[sheetname] = sheet_data
                self.comboBox_sheet_names.addItem(sheetname)

            except Exception as error_log:
                window_title = "Error"
                title = "Error while reading data from file"
                message = f"{str(error_log)}"
                PrintMessageInput([window_title, title, message])
                return True

        self.comboBox_sheet_names.setDisabled(False)

    def confirm_button_callback(self):
        if self.imported_data:
            selection = self.comboBox_sheet_names.currentText()
            self.fluid_composition_data = self.imported_data[selection]
            self.complete = True
            self.close()