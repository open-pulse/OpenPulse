from vtk import vtkAppendPolyData, vtkLineSource, vtkTubeFilter, vtkPolyDataMapper, vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkActor

from molde.render_widgets import CommonRenderWidget

from pulse import ICON_DIR, app

from pulse.editor.single_volume_psd import SingleVolumePSD
from pulse.editor.dual_volume_psd import DualVolumePSD
class PSDPreviewRenderWidget(CommonRenderWidget):

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

        if "volume #2 parameters" in device_data.keys():
            device = DualVolumePSD(device_data)
        else:
            device = SingleVolumePSD(device_data)

        device.process_segment_data()
        filter = vtkAppendPolyData()

        connection_point = device_data['connection pipe']

        for start_coords, end_coords, section_data, segment_label in device.segment_data:

            if segment_label is not None:
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

                filter.AddInputData(tube.GetOutput())
                filter.Update()
            
            if segment_label == connection_point:
                sphere = vtkSphereSource()
                sphere.SetCenter(*start_coords)
                sphere.SetRadius(section_data[0] / 4)
                sphere.Update()

                sphere_mapper = vtkPolyDataMapper()
                sphere_mapper.SetInputData(sphere.GetOutput())

                sphere_actor = vtkActor()
                sphere_actor.SetMapper(sphere_mapper)

                sphere_actor.GetProperty().SetColor(1, 0, 0) 

                self.add_actors(sphere_actor)


    
        mapper = vtkPolyDataMapper()
        filter_actor = vtkActor()

        mapper.SetInputData(filter.GetOutput())
        filter_actor.SetMapper(mapper)

        self.add_actors(filter_actor)















