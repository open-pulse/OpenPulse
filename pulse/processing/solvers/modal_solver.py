import numpy as np
from scipy.sparse import csr_matrix, bmat, eye
from scipy.sparse.linalg import eigs, inv

from pulse.processing.assemblers.base import Assembler


class ModalSolver:
    """
    Generic modal solver.

    Solves the eigenvalue problem  K·φ = λ·M·φ  using any assembler
    that implements the Assembler interface.

    When the assembler returns a damping matrix C ≠ None
    (nonproportional damping, e.g. acoustic), uses the state-space
    formulation to obtain complex eigenvalues.
    """

    def solve(
        self,
        assembler: Assembler,
        n_modes: int = 40,
        which: str = "LM",
        sigma: float = 1e-4,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Solve the modal analysis.

        Parameters
        ----------
        assembler : Assembler
            Assembler providing K, M (and optionally C).
        n_modes : int
            Number of modes to compute.
        which : str
            Eigenvalue selection criterion for scipy.sparse.linalg.eigs.
        sigma : float
            Shift-invert point in (rad/s)² or rad/s.

        Returns
        -------
        natural_frequencies : np.ndarray
            Natural frequencies in Hz, sorted in ascending order.
        modal_shapes : np.ndarray
            Corresponding mode shapes (columns), with prescribed DOFs
            reinserted (zero value).
        """

        K = assembler.get_stiffness_matrix()
        M = assembler.get_mass_matrix()
        C = assembler.get_damping_matrix()

        if C is not None and np.sum(C) != 0:
            natural_frequencies, modal_shapes = self._solve_state_space(
                K, M, C, n_modes, which, sigma
            )
        else:
            natural_frequencies, modal_shapes = self._solve_undamped(
                K, M, n_modes, which, sigma
            )

        modal_shapes = assembler.reinsert_prescribed_dofs(modal_shapes, modal=True)
        return natural_frequencies, modal_shapes

    # ── Internal solvers ──────────────────────────────────────────────────

    def _solve_undamped(
        self,
        K,
        M,
        n_modes: int,
        which: str,
        sigma: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Undamped eigenvalue problem: K·φ = λ·M·φ."""

        eigen_values, eigen_vectors = eigs(K, M=M, k=n_modes, which=which, sigma=sigma)

        Wn_2 = np.absolute(np.real(eigen_values))
        natural_frequencies = np.sqrt(Wn_2) / (2 * np.pi)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shapes = eigen_vectors[:, index_order]

        return natural_frequencies, modal_shapes

    def _solve_state_space(
        self,
        K,
        M,
        C,
        n_modes: int,
        which: str,
        sigma: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        State-space formulation for systems with general damping.

        Builds:
            AA = [[0,      I   ],
                  [-M⁻¹K, -M⁻¹C]]

        and solves the eigenvalue problem AA·z = λ·z.
        Selects only eigenvalues with positive imaginary part.
        """

        N_t = K.shape[0]
        ones = eye(N_t, dtype=complex, format="csr")
        zeros = csr_matrix((N_t, N_t), dtype=complex)

        inv_M = inv(M.tocsc()).tocsr()

        AA = bmat(
            [
                [zeros, ones],
                [-inv_M @ K, -inv_M @ C],
            ]
        )

        eigen_values, eigen_vectors = eigs(AA, k=n_modes, which=which, sigma=sigma)

        N_dofs = eigen_vectors.shape[0] // 2

        # Keep only eigenvalues with positive imaginary part (conjugate pairs)
        mask = np.imag(eigen_values) > 0
        eigen_values = eigen_values[mask]
        eigen_vectors = eigen_vectors[:, mask]

        Wn = np.abs(eigen_values)
        natural_frequencies = Wn / (2 * np.pi)
        damping_ratio = -np.real(eigen_values) / Wn

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shapes = eigen_vectors[:N_dofs, index_order]

        # Filter out overdamped modes
        mask_dmp = np.round(np.abs(damping_ratio[index_order]), 6) < 1
        natural_frequencies = natural_frequencies[mask_dmp]
        modal_shapes = modal_shapes[:, mask_dmp]

        return natural_frequencies, modal_shapes
