
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.model.elements.structural_element import StructuralElement
from pulse.model.elements.pipe_structural_element import PipeStructuralElement
from pulse.model.elements.beam_structural_element import BeamStructuralElement
from pulse.model.elements.rigid_structural_element import RigidStructuralElement
from pulse.model.elements.expansion_joint_structural_element import ExpansionJointStructuralElement
from pulse.model.elements.valve_structural_element import ValveStructuralElement


class StructuralElementBuilder:
    def __init__(self, element_attributes: ElementAttributes):
        self.element_attributes = element_attributes
    
    def build_structural_element(self) -> StructuralElement:
        element_type = self.element_attributes.structural_element_type
        match element_type:
            case "pipe_1":
                return PipeStructuralElement(self.element_attributes)
            case "beam_1":
                return BeamStructuralElement(self.element_attributes)
            case "rigid_element":
                return RigidStructuralElement(self.element_attributes)
            case "expansion_joint":
                return ExpansionJointStructuralElement(self.element_attributes)
            case "valve":
                return ValveStructuralElement(self.element_attributes)


class AcousticElementBuilder:
    def __init__(self, element_attributes: ElementAttributes):
        self.element_attributes = element_attributes

    def build_element(self) -> StructuralElement:
        element_type = self.element_attributes.acoustic_element_type
        match element_type:
            case "pipe_1":
                return PipeStructuralElement(self.element_attributes)
            case "beam_1":
                return BeamStructuralElement(self.element_attributes)
            case "rigid_element":
                return RigidStructuralElement(self.element_attributes)
            case "expansion_joint":
                return ExpansionJointStructuralElement(self.element_attributes)
            case "valve":
                return ValveStructuralElement(self.element_attributes)