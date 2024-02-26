from pulse.interface.viewer_3d.vtk.vtkMeshClicker import vtkMeshClicker


class vtkGeometryClicker(vtkMeshClicker):
    def selectionPriority(self, picked_points, picked_elements, picked_entities, box_selection=False):
        '''
        Prioritizes points over other in single click selection.
        '''

        if box_selection:
            return
        
        if len(picked_points) != 1:
            return

        if len(picked_elements) == 1 or len(picked_entities) == 1:
            picked_elements.clear()
            picked_entities.clear()
