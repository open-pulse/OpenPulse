from .pipe_options import PipeOptions


class UncorrectedBranchOptions(PipeOptions):
    """
    Pipe branch attached directly to the junction point, without the
    CouplingElement correction that is applied at T-junctions.
    """

    correct_t_junction = False
