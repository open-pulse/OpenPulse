from vtk import vtkAppendPolyData, vtkLineSource, vtkTubeFilter, vtkPolyDataMapper
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
        # section data é [diametro, thickness]
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
        
        mapper = vtkPolyDataMapper()
        actor = vtkActor()

        mapper.SetInputData(filter.GetOutput())
        actor.SetMapper(mapper)

        self.add_actors(actor)


    def create_test_line(self):
        filter = vtkAppendPolyData()

        line_0 = vtkLineSource()
        line_0.SetPoint1(0, 0, 0)
        line_0.SetPoint2(1, 1, 0)
        line_0.Update()

        tube_0 = vtkTubeFilter()

        tube_0.AddInputData(line_0.GetOutput())
        tube_0.SetRadius(0.5)
        tube_0.SetNumberOfSides(50)
        tube_0.CappingOn()
        tube_0.Update()

        filter.AddInputData(tube_0.GetOutput())

        line_1 = vtkLineSource()
        line_1.SetPoint1(0, 0, 0)
        line_1.SetPoint2(1.5, 3, 1)
        line_1.Update()


        tube_1 = vtkTubeFilter()

        tube_1.AddInputData(line_1.GetOutput())
        tube_1.SetRadius(0.5)
        tube_1.SetNumberOfSides(50)
        tube_1.CappingOn()
        tube_1.Update()

        filter.AddInputData(tube_1.GetOutput())

        filter.Update()

        mapper = vtkPolyDataMapper()
        actor = vtkActor()

        mapper.SetInputData(filter.GetOutput())
        actor.SetMapper(mapper)

        self.add_actors(actor)

