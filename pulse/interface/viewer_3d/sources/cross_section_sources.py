import vtk


def closed_pipe_data(length, outside_diameter):
    cilinder = vtk.vtkCylinderSource()
    cilinder.SetResolution(20)
    cilinder.SetRadius(outside_diameter / 2)
    cilinder.SetHeight(length)
    cilinder.CappingOn()
    cilinder.Update()
    return cilinder.GetOutput()

def pipe_data(length, outside_diameter, thickness):
    if thickness == 0:
        return closed_pipe_data(length, outside_diameter)
    cilinder = vtk.vtkCylinderSource()
    cilinder.SetResolution(20)
    cilinder.SetRadius(outside_diameter / 2)
    cilinder.SetHeight(length)
    cilinder.CappingOff()
    cilinder.Update()
    return cilinder.GetOutput()

def circular_beam_data(length, outside_diameter, thickness):
    return pipe_data(length, outside_diameter, thickness)

def closed_rectangular_beam_data(length, b, h):
    rectangular = vtk.vtkCubeSource()
    rectangular.SetYLength(length)
    rectangular.SetXLength(b)
    rectangular.SetZLength(h)
    rectangular.Update()
    return rectangular.GetOutput()

def rectangular_beam_data(length, b, h, t):
    if t == 0:
        return closed_rectangular_beam_data(length, b, h)

    rectangular_top = vtk.vtkCubeSource()
    rectangular_left = vtk.vtkCubeSource()
    rectangular_right = vtk.vtkCubeSource()
    rectangular_bottom = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t)
    rectangular_top.SetXLength(b)
    rectangular_top.SetCenter(0, 0, -h/2 + t/2)

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(t)
    rectangular_left.SetCenter(-b/2 + t/2, 0, 0)

    rectangular_right.SetYLength(length)
    rectangular_right.SetZLength(h)
    rectangular_right.SetXLength(t)
    rectangular_right.SetCenter(b/2 - t/2, 0, 0)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t)
    rectangular_bottom.SetXLength(b)
    rectangular_bottom.SetCenter(0, 0, h/2 - t/2)

    rectangular_top.Update()
    rectangular_left.Update()
    rectangular_right.Update()
    rectangular_bottom.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_right.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()

def c_beam_data(length, h, w1, w2, t1, t2, tw):
    rectangular_top = vtk.vtkCubeSource()
    rectangular_left = vtk.vtkCubeSource()
    rectangular_bottom = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(w1/2 - max(w1, w2)/2, 0, -h/2 + t1/2)

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(tw)
    rectangular_left.SetCenter(-max(w1, w2)/2 + tw/2, 0, 0)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(w2/2 - max(w1, w2)/2, 0, h/2 - t2/2)

    rectangular_top.Update()
    rectangular_left.Update()
    rectangular_bottom.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()

def i_beam_data(length, h, w1, w2, t1, t2, tw):
    rectangular_top = vtk.vtkCubeSource()
    rectangular_center = vtk.vtkCubeSource()
    rectangular_bottom = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(0, 0, -h/2 + t1/2)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetXLength(tw)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(0, 0, h/2 - t2/2)

    rectangular_top.Update()
    rectangular_center.Update()
    rectangular_bottom.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()

def t_beam_data(length, h, w1, t1, tw):
    rectangular_top = vtk.vtkCubeSource()
    rectangular_center = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(0, 0, -h/2 + t1/2)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetXLength(tw)

    rectangular_top.Update()
    rectangular_center.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()
