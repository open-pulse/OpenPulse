from vtkmodules.vtkFiltersSources import vtkLineSource, vtkSphereSource
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkTubeFilter
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor

from molde.render_widgets import CommonRenderWidget

from pulse import ICON_DIR, app

from pulse.editor.single_volume_psd import SingleVolumePSD
from pulse.editor.dual_volume_psd import DualVolumePSD


class PSDPreviewRenderWidget(CommonRenderWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window

        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.renderer.RemoveAllLights()

        self.create_axes()
        self.create_camera_light(0.1, 0.1)

        self.update_plot()

        self.update_theme()

        self.main_window.theme_changed.connect(self.set_theme)

    def update_plot(self):
        self.update()

    def build_device_preview(self, device_data):
    
        self.remove_all_actors()

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
        filter_actor.GetProperty().SetInterpolationToPhong()
        filter_actor.GetProperty().SetDiffuse(0.8)
        filter_actor.GetProperty().SetSpecular(1.5)
        filter_actor.GetProperty().SetSpecularPower(80)
        filter_actor.GetProperty().SetSpecularColor(1, 1, 1)

        self.add_actors(filter_actor)

    def config_view(self):
        self.renderer.ResetCamera()
        self.renderer.ResetCameraClippingRange()        
        self.renderer.ResetCameraScreenSpace()
            
    def update_theme(self):
        user_preferences = app().main_window.config.user_preferences
        bkg_1 = user_preferences.renderer_background_color_1
        bkg_2 = user_preferences.renderer_background_color_2
        font_color = user_preferences.renderer_font_color

        if bkg_1 is None:
            raise ValueError('Missing value "bkg_1"')
        if bkg_2 is None:
            raise ValueError('Missing value "bkg_2"')
        if font_color is None:
            raise ValueError('Missing value "font_color"')

        self.renderer.GradientBackgroundOn()
        self.renderer.SetBackground(bkg_1.to_rgb_f())
        self.renderer.SetBackground2(bkg_2.to_rgb_f())

        if hasattr(self, "text_actor"):
            self.text_actor.GetTextProperty().SetColor(font_color.to_rgb_f())

        if hasattr(self, "colorbar_actor"):
            self.colorbar_actor.GetTitleTextProperty().SetColor(font_color.to_rgb_f())
            self.colorbar_actor.GetLabelTextProperty().SetColor(font_color.to_rgb_f())

        if hasattr(self, "scale_bar_actor"):
            self.scale_bar_actor.GetLegendTitleProperty().SetColor(font_color.to_rgb_f())
            self.scale_bar_actor.GetLegendLabelProperty().SetColor(font_color.to_rgb_f())

    def turn_red(self):
        for actor in self.get_widget_actors():
            actor.GetProperty().SetColor(1, 0, 0)
            self.update_plot()

    def set_theme(self, *args, **kwargs):
        self.update_theme()

    def close_preview(self):
        self.render_interactor.Finalize()
        









