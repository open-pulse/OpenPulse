
import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import VTK_TRIANGLE, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkCylinderSource,
    vtkDiskSource,
    vtkRegularPolygonSource,
    vtkSphereSource,
)
from vtkmodules.vtkIOGeometry import vtkOBJReader

from pulse import SYMBOLS_DIR
from pulse.model.cross_sections.c_beam_cross_section import CBeamCrossSection
from pulse.model.cross_sections.i_beam_cross_section import IBeamCrossSection
from pulse.model.cross_sections.t_beam_cross_section import TBeamCrossSection

def load_symbol(path):
    reader = vtkOBJReader()
    reader.SetFileName(str(path))
    reader.Update()
    return reader.GetOutput()

def apply_transform(data, dx=0, dy=0, dz=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1):
    transform = vtkTransform()
    transform.Translate(dx, dy, dz)
    transform.Scale(sx, sy, sz)
    transform.RotateZ(rz)
    transform.RotateX(rx)
    transform.RotateY(ry)
    transform.Update()
    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(data)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    return transform_filter.GetOutput()

VALVE_WHEEL = load_symbol(SYMBOLS_DIR / "other/valve_wheel.obj")

def closed_pipe_data(length, outside_diameter, offset_y=0, offset_z=0, sides=20):
    cilinder = vtkCylinderSource()
    cilinder.SetResolution(sides)
    cilinder.SetRadius(outside_diameter / 2)
    cilinder.SetCenter(0, length / 2, 0)
    cilinder.SetHeight(length)
    cilinder.CappingOn()
    cilinder.Update()

    return apply_transform(cilinder.GetOutput(), rz=-90, dy=offset_y, dz=offset_z)

def pipe_data(length, outside_diameter, thickness, offset_y=0, offset_z=0, sides=20):
    if (thickness == 0) or (2 * thickness > outside_diameter):
        return closed_pipe_data(length, outside_diameter, offset_y, offset_z, sides)

    outer_radius = outside_diameter / 2
    inner_radius = (outside_diameter) / 2 - thickness

    outer_cilinder = vtkCylinderSource()
    outer_cilinder.SetResolution(sides)
    outer_cilinder.SetRadius(outer_radius)
    outer_cilinder.SetHeight(length)
    outer_cilinder.SetCenter(0, length / 2, 0)
    outer_cilinder.CappingOff()
    outer_cilinder.Update()

    inner_cilinder = vtkCylinderSource()
    inner_cilinder.SetResolution(sides)
    inner_cilinder.SetRadius(inner_radius)
    inner_cilinder.SetHeight(length)
    inner_cilinder.SetCenter(0, length / 2, 0)
    inner_cilinder.CappingOff()
    inner_cilinder.Update()

    ring_bottom = vtkDiskSource()
    ring_bottom.SetCircumferentialResolution(sides)
    ring_bottom.SetOuterRadius(outer_radius)
    ring_bottom.SetInnerRadius(inner_radius)
    ring_bottom.SetCenter(0, 0, 0)
    ring_bottom.SetNormal(0, 1, 0)
    ring_bottom.Update()

    ring_top = vtkDiskSource()
    ring_top.SetCircumferentialResolution(sides)
    ring_top.SetOuterRadius(outer_radius)
    ring_top.SetInnerRadius(inner_radius)
    ring_top.SetCenter(0, length, 0)
    ring_top.SetNormal(0, 1, 0)
    ring_top.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(outer_cilinder.GetOutput())
    append_polydata.AddInputData(inner_cilinder.GetOutput())
    append_polydata.AddInputData(ring_bottom.GetOutput())
    append_polydata.AddInputData(ring_top.GetOutput())
    append_polydata.Update()

    return apply_transform(append_polydata.GetOutput(), rz=-90, dy=offset_y, dz=offset_z)

def circular_beam_data(length, outside_diameter, thickness, offset_y=0, offset_z=0):
    return pipe_data(
        length,
        outside_diameter,
        thickness,
        offset_y=offset_y,
        offset_z=offset_z,
        sides=12,
    )

def closed_rectangular_beam_data(length, b, h, offset_y=0, offset_z=0):
    rectangle = vtkCubeSource()
    rectangle.SetXLength(length)
    rectangle.SetYLength(h)
    rectangle.SetZLength(b)
    rectangle.SetCenter(length / 2, offset_y, offset_z)
    rectangle.Update()

    return rectangle.GetOutput()

def rectangular_beam_data(length, b, h, b_in, h_in, offset_y=0, offset_z=0):

    tb = (b - b_in) / 2
    th = (h - h_in) / 2

    if tb == 0 or th == 0:
        return closed_rectangular_beam_data(length, b, h, offset_y, offset_z)

    rectangular_top = vtkCubeSource()
    rectangular_left = vtkCubeSource()
    rectangular_right = vtkCubeSource()
    rectangular_bottom = vtkCubeSource()

    rectangular_top.SetXLength(length)
    rectangular_top.SetYLength(tb)
    rectangular_top.SetZLength(b)
    rectangular_top.SetCenter(length / 2, (h - tb) / 2 + offset_y, offset_z)
    rectangular_top.Update()

    rectangular_left.SetXLength(length)
    rectangular_left.SetYLength(h - 2*th)
    rectangular_left.SetZLength(th)
    rectangular_left.SetCenter(length / 2, offset_y, -(b - th) / 2 + offset_z)
    rectangular_left.Update()

    rectangular_right.SetXLength(length)
    rectangular_right.SetYLength(h - 2*th)
    rectangular_right.SetZLength(th)
    rectangular_right.SetCenter(length / 2, offset_y, (b - th) / 2 + offset_z)
    rectangular_right.Update()

    rectangular_bottom.SetXLength(length)
    rectangular_bottom.SetYLength(tb)
    rectangular_bottom.SetZLength(b)
    rectangular_bottom.SetCenter(length / 2, -(h - tb) / 2 + offset_y, offset_z)
    rectangular_bottom.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_right.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()

def c_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=0, offset_z=0):

    Zc, Yc = CBeamCrossSection(h, w1, t1, w2, t2, tw, offset_y, offset_z).centroid

    # compute the y coordinate centroid for the left rectangle of the C-Beam
    y_left = (((h/2 - t1)**2) - ((h/2 - t2)**2))*(tw/2) / ((h-(t1+t2))*tw)

    rectangular_top = vtkCubeSource()
    rectangular_left = vtkCubeSource()
    rectangular_bottom = vtkCubeSource()

    rectangular_top.SetXLength(length)
    rectangular_top.SetYLength(t1)
    rectangular_top.SetZLength(w1)
    rectangular_top.SetCenter(length / 2, (h - t1) / 2 + offset_y - Yc, (w1 / 2) - Zc + offset_z)
    rectangular_top.Update()

    rectangular_left.SetXLength(length)
    rectangular_left.SetYLength(h - (t1 + t2))
    rectangular_left.SetZLength(tw)
    rectangular_left.SetCenter(length / 2, y_left - Yc + offset_y, (tw / 2) - Zc + offset_z)
    rectangular_left.Update()

    rectangular_bottom.SetXLength(length)
    rectangular_bottom.SetYLength(t2)
    rectangular_bottom.SetZLength(w2)
    rectangular_bottom.SetCenter(length / 2, -(h - t2) / 2 + offset_y - Yc,  (w2 / 2) - Zc + offset_z)
    rectangular_bottom.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()

def i_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=0, offset_z=0):

    Zc, Yc = IBeamCrossSection(h, w1, t1, w2, t2, tw, offset_y, offset_z).centroid

    # compute the y coordinate centroid for the center rectangle of the I-Beam
    y_center = (((h/2 - t1)**2) - ((h/2 - t2)**2))*(tw/2) / ((h-(t1+t2))*tw)

    rectangular_top = vtkCubeSource()
    rectangular_center = vtkCubeSource()
    rectangular_bottom = vtkCubeSource()

    rectangular_top.SetXLength(length)
    rectangular_top.SetYLength(t1)
    rectangular_top.SetZLength(w1)
    rectangular_top.SetCenter(length / 2, (h - t1) / 2 - Yc + offset_y, -Zc + offset_z)
    rectangular_top.Update()

    rectangular_center.SetXLength(length)
    rectangular_center.SetYLength(h - (t1+t2))
    rectangular_center.SetZLength(tw)
    rectangular_center.SetCenter(length / 2, y_center - Yc + offset_y, -Zc + offset_z)
    rectangular_center.Update()

    rectangular_bottom.SetXLength(length)
    rectangular_bottom.SetYLength(t2)
    rectangular_bottom.SetZLength(w2)
    rectangular_bottom.SetCenter(length / 2, -(h - t2) / 2 - Yc + offset_y, -Zc + offset_z)
    rectangular_bottom.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()

def t_beam_data(length, h, w1, t1, tw, offset_y=0, offset_z=0):

    hw = h - t1
    Zc, Yc = TBeamCrossSection(h, w1, t1, tw, offset_y, offset_z).centroid

    rectangular_top = vtkCubeSource()
    rectangular_center = vtkCubeSource()

    rectangular_top.SetXLength(length)
    rectangular_top.SetYLength(t1)
    rectangular_top.SetZLength(w1)
    rectangular_top.SetCenter(length / 2, (hw - t1) / 2 - Yc + offset_y, -Zc + offset_z)
    rectangular_top.Update()

    rectangular_center.SetXLength(length)
    rectangular_center.SetYLength(hw)
    rectangular_center.SetZLength(tw)
    rectangular_center.SetCenter(length / 2, - Yc + offset_y, -Zc + offset_z)
    rectangular_center.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.Update()
    append_polydata.SetObjectName("t_beam_data")

    return append_polydata.GetOutput()

def reducer_data(
    length,
    initial_diameter,
    final_diameter,
    initial_offset_y,
    initial_offset_z,
    final_offset_y,
    final_offset_z,
):
    initial_radius = initial_diameter / 2
    final_radius = final_diameter / 2

    sides = 20

    initial_ring = vtkRegularPolygonSource()
    initial_ring.SetRadius(initial_radius)
    initial_ring.SetNumberOfSides(sides)
    initial_ring.SetCenter(0, initial_offset_y, initial_offset_z)
    initial_ring.SetNormal(1, 0, 0)
    initial_ring.Update()

    final_ring = vtkRegularPolygonSource()
    final_ring.SetRadius(final_radius)
    final_ring.SetNumberOfSides(sides)
    final_ring.SetCenter(length, final_offset_y, final_offset_z)
    final_ring.SetNormal(1, 0, 0)
    final_ring.Update()

    initial_points = initial_ring.GetOutput().GetPoints()
    final_points = final_ring.GetOutput().GetPoints()

    points = vtkPoints()
    points.InsertPoints(0, sides, 0, initial_points)
    points.InsertPoints(sides, sides, 0, final_points)

    external_face = vtkPolyData()
    external_face.Allocate()
    external_face.SetPoints(points)

    for i in range(sides):
        external_face.InsertNextCell(
            VTK_TRIANGLE,
            3,
            [i, i + sides, (i + 1) % sides],
        )
        external_face.InsertNextCell(
            VTK_TRIANGLE,
            3,
            [i + sides, (i + 1) % sides + sides, (i + 1) % sides],
        )

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(initial_ring.GetOutput())
    append_polydata.AddInputData(final_ring.GetOutput())
    append_polydata.AddInputData(external_face)
    append_polydata.Update()

    return append_polydata.GetOutput()

def flange_data(length, outside_diameter, thickness, n_bolts=8, offset_y=0, offset_z=0):
    pipe = closed_pipe_data(length, outside_diameter, offset_y, offset_z)
    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(pipe)
    bolt_radius = outside_diameter / 25
    bolt_length = length + bolt_radius * 2

    for i in range(n_bolts):
        angle = i * 2 * np.pi / n_bolts
        dz = offset_z + (outside_diameter - bolt_radius * 4) * np.cos(angle) / 2
        dy = offset_y + (outside_diameter - bolt_radius * 4) * np.sin(angle) / 2

        bolt = closed_pipe_data(bolt_length, 2*bolt_radius, offset_y=dy, offset_z=dz)
        bolt = apply_transform(bolt, dx=-bolt_radius)
        append_polydata.AddInputData(bolt)

    append_polydata.Update()

    return append_polydata.GetOutput()

def expansion_joint_data(length, outside_diameter, thickness, offset_y=0, offset_z=0):
    append_polydata = vtkAppendPolyData()

    width = 0.15 * outside_diameter
    pipe = pipe_data(length, outside_diameter, thickness)
    start_flange = flange_data(width, outside_diameter + 3*width, width)

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtkTransform()
    transform.Translate(length - width, 0, 0)
    transform.Update()
    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(flange_data(width, outside_diameter + 3*width, width))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    end_flange = transform_filter.GetOutput()

    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(start_flange)
    append_polydata.AddInputData(end_flange)

    # Draw rings in the middle portion of the pipe
    rings = int(3 * length / width / 5)
    for i in range(0, rings, 2):
        position = i / (rings - 1) * (3 * length / 5) + length / 5
        ring = vtkCylinderSource()
        ring.SetHeight(width)
        ring.SetRadius(width + outside_diameter / 2)
        ring.SetCenter(0, position + width / 2, 0)
        ring.SetResolution(15)
        ring.Update()
        ring_data = apply_transform(ring.GetOutput(), rz=-90)
        append_polydata.AddInputData(ring_data)

    tie_rods = 2
    for i in range(tie_rods):
        angle = i * 2 * np.pi / tie_rods
        x = (4 * width + outside_diameter) / 2 * np.sin(angle)
        z = (4 * width + outside_diameter) / 2 * np.cos(angle)

        tie_rod = vtkCylinderSource()
        tie_rod.SetHeight(length)
        tie_rod.SetRadius(width / 2)
        tie_rod.SetCenter(x, length / 2, z)
        tie_rod.Update()
        tie_rod_data = apply_transform(tie_rod.GetOutput(), rz=-90)
        append_polydata.AddInputData(tie_rod_data)

        initial_nut = vtkCubeSource()
        initial_nut.SetCenter(x, width / 2, z)
        initial_nut.SetXLength(2 * width)
        initial_nut.SetYLength(width)
        initial_nut.SetZLength(2.5 * width)
        initial_nut.Update()
        initial_nut_data = apply_transform(initial_nut.GetOutput(), rz=-90)
        append_polydata.AddInputData(initial_nut_data)

        final_nut = vtkCubeSource()
        final_nut.SetCenter(x, length - width / 2, z)
        final_nut.SetXLength(2 * width)
        final_nut.SetYLength(width)
        final_nut.SetZLength(2.5 * width)
        final_nut.Update()
        final_nut_data = apply_transform(final_nut.GetOutput(), rz=-90)
        append_polydata.AddInputData(final_nut_data)

    append_polydata.Update()

    return apply_transform(append_polydata.GetOutput(), dy=offset_y, dz=offset_z)

def valve_data(length, outside_diameter, thickness, flange_diameter, flange_length):
    append_polydata = vtkAppendPolyData()

    if length == 0:
        # empty poly data
        return vtkPolyData()

    pipe = pipe_data(length, outside_diameter, thickness)
    start_flange = flange_data(flange_length, flange_diameter, 0)
    end_flange = apply_transform(start_flange, dx=length - flange_length)
    handle = valve_handle(outside_diameter)
    handle = apply_transform(handle, dx=length/2, rz=90)

    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(start_flange)
    append_polydata.AddInputData(end_flange)
    append_polydata.AddInputData(handle)
    append_polydata.Update()
    
    return append_polydata.GetOutput()

def valve_handle(outside_diameter):
    height = 1.5 * outside_diameter
    width = 0.20 * outside_diameter
    wheel_diameter = outside_diameter * 1.5

    center_sphere = vtkSphereSource()
    center_sphere.SetPhiResolution(20)
    center_sphere.SetThetaResolution(20)
    center_sphere.SetRadius(outside_diameter)
    center_sphere.Update()

    pipe = pipe_data(height, outside_diameter, 0)
    flange = flange_data(width, outside_diameter + width, 0)
    flange = apply_transform(flange, dx=height)
    wheel = apply_transform(
        VALVE_WHEEL,
        rz=-90,
        dx=height,
        sx=wheel_diameter,
        sy=wheel_diameter,
        sz=wheel_diameter,
    )

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(center_sphere.GetOutput())
    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(flange)
    append_polydata.AddInputData(wheel)
    append_polydata.Update()

    return append_polydata.GetOutput()