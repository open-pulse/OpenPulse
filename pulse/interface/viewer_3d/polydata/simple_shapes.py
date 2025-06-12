from molde.utils.poly_data_utils import transform_polydata
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkFiltersCore import vtkAppendPolyData


def create_cone_source():
    source = vtkConeSource()
    source.SetHeight(1)
    source.SetRadius(0.5)
    source.SetResolution(12)
    source.Update()
    return transform_polydata(
        source.GetOutput(),
        position=(-0.5, 0, 0),
    )


def create_double_cone_source():
    cone = vtkConeSource()
    cone.SetHeight(1)
    cone.SetRadius(0.4)
    cone.SetResolution(12)
    cone.Update()

    source = vtkAppendPolyData()
    source.AddInputData(cone.GetOutput())
    source.AddInputData(
        transform_polydata(
            cone.GetOutput(),
            position=(-0.4, 0, 0),
        )
    )
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-0.5, 0, 0),
    )


def create_cube_source():
    source = vtkCubeSource()
    source.SetBounds(0, 1, 0, 1, 0, 1)
    source.Update()
    return source.GetOutput()


def create_sphere_source():
    source = vtkSphereSource()
    source.SetRadius(0.3)
    source.SetThetaResolution(12)
    source.SetPhiResolution(12)
    source.Update()
    return source.GetOutput()
