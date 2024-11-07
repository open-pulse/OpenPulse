# isort: skip_file

# Abstract classes
from .linear_structure import LinearStructure
from .fillet import Fillet
from .structure import Structure
from .arc import Arc

# Normal Clases
from .beam import *
from .bend import Bend
from .arc_bend import ArcBend
from .elbow import Elbow
from .expansion_joint import ExpansionJoint
from .flange import Flange
from .pipe import Pipe
from .point import Point
from .reducer import Reducer
from .valve import Valve
from .support import Support

# Dont forget to update this list when a new concrete class is created
ALL_STRUCTURE_TYPES = [
    Pipe,
    Flange,
    Reducer,

    Bend,
    Elbow,
    ArcBend,

    Valve,
    ExpansionJoint,
    
    CircularBeam,
    RectangularBeam,
    TBeam,
    CBeam,
    IBeam,
]