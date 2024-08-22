from PyQt5.QtWidgets import QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.postprocessing.plot_structural_data import get_reactions
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

import numpy as np

class PlotReactionsForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_reactions_for_harmonic_analysis.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.load_nodes_info()

    def _initialize(self):

        [   self.reactions_at_constrained_dofs, 
            self.reactions_at_springs, 
            self.reactions_at_dampers   ] = self.project.get_structural_reactions()
        
        self.analysis_method = self.project.analysis_method_label
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.frequencies = self.model.frequencies

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_nodeID : QLineEdit

        # QPushButton
        self.pushButton_plot_data : QPushButton
        self.pushButton_export_data : QPushButton

        # QRadioButton
        self.radioButton_Fx : QRadioButton
        self.radioButton_Fy : QRadioButton
        self.radioButton_Fz : QRadioButton
        self.radioButton_Mx : QRadioButton
        self.radioButton_My : QRadioButton
        self.radioButton_Mz : QRadioButton

        self.list_radioButtons = [  self.radioButton_Fx, 
                                    self.radioButton_Fy, 
                                    self.radioButton_Fz,
                                    self.radioButton_Mx, 
                                    self.radioButton_My, 
                                    self.radioButton_Mz  ]

        # QTabWidget
        self.tabWidget_reactions : QTabWidget
        self.tabWidget_springs_dampers : QTabWidget

        # QTreeWidget
        self.treeWidget_reactions_at_springs : QTreeWidget
        self.treeWidget_reactions_at_dampers : QTreeWidget
        self.treeWidget_reactions_at_constrained_dofs : QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        #
        self.treeWidget_reactions_at_springs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_springs.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_dampers.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_dampers.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_constrained_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_constrained_dofs.itemDoubleClicked.connect(self.on_doubleclick_item)
    
    def _config_widgets(self):

        self.treeWidget_reactions_at_springs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_springs.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_dampers.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_dampers.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(2, 80)

    def text_label(self, mask):
        
        text = ""
        load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])
        labels = load_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            text = "[{}]".format(*labels)
        return text

    def load_nodes_info(self):
        
        for (property, *args), data in self.model.properties.nodal_properties.items():

            if property == "lumped_stiffness":
                node_id = args[0]
                values = data["values"]

                lumped_stiffness_mask = self.get_lumped_stiffness_mask(values)
                new = QTreeWidgetItem([str(node_id), str(self.text_label(lumped_stiffness_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_reactions_at_springs.addTopLevelItem(new)

            if property == "lumped_dampings":
                node_id = args[0]
                values = data["values"]

                lumped_dampings_mask = self.get_lumped_dampings_mask(values)
                new = QTreeWidgetItem([str(node_id), str(self.text_label(lumped_dampings_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_reactions_at_dampers.addTopLevelItem(new)
        
            if property == "prescribed_dofs":
                node_id = args[0]
                values = data["values"]

                constrained_dofs_mask = self.get_constrained_dofs_mask(values)
                if constrained_dofs_mask.count(False) != 6:         
                    new = QTreeWidgetItem([str(node_id), str(self.text_label(constrained_dofs_mask))])
                    new.setTextAlignment(0, Qt.AlignCenter)
                    new.setTextAlignment(1, Qt.AlignCenter)
                    self.treeWidget_reactions_at_constrained_dofs.addTopLevelItem(new)

    def get_lumped_dampings_mask(self, values: list) -> list:
        return [False if bc is None else True for bc in values]

    def get_lumped_stiffness_mask(self, values: list) -> list:
        return [False if bc is None else True for bc in values]

    def get_constrained_dofs_mask(self, values: list) -> list:

        constrained_dofs_mask = [False, False, False, False, False, False]
        for index, value in enumerate(values):

            if isinstance(value, complex):
                if value == complex(0):
                    constrained_dofs_mask[index] = True

            elif isinstance(value, np.ndarray):
                if np.sum(value) == complex(0):
                    constrained_dofs_mask[index] = True
                else:
                    constrained_dofs_mask[index] = False

        return constrained_dofs_mask

    def disable_non_existing_reactions(self, node_id):
        
        if self.tabWidget_reactions.currentIndex()==0:

            data = self.model.properties._get_property("prescribed_dofs", node_ids=int(node_id))
            values = data["values"]

            mask = [False, False, False, False, False, False]
            for index, value in enumerate(values):
                if isinstance(value, complex):
                    if value == complex(0):
                        mask[index] = True
                elif isinstance(value, np.ndarray):
                    if np.sum(value) == complex(0):
                        mask[index] = False
                    else:
                        mask[index] = True

            self.reactions = self.reactions_at_constrained_dofs
            self.damper = False

        elif self.tabWidget_reactions.currentIndex()==1:

            if self.tabWidget_springs_dampers.currentIndex()==0:

                data = self.model.properties._get_property("lumped_stiffness", node_ids=int(node_id))
                values = data["values"]

                mask = [False if bc is None else True for bc in values]
                self.reactions = self.reactions_at_springs
                self.damper = False

            elif self.tabWidget_springs_dampers.currentIndex()==1:

                data = self.model.properties._get_property("lumped_dampings", node_ids=int(node_id))
                values = data["values"]

                mask = [False if bc is None else True for bc in values]
                self.reactions = self.reactions_at_dampers
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
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):
        
        str_nodes = self.lineEdit_nodeID.text()
        stop, self.node_ID = self.before_run.check_selected_ids(str_nodes, "nodes", single_id=True)
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
        response = get_reactions(   self.reactions, 
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