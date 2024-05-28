# fmt: off

from pulse import app

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

class DualVolumePSD:
    def __init__(self, device_data : dict) -> None:

        self.project = app().project
        self.preprocessor = app().project.preprocessor

        self.initialize()
        self.unwrap_device_data(device_data)

    def initialize(self):
        self.pipe1_angle = None
        self.pipe2_angle = None
        self.segment_data = list()
        self.branch_data = list()

    def unwrap_device_data(self, device_data : dict):

        self.connection_pipe = device_data["connection pipe"]
        self.connection_point = device_data["connecting coords"]
        self.axis = device_data["main axis"]

        if "volume #1 parameters" in device_data.keys():
            self.volume1_diameter = device_data["volume #1 parameters"][0]
            self.volume1_wall_thickness = device_data["volume #1 parameters"][1]
            self.volume1_length = device_data["volume #1 parameters"][2]
            self.volume1_section_data = [self.volume1_diameter, self.volume1_wall_thickness, 0, 0, 0, 0]

        if "volume #2 parameters" in device_data.keys():
            self.volume2_diameter = device_data["volume #2 parameters"][0]
            self.volume2_wall_thickness = device_data["volume #2 parameters"][1]
            self.volume2_length = device_data["volume #2 parameters"][2]
            self.volume2_section_data = [self.volume2_diameter, self.volume2_wall_thickness, 0, 0, 0, 0]

        if "pipe #1 parameters" in device_data.keys():

            self.pipe1_diameter = device_data["pipe #1 parameters"][0]
            self.pipe1_wall_thickness = device_data["pipe #1 parameters"][1]
            self.pipe1_length = device_data["pipe #1 parameters"][2]

            if len(device_data["pipe #1 parameters"]) == 5:
                self.pipe1_distance = device_data["pipe #1 parameters"][3]
                self.pipe1_angle = device_data["pipe #1 parameters"][4]

            self.pipe1_section_data = [self.pipe1_diameter, self.pipe1_wall_thickness, 0, 0, 0, 0]

        if "pipe #2 parameters" in device_data.keys():

            self.pipe2_diameter = device_data["pipe #2 parameters"][0]
            self.pipe2_wall_thickness = device_data["pipe #2 parameters"][1]
            self.pipe2_length = device_data["pipe #2 parameters"][2]

            if len(device_data["pipe #2 parameters"]) == 5:
                self.pipe2_distance = device_data["pipe #2 parameters"][3]
                self.pipe2_angle = device_data["pipe #2 parameters"][4]
            
            self.pipe2_section_data = [self.pipe2_diameter, self.pipe2_wall_thickness, 0, 0, 0, 0]

        self.volumes_spacing = device_data["volumes spacing"]
        self.volumes_connection = device_data["volumes connection"]

        if "pipe #3 parameters" in device_data.keys():
            if self.volumes_connection in ["pipe", "pipe-plate"]:
                self.pipe3_diameter = device_data["pipe #3 parameters"][0]
                self.pipe3_wall_thickness = device_data["pipe #3 parameters"][1]
                self.pipe3_length = device_data["pipe #3 parameters"][2]
                self.pipe3_distance = device_data["pipe #3 parameters"][3]
                self.pipe3_section_data = [self.pipe3_diameter, self.pipe3_wall_thickness, 0, 0, 0, 0]

        if "pipe #4 parameters" in device_data.keys():
            self.pipe4_diameter = device_data["pipe #4 parameters"][0]
            self.pipe4_wall_thickness = device_data["pipe #4 parameters"][1]
            self.pipe4_length = device_data["pipe #4 parameters"][2]
            self.pipe4_section_data = [self.pipe4_diameter, self.pipe4_wall_thickness, 0, 0, 0, 0]

    def get_axial_axial_segment_data(self):

        inlet = np.array([0, 0, 0], dtype=float)
        versor_x = np.array([1, 0, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        offset_y = np.array([0, 0.01, 0], dtype=float)

        P0 = inlet + versor_x * self.pipe1_length
        Q0 = P0

        Q2 = Q0 + versor_x * self.volume1_length
        Q3 = Q2 + versor_x * self.volumes_spacing
        Q5 = Q3 + versor_x * self.volume2_length
        
        if self.volumes_connection in ["pipe", "pipe-plate"]:
            Q1 = Q0 + versor_x * self.pipe3_distance
            Q4 = Q1 + versor_x * self.pipe3_length
        else:
            Q1 = Q2
            Q4 = Q3

        P1 = Q5
        outlet = Q5 + versor_x * self.pipe2_length

        Q1o = Q1 + offset_y
        Q2o = Q2 + offset_y
        Q3o = Q3 + offset_y
        Q4o = Q4 + offset_y

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o], dtype=float)
        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, P0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, P1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((Q0, Q1, self.volume1_section_data, "volume #1"))
        self.segment_data.append((Q4, Q5, self.volume2_section_data, "volume #2"))

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1o, Q2o, self.pipe3_section_data, "pipe #3"))
            self.segment_data.append((Q3o, Q4o, self.pipe3_section_data, "pipe #3"))
            self.segment_data.append((Q1, Q2, self.volume1_section_data, "volume #1"))
            self.segment_data.append((Q3, Q4, self.volume2_section_data, "volume #2"))

        if self.volumes_connection == "pipe":
            self.segment_data.append((Q2o, Q3o, self.pipe3_section_data, "pipe #3"))

        elif self.volumes_connection == "pipe-plate":
            self.segment_data.append((Q2o, Q3o, self.pipe4_section_data, "pipe #4"))

        else:
            self.segment_data.append((Q2, Q3, self.pipe4_section_data, "pipe #4"))

        self.branch_data.append((P0, "axial"))
        self.branch_data.append((P1, "axial"))

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1, Q1o, "acoustic_link", None))
            self.segment_data.append((Q4, Q4o, "acoustic_link", None))
            self.segment_data.append((Q2, Q2o, "structural_link", None))
            self.segment_data.append((Q3, Q3o, "structural_link", None))

        else:
            self.branch_data.append((Q2, "axial"))
            self.branch_data.append((Q3, "axial"))

    def get_axial_radial_segment_data(self):

        inlet = np.array([0, 0, 0], dtype=float)
        versor_x = np.array([1, 0, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        offset_y = np.array([0, 0.01, 0], dtype=float)

        pipe2_angle = self.pipe2_angle * (np.pi / 180)
        rot_pipe2 =  rotation_about_x_axis(pipe2_angle) @ versor_z

        P0 = inlet + versor_x * self.pipe1_length
        Q0 = P0

        Q2 = Q0 + versor_x * self.volume1_length
        Q3 = Q2 + versor_x * self.volumes_spacing
        Q5 = Q3 + versor_x * self.volume2_length
        
        if self.volumes_connection in ["pipe", "pipe-plate"]:
            Q1 = Q0 + versor_x * self.pipe3_distance
            Q4 = Q1 + versor_x * self.pipe3_length
        else:
            Q1 = Q2
            Q4 = Q3

        P1 = Q0 + versor_x * self.pipe2_distance
        outlet = P1 + rot_pipe2 * self.pipe2_length

        Q1o = Q1 + offset_y
        Q2o = Q2 + offset_y
        Q3o = Q3 + offset_y
        Q4o = Q4 + offset_y

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o], dtype=float)
        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, P0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, P1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((Q0, Q1, self.volume1_section_data, "volume #1"))
        self.segment_data.append((Q4, P1, self.volume2_section_data, "volume #2"))
        self.segment_data.append((P1, Q5, self.volume2_section_data, "volume #2"))
 
        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1o, Q2o, self.pipe3_section_data, "pipe #3"))
            self.segment_data.append((Q3o, Q4o, self.pipe3_section_data, "pipe #3"))
            self.segment_data.append((Q1, Q2, self.volume1_section_data, "volume #1"))
            self.segment_data.append((Q3, Q4, self.volume2_section_data, "volume #2"))
        
        if self.volumes_connection == "pipe":
            self.segment_data.append((Q2o, Q3o, self.pipe3_section_data, "pipe #3"))

        elif self.volumes_connection == "pipe-plate":
            self.segment_data.append((Q2o, Q3o, self.pipe4_section_data, "pipe #4"))

        else:
            self.segment_data.append((Q2, Q3, self.pipe4_section_data, "pipe #4"))

        self.branch_data.append((P0, "axial"))
        self.branch_data.append((P1, "radial"))

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1, Q1o, "acoustic_link", None))
            self.segment_data.append((Q4, Q4o, "acoustic_link", None))
            self.segment_data.append((Q2, Q2o, "structural_link", None))
            self.segment_data.append((Q3, Q3o, "structural_link", None))

        else:
            self.branch_data.append((Q2, "axial"))
            self.branch_data.append((Q3, "axial"))

    def get_radial_axial_segment_data(self):

        inlet = np.array([0, 0, 0], dtype=float)
        versor_x = np.array([1, 0, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        offset_y = np.array([0, 0.01, 0], dtype=float)

        pipe1_angle = self.pipe1_angle * (np.pi / 180)
        rot_pipe1 =  rotation_about_x_axis(pipe1_angle) @ versor_z

        P0 = inlet - rot_pipe1 * self.pipe1_length
        Q0 = P0 - versor_x * self.pipe1_distance

        Q2 = Q0 + versor_x * self.volume1_length
        Q3 = Q2 + versor_x * self.volumes_spacing
        Q5 = Q3 + versor_x * self.volume2_length
        
        if self.volumes_connection in ["pipe", "pipe-plate"]:
            Q1 = Q0 + versor_x * self.pipe3_distance
            Q4 = Q1 + versor_x * self.pipe3_length
        else:
            Q1 = Q2
            Q4 = Q3

        P1 = Q5
        outlet = Q5 + versor_x * self.pipe2_length

        Q1o = Q1 + offset_y
        Q2o = Q2 + offset_y
        Q3o = Q3 + offset_y
        Q4o = Q4 + offset_y

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o], dtype=float)
        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, P0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, P1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((Q0, P0, self.volume1_section_data, "volume #1"))
        self.segment_data.append((P0, Q1, self.volume1_section_data, "volume #1"))
        self.segment_data.append((Q4, Q5, self.volume2_section_data, "volume #2"))

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1, Q2, self.volume1_section_data, "volume #1"))
            self.segment_data.append((Q3, Q4, self.volume2_section_data, "volume #2"))
            self.segment_data.append((Q1o, Q2o, self.pipe3_section_data, "pipe #3"))
            self.segment_data.append((Q3o, Q4o, self.pipe3_section_data, "pipe #3"))
    
        if self.volumes_connection == "pipe":
            self.segment_data.append((Q2o, Q3o, self.pipe3_section_data, "pipe #3"))

        elif self.volumes_connection == "pipe-plate":
            self.segment_data.append((Q2o, Q3o, self.pipe4_section_data, "pipe #4"))

        else:
            self.segment_data.append((Q2, Q3, self.pipe4_section_data, "pipe #4"))

        self.branch_data.append((P0, "radial"))
        self.branch_data.append((P1, "axial"))

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1, Q1o, "acoustic_link", None))
            self.segment_data.append((Q4, Q4o, "acoustic_link", None))
            self.segment_data.append((Q2, Q2o, "structural_link", None))
            self.segment_data.append((Q3, Q3o, "structural_link", None))

        else:
            self.branch_data.append((Q2, "axial"))
            self.branch_data.append((Q3, "axial"))

    def get_radial_radial_segment_data(self):

        inlet = np.array([0, 0, 0], dtype=float)
        versor_x = np.array([1, 0, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        offset_y = np.array([0, 0.01, 0], dtype=float)

        pipe1_angle = self.pipe1_angle * (np.pi / 180)
        rot_pipe1 =  rotation_about_x_axis(pipe1_angle) @ versor_z

        pipe2_angle = self.pipe2_angle * (np.pi / 180)
        rot_pipe2 =  rotation_about_x_axis(pipe2_angle) @ versor_z

        P0 = inlet - rot_pipe1 * self.pipe1_length
        Q0 = P0 - versor_x * self.pipe1_distance

        Q2 = Q0 + versor_x * self.volume1_length
        Q3 = Q2 + versor_x * self.volumes_spacing
        Q5 = Q3 + versor_x * self.volume2_length

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            Q1 = Q0 + versor_x * self.pipe3_distance
            Q4 = Q1 + versor_x * self.pipe3_length
        else:
            Q1 = Q2
            Q4 = Q3

        P1 = Q0 + versor_x * self.pipe2_distance
        outlet = P1 + rot_pipe2 * self.pipe2_length

        Q1o = Q1 + offset_y
        Q2o = Q2 + offset_y
        Q3o = Q3 + offset_y
        Q4o = Q4 + offset_y

        base_points = np.array([inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o], dtype=float)
        if self.connection_pipe == "pipe #2":
            base_points -= outlet

        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5, Q1o, Q2o, Q3o, Q4o = translate_to_connection_point(rot_points, self.connection_point)

        self.segment_data.append((inlet, P0, self.pipe1_section_data, "pipe #1"))
        self.segment_data.append((outlet, P1, self.pipe2_section_data, "pipe #2"))
        self.segment_data.append((Q0, P0, self.volume1_section_data, "volume #1"))
        self.segment_data.append((P0, Q1, self.volume1_section_data, "volume #1"))
        self.segment_data.append((Q4, P1, self.volume2_section_data, "volume #2"))
        self.segment_data.append((P1, Q5, self.volume2_section_data, "volume #2"))

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1, Q2, self.volume1_section_data, "volume #1"))
            self.segment_data.append((Q3, Q4, self.volume2_section_data, "volume #2"))
            self.segment_data.append((Q1o, Q2o, self.pipe3_section_data, "pipe #3"))
            self.segment_data.append((Q3o, Q4o, self.pipe3_section_data, "pipe #3"))
    
        if self.volumes_connection == "pipe":
            self.segment_data.append((Q2o, Q3o, self.pipe3_section_data, "pipe #3"))

        elif self.volumes_connection == "pipe-plate":
            self.segment_data.append((Q2o, Q3o, self.pipe4_section_data, "pipe #4"))

        else:
            self.segment_data.append((Q2, Q3, self.pipe4_section_data, "pipe #4"))

        self.branch_data.append((P0, "radial"))
        self.branch_data.append((P1, "radial"))

        if self.volumes_connection in ["pipe", "pipe-plate"]:
            self.segment_data.append((Q1, Q1o, "acoustic_link", None))
            self.segment_data.append((Q4, Q4o, "acoustic_link", None))
            self.segment_data.append((Q2, Q2o, "structural_link", None))
            self.segment_data.append((Q3, Q3o, "structural_link", None))

        else:
            self.branch_data.append((Q2, "axial"))
            self.branch_data.append((Q3, "axial"))

    def process_double_tunned_psd(self):
        pass

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