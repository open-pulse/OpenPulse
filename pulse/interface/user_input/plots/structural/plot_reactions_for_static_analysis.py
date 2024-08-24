from PyQt5.QtWidgets import QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR

import numpy as np


class PlotReactionsForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_reactions_for_static_analysis.ui"
        uic.loadUi(ui_path, self)
        
        app().main_window.set_input_widget(self)
        self.model = app().project.model

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._load_nodes_info()
        self._config_widgets()

    def _initialize(self):

        reactions_data = app().project.get_structural_reactions()

        self.reactions_at_constrained_dofs = reactions_data.get("reactions_at_constrained_dofs", None)
        self.reactions_at_springs = reactions_data.get("reactions_at_springs", None)
        self.reactions_at_dampers = reactions_data.get("reactions_at_dampers", None)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        
        # QLineEdit
        self.lineEdit_node_id: QLineEdit
        self.lineEdit_reaction_fx: QLineEdit
        self.lineEdit_reaction_fy: QLineEdit
        self.lineEdit_reaction_fz: QLineEdit
        self.lineEdit_reaction_mx: QLineEdit
        self.lineEdit_reaction_my: QLineEdit
        self.lineEdit_reaction_mz: QLineEdit

        self.lineEdits = [  self.lineEdit_node_id,
                            self.lineEdit_reaction_fx,
                            self.lineEdit_reaction_fy,
                            self.lineEdit_reaction_fz,
                            self.lineEdit_reaction_mx,
                            self.lineEdit_reaction_my,
                            self.lineEdit_reaction_mz  ]

        # QPushButton
        self.pushButton_reset: QPushButton
        
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
        self.pushButton_reset.clicked.connect(self._reset_lineEdits)
        #
        self.treeWidget_reactions_at_constrained_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_constrained_dofs.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_dampers.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_dampers.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.treeWidget_reactions_at_springs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_springs.itemDoubleClicked.connect(self.on_doubleclick_item)

    def _config_widgets(self):

        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_dampers.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_dampers.setColumnWidth(2, 80)

        self.treeWidget_reactions_at_springs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_springs.setColumnWidth(2, 80)

    def _reset_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setText("")

    def _update_lineEdit(self, node_id: int):

        self._reset_lineEdits()
        self.lineEdit_node_id.setText(str(node_id))

        node = app().project.model.preprocessor.nodes[node_id]
        reactions = [None, None, None, None, None, None]
        print("passei 1")

        if self.tabWidget_main.currentIndex() == 0:
            print("passei 2")
            if isinstance(self.reactions_at_constrained_dofs, dict):
                print("passei 3")
                for dof_index, value in self.reactions_at_constrained_dofs.items():
                    print(dof_index, value)
                    global_dofs = list(node.global_dof)
                    if dof_index in global_dofs:
                        i = global_dofs.index(dof_index)
                        reactions[i] = value

        else:

            if self.tabWidget_springs_dampers.currentIndex() == 0:

                if isinstance(self.reactions_at_springs, dict):
                    for dof_index, value in self.reactions_at_springs.items():
                        global_dofs = list(node.global_dof)
                        if dof_index in global_dofs:
                            i = global_dofs.index(dof_index)
                            reactions[i] = value

            elif self.tabWidget_springs_dampers.currentIndex() == 1:

                if isinstance(self.reactions_at_dampers, dict):
                    for dof_index, value in self.reactions_at_dampers.items():
                        global_dofs = list(node.global_dof)
                        if dof_index in global_dofs:
                            i = global_dofs.index(dof_index)
                            reactions[i] = value        

        try:

            if reactions.count(None) != 6:
                for i, lineEdit in enumerate(self.lineEdits[1:]):
                    if reactions[i] is not None:
                        value = float(np.real(reactions[i]))
                        lineEdit.setText(f"{value : .6e}")

        except Exception as log_error:
            print(str(log_error))

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

    def _load_nodes_info(self):

        for (property, *args), data in self.model.properties.nodal_properties.items():

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

    # def get_lumped_dampings_mask(self, values: list) -> list:
    #     return [False if bc is None else True for bc in values]

    # def get_lumped_stiffness_mask(self, values: list) -> list:
    #     return [False if bc is None else True for bc in values]

    # def get_constrained_dofs_mask(self, values: list) -> list:

    #     constrained_dofs_mask = [False, False, False, False, False, False]
    #     for index, value in enumerate(values):

    #         if isinstance(value, complex):
    #             if value == complex(0):
    #                 constrained_dofs_mask[index] = True

    #         elif isinstance(value, np.ndarray):
    #             if np.sum(value) == complex(0):
    #                 constrained_dofs_mask[index] = True
    #             else:
    #                 constrained_dofs_mask[index] = False

    #     return constrained_dofs_mask

    def on_click_item(self, item):
        node_id = int(item.text(0))
        # self.lineEdit_node_id.setText(item.text(0))
        print("on_click_item deveria atualizar")
        self.plot_reactions(node_id)

    def on_doubleclick_item(self, item):
        node_id = int(item.text(0))
        # self.lineEdit_node_id.setText(item.text(0))
        print("on_click_item deveria atualizar")
        self.plot_reactions(node_id)

    def plot_reactions(self, node_id: int):
        try:
            self._update_lineEdit(node_id)
        except Exception as error_log:
            self._reset_lineEdits()
            print(str(error_log))