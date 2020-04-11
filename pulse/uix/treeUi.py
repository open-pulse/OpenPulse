from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor
from pulse.uix.matplotlib.frf import FRF

class TreeUi(QTreeWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._set_config()
        self._create_itens()

    def _set_config(self):
        self.setColumnCount(1)
        self.setHeaderLabels(["OpenPulse"])
        self.itemClicked.connect(self.on_click_item)

    def _create_itens(self):
        #Hidden data
        hiden_data = QTreeWidgetItem(["Hidden Data"])
        
        #Mesh - Possivelmente será removido
        mesh = QTreeWidgetItem(["Mesh"])
        generate = QTreeWidgetItem(["Generate"])
        list_of_nodes = QTreeWidgetItem(["List of Nodes"])
        list_of_connections = QTreeWidgetItem(['List of Connections'])

        #PreProcessing
        pre_processing = QTreeWidgetItem(["Pre-Processing"])
        pre_processing_material = QTreeWidgetItem(["Set Material"])
        pre_processing_cross = QTreeWidgetItem(["Set Cross Section"])
        pre_processing_dof = QTreeWidgetItem(["Set DOF"])
        pre_processing_dof_node = QTreeWidgetItem(["Set DOF NodeID"])
        pre_processing_dof_import = QTreeWidgetItem(["Import DOF"])
        pre_processing_force = QTreeWidgetItem(["Set Force"])
        pre_processing_force_node = QTreeWidgetItem(["Set Force NodeID"])
        #Preprocessing - Temporário
        pre_processing_temp_set_all_material = QTreeWidgetItem(["Set Material <All>"])
        pre_processing_temp_set_all_cross = QTreeWidgetItem(["Set Cross Section <All>"])

        #Grafic - COnfiguração de plot
        graphic = QTreeWidgetItem(["Graphic"])
        graphic_direct = QTreeWidgetItem(['Direct'])
        graphic_modal = QTreeWidgetItem(['Modal'])

        #Assembly
        assembly = QTreeWidgetItem(["Assembly"])
        assembly_get_global_matrices = QTreeWidgetItem(["Global Matrices"])

        #Graph Plots
        matplot_graph = QTreeWidgetItem(["Matplotlib"])
        matplot_graph_frf = QTreeWidgetItem(["FRF"])

        #Desativados
        mesh.setDisabled(True)
        generate.setDisabled(True)
        #graphic.setDisabled(True)
        assembly.setDisabled(True)
        hiden_data.setDisabled(True)
        pre_processing_dof_import.setDisabled(True)

        mesh.addChild(generate)
        mesh.addChild(list_of_nodes)
        mesh.addChild(list_of_connections)
        pre_processing.addChild(pre_processing_material)
        pre_processing.addChild(pre_processing_cross)
        pre_processing.addChild(pre_processing_dof)
        pre_processing.addChild(pre_processing_dof_node)
        pre_processing.addChild(pre_processing_dof_import)
        pre_processing.addChild(pre_processing_force)
        pre_processing.addChild(pre_processing_force_node)
        pre_processing.addChild(pre_processing_temp_set_all_material)
        pre_processing.addChild(pre_processing_temp_set_all_cross)
        graphic.addChild(graphic_direct)
        graphic.addChild(graphic_modal)
        assembly.addChild(assembly_get_global_matrices)

        matplot_graph.addChild(matplot_graph_frf)

        self.addTopLevelItem(hiden_data)
        self.addTopLevelItem(mesh)
        self.addTopLevelItem(pre_processing)
        self.addTopLevelItem(graphic)
        self.addTopLevelItem(assembly)
        self.addTopLevelItem(matplot_graph)

        pre_processing.setExpanded(True)
        assembly.setExpanded(True)
        matplot_graph.setExpanded(True)

    def on_click_item(self, item, column):
        if item.text(0) == "Generate":
            return
            self.main_window.getInfoWidget().generate()

        elif item.text(0) == "Hidden Data":
            return
            self.main_window.getInfoWidget().hidden_data()
        
        elif item.text(0) == "Plot Config":
            return
            self.main_window.getInfoWidget().plot_config()
        
        elif item.text(0) == "List of Nodes":
            return
            self.main_window.getInfoWidget().list_of_nodes()
        
        elif item.text(0) == "List of Connections":
            return
            self.main_window.getInfoWidget().list_of_connections()

        elif item.text(0) == "Set Material":
            self.main_window.getInputWidget().material_list()

        elif item.text(0) == "Set Cross Section":
            self.main_window.getInputWidget().cross_input()

        elif item.text(0) == "Set DOF":
            self.main_window.getInputWidget().dof_input()

        elif item.text(0) == "Set DOF NodeID":
            self.main_window.getInputWidget().dof_input_node()

        elif item.text(0) == "Import DOF":
            self.main_window.getInputWidget().import_dof()

        elif item.text(0) == "Set Force":
            self.main_window.getInputWidget().force_input()

        elif item.text(0) == "Set Force NodeID":
            self.main_window.getInputWidget().force_input_node()

        elif item.text(0) == "Set Material <All>":
            self.main_window.getInputWidget().define_material_all()

        elif item.text(0) == "Set Cross Section <All>":
            self.main_window.getInputWidget().define_cross_all()

        elif item.text(0) == "Global Matrices":
            self.main_window.getInputWidget().preProcessingInfo()

        elif item.text(0) == "FRF":
            frf = FRF(self.main_window.getProject())
            frf.show()

        elif item.text(0) == "Direct":
            pass

        elif item.text(0) == "Modal":
            pass