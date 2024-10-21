from itertools import chain

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


def load_symbol(path):
    reader = vtkOBJReader()
    reader.SetFileName(str(path))
    reader.Update()
    return reader.GetOutput()


VALVE_WHEEL = load_symbol(SYMBOLS_DIR / "other/valve_wheel.obj")


def closed_pipe_data(length, outside_diameter, offset_y=0, offset_z=0, sides=20):
    cilinder = vtkCylinderSource()
    cilinder.SetResolution(sides)
    cilinder.SetRadius(outside_diameter / 2)
    cilinder.SetCenter(offset_y, length / 2, offset_z)
    cilinder.SetHeight(length)
    cilinder.CappingOn()
    cilinder.Update()
    return cilinder.GetOutput()


def pipe_data(length, outside_diameter, thickness, offset_y=0, offset_z=0, sides=20):
    if (thickness == 0) or (2 * thickness > outside_diameter):
        return closed_pipe_data(length, outside_diameter, offset_y, offset_z, sides)

    outer_radius = outside_diameter / 2
    inner_radius = (outside_diameter) / 2 - thickness

    outer_cilinder = vtkCylinderSource()
    outer_cilinder.SetResolution(sides)
    outer_cilinder.SetRadius(outer_radius)
    outer_cilinder.SetHeight(length)
    outer_cilinder.SetCenter(offset_y, length / 2, offset_z)
    outer_cilinder.CappingOff()
    outer_cilinder.Update()

    inner_cilinder = vtkCylinderSource()
    inner_cilinder.SetResolution(sides)
    inner_cilinder.SetRadius(inner_radius)
    inner_cilinder.SetHeight(length)
    inner_cilinder.SetCenter(offset_y, length / 2, offset_z)
    inner_cilinder.CappingOff()
    inner_cilinder.Update()

    ring_bottom = vtkDiskSource()
    ring_bottom.SetCircumferentialResolution(sides)
    ring_bottom.SetOuterRadius(outer_radius)
    ring_bottom.SetInnerRadius(inner_radius)
    ring_bottom.SetCenter(offset_y, 0, offset_z)
    ring_bottom.SetNormal(0, 1, 0)
    ring_bottom.Update()

    ring_top = vtkDiskSource()
    ring_top.SetCircumferentialResolution(sides)
    ring_top.SetOuterRadius(outer_radius)
    ring_top.SetInnerRadius(inner_radius)
    ring_top.SetCenter(offset_y, length, offset_z)
    ring_top.SetNormal(0, 1, 0)
    ring_top.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(outer_cilinder.GetOutput())
    append_polydata.AddInputData(inner_cilinder.GetOutput())
    append_polydata.AddInputData(ring_bottom.GetOutput())
    append_polydata.AddInputData(ring_top.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def circular_beam_data(length, outside_diameter, thickness, offset_y=0, offset_z=0):
    cilinder = vtkCylinderSource()
    cilinder.SetResolution(12)
    cilinder.SetRadius(outside_diameter / 2)
    cilinder.SetHeight(length)
    cilinder.SetCenter(offset_y, length / 2, offset_z)
    cilinder.CappingOn()
    cilinder.Update()
    return cilinder.GetOutput()


def closed_rectangular_beam_data(length, b, h, offset_y=0, offset_z=0):
    rectangle = vtkCubeSource()
    rectangle.SetYLength(length)
    rectangle.SetXLength(b)
    rectangle.SetZLength(h)
    rectangle.SetCenter(offset_y, length / 2, offset_z)
    rectangle.Update()
    return rectangle.GetOutput()


def rectangular_beam_data(length, b, h, t0, t1, offset_y=0, offset_z=0):
    if t0 == 0 or t1 == 0:
        return closed_rectangular_beam_data(length, b, h, offset_y, offset_z)

    rectangular_top = vtkCubeSource()
    rectangular_left = vtkCubeSource()
    rectangular_right = vtkCubeSource()
    rectangular_bottom = vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(b)
    rectangular_top.SetCenter(offset_y, length / 2, -h / 2 + t1 / 2 + offset_z)

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(t0)
    rectangular_left.SetCenter(offset_y - b / 2 + t0 / 2, length / 2, offset_z)

    rectangular_right.SetYLength(length)
    rectangular_right.SetZLength(h)
    rectangular_right.SetXLength(t0)
    rectangular_right.SetCenter(offset_y + b / 2 - t0 / 2, length / 2, offset_z)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t1)
    rectangular_bottom.SetXLength(b)
    rectangular_bottom.SetCenter(offset_y, length / 2, h / 2 - t1 / 2 + offset_z)

    rectangular_top.Update()
    rectangular_left.Update()
    rectangular_right.Update()
    rectangular_bottom.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_right.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def c_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=0, offset_z=0):
    rectangular_top = vtkCubeSource()
    rectangular_left = vtkCubeSource()
    rectangular_bottom = vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(offset_y + w1 / 2 - max(w1, w2) / 2, length / 2, -h / 2 + t1 / 2 + offset_z)

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(tw)
    rectangular_left.SetCenter(offset_y - max(w1, w2) / 2 + tw / 2, length / 2, offset_z)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(offset_y + w2 / 2 - max(w1, w2) / 2, length / 2, h / 2 - t2 / 2 + offset_z)

    rectangular_top.Update()
    rectangular_left.Update()
    rectangular_bottom.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def i_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=0, offset_z=0):
    rectangular_top = vtkCubeSource()
    rectangular_center = vtkCubeSource()
    rectangular_bottom = vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(offset_y, length / 2, -h / 2 + t1 / 2 + offset_z)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetCenter(offset_y, length / 2, offset_z)
    rectangular_center.SetXLength(tw)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(offset_y, length / 2, h / 2 - t2 / 2 + offset_z)

    rectangular_top.Update()
    rectangular_center.Update()
    rectangular_bottom.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def t_beam_data(length, h, w1, t1, tw, offset_y=0, offset_z=0):
    rectangular_top = vtkCubeSource()
    rectangular_center = vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(offset_y, length / 2, -h / 2 + t1 / 2 + offset_z)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetCenter(offset_y, length / 2, offset_z)
    rectangular_center.SetXLength(tw)

    rectangular_top.Update()
    rectangular_center.Update()

    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.Update()

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
    initial_ring.SetCenter(initial_offset_y, 0, initial_offset_z)
    initial_ring.SetNormal(0, 1, 0)
    initial_ring.Update()

    final_ring = vtkRegularPolygonSource()
    final_ring.SetRadius(final_radius)
    final_ring.SetNumberOfSides(sides)
    final_ring.SetCenter(final_offset_y, length, final_offset_z)
    final_ring.SetNormal(0, 1, 0)
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


def flange_data(length, outside_diameter, thickness, n_bolts=8):
    pipe = pipe_data(length, outside_diameter, thickness)
    append_polydata = vtkAppendPolyData()
    append_polydata.AddInputData(pipe)
    bolt_radius = thickness / 6

    for i in range(n_bolts):
        angle = i * 2 * np.pi / n_bolts
        bolt = vtkCylinderSource()
        bolt.SetHeight(length + thickness / 2)
        bolt.SetRadius(bolt_radius)
        bolt.SetCenter(
            (outside_diameter - bolt_radius * 4) * np.sin(angle) / 2,
            length / 2,
            (outside_diameter - bolt_radius * 4) * np.cos(angle) / 2,
        )
        bolt.Update()
        append_polydata.AddInputData(bolt.GetOutput())

    append_polydata.Update()
    return append_polydata.GetOutput()


def expansion_joint_data(length, outside_diameter, thickness):
    append_polydata = vtkAppendPolyData()

    width = 0.15 * outside_diameter
    pipe = pipe_data(length, outside_diameter, thickness)
    start_flange = flange_data(width, outside_diameter + width, width)

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtkTransform()
    transform.Translate(0, length - width, 0)
    transform.Update()
    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(flange_data(width, outside_diameter + width, width))
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
        append_polydata.AddInputData(ring.GetOutput())

    tie_rods = 2
    for i in range(tie_rods):
        angle = i * 2 * np.pi / tie_rods
        x = (3 * width + outside_diameter) / 2 * np.sin(angle)
        z = (3 * width + outside_diameter) / 2 * np.cos(angle)

        tie_rod = vtkCylinderSource()
        tie_rod.SetHeight(length)
        tie_rod.SetRadius(width / 2)
        tie_rod.SetCenter(x, length / 2, z)
        tie_rod.Update()
        append_polydata.AddInputData(tie_rod.GetOutput())

        initial_nut = vtkCubeSource()
        initial_nut.SetCenter(x, width / 2, z)
        initial_nut.SetXLength(2 * width)
        initial_nut.SetYLength(width)
        initial_nut.SetZLength(2 * width)
        initial_nut.Update()
        append_polydata.AddInputData(initial_nut.GetOutput())

        final_nut = vtkCubeSource()
        final_nut.SetCenter(x, length - width / 2, z)
        final_nut.SetXLength(2 * width)
        final_nut.SetYLength(width)
        final_nut.SetZLength(2 * width)
        final_nut.Update()
        append_polydata.AddInputData(final_nut.GetOutput())

    append_polydata.Update()
    return append_polydata.GetOutput()


def valve_data(length, outside_diameter, thickness):
    append_polydata = vtkAppendPolyData()

    if length == 0:
        # empty poly data
        return vtkPolyData()

    width = 0.20 * outside_diameter
    pipe = pipe_data(length, outside_diameter, thickness)
    start_flange = flange_data(width, outside_diameter + width, width)

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtkTransform()
    transform.Translate(0, length - width, 0)
    transform.Update()
    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(flange_data(width, outside_diameter + width, width))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    end_flange = transform_filter.GetOutput()

    center_sphere = vtkSphereSource()
    center_sphere.SetPhiResolution(20)
    center_sphere.SetThetaResolution(20)
    center_sphere.SetRadius(outside_diameter)
    center_sphere.SetCenter(0, length / 2, 0)
    center_sphere.Update()

    transform = vtkTransform()
    transform.Translate(0, length / 2, 0)
    transform.RotateZ(90)
    transform.Translate(0, outside_diameter / 3, 0)
    transform.Update()
    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(valve_handle(outside_diameter, length / 4, width))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    handle = transform_filter.GetOutput()

    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(start_flange)
    append_polydata.AddInputData(end_flange)
    append_polydata.AddInputData(center_sphere.GetOutput())
    append_polydata.AddInputData(handle)

    append_polydata.Update()
    return append_polydata.GetOutput()


def valve_handle(outside_diameter, height, axis_diameter):
    append_polydata = vtkAppendPolyData()
    width = 0.20 * outside_diameter

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtkTransform()
    transform.Translate(0, (height - axis_diameter), 0)
    transform.Update()
    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(
        flange_data(axis_diameter, outside_diameter + width, axis_diameter)
    )
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    end_flange = transform_filter.GetOutput()

    pipe = pipe_data(height, outside_diameter, 0)

    wheel_diameter = outside_diameter * 1.5
    transform = vtkTransform()
    transform.Translate(0, height, 0)
    transform.Scale(wheel_diameter, wheel_diameter, wheel_diameter)
    transform.Update()
    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(VALVE_WHEEL)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    wheel = transform_filter.GetOutput()

    append_polydata.AddInputData(end_flange)
    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(wheel)
    append_polydata.Update()
    return append_polydata.GetOutput()
