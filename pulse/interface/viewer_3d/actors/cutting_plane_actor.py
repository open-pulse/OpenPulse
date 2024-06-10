import vtk


class CuttingPlaneActor(vtk.vtkActor):
    def __init__(self):
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        plane = vtk.vtkCubeSource()
        cylinder = vtk.vtkCylinderSource()
        cone = vtk.vtkConeSource()

        plane.SetCenter(0, 0, 0)
        plane.SetXLength(0.005)
        plane.SetYLength(1)
        plane.SetZLength(1)
        cone.SetCenter(0.025, 0, 0)
        cone.SetRadius(0.01)
        cone.SetHeight(0.04)
        cone.SetResolution(10)

        plane.Update()
        cone.Update()
        cylinder.Update()

        append_filter = vtk.vtkAppendPolyData()
        append_filter.AddInputData(plane.GetOutput())
        # append_filter.AddInputData(cone.GetOutput())
        # append_filter.AddInputData(cylinder.GetOutput())
        append_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(append_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetColor(0, 0.333, 0.867)
        self.GetProperty().LightingOff()