from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
from os.path import basename
import matplotlib.pyplot as plt

from pulse.postprocessing.plot_structural_data import get_reactions
from data.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "ERROR"
window_title_2 = "WARNING"
window_title_3 = "INFORMATION"

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

import numpy as np

class PlotStaticAnalysisReactions(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/plots_/results_/structural_/reactions_plot.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Get the static reactions")

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.preprocessor = project.preprocessor
        
        [   self.dict_reactions_at_constrained_dofs, 
            self.dict_reactions_at_springs, 
            self.dict_reactions_at_dampers   ] = project.get_structural_reactions()

        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _define_qt_variables(self):
        #
        self.lineEdit_node_id = self.findChild(QLineEdit, 'lineEdit_node_id')
        self.lineEdit_reaction_fx = self.findChild(QLineEdit, 'lineEdit_reaction_fx')
        self.lineEdit_reaction_fy = self.findChild(QLineEdit, 'lineEdit_reaction_fy')
        self.lineEdit_reaction_fz = self.findChild(QLineEdit, 'lineEdit_reaction_fz')
        self.lineEdit_reaction_mx = self.findChild(QLineEdit, 'lineEdit_reaction_mx')
        self.lineEdit_reaction_my = self.findChild(QLineEdit, 'lineEdit_reaction_my')
        self.lineEdit_reaction_mz = self.findChild(QLineEdit, 'lineEdit_reaction_mz')
        #
        self.lineEdits = [  self.lineEdit_node_id,
                            self.lineEdit_reaction_fx,
                            self.lineEdit_reaction_fy,
                            self.lineEdit_reaction_fz,
                            self.lineEdit_reaction_mx,
                            self.lineEdit_reaction_my,
                            self.lineEdit_reaction_mz  ]
        #
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        #
        self.tabWidget_reactions = self.findChild(QTabWidget, "tabWidget_reactions")
        self.tab_constrained_dofs = self.tabWidget_reactions.findChild(QWidget, "tab_constrained_dofs")
        self.tab_external_springs_dampers = self.tabWidget_reactions.findChild(QWidget, "tab_external_springs_dampers")
        
        self.tabWidget_springs_dampers = self.findChild(QTabWidget, "tabWidget_springs_dampers")
        self.tab_nodes_with_springs = self.tabWidget_springs_dampers.findChild(QWidget, "tab_nodes_with_springs")
        self.tab_nodes_with_dampers = self.tabWidget_springs_dampers.findChild(QWidget, "tab_nodes_with_dampers")

        self.treeWidget_reactions_at_constrained_dofs = self.findChild(QTreeWidget, 'treeWidget_reactions_at_constrained_dofs')
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_dampers = self.findChild(QTreeWidget, 'treeWidget_reactions_at_dampers')
        self.treeWidget_reactions_at_dampers.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_dampers.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_springs = self.findChild(QTreeWidget, 'treeWidget_reactions_at_springs')
        self.treeWidget_reactions_at_springs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_springs.setColumnWidth(2, 80)

        self._load_nodes_info()
        self._config_lineEdits()
        self._tabWidgets_visibility()

    def _create_connections(self):
        self.pushButton_reset.clicked.connect(self._reset_lineEdits)
        self.treeWidget_reactions_at_constrained_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_constrained_dofs.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_dampers.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_dampers.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_springs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_springs.itemDoubleClicked.connect(self.on_doubleclick_item)

    def _config_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setDisabled(True)
            lineEdit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")

    def _tabWidgets_visibility(self):
        self.tabWidget_springs_dampers.removeTab(1)
        if len(self.dict_reactions_at_springs) == 0:
            self.tabWidget_reactions.removeTab(1)

    def _reset_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setText("")

    def _update_lineEdit(self, node_id):

        reactions = []
        node = self.project.preprocessor.nodes[node_id]

        if self.tabWidget_reactions.currentIndex() == 0:
            dict_reactions = self.dict_reactions_at_constrained_dofs
            for dof_index, value in dict_reactions.items():
                if dof_index in node.global_dof:
                    reactions.append(value)
                else:
                    reactions.append(complex(0))

            if len(reactions) != 0:
                mask = self.get_constrained_dofs_mask(node)

        else:

            if self.tabWidget_springs_dampers.currentIndex() == 0:
                dict_reactions = self.dict_reactions_at_springs
                for dof_index, value in dict_reactions.items():
                    if dof_index in node.global_dof:
                        reactions.append(value)
                    else:
                        reactions.append(complex(0))

                if len(reactions) != 0:
                    mask = self.get_lumped_stiffness_mask(node)

            else:

                dict_reactions = self.dict_reactions_at_dampers
                for dof_index, value in dict_reactions.items():
                    if dof_index in node.global_dof:
                        reactions.append(value)
                    else:
                        reactions.append(complex(0))

                if len(reactions) != 0:
                    mask = self.get_lumped_dampings_mask(node)           
        
        try:

            if True in list(mask):
                reactions = np.real(reactions).flatten()
                for ind, lineEdit in enumerate(self.lineEdits[1:]):
                    if mask[ind]:
                        lineEdit.setText("{:.6e}".format(reactions[ind]))

        except Exception as log_error:
            print(str(log_error))


    def text_label(self, mask):
        
        text = ""
        load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])
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

    def _load_nodes_info(self):
        
        for node in self.preprocessor.nodes_connected_to_springs:
            lumped_stiffness_mask = self.get_lumped_stiffness_mask(node)
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_stiffness_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_reactions_at_springs.addTopLevelItem(new)

        for node in self.preprocessor.nodes_connected_to_dampers:
            lumped_dampings_mask = self.get_lumped_dampings_mask(node)
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_dampings_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_reactions_at_dampers.addTopLevelItem(new)

        for node in self.preprocessor.nodes_with_constrained_dofs:
            # constrained_dofs_mask = np.array(node.prescribed_dofs) == complex(0)
            constrained_dofs_mask = self.get_constrained_dofs_mask(node)
            if constrained_dofs_mask.count(False) != 6:         
                new = QTreeWidgetItem([str(node.external_index), str(self.text_label(constrained_dofs_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_reactions_at_constrained_dofs.addTopLevelItem(new)

    def get_constrained_dofs_mask(self, node):
        constrained_dofs_mask = [False, False, False, False, False, False]
        for index, value in enumerate(node.prescribed_dofs):
            if isinstance(value, complex):
                if value == complex(0):
                    constrained_dofs_mask[index] = True
            elif isinstance(value, np.ndarray):
                constrained_dofs_mask[index] = False
        return constrained_dofs_mask
        
    def get_lumped_dampings_mask(self, node):
        return [False if bc is None else True for bc in node.lumped_dampings]
        
    def get_lumped_stiffness_mask(self, node):
        return [False if bc is None else True for bc in node.lumped_stiffness]

    def on_click_item(self, item):
        self.lineEdit_node_id.setText(item.text(0))
        self.plot_reactions()

    def on_doubleclick_item(self, item):
        self.lineEdit_node_id.setText(item.text(0))
        self.plot_reactions()

    def plot_reactions(self):
        try:
            node_id = int(self.lineEdit_node_id.text())
            self._update_lineEdit(node_id)
        except:
            self._reset_lineEdits()