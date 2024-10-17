from .bend import Bend


class Elbow(Bend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import ElbowActor

        return ElbowActor(self)
