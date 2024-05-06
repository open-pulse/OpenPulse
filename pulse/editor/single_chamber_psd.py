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

def rotate_points(points, axis="along x-axis"):
    if axis == "along y-axis":
        matrix = rotation_matrix_z(np.pi/2)
    elif axis == "along z-axis":
        matrix = rotation_matrix_y(np.pi/2)
    else:
        matrix = np.identity(3)

    rotated_points = list()
    for point in points:
        rotated_point = matrix @ point
        rotated_points.append(rotated_point)
    
    return rotated_points

class SingleChamberPSD:
    def __init__(self, device_data : dict) -> None:

        self.initialize()
        self.unwrap_device_data(device_data)

    def initialize(self):
        self.pipe1_angle = None
        self.pipe2_angle = None

    def unwrap_device_data(self, device_data : dict):

        self.connection_pipe = device_data["connection pipe"]
        self.connection_point = device_data["connecting coords"]
        self.axis = device_data["main axis"]

        self.pipe1_length = device_data["pipe #1 parameters"][0]
        self.pipe1_diameter = device_data["pipe #1 parameters"][1]
        self.pipe1_wall_thickness = device_data["pipe #1 parameters"][2]
        self.pipe1_distance = device_data["pipe #1 parameters"][3]

        if len(device_data["pipe #1 parameters"]) == 5:
            self.pipe1_angle = device_data["pipe #1 parameters"][4]

        self.pipe2_length = device_data["pipe #2 parameters"][0]
        self.pipe2_diameter = device_data["pipe #2 parameters"][1]
        self.pipe2_wall_thickness = device_data["pipe #2 parameters"][2]
        self.pipe2_distance = device_data["pipe #2 parameters"][3]

        if len(device_data["pipe #2 parameters"]) == 5:
            self.pipe2_angle = device_data["pipe #2 parameters"][4]

        self.volume1_length = device_data["volume #1 parameters"][0]     
        self.volume1_diameter = device_data["volume #1 parameters"][1]
        self.volume1_wall_thickness = device_data["volume #1 parameters"][2] 

    def process_segment_data(self):

        # P0 -> connection point between inlet pipe and main chamber
        # P1 -> connection point between outlet pipe and main chamber

        # Q0 -> start point of the main chamber
        # Q1 -> end point of the main chamber

        versor_x = np.array([1, 0, 0], dtype=float)
        versor_y = np.array([0, 1, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        inlet = np.array([0, 0, 0], dtype=float)

        axial_axial = self.pipe1_angle is None and self.pipe2_angle is None
        if axial_axial:

            if self.connection_pipe == "pipe #1":
                Q0 = inlet + versor_x * self.pipe1_distance
                Q1 = Q0 + versor_x * self.volume1_length
                outlet = Q1 + versor_x * self.pipe2_length

            else:
                Q0 = inlet - versor_x * self.pipe2_distance
                Q1 = Q0 - versor_x * self.volume1_length
                outlet = Q1 - versor_x * self.pipe1_length

            P0 = Q0
            P1 = Q1

        elif self.pipe1_angle is None:

            # axial-radial
            pipe2_angle = self.pipe2_angle * (np.pi / 180)
            rot_pipe2 =  rotation_about_x_axis(pipe2_angle) @ versor_z

            if self.connection_pipe == "pipe #1":
                P0 = inlet + versor_x * self.pipe1_length
                Q0 = P0
                P1 = Q0 + versor_x * self.pipe2_distance
                Q1 = Q0 + versor_x * self.volume1_length
                outlet = P1 - rot_pipe2 * self.pipe2_length

            else:
                P0 = inlet - rot_pipe2 * self.pipe2_length
                Q1 = P0 - versor_x * self.pipe2_distance
                P1 = Q1
                Q0 = Q1 + versor_x * self.volume1_length
                outlet = P1 - versor_x * self.pipe1_length 

        elif self.pipe2_angle is None:

            # radial-axial
            pipe1_angle = self.pipe1_angle * (np.pi / 180)
            rot_pipe1 =  rotation_about_x_axis(pipe1_angle) @ versor_z

            if self.connection_pipe == "pipe #1":
                P0 = inlet - rot_pipe1 * self.pipe1_length
                Q0 = P0 - versor_x * self.pipe1_distance
                P1 = Q0 + versor_x * self.volume1_length
                Q1 = P1
                outlet = P1 + versor_x * self.pipe2_length

            else:
                P0 = inlet - versor_x * self.pipe2_length
                Q0 = P0
                Q1 = Q0 - versor_x * self.volume1_length
                P1 = Q1 + versor_x * self.pipe1_distance
                outlet = P1 + rot_pipe1 * self.pipe1_length

        else:

            # radial-radial
            pipe1_angle = self.pipe1_angle * (np.pi / 180)
            rot_pipe1 =  rotation_about_x_axis(pipe1_angle) @ versor_z

            pipe2_angle = self.pipe2_angle * (np.pi / 180)
            rot_pipe2 =  rotation_about_x_axis(pipe2_angle) @ versor_z

            if self.connection_pipe == "pipe #1":
                P0 = inlet - rot_pipe1 * self.pipe1_length
                Q0 = P0 - versor_x * self.pipe1_distance
                P1 = Q0 + versor_x * self.pipe2_distance
                Q1 = Q0 + versor_x * self.volume1_length
                outlet = P1 + rot_pipe2 * self.pipe2_length

            else:
                P0 = inlet - rot_pipe2 * self.pipe2_length
                Q0 = P0 - versor_x * self.pipe2_distance
                P1 = Q0 + versor_x * self.pipe1_distance
                Q1 = Q0 + versor_x * self.volume1_length
                outlet = P1 + rot_pipe1 * self.pipe1_length

        base_points = [inlet, outlet, P0, P1, Q0, Q1]
        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1 = translate_to_connection_point(rot_points, self.connection_point)

        self.get_section_parameters()

        self.segment_data = list()
        if axial_axial:
            if self.connection_pipe == "pipe #1":
                self.segment_data.append((inlet, Q0, self.pipe1_section_data))
                self.segment_data.append((outlet, Q1, self.pipe2_section_data))
                self.segment_data.append((Q0, Q1, self.volume1_section_data))
            else:
                self.segment_data.append((inlet, Q0, self.pipe2_section_data))
                self.segment_data.append((outlet, Q1, self.pipe1_section_data))
                self.segment_data.append((Q0, Q1, self.volume1_section_data))

        elif self.pipe1_angle is None:
            if self.connection_pipe == "pipe #1":
                self.segment_data.append((inlet, P0, self.pipe1_section_data))
                self.segment_data.append((outlet, P1, self.pipe2_section_data))
                self.segment_data.append((P0, P1, self.volume1_section_data))
                self.segment_data.append((P1, Q1, self.volume1_section_data))
            else:
                self.segment_data.append((inlet, P0, self.pipe2_section_data))
                self.segment_data.append((outlet, P1, self.pipe1_section_data))
                self.segment_data.append((P0, P1, self.volume1_section_data))
                self.segment_data.append((P0, Q0, self.volume1_section_data))

        elif self.pipe2_angle is None:
            if self.connection_pipe == "pipe #1":
                self.segment_data.append((inlet, P0, self.pipe1_section_data))
                self.segment_data.append((outlet, P1, self.pipe2_section_data))
                self.segment_data.append((Q0, P0, self.volume1_section_data))
                self.segment_data.append((P0, P1, self.volume1_section_data))
            else:
                self.segment_data.append((inlet, P0, self.pipe2_section_data))
                self.segment_data.append((outlet, P1, self.pipe1_section_data))
                self.segment_data.append((P0, P1, self.volume1_section_data))
                self.segment_data.append((P1, Q1, self.volume1_section_data))

        else:

            if self.connection_pipe == "pipe #1":
                self.segment_data.append((inlet, P0, self.pipe1_section_data))
                self.segment_data.append((outlet, P1, self.pipe2_section_data))
                self.segment_data.append((Q0, P0, self.volume1_section_data))
                self.segment_data.append((P0, P1, self.volume1_section_data))
                self.segment_data.append((P1, Q1, self.volume1_section_data))

            else:
                self.segment_data.append((inlet, P0, self.pipe2_section_data))
                self.segment_data.append((outlet, P1, self.pipe1_section_data))
                self.segment_data.append((Q0, P1, self.volume1_section_data))
                self.segment_data.append((P1, P0, self.volume1_section_data))
                self.segment_data.append((P0, Q1, self.volume1_section_data))

    def get_section_parameters(self):
        self.pipe1_section_data = [self.pipe1_diameter, self.pipe1_wall_thickness, 0, 0, 0, 0]
        self.pipe2_section_data = [self.pipe2_diameter, self.pipe2_wall_thickness, 0, 0, 0, 0]
        self.volume1_section_data = [self.volume1_diameter, self.volume1_wall_thickness, 0, 0, 0, 0]
    
# fmt: on