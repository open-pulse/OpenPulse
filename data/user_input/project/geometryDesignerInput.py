from PyQt5.QtWidgets import QDialog, QLineEdit, QCheckBox, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic
import os
import configparser
import numpy as np
from time import time
from collections import defaultdict

from pulse.utils import get_new_path, get_fillet_parameters
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class GeometryDesignerInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/geometryDesigner.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.preprocessor = project.preprocessor
        self.opv = opv
        self.project_path = project.file._project_path
        self.project_ini_path = get_new_path(self.project_path, "project.ini")
        self.cache_dict_nodes = self.preprocessor.dict_coordinate_to_update_bc_after_remesh.copy()
        self.cache_dict_update_entity_file = self.preprocessor.dict_element_info_to_update_indexes_in_entity_file.copy() 
        self.cache_dict_update_element_info_file = self.preprocessor.dict_element_info_to_update_indexes_in_element_info_file.copy() 
        self.dict_list_elements_to_subgroups = self.preprocessor.dict_list_elements_to_subgroups.copy()

        self.points = {}
        self.lines = {}
        self.fillets = {}
        self.dict_map_lines = {}

        # self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self._define_Qt_variables()
        self._update_buttons()
        self._create_pushbutton_connections()
        self._create_checkbox_connections()
        self.update_export_geometry_state()
        self.update_process_geometry_and_mesh_state()
        self._create_onSingleClick_connections()
        self._create_onDoubleClick_connections()
        self.disable_fillet_line_points_lineEdits()
        self.load_geometry_entities_from_file()

        self.complete = False
        self.exec_()

    def _define_Qt_variables(self):
        
        self.tabWidget_geometry_designer = self.findChild(QTabWidget, 'tabWidget_geometry_designer')
        self.treeWidget_points = self.findChild(QTreeWidget, 'treeWidget_points')
        self.treeWidget_lines = self.findChild(QTreeWidget, 'treeWidget_lines')
        self.treeWidget_fillets = self.findChild(QTreeWidget, 'treeWidget_fillets')
        self.treeWidget_lines_info = self.findChild(QTreeWidget, 'treeWidget_lines_info')
        
        self.lineEdit_point_id = self.findChild(QLineEdit, 'lineEdit_point_id')
        self.lineEdit_coord_x = self.findChild(QLineEdit, 'lineEdit_coord_x')
        self.lineEdit_coord_y = self.findChild(QLineEdit, 'lineEdit_coord_y')
        self.lineEdit_coord_z = self.findChild(QLineEdit, 'lineEdit_coord_z')

        self.lineEdit_line_id = self.findChild(QLineEdit, 'lineEdit_line_id')
        self.lineEdit_line_point_id_1 = self.findChild(QLineEdit, 'lineEdit_line_point_id_1')
        self.lineEdit_line_point_id_2 = self.findChild(QLineEdit, 'lineEdit_line_point_id_2')

        self.lineEdit_fillet_id = self.findChild(QLineEdit, 'lineEdit_fillet_id')
        self.lineEdit_fillet_line_id_1 = self.findChild(QLineEdit, 'lineEdit_fillet_line_id_1')
        self.lineEdit_fillet_line_id_2 = self.findChild(QLineEdit, 'lineEdit_fillet_line_id_2')
        self.lineEdit_fillet_radius = self.findChild(QLineEdit, 'lineEdit_fillet_radius')

        self.lineEdit_fillet_point_id_1 = self.findChild(QLineEdit, 'lineEdit_fillet_point_id_1')
        self.lineEdit_fillet_point_id_2 = self.findChild(QLineEdit, 'lineEdit_fillet_point_id_2')
        self.lineEdit_fillet_coord_x_point1 = self.findChild(QLineEdit, 'lineEdit_fillet_coord_x_point1')
        self.lineEdit_fillet_coord_x_point2 = self.findChild(QLineEdit, 'lineEdit_fillet_coord_x_point2')
        self.lineEdit_fillet_coord_y_point1 = self.findChild(QLineEdit, 'lineEdit_fillet_coord_y_point1')
        self.lineEdit_fillet_coord_y_point2 = self.findChild(QLineEdit, 'lineEdit_fillet_coord_y_point2')
        self.lineEdit_fillet_coord_z_point1 = self.findChild(QLineEdit, 'lineEdit_fillet_coord_z_point1')
        self.lineEdit_fillet_coord_z_point2 = self.findChild(QLineEdit, 'lineEdit_fillet_coord_z_point2')
        self.lineEdit_geometry_name = self.findChild(QLineEdit,'lineEdit_geometry_name')
        self.lineEdit_element_size = self.findChild(QLineEdit, 'lineEdit_element_size')
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        
        if self.project.file._element_size is None:
            self.lineEdit_element_size.setText("")
        else:
            self.lineEdit_element_size.setText(str(self.project.file._element_size))
        
        if self.project.file._geometry_tolerance is None:
            self.lineEdit_geometry_tolerance.setText("")
        else:
            self.lineEdit_geometry_tolerance.setText(str(self.project.file._geometry_tolerance))

        self.checkBox_auto_point_ID = self.findChild(QCheckBox, 'checkBox_auto_point_ID')
        self.checkBox_auto_line_ID = self.findChild(QCheckBox, 'checkBox_auto_line_ID')
        self.checkBox_auto_fillet_ID = self.findChild(QCheckBox, 'checkBox_auto_fillet_ID')
        self.checkBox_export_geometry = self.findChild(QCheckBox, 'checkBox_export_geometry')
        self.checkBox_process_geometry_and_mesh = self.findChild(QCheckBox, 'checkBox_process_geometry_and_mesh')
        self.checkBox_maintain_nodes_attributes = self.findChild(QCheckBox, "checkBox_maintain_nodes_attributes")
        self.checkBox_maintain_lines_attributes = self.findChild(QCheckBox, "checkBox_maintain_lines_attributes")
        
        self.radioButton_open_Cascade = self.findChild(QRadioButton, 'radioButton_open_Cascade')
        self.radioButton_built_in = self.findChild(QRadioButton, 'radioButton_built_in')
        self.radioButton_open_Cascade.setChecked(True)
        
        self.pushButton_add_point = self.findChild(QPushButton, 'pushButton_add_point')
        self.pushButton_add_line = self.findChild(QPushButton, 'pushButton_add_line')
        self.pushButton_add_fillet = self.findChild(QPushButton, 'pushButton_add_fillet')
        self.pushButton_remove_point = self.findChild(QPushButton, 'pushButton_remove_point')
        self.pushButton_remove_line = self.findChild(QPushButton, 'pushButton_remove_line')
        self.pushButton_remove_fillet = self.findChild(QPushButton, 'pushButton_remove_fillet')

        self.pushButton_reset_points = self.findChild(QPushButton, 'pushButton_reset_points')
        self.pushButton_reset_lines = self.findChild(QPushButton, 'pushButton_reset_lines')
        self.pushButton_reset_fillets = self.findChild(QPushButton, 'pushButton_reset_fillets')

        self.pushButton_clear_all_entities = self.findChild(QPushButton, 'pushButton_clear_all_entities')
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_generate_geometry = self.findChild(QPushButton, 'pushButton_generate_geometry')
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.generate_geometry()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def cancel(self):
        self.close()

    def _update_buttons(self):
        self.pushButton_add_point.setDisabled(False)
        self.pushButton_add_line.setDisabled(False)
        self.pushButton_add_fillet.setDisabled(False)
        self.pushButton_remove_point.setDisabled(True)
        self.pushButton_remove_line.setDisabled(True)
        self.pushButton_remove_fillet.setDisabled(True)
    
    def _create_checkbox_connections(self):
        self.checkBox_auto_point_ID.toggled.connect(self.update_auto_point_ID)
        self.checkBox_auto_line_ID.toggled.connect(self.update_auto_line_ID)
        self.checkBox_auto_fillet_ID.toggled.connect(self.update_auto_fillet_ID)
        self.checkBox_export_geometry.toggled.connect(self.update_export_geometry_state)
        self.checkBox_process_geometry_and_mesh.toggled.connect(self.update_process_geometry_and_mesh_state)
        self.radioButton_built_in.clicked.connect(self.update_radioButton_built_in)
        self.radioButton_open_Cascade.clicked.connect(self.update_radioButton_open_Cascade)

    def update_radioButton_built_in(self):
        self.checkBox_export_geometry.setChecked(False)
        self.lineEdit_geometry_name.setDisabled(True)

    def update_radioButton_open_Cascade(self):
        if self.checkBox_export_geometry.isChecked():
            self.lineEdit_geometry_name.setDisabled(True)

    def update_process_geometry_and_mesh_state(self):
        _bool = self.checkBox_process_geometry_and_mesh.isChecked()
        self.lineEdit_element_size.setDisabled(not _bool)
        self.lineEdit_geometry_tolerance.setDisabled(not _bool)
        if _bool or self.project.check_mesh_setup():
            self.pushButton_generate_geometry.setGeometry(QRect(410, 508, 260, 36))
            self.pushButton_generate_geometry.setText("Generate geometry and mesh")
        else:
            self.pushButton_generate_geometry.setGeometry(QRect(410, 508, 180, 36))
            self.pushButton_generate_geometry.setText("Generate geometry")

    def update_export_geometry_state(self):
        _bool = self.checkBox_export_geometry.isChecked()
        self.radioButton_open_Cascade.setChecked(_bool)
        self.lineEdit_geometry_name.setDisabled(not _bool)
            
    def _create_pushbutton_connections(self):
        self.pushButton_add_point.clicked.connect(self.add_point)
        self.pushButton_add_line.clicked.connect(self.add_line)
        self.pushButton_add_fillet.clicked.connect(self.add_fillet)
        self.pushButton_remove_point.clicked.connect(self.remove_point)
        self.pushButton_remove_line.clicked.connect(self.remove_line)
        self.pushButton_remove_fillet.clicked.connect(self.remove_fillet)
        self.pushButton_reset_points.clicked.connect(self.reset_points)
        self.pushButton_reset_lines.clicked.connect(self.reset_lines)
        self.pushButton_reset_fillets.clicked.connect(self.reset_fillets)
        self.pushButton_clear_all_entities.clicked.connect(self.clear_all_entities)
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_generate_geometry.clicked.connect(self.generate_geometry)

    def _create_onSingleClick_connections(self):
        self.treeWidget_points.itemClicked.connect(self.on_click_item_points)
        self.treeWidget_lines.itemClicked.connect(self.on_click_item_lines)
        self.treeWidget_fillets.itemClicked.connect(self.on_click_item_fillets)
        self.treeWidget_lines_info.itemClicked.connect(self.on_click_item_line_and_points_info)

    def _create_onDoubleClick_connections(self):
        self.treeWidget_points.itemDoubleClicked.connect(self.on_double_click_item_points)
        self.treeWidget_lines.itemDoubleClicked.connect(self.on_double_click_item_lines)
        self.treeWidget_fillets.itemDoubleClicked.connect(self.on_double_click_item_fillets)
        self.treeWidget_lines_info.itemDoubleClicked.connect(self.on_double_click_item_line_and_points_info)

    def on_click_item_points(self, item):
        self.pushButton_add_point.setDisabled(False)
        self.pushButton_remove_point.setDisabled(True)
        self.lineEdit_point_id.setDisabled(False)
        self.lineEdit_coord_x.setDisabled(False)
        self.lineEdit_coord_y.setDisabled(False)
        self.lineEdit_coord_z.setDisabled(False)
        #
        if item.text(0) != "":
            self.lineEdit_point_id.setText(item.text(0))
            self.lineEdit_coord_x.setText(item.text(1))
            self.lineEdit_coord_y.setText(item.text(2))
            self.lineEdit_coord_z.setText(item.text(3))

    def on_click_item_lines(self, item):
        self.pushButton_add_line.setDisabled(False)
        self.pushButton_remove_line.setDisabled(True)
        self.lineEdit_line_id.setDisabled(False)
        self.lineEdit_line_point_id_1.setDisabled(False)
        self.lineEdit_line_point_id_2.setDisabled(False)
        #
        if item.text(0) != "":
            self.lineEdit_line_id.setText(item.text(0))
            self.lineEdit_line_point_id_1.setText(item.text(1))
            self.lineEdit_line_point_id_2.setText(item.text(2))

    def on_click_item_fillets(self, item):
        self.lineEdit_fillet_id.setDisabled(False)
        self.lineEdit_fillet_line_id_1.setDisabled(False)
        self.lineEdit_fillet_line_id_2.setDisabled(False)
        self.lineEdit_fillet_radius.setDisabled(False)
        self.pushButton_add_fillet.setDisabled(False)
        self.pushButton_remove_fillet.setDisabled(True)
        #
        if item.text(0) != "":
            self.lineEdit_fillet_id.setText(item.text(0))
            self.lineEdit_fillet_line_id_1.setText(item.text(1))
            self.lineEdit_fillet_line_id_2.setText(item.text(2))
            self.lineEdit_fillet_radius.setText(item.text(3))

    def disable_fillet_line_points_lineEdits(self):
        self.lineEdit_fillet_point_id_1.setDisabled(True)
        self.lineEdit_fillet_point_id_2.setDisabled(True)
        self.lineEdit_fillet_coord_x_point1.setDisabled(True)
        self.lineEdit_fillet_coord_y_point1.setDisabled(True)
        self.lineEdit_fillet_coord_z_point1.setDisabled(True)
        self.lineEdit_fillet_coord_x_point2.setDisabled(True)
        self.lineEdit_fillet_coord_y_point2.setDisabled(True)
        self.lineEdit_fillet_coord_z_point2.setDisabled(True)

    def on_click_item_line_and_points_info(self, item):
        #
        if item.text(0) != "":
            line_id = int(item.text(0))
            point_id1 = int(item.text(1))
            point_id2 = int(item.text(2))
            coords_1 = self.points[point_id1]
            coords_2 = self.points[point_id2]
            self.lineEdit_fillet_point_id_1.setText(str(point_id1))
            self.lineEdit_fillet_point_id_2.setText(str(point_id2))
            self.lineEdit_fillet_coord_x_point1.setText(str(coords_1[0]))
            self.lineEdit_fillet_coord_y_point1.setText(str(coords_1[1]))
            self.lineEdit_fillet_coord_z_point1.setText(str(coords_1[2]))
            self.lineEdit_fillet_coord_x_point2.setText(str(coords_2[0]))
            self.lineEdit_fillet_coord_y_point2.setText(str(coords_2[1]))
            self.lineEdit_fillet_coord_z_point2.setText(str(coords_2[2]))
    
    def on_double_click_item_points(self, item):
        self.lineEdit_point_id.setDisabled(True)
        self.lineEdit_coord_x.setDisabled(True)
        self.lineEdit_coord_y.setDisabled(True)
        self.lineEdit_coord_z.setDisabled(True)
        self.pushButton_add_point.setDisabled(True)
        self.pushButton_remove_point.setDisabled(False)
        #
        if item.text(0) != "":
            self.lineEdit_point_id.setText(item.text(0))
            self.lineEdit_coord_x.setText(item.text(1))
            self.lineEdit_coord_y.setText(item.text(2))
            self.lineEdit_coord_z.setText(item.text(3))
        
    def on_double_click_item_lines(self, item):
        self.lineEdit_line_id.setDisabled(True)
        self.lineEdit_line_point_id_1.setDisabled(True)
        self.lineEdit_line_point_id_2.setDisabled(True)
        self.pushButton_add_line.setDisabled(True)
        self.pushButton_remove_line.setDisabled(False)
        #
        if item.text(0) != "":
            self.lineEdit_line_id.setText(item.text(0))
            self.lineEdit_line_point_id_1.setText(item.text(1))
            self.lineEdit_line_point_id_2.setText(item.text(2))

    def on_double_click_item_fillets(self, item):
        self.lineEdit_fillet_id.setDisabled(True)
        self.lineEdit_fillet_line_id_1.setDisabled(True)
        self.lineEdit_fillet_line_id_2.setDisabled(True)
        self.lineEdit_fillet_radius.setDisabled(True)
        self.pushButton_add_fillet.setDisabled(True)
        self.pushButton_remove_fillet.setDisabled(False)
        #
        if item.text(0) != "":
            self.lineEdit_fillet_id.setText(item.text(0))
            self.lineEdit_fillet_line_id_1.setText(item.text(1))
            self.lineEdit_fillet_line_id_2.setText(item.text(2))
            self.lineEdit_fillet_radius.setText(item.text(3))

    def on_double_click_item_line_and_points_info(self, item):
        self.lineEdit_fillet_point_id_1.setText("")
        self.lineEdit_fillet_point_id_2.setText("")
        self.lineEdit_fillet_coord_x_point1.setText("")
        self.lineEdit_fillet_coord_y_point1.setText("")
        self.lineEdit_fillet_coord_z_point1.setText("")
        self.lineEdit_fillet_coord_x_point2.setText("")
        self.lineEdit_fillet_coord_y_point2.setText("")
        self.lineEdit_fillet_coord_z_point2.setText("")

    def clear_point_input_fields(self):
        self.lineEdit_point_id.setDisabled(False)
        self.lineEdit_coord_x.setDisabled(False)
        self.lineEdit_coord_y.setDisabled(False)
        self.lineEdit_coord_z.setDisabled(False)
        self.lineEdit_point_id.setText("")
        self.lineEdit_coord_x.setText("")
        self.lineEdit_coord_y.setText("")
        self.lineEdit_coord_z.setText("")

    def clear_line_input_fields(self):
        self.lineEdit_line_id.setDisabled(False)
        self.lineEdit_line_point_id_1.setDisabled(False)
        self.lineEdit_line_point_id_2.setDisabled(False)
        self.lineEdit_line_id.setText("")
        self.lineEdit_line_point_id_1.setText("")
        self.lineEdit_line_point_id_2.setText("")

    def clear_fillet_input_fields(self):
        self.lineEdit_fillet_id.setDisabled(False)
        self.lineEdit_fillet_line_id_1.setDisabled(False)
        self.lineEdit_fillet_line_id_2.setDisabled(False)  
        self.lineEdit_fillet_radius.setDisabled(False) 
        self.lineEdit_fillet_id.setText("")
        self.lineEdit_fillet_line_id_1.setText("")
        self.lineEdit_fillet_line_id_2.setText("")
        self.lineEdit_fillet_radius.setText("")         

    def load_geometry_entities_from_file(self):
        try:
            self.cache_geometry = self.preprocessor.geometry
        except:
               self.cache_geometry= None
        self.cache_dict_lines_to_edge_coord = self.preprocessor.get_lines_vertex_coordinates()
        entities_data = self.project.file.load_geometry_entities_file()
        
        self.update_process_geometry_and_mesh_state()
        if entities_data is None:
            return
        
        self.points = {}
        if 'points_data' in entities_data.keys():
            self.points = entities_data['points_data']

        self.lines = {}
        if 'lines_data' in entities_data.keys():
            self.lines = entities_data['lines_data']
        
        self.fillets = {}
        if 'fillets_data' in entities_data.keys():
            for fillet_id, data in entities_data['fillets_data'].items():
                fillets_data = []
                for index, value in enumerate(data):
                    if index == 2:
                        fillets_data.append(value)
                    else:
                        fillets_data.append(int(value))
                self.fillets[fillet_id] = fillets_data

        if len(self.points) > 0:
            self.load_points_info()

        if len(self.lines) > 0:
            self.load_lines_info()

        if len(self.fillets) > 0:
            self.load_fillets_info()

    def update_auto_point_ID(self):
        _checked = self.checkBox_auto_point_ID.isChecked()
        if _checked:
            point_id = 1
            stop = False
            if len(self.points) > 0:
                while not stop:
                    if point_id in self.points.keys():
                        point_id += 1
                    else:
                        stop = True 
            self.lineEdit_point_id.setText(str(point_id))
        self.lineEdit_point_id.setDisabled(_checked)

    def update_auto_line_ID(self):
        _checked = self.checkBox_auto_line_ID.isChecked()
        if _checked:
            line_id = 1
            stop = False
            if len(self.lines) > 0:
                while not stop:
                    if line_id in self.lines.keys():
                        line_id += 1
                    else:
                        stop = True 
            self.lineEdit_line_id.setText(str(line_id))
        self.lineEdit_line_id.setDisabled(_checked)

    def update_auto_fillet_ID(self):
        _checked = self.checkBox_auto_fillet_ID.isChecked()
        if _checked:
            fillet_id = 1
            stop = False
            if len(self.fillets) > 0:
                while not stop:
                    if fillet_id in self.fillets.keys():
                        fillet_id += 1
                    else:
                        stop = True 
            self.lineEdit_fillet_id.setText(str(fillet_id))
        self.lineEdit_fillet_id.setDisabled(_checked)

    def load_points_info(self):
        self.treeWidget_points.clear()
        self.update_auto_point_ID()
        for point_id, [coord_x, coord_y, coord_z] in self.points.items():
            new = QTreeWidgetItem([str(point_id), str(coord_x), str(coord_y), str(coord_z)])
            for i in range(4):
                new.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_points.addTopLevelItem(new)         

    def load_lines_info(self):
        self.treeWidget_lines.clear()
        self.treeWidget_lines_info.clear()
        self.update_auto_line_ID()
        for line_id, [point_id1, point_id2] in self.lines.items():
            new_1 = QTreeWidgetItem([str(line_id), str(point_id1), str(point_id2)])
            new_2 = QTreeWidgetItem([str(line_id), str(point_id1), str(point_id2)])
            for i in range(3):
                new_1.setTextAlignment(i, Qt.AlignCenter)
                new_2.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_lines.addTopLevelItem(new_1) 
            self.treeWidget_lines_info.addTopLevelItem(new_2)

    def load_fillets_info(self):
        self.update_auto_fillet_ID()
        self.treeWidget_fillets.clear()
        for fillet_id, [line_id1, line_id2, radius, _, _, _, _, _, _] in self.fillets.items():
            new = QTreeWidgetItem([str(fillet_id), str(line_id1), str(line_id2), str(radius)])
            for i in range(4):
                new.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_fillets.addTopLevelItem(new) 

    def add_point(self):
        self.stop, self.point_typed = self.check_input_ID(self.lineEdit_point_id, label="Point")
        if self.stop:
            self.lineEdit_point_id.setFocus()
            return
        
        if self.check_inputs(self.lineEdit_coord_x, label="coord_x", zero_if_blank=True):
            coord_x = self.value
        else:
            return
  
        if self.check_inputs(self.lineEdit_coord_y, label="coord_y", zero_if_blank=True):
            coord_y = self.value
        else:
            return

        if self.check_inputs(self.lineEdit_coord_z, label="coord_z", zero_if_blank=True):
            coord_z = self.value
        else:
            return
        
        for point_id, coords in self.points.items():
            if coords == [coord_x, coord_y, coord_z]:
                title = "Invalid point coordinates" 
                message = f"The typed coordinates {coords} are the same coordinates of the \nalready existing Point ID {point_id}. "
                message += "You should to modify the current Point \ncoordinates to proceed."
                PrintMessageInput([title, message, window_title_2])
                self.lineEdit_coord_x.setFocus()
                return

        self.points[self.point_typed] = [coord_x, coord_y, coord_z]
        self.clear_point_input_fields()
        self.load_points_info()

    def add_line(self):
        _stop, line_typed = self.check_input_ID(self.lineEdit_line_id, label="Line")
        if _stop:
            self.lineEdit_line_id.setFocus()
            return
        
        _stop, point_id1_typed = self.check_input_ID(self.lineEdit_line_point_id_1, label="Point ID 1")
        if _stop:
            self.lineEdit_line_point_id_1.setFocus()
            self.lineEdit_line_point_id_1.setText("")
            return
        if point_id1_typed not in self.points.keys():
            title = "Invalid typed point ID" 
            message = "The typed point ID 1 did not defined yet. Please, you should to add \nthis point before or type an alread defined point to proceed."
            PrintMessageInput([title, message, window_title_2])
            self.lineEdit_line_point_id_1.setText("")
            return

        _stop, point_id2_typed = self.check_input_ID(self.lineEdit_line_point_id_2, label="Point ID 2")
        if _stop:
            self.lineEdit_line_point_id_2.setFocus()
            self.lineEdit_line_point_id_2.setText("")
            return
        if point_id2_typed not in self.points.keys():
            title = "Invalid typed point ID" 
            message = "The typed point ID 2 did not defined yet. Please, you should to add \nthis point before or type an alread defined point to proceed."
            PrintMessageInput([title, message, window_title_2])
            self.lineEdit_line_point_id_2.setText("")
            return
        
        if point_id1_typed != point_id2_typed:
            if len(self.lines) == 0:
                self.lines[line_typed] = [point_id1_typed, point_id2_typed]
                self.clear_line_input_fields()
                self.load_lines_info()
            else:
                cache_dict_lines = self.lines.copy()
                for _line_id, _line_points in cache_dict_lines.items():
                    if _line_points != [point_id1_typed, point_id2_typed] and _line_points != [point_id2_typed, point_id1_typed]:
                        self.lines[line_typed] = [point_id1_typed, point_id2_typed]
                    elif _line_id == int(self.lineEdit_line_id.text()):
                        self.lines[line_typed] = [point_id1_typed, point_id2_typed]
                    else:
                        title = "Lines: invalid inputs for point IDs" 
                        message = f"The typed point ID 1 and point ID 2 has alread been attributed to the \nline ID #{_line_id}. "
                        message += "As suggestion, we recommend you to check all existent \nlines to proceed."
                        PrintMessageInput([title, message, window_title_2])
                        self.lineEdit_line_point_id_1.setText("")
                        self.lineEdit_line_point_id_2.setText("")
                        return
                self.clear_line_input_fields()
                self.load_lines_info()
        else:
            title = "Invalid typed point ID" 
            message = "The typed point ID 1 and point ID 2 should differs. As suggestion, \nwe recommend you to change the typed point ID 2 to proceed."
            PrintMessageInput([title, message, window_title_2])
            self.lineEdit_line_point_id_2.setText("")

    def add_fillet(self):

        _stop, fillet_typed = self.check_input_ID(self.lineEdit_fillet_id, label="Fillet")
        if _stop:
            self.lineEdit_fillet_id.setFocus()
            return

        _stop, line_id1_typed = self.check_input_ID(self.lineEdit_fillet_line_id_1, label="Line ID 1")
        if _stop:
            self.lineEdit_fillet_line_id_1.setFocus()
            self.lineEdit_fillet_line_id_1.setText("")
            return
        if line_id1_typed not in self.lines.keys():
            title = "Invalid typed Line ID" 
            message = "The typed Line ID 1 did not defined yet. Please, you should to add \nthis line previously or type an alread defined line to proceed."
            PrintMessageInput([title, message, window_title_2])
            self.lineEdit_fillet_line_id_1.setText("")
            return

        _stop, line_id2_typed = self.check_input_ID(self.lineEdit_fillet_line_id_2, label="Line ID 2")
        if _stop:
            self.lineEdit_fillet_line_id_2.setFocus()
            self.lineEdit_fillet_line_id_2.setText("")
            return
        if line_id2_typed not in self.lines.keys():
            title = "Invalid typed point ID" 
            message = "The typed Line ID 2 did not defined yet. Please, you should to add \nthis line previously or type an alread defined line to proceed."
            PrintMessageInput([title, message, window_title_2])
            self.lineEdit_fillet_line_id_2.setText("")
            return

        if line_id1_typed == line_id2_typed:
            title = "Same Line ID inputs" 
            message = "The typed line IDs should be connected, share a common point and differ. It is necessary "
            message += "to accomplish this requisite to proceed with the fillet parameters processing."
            PrintMessageInput([title, message, window_title_2])
            return

        if self.check_inputs(self.lineEdit_fillet_radius, label="fillet radius", only_positive=True):
            fillet_radius = self.value
        else:
            return

        list_points = []
        corner_point = None
        for point_line_1 in self.lines[line_id1_typed]:
            if point_line_1 not in list_points:
                list_points.append(point_line_1)
        
        for point_line_2 in self.lines[line_id2_typed]:
            if point_line_2 not in list_points:
                list_points.append(point_line_2)
            else:
                corner_point = point_line_2 
        
        if corner_point is None:
            title = "Disconnected line inputs" 
            message = "The typed Line IDs should be connected and share a common point. It is necessary "
            message += "to accomplish this requisite to proceed with the fillet parameters processing."
            PrintMessageInput([title, message, window_title_2])
            # self.lineEdit_fillet_line_id_1.setText("")
            # self.lineEdit_fillet_line_id_2.setText("")
            return

        list_points.remove(corner_point)
        set_points = [list_points[0], corner_point, list_points[1]]
        
        if line_id1_typed != line_id2_typed:
            if len(set_points) == 3:  
                
                P1 = self.points[set_points[0]]
                P2 = self.points[set_points[1]]
                P3 = self.points[set_points[2]]

                fillet_parameters, stop = get_fillet_parameters(P1, P2, P3, radius=fillet_radius, unit_length="m")
                if stop:
                    return
                   
                _point_id = 0
                fillet_points = []
                while len(fillet_points) <= 2:
                    _point_id += 1
                    if _point_id not in self.points.keys():
                        fillet_points.append(_point_id)

                if len(self.fillets) == 0:
                    self.fillets[fillet_typed] = [  line_id1_typed, line_id2_typed, fillet_radius, set_points[0], set_points[1], 
                                                        set_points[2], fillet_points[0], fillet_points[1], fillet_points[2]  ]
                else:
                    cache_dict_fillets = self.fillets.copy()
                    for _fillet_id, data in cache_dict_fillets.items():
                        _fillet_lines = [data[0], data[1]]
                        if _fillet_lines != [line_id1_typed, line_id2_typed] and _fillet_lines != [line_id2_typed, line_id1_typed]:
                            self.fillets[fillet_typed] = [  line_id1_typed, line_id2_typed, fillet_radius, set_points[0], set_points[1], 
                                                            set_points[2], fillet_points[0], fillet_points[1], fillet_points[2]  ]
                        elif _fillet_id == int(self.lineEdit_fillet_id.text()):
                            fillet_points = [data[6], data[7], data[8]]
                            self.fillets[fillet_typed] = [  line_id1_typed, line_id2_typed, fillet_radius, set_points[0], set_points[1], 
                                                            set_points[2], fillet_points[0], fillet_points[1], fillet_points[2]  ]
                        else:
                            title = "Fillets: invalid inputs for line IDs" 
                            message = f"The typed line ID 1 and line ID 2 has alread been attributed to the \nfillet ID #{_fillet_id}. "
                            message += "As suggestion, we recommend you to check all existent \nfillets to proceed."
                            PrintMessageInput([title, message, window_title_2])
                            self.lineEdit_fillet_line_id_1.setText("")
                            self.lineEdit_fillet_line_id_2.setText("")
                            return
        
                for index, data in enumerate(fillet_parameters[3:]):
                    self.points[fillet_points[index]] = list(data)

                self.clear_fillet_input_fields()
                self.load_fillets_info()

            else:
                title = "Invalid typed Line ID" 
                message = "The typed Line ID 1 and Line ID 2 should have a commom Point. \nAs suggestion, we recommend you to verify all line Points \nto proceed."
                PrintMessageInput([title, message, window_title_2])
                
        else:
            title = "Invalid typed Line ID" 
            message = "The typed Line ID 1 and Line ID 2 should differs. As suggestion, we recommend you to change the typed Line ID 2 to proceed."
            PrintMessageInput([title, message, window_title_2])
            self.lineEdit_line_point_id_2.setText("")

    def remove_point(self):
        if self.lineEdit_point_id.text() != "":
            point_id = int(self.lineEdit_point_id.text())
            if point_id in self.points.keys():
                self.points.pop(point_id)
                self.remove_line_by_point(point_id)
        self.clear_point_input_fields()
        self.load_points_info()
        self._update_buttons()

    def remove_line(self):
        if self.lineEdit_line_id.text() != "":
            line_id = int(self.lineEdit_line_id.text())
            if line_id in self.lines.keys():
                self.lines.pop(line_id)
                self.remove_fillet_by_line(line_id)
        self.clear_line_input_fields()
        self.load_lines_info()
        self._update_buttons()

    def remove_fillet(self):
        if self.lineEdit_fillet_id.text() != "":
            fillet_id = int(self.lineEdit_fillet_id.text())
            fillet_data = self.fillets[fillet_id]
            self.fillets.pop(fillet_id)
            for point_id in fillet_data[6:]:
                self.points.pop(point_id)
        self.clear_fillet_input_fields()
        self.load_fillets_info()
        self.load_lines_info()
        self.load_points_info()
        self._update_buttons()

    def remove_line_by_point(self, point_id):
        cache_lines = self.lines.copy()
        for line_id, line_points in cache_lines.items():
            if point_id in line_points:
                if line_id in self.lines.keys():
                    self.lines.pop(line_id)
                self.remove_fillet_by_line(line_id)
        self.load_fillets_info()
        self.load_lines_info()

    def remove_fillet_by_line(self, line_id):
        cache_fillets = self.fillets.copy()
        for fillet_id, fillet_data in cache_fillets.items(): 
            if line_id in fillet_data[:2]:
                self.fillets.pop(fillet_id)
                for point_id in fillet_data[6:]:
                    self.points.pop(point_id)
        self.load_fillets_info()
        self.load_points_info()

    def generate_geometry(self):
        
        try:

            self.complete = False
            if len(self.lines) == 0:
                title = "None lines detected in geometry"
                message = "There is no lines connecting points in geometry design. Please, it is necessary " 
                message += "to define at least one line to proceed with the geometry and mesh processing."
                PrintMessageInput([title, message, window_title_2])
                return True

            if len(self.points) > 0:
                entities_data = {   "points_data" : self.points,
                                    "lines_data" : self.lines,
                                    "fillets_data" : self.fillets    }
                 
                if self.radioButton_built_in.isChecked():
                    kernel = "built-in"
                elif self.radioButton_open_Cascade.isChecked():
                    kernel = "Open Cascade"

                if self.checkBox_export_geometry.isChecked():
                    if self.radioButton_built_in.isChecked():
                        ext = "opt"
                    elif self.radioButton_open_Cascade.isChecked():
                        ext = "step"
                    if self.lineEdit_geometry_name.text() != "":
                        filename = f"{self.lineEdit_geometry_name.text()}.{ext}"
                        geometry_path = get_new_path(self.project.file._project_path, filename)
                    else:
                        window_title = "ERROR"
                        message_title = f"Invalid geometry name"
                        message = "An empty entry was detecetd at 'Geometry name' input field. \nIt is necessary enter a valid geometry name to proceed."
                        PrintMessageInput([message_title, message, window_title])  
                        self.lineEdit_geometry_name.setFocus()
                        return                  
                else:                   
                    geometry_path = ""
 
                self.project.set_geometry_entities(entities_data, geometry_path, kernel=kernel)
                if self.checkBox_process_geometry_and_mesh.isChecked() or self.project.check_mesh_setup():
                    if self.process_mesh():
                        return
                    self.complete = True
                else:
                    self.complete = None

            self.close()

        except Exception as log_error:
            print(str(log_error))

    def process_mesh(self):
 
        if self.check_element_size_input_value():
            return True

        if self.check_geometry_tolerance_input_value():
            return True

        self.project.file.update_project_attributes(self.element_size, self.geometry_tolerance)
        self.project.initial_load_project_actions(self.project_ini_path)
        if self.checkBox_maintain_lines_attributes.isChecked():
            self.process_lines_mapping()
        if self.checkBox_maintain_nodes_attributes.isChecked():
            self.process_nodes_mapping()
        self.project.load_project_files()
        self.preprocessor.check_disconnected_lines(self.element_size)
        self.opv.updatePlots()
        self.opv.changePlotToMesh()
        return False

    def process_lines_mapping(self):
        dict_map_lines = {}
        self.geometry = self.preprocessor.geometry
        if self.cache_geometry.lines == self.geometry.lines:
            for line_id in self.geometry.lines.keys():
                dict_map_lines[line_id] = line_id
        else:
            self.dict_lines_edge_coord = self.preprocessor.get_lines_vertex_coordinates()
            for cache_line_id, cache_coords in self.cache_dict_lines_to_edge_coord.items():
                for line_id, new_coords in self.dict_lines_edge_coord.items():
                    if (np.array(cache_coords) == np.array(new_coords)).all() or (np.array(cache_coords) == np.flip(new_coords, axis=0)).all():
                        dict_map_lines[line_id] = cache_line_id
        self.project.file.update_entity_file(self.preprocessor.all_lines, dict_map_lines=dict_map_lines)

    def process_nodes_mapping(self):

        data_1 = self.preprocessor.update_node_ids_after_remesh(self.cache_dict_nodes)
        [self.dict_old_to_new_node_external_indexes, self.dict_non_mapped_bcs] = data_1

        if len(self.dict_old_to_new_node_external_indexes) > 0:
            self.project.update_node_ids_in_file_after_remesh(self.dict_old_to_new_node_external_indexes, self.dict_non_mapped_bcs)

    def process_elements_mapping(self):
    
        data_2 = self.preprocessor.update_element_ids_after_remesh(self.cache_dict_update_entity_file)
        data_3 = self.preprocessor.update_element_ids_after_remesh(self.cache_dict_update_element_info_file)
        
        [self.dict_group_elements_to_update_entity_file, self.dict_non_mapped_subgroups_entity_file] = data_2
        [self.dict_group_elements_to_update_element_info_file, self.dict_non_mapped_subgroups_info_file] = data_3

        if len(self.dict_group_elements_to_update_entity_file) > 0:
            self.project.update_element_ids_in_entity_file_after_remesh(self.dict_group_elements_to_update_entity_file,
                                                                        self.dict_non_mapped_subgroups_entity_file)
        if len(self.dict_group_elements_to_update_element_info_file) > 0:
            self.project.update_element_ids_in_element_info_file_after_remesh(  self.dict_group_elements_to_update_element_info_file,
                                                                                self.dict_non_mapped_subgroups_info_file,
                                                                                self.dict_list_elements_to_subgroups    )
 
    def check_element_size_input_value(self):
        self.element_size = 0.01
        try:
            self.element_size = float(self.lineEdit_element_size.text())
        except Exception as _error:
            self.print_error_message('Element length', str(_error))
            return True
        return False

    def check_geometry_tolerance_input_value(self):
        self.geometry_tolerance = 1e-8
        try:
            self.geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        except Exception as _error:
            self.print_error_message('Mesh tolerance', str(_error))
            return True
        return False

    def print_error_message(self, label_1, label_2, text):
        window_title = "ERROR"
        message_title = f"Invalid {label_1}"
        message = f"Please, inform a valid entry at '{label_1}' input field to continue."
        message += "The input value should be a float or an integer number greater than zero."
        message += f"\n\n{text}"
        PrintMessageInput([message_title, message, window_title])

    def reset_points(self):

        title = "Resetting of all Points"
        message = "Do you really want to reset the all defined Points?\n\n\n"
        message += "Press the 'Proceed' button to proceed with resetting or press 'Cancel' or 'Close' buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Proceed')

        if read._doNotRun:
            return

        if read._continue:
            self.points = {}
            self.lines = {}
            self.fillets = {}
            self.clear_point_input_fields()
            self.clear_line_input_fields()
            self.clear_fillet_input_fields()
            self._update_buttons()
            self.load_points_info()
            self.load_lines_info()
            self.load_fillets_info()

    def reset_lines(self):

        title = "Resetting of all Lines"
        message = "Do you really want to reset the all defined Lines?\n\n\n"
        message += "Press the 'Proceed' button to proceed with resetting or press 'Cancel' or 'Close' buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Proceed')
        if read._doNotRun:
            return

        if read._continue:
            self.lines = {}
            self.fillets = {}
            self.load_lines_info()
            self.load_fillets_info()

    def reset_fillets(self):
        
        title = "Resetting of all Fillets"
        message = "Do you really want to reset the all defined Fillets?\n\n\n"
        message += "Press the 'Proceed' button to proceed with resetting or press 'Cancel' or 'Close' buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Proceed')
        if read._doNotRun:
            return

        if read._continue:

            for data in self.fillets.values():
                for point_id in data[6:]:
                    self.points.pop(point_id) 

            self.fillets = {}
            self.load_fillets_info()
            self.load_points_info()

    def clear_all_entities(self):

        title = "Removal of all Entities"
        message = "Do you really want to remove the all defined Entities?\n\n\n"
        message += "Press the 'Proceed' button to proceed with resetting or press 'Cancel' or 'Close' buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Proceed')
        if read._doNotRun:
            return

        if read._continue:
            self.points = {}
            self.lines = {}
            self.fillets = {}
            self.load_points_info()
            self.load_lines_info()
            self.load_fillets_info()

    def check_input_ID(self, lineEdit, label=""):
        try:
            
            title = f"Invalid entry to the {label} ID"
            message = ""
            str_lineEdit = lineEdit.text()
            tokens = str_lineEdit.strip().split(',')

            try:
                tokens.remove('')
            except:
                pass

            list_nodes_typed = list(map(int, tokens))

            if len(list_nodes_typed) == 0:
                    message = f"An empty input field for the {label} ID has been detected. \n\nPlease, enter a valid {label} ID to proceed!"
            
            elif len(list_nodes_typed) >= 1: 
                if len(list_nodes_typed) > 1:
                    message = f"Multiple {label} IDs"
                else:
                    if list_nodes_typed[-1] == 0:
                        message = f"Dear user, you have typed an invalid entry at the {label} ID input field.\n\n" 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1."

        except Exception as log_error:
            message = f"Wrong input for the {label} ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
            return True, [] 

        return False, list_nodes_typed[0]
 

    def check_inputs(self, lineEdit, label="--", only_positive=False, zero_if_blank=False):
        self.value = None
        try:
            if zero_if_blank and lineEdit.text() == "":
                self.value = float(0)
                return True

            self.value = float(lineEdit.text())

            if only_positive:
                if self.value <= 0:
                    window_title ="ERROR"
                    title = f"Invalid entry to the {label}"
                    message = f"The allowable input values must be non-zero positive integers or float numbers."
                    PrintMessageInput([title, message, window_title])
                    lineEdit.setFocus()
                    # self.stop = True
                    return False
                
        except Exception:
            window_title ="ERROR"
            title = f"Invalid entry to the {label}"
            message = f"The allowable input values must be any real numbers."
            PrintMessageInput([title, message, window_title])
            lineEdit.setFocus()
            # self.stop = True
            return False
        return True