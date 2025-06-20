from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QIcon, QAction

import io

from pulse import ICON_DIR


class CustomNavigationToolbar(NavigationToolbar2QT):

    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)

        self.canvas = canvas

        self.action_copy_graph = QAction()
        self.action_copy_graph.setToolTip("Copy Graph (Ctrl+C)")
        self.action_copy_graph.triggered.connect(self.copy_graph)
        self.action_copy_graph.setIcon(QIcon(str(ICON_DIR / "mpltoolbar/copy_icon.png")))
        self.action_copy_graph.setShortcut("ctrl+c")

        action_save_figure = self._actions["save_figure"]
        self.insertAction(action_save_figure, self.action_copy_graph)
        self.insertAction(self.action_copy_graph, action_save_figure)
    
    def copy_graph(self):
        with io.BytesIO() as buffer:
            self.canvas.fig.savefig(buffer)
            QApplication.clipboard().setImage(QImage.fromData(buffer.getvalue()))