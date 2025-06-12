from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from molde.utils.poly_data_utils import transform_polydata


def create_arrow_source():
    source = vtkArrowSource()
    source.SetTipLength(0.25)
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-1, 0, 0),
    )


def create_long_arrow_source():
    source = vtkArrowSource()
    source.SetTipResolution(4)
    source.SetShaftResolution(4)
    source.SetTipLength(0.85)
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-1, 0, 0),
    )


def create_double_arrow_source():
    arrow1 = vtkArrowSource()
    arrow1.SetTipLength(0.45)
    arrow1.Update()

    arrow2 = vtkArrowSource()
    arrow2.SetTipLength(0.3)
    arrow2.Update()

    source = vtkAppendPolyData()
    source.AddInputData(arrow1.GetOutput())
    source.AddInputData(arrow2.GetOutput())
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-1, 0, 0),
    )


def create_outwards_arrow_source():
    source = vtkArrowSource()
    source.SetTipLength(0.25)
    source.Update()
    return source.GetOutput()
