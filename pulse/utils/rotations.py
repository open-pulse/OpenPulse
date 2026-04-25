import numpy as np
from scipy.spatial.transform import Rotation
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter


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


def transformation_matrix_3x3_by_angles(gamma: float | np.ndarray, epsilon: float | np.ndarray, delta: float | np.ndarray):
    '''    
    This method returns the rotation matrix of an element based on 
    the angles of rotations gamma, epsilon and delta. 
    
    Parameters
    ----------
    gamma: float | np.ndarray
        Angle value(s) in radians
    
    epsilon: float | np.ndarray
        Angle value(s) in radians

    delta: float | np.ndarray
        Angle value(s) in radians

    Returns
    -------
    data_rot: numpy.ndarray
        The rotation matrix having dimension 3x3 if if the arguments are float numbers
        or Nx3x3 if they are np.ndarrays (N=len(gamma)=len(epsilon)=len(delta))

    '''

    sine_delta = np.sin(delta)
    cossine_delta = np.cos(delta)

    sine_epsilon = np.sin(epsilon)
    cossine_epsilon = np.cos(epsilon)

    sine_gamma = np.sin(gamma)
    cossine_gamma = np.cos(gamma)

    # Matrices product order - Rx@Ry@Rz 
    # Reference: Palazzolo, A. Vibration theory and applications with finite element and active vibration control. pg 677
    data_rot = np.array([   
        cossine_delta * cossine_epsilon,
        sine_delta * cossine_epsilon,
        -sine_epsilon,
        cossine_delta * sine_epsilon * sine_gamma - sine_delta * cossine_gamma,
        sine_delta * sine_epsilon * sine_gamma + cossine_delta * cossine_gamma,
        cossine_epsilon * sine_gamma,
        cossine_delta * sine_epsilon * cossine_gamma + sine_delta * sine_gamma,
        sine_delta * sine_epsilon * cossine_gamma - cossine_delta * sine_gamma,
        cossine_epsilon * cossine_gamma,
        ], dtype=float)

    if isinstance(gamma, np.ndarray):
        return data_rot.T.reshape(-1, 3, 3)
    else:
        return data_rot.reshape(3, 3)


def align_vtk_geometry(geometry: vtkPolyData, start: np.ndarray, vector: np.ndarray, angle: float = 0):
    x, y, z = start

    # compute the transformation matrix
    transformation_matrices = transformation_matrix_3x3( 
        vector[0],
        vector[1],
        vector[2],
        gamma = angle,
    )

    # compute the rotation matrix
    rot_matrix = Rotation.from_matrix(transformation_matrices)

    # compute the rotation angles rz, rx and ry in degrees
    rz, rx, ry = -rot_matrix.as_euler('zxy', degrees=True)

    transform = vtkTransform()
    transform.Translate(x, y, z)
    transform.RotateZ(rz)
    transform.RotateX(rx)
    transform.RotateY(ry)
    transform.Update()

    transform_filter = vtkTransformFilter()
    transform_filter.SetInputData(geometry)
    transform_filter.SetTransform(transform)
    transform_filter.Update()

    return transform_filter.GetOutput()


def rotation_matrices(theta_x: float, theta_y: float, theta_z: float):
    """
    This function computes the 3D rotation matrices from the rotation angles 
    theta_x, theta_y and theta_z.

    Parameters
    ----------
    theta_x: float
        The rotation angle about the x-axis in radians.

    theta_y: float
        The rotation angle about the y-axis in radians.

    theta_z: float
        The rotation angle about the z-axis in radians.

    Returns
    -------
    rot_x: np.ndarray
        The rotation matrix 3x3 about the x-axis.

    rot_y: np.ndarray
        The rotation matrix 3x3 about the y-axis.

    rot_z: np.ndarray
        The rotation matrix 3x3 about the z-axis.
    """

    sin = np.sin([theta_x, theta_y, theta_z])
    cos = np.cos([theta_x, theta_y, theta_z])

    # rotation matrix about x-axis
    rot_x = np.array([
        [1, 0, 0],
        [0, cos[0], -sin[0]],
        [0, sin[0], cos[0]],
        ]
    )

    # rotation about y-axis
    rot_y = np.array(
        [
        [cos[1], 0, sin[1]],
        [0, 1, 0],
        [-sin[1], 0, cos[1]],
        ]
    )

    # rotation about x-axis
    rot_z = np.array(
        [
        [cos[2], -sin[2], 0],
        [sin[2], cos[2], 0],
        [0, 0, 1],
        ]
    )

    return rot_x, rot_y, rot_z