import vtk
import numpy as np 
from time import time
from scipy.spatial.transform import Rotation

from pulse.interface.tubeActor import TubeActor
from pulse.uix.vtk.colorTable import ColorTable

class TubeDeformedActor(TubeActor):
    def __init__(self, elements, project):
        super().__init__(elements, project)
        self.transparent = False

    def source(self):
        points = vtk.vtkPoints()
        sources = vtk.vtkIntArray()
        sources.SetName('sources')
        rotations = vtk.vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName('rotations')

        cache = dict()
        counter = 0
        
        for element in self.elements.values():
            x,y,z = element.first_node.deformed_coordinates
            points.InsertNextPoint(x,y,z)
            section_rotation_xyz = element.deformed_rotation_xyz

            rotations.InsertNextTuple(section_rotation_xyz)

            self._colors.InsertNextTuple((255,255,255))

            if element.cross_section not in cache:
                cache[element.cross_section] = counter
                # source = self.createTubeSectionDeformed(element)
                source = self.createTubeSection(element)
                self._mapper.SetSourceData(counter, source)
                counter += 1
            sources.InsertNextTuple1(cache[element.cross_section])
     
        self._data.SetPoints(points)
        self._data.GetPointData().AddArray(sources)
        self._data.GetPointData().AddArray(rotations)

    def createTubeSectionDeformed(self, element):
        transformation = vtk.vtkTransform()
        data = vtk.vtkTransformPolyDataFilter()
        extruderFilter = vtk.vtkLinearExtrusionFilter()
        matrix = vtk.vtkMatrix4x4()

        polygon = self.createSectionPolygon(element)
        size = self.project.get_element_size()
        vector = element.section_normal_vectors_at_lcs()

        start_point = [0,0,0]
        mat = element.rotation_matrix_results_at_local_coordinate_system

        matrix.Identity()

        for i in range(3):
            matrix.SetElement(i, 0, mat[i,0])
            matrix.SetElement(i, 1, mat[i,1])
            matrix.SetElement(i, 2, mat[i,2])

        transformation.Translate(start_point)
        transformation.Concatenate(matrix)
        data.SetTransform(transformation)
        data.SetInputConnection(polygon.GetOutputPort())

        # extruderFilter.SetInputConnection(polygon.GetOutputPort())
        extruderFilter.SetInputConnection(data.GetOutputPort())
        extruderFilter.SetExtrusionTypeToVectorExtrusion()
        extruderFilter.SetVector(vector)
        extruderFilter.SetScaleFactor(size)
        extruderFilter.Update()
        return extruderFilter.GetOutput()
