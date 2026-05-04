import numpy as np
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter


def rotation_matrix_3x3_by_deltas(delta_x: np.ndarray, delta_y: np.ndarray, delta_z: np.ndarray, gamma: float=0):
    '''    
    This method returns the rotation matrix of an element (or structure) based on 
    the delta x, y and z lengths from the start node, beyond the x-axis rotation 
    angle (twist angle). This rotation matrix transforms the global coordinate system 
    into the local coordinate system.

    Parameters
    ----------
    delta_x: float | np.ndarray
        Angle value(s) in radians

    delta_y: float | np.ndarray
        Angle value(s) in radians

    delta_z: float | np.ndarray
        Angle value(s) in radians

    gamma: float
        X-axis rotation angle.

    Returns
    -------
    data_rot: numpy.ndarray
        The rotation matrix having dimension 3x3 if if the arguments are float numbers
        or Nx3x3 if they are np.ndarrays (N=len(delta_x)=len(delta_y)=len(delta_z))

    '''

    L_ = np.sqrt(delta_x**2 + delta_y**2)
    L  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    cossine_gamma = np.cos(gamma)
    sine_gamma = np.sin(gamma)

    mask = L_ > 0.0001 * L

    if isinstance(L, np.ndarray):
        number_elements = len(delta_x)
        indexes = np.arange(number_elements, dtype=int)
        sine_delta = np.zeros(number_elements, dtype=float)
        cossine_delta = np.ones(number_elements, dtype=float)

        mask_ind = indexes[mask]
        sine_delta[mask_ind] = delta_y[mask_ind] / L_[mask_ind]
        cossine_delta[mask_ind] = delta_x[mask_ind] / L_[mask_ind]

    else:

        if mask:
            sine_delta = delta_y / L_
            cossine_delta = delta_x / L_

        else:
            sine_delta = 0
            cossine_delta = 1

    # for i in range(number_elements):

    #     if L_[i] > 0.0001*L[i]:
    #         sine_delta[i] = delta_y[i]/L_[i]
    #         cossine_delta[i] = delta_x[i]/L_[i]

    #     else:
    #         sine_delta[i] = 0
    #         cossine_delta[i] = 1

    cossine_epsilon = L_ / L
    sine_epsilon = - delta_z / L

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

    if isinstance(delta_x, np.ndarray):
        return data_rot.T.reshape(-1, 3, 3)
    else:
        return data_rot.reshape(3, 3)


def rotation_matrix_3x3_by_angles(gamma: float | np.ndarray, epsilon: float | np.ndarray, delta: float | np.ndarray):
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


def align_vtk_geometry(geometry: vtkPolyData, start_coords: np.ndarray, vector: np.ndarray, angle: float = 0):

    # compute the rotation matrix
    rotation_matrix = rotation_matrix_3x3_by_deltas( 
        vector[0],
        vector[1],
        vector[2],
        gamma = angle,
    )


    """
    The transformation matrix M combines the rotation and translation.
    
    #    M = | R_00 R_01 R_02 T_x |
    #        | R_10 R_11 R_12 T_y |
    #        | R_20 R_21 R_22 T_z |
    #        |  0    0    0    1  |


    """

    # define the transformation matrix M
    transformation_matrix = np.eye(4, dtype=float)
    transformation_matrix[:3, :3] = rotation_matrix.T
    transformation_matrix[:3, -1] = start_coords

    transform = vtkTransform()
    transform.SetMatrix(transformation_matrix.flatten())
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
        ], dtype=float
    )

    # rotation about y-axis
    rot_y = np.array(
        [
        [cos[1], 0, sin[1]],
        [0, 1, 0],
        [-sin[1], 0, cos[1]],
        ], dtype=float
    )

    # rotation about x-axis
    rot_z = np.array(
        [
        [cos[2], -sin[2], 0],
        [sin[2], cos[2], 0],
        [0, 0, 1],
        ], dtype=float
    )

    return rot_x, rot_y, rot_z

## TODO: to be removed
# def rotation_matrix_3x3_by_deltas(delta_x, delta_y, delta_z, gamma=0):
#     '''    
#     This method returns the rotation matrix of an element 
#     based on its spatial position. 
    
#     Parameters
#     ----------
#     delta_x: int, float
#         value in meters
    
#     delta_y: int, float
#         value in meters

#     delta_z: int, float
#         value in meters

#     Returns
#     -------
#     out: numpy.ndarray(3,3)
#         rotation matrix

#     '''

#     L_ = np.sqrt(delta_x**2 + delta_y**2)
#     L  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

#     cossine_epsilon = L_ / L
#     sine_epsilon = - delta_z / L

#     if L_ > 0.0001*L:
#         sine_delta = delta_y/L_
#         cossine_delta = delta_x/L_

#     else:
#         sine_delta = 0
#         cossine_delta = 1

#     cossine_gamma = np.cos(gamma)
#     sine_gamma = np.sin(gamma)

#     # Matrices product order - Rx@Ry@Rz 
#     # Reference: Palazzolo, A. Vibration theory and applications with finite element and active vibration control. pg 677
#     rotation_matrix = np.array([
#         cossine_delta * cossine_epsilon, 
#         sine_delta * cossine_epsilon, 
#         -sine_epsilon, 
#         cossine_delta * sine_epsilon * sine_gamma - sine_delta * cossine_gamma,
#         sine_delta * sine_epsilon * sine_gamma + cossine_delta * cossine_gamma,
#         cossine_epsilon * sine_gamma,
#         cossine_delta * sine_epsilon * cossine_gamma + sine_delta * sine_gamma,
#         sine_delta * sine_epsilon * cossine_gamma - cossine_delta * sine_gamma,
#         cossine_epsilon * cossine_gamma,
#         ], dtype=float) 

#     return rotation_matrix.reshape(3, 3)
