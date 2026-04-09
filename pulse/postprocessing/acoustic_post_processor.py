import numpy as np


class AcousticPostProcessor:
    """
    Post-processor for acoustic results.

    Stores acoustic solution metadata (perforated plate convergence,
    unstable frequencies) and provides access to the solution by node/DOF.

    Parameters
    ----------
    source : solver instance or Project
        Either a HarmonicSolver / ModalSolver instance whose ``assembler``
        and ``solution`` attributes hold the relevant data, or a Project
        instance from which ``acoustic_solver`` is retrieved live.
    """

    def __init__(self, source):
        self._source = source

    # ── Solver / delegation properties ───────────────────────────────────

    @property
    def solver(self):
        """Return the solver, deriving it from a Project if that was passed."""
        src = self._source
        if hasattr(src, "acoustic_solver"):
            return src.acoustic_solver
        return src

    @property
    def model(self):
        return self.solver.assembler.model

    @property
    def assembler(self):
        return self.solver.assembler

    @property
    def solution(self):
        return self.solver.solution

    @property
    def frequencies(self):
        return self.solver.frequencies

    # ── Perforated plate convergence data ────────────────────────────────

    @property
    def convergence_data_log(self) -> list | None:
        """
        Convergence log from the nonlinear iteration (perforated plate).
        Format: [iterations, pressure_residues, delta_residues, target_pct].
        None if no nonlinear analysis was run or if it did not converge with log.
        """
        return self.assembler.convergence_data_log

    @property
    def has_nl_elements(self) -> bool:
        """True if the model has nonlinear perforated plate elements."""
        return bool(self.assembler.nl_elements)

    # ── Solution access ───────────────────────────────────────────────────

    def get_pressure_at_node(self, node_id: int) -> np.ndarray:
        """
        Returns the acoustic pressure vector (n_freqs,) at node `node_id`.
        """
        node = self.model.preprocessor.nodes[node_id]
        idx = node.global_index
        return self.solution[idx, :]

    def get_pressure_field(self) -> np.ndarray:
        """
        Returns the full solution (n_dofs, n_freqs).
        """
        return self.solution
