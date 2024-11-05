import numpy as np


def lerp(a, b, t):
    return a + (b - a) * t


def normalize(vec):
    return vec / np.linalg.norm(vec)