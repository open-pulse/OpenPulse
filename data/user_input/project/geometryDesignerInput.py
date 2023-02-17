from PyQt5.QtWidgets import QDialog, QLineEdit, QCheckBox, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
import configparser
from time import time
# from collections import defaultdict

from pulse.utils import get_new_path, get_fillet_parameters, generate_geometry_gmsh
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

        self.points = {}#defaultdict(list)
        self.lines = {}#defaultdict(list)
        self.fillets = {}#defaultdict(list)

        # self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self._define_Qt_variables()
        self._update_buttons()
        self._create_pushbutton_connections()
        self._create_checkbox_connections()
        self._create_onSingleClick_connections()
        self._create_onDoubleClick_connections()
        self.disable_fillet_line_points_lineEdits()
        self.load_geometry_entities_from_file()

        self.complete = False
        self.exec_()

    def load_geometry_entities_from_file(self):
        
        entities_data = self.project.file.load_geometry_entities_file()
        if entities_data is None:
            return
        
        self.points = entities_data['points_data']
        self.lines = entities_data['lines_data']

        self.fillets = {}
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

        self.checkBox_auto_point_ID = self.findChild(QCheckBox, 'checkBox_auto_point_ID')
        self.checkBox_auto_line_ID = self.findChild(QCheckBox, 'checkBox_auto_line_ID')
        self.checkBox_auto_fillet_ID = self.findChild(QCheckBox, 'checkBox_auto_fillet_ID')

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
            print("Enter pressed")
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
        # return
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
                PrintMessageInput([window_title_2, message, title])
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
            PrintMessageInput([window_title_2, message, title])
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
            PrintMessageInput([window_title_2, message, title])
            self.lineEdit_line_point_id_2.setText("")
            return
        
        if point_id1_typed != point_id2_typed:
            self.lines[line_typed] = [point_id1_typed, point_id2_typed]
            self.clear_line_input_fields()
            self.load_lines_info()
        else:
            title = "Invalid typed point ID" 
            message = "The typed point ID 1 and point ID 2 should differs. As suggestion, \nwe recommend you to change the typed point ID 2 to proceed."
            PrintMessageInput([window_title_2, message, title])
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
            PrintMessageInput([window_title_2, message, title])
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
            PrintMessageInput([window_title_2, message, title])
            self.lineEdit_fillet_line_id_2.setText("")
            return

        if self.check_inputs(self.lineEdit_fillet_radius, label="fillet radius", only_positive=True):
            fillet_radius = self.value
        else:
            return

        list_points = []
        for point_line_1 in self.lines[line_id1_typed]:
            if point_line_1 not in list_points:
                list_points.append(point_line_1)
        
        for point_line_2 in self.lines[line_id2_typed]:
            if point_line_2 not in list_points:
                list_points.append(point_line_2)
            else:
                corner_point = point_line_2 
        
        list_points.remove(corner_point)
        set_points = [list_points[0], corner_point, list_points[1]]

        # print(f"Line 1 points: {self.lines[line_id1_typed]}")
        # print(f"Line 2 points: {self.lines[line_id2_typed]}")
        # print(f"Corner point: {corner_point}")
        
        if line_id1_typed != line_id2_typed:
            if len(set_points) == 3:  
                P1 = self.points[set_points[0]]
                P2 = self.points[set_points[1]]
                P3 = self.points[set_points[2]]
                fillet_parameters, stop = get_fillet_parameters(P1, P2, P3, radius=fillet_radius, unit_length="m")
                fillet_points = []
                for index in range(3,6):
                    point_id = len(self.points)+1
                    fillet_points.append(point_id)
                    if point_id not in self.points.keys():
                        self.points[point_id] = list(fillet_parameters[index]) 
                # call_gmsh(P1, P2, P3, fillet_radius, unit_length="m")
                if stop:
                    return     
                else:
                    self.fillets[fillet_typed] = [  line_id1_typed, line_id2_typed, fillet_radius, set_points[0], set_points[1], 
                                                    set_points[2], fillet_points[0], fillet_points[1], fillet_points[2]  ]
                    self.clear_fillet_input_fields()
                    self.load_fillets_info()
                    return
            else:
                title = "Invalid typed Line ID" 
                message = "The typed Line ID 1 and Line ID 2 should have a commom Point. \nAs suggestion, we recommend you to verify all line Points \nto proceed."
                PrintMessageInput([window_title_2, message, title])
                # self.lineEdit_line_point_id_2.setText("")
        else:
            title = "Invalid typed Line ID" 
            message = "The typed Line ID 1 and Line ID 2 should differs. As suggestion, we recommend you to change the typed Line ID 2 to proceed."
            PrintMessageInput([window_title_2, message, title])
            self.lineEdit_line_point_id_2.setText("")

    def remove_point(self):
        if self.lineEdit_point_id.text() != "":
            point_id = int(self.lineEdit_point_id.text())
            if point_id in self.points.keys():
                self.points.pop(point_id)
        self.clear_point_input_fields()
        self.load_points_info()
        self._update_buttons()

    def remove_line(self):
        if self.lineEdit_line_id.text() != "":
            line_id = int(self.lineEdit_line_id.text())
            if line_id in self.lines.keys():
                self.lines.pop(line_id)
        self.clear_line_input_fields()
        self.load_lines_info()
        self._update_buttons()

    def remove_fillet(self):
        if self.lineEdit_fillet_id.text() != "":
            fillet_id = int(self.lineEdit_fillet_id.text())
            if fillet_id in self.lines.keys():
                self.lines.pop(fillet_id)
        self.clear_fillet_input_fields()
        self.load_fillets_info()
        self._update_buttons()
        
    def generate_geometry(self):
        save_geometry_file = True
        built_in = False
        self.close()
        try:
            self.complete = False
            if len(self.points) > 0:
                entities_data = {   "points_data" : self.points,
                                    "lines_data" : self.lines,
                                    "fillets_data" : self.fillets    }
                
                geometry_path = ""
                if save_geometry_file:
                    if False:
                        ext = "opt"
                    else:
                        ext = "step"
                    filename = f"export_geometry.{ext}"
                    geometry_path = get_new_path(self.project.file._project_path, filename)
                self.project.set_geometry_entities(entities_data, geometry_path, built_in=built_in)
                self.complete = True
                
        except Exception as log_error:
            print(str(log_error))

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
            self.fillets = {}
            self.load_fillets_info()

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