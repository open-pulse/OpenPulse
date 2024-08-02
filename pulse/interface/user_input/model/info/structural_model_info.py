from PyQt5.QtWidgets import QDialog, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np

from pulse import UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon

class StructuralModelInfo(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/info/structural_model_Info.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        app().main_window.set_input_widget(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_nodes_info()
        self.project_info()
        self._load_icons()
        self._config_window()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.preprocessor = self.project.preprocessor

    def _define_qt_variables(self):
        # QLineEdit
        self.lineEdit_number_nodes : QLineEdit
        self.lineEdit_number_elements : QLineEdit
        # QTreeWidget
        self.treeWidget_prescribed_dofs : QTreeWidget
        self.treeWidget_constrained_dofs : QTreeWidget
        self.treeWidget_nodal_loads : QTreeWidget
        self.treeWidget_masses : QTreeWidget
        self.treeWidget_springs : QTreeWidget
        self.treeWidget_dampers : QTreeWidget

    def _create_connections(self):
        pass

    def _config_widgets(self):

        self.treeWidget_prescribed_dofs.setColumnWidth(1, 20)
        self.treeWidget_prescribed_dofs.setColumnWidth(2, 80)
        
        self.treeWidget_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_constrained_dofs.setColumnWidth(2, 80)

        self.treeWidget_nodal_loads.setColumnWidth(1, 20)
        self.treeWidget_nodal_loads.setColumnWidth(2, 80)

        self.treeWidget_masses.setColumnWidth(1, 20)
        self.treeWidget_masses.setColumnWidth(2, 80)

        self.treeWidget_springs.setColumnWidth(1, 20)
        self.treeWidget_springs.setColumnWidth(2, 80)

        self.treeWidget_dampers.setColumnWidth(1, 20)
        self.treeWidget_dampers.setColumnWidth(2, 80)

    def project_info(self):
        self.lineEdit_number_nodes.setText(str(len(self.project.preprocessor.nodes)))
        self.lineEdit_number_elements.setText(str(len(self.project.preprocessor.structural_elements)))
        
    def text_label(self, mask, load_labels):
        
        text = ""
        temp = load_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4])
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3])
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(temp[0], temp[1], temp[2])
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(temp[0], temp[1])
        elif list(mask).count(True) == 1:
            text = "[{}]".format(temp[0])
        return text

    def load_nodes_info(self):

        load_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])        
        for node in self.project.preprocessor.nodes_connected_to_springs:
            lumped_stiffness_mask = [False if bc is None else True for bc in node.lumped_stiffness]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_stiffness_mask, load_labels))])
            self.treeWidget_springs.addTopLevelItem(new)

        load_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz'])
        for node in self.project.preprocessor.nodes_connected_to_dampers:
            lumped_dampings_mask = [False if bc is None else True for bc in node.lumped_dampings]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_dampings_mask, load_labels))])
            self.treeWidget_dampers.addTopLevelItem(new)

        load_labels = np.array(['m_x','m_y','m_z','Jx','Jy','Jz'])
        for node in self.project.preprocessor.nodes_with_masses:
            lumped_masses_mask = [False if bc is None else True for bc in node.lumped_masses]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_masses_mask, load_labels))])
            self.treeWidget_masses.addTopLevelItem(new)

        load_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])
        for node in self.project.preprocessor.nodes_with_prescribed_dofs:
            prescribed_dofs_mask = [False, False, False, False, False, False]
            for index, value in enumerate(node.prescribed_dofs):
                if isinstance(value, complex):
                    if value != complex(0):
                        prescribed_dofs_mask[index] = True
                elif isinstance(value, np.ndarray):
                    prescribed_dofs_mask[index] = True
            # prescribed_dofs_mask = [False if bc == complex(0) or bc is None else True for bc in node.prescribed_dofs]
            if prescribed_dofs_mask.count(False) != 6:    
                new = QTreeWidgetItem([str(node.external_index), str(self.text_label(prescribed_dofs_mask, load_labels))])
                self.treeWidget_prescribed_dofs.addTopLevelItem(new)
            
        for node in self.project.preprocessor.nodes_with_constrained_dofs:
            # constrained_dofs_mask = np.array(node.prescribed_dofs) == complex(0)
            constrained_dofs_mask = [False, False, False, False, False, False]
            for index, value in enumerate(node.prescribed_dofs):
                if isinstance(value, complex):
                    if value == complex(0):
                        constrained_dofs_mask[index] = True
                elif isinstance(value, np.ndarray):
                    constrained_dofs_mask[index] = False
            if constrained_dofs_mask.count(False) != 6:    
                new = QTreeWidgetItem([str(node.external_index), str(self.text_label(constrained_dofs_mask, load_labels))])
                self.treeWidget_constrained_dofs.addTopLevelItem(new)

        load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])
        for node in self.project.preprocessor.nodes_with_nodal_loads:
            nodal_loads_mask = [False if bc is None else True for bc in node.nodal_loads]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(nodal_loads_mask, load_labels))])
            self.treeWidget_nodal_loads.addTopLevelItem(new)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F3:
            self.close()