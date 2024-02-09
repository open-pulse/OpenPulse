import vtk
from dataclasses import dataclass
from vtkat.render_widgets import CommonRenderWidget
from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from pulse.interface.viewer_3d.actors import NodesActor, ElementLinesActor, TubeActor
from pulse.interface.acousticSymbolsActor import AcousticNodesSymbolsActor, AcousticElementsSymbolsActor
from pulse.interface.structuralSymbolsActor import StructuralNodesSymbolsActor, StructuralElementsSymbolsActor
from pulse import app

@dataclass
class PlotFilter:
    nodes: bool = False
    lines: bool = False
    tubes: bool = False
    transparent: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False
    raw_lines: bool = False


@dataclass
class SelectionFilter:
    nodes: bool    = False
    entities: bool = False
    elements: bool = False


class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mouse_click = (0, 0)
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        
        self.interactor_style = BoxSelectionInteractorStyle()
        self.render_interactor.SetInteractorStyle(self.interactor_style)

        self.open_pulse_logo = None
        self.mopt_logo = None

        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None

        self.plot_filter = PlotFilter(True, True, True, True, True, True)
        self.selection_filter = SelectionFilter(True, True, True)

        self.create_axes()
        self.create_scale_bar()
        self.create_logos()
        self.set_theme("light")

    def update_plot(self, reset_camera=True):
        from time import time

        self.remove_actors()
        self.create_logos()

        project = app().project

        self.nodes_actor = NodesActor(project)
        self.lines_actor = ElementLinesActor(project)
        self.tubes_actor = TubeActor(project)

        # TODO: Replace these actors for newer ones that
        # are lighter and easier to update
        self._acoustic_nodes_symbols = AcousticNodesSymbolsActor(project)
        self._acoustic_elements_symbols = AcousticElementsSymbolsActor(project)
        self._structural_nodes_symbols = StructuralNodesSymbolsActor(project)
        self._structural_elements_symbols = StructuralElementsSymbolsActor(project)
        self._acoustic_nodes_symbols.build()
        self._acoustic_elements_symbols.build()
        self._structural_nodes_symbols.build()
        self._structural_elements_symbols.build()
        self.acoustic_nodes_symbols_actor = self._acoustic_nodes_symbols.getActor()
        self.acoustic_elements_symbols_actor = self._acoustic_elements_symbols.getActor()
        self.structural_nodes_symbols_actor = self._structural_nodes_symbols.getActor()
        self.structural_elements_symbols_actor = self._structural_elements_symbols.getActor()

        self.renderer.AddActor(self.lines_actor)
        self.renderer.AddActor(self.nodes_actor)
        self.renderer.AddActor(self.tubes_actor)
        self.renderer.AddActor(self.acoustic_nodes_symbols_actor)
        self.renderer.AddActor(self.acoustic_elements_symbols_actor)
        self.renderer.AddActor(self.structural_nodes_symbols_actor)
        self.renderer.AddActor(self.structural_elements_symbols_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        # self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.tubes_actor)
        self.renderer.RemoveActor(self.acoustic_nodes_symbols_actor)
        self.renderer.RemoveActor(self.acoustic_elements_symbols_actor)
        self.renderer.RemoveActor(self.structural_nodes_symbols_actor)
        self.renderer.RemoveActor(self.structural_elements_symbols_actor)

        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None

    def update_visualization(self, nodes, lines, tubes, symbols):
        transparent = nodes or lines or symbols
        self.plot_filter = PlotFilter(
            nodes=nodes,
            lines=lines,
            tubes=tubes,
            acoustic_symbols=symbols,
            structural_symbols=symbols,
            transparent=transparent,
        )
        
        elements = (lines or tubes) and nodes
        entities = (lines or tubes) and (not nodes) 
        self.selection_filter = SelectionFilter(
            nodes=nodes,
            elements=elements,
            entities=entities,
        )

        if not self._actor_exists():
            return 

        self.nodes_actor.SetVisibility(self.plot_filter.nodes)
        self.lines_actor.SetVisibility(self.plot_filter.lines)
        self.tubes_actor.SetVisibility(self.plot_filter.tubes)
        self.acoustic_nodes_symbols_actor.SetVisibility(self.plot_filter.acoustic_symbols)
        self.acoustic_elements_symbols_actor.SetVisibility(self.plot_filter.acoustic_symbols)
        self.structural_nodes_symbols_actor.SetVisibility(self.plot_filter.structural_symbols)
        self.structural_elements_symbols_actor.SetVisibility(self.plot_filter.structural_symbols)
        self.update()

    def _actor_exists(self):
        actors = [
            self.nodes_actor,
            self.lines_actor,
            self.tubes_actor,
            self.acoustic_nodes_symbols_actor,
            self.acoustic_elements_symbols_actor,
            self.structural_nodes_symbols_actor,
            self.structural_elements_symbols_actor,
        ]
        return all([actor is not None for actor in actors])

    def set_theme(self, theme):
        super().set_theme(theme)
        try:
            self.create_logos(theme)
        except:
            return

    def create_logos(self, theme="light"):
        self.renderer.RemoveViewProp(self.open_pulse_logo)
        self.renderer.RemoveViewProp(self.mopt_logo)
        self.renderer.AddViewProp(self.open_pulse_logo)
        self.renderer.AddViewProp(self.mopt_logo)

        if theme == "light":
            open_pulse_path = Path('data/icons/OpenPulse_logo_black.png')
            mopt_path = Path('data/icons/mopt_logo_black.png')     
        elif theme == "dark":
            open_pulse_path = Path('data/icons/OpenPulse_logo_white.png')
            mopt_path = Path('data/icons/mopt_logo_white.png')
        else:
            raise NotImplementedError()

        self.open_pulse_logo = self._load_vtk_logo(open_pulse_path)
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)
        self.renderer.AddViewProp(self.open_pulse_logo)
        self.open_pulse_logo.SetRenderer(self.renderer)

        self.mopt_logo = self._load_vtk_logo(mopt_path)
        self.mopt_logo.SetPosition(0.01, -0.015)
        self.mopt_logo.SetPosition2(0.07, 0.1)
        self.renderer.AddViewProp(self.mopt_logo)
        self.mopt_logo.SetRenderer(self.renderer)

    def _load_vtk_logo(self, path):
        image_reader = vtk.vtkPNGReader()
        image_reader.SetFileName(path)
        image_reader.Update()

        logo = vtk.vtkLogoRepresentation()
        logo.SetImage(image_reader.GetOutput())
        logo.ProportionalResizeOn()
        logo.GetImageProperty().SetOpacity(0.9)
        logo.GetImageProperty().SetDisplayLocationToBackground()
        return logo

    def click_callback(self, x, y):
        self.mouse_click = x, y

    def selection_callback(self, x, y):
        picked_nodes = self._pick_nodes(x, y)
        picked_entities = self._pick_entities(x, y)
        picked_elements = self._pick_elements(x, y)

        # selection priority is: nodes > entities > elements
        if len(picked_nodes) == 1 and len(picked_entities) <= 1 and len(picked_elements) <= 1:
            picked_entities.clear()
            picked_elements.clear()
        elif len(picked_entities) == 1 and len(picked_elements) <= 1:
            picked_elements.clear()

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)
        
        self.nodes_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.tubes_actor.clear_colors()

        selection_color = (255, 0, 0)
        self.nodes_actor.set_color(selection_color, picked_nodes)
        self.lines_actor.set_color(selection_color, entities=picked_entities)
        self.tubes_actor.set_color(selection_color, elements=picked_elements)

    def _pick_nodes(self, x, y):
        picked = self._pick_actor(x, y, self.nodes_actor)
        if not self.nodes_actor in picked:
            return set()

        cells = picked[self.nodes_actor]
        return set(cells)

    def _pick_entities(self, x, y):
        picked = self._pick_actor(x, y, self.lines_actor)
        if not self.lines_actor in picked:
            return set()
        cells = picked[self.lines_actor]
        entities = {self.lines_actor.get_cell_entity(i) for i in cells}
        return entities

    def _pick_elements(self, x, y):
        picked = self._pick_actor(x, y, self.tubes_actor)
        if not self.tubes_actor in picked:
            return set()

        cells = picked[self.tubes_actor]
        elements = {self.tubes_actor.get_cell_element(i) for i in cells}
        return elements
    
    def _pick_actor(self, x, y, actor_to_select):
        selection_picker = CellAreaPicker()
        selection_picker._cell_picker.SetTolerance(0.0015)
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == actor_to_select:
                actor.PickableOn()
            else:
                actor.PickableOff()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            selection_picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            selection_picker.pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.get_picked()
