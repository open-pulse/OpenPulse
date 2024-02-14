from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse.postprocessing.plot_structural_data import get_reactions
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class PlotReactions(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/structural_/plot_reactions_for_harmonic_analysis.ui'), self)
        
        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.analysis_method = project.analysis_method_label
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        self.frequencies = project.frequencies
        
        self._config_window()
        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_nodes_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.update_icon = QIcon(get_icons_path('update_icon.jpg'))
        self.setWindowIcon(self.pulse_icon)

    def _reset_variables(self):
        #
        [   self.dict_reactions_at_constrained_dofs, 
            self.dict_reactions_at_springs, 
            self.dict_reactions_at_dampers   ] = self.project.get_structural_reactions()

    def _define_qt_variables(self):
        # QLineEdit
        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID') 
        # QPushButton
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        # QRadioButton
        self.radioButton_Fx = self.findChild(QRadioButton, 'radioButton_Fx')
        self.radioButton_Fy = self.findChild(QRadioButton, 'radioButton_Fy')
        self.radioButton_Fz = self.findChild(QRadioButton, 'radioButton_Fz')
        self.radioButton_Mx = self.findChild(QRadioButton, 'radioButton_Mx')
        self.radioButton_My = self.findChild(QRadioButton, 'radioButton_My')
        self.radioButton_Mz = self.findChild(QRadioButton, 'radioButton_Mz')
        self.list_radioButtons = [  self.radioButton_Fx, self.radioButton_Fy, self.radioButton_Fz,
                                    self.radioButton_Mx, self.radioButton_My, self.radioButton_Mz   ]
        # QTabWidget
        self.tabWidget_reactions = self.findChild(QTabWidget, "tabWidget_reactions")
        self.tabWidget_springs_dampers = self.findChild(QTabWidget, "tabWidget_springs_dampers")
        # QWidget
        self.tab_constrained_dofs = self.tabWidget_reactions.findChild(QWidget, "tab_constrained_dofs")
        self.tab_external_springs_dampers = self.tabWidget_reactions.findChild(QWidget, "tab_external_springs_dampers")
        self.tab_nodes_with_springs = self.tabWidget_springs_dampers.findChild(QWidget, "tab_nodes_with_springs")
        self.tab_nodes_with_dampers = self.tabWidget_springs_dampers.findChild(QWidget, "tab_nodes_with_dampers")
        # QTreeWidget
        self.treeWidget_reactions_at_springs = self.findChild(QTreeWidget, 'treeWidget_reactions_at_springs')
        self.treeWidget_reactions_at_springs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_springs.setColumnWidth(2, 80)
        self.treeWidget_reactions_at_dampers = self.findChild(QTreeWidget, 'treeWidget_reactions_at_dampers')
        self.treeWidget_reactions_at_dampers.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_dampers.setColumnWidth(2, 80)
        self.treeWidget_reactions_at_constrained_dofs = self.findChild(QTreeWidget, 'treeWidget_reactions_at_constrained_dofs')
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
        #
        self.treeWidget_reactions_at_springs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_springs.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_dampers.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_dampers.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_constrained_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_constrained_dofs.itemDoubleClicked.connect(self.on_doubleclick_item)
    
    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

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

    def load_nodes_info(self):
        
        for node in self.preprocessor.nodes_connected_to_springs:
            lumped_stiffness_mask = [False if bc is None else True for bc in node.lumped_stiffness]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_stiffness_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_reactions_at_springs.addTopLevelItem(new)

        for node in self.preprocessor.nodes_connected_to_dampers:
            lumped_dampings_mask = [False if bc is None else True for bc in node.lumped_dampings]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_dampings_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_reactions_at_dampers.addTopLevelItem(new)

        for node in self.preprocessor.nodes_with_constrained_dofs:
            constrained_dofs_mask = [False, False, False, False, False, False]
            for index, value in enumerate(node.prescribed_dofs):
                if isinstance(value, complex):
                    if value == complex(0):
                        constrained_dofs_mask[index] = True
                elif isinstance(value, np.ndarray):
                    constrained_dofs_mask[index] = False

            if constrained_dofs_mask.count(False) != 6:         
                new = QTreeWidgetItem([str(node.external_index), str(self.text_label(constrained_dofs_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_reactions_at_constrained_dofs.addTopLevelItem(new)

    def disable_non_existing_reactions(self, node_id):

        node = self.preprocessor.nodes[int(node_id)]
        if self.tabWidget_reactions.currentIndex()==0:
            mask = [False, False, False, False, False, False]
            for index, value in enumerate(node.prescribed_dofs):
                if isinstance(value, complex):
                    if value == complex(0):
                        mask[index] = True
                elif isinstance(value, np.ndarray):
                    mask[index] = True

            self.reactions = self.dict_reactions_at_constrained_dofs
            self.damper = False

        elif self.tabWidget_reactions.currentIndex()==1:
            if self.tabWidget_springs_dampers.currentIndex()==0:
                mask = [False if bc is None else True for bc in node.lumped_stiffness]
                self.reactions = self.dict_reactions_at_springs
                self.damper = False

            elif self.tabWidget_springs_dampers.currentIndex()==1:
                mask = [False if bc is None else True for bc in node.lumped_dampings]
                self.reactions = self.dict_reactions_at_dampers
                self.damper = True

        list_disabled_buttons = []
        for index, radioButton in enumerate(self.list_radioButtons):
            radioButton.setDisabled(not mask[index])
            if not radioButton.isEnabled():
                list_disabled_buttons.append(radioButton)

        if len(list_disabled_buttons) > 0:
            for radioButton in self.list_radioButtons:
                if radioButton.isEnabled():
                    radioButton.setChecked(True)
                    break

    def on_click_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.disable_non_existing_reactions(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.call_plotter()      

    def call_plotter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_data_to_plot(self.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):
        
        lineEdit_nodeID = self.lineEdit_nodeID.text()
        stop, self.node_ID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if stop:
            return True

        self.local_dof = None
        if self.radioButton_Fx.isChecked():
            self.local_dof = 0
            self.local_dof_label = "Fx"
            self.unit_label = "N"
            self.reaction_label = "Force reactions"

        if self.radioButton_Fy.isChecked():
            self.local_dof = 1
            self.local_dof_label = "Fy"
            self.unit_label = "N"
            self.reaction_label = "Force reactions"

        if self.radioButton_Fz.isChecked():
            self.local_dof = 2
            self.local_dof_label = "Fz"
            self.unit_label = "N"
            self.reaction_label = "Force reactions"
 
        if self.radioButton_Mx.isChecked():
            self.local_dof = 3
            self.local_dof_label = "Mx"
            self.unit_label = "N.m"
            self.reaction_label = "Moment reactions"

        if self.radioButton_My.isChecked():
            self.local_dof = 4
            self.local_dof_label = "My"
            self.unit_label = "N.m"
            self.reaction_label = "Moment reactions"

        if self.radioButton_Mz.isChecked():
            self.local_dof = 5
            self.local_dof_label = "Mz"
            self.unit_label = "N.m"
            self.reaction_label = "Moment reactions"

    def get_reactions(self):
        response = get_reactions(   self.preprocessor, 
                                    self.reactions, 
                                    self.node_ID, 
                                    self.local_dof   )
        return response

    def join_model_data(self):
        self.model_results = dict()
        self.title = "Structural frequency response - {}".format(self.analysis_method)
        legend_label = "Reaction {} at node {}".format(self.local_dof_label, self.node_ID)
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_reactions(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : "Reaction",
                                "title" : self.title,
                                "data_information" : legend_label,
                                "legend" : legend_label,
                                "unit" : self.unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()