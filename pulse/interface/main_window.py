from PyQt5.QtWidgets import QAction, QComboBox, QFileDialog, QLabel, QMainWindow, QMenu, QMessageBox, QSplitter, QStackedWidget, QToolBar
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5 import uic
from pathlib import Path

from pulse.interface.viewer_3d.opv_ui import OPVUi
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget
from pulse.interface.viewer_3d.render_widgets import MeshRenderWidget

from pulse.interface.user_input.input_ui import InputUi
from pulse.interface.user_input.model.geometry.geometry_designer import OPPGeometryDesignerInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput

from pulse.interface.menu.model_and_analysis_setup_widget import ModelAndAnalysisSetupWidget
from pulse.interface.menu.results_viewer_widget import ResultsViewerWidget

from pulse.interface.toolbars.mesh_toolbar import MeshToolbar

from pulse import app, UI_DIR

import sys
from functools import partial
import os
import qdarktheme

class MainWindow(QMainWindow):
    permission_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_DIR / 'main_window.ui', self)

        # i am keeping these atributes here to make
        # the transition easier, but it should be
        # defined only in the app.
        self.ui_dir = UI_DIR
        self.config = app().config
        self.project = app().project
        self.reset()

    def reset(self):
        self.theme = None
        self.model_and_analysis_setup_widget = None
        self.results_viewer_wigdet = None
        self.opv_widget = None
        self.input_widget = None
        self.cache_indexes = list()
        self.last_index = None

    def configure_window(self):
        self._config_window()
        self._define_qt_variables()
        self._connect_actions()
        self._create_layout()
        self._create_workspaces_toolbar()
        self._update_recent_projects()
        self._createMeshToolbar()
    
        self.plot_entities_with_cross_section()
        self.use_structural_setup_workspace()
        self.load_recent_project()
        
    # public
    def new_project(self):
        if not self.input_widget.new_project(self.config):
            return 
        self._update_recent_projects()
        self.set_window_title(self.project.file._project_name)
        self.update()

    def open_project(self, path=None):
        if not self.input_widget.load_project(path):
            return 

        self._update_recent_projects()
        self.set_window_title(self.project.file._project_name)
        self.update()

    def export_geometry(self):
        self.input_widget.export_geometry()

    def update(self):
        self.geometry_widget.update_plot(reset_camera=True)
        self.mesh_widget.update_plot(reset_camera=True)
        self.opv_widget.updatePlots()

    def use_geometry_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(0)

    def use_structural_setup_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(1)

    def use_acoustic_setup_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(2)

    def use_results_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(3)

    def plot_entities(self):
        # self.use_structural_setup_workspace()
        self.opv_widget.changePlotToEntities()

    def plot_entities_with_cross_section(self):
        # self.use_structural_setup_workspace()
        self.opv_widget.changePlotToEntitiesWithCrossSection()

    def plot_mesh(self):
        # self.use_structural_setup_workspace()
        self.opv_widget.changePlotToMesh()

    def plot_raw_geometry(self):
        # self.use_structural_setup_workspace()
        self.opv_widget.changePlotToRawGeometry()
    
    def plot_geometry_editor(self):
        self.use_geometry_workspace()

    def set_window_title(self, msg=""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def load_recent_project(self):
        if self.config.openLastProject and self.config.haveRecentProjects():
            self.importProject_call(self.config.getMostRecentProjectDir())
        elif self.input_widget.get_started():
            self.update()  # update the renders before change the view
            self.action_front_view_callback()
            self._update_recent_projects()
            self.set_window_title(self.project.file.project_name)

    # internal
    def _update_recent_projects(self):
        actions = self.menurecent.actions()
        for action in actions:
            self.menurecent.removeAction(action)

        self.menu_actions = []
        for name, path in reversed(self.config.recentProjects.items()):
            import_action = QAction(str(name) + "\t" + str(path))
            import_action.setStatusTip(str(path))
            import_action.triggered.connect(partial(self.open_project, path))
            self.menurecent.addAction(import_action)
            self.menu_actions.append(import_action)

    def _config_window(self):
        self.showMaximized()
        self.installEventFilter(self)
    
    def _define_qt_variables(self):
        '''
        This function is doing nothing. Every variable was
        already defined in the UI file.

        Despite that, it is nice to list the variables to
        help future maintainers and the code editor with
        type inference.
        '''
        self.setup_widgets_stack: QStackedWidget
        self.render_widgets_stack: QStackedWidget
        self.action_geometry_workspace: QAction
        self.action_structural_setup_workspace: QAction
        self.action_acoustic_setup_workspace: QAction
        self.action_analysis_setup_workspace: QAction
        self.action_results_workspace: QAction
        self.action_export_geometry: QAction
        self.action_set_dark_theme : QAction
        self.action_set_light_theme : QAction
        self.action_remove_themes : QAction
        self.tool_bar: QToolBar
        self.splitter: QSplitter
        self.menurecent: QMenu
        self.menu_project: QMenu
        self.menu_graphic: QMenu
        self.menu_general_settings: QMenu
        self.menu_structural_model: QMenu
        self.menu_acoustic_model: QMenu
        self.menu_model_info: QMenu
        self.menu_analysis: QMenu
        self.menu_results_viewer: QMenu
        self.menu_help: QMenu
        self.action_show_points: QAction
        self.action_show_lines: QAction
        self.action_show_tubes: QAction
        self.action_show_transparent: QAction
        self.action_show_symbols: QAction
        self.action_select_elements: QAction

    def _connect_actions(self):
        '''
        Instead of connecting every action manually, one by one,
        this function loops through every action and connects it
        to a function ending with "_callback".

        For example an action named "action_new" will be connected to 
        the function named "action_new_callback" if it exists.
        '''
        for action in self.findChildren(QAction):
            function_name = action.objectName() + "_callback"
            function_exists = hasattr(self, function_name)
            if not function_exists:
                continue

            function = getattr(self, function_name)
            if callable(function):
                action.triggered.connect(function)

    def _create_workspaces_toolbar(self):

        actions = [ self.action_geometry_workspace,
                    self.action_structural_setup_workspace,
                    self.action_acoustic_setup_workspace,
                    self.action_results_workspace ]

        self.combo_box_workspaces = QComboBox()
        for action in actions:
            self.combo_box_workspaces.addItem(action.text())

        self.combo_box_workspaces.currentIndexChanged.connect(self.update_combox_indexes)
        self.combo_box_workspaces.currentIndexChanged.connect(lambda x: actions[x].trigger())
        self.tool_bar.addWidget(self.combo_box_workspaces)

    def update_combox_indexes(self):
        index = self.combo_box_workspaces.currentIndex()
        self.cache_indexes.append(index)

    def _create_layout(self):
        editor = app().geometry_toolbox.editor

        self.opv_widget = OPVUi(self.project, self)
        self.model_and_analysis_setup_widget = ModelAndAnalysisSetupWidget(self)
        self.results_viewer_wigdet = ResultsViewerWidget()
        self.opv_widget.opvAnalysisRenderer._createPlayer()
        self.input_widget = InputUi(self)

        self.mesh_widget = MeshRenderWidget()
        self.geometry_widget = EditorRenderWidget(editor)
        self.geometry_widget.set_theme("light")
        #
        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.addWidget(self.opv_widget)

        self.geometry_input_wigdet = OPPGeometryDesignerInput(self.geometry_widget)
        self.setup_widgets_stack.addWidget(self.geometry_input_wigdet)
        self.setup_widgets_stack.addWidget(self.model_and_analysis_setup_widget)
        self.setup_widgets_stack.addWidget(self.results_viewer_wigdet)

        self.splitter.setSizes([100, 400])
        # self.splitter.widget(0).setFixedWidth(340)
        self.opv_widget.updatePlots()
        self.opv_widget.changePlotToEntitiesWithCrossSection()

    def _update_permissions(self):
        pass
    
    def _update_visualization(self):
        points = self.action_show_points.isChecked()
        lines = self.action_show_lines.isChecked()
        tubes = self.action_show_tubes.isChecked()
        symbols = self.action_show_symbols.isChecked()
        transparent = self.action_show_transparent.isChecked()
        self.opv_widget.update_visualization(points, lines, tubes, symbols, transparent)
        self.mesh_widget.update_visualization(points, lines, tubes, symbols, transparent)

        if self.action_select_elements.isChecked():
            self.opv_widget.selection_to_elements()
            self.mesh_widget.selection_to_elements()
        else:
            self.opv_widget.selection_to_lines()
            self.mesh_widget.selection_to_lines()

    # callbacks
    def action_new_project_callback(self):
        self.new_project()

    def action_open_project_callback(self):
        self.open_project()

    def action_export_geometry_callback(self):
        self.export_geometry()

    def action_geometry_workspace_callback(self):
        self.setup_widgets_stack.setCurrentWidget(self.geometry_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)
        self.geometry_input_wigdet.add_widget.load_defined_unit()

    def action_structural_setup_workspace_callback(self):
        self.model_and_analysis_setup_widget.update_visibility_for_structural_analysis()
        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.opv_widget)
        self.plot_entities_with_cross_section()

    def action_acoustic_setup_workspace_callback(self):
        self.model_and_analysis_setup_widget.update_visibility_for_acoustic_analysis()
        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)
        self.plot_entities_with_cross_section()

    def action_coupled_setup_workspace_callback(self):
        self.model_and_analysis_setup_widget.update_visibility_for_coupled_analysis()
        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.opv_widget)
        self.plot_entities_with_cross_section()

    def action_results_workspace_callback(self):
        if self.project.is_the_solution_finished():
            self.results_viewer_wigdet.animation_widget.setVisible(False)
            self.setup_widgets_stack.setCurrentWidget(self.results_viewer_wigdet)
            self.render_widgets_stack.setCurrentWidget(self.opv_widget)
            self.results_viewer_wigdet.udate_visibility_items()
        else:
            if self.cache_indexes:
                self.combo_box_workspaces.setCurrentIndex(self.cache_indexes[-2])

    def action_save_as_png_callback(self):
        self.savePNG_call()
    
    def action_reset_callback(self):
        self.input_widget.reset_project()
    
    def action_isometric_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(0)
            return
        render_widget.set_isometric_view()

    def action_top_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(1)
            return
        render_widget.set_top_view()

    def action_bottom_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(2)
            return
        render_widget.set_bottom_view()

    def action_left_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(3)
            return
        render_widget.set_left_view()

    def action_right_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(4)
            return
        render_widget.set_right_view()

    def action_front_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(5)
            return
        render_widget.set_front_view()

    def action_back_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(6)
            return
        render_widget.set_back_view()

    def action_set_structural_element_type_callback(self):
        self.input_widget.setStructuralElementType()

    def action_add_connecting_flanges_callback(self):
        self.input_widget.add_flanges()

    def action_set_prescribed_dofs_callback(self):
        self.input_widget.setDOF()

    def action_set_nodal_loads_callback(self):
        self.input_widget.setNodalLoads()

    def action_add_mass_spring_damper_callback(self):
        self.input_widget.addMassSpringDamper()

    def action_set_capped_end_callback(self):
        self.input_widget.setcappedEnd()

    def action_set_stress_stiffening_callback(self):
        self.input_widget.set_stress_stress_stiffening()

    def action_add_elastic_nodal_links_callback(self):
        self.input_widget.add_elastic_nodal_links()

    def action_structural_model_info_callback(self):
        self.input_widget.structural_model_info()

    def action_set_acoustic_element_type_callback(self):
        self.input_widget.set_acoustic_element_type()

    def action_set_acoustic_pressure_callback(self):
        self.input_widget.setAcousticPressure()

    def action_set_volume_velocity_callback(self):
        self.input_widget.setVolumeVelocity()

    def action_set_specific_impedance_callback(self):
        self.input_widget.setSpecificImpedance()

    def action_add_perforated_plate_callback(self):
        self.input_widget.add_perforated_plate()

    def action_set_acoustic_element_length_correction_callback(self):
        self.input_widget.set_acoustic_element_length_correction()

    def action_add_compressor_excitation_callback(self):
        self.input_widget.add_compressor_excitation()

    def action_acoustic_model_info_callback(self):
        self.input_widget.acoustic_model_info()
    
    def action_check_beam_criteria_callback(self):
        self.input_widget.check_beam_criteria()

    def action_select_analysis_type_callback(self):
        self.input_widget.analysisTypeInput()

    def action_analysis_setup_callback(self):
        self.input_widget.analysis_setup()
    
    def action_run_analysis_callback(self):
        self.input_widget.run_analysis()

    def action_about_openpulse(self):
        self.input_widget.about_OpenPulse()

    def action_show_points_callback(self, cond):
        self._update_visualization()

    def action_show_lines_callback(self, cond):
        self._update_visualization()

    def action_show_tubes_callback(self, cond):
        self._update_visualization()
    
    def action_show_symbols_callback(self, cond):
        self._update_visualization()
    
    def action_show_transparent_callback(self, cond):
        self._update_visualization()
    
    def action_select_elements_callback(self, cond):
        self._update_visualization()

    def update_export_geometry_file_access(self):
        import_type = self.project.file.get_import_type()
        if import_type == 0:
            self.action_export_geometry.setDisabled(True)
        elif import_type == 1:
            self.action_export_geometry.setDisabled(False)

    # DEPRECATED, REMOVE AS SOON AS POSSIBLE
    def getInputWidget(self):
        return self.input_widget

    def getOPVWidget(self):
        return self.opv_widget

    def getProject(self):
        return self.project
    
    def changeWindowTitle(self, msg = ""):
        self.set_window_title(msg)

    def draw(self):
        self.update()
        self.opv_widget.updatePlots()
        self.plot_entities_with_cross_section()
        self.action_front_view_callback()
        # self.opv_widget.setCameraView(5)
        
    def _loadProjectMenu(self):
        self._update_recent_projects()

    def importProject_call(self, path=None):
        if self.input_widget.load_project(path):
            self._loadProjectMenu()
            self.changeWindowTitle(self.project.file.project_name)
            self.draw()

    def newProject_call(self):
        if self.input_widget.new_project(self.config):
            self._loadProjectMenu()
            self.changeWindowTitle(self.project.file.project_name)
            self.draw()

    def _createMeshToolbar(self):
        self.mesh_toolbar = MeshToolbar(self)
        self.addToolBar(self.mesh_toolbar)
        self.insertToolBarBreak(self.mesh_toolbar)

    def _updateStatusBar(self):
        pass
    
    def set_enable_menuBar(self, *args, **kwargs):
        pass

    def action_set_dark_theme_callback(self):
        if self.theme in [None, "light"]:
            self.theme = "dark"
            self.custom_colors = { "[dark]": { "toolbar.background": "#202124"} }
            qdarktheme.setup_theme("dark", custom_colors=self.custom_colors)
            # self.dark_theme_configuration()
            self.action_set_light_theme.setDisabled(False)
            self.action_set_dark_theme.setDisabled(True)

    def action_set_light_theme_callback(self):
        if self.theme in [None, "dark"]:
            self.theme = "light"
            qdarktheme.setup_theme("light")
            # self.light_theme_configuration()
            self.action_set_light_theme.setDisabled(True)
            self.action_set_dark_theme.setDisabled(False)

    def action_remove_themes_callback(self):
        if self.theme is not None:
            self.theme = None
            qdarktheme.setup_theme()
            self.action_set_light_theme.setDisabled(False)
            self.action_set_dark_theme.setDisabled(False)

    def savePNG_call(self):
        project_path = self.project.file._project_path
        if not os.path.exists(project_path):
            project_path = ""
        path, _type = QFileDialog.getSaveFileName(None, 'Save file', project_path, 'PNG (*.png)')
        if path != "":
            self.getOPVWidget().savePNG(path)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.ShortcutOverride:
            if event.key() == Qt.Key_Space:
                self.opv_widget.opvAnalysisRenderer.tooglePlayPauseAnimation()
        return super(MainWindow, self).eventFilter(obj, event)
    
    def closeEvent(self, event):
        title = "OpenPulse"
        message = "Would you like to exit from the OpenPulse application?"
        close = QMessageBox.question(self, title, message, QMessageBox.No | QMessageBox.Yes)
        if close == QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()

    # def closeEvent(self, event):

    #     title = "OpenPulse stop execution requested"
    #     message = "Would you like to exit from the OpenPulse application?"
    #     right_toolTip = "The current project setup progress has already been saved in the project files."
        
    #     buttons_config = {"left_button_label" : "No", 
    #                       "right_button_label" : "Yes",
    #                       "right_toolTip" : right_toolTip}
        
    #     read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

    #     if read._stop:
    #         event.ignore()
    #         return

    #     if read._continue:
    #         sys.exit()

    # def remove_selected_lines(self):
    #     lines = self.opv_widget.getListPickedLines()
    #     if len(lines) > 0:
    #         if self.project.remove_selected_lines_from_geometry(lines):
    #             self.opv_widget.updatePlots()
    #             self.opv_widget.changePlotToEntities()
    #             # self.cameraFront_call()
    #             # self.opv_widget.changePlotToMesh()
            
    # def _createStatusBar(self):
    #     self.status_bar = QStatusBar()
    #     self.setStatusBar(self.status_bar)
    #     #
    #     label_font = self._getFont(10, bold=True, italic=False, family_type="Arial")
    #     self.label_geometry_state = QLabel("", self)
    #     self.label_geometry_state.setFont(label_font)
    #     self.status_bar.addPermanentWidget(self.label_geometry_state)
    #     #
    #     self.label_mesh_state = QLabel("", self)
    #     self.label_mesh_state.setFont(label_font)
    #     self.status_bar.addPermanentWidget(self.label_mesh_state)

    # def _updateGeometryState(self, label):
    #     _state = ""
    #     if label != "":
    #         _state = f" Geometry: {label} "            
    #     self.label_geometry_state.setText(_state)

    # def _updateMeshState(self, label):
    #     _state = ""
    #     if label != "":
    #         _state = f" Mesh: {label} "           
    #     self.label_mesh_state.setText(_state)

    # def _updateStatusBar(self):
    #     # Check and update geometry state
    #     if self.project.empty_geometry:
    #         self._updateGeometryState("pending")
    #     else:
    #         self._updateGeometryState("ok")
    #     # Check and update mesh state
    #     if len(self.project.preprocessor.structural_elements) == 0:
    #         if self.project.check_mesh_setup():
    #             self._updateMeshState("setup complete but not generated")
    #         else:
    #             self._updateMeshState("pending")
    #     else:
    #         self._updateMeshState("ok")