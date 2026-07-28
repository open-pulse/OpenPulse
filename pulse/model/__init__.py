from enum import IntEnum


class AnalysisID(IntEnum):
    NO_ANALYSIS = -1
    STRUCTURAL_MODAL = 0
    STRUCTURAL_HARMONIC = 1
    ACOUSTIC_MODAL = 2
    ACOUSTIC_HARMONIC = 3
    COUPLED_HARMONIC = 4
    STRUCTURAL_STATIC = 5

    def is_harmonic(self):
        return self in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.COUPLED_HARMONIC,
        ]

    def is_modal(self):
        return self in [
            AnalysisID.STRUCTURAL_MODAL,
            AnalysisID.ACOUSTIC_MODAL,
        ]

    def is_static(self):
        return self == AnalysisID.STRUCTURAL_STATIC

    def is_structural(self):
        return self in [
            AnalysisID.STRUCTURAL_MODAL,
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.STRUCTURAL_STATIC,
        ]

    def is_acoustic(self):
        return self in [
            AnalysisID.ACOUSTIC_MODAL,
            AnalysisID.ACOUSTIC_HARMONIC,
        ]

    def is_coupled(self):
        return self == AnalysisID.COUPLED_HARMONIC
    
    def is_harmonic_structural(self):
        return self in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.COUPLED_HARMONIC,
        ]