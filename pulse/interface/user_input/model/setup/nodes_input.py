from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.user_input.model.setup.user_input import UserInput


class NodesInput(UserInput):
    def __init__(self):
        super().__init__()

        self.properties = app().project.model.properties
        self.before_run = app().project.get_pre_solution_model_checks()


    def remove_conflicting_data(
        self, properties: str | list[str], node_ids: int | list | tuple
    ):
        if isinstance(node_ids, int):
            node_ids = [node_ids]

        if isinstance(properties, str):
            properties = [properties]

        for node_id in node_ids:
            for _property in properties:
                table_names = self.properties.get_nodal_related_table_names(
                    _property, node_id
                )
                self.properties._remove_nodal_property(_property, node_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_nodes(self, properties: str | list[str], node_id: int):
        if isinstance(properties, str):
            properties = [properties]

        for property in properties:
            table_names = self.properties.get_nodal_related_table_names(
                property, node_id
            )
            self.process_table_file_removal(table_names)

    def process_table_file_removal(self, group_label: str, table_names: list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables(group_label, table_name)
            app().project.file.write_imported_table_data_in_file()

    def actions_to_finalize(self, reset_camera: bool = True):
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
        app().main_window.update_plots(reset_camera)
        self.load_nodes_info()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Enter:
            self.remove_callback()
        if event.key() == Qt.Key_Escape:
            self.close()
