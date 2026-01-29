from enum import IntEnum


class AnalysisID(IntEnum):
    NO_ANALYSIS = -1
    STRUCTURAL_MODAL = 0
    STRUCTURAL_HARMONIC = 1
    ACOUSTIC_MODAL = 2
    ACOUSTIC_HARMONIC = 3
    COUPLED_HARMONIC = 4
    STRUCTURAL_STATIC = 5


class RadiationImpedanceType(IntEnum):
    ANECHOIC = 0
    FLANGED = 1
    UNFLANGED = 2