from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

class TreeWidget(QTreeWidget):
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
        hiden_data = QTreeWidgetItem(["Hidden Data"])
        
        mesh = QTreeWidgetItem(["Mesh"])
        generate = QTreeWidgetItem(["Generate"])
        list_of_nodes = QTreeWidgetItem(["List of Nodes"])
        list_of_connections = QTreeWidgetItem(['List of Connections'])

        graphic = QTreeWidgetItem(["Graphic"])
        plot = QTreeWidgetItem(['Plot Config'])

        pre_processing = QTreeWidgetItem(["Pre-Processing"])
        pre_processing_material = QTreeWidgetItem(["Set Material"])
        pre_processing_cross = QTreeWidgetItem(["Set Cross Section"])
        pre_processing_dof = QTreeWidgetItem(["Set DOF"])
        pre_processing_dof_import = QTreeWidgetItem(["Import DOF"])

        mesh.addChild(generate)
        mesh.addChild(list_of_nodes)
        mesh.addChild(list_of_connections)
        graphic.addChild(plot)
        pre_processing.addChild(pre_processing_material)
        pre_processing.addChild(pre_processing_cross)
        pre_processing.addChild(pre_processing_dof)
        pre_processing.addChild(pre_processing_dof_import)

        self.addTopLevelItem(hiden_data)
        self.addTopLevelItem(mesh)
        self.addTopLevelItem(graphic)
        self.addTopLevelItem(pre_processing)

    def on_click_item(self, item, column):
        if item.text(0) == "Generate":
            self.main_window.info_widget.generate()

        elif item.text(0) == "Hidden Data":
            self.main_window.info_widget.hidden_data()
        
        elif item.text(0) == "Plot Config":
            self.main_window.info_widget.plot_config()
        
        elif item.text(0) == "List of Nodes":
            self.main_window.info_widget.list_of_nodes()
        
        elif item.text(0) == "List of Connections":
            self.main_window.info_widget.list_of_connections()

        elif item.text(0) == "Set Material":
            self.main_window.inputWidget.material_input()

        elif item.text(0) == "Set Cross Section":
            self.main_window.inputWidget.cross_input()

        elif item.text(0) == "Set DOF":
            self.main_window.inputWidget.dof_input()

        elif item.text(0) == "Import DOF":
            self.main_window.inputWidget.import_dof()

        