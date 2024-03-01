from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRect, pyqtSignal, QObject, pyqtBoundSignal
from pathlib import Path

from pulse.interface.menu.border_item_delegate import BorderItemDelegate


class CommonMenuItems(QTreeWidget):
    """Common Menu Items

    This class simplifies the creation of menu items.

    """

    def __init__(self):
        super().__init__()

        self._last_top_level = None
        self._callback_list = dict()

        self._config_tree()

    def add_top_item(self, name, icon=None, expanded=True):
        item = TopTreeWidgetItem(name)
        self._last_top_level = item
        self.addTopLevelItem(item)
        item.setExpanded(expanded)
        return item

    def add_item(self, name, callback=None):
        if self._last_top_level is None:
            self.add_top_item("")

        item = ChildTreeWidgetItem(name)
        self._last_top_level.addChild(item)

        # if callable(callback):
        #     item.clicked.connect(callback)

        return item

    def _config_tree(self):
        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setRootIsDecorated(True)
        delegate = BorderItemDelegate(self, Qt.UserRole + 1)
        self.setItemDelegate(delegate)
        self.itemClicked.connect(self.item_clicked_callback)

    def item_clicked_callback(self, item, _):
        if item.isDisabled():
            return
        
        if not hasattr(item, "clicked"):
            return
        
        item.clicked.emit()


# It is usually bad to have multiple classes in the same file
# but I will do it anyway >=)


class CustomBoundSignal:
    '''
    Copies the funcionality of pyqtBoundSignal and is meant 
    to be used in objects that are not instances of QObjects.
    '''

    def __init__(self) -> None:
        self.callbacks = set()
    
    def connect(self, function):
        self.callbacks.add(function)

    def disconnect(self, function):
        self.callbacks.remove(function)

    def emit(self, *args, **kwargs):
        for function in self.callbacks:
            if callable(function):
                function(*args, **kwargs)


class TopTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, name):
        super(QTreeWidgetItem, self).__init__([name])
        self.clicked = CustomBoundSignal()
        self._configure_appearance()

    def toggle_expansion(self):
        self.setExpanded(not self.isExpanded())

    def _configure_appearance(self):
        font = QFont()
        font.setBold(True)

        border_role = Qt.UserRole + 1
        border_pen = QPen(QColor(0,0,0))
        border_pen.setWidth(1)

        linear_gradient = QLinearGradient(0, 0, 400, 0)
        linear_gradient.setColorAt(0, QColor(240, 240, 240, 150))
        linear_gradient.setColorAt(1, QColor(102, 204, 255, 100))
        
        self.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.setFont(0, font)
        self.setData(0, border_role, border_pen)
        self.setForeground(0, QColor(0,0,0))
        self.setBackground(0, linear_gradient)
        self.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)


class ChildTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, name):
        super(QTreeWidgetItem, self).__init__([name])
        self.clicked = CustomBoundSignal()

    def set_warning(self, cond):
        if cond:
            font = QFont()
            font.setBold(True)
            warning_icon = QIcon(str(Path("data/icons/warning.png")))
            self.setFont(0, font)
            self.setForeground(0, QColor(210, 144, 0))
            self.setIcon(0, warning_icon)
        else:
            # Resets data to default
            self.setData(0, Qt.FontRole, None)  # reset color
            self.setData(0, Qt.ForegroundRole, None)  # reset color
            self.setData(0, Qt.DecorationRole, None)