from PySide6.QtWidgets import QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.postprocessing.plot_structural_data import get_reactions
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.interface.user_input.project.loading_window import LoadingWindow

from molde import load_ui

import logging
import numpy as np

class PlotReactionsForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_reactions_for_harmonic_analysis.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)

        self.before_run = app().project.get_pre_solution_model_checks()

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._load_structural_solver_and_reactions()
        self._load_nodes_info()

    def _initialize(self):
        pass

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_node_id : QLineEdit

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
        self.tabWidget_main: QTabWidget
        self.tabWidget_springs_dampers: QTabWidget

        # QTreeWidget
        self.treeWidget_reactions_at_constrained_dofs: QTreeWidget
        self.treeWidget_reactions_at_dampers: QTreeWidget
        self.treeWidget_reactions_at_springs: QTreeWidget

        # QWidget
        self.tab_external_springs_dampers: QWidget
        self.tab_constrained_dofs: QWidget
        self.tab_reactions_at_springs: QWidget
        self.tab_reactions_at_dampers: QWidget

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

    def _load_structural_solver_and_reactions(self):

        if app().project.structural_solver is None:

            def solver_callback():

                logging.info("Processing the cross-sections [5%]")
                app().project.model.preprocessor.process_cross_sections_mapping()

                logging.info("Processing global matrices [50%]")
                app().project.structural_solver = app().project.get_structural_solver()

                logging.info("Processing global matrices [100%]")

                if app().project.structural_solver.solution is None:
                    app().project.structural_solver.solution = app().project.structural_solution

                logging.info("Evaluating the structural reactions [20%]")
                app().project.calculate_structural_reactions()

            LoadingWindow(solver_callback).run()

        reactions_data = app().project.get_structural_reactions()

        self.reactions_at_constrained_dofs = reactions_data.get("reactions_at_constrained_dofs", None)
        self.reactions_at_springs = reactions_data.get("reactions_at_springs", None)
        self.reactions_at_dampers = reactions_data.get("reactions_at_dampers", None)

    def _load_nodes_info(self):

        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "lumped_stiffness":
                node_id = args[0]
                values = data["values"]

                lumped_stiffness_mask = self.get_mask_for_values(values)
                if lumped_stiffness_mask.count(False) != 6: 
                    item = QTreeWidgetItem([str(node_id), str(self.text_label(lumped_stiffness_mask))])
                    for i in range(2):
                        item.setTextAlignment(i, Qt.AlignCenter)
                    self.treeWidget_reactions_at_springs.addTopLevelItem(item)

            if property == "lumped_dampings":
                node_id = args[0]
                values = data["values"]

                lumped_dampings_mask = self.get_mask_for_values(values)
                if lumped_dampings_mask.count(False) != 6: 
                    item = QTreeWidgetItem([str(node_id), str(self.text_label(lumped_dampings_mask))])
                    for i in range(2):
                        item.setTextAlignment(i, Qt.AlignCenter)
                    self.treeWidget_reactions_at_dampers.addTopLevelItem(item)

            if property == "prescribed_dofs":
                node_id = args[0]
                values = data["values"]

                constrained_dofs_mask = self.get_mask_for_values(values)
                if constrained_dofs_mask.count(False) != 6:         
                    item = QTreeWidgetItem([str(node_id), str(self.text_label(constrained_dofs_mask))])
                    for i in range(2):
                        item.setTextAlignment(i, Qt.AlignCenter)
                    self.treeWidget_reactions_at_constrained_dofs.addTopLevelItem(item)

        self._tabWidgets_visibility()

    def _tabWidgets_visibility(self):

        check_1 = self.reactions_at_constrained_dofs is None
        self.tab_constrained_dofs.setDisabled(check_1)
        
        check_2 = self.reactions_at_springs is None
        self.tab_reactions_at_springs.setDisabled(check_2)

        check_3 = self.reactions_at_dampers is None
        self.tab_reactions_at_dampers.setDisabled(check_3)

    def get_mask_for_values(self, values: list) -> list:
        return [False if value is None else True for value in values]

    def disable_non_existing_reactions(self, node_id):
        
        if self.tabWidget_main.currentIndex()==0:

            data = app().project.model.properties._get_property("prescribed_dofs", node_ids=int(node_id))
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

        elif self.tabWidget_main.currentIndex()==1:

            if self.tabWidget_springs_dampers.currentIndex()==0:

                data = app().project.model.properties._get_property("lumped_stiffness", node_ids=int(node_id))
                values = data["values"]

                mask = [False if bc is None else True for bc in values]
                self.reactions = self.reactions_at_springs
                self.damper = False

            elif self.tabWidget_springs_dampers.currentIndex()==1:

                data = app().project.model.properties._get_property("lumped_dampings", node_ids=int(node_id))
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
        self.lineEdit_node_id.setText(item.text(0))
        self.disable_non_existing_reactions(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_node_id.setText(item.text(0))
        self.call_plotter()

    def call_plotter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(app().project.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(app().project.model_results)

    def check_inputs(self):
        
        str_nodes = self.lineEdit_node_id.text()
        stop, self.node_id = self.before_run.check_selected_ids(str_nodes, "nodes", single_id=True)
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
        return get_reactions(self.reactions, self.node_id, self.local_dof)

    def join_model_data(self):

        app().project.model_results = dict()
        analysis_method = app().project.analysis_method_label
        self.title = f"Structural frequency response - {analysis_method}"
        legend_label = f"Reaction {self.local_dof_label} at node {self.node_id}"

        key = ("node", self.node_id)
        app().project.model_results[key] = {
                                    "x_data" : app().project.model.frequencies,
                                    "y_data" : self.get_reactions(),
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : "Reaction",
                                    "title" : self.title,
                                    "data_information" : legend_label,
                                    "legend" : legend_label,
                                    "unit" : self.unit_label,
                                    "color" : self.get_color(0),
                                    "linestyle" : "-"  
                                    }

    def get_color(self, index):

        colors = [  (0,0,1), 
                    (0,0,0), 
                    (1,0,0),
                    (0,1,1), 
                    (1,0,1), 
                    (1,1,0),
                    (0.25,0.25,0.25)  ]
        
        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()