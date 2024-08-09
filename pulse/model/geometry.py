class Geometry:
    """A geometry class.
    This class creates a geometry object from input data.

    Parameters
    ----------
    geometry_data : dictionary, optional.
        A dictionary gathering points, lines, areas and volumes info.
    """
    def __init__(self, **kwargs):
        self.reset()
        
    def reset(self):
        self.points = {}
        self.lines = {}
        self.geometry_data = {}

    def set_points(self, point_id, coordinates):
        self.points[point_id] = coordinates

    def set_lines(self, line_id, points):
        self.lines[line_id] = points

    def set_geometry_data(self, geometry_data):
        self.geometry_data = geometry_data

    def get_points(self):
        if "points_data" in self.geometry_data.keys():
            self.points = self.geometry_data['points_data']
        return self.points
    
    def get_lines(self):
        if "lines_data" in self.geometry_data.keys():
            self.lines = self.geometry_data['lines_data']
        return self.lines
    
    def get_geometry_data(self):
        self.geometry_data = {"points_data" : self.points,
                              "lines_data" : self.lines}