from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

from pulse.interface.formatters.icons import Icon
from pulse.interface.menu.border_item_delegate import BorderItemDelegate
from pulse.interface.menu.tooltips import get_tooltip

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

    def add_item(self, name, callback=None, property_name=""):
        if self._last_top_level is None:
            self.add_top_item("")

        item = ChildTreeWidgetItem(name)
        self._last_top_level.addChild(item)
        item.setFont(0, self.font_item)

        if property_name:
            item.set_property_name(property_name)

        # if callable(callback):
        #     item.clicked.connect(callback)

        return item

    def _config_tree(self):

        self.font_item = QFont()
        self.font_item.setPointSize(10)

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
        super().__init__([name])
        self.clicked = CustomBoundSignal()
        self._configure_appearance()

    def toggle_expansion(self):
        self.setExpanded(not self.isExpanded())

    def _configure_appearance(self):
        font = QFont()
        font.setBold(True)
        font.setWeight(QFont.Weight(60))
        font.setPointSize(10)
        self.setFont(0, font)
        self.setTextAlignment(0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setFlags(Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)

        # border_role = Qt.UserRole + 1
        # border_pen = QPen(self.line_color)
        # border_pen.setWidth(1)

        # linear_gradient = QLinearGradient(0, 0, 400, 0)
        # linear_gradient.setColorAt(0, QColor(240, 240, 240))#, 150))
        # linear_gradient.setColorAt(1, QColor(102, 204, 255))#, 100))

        # self.setData(0, border_role, border_pen)
        # self.setForeground(0, self.foreground_color)
        # self.setBackground(0, linear_gradient)
        # self.setBackground(0, self.background_color)


class ChildTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])
        self.clicked = CustomBoundSignal()
        self.should_paint = False

    def set_warning(self, cond):
        if cond:
            font = QFont()
            font.setBold(True)
            self.setFont(0, font)
            self.setForeground(0, QColor("#E89403"))
            warning_icon = Icon(":/icons/model_setup_items/warning_yellow.png")
            self.setIcon(0, warning_icon)
        else:
            # Resets data to default
            self.setData(0, Qt.ItemDataRole.FontRole, None)  # reset color
            self.setData(0, Qt.ItemDataRole.ForegroundRole, None)  # reset color
            self.setData(0, Qt.ItemDataRole.DecorationRole, None)

    def set_error(self, cond: bool):
        if cond:
            font = QFont()
            font.setBold(True)
            self.setFont(0, font)
            self.setForeground(0, QColor("#E2483D"))
            error_icon = Icon(":/icons/model_setup_items/error_red.png")
            self.setIcon(0, error_icon)
        else:
            # Resets data to default
            self.setData(0, Qt.ItemDataRole.FontRole, None)  # reset color
            self.setData(0, Qt.ItemDataRole.ForegroundRole, None)  # reset color
            self.setData(0, Qt.ItemDataRole.DecorationRole, None)

    def set_icon(self, file_name: str = "", visible: bool = True):
        # to set an alternative icon
        file_name = file_name if file_name != "" else self.property_name

        if visible:
            path_image = str(":/icons/model_setup_items/" + str(file_name + ".png"))
            self.setIcon(0, Icon(path_image))
        else:
            self.setIcon(0, Icon())
 
    def set_property_name(self, name: str):
        name = name.lower()
        name = name.strip()
        self.property_name = name

    def set_tooltips(self, property_name: str = "", requirement: bool = False, message_requirement: str = ""):
        if requirement and message_requirement == "":
            message_requirement = "<b style='color:red'>Required for the selected configuration.</b><br>"

        if property_name == "":
            property_name = getattr(self, "property_name", "")

        text = get_tooltip(property_name)

        if text:
            self.setToolTip(0, message_requirement + text)
        else:
            self.setToolTip(0, message_requirement)
