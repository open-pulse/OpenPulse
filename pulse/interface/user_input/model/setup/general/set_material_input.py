from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from pulse.interface.user_input.model.setup.general.material_widget import MaterialInputs
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.preprocessing.material import Material

window_title = "Error"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class SetMaterialInput(QDialog):
    def __init__(   self, project, opv, cache_selected_lines=[], *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/model/setup/general/set_material.ui'), self)

        self.project = project
        self.opv = opv
        self.cache_selected_lines = cache_selected_lines

        self.opv.setInputObject(self)
        self.lines_ids = self.opv.getListPickedLines()
        
        self._config_window()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self._loading_info_at_start()
        self.exec()

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set material")
        self.setFixedSize(680,600)

    def _reset_variables(self):
        self.selected_row = None
        self.material = None
        self.main_window = self.opv.parent
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.material_path = self.project.get_material_list_path()
        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_attribution_type = self.findChild(QComboBox, 'comboBox_attribution_type')

        # QFrame
        self.frame_main_widget = self.findChild(QFrame, 'frame_main_widget')

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.frame_main_widget.setLayout(self.grid_layout)
        self._add_material_input_widget()

        # QLineEdit
        self.lineEdit_selected_id = self.findChild(QLineEdit, 'lineEdit_selected_id')
        self.lineEdit_selected_material_name = self.findChild(QLineEdit, 'lineEdit_selected_material_name')

        # QPushButtonget_comboBox_index
        self.pushButton_attribute_material = self.findChild(QPushButton, 'pushButton_attribute_material')

        # QTableWidget
        self.tableWidget_material_data = self.findChild(QTableWidget, 'tableWidget_material_data')

    def _add_material_input_widget(self):
        self.material_widget = MaterialInputs(self.main_window)
        self.grid_layout.addWidget(self.material_widget)

    def _create_connections(self):
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.pushButton_attribute_material.clicked.connect(self.confirm_material_attribution)
        # self.tableWidget_material_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        # self.tableWidget_material_data.cellDoubleClicked.connect(self.on_cell_double_clicked)

    def on_cell_clicked(self, row, col):
        self.selected_row = row
        self.update_material_selection()

    def on_cell_double_clicked(self, row, col):
        self.selected_row = row
        self.confirm_material_attribution()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_row = current_row
        self.update_material_selection()

    def update_material_selection(self):
        if self.selected_row is None:
            return
        item = self.tableWidget_material_data.item(self.selected_row, 0)
        if item is None:
            return
        material_name = item.text()
        self.lineEdit_selected_material_name.setText("")
        if material_name != "":
            self.lineEdit_selected_material_name.setText(material_name)

    def update_attribution_type(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)
            self.comboBox_attribution_type.setCurrentIndex(0)
        elif index == 1:
            self.write_ids(self.lines_ids)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text)

    def update_selection(self):
        if self.lines_ids != []:
            self.write_ids(self.lines_ids)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)
        else:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)
            self.comboBox_attribution_type.setCurrentIndex(0)

    def _loading_info_at_start(self):
        if self.cache_selected_lines != []:
            self.lines_ids = self.cache_selected_lines
        self.update_selection()

    def update(self):
        self.lines_ids = self.opv.getListPickedLines()
        self.update_selection()

    def confirm_material_attribution(self):

        if self.selected_row is None:
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([window_title, self.title, self.message])
            return
        
        try:
            _row = self.selected_row
            name = self.tableWidget_material_data.item(_row, 0).text()
            identifier = int(self.tableWidget_material_data.item(_row, 1).text())
            density = float(self.tableWidget_material_data.item(_row, 2).text())
            young = float(self.tableWidget_material_data.item(_row, 3).text())*(10**(9))
            poisson = float(self.tableWidget_material_data.item(_row, 4).text())
            thermal_expansion_coefficient = float(self.tableWidget_material_data.item(_row, 5).text())
            color = self.tableWidget_material_data.item(_row, 6).text()
            
            new_material = Material(name, 
                                    density,
                                    poisson_ratio = poisson, 
                                    young_modulus = young, 
                                    identifier = identifier, 
                                    thermal_expansion_coefficient = thermal_expansion_coefficient, 
                                    color = color)
            self.material = new_material
            
            if self.comboBox_attribution_type.currentIndex():

                lineEdit = self.lineEdit_selected_id.text()
                self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
                if self.stop:
                    return True 
                               
                self.project.set_material_by_lines(self.lines_typed, self.material)
                print("[Set Material] - {} defined in the entities {}".format(self.material.name, self.lines_typed))
                # self.opv.changeColorEntities(self.lines_typed, self.material.getNormalizedColorRGB())
            else:
                self.project.set_material_to_all_lines(self.material)       
                print("[Set Material] - {} defined in all entities".format(self.material.name))
                # self.opv.changeColorEntities(entities, self.material.getNormalizedColorRGB())
            self.close()

        except Exception as error_log:
            self.title = "Error detected on material list data"
            self.message = str(error_log)
            PrintMessageInput([window_title, self.title, self.message])
            return
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_material_attribution()
        elif event.key() == Qt.Key_Delete:
            self.confirm_material_removal()
        elif event.key() == Qt.Key_Escape:
            self.close()