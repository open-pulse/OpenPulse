from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.info.structural_model_Info_ui import StructuralModelInfo_UI


import numpy as np

class StructuralModelInfo(StructuralModelInfo_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self.project = app().project

        self._config_window()
        self._initialize()
        self._create_connections()
        self._config_widgets()
        self.load_nodal_properties()
        self.load_project_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.preprocessor = app().project.model.preprocessor

    def _create_connections(self):
        pass

    def _config_widgets(self):

        for i, width in enumerate([70, 70]):
            self.treeWidget_prescribed_dof.setColumnWidth(i, width)
            self.treeWidget_constrained_dof.setColumnWidth(i, width)
            self.treeWidget_masses.setColumnWidth(i, width)
            self.treeWidget_springs.setColumnWidth(i, width)
            self.treeWidget_dampers.setColumnWidth(i, width)

            self.treeWidget_prescribed_dof.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_constrained_dof.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_masses.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_springs.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_dampers.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def text_label(self, mask, load_labels):

        text = ""
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

    def load_nodal_properties(self):

                
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "lumped_stiffness":

                node_id = args[0]
                values = data["values"]
                load_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])        
                lumped_stiffness_mask = [False if bc is None else True for bc in values]

                item = QTreeWidgetItem([str(node_id), str(self.text_label(lumped_stiffness_mask, load_labels))])
                self.treeWidget_springs.addTopLevelItem(item)

            if property == "lumped_dampings":

                node_id = args[0]
                values = data["values"]
                load_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz'])
                lumped_dampings_mask = [False if bc is None else True for bc in values]

                item = QTreeWidgetItem([str(node_id), str(self.text_label(lumped_dampings_mask, load_labels))])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_dampers.addTopLevelItem(item)

            if property == "lumped_masses":

                node_id = args[0]
                values = data["values"]
                load_labels = np.array(['m_x','m_y','m_z','Jx','Jy','Jz'])
                lumped_masses_mask = [False if bc is None else True for bc in values]

                item = QTreeWidgetItem([str(node_id), str(self.text_label(lumped_masses_mask, load_labels))])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_masses.addTopLevelItem(item)

            if property == "prescribed_dofs":

                node_id = args[0]
                values = data["values"]
                load_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])
                prescribed_dof_mask = [False, False, False, False, False, False]
                constrained_dof_mask = [False, False, False, False, False, False]

                for index, value in enumerate(values):
                    if isinstance(value, complex):
                        if value != complex(0):
                            prescribed_dof_mask[index] = True
                    elif isinstance(value, np.ndarray):
                        prescribed_dof_mask[index] = True

                if prescribed_dof_mask.count(False) != 6:    
                    item = QTreeWidgetItem([str(node_id), str(self.text_label(prescribed_dof_mask, load_labels))])
                    for i in range(2):
                        item.setTextAlignment(i, Qt.AlignCenter)
                    self.treeWidget_prescribed_dof.addTopLevelItem(item)

                for index, value in enumerate(values):
                    if isinstance(value, complex):
                        if value == complex(0):
                            constrained_dof_mask[index] = True
                    elif isinstance(value, np.ndarray):
                        constrained_dof_mask[index] = False

                if constrained_dof_mask.count(False) != 6:    
                    item = QTreeWidgetItem([str(node_id), str(self.text_label(constrained_dof_mask, load_labels))])
                    for i in range(2):
                        item.setTextAlignment(i, Qt.AlignCenter)
                    self.treeWidget_constrained_dof.addTopLevelItem(item)

            if property == "nodal_loads":

                node_id = args[0]
                values = data["values"]
                load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])
                nodal_loads_mask = [False if bc is None else True for bc in values]

                item = QTreeWidgetItem([str(node_id), str(self.text_label(nodal_loads_mask, load_labels))])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_nodal_loads.addTopLevelItem(item)

    def load_project_info(self):
        self.lineEdit_number_nodes.setText(str(len(self.preprocessor.nodes)))
        self.lineEdit_number_elements.setText(str(self.preprocessor.number_structural_elements))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F3:
            self.close()