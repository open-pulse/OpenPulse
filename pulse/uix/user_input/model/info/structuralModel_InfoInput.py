import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox, QCheckBox, QTreeWidget
from pulse.utils import error, info_messages, remove_bc_from_file
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile

class StructuralModelInfoInput(QDialog):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/Model/Info/structuralModel_Info.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project

        self.lineEdit_number_nodes = self.findChild(QLineEdit, 'lineEdit_number_nodes')
        self.lineEdit_number_elements = self.findChild(QLineEdit, 'lineEdit_number_elements')

        self.treeWidget_prescribed_dofs = self.findChild(QTreeWidget, 'treeWidget_prescribed_dofs')
        self.treeWidget_prescribed_dofs.setColumnWidth(1, 20)
        self.treeWidget_prescribed_dofs.setColumnWidth(2, 80)

        self.treeWidget_constrained_dofs = self.findChild(QTreeWidget, 'treeWidget_constrained_dofs')
        self.treeWidget_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_constrained_dofs.setColumnWidth(2, 80)

        self.treeWidget_nodal_loads = self.findChild(QTreeWidget, 'treeWidget_nodal_loads')
        self.treeWidget_nodal_loads.setColumnWidth(1, 20)
        self.treeWidget_nodal_loads.setColumnWidth(2, 80)

        self.treeWidget_masses = self.findChild(QTreeWidget, 'treeWidget_masses')
        self.treeWidget_masses.setColumnWidth(1, 20)
        self.treeWidget_masses.setColumnWidth(2, 80)

        self.treeWidget_springs = self.findChild(QTreeWidget, 'treeWidget_springs')
        self.treeWidget_springs.setColumnWidth(1, 20)
        self.treeWidget_springs.setColumnWidth(2, 80)

        self.treeWidget_dampers = self.findChild(QTreeWidget, 'treeWidget_dampers')
        self.treeWidget_dampers.setColumnWidth(1, 20)
        self.treeWidget_dampers.setColumnWidth(2, 80)

        self.load_nodes_info()
        self.project_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F3:
            self.close()

    def project_info(self):
        self.lineEdit_number_nodes.setText(str(len(self.project.mesh.nodes)))
        self.lineEdit_number_elements.setText(str(len(self.project.mesh.structural_elements)))
        
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
        for node in self.project.mesh.nodes_connected_to_springs:
            lumped_stiffness_mask = [False if bc is None else True for bc in node.lumped_stiffness]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_stiffness_mask, load_labels))])
            self.treeWidget_springs.addTopLevelItem(new)

        load_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz'])
        for node in self.project.mesh.nodes_connected_to_dampers:
            lumped_dampings_mask = [False if bc is None else True for bc in node.lumped_dampings]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_dampings_mask, load_labels))])
            self.treeWidget_dampers.addTopLevelItem(new)

        load_labels = np.array(['m_x','m_y','m_z','Jx','Jy','Jz'])
        for node in self.project.mesh.nodes_with_masses:
            lumped_masses_mask = [False if bc is None else True for bc in node.lumped_masses]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_masses_mask, load_labels))])
            self.treeWidget_masses.addTopLevelItem(new)

        load_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])
        for node in self.project.mesh.nodes_with_prescribed_dofs:
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
            
        for node in self.project.mesh.nodes_with_constrained_dofs:
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
        for node in self.project.mesh.nodes_with_nodal_loads:
            nodal_loads_mask = [False if bc is None else True for bc in node.nodal_loads]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(nodal_loads_mask, load_labels))])
            self.treeWidget_nodal_loads.addTopLevelItem(new)