from pulse.utils import error

from time import time, sleep
import configparser


# Essa classe deixou de ser uma janelinha do PyQt
# Na verdade ela não precisa existir. Só mantive pra seguir
# a orientação de resolver o problema fazendo o mínimo de 
# mudanças possíveis.
class RunAnalysisInput:
    def __init__(self, solve, analysis_ID, analysis_type, frequencies, modes, damping, project, *args, **kwargs):
        self.project = project
        self.solve = solve
        self.analysis_ID = analysis_ID
        self.analysis_type = analysis_type
        self.frequencies = frequencies
        self.damping = damping
        self.modes = modes
        self.solution_acoustic = None
        self.solution_structural = None
        self.natural_frequencies_acoustic = []
        self.natural_frequencies_structural = []
        self.run()

    def run(self):
        t0 = time()

        if self.analysis_ID == 0:
            self.solution_structural = self.solve.direct_method(self.damping) # Structural Harmonic Analysis - Direct Method
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()

        elif self.analysis_ID == 1: # Structural Harmonic Analysis - Mode Superposition Method
            self.solution_structural = self.solve.mode_superposition(self.modes, self.damping)
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()

        elif self.analysis_ID == 3: # Acoustic Harmonic Analysis - Direct Method
            self.solution_acoustic = self.solve.direct_method()

        elif self.analysis_ID == 5: # Coupled Harmonic Analysis - Direct Method
            self.solution_acoustic = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            self.solution_structural = self.solve.direct_method(self.damping) #Coupled Harmonic Analysis - Direct Method
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()

        elif self.analysis_ID == 6: # Coupled Harmonic Analysis - Mode Superposition Method
            self.solution_acoustic = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            self.solution_structural = self.solve.mode_superposition(self.modes, self.damping)
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()

        elif self.analysis_ID == 2: # Structural Modal Analysis
            self.natural_frequencies_structural, self.solution_structural = self.solve.modal_analysis(modes = self.modes, sigma=self.project.sigma)

        elif self.analysis_ID == 4: # Acoustic Modal Analysis
            self.natural_frequencies_acoustic, self.solution_acoustic = self.solve.modal_analysis(modes = self.modes, sigma=self.project.sigma)

        self.project.time_to_solve_model = time() - t0

        # WARNINGS REACHED DURING SOLUTION
        if self.analysis_type == "Harmonic Analysis - Structural":
            if self.solve.flag_ModeSup_prescribed_NonNull_DOFs:
                error(self.solve.warning_ModeSup_prescribedDOFs, title = "WARNING")
            if self.solve.flag_Clump and self.analysis_ID==1:
                error(self.solve.warning_Clump[0], title = "WARNING")
        if self.analysis_type == "Modal Analysis - Structural":
            if self.solve.flag_Modal_prescribed_NonNull_DOFs:
                error(self.solve.warning_Modal_prescribedDOFs[0], title = "WARNING")  
