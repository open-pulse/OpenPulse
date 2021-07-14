from data.user_input.project.printMessageInput import PrintMessageInput
from functools import wraps
from time import time
from scipy.sparse import issparse
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import configparser
import numpy as np
from scipy.spatial.transform import Rotation



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
    
def m_to_mm(m):
    ''' 
    Converts meter to millimeter.

    Parameters
    ----------
    m: int, float
        Value in meters

    Returns
    -------
    out: float
        Value in millimeters
    '''
    return float(m) * 1000

def mm_to_m(mm):
    ''' 
    Converts meter to millimeter.

    Parameters
    ----------
    mm: int, float
        Value in millimeters

    Returns
    -------
    out: float
        Value in meters

    '''
    return float(mm) / 1000

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

def _transformation_matrix_3x3(delta_x, delta_y, delta_z, gamma=0):
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


def _transformation_matrix_3x3xN(delta_x, delta_y, delta_z, gamma=0):
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

def _transformation_matrix_3x3_by_angles(gamma, epsilon, delta):
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

def _transformation_matrix_Nx3x3_by_angles(gamma, epsilon, delta):
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


def error( msg, title = " ERROR "):
    '''
    PyQt5 error message.

    Parameters
    ----------
    msg: str
        text to be displayed.

    title: str
        window title.
    '''

    msg_box = QMessageBox()
    msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)
    # msg_box.setWindowModality(Qt.WindowModal)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def info_messages(msg, title = " INFORMATION "):
    '''
    PyQt5 info message.

    Parameters
    ----------
    msg: str
        text to be displayed.

    title: str
        window title.
    '''

    msg_box = QMessageBox()
    msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)
    # msg_box.setWindowModality(Qt.WindowModal)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def remove_bc_from_file(entries_typed, path, keys_to_remove, message):
    try:

        bc_removed = False
        config = configparser.ConfigParser()
        config.read(path)

        for entry in entries_typed: 
            entry_id = str(entry)

            if entry_id in config.sections():
                keys = list(config[entry_id].keys())

                for key_to_remove in keys_to_remove:
                    if key_to_remove in keys:
                        bc_removed = True
                        config.remove_option(section=entry_id, option=key_to_remove)
                        if list(config[entry_id].keys())==[]:
                            config.remove_section(section=entry_id)
           
            if bc_removed:
                with open(path, 'w') as config_file:
                    config.write(config_file)

        if message is not None and bc_removed:
            PrintMessageInput(["Error while removing BC from file" ,message, "ERROR"])

    except Exception as log_error:
        PrintMessageInput(["Error while removing BC from file" ,str(log_error), "ERROR"])


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
        A sparce matrix.

    b: scipy.sparse
        Another sparce matrix.

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
    if "\\" in path:
        new_path = '{}\\{}'.format(path, name)
    elif "/" in path:
        new_path = '{}/{}'.format(path, name)
    return new_path

def get_linear_distribution(x_initial, x_final, N):
    n = np.arange(N)/(N-1)
    return (x_final-x_initial)*n + x_initial