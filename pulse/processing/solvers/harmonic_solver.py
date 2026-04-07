from __future__ import annotations

import logging

import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import spsolve

from pulse.processing.assemblers.base import Assembler


def _relative_error(v1: np.ndarray, v2: np.ndarray) -> float:
    return norm(v2 - v1) / norm(v1)


def _build_convergence_plot(convergence_target: float):
    """
    Creates and returns an XYPlot for nonlinear PP convergence monitoring.
    Returns None when the UI is not available (headless / unit-test runs).
    """
    try:
        from pulse.interface.user_input.plots.general.xy_plot import XYPlot

        legends = [
            f"Target: {convergence_target * 100}%",
            "Pressure residues",
            "Delta pressure residues",
        ]
        config = {
            "number_of_plots": 3,
            "x_label": "Iterations [n]",
            "y_label": "Relative error [%]",
            "colors": [(0, 0, 0), (0, 0, 1), (1, 0, 0)],
            "line_styles": ["--", "-", "-"],
            "markers": [None, "o", "o"],
            "legends": legends,
            "title": "Perforated plate convergence plot",
        }
        xy_plot = XYPlot(config)
        criteria = 100 * convergence_target
        xy_plot.set_plot_data([0, 100], [criteria, criteria], 0, ((1, 100), (0, 120)))
        return xy_plot
    except Exception:
        return None


def _update_convergence_plot(
    xy_plot,
    iterations: list,
    pressure_residues: list,
    delta_residues: list,
) -> None:
    """Updates the live convergence plot after each nonlinear iteration."""
    if xy_plot is None or not iterations:
        return
    dy = 20
    xlim = (1, max(iterations))
    ylim = (0, (round(max(pressure_residues) / dy, 0) + 1) * dy)
    xy_plot.set_plot_data(iterations, pressure_residues, 1, (xlim, ylim))
    if delta_residues:
        xy_plot.set_plot_data(iterations, delta_residues, 2, (xlim, ylim))


class HarmonicSolver:
    """
    Generic harmonic solver (frequency-domain analysis).

    Solves  A(ω)·x = f(ω)  for each frequency using any assembler
    that implements the Assembler interface.

    Available methods
    -----------------
    direct_method          : direct solution frequency by frequency.
    nonlinear_direct_method: same, with iteration for nonlinearities
                             (e.g. acoustic perforated plate).
    mode_superposition     : modal superposition using ModalSolver.
    """

    # ── Linear direct method ──────────────────────────────────────────────

    def direct_method(
        self,
        assembler: Assembler,
        frequencies: np.ndarray,
    ) -> np.ndarray:
        """
        Direct solution frequency by frequency.

        Parameters
        ----------
        assembler : Assembler
            Assembler providing A(ω) and f(ω).
        frequencies : np.ndarray
            Frequency vector in Hz.

        Returns
        -------
        np.ndarray
            Full solution, shape (n_dofs_total, n_freqs).
        """

        n_dofs = assembler.get_system_matrix(0, 0.0).shape[0]
        n_freqs = len(frequencies)
        solution = np.zeros((n_dofs, n_freqs), dtype=complex)

        for i, freq in enumerate(frequencies):
            logging.info(
                f"Solution step {i + 1} and frequency {freq:.3f} Hz "
                f"[{i + 1}/{n_freqs}]"
            )

            omega = 2 * np.pi * freq
            A = assembler.get_system_matrix(i, omega)
            f = assembler.get_load_vector(i, omega)

            solution[:, i] = spsolve(A, f)

            if assembler.stop_processing():
                return None

        return assembler.reinsert_prescribed_dofs(solution)

    # ── Nonlinear direct method ───────────────────────────────────────────

    def nonlinear_direct_method(
        self,
        assembler: Assembler,
        frequencies: np.ndarray,
    ) -> tuple[np.ndarray, list | None]:
        """
        Direct solution with iteration for nonlinearities.

        Depends on additional assembler methods:
        - assembler.update_after_iteration()        → rebuilds matrices after element state update
        - assembler.check_convergence(pressure_residues, delta_residues) → bool
        - assembler.convergence_data_log            → filled upon convergence
        - assembler.convergence_plot                → set to the XY plot after the run

        Parameters
        ----------
        assembler : Assembler
            Assembler with nonlinearity support.
        frequencies : np.ndarray
            Frequency vector in Hz.

        Returns
        -------
        solution : np.ndarray  shape (n_dofs_total, n_freqs)
        convergence_data_log : list | None
        """

        n_dofs = assembler.get_system_matrix(0, 0.0).shape[0]
        n_freqs = len(frequencies)

        indexes = list(np.arange(n_freqs, dtype=int))[1:]
        previous_solution = np.zeros((n_dofs, n_freqs), dtype=complex)

        pressure_residues: list[float] = []
        delta_residues: list[float] = []
        iterations: list[int] = []

        cache_delta_pressures: list = []
        cache_delta: list = []
        unstable_frequencies: dict = {}
        freq_indexes: dict = {}

        xy_plot = _build_convergence_plot(assembler.convergence_target)

        count = 0
        converged = False
        relative_difference = 1.0

        while relative_difference > assembler.convergence_target or not converged:

            if assembler.stop_processing():
                return None, None

            # ── Solve for all frequencies ─────────────────────────────────
            solution = np.zeros((n_dofs, n_freqs), dtype=complex)
            for i, freq in enumerate(frequencies):
                omega = 2 * np.pi * freq
                A = assembler.get_system_matrix(i, omega)
                f = assembler.get_load_vector(i, omega)
                solution[:, i] = spsolve(A, f)

            solution = assembler.reinsert_prescribed_dofs(solution)

            # ── Update nonlinear state and compute residuals ───────────────
            delta_pressures_list: list = []
            cache_delta_residues: list = []
            cache_pressure_residues = np.array([])

            nl_elements = assembler.nl_elements
            for i, element in enumerate(nl_elements):

                first_idx = element.first_node.global_index
                last_idx = element.last_node.global_index

                p_first = solution[first_idx, :]
                p_last = solution[last_idx, :]
                pp_delta = p_last - p_first
                element.update_delta_pressure(pp_delta)

                res_first = _relative_error(
                    solution[first_idx, indexes],
                    previous_solution[first_idx, indexes],
                )
                res_last = _relative_error(
                    solution[last_idx, indexes],
                    previous_solution[last_idx, indexes],
                )
                cache_pressure_residues = np.r_[
                    cache_pressure_residues, res_first, res_last
                ]

                idx_max = np.argmax(np.abs(pp_delta[indexes]))
                max_val = np.max(np.abs(pp_delta[indexes]))

                if len(delta_pressures_list) == len(nl_elements):
                    delta_pressures_list[i] = pp_delta[1:]
                    cache_delta_residues[i] = _relative_error(
                        delta_pressures_list[i], cache_delta_pressures[i]
                    )
                else:
                    delta_pressures_list.append(pp_delta[1:])
                    cache_delta_pressures.append(
                        np.zeros_like(pp_delta[1:], dtype=complex)
                    )
                    cache_delta_residues.append(
                        _relative_error(
                            delta_pressures_list[i], cache_delta_pressures[i]
                        )
                    )

                if count >= 5:
                    if len(cache_delta) == len(nl_elements):
                        if abs((cache_delta[i] - max_val) / cache_delta[i]) > 0.5:
                            if idx_max in freq_indexes:
                                freq_indexes[idx_max] += 1
                            else:
                                freq_indexes[idx_max] = 1
                        cache_delta[i] = max_val
                    else:
                        cache_delta.append(max_val)

            count += 1
            relative_difference = float(np.max(cache_pressure_residues))
            pressure_residues.append(100 * relative_difference)
            delta_residues.append(100 * max(cache_delta_residues))
            iterations.append(count)

            cache_delta_pressures = delta_pressures_list.copy()
            previous_solution = solution.copy()

            for ind, repetitions in freq_indexes.items():
                if repetitions >= 4 and ind not in unstable_frequencies:
                    _freqs = frequencies[indexes]
                    freq = _freqs[ind]
                    unstable_frequencies[ind] = freq
                    indexes.remove(ind)
                    msg = (
                        f"The {freq}Hz frequency step produces unstable results, "
                        "therefore it will be excluded from the convergence criteria.\n"
                    )
                    print(msg)

            # Rebuild assembler matrices now that element delta-pressures are updated
            assembler.update_after_iteration()

            _update_convergence_plot(xy_plot, iterations, pressure_residues, delta_residues)

            converged = assembler.check_convergence(
                iterations, pressure_residues, delta_residues, unstable_frequencies
            )

            if converged:
                if xy_plot is not None:
                    xy_plot.show()
                assembler.convergence_plot = xy_plot
                return previous_solution, assembler.convergence_data_log

        assembler.convergence_plot = xy_plot
        return previous_solution, None

    # ── Mode superposition ────────────────────────────────────────────────

    def mode_superposition(
        self,
        assembler: Assembler,
        frequencies: np.ndarray,
        modal_solver,
        n_modes: int,
        fastest: bool = True,
    ) -> np.ndarray:
        """
        Harmonic solution via mode superposition.

        Parameters
        ----------
        assembler : Assembler
            Assembler providing K, M and F for superposition.
        frequencies : np.ndarray
            Frequency vector in Hz.
        modal_solver : ModalSolver
            ModalSolver instance to obtain mode shapes.
        n_modes : int
            Number of modes to use.
        fastest : bool
            If True uses 3-D tensor product (faster).

        Returns
        -------
        np.ndarray  shape (n_dofs_total, n_freqs)
        """

        from pulse.processing.solvers.modal_solver import ModalSolver

        alpha, beta, eta = assembler.global_damping

        natural_frequencies, modal_shape = modal_solver.solve(
            assembler, n_modes=n_modes
        )
        # modal_shape here is already full (with prescribed DOFs reinserted) from
        # ModalSolver.solve(); mode_superposition needs the reduced space version,
        # so we use the internal method without reinsertion.
        natural_frequencies, modal_shape = assembler.modal_analysis_reduced(n_modes)

        n_freqs = len(frequencies)
        rows = modal_shape.shape[0]

        F = assembler.get_loads_matrix(loads_matrix3D=fastest)

        if fastest:
            n_m = len(natural_frequencies)
            omega = 2 * np.pi * frequencies.reshape(n_freqs, 1, 1)
            omega_n = 2 * np.pi * natural_frequencies

            F_kg = omega_n ** 2
            F_mg = -(omega ** 2)
            F_cg = 1j * ((eta + beta * omega) * (omega_n ** 2) + (omega * alpha))

            diag = np.divide(1, (F_kg + F_mg + F_cg)) * np.eye(n_m)
            F_aux = modal_shape.T @ F
            solution = modal_shape @ (diag @ F_aux)
            solution = solution.reshape(n_freqs, rows).T

            if assembler.stop_processing():
                return None

        else:
            solution = np.zeros((rows, n_freqs), dtype=complex)
            F_aux = modal_shape.T @ F
            omega_n = 2 * np.pi * natural_frequencies
            F_kg = omega_n ** 2

            for i, freq in enumerate(frequencies):
                omega = 2 * np.pi * freq
                F_mg = -(omega ** 2)
                F_cg = 1j * ((eta + beta * omega) * (omega_n ** 2) + (omega * alpha))
                data = np.divide(1, (F_kg + F_mg + F_cg))
                diag = np.diag(data)
                solution[:, i] = modal_shape @ (diag @ F_aux[:, i])

                if assembler.stop_processing():
                    return None

        return assembler.reinsert_prescribed_dofs(solution)
