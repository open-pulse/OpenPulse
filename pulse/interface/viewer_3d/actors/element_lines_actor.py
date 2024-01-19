import vtk
from vtkat.actors import LinesActor


class ElementLinesActor(LinesActor):
    def __init__(self, project, **kwargs) -> None:
        self.project = project
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())

        lines = self.get_lines()
        super().__init__(lines)
    
    def get_lines(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        self._key_index  = {j:i for i,j in enumerate(visible_elements)}

        lines = []
        for element in visible_elements.values():
            x0, y0, z0 = element.first_node.coordinates
            x1, y1, z1 = element.last_node.coordinates
            lines.append((x0, y0, z0, x1, y1, z1))
        return lines
