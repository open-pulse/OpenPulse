from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from opps.interface.toolboxes import GeometryToolbox
from pulse.uix.mainWindow import MainWindow


class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry_toolbox = GeometryToolbox()
        self.geometry_toolbox.editor.add_pipe((1, 0, 0))
        self.geometry_toolbox.editor.add_bend()
        self.geometry_toolbox.editor.add_pipe((1, 1, 0))
        self.geometry_toolbox.editor.commit()
        self.geometry_toolbox.editor.add_bend()
        self.geometry_toolbox.editor.add_pipe((1, 0, 0))

        self.main_window = MainWindow()
        self.main_window.show()

        self.update()

    def update(self):
        self.geometry_toolbox.update()
        self.main_window.render_widget.update_plot(reset_camera=False)
