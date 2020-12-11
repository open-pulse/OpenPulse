from functools import wraps
from time import time
from scipy.sparse import issparse
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import configparser
import numpy as np
from scipy.spatial.transform import Rotation


def split_sequence(sequence, size):
    subsequences = []
    for start in range(0, len(sequence), size):
        end = start + size
        subsequence = sequence[start:end]
        subsequences.append(subsequence)
    return subsequences

def slicer(iterable, argument):
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
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time()
        values = function(*args, **kwargs)
        end_time = time()
        print(f'Time to finish {function.__name__}: {end_time - start_time} [s]')
        return values
    return wrapper
    
def m_to_mm(m):
    return float(m) * 1000

def mm_to_m(mm):
    return float(mm) / 1000

def inverse_matrix_3x3xN(A):
    
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

    invA = (b*np.array([[b11,b12,b13],[b21,b22,b23],[b31,b32,b33]])).T
    # invA = (b*np.array([[b11,b21,b31],[b12,b22,b32],[b13,b23,b33]])).T
    
    return invA

def inverse_matrix_3x3(A):
    
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

def _rotation_matrix_3x3(delta_x, delta_y, delta_z, gamma=0):
    """ Make the rotation from the element coordinate system to the global doordinate system."""
    # Rotation Matrix

    L_ = np.sqrt(delta_x**2 + delta_y**2)
    L  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    cos_gamma = np.cos(gamma)
    sin_gamma = np.sin(gamma)

    if L_ > 0.0001*L:
        sine = delta_y/L_
        cossine = delta_x/L_
    else:
        sine = 0
        cossine = 1
        
    # perform a double check and remove these lines if it is not necessary
    # C = np.zeros((3,3), dtype=float)
    # if L_ != 0.:
    #     C[0,:] = [  cossine * L_ / L, sine * L_ / L, delta_z / L  ]

    #     C[1,:] = [  -cossine * delta_z * sin_gamma / L - sine * cos_gamma,
    #                 -sine * delta_z * sin_gamma / L + cossine * cos_gamma,
    #                 L_ * sin_gamma / L  ] 

    #     C[2,:] = [  -cossine * delta_z * cos_gamma / L + sine * sin_gamma,
    #                 -sine * delta_z * cos_gamma / L - cossine * sin_gamma,
    #                 L_ * cos_gamma / L  ] 
    # else:
    #     # C[0,0], C[0,1], C[1,2], C[2,2] = 0., 0., 0., 0. 
    #     C[0,2] = delta_z/np.abs(delta_z)
    #     #
    #     C[1,0] = -(delta_z/np.abs(delta_z))*sin_gamma
    #     C[1,1] = cos_gamma
    #     #
    #     C[2,0] = -(delta_z/np.abs(delta_z))*cos_gamma
    #     C[2,1] = -sin_gamma

    a = [   cossine * L_, sine * L_, delta_z   ]

    b = [   -cossine * delta_z * sin_gamma - sine * cos_gamma * L,
            -sine * delta_z * sin_gamma + cossine * cos_gamma * L,
            L_ * sin_gamma   ] 

    c = [   -cossine * delta_z * cos_gamma + sine * sin_gamma * L,
            -sine * delta_z * cos_gamma - cossine * sin_gamma * L,
            L_ * cos_gamma   ] 

    return np.array([a,b,c])/L


def _rotation_matrix_3x3xN(delta_x, delta_y, delta_z, gamma=0):
    """ Make the rotation from the element coordinate system to the global doordinate system."""
    # Rotation Matrix

    number_elements = len(delta_x)
    L_ = np.sqrt(delta_x**2 + delta_y**2)
    L  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
    
    cos_gamma = np.cos(gamma)
    sin_gamma = np.sin(gamma)

    data_rot = np.zeros((number_elements,3,3), dtype=float)
    sine = np.zeros(number_elements, dtype=float)
    cossine = np.zeros(number_elements, dtype=float)

    for i in range(number_elements):

        if L_[i] > 0.0001*L[i]:
            sine[i] = delta_y[i]/L_[i]
            cossine[i] = delta_x[i]/L_[i]
        else:
            sine[i] = 0
            cossine[i] = 1

    data_rot = np.array([   cossine * L_ / L, 
                            sine * L_ / L, 
                            delta_z / L, 
                            -cossine * delta_z * sin_gamma / L - sine * cos_gamma,
                            -sine * delta_z * sin_gamma / L + cossine * cos_gamma,
                            L_ * sin_gamma / L,
                            -cossine * delta_z * cos_gamma / L + sine * sin_gamma,
                            -sine * delta_z * cos_gamma / L - cossine * sin_gamma,
                            L_ * cos_gamma / L   ])

    return data_rot.T.reshape(-1,3,3)

def directional_vectors_xyz_rotation(directional_vectors):
    # we can perform much better doing it by hand
    
    # it's still a little bit weird
    # for some reason the rotations are made in the z,x,y order
    # so, to get the euler we need to do it backwards
    
    u,v,w = directional_vectors
    matrix = np.concatenate((v,w,u)).reshape(3,3)
    r = Rotation.from_matrix(matrix)
    y,x,z = r.as_euler('yxz', degrees=True)
    return x,y,z

def error( msg, title = " ERROR "):
    msg_box = QMessageBox()
    msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)
    # msg_box.setWindowModality(Qt.WindowModal)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def info_messages(msg, title = " INFORMATION "):
    msg_box = QMessageBox()
    msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)
    # msg_box.setWindowModality(Qt.WindowModal)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def remove_bc_from_file(entries_typed, path, key_strings, message):

    try:
        bc_removed = False
        config = configparser.ConfigParser()
        config.read(path)

        for entry in entries_typed: 
            entry_id = str(entry)

            if entry_id in config.sections():
                keys = list(config[entry_id].keys())
                for str_key in key_strings:
                    if str_key in keys:
                        # print("delete {} at entry {}".format(str_key, entry_id))
                        config.remove_option(section=entry_id, option=str_key)
                        if list(config[entry_id].keys())==[]:
                            config.remove_section(entry_id)
                        bc_removed = True

        with open(path, 'w') as config_file:
            config.write(config_file)

        if message is not None and bc_removed:
            info_messages(message)

    except Exception as e:
        error(str(e))

def isInteger(value):
    try:
        int(value)
        return True
    except:
        return False

def isFloat(value):
    try:
        float(value)
        return True
    except:
        return False

def getColorRGB(color):
    temp = color[1:-1] #Remove "[ ]"
    tokens = temp.split(',')
    return list(map(int, tokens))

def sparse_is_equal(a, b):
    if not (issparse(a) and issparse(b)):
        raise TypeError('a and b should be sparse matrices')

    diference = a != b
    if isinstance(diference, bool):
        return not diference

    if issparse(diference):
        return diference.nnz == 0