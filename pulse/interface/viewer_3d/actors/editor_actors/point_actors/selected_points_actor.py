from molde.actors import RoundPointsActor


class SelectedPointsActor(RoundPointsActor):
    def __init__(self, points):
        coords = [p.coords() for p in points]
        super().__init__(coords)
        self.GetProperty().SetColor([i / 255 for i in (255, 50, 50)])
        self.appear_in_front(True)
