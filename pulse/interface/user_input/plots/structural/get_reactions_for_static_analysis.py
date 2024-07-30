from PyQt5.QtWidgets import QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np
from pathlib import Path

class GetReactionsForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_reactions_for_static_analysis.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        app().main_window.input_widget.set_input_widget(self)

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._load_nodes_info()
        self._config_widgets()

    def _initialize(self):
        [   self.dict_reactions_at_constrained_dofs, 
            self.dict_reactions_at_springs, 
            self.dict_reactions_at_dampers   ] = self.project.get_structural_reactions()
        
        self.preprocessor = self.project.preprocessor

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Get the static reactions")
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):
        
        # QLineEdit
        self.lineEdit_node_id : QLineEdit
        self.lineEdit_reaction_fx : QLineEdit
        self.lineEdit_reaction_fy : QLineEdit
        self.lineEdit_reaction_fz : QLineEdit
        self.lineEdit_reaction_mx : QLineEdit
        self.lineEdit_reaction_my : QLineEdit
        self.lineEdit_reaction_mz : QLineEdit

        self.lineEdits = [  self.lineEdit_node_id,
                            self.lineEdit_reaction_fx,
                            self.lineEdit_reaction_fy,
                            self.lineEdit_reaction_fz,
                            self.lineEdit_reaction_mx,
                            self.lineEdit_reaction_my,
                            self.lineEdit_reaction_mz  ]

        # QPushButton
        self.pushButton_reset : QPushButton
        
        # QTabWidget
        self.tabWidget_reactions : QTabWidget    
        self.tabWidget_springs_dampers : QTabWidget

        # QTreeWidget        
        self.treeWidget_reactions_at_constrained_dofs : QTreeWidget
        self.treeWidget_reactions_at_dampers : QTreeWidget
        self.treeWidget_reactions_at_springs : QTreeWidget

    def _create_connections(self):
        self.pushButton_reset.clicked.connect(self._reset_lineEdits)
        self.treeWidget_reactions_at_constrained_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_constrained_dofs.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_dampers.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_dampers.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_springs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_springs.itemDoubleClicked.connect(self.on_doubleclick_item)
        self._tabWidgets_visibility()

    def _config_widgets(self):

        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_dampers.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_dampers.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_springs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_springs.setColumnWidth(2, 80)

    def _tabWidgets_visibility(self):
        self.tabWidget_springs_dampers.removeTab(1)
        if len(self.dict_reactions_at_springs) == 0:
            self.tabWidget_reactions.removeTab(1)

    def _reset_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setText("")

    def _update_lineEdit(self, node_id):

        self._reset_lineEdits()
        self.lineEdit_node_id.setText(str(node_id))
        node = self.project.preprocessor.nodes[node_id]
        reactions = [None, None, None, None, None, None]

        if self.tabWidget_reactions.currentIndex() == 0:
            dict_reactions = self.dict_reactions_at_constrained_dofs
            for dof_index, value in dict_reactions.items():
                global_dofs = list(node.global_dof)
                if dof_index in global_dofs:
                    i = global_dofs.index(dof_index)
                    reactions[i] = value
            mask = self.get_constrained_dofs_mask(node)

        else:

            if self.tabWidget_springs_dampers.currentIndex() == 0:
                dict_reactions = self.dict_reactions_at_springs
                for dof_index, value in dict_reactions.items():
                    global_dofs = list(node.global_dof)
                    if dof_index in global_dofs:
                        i = global_dofs.index(dof_index)
                        reactions[i] = value
                mask = self.get_lumped_stiffness_mask(node)

            else:

                dict_reactions = self.dict_reactions_at_dampers
                for dof_index, value in dict_reactions.items():
                    global_dofs = list(node.global_dof)
                    if dof_index in global_dofs:
                        i = global_dofs.index(dof_index)
                        reactions[i] = value
                mask = self.get_lumped_dampings_mask(node)           
        
        try:

            if True in list(mask):
                for ind, lineEdit in enumerate(self.lineEdits[1:]):
                    if mask[ind]:
                        value = float(np.real(reactions[ind]))
                        lineEdit.setText("{:.6e}".format(value))

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