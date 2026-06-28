from pulse.model.elements.acoustic.acoustic_element import AcousticElement
from pulse.model.elements.acoustic.fem_acoustic_element import FEMAcousticElement
from pulse.model.elements.acoustic.fetm_acoustic_element import FETMAcousticElement
from pulse.model.elements.beam_structural_element import BeamStructuralElement
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.model.elements.expansion_joint_structural_element import ExpansionJointStructuralElement
from pulse.model.elements.pipe_structural_element import PipeStructuralElement
from pulse.model.elements.rigid_structural_element import RigidStructuralElement
from pulse.model.elements.structural_element import StructuralElement
from pulse.model.elements.valve_structural_element import ValveStructuralElement


def build_structural_element(element_attributes: ElementAttributes) -> StructuralElement:

    element_type = element_attributes.structural_element_type

    if element_type == "pipe_1":
        return PipeStructuralElement(element_attributes)

    if element_type == "beam_1":
        return BeamStructuralElement(element_attributes)

    if element_type == "rigid_element":
        return RigidStructuralElement(element_attributes)

    if element_type == "expansion_joint":
        return ExpansionJointStructuralElement(element_attributes)

    if element_type == "valve":
        return ValveStructuralElement(element_attributes)


def build_acoustic_element(element_attributes: ElementAttributes) -> AcousticElement:

    element_type = element_attributes.acoustic_element_formulation

    if element_type == "FETM":
        return FETMAcousticElement(element_attributes)

    if element_type == "FEM":
        return FEMAcousticElement(element_attributes)
