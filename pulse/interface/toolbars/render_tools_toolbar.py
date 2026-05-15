from PySide6.QtWidgets import QToolBar, QSizePolicy
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, Signal

from pulse import ICON_DIR
from pulse.interface.viewer_3d.render_tools import (
    RenderTool,
    RotationTool,
    GrabTool,
    ZoomTool,
    SelectionTool
)

from pulse import app


class RenderToolsToolbar(QToolBar):
    render_tool_changed = Signal(RenderTool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._define_qt_variables()
        self._load_icons()
        self._configure_layout()
        self._configure_appearence()
        self._configure_widgets()
        self._connect_actions()

        self.setWindowTitle("Render tools toolbar")

    def _define_qt_variables(self):
        self.action_selection_tool = QAction(self)
        self.action_grab_tool = QAction(self)
        self.action_rotation_tool = QAction(self)
        self.action_zoom_tool = QAction(self)

    def _load_icons(self):
        self.selection_tool_icon = QIcon(str(ICON_DIR / "common/selection_icon.png"))
        self.grab_tool_icon = QIcon(str(ICON_DIR / "common/grab_icon.png"))
        self.rotation_tool_icon = QIcon(str(ICON_DIR / "common/rotation_icon.png"))
        self.zoom_tool_icon = QIcon(str(ICON_DIR / "common/zoom_icon.png"))
    
    def _configure_layout(self):
        self.addAction(self.action_selection_tool)
        self.addAction(self.action_grab_tool)
        self.addAction(self.action_rotation_tool)
        self.addAction(self.action_zoom_tool)
    
    def _configure_appearence(self):
        self.setMovable(True)
        self.setOrientation(Qt.Horizontal)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
       
    def _configure_widgets(self):
        for action in self.actions():
            action.setCheckable(True)

        self.action_selection_tool.setChecked(True)

        self.action_selection_tool.setIcon(self.selection_tool_icon)
        self.action_selection_tool.setToolTip("Selection tool")

        self.action_grab_tool.setIcon(self.grab_tool_icon)
        self.action_grab_tool.setToolTip("Grab tool")

        self.action_rotation_tool.setIcon(self.rotation_tool_icon)
        self.action_rotation_tool.setToolTip("Rotation tool")

        self.action_zoom_tool.setIcon(self.zoom_tool_icon)
        self.action_zoom_tool.setToolTip("Zoom tool")
    
    def _connect_actions(self):
        self.action_selection_tool.triggered.connect(self.action_selection_tool_callback)
        self.action_grab_tool.triggered.connect(self.action_grab_tool_callback)
        self.action_rotation_tool.triggered.connect(self.action_rotation_tool_callback)
        self.action_zoom_tool.triggered.connect(self.action_zoom_tool_callback)

    def action_grab_tool_callback(self):
        if self.action_grab_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_grab_tool)
            self.render_tool_changed.emit(GrabTool)
        else:
            self.action_selection_tool_callback()

    def action_selection_tool_callback(self):
        self.discheck_all_actions_of_render_tools_toolbar_except(self.action_selection_tool)

        if not app().main_window.use_base_render_tool:
            self.render_tool_changed.emit(SelectionTool)
        else:
            self.render_tool_changed.emit(RenderTool)

    def action_rotation_tool_callback(self):
        if self.action_rotation_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_rotation_tool)
            self.render_tool_changed.emit(RotationTool)
        else:
            self.action_selection_tool_callback()

    def action_zoom_tool_callback(self):
        if self.action_zoom_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_zoom_tool)
            self.render_tool_changed.emit(ZoomTool)
        else:
            self.action_selection_tool_callback()

    def discheck_all_actions_of_render_tools_toolbar_except(self, action: QAction):
        for _action in self.actions():
            _action.setChecked(False)

        action.setChecked(True)
    
    def enable_selection_tool(self):
        self.action_selection_tool.setEnabled(True)
        app().main_window.use_base_render_tool = False

    def disable_selection_tool(self):
        self.action_selection_tool.setEnabled(False)
        app().main_window.use_base_render_tool = True


