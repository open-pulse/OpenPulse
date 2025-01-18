from vtk import vtkAppendPolyData, vtkLineSource, vtkTubeFilter, vtkPolyDataMapper, vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkActor

from molde.render_widgets import CommonRenderWidget

from pulse import ICON_DIR, app
from pulse.editor.pulsation_damper import PulsationDamper

class DamperPreviewRenderWidget(CommonRenderWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window

        # It is better for an editor to have parallel projection
        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.renderer.RemoveAllLights()

        self.create_axes()
        self.create_camera_light(0.1, 0.1)

    
        self.update_plot()

    def update_plot(self):
        self.update()

    def build_device_preview(self, device_data):
        device = PulsationDamper(device_data)
        device.process_segment_data()

        damper = vtkAppendPolyData()

        connection_point = device_data["connecting_coords"]

        for start_coords, end_coords, section_data, segment_label, fluid_id in device.segment_data:
            line = vtkLineSource()
            line.SetPoint1(*start_coords)
            line.SetPoint2(*end_coords)
            line.Update()

            tube = vtkTubeFilter()
            tube.AddInputData(line.GetOutput())
            tube.SetRadius(section_data[0] / 2)
            tube.SetNumberOfSides(50)
            tube.CappingOn()
            tube.Update()

            damper.AddInputData(tube.GetOutput())
            damper.Update()
            

            sphere = vtkSphereSource()
            sphere.SetCenter(*connection_point)
            sphere.SetRadius(device_data["outside_diameter_neck"] / 4)
            sphere.Update()

            sphere_mapper = vtkPolyDataMapper()
            sphere_mapper.SetInputData(sphere.GetOutput())

            sphere_actor = vtkActor()
            sphere_actor.SetMapper(sphere_mapper)

            sphere_actor.GetProperty().SetColor(1, 0, 0) 

            self.add_actors(sphere_actor)

        mapper = vtkPolyDataMapper()
        damper_actor = vtkActor()

        mapper.SetInputData(damper.GetOutput())
        damper_actor.SetMapper(mapper)

        self.add_actors(damper_actor)

