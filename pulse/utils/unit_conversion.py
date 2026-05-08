import numpy as np


def m_to_mm(value: float|int):
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


def in_to_mm(value: float|int):
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


def in_to_m(value: float|int):
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


def um_to_m(value: float|int):
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

def mm_to_m(value: float|int):
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

def mm_to_in(value: float|int):
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

def lbft_to_kgm(value: float|int):
    """
    Converts the linear mass from pounds per foot to kilograms per meter.

    Parameters
    ----------
    value: int, float
        Input value in pounds per foot.

    Returns
    -------
    out: float
        Converted value in kilograms per meter.
    """
    return (0.45359237 / 0.3048) * value