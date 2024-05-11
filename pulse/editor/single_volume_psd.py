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

class SingleVolumePSD:
    def __init__(self, device_data : dict) -> None:

        self.initialize()
        self.unwrap_device_data(device_data)
        self.get_section_parameters()

    def initialize(self):
        self.pipe1_angle = None
        self.pipe2_angle = None
        self.segment_data = list()
        self.branch_data = list()

    def unwrap_device_data(self, device_data : dict):

        self.connection_pipe = device_data["connection pipe"]
        self.connection_point = device_data["connecting coords"]
        self.axis = device_data["main axis"]

        self.pipe1_diameter = device_data["pipe #1 parameters"][0]
        self.pipe1_wall_thickness = device_data["pipe #1 parameters"][1]
        self.pipe1_length = device_data["pipe #1 parameters"][2]

        if len(device_data["pipe #1 parameters"]) == 5:
            self.pipe1_distance = device_data["pipe #1 parameters"][3]
            self.pipe1_angle = device_data["pipe #1 parameters"][4]

        self.pipe2_diameter = device_data["pipe #2 parameters"][0]
        self.pipe2_wall_thickness = device_data["pipe #2 parameters"][1]
        self.pipe2_length = device_data["pipe #2 parameters"][2]

        if len(device_data["pipe #2 parameters"]) == 5:
            self.pipe2_distance = device_data["pipe #2 parameters"][3]
            self.pipe2_angle = device_data["pipe #2 parameters"][4]

        self.volume1_diameter = device_data["volume #1 parameters"][0]
        self.volume1_wall_thickness = device_data["volume #1 parameters"][1] 
        self.volume1_length = device_data["volume #1 parameters"][2]     

    def get_section_parameters(self):
        self.pipe1_section_data = [self.pipe1_diameter, self.pipe1_wall_thickness, 0, 0, 0, 0]
        self.pipe2_section_data = [self.pipe2_diameter, self.pipe2_wall_thickness, 0, 0, 0, 0]
        self.volume1_section_data = [self.volume1_diameter, self.volume1_wall_thickness, 0, 0, 0, 0]

    def get_axial_axial_segment_data(self):

        versor_x = np.array([1, 0, 0], dtype=float)
        inlet = np.array([0, 0, 0], dtype=float)

        Q0 = inlet + versor_x * self.pipe1_length
        Q1 = Q0 + versor_x * self.volume1_length
        outlet = Q1 + versor_x * self.pipe2_length
        P0 = Q0
        P1 = Q1

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1], dtype=float)

        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1 = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, Q0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, Q1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((Q0, Q1, self.volume1_section_data, "volume #1"))

        self.branch_data.append((P0, "axial"))
        self.branch_data.append((P1, "axial"))

    def get_axial_radial_segment_data(self):

        versor_x = np.array([1, 0, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        inlet = np.array([0, 0, 0], dtype=float)

        pipe2_angle = self.pipe2_angle * (np.pi / 180)
        rot_pipe2 =  rotation_about_x_axis(pipe2_angle) @ versor_z

        P0 = inlet + versor_x * self.pipe1_length
        Q0 = P0
        P1 = Q0 + versor_x * self.pipe2_distance
        Q1 = Q0 + versor_x * self.volume1_length
        outlet = P1 + rot_pipe2 * self.pipe2_length

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1], dtype=float)

        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1 = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, P0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, P1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((P0, P1, self.volume1_section_data, "volume #1"))
        self.segment_data.append((P1, Q1, self.volume1_section_data, "volume #1"))

        self.branch_data.append((P0, "axial"))
        self.branch_data.append((P1, "radial"))

    def get_radial_axial_segment_data(self):

        versor_x = np.array([1, 0, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        inlet = np.array([0, 0, 0], dtype=float)

        pipe1_angle = self.pipe1_angle * (np.pi / 180)
        rot_pipe1 =  rotation_about_x_axis(pipe1_angle) @ versor_z

        P0 = inlet - rot_pipe1 * self.pipe1_length
        Q0 = P0 - versor_x * self.pipe1_distance
        P1 = Q0 + versor_x * self.volume1_length
        Q1 = P1
        outlet = P1 + versor_x * self.pipe2_length

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1], dtype=float)

        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1 = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, P0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, P1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((Q0, P0, self.volume1_section_data, "volume #1"))
        self.segment_data.append((P0, P1, self.volume1_section_data, "volume #1"))

        self.branch_data.append((P0, "radial"))
        self.branch_data.append((P1, "axial"))

    def get_radial_radial_segment_data(self):

        versor_x = np.array([1, 0, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        inlet = np.array([0, 0, 0], dtype=float)

        pipe1_angle = self.pipe1_angle * (np.pi / 180)
        rot_pipe1 =  rotation_about_x_axis(pipe1_angle) @ versor_z

        pipe2_angle = self.pipe2_angle * (np.pi / 180)
        rot_pipe2 =  rotation_about_x_axis(pipe2_angle) @ versor_z

        P0 = inlet - rot_pipe1 * self.pipe1_length
        Q0 = P0 - versor_x * self.pipe1_distance
        P1 = Q0 + versor_x * self.pipe2_distance
        Q1 = Q0 + versor_x * self.volume1_length
        outlet = P1 + rot_pipe2 * self.pipe2_length

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1], dtype=float)

        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1 = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, P0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, P1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((Q0, P0, self.volume1_section_data, "volume #1"))
        self.segment_data.append((P0, P1, self.volume1_section_data, "volume #1"))
        self.segment_data.append((P1, Q1, self.volume1_section_data, "volume #1"))

        self.branch_data.append((P0, "radial"))
        self.branch_data.append((P1, "radial"))

    def process_segment_data(self):

        if self.pipe1_angle is None and self.pipe2_angle is None:
            self.get_axial_axial_segment_data()

        elif self.pipe1_angle is None:
            self.get_axial_radial_segment_data()

        elif self.pipe2_angle is None:
            self.get_radial_axial_segment_data()

        else:
            self.get_radial_radial_segment_data()

# fmt: on