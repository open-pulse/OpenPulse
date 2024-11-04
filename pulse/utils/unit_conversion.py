import numpy as np


def m_to_mm(value):
    """
    Converts meters to millimeters.

    Parameters
    ----------
    m: int, float
        Value in meters

    Returns
    -------
    out: float
        Value in millimeters
    """
    if isinstance(value, list):
        return np.array(value) * 1e3
    elif isinstance(value, np.ndarray):
        return value * 1e3
    return float(value) * 1e3


def in_to_mm(value):
    """
    Converts inches to millimeters.

    Parameters
    ----------
    m: int, float
        Value in meters

    Returns
    -------
    out: float
        Value in millimeters
    """
    if isinstance(value, list):
        return np.array(value) * 25.4
    elif isinstance(value, np.ndarray):
        return value * 25.4
    return float(value) * 25.4


def in_to_m(value):
    """
    Converts inches to meters.

    Parameters
    ----------
    value: int, float, list, np.ndarray
        Value in inches

    Returns
    -------
    out: float or np.ndarray
        Value in meters
    """
    if isinstance(value, list):
        return np.array(value) * 0.0254
    elif isinstance(value, np.ndarray):
        return value * 0.0254
    return float(value) * 0.0254


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

def mm_to_m(value):
    """
    Converts millimeters to meters.

    Parameters
    ----------
    mm: int, float
        Value in millimeters

    Returns
    -------
    out: float
        Value in meters

    """
    if isinstance(value, list):
        return np.array(value) * 1e-3
    elif isinstance(value, np.ndarray):
        return value * 1e-3
    return float(value) * 1e-3


def mm_to_in(value):
    """
    Converts inches to millimeters.

    Parameters
    ----------
    m: int, float
        Value in meters

    Returns
    -------
    out: float
        Value in millimeters
    """
    if isinstance(value, list):
        return np.array(value) / 25.4
    elif isinstance(value, np.ndarray):
        return value / 25.4
    return float(value) / 25.4

