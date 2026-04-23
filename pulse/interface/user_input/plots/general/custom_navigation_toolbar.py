from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QIcon, QAction, QColor

import io

from pulse.interface.formatters import icons
from pulse import app, ICON_DIR


class CustomNavigationToolbar(NavigationToolbar2QT):

    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
 
        self.canvas = canvas

        self._create_connections()
        self._configure_toolbar()
        self._paint_toolbar_icons()

    def _create_connections(self):
        app().main_window.theme_changed.connect(self._paint_toolbar_icons)
    
    def _configure_toolbar(self):
        self.action_copy_graph = QAction()
        self.action_copy_graph.setToolTip("Copy Graph (Ctrl+C)")
        self.action_copy_graph.triggered.connect(self.copy_graph)
        self.action_copy_graph.setIcon(QIcon(str(ICON_DIR / "mpltoolbar/copy_icon.png")))
        self.action_copy_graph.setShortcut("ctrl+c")

        action_save_figure = self._actions["save_figure"]
        self.insertAction(action_save_figure, self.action_copy_graph)
        self.insertAction(self.action_copy_graph, action_save_figure)
    
    def _paint_toolbar_icons(self):

        if app().main_window.interface_theme == "dark":
            color = QColor("#5f9af4")
        else:
            color = QColor("#1a73e8")

        icons.change_icon_color_for_widgets(self.actions(), color)

    def copy_graph(self):
        with io.BytesIO() as buffer:
            self.canvas.fig.savefig(buffer)
            QApplication.clipboard().setImage(QImage.fromData(buffer.getvalue()))