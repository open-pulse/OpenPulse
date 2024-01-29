from PyQt5.QtGui import QCloseEvent
from opps.interface.widgets import AddStructuresWidget, EditStructuresWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt


class CreateEditStructuresWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent.parent
        self.configure_window()

        self.add_structure_widget = AddStructuresWidget(self.main_window.geometry_widget, self)
        self.edit_structure_widget = EditStructuresWidget(self.main_window.geometry_widget, self)
        
        # self.main_window.plot_geometry_editor()

        self.addTab(self.add_structure_widget, "Add")
        self.addTab(self.edit_structure_widget, "Edit")
        self.show()

    def configure_window(self):
        self.setGeometry(200, 200, 400, 400)
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint
            | Qt.FramelessWindowHint
            | Qt.WindowShadeButtonHint
        )

    def closeEvent(self, a0) -> None:
        self.main_window.plot_entities_with_cross_section()
