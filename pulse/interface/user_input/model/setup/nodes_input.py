from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.user_input.model.setup.user_input import UserInput


class NodesInput(UserInput):
    def __init__(self):
        super().__init__()

        self.properties = app().project.model.properties
        self.before_run = app().project.get_pre_solution_model_checks()

    def remove_properties_from_node(self, node_ids: int | list | tuple, properties: str | list, all_dof_free: bool=False):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        if isinstance(properties, str):
            properties = [properties]

        for _property in properties:
            self.properties._remove_nodal_property(_property, node_ids)

        app().project.file.write_nodal_properties_in_file()

    def actions_to_finalize(self, reset_camera: bool = True):
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
        self.load_nodes_info()
        app().main_window.update_plots(reset_camera)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Enter:
            self.remove_callback()
        if event.key() == Qt.Key_Escape:
            self.close()
