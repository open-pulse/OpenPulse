from vtkmodules.vtkFiltersSources import vtkLineSource, vtkSphereSource
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkTubeFilter
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor

from molde.render_widgets import CommonRenderWidget

from pulse import ICON_DIR, app
from pulse.editor.pulsation_damper import PulsationDamper


class DamperPreviewRenderWidget(CommonRenderWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window

        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.renderer.RemoveAllLights()

        self.create_axes()
        self.create_camera_light(0.1, 0.1)

    
        self.update_plot()

        self.main_window.theme_changed.connect(self.set_theme)

    def update_plot(self):
        self.update()

    def build_device_preview(self, device_data):

        self.renderer.RemoveAllViewProps()

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

            if segment_label == "gas_filled":

                liquid_filled_tube_mapper = vtkPolyDataMapper()
                liquid_filled_tube_mapper.SetInputData(tube.GetOutput())
                liquid_filled_tube_actor = vtkActor()
                liquid_filled_tube_actor.SetMapper(liquid_filled_tube_mapper)
                liquid_filled_tube_actor.GetProperty().SetColor(0.5176470588235295, 0.6666666666666666, 1)
                liquid_filled_tube_actor.GetProperty().SetInterpolationToPhong()
                liquid_filled_tube_actor.GetProperty().SetDiffuse(0.8)
                liquid_filled_tube_actor.GetProperty().SetSpecular(1.5)
                liquid_filled_tube_actor.GetProperty().SetSpecularPower(80)
                liquid_filled_tube_actor.GetProperty().SetSpecularColor(1, 1, 1)

                self.add_actors(liquid_filled_tube_actor)

            else:
                
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
        damper_actor.GetProperty().SetInterpolationToPhong()
        damper_actor.GetProperty().SetDiffuse(0.8)
        damper_actor.GetProperty().SetSpecular(1.5)
        damper_actor.GetProperty().SetSpecularPower(80)
        damper_actor.GetProperty().SetSpecularColor(1, 1, 1)


        self.add_actors(damper_actor)

    def config_view(self):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(1, 1, 1)
        camera.SetFocalPoint(0, 0, 0) 
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

    def close_render(self):
        self.render_interactor
    
    def turn_red(self):
        for actor in self.get_widget_actors():
            actor.GetProperty().SetColor(1, 0, 0)
            self.update_plot()



    def set_theme(self, *args, **kwargs):
        self.update_theme()

    def close_preview(self):
        self.render_interactor.Finalize()
        