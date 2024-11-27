# fmt: off

import numpy as np

def translate_to_connection_point(points, connection_point):
    translated_points = list()
    for point in points:
        translated_point = point + connection_point
        translated_points.append(translated_point)
    return translated_points    

def rotation_about_x_axis(angle):
    return np.array([[ 1,              0,              0],
                     [ 0,  np.cos(angle), -np.sin(angle)], 
                     [ 0,  np.sin(angle),  np.cos(angle)]], dtype=float)

def rotation_matrix_y(angle):
    return np.array([[ np.cos(angle), 0, np.sin(angle)], 
                     [             0, 1,             0], 
                     [-np.sin(angle), 0, np.cos(angle)]], dtype=float)

def rotation_matrix_z(angle):
    return np.array([[ np.cos(angle), -np.sin(angle), 0],
                     [ np.sin(angle),  np.cos(angle), 0], 
                     [             0,              0, 1]], dtype=float)

def rotate_points(points, axis="x-axis (+)"):
    if axis == "y-axis (+)":
        matrix = rotation_matrix_z(np.pi/2)
    elif axis == "y-axis (-)":
        matrix = rotation_matrix_z(-np.pi/2)
    elif axis == "z-axis (+)":
        matrix = rotation_matrix_y(-np.pi/2)
    elif axis == "z-axis (-)":
        matrix = rotation_matrix_y(np.pi/2)
    elif axis == "x-axis (-)":
        matrix = rotation_matrix_y(np.pi)
    else:
        matrix = np.identity(3)

    rotated_points = list()
    for point in points:
        rotated_point = matrix @ point
        rotated_points.append(rotated_point)
    
    return rotated_points

class PulsationDamper:
    def __init__(self, device_data : dict) -> None:

        self._initialize()
        self.unwrap_device_data(device_data)
        self.get_section_parameters()

    def _initialize(self):
        self.segment_data = list()
        self.elc_data = list()

    def unwrap_device_data(self, device_data : dict):

        self.connection_point = device_data["connecting_coords"]
        self.damper_type = device_data["damper_type"]
        self.axis = device_data["main_axis"]

        self.damper_volume = device_data["damper_volume"]
        self.gas_volume = device_data["gas_volume"]

        self.damper_outside_diameter = device_data["damper_outside_diameter"]
        self.wall_thickness = device_data["wall_thickness"]
        
        if "neck_outside_diameter" in device_data.keys():
            self.neck_outside_diameter = device_data["neck_outside_diameter"]

        if "neck_height" in device_data.keys():
            self.neck_height = device_data["neck_height"]

        self.liquid_fluid_id = device_data["liquid_fluid_id"]
        self.gas_fluid_id = device_data["gas_fluid_id"]

    def process_damper_heights(self):

        d_in = self.damper_outside_diameter - 2*self.wall_thickness
        area = (np.pi / 4) * (d_in**2) 

        self.liquid_height = (self.damper_volume - self.gas_volume) / area
        self.gas_height = self.gas_volume / area

    def get_section_parameters(self):
        self.liquid_section_data = [self.damper_outside_diameter, self.wall_thickness, 0, 0, 0, 0]
        self.gas_section_data = [self.damper_outside_diameter, self.wall_thickness, 0, 0, 0, 0]
        self.neck_section_data = [self.neck_outside_diameter, self.wall_thickness, 0, 0, 0, 0]

    def get_axial_axial_segment_data(self):

        versor_x = np.array([1, 0, 0], dtype=float)
        origin = np.array([0, 0, 0], dtype=float)

        P0 = origin
        P1 = P0 + versor_x * self.neck_height
        P2 = P1 + versor_x * self.liquid_height
        P3 = P2 + versor_x * self.gas_height

        base_points = np.array([P0, P1, P2, P3], dtype=float)

        rot_points = rotate_points(base_points, axis=self.axis)
        P0, P1, P2, P3 = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((P0, P1, self.neck_section_data, "neck", self.liquid_fluid_id))
        self.segment_data.append((P1, P2, self.liquid_section_data, "liquid_filled", self.liquid_fluid_id))
        self.segment_data.append((P2, P3, self.gas_section_data, "gas_filled", self.gas_fluid_id))

        self.elc_data.append((P0, "side-branch"))
        self.elc_data.append((P1, "expansion"))

    def process_segment_data(self):

        self.process_damper_heights()

        if self.damper_type in ["Bladder", "bladder"]:
            self.get_axial_axial_segment_data()

# fmt: on