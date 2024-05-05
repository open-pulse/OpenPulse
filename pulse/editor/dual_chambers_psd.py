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

class DualChambersPSD:
    def __init__(self, device_data : dict) -> None:
            
        self.unwrap_device_data(device_data)

    def unwrap_device_data(self, device_data : dict):

        self.connection_pipe = device_data["connection pipe"]
        self.connection_point = device_data["connecting coords"]
        self.axis = device_data["main axis"]

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

        self.volume2_length = device_data["volume #2 parameters"][0]     
        self.volume2_diameter = device_data["volume #2 parameters"][1]
        self.volume2_wall_thickness = device_data["volume #2 parameters"][2] 

        if device_data["volumes connection"] in ["pipe"]:

            self.pipe3_length = device_data["pipe #3 parameters"][0]
            self.pipe3_diameter = device_data["pipe #3 parameters"][1]
            self.pipe3_wall_thickness = device_data["pipe #3 parameters"][2]
            self.pipe3_distance = device_data["pipe #3 parameters"][3]

        self.volumes_spacing = device_data["volumes spacing"]

    def get_points(self):

        # P0 -> connection point between inlet pipe and main chamber
        # P1 -> connection point between outlet pipe and main chamber

        # Q0 -> start point of the volume #1
        # Q1 -> start point of the connecting volumes pipe
        # Q2 -> end point of the volume #1
        # Q3 -> start point of the volume #2
        # Q4 -> end point of the connecting volumes pipe
        # Q5 -> end point of the volume #2

        versor_x = np.array([1, 0, 0], dtype=float)
        versor_y = np.array([0, 1, 0], dtype=float)
        versor_z = np.array([0, 0, 1], dtype=float)
        inlet = np.array([0, 0, 0], dtype=float)

        axial_axial = self.pipe1_angle is None and self.pipe2_angle is None
        if axial_axial:
            pass

        elif self.pipe2_angle is None:
            # radial-axial
            pass

        elif self.pipe1_angle is None:
            # radial-axial
            pass

        else:
            # radial-radial

            inlet_angle = self.pipe1_angle * (np.pi / 180)
            rot_inlet =  rotation_about_x_axis(inlet_angle) @ versor_z

            outlet_angle = self.pipe2_angle * (np.pi / 180)
            rot_outlet =  rotation_about_x_axis(outlet_angle) @ versor_z

            P0 = inlet - rot_inlet * self.pipe1_length
            Q0 = P0 - versor_x * self.pipe1_distance
            P1 = Q0 + versor_x * self.pipe2_distance
            Q1 = Q0 + versor_x * self.pipe3_distance
            Q2 = Q0 + versor_x * self.volume1_length
            Q3 = Q2 + versor_x * self.volumes_spacing
            Q4 = Q1 + versor_x * self.pipe3_length
            Q5 = Q3 + versor_x * self.volume2_length
            outlet = P1 + rot_outlet * self.pipe2_length         

        base_points = [inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5]
        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1, Q2, Q3, Q4, Q5 = translate_to_connection_point(rot_points, self.connection_point)

        self.get_section_parameters()

        self.segment_data = list()

        if axial_axial:
            self.segment_data.append((inlet, Q0, self.pipe1_section_data))
            self.segment_data.append((outlet, Q1, self.pipe2_section_data))

        elif self.pipe1_angle is None:
            self.segment_data.append((inlet, Q0, self.pipe1_section_data))
            self.segment_data.append((outlet, Q1, self.pipe2_section_data))

        elif self.pipe2_angle is None:
            self.segment_data.append((inlet, Q0, self.pipe1_section_data))
            self.segment_data.append((outlet, Q1, self.pipe2_section_data))

        else:

            if np.linalg.norm(P0-Q0) > np.linalg.norm(P1-Q0):
                self.segment_data.append((inlet, P0, self.pipe1_section_data))
                self.segment_data.append((outlet, P1, self.pipe2_section_data))
                self.segment_data.append((Q0, P1, self.volume1_section_data))
                self.segment_data.append((P1, Q2, self.volume1_section_data))
                self.segment_data.append((Q3, P0, self.volume2_section_data))
                self.segment_data.append((P0, Q5, self.volume2_section_data))
                self.segment_data.append((Q1, Q2, self.pipe3_section_data))
                self.segment_data.append((Q2, Q3, self.pipe3_section_data))
                self.segment_data.append((Q3, Q4, self.pipe3_section_data))

            else:
                self.segment_data.append((inlet, P0, self.pipe1_section_data))
                self.segment_data.append((outlet, P1, self.pipe2_section_data))
                self.segment_data.append((Q0, P0, self.volume1_section_data))
                self.segment_data.append((P0, Q2, self.volume1_section_data))
                self.segment_data.append((Q3, P1, self.volume2_section_data))
                self.segment_data.append((P1, Q5, self.volume2_section_data))
                self.segment_data.append((Q1, Q2, self.pipe3_section_data))
                self.segment_data.append((Q2, Q3, self.pipe3_section_data))
                self.segment_data.append((Q3, Q4, self.pipe3_section_data))

    def get_section_parameters(self):
        self.pipe1_section_data = [self.pipe1_diameter, self.pipe1_wall_thickness, 0, 0, 0, 0]
        self.pipe2_section_data = [self.pipe2_diameter, self.pipe2_wall_thickness, 0, 0, 0, 0]
        self.pipe3_section_data = [self.pipe3_diameter, self.pipe3_wall_thickness, 0, 0, 0, 0]
        self.volume1_section_data = [self.volume1_diameter, self.volume1_wall_thickness, 0, 0, 0, 0]
        self.volume2_section_data = [self.volume2_diameter, self.volume2_wall_thickness, 0, 0, 0, 0]

# fmt: on