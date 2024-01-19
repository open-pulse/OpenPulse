import vtk
from vtkat.actors import RoundPointsActor


class NodesActor(RoundPointsActor):
    def __init__(self, project, **kwargs) -> None:
        self.project = project
        self.nodes = project.get_nodes()
        self.hidden_nodes = kwargs.get('hidden_nodes', set())

        points = self.get_points()
        super().__init__(points)

        self.appear_in_front(True)
        self.GetProperty().SetPointSize(6)
        self.GetProperty().SetColor([i/255 for i in (255, 180, 50)])
    
    def get_points(self):
        nodes = self.project.get_nodes()
        visible_nodes = {i:e for i,e in self.nodes.items() if (i not in self.hidden_nodes)}
        self._key_index = {j:i for i,j in enumerate(visible_nodes)}
        coords = [n.coordinates for n in visible_nodes.values()]
        return coords
