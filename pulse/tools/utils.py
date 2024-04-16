import os
import configparser
import numpy as np
from time import time
from functools import wraps
from scipy.sparse import issparse

from pathlib import Path
from scipy.spatial.transform import Rotation

from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

def split_sequence(sequence, size):
    ''' 
    This function breaks a sequence in equal sized blocks of choosen size.

    Parameters
    ----------
    sequence: list like object
              Any iterable object.

    size: int
          Size of the desired chunks.

    Returns
    -------
    out: list
         list with small chuncks with desired size.

    Examples
    --------
        >>> colors  = [255,0,0,0,255,0,0,0,255] # a list with colors concatenated.
        >>> split_sequence(colors, 3)
        [[255,0,0], [0,255,0], [0,0,255]]
    '''

    subsequences = []
    for start in range(0, len(sequence), size):
        end = start + size
        subsequence = sequence[start:end]
        subsequences.append(subsequence)
    return subsequences

def unwrap(data):
    return list(data[0]) if data else []

def slicer(iterable, argument):
    ''' 
    A function to deal better with elements. 

    Parameters
    ----------
    iterable: Iterable sequence.

    argument: str, int, iterable
              argument can be 'all', the index, or a sequence of indexes
    
    Yields
    ------
    out: Value according to the argument.

    Examples
    --------
    >>> sequence = ['a', 'b', 'c', 'd']
    >>> for i in slicer(sequence, [1,3,2]):
            print(i)
    'b'
    'd'
    'c'
    >>> for i in slicer(sequence, 'all'):
        print(i)
    'a'
    'b'
    'c'
    'd'
    '''

    if isinstance(argument, str) and argument == 'all':
        if isinstance(iterable, dict):
            for i in iterable.values():
                yield i 
        else:
            for i in iterable:
                yield i 

    elif isinstance(argument, int):
        yield iterable[argument]
    
    elif hasattr(argument, '__iter__'):
        for i in argument:
            yield iterable[i]
            
    else:
        raise AttributeError('Argument not supported')

def timer(function):
    ''' 
    A decorator to time functions.

    Parameters
    ----------
    function: Any function.

    Returns
    -------
    function: A function that does the same as input, but prints the time spent.

    Examples
    --------
    >>> @timer
    >>> def timeConsumingFunction(x):
    ...     doSomethingHeavy()
    ...
    >>> timeConsumingFunction(5)
    Time to finish timeConsumingFunction: 35.5235 [s]
    '''

    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time()
        values = function(*args, **kwargs)
        end_time = time()
        print(f'Time to finish {function.__name__}: {end_time - start_time} [s]')
        return values
    return wrapper
    
def m_to_mm(value):
    ''' 
    Converts meters to millimeters.

    Parameters
    ----------
    m: int, float
        Value in meters

    Returns
    -------
    out: float
        Value in millimeters
    '''
    if isinstance(value, list):
        return np.array(value) * 1e3
    elif isinstance(value, np.ndarray):
        return value * 1e3
    return float(value) * 1e3

def in_to_mm(value):
    ''' 
    Converts inches to millimeters.

    Parameters
    ----------
    m: int, float
        Value in meters

    Returns
    -------
    out: float
        Value in millimeters
    '''
    if isinstance(value, list):
        return np.array(value) * 25.4
    elif isinstance(value, np.ndarray):
        return value * 25.4
    return float(value) * 25.4

def in_to_m(value):
    ''' 
    Converts inches to meters.

    Parameters
    ----------
    value: int, float, list, np.ndarray
        Value in inches

    Returns
    -------
    out: float or np.ndarray
        Value in meters
    '''
    if isinstance(value, list):
        return np.array(value) * 0.0254
    elif isinstance(value, np.ndarray):
        return value * 0.0254
    return float(value) * 0.0254

def mm_to_m(value):
    ''' 
    Converts millimeters to meters.

    Parameters
    ----------
    mm: int, float
        Value in millimeters

    Returns
    -------
    out: float
        Value in meters

    '''
    if isinstance(value, list):
        return np.array(value) * 1e-3
    elif isinstance(value, np.ndarray):
        return value * 1e-3
    return float(value) * 1e-3

def mm_to_in(value):
    ''' 
    Converts inches to millimeters.

    Parameters
    ----------
    m: int, float
        Value in meters

    Returns
    -------
    out: float
        Value in millimeters
    '''
    if isinstance(value, list):
        return np.array(value) / 25.4
    elif isinstance(value, np.ndarray):
        return value / 25.4
    return float(value) / 25.4

def um_to_m(value):
    ''' 
    Converts millimeters to meters.

    Parameters
    ----------
    mm: int, float
        Value in millimeters

    Returns
    -------
    out: float
        Value in meters

    '''
    if isinstance(value, list):
        return np.array(value) * 1e-6
    elif isinstance(value, np.ndarray):
        return value * 1e-6
    return float(value) * 1e-6

def inverse_matrix_Nx3x3(A):
    ''' 
    Given a 3x3xN matrix, compute its inverse faster than 
    numpy's default function.

    Parameters
    ----------
    A: numpy.ndarray
        Matrix of shape (N,3,3)
    
    Returns
    -------
    out: numpy.ndarray
        inverse matrix
    '''
    
    b = 1/( A[:,0,0]*A[:,1,1]*A[:,2,2] + A[:,0,1]*A[:,1,2]*A[:,2,0] +
            A[:,0,2]*A[:,1,0]*A[:,2,1] - A[:,0,2]*A[:,1,1]*A[:,2,0] -
            A[:,0,1]*A[:,1,0]*A[:,2,2] - A[:,0,0]*A[:,1,2]*A[:,2,1] )

    b11 =    A[:,1,1]*A[:,2,2] - A[:,1,2]*A[:,2,1]
    b12 = -( A[:,0,1]*A[:,2,2] - A[:,0,2]*A[:,2,1] )
    b13 =    A[:,0,1]*A[:,1,2] - A[:,0,2]*A[:,1,1]
    
    b21 = -( A[:,1,0]*A[:,2,2] - A[:,1,2]*A[:,2,0] )
    b22 =    A[:,0,0]*A[:,2,2] - A[:,0,2]*A[:,2,0]
    b23 = -( A[:,0,0]*A[:,1,2] - A[:,0,2]*A[:,1,0] )

    b31 =    A[:,1,0]*A[:,2,1] - A[:,1,1]*A[:,2,0]
    b32 = -( A[:,0,0]*A[:,2,1] - A[:,0,1]*A[:,2,0] )
    b33 =    A[:,0,0]*A[:,1,1] - A[:,0,1]*A[:,1,0]

    data = (b*np.array([[b11,b12,b13],[b21,b22,b23],[b31,b32,b33]]))
    invA = np.transpose(data, axes=[2,0,1])
    
    return invA

def inverse_matrix_3x3(A):
    '''    
    Given a 3x3 matrix, compute its inverse faster than
    numpy's default function.

    Parameters
    ----------
    A: numpy.ndarray
        Matrix of shape (3,3)
    
    Returns
    -------
    out: numpy.ndarray
        inverse matrix

    '''
    
    b = 1/( A[0,0]*A[1,1]*A[2,2] + A[0,1]*A[1,2]*A[2,0] +
            A[0,2]*A[1,0]*A[2,1] - A[0,2]*A[1,1]*A[2,0] -
            A[0,1]*A[1,0]*A[2,2] - A[0,0]*A[1,2]*A[2,1] )

    b11 =    A[1,1]*A[2,2] - A[1,2]*A[2,1]
    b12 = -( A[0,1]*A[2,2] - A[0,2]*A[2,1] )
    b13 =    A[0,1]*A[1,2] - A[0,2]*A[1,1]
    
    b21 = -( A[1,0]*A[2,2] - A[1,2]*A[2,0] )
    b22 =    A[0,0]*A[2,2] - A[0,2]*A[2,0]
    b23 = -( A[0,0]*A[1,2] - A[0,2]*A[1,0] )

    b31 =    A[1,0]*A[2,1] - A[1,1]*A[2,0]
    b32 = -( A[0,0]*A[2,1] - A[0,1]*A[2,0] )
    b33 =    A[0,0]*A[1,1] - A[0,1]*A[1,0]

    invA = b*np.array([[b11,b12,b13],[b21,b22,b23],[b31,b32,b33]])
    
    return invA

def transformation_matrix_3x3(delta_x, delta_y, delta_z, gamma=0):
    '''    
    This method returns the rotation matrix of an element 
    based on its spatial position. 
    
    Parameters
    ----------
    delta_x: int, float
        value in meters
    
    delta_y: int, float
        value in meters

    delta_z: int, float
        value in meters

    Returns
    -------
    out: numpy.ndarray(3,3)
        rotation matrix

    '''

    L_ = np.sqrt(delta_x**2 + delta_y**2)
    L  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    cossine_epsilon = L_ / L
    sine_epsilon = - delta_z / L
    
    if L_ > 0.0001*L:
        sine_delta = delta_y/L_
        cossine_delta = delta_x/L_
    else:
        sine_delta = 0
        cossine_delta = 1
    
    cossine_gamma = np.cos(gamma)
    sine_gamma = np.sin(gamma)

    # Matrices product order - Rx@Ry@Rz (@Palazzolo, A. Vibration theory and applications with finite element and active vibration control. pg 677)
    rotation_matrix = np.array([    [   cossine_delta * cossine_epsilon, 
                                       sine_delta * cossine_epsilon, 
                                        -sine_epsilon   ], 
                                    [   cossine_delta * sine_epsilon * sine_gamma - sine_delta * cossine_gamma,
                                        sine_delta * sine_epsilon * sine_gamma + cossine_delta * cossine_gamma,
                                        cossine_epsilon * sine_gamma    ],
                                    [   cossine_delta * sine_epsilon * cossine_gamma + sine_delta * sine_gamma,
                                        sine_delta * sine_epsilon * cossine_gamma - cossine_delta * sine_gamma,
                                        cossine_epsilon * cossine_gamma ]    ]) 

    return rotation_matrix


def transformation_matrix_3x3xN(delta_x, delta_y, delta_z, gamma=0):
    '''    
    This method returns the rotation matrices to a set of N elements 
    based on their spatial positions. 
    
    Parameters
    ----------
    delta_x: numpy.ndarray
        values in meters
    
    delta_y: numpy.ndarray
        values in meters

    delta_z: numpy.ndarray
        values in meters

    Returns
    -------
    out: numpy.ndarray(N,3,3)
        rotation matrix

    '''

    number_elements = len(delta_x)
    L_ = np.sqrt(delta_x**2 + delta_y**2)
    L  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
    
    cossine_gamma = np.cos(gamma)
    sine_gamma = np.sin(gamma)

    sine_delta = np.zeros(number_elements, dtype=float)
    cossine_delta = np.zeros(number_elements, dtype=float)

    for i in range(number_elements):

        if L_[i] > 0.0001*L[i]:
            sine_delta[i] = delta_y[i]/L_[i]
            cossine_delta[i] = delta_x[i]/L_[i]
        else:
            sine_delta[i] = 0
            cossine_delta[i] = 1

    cossine_epsilon = L_ / L
    sine_epsilon = - delta_z / L
    
    # Matrices product order - Rx@Ry@Rz (@Palazzolo, A. Vibration theory and applications with finite element and active vibration control. pg 677)
    data_rot = np.array([   cossine_delta * cossine_epsilon, 
                            sine_delta * cossine_epsilon, 
                            -sine_epsilon, 
                            cossine_delta * sine_epsilon * sine_gamma - sine_delta * cossine_gamma,
                            sine_delta * sine_epsilon * sine_gamma + cossine_delta * cossine_gamma,
                            cossine_epsilon * sine_gamma,
                            cossine_delta * sine_epsilon * cossine_gamma + sine_delta * sine_gamma,
                            sine_delta * sine_epsilon * cossine_gamma - cossine_delta * sine_gamma,
                            cossine_epsilon * cossine_gamma   ])

    return data_rot.T.reshape(-1,3,3)

def transformation_matrix_3x3_by_angles(gamma, epsilon, delta):
    '''    
    This method returns the rotation matrix of an element based on 
    the angles of rotations gamma, epsilon and delta. 
    
    Parameters
    ----------
    gamma: int, float
        values in radians
    
    epsilon: int, float
        values in radians

    delta: int, float
        values in radians

    Returns
    -------
    out: numpy.ndarray(3,3)
        rotation matrix

    '''

    sine_delta = np.sin(delta)
    cossine_delta = np.cos(delta)

    sine_epsilon = np.sin(epsilon)
    cossine_epsilon = np.cos(epsilon)

    sine_gamma = np.sin(gamma)
    cossine_gamma = np.cos(gamma)

    # Matrices product order - Rx@Ry@Rz (@Palazzolo, A. Vibration theory and applications with finite element and active vibration control. pg 677)
    data_rot = np.array([   cossine_delta * cossine_epsilon, 
                            sine_delta * cossine_epsilon, 
                            -sine_epsilon, 
                            cossine_delta * sine_epsilon * sine_gamma - sine_delta * cossine_gamma,
                            sine_delta * sine_epsilon * sine_gamma + cossine_delta * cossine_gamma,
                            cossine_epsilon * sine_gamma,
                            cossine_delta * sine_epsilon * cossine_gamma + sine_delta * sine_gamma,
                            sine_delta * sine_epsilon * cossine_gamma - cossine_delta * sine_gamma,
                            cossine_epsilon * cossine_gamma   ])

    return data_rot.reshape(3,3)

def transformation_matrix_Nx3x3_by_angles(gamma, epsilon, delta):
    '''    
    This method returns the rotation matrices to a set of N elements 
    based on the angles of rotations gamma, epsilon and delta. 
    
    Parameters
    ----------
    gamma: numpy.ndarray
        values in radians
    
    epsilon: numpy.ndarray
        values in radians

    delta: numpy.ndarray
        values in radians

    Returns
    -------
    out: numpy.ndarray(N,3,3)
        rotation matrix

    '''

    sine_delta = np.sin(delta)
    cossine_delta = np.cos(delta)

    sine_epsilon = np.sin(epsilon)
    cossine_epsilon = np.cos(epsilon)

    sine_gamma = np.sin(gamma)
    cossine_gamma = np.cos(gamma)

    # Matrices product order - Rx@Ry@Rz (@Palazzolo, A. Vibration theory and applications with finite element and active vibration control. pg 677)
    data_rot = np.array([   cossine_delta * cossine_epsilon, 
                            sine_delta * cossine_epsilon, 
                            -sine_epsilon, 
                            cossine_delta * sine_epsilon * sine_gamma - sine_delta * cossine_gamma,
                            sine_delta * sine_epsilon * sine_gamma + cossine_delta * cossine_gamma,
                            cossine_epsilon * sine_gamma,
                            cossine_delta * sine_epsilon * cossine_gamma + sine_delta * sine_gamma,
                            sine_delta * sine_epsilon * cossine_gamma - cossine_delta * sine_gamma,
                            cossine_epsilon * cossine_gamma   ])

    return data_rot.T.reshape(-1,3,3)


# def error( msg, title = " ERROR "):
#     '''
#     PyQt5 error message.

#     Parameters
#     ----------
#     msg: str
#         text to be displayed.

#     title: str
#         window title.
#     '''

#     msg_box = QMessageBox()
#     msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)
#     # msg_box.setWindowModality(Qt.WindowModal)
#     msg_box.setIcon(QMessageBox.Critical)
#     msg_box.setText(msg)
#     msg_box.setWindowTitle(title)
#     msg_box.exec_()


# def info_messages(msg, title = " INFORMATION "):
#     '''
#     PyQt5 info message.

#     Parameters
#     ----------
#     msg: str
#         text to be displayed.

#     title: str
#         window title.
#     '''

#     msg_box = QMessageBox()
#     msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)
#     # msg_box.setWindowModality(Qt.WindowModal)
#     msg_box.setIcon(QMessageBox.Information)
#     msg_box.setText(msg)
#     msg_box.setWindowTitle(title)
#     msg_box.exec_()


def remove_bc_from_file(typed_values, path, keys_to_remove, message, equals_keys=False):
    try:

        if isinstance(typed_values, int):
            typed_values = [typed_values]

        bc_removed = False
        config = configparser.ConfigParser()
        config.read(path)
        sections = config.sections()
        for typed_value in typed_values: 
            _typed_value = str(typed_value)
            if _typed_value in sections:
                keys = config[_typed_value].keys()
                for key_to_remove in keys_to_remove:
                    for key in keys:
                        if key_to_remove in key:
                            if equals_keys:
                                if key_to_remove != key:
                                    continue
                            bc_removed = True
                            config.remove_option(section=_typed_value, option=key)
                            if list(config[_typed_value].keys()) == []:
                                config.remove_section(section=_typed_value)
                                        
            if bc_removed:
                if len(list(config.sections())):    
                    with open(path, 'w') as config_file:
                        config.write(config_file)
                else:
                    os.remove(path)

        if message is not None and bc_removed:
            title = "Removal of selected boundary condition"
            PrintMessageInput([window_title_2, title, message])

    except Exception as log_error:
        title = "Error while removing BC from file"
        PrintMessageInput([window_title_1, title, str(log_error)])


def getColorRGB(color):
    temp = color[1:-1] #Remove "[ ]"
    tokens = temp.split(',')
    return list(map(int, tokens))

def sparse_is_equal(a, b):
    '''
    Function to check if two scipy.sparse matrices are equal. 
    
    Notes
    -----
    Because of implementation reasons, the right way to do this is checking 
    the differences, not the similarities.

    Parameters
    ----------
    a: scipy.sparse
        A sparse matrix.

    b: scipy.sparse
        Another sparse matrix.

    Returns
    -------
    out: True if the matrices are equal, else False.
    
    Raises
    ------
    Type Error
        If matrices are not sparse.
    '''

    if not (issparse(a) and issparse(b)):
        raise TypeError('a and b should be sparse matrices')

    diference = a != b
    if isinstance(diference, bool):
        return not diference

    if issparse(diference):
        return diference.nnz == 0

def get_new_path(path, name):
    path = Path(path)
    return path / name

def get_edited_filename(path):
    new_path = ""
    new_basename = ""
    if os.path.exists(path):
        if os.path.basename(path) != "":
            basename = os.path.basename(path)
            dirname = os.path.dirname(path)
            for ext in [".step", ".stp", ".STEP", ".STP", ".iges", ".igs", ".IGES", ".IGS"]:
                if ext in basename:
                    strings = basename.split(ext)
                    if strings[0][-7:] == "_edited":
                        new_basename = basename
                    else:
                        new_basename = strings[0] + "_edited.stp"
                    new_path = get_new_path(dirname, new_basename)
                    break
    return new_path, new_basename

def get_offset_from_string(offset):
    offset = offset[1:-1].split(',')
    offset_y = offset_z = 0.0
    if len(offset) == 2:
        if offset[0] != '0.0':
            offset_y = float(offset[0])
        if offset[1] != '0.0':
            offset_z = float(offset[1])
    return offset_y, offset_z

def get_list_of_values_from_string(input_string, int_values=True):
    """ 
    This function returns a list of values for a given string of a list.

    Parameters
    ----------
    input_string: string of a list
    int_values: bool

    Returns
    ----------
    list of int values if int_values is True or a list of float numbers if int_values is False
    """
    input_string = input_string[1:-1].split(',')
    list_values = []
    if int_values:
        for value in input_string:
            list_values.append(int(value))
    else:
        for value in input_string:
            list_values.append(float(value))
    return list_values

def get_list_bool_from_string(input_string):
    """
    This function returns a list of boolean variables for a given string of a boolean list.

    Parameters
    ----------
    input_string: string of a list of boolean variables

    Returns
    ----------
    list of boolean variables

    """
    for text in ["[", "]", " "]:
        input_string = input_string.replace(text,"")
    list_of_strings = input_string.strip().split(",")
    list_bool = [True if item=="True" else False for item in list_of_strings]
    return list_bool

def get_linear_distribution_for_variable_section(x_initial, x_final, N):
    """This function returns the linear distributions for variable sections"""
    n = np.arange(N, dtype=float)/N
    n_shift = np.arange(1, N+1, 1, dtype=float)/N
    return (x_final-x_initial)*n + x_initial, (x_final-x_initial)*n_shift + x_initial

def get_linear_distribution(x_initial, x_final, N):
    n = np.arange(N)/(N-1)
    return (x_final-x_initial)*n + x_initial

def get_V_linear_distribution(x, N,  reduction_start=10, reduction_half=50):
    if N == 3:
        reduction_start = 25
    output = np.zeros(N)
    x_i = x*(1-(reduction_start/100))
    x_m = x*(1-(reduction_half/100))
    
    if N == 1:
        return x_m
    
    if np.remainder(N,2) == 0:
        half = int(N/2)
        shift = 0
    else:
        half = int((N+1)/2)
        shift = 1
    
    output[0:half] = get_linear_distribution(x_i, x_m, half) 
    output[half-shift:] = get_linear_distribution(x_m, x_i, half)
    
    return output

def create_new_folder(path, folder_name):
    folder_path = get_new_path(path, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path

def check_is_there_a_group_of_elements_inside_list_elements(input_list):
    ord_list = np.sort(input_list)
    _value = ord_list[0]
    list_i = [_value]
    list_of_lists = []
    for value in ord_list[1:]:
        if value == _value + 1:
            list_i.append(value)
        else:
            temp_list = list_i.copy()
            list_of_lists.append(temp_list)
            list_i = [value]
        _value = value
    list_of_lists.append(list_i)
    return list_of_lists

def get_fillet_parameters(P1, P2, P3, radius, unit_length="m"):
    """
    This method process the fillet parameters, respectiveliy, start point, center point and end point of the arc circle.
    For a given two pair of points P1P2 and P2P3, P2 is the commom point.

    Inputs: np.ndarray(3x3)
    P1, P2, P3: 3d nodal coordinates of each point in which the P2 point is the common one of both lines

    Outputs: np.ndarray(6x3)
    P1, P2, P3, Pc, Q1, Q2
    """

    if unit_length == "m":
        factor = 1
    elif unit_length == "in":
        factor = 1/25.4
    elif unit_length == "mm":
        factor = 1/1000
    
    radius *= factor

    try:

        if isinstance(P1, list):
            P1 = np.array(P1)
        if isinstance(P2, list):
            P2 = np.array(P2)
        if isinstance(P3, list):
            P3 = np.array(P3)
                    
        cache_P2 = P2*factor
        Points = (np.array([P1,P2,P3]) - np.array([P2,P2,P2]))*factor

        u = Points[0,:] - Points[1,:]
        v = Points[2,:] - Points[1,:]
        theta = get_angle_between_vectors(u,v)
        if np.dot(u,v) < 0:
            theta = np.pi - theta 

        alpha = theta/2
        d = radius/np.sin(alpha)

        L_min = np.min([np.linalg.norm(u),np.linalg.norm(v)])
        allowable_radius = L_min*np.tan(alpha)
        if radius >= allowable_radius:
            print(f"The fillet radius must be less than {round(allowable_radius,2)} [mm].")
            return None, True

        if np.linalg.norm(np.cross(u,v)) == 0:
            print("The input points belong to the same line. Please, check the point coordinates to proceed!")
            return None, True

        n_plane = np.cross(u,v)/np.linalg.norm(np.cross(u,v))
        n_z = np.array([0,0,1])

        if np.linalg.norm(np.cross(n_plane,n_z)) == 0:
            r = Rotation.from_rotvec([0,0,0])
        else:
            rot_axis = np.cross(n_plane,n_z)/np.linalg.norm(np.cross(n_plane,n_z))
            rot_axis_norm = rot_axis/np.linalg.norm(rot_axis)
            ang_rot = np.arccos(np.dot(n_plane,n_z)/(np.linalg.norm(n_plane)*np.linalg.norm(n_z)))
            rot_vect = rot_axis_norm*ang_rot
            r = Rotation.from_rotvec(rot_vect)

        rot_matrix = r.as_matrix()

        # This operation rotates the plane containing the lines P1P2 and P2P3 aligning it with the xy plane.
        Points = Points@rot_matrix.T

        u = Points[0,:] - Points[1,:]
        v = Points[2,:] - Points[1,:]

        nx = np.array([1,0,0])
        ang_z = get_angle_between_vectors(u,nx)
                
        if u[0]>=0 and u[1]>=0:
            rot_ang_z_axis = -ang_z
        elif u[0]>=0 and u[1]<=0:
            rot_ang_z_axis = ang_z
        elif u[0]<0 and u[1]<=0:
            rot_ang_z_axis = -ang_z
        elif u[0]<0 and u[1]>=0:
            rot_ang_z_axis = ang_z

        rot_xy_plane = np.array([   [np.cos(rot_ang_z_axis), -np.sin(rot_ang_z_axis), 0],
                                    [np.sin(rot_ang_z_axis), np.cos(rot_ang_z_axis), 0],
                                    [0, 0, 1]   ])
        Points = Points@rot_xy_plane.T
        
        P1 = Points[0,:]
        P2 = Points[1,:]
        P3 = Points[2,:]
        x1,y1,_ = P1
        x2,y2,_ = P2
        x3,y3,_ = P3
        
        if x1>0 and y3>0:
            w = np.array([np.cos(alpha),np.sin(alpha),0])
        elif x1<0 and y3>0:
            w = np.array([-np.cos(alpha),np.sin(alpha),0])
        elif x1<0 and y3<0:
            w = np.array([-np.cos(alpha),-np.sin(alpha),0])
        elif x1>0 and y3<0:
            w = np.array([np.cos(alpha),-np.sin(alpha),0])

        Pc = P2 + w*d
  
        # Define a normal vetor to the line P1P2 
        # equation: (nx_1,ny_1).(x2-x1,y2-y1) = 0
        nx_1 = 1
        ny_1 = 1
        if x2-x1 != 0:
            nx_1 = -ny_1*((y2-y1)/(x2-x1))
        else:
            ny_1 = -nx_1*((x2-x1)/(y2-y1))

        n1 = np.array([nx_1,ny_1,0])/np.linalg.norm(np.array([nx_1,ny_1,0]))
        Q1 = Pc - n1*radius

        if round(np.linalg.norm(np.cross(Q1-P2, P2-P1)),6) != 0:
            Q1 = Pc + n1*radius

        # Define a normal vetor to the line P2P3 
        # equation: (nx_2,ny_2).(x3-x2,y3-y2) = 0
        nx_2 = 1
        ny_2 = 1
        if x3-x2 != 0:
            nx_2 = -ny_2*((y3-y2)/(x3-x2))
        else:
            ny_2 = -nx_2*((x3-x2)/(y3-y2))

        n2 = np.array([nx_2,ny_2,0])/np.linalg.norm(np.array([nx_2,ny_2,0]))
        Q2 = Pc - n2*radius
        if round(np.linalg.norm(np.cross(Q2-P2, P3-P2)),6) != 0:
            Q2 = Pc + n2*radius
       
        Points2 = np.zeros((6,3))
        Points2[0:3,:] = Points
        Points2[3,:] = Pc
        Points2[4,:] = Q1
        Points2[5,:] = Q2
        Points2 = Points2@rot_xy_plane
        
        # Points_f = Points2 + np.ones((6,3))*np.array(cache_P2)*0
        Points_f = Points2@rot_matrix + np.ones((6,3))*np.array(cache_P2)
        P1 = Points_f[0,:]
        P2 = Points_f[1,:]
        P3 = Points_f[2,:]
        Pc = np.round(Points_f[3,:],8)
        Q1 = np.round(Points_f[4,:],8)
        Q2 = np.round(Points_f[5,:],8)
        # print(f"output data:\n\n P1: {P1}\n P2: {P2}\n P3: {P3}\n Pc: {Pc}\n Q1: {Q1}\n Q2: {Q2}")

       # Checks if P1Q1P2 and P2Q2P3 are colinear 
        cross_P1Q1_P1P2 = round(np.linalg.norm(np.cross(Q1-P2, P2-P1)),6)
        cross_P2Q2_P2P3 =  round(np.linalg.norm(np.cross(Q2-P2, P3-P2)),6)
        if [cross_P1Q1_P1P2,cross_P2Q2_P2P3] != [0,0]:
            print(f"The P1-Q1-P2 and P2Q2-P3 are colinear: {cross_P1Q1_P1P2, cross_P2Q2_P2P3}")
            return None, True

    except Exception as error:
        print(str(error))
        return None, True

    return [P1, P2, P3, Pc, Q1, Q2], False

def get_angle_between_vectors(vect_1, vect_2):
    return np.arccos(np.linalg.norm(np.dot(vect_1,vect_2))/(np.linalg.norm(vect_1)*np.linalg.norm(vect_2)))