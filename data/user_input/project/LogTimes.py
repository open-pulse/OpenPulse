from PyQt5.QtWidgets import QLineEdit, QDialog, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic

from threading import Thread
from time import time

from data.user_input.analysis.runAnalysisInput import RunAnalysisInput


# Vou comentar as coisas aqui em português mesmo só pra 
# explicar melhor. Qualquer coisa chama no telezap.

# Dá pra mudar o nome da classe pra algo como LogSolution. 
# Parece mais coerente agora.
class LogTimes(QDialog):
    def __init__(self, project, analysis_ID, analysis_type_label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Analysis/runAnalysisInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.project = project
        self.analysis_ID = analysis_ID
        self.analysis_type_label = analysis_type_label

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_message = self.findChild(QLabel, 'label_message')
        self.label_message.setWordWrap(True)
        self.config_title_font()
        self.config_message_font()

        Thread(target=self.run).start()
        self.exec_()

    def run(self):
        # Agora o método Run tá "unificado" e chama todas as 
        # etapas que o usuário precisa aguardar.

        self.logTransversalSectionSolving()
        self.solveTransversalSection()

        self.logProblemSolving()
        self.solveProblem()

        self.logTimes()

    def solveTransversalSection(self):        
        # Aqui eu praticamente só copiei e colei a parte das seções transversais
        # pra não estragar muito. Só o tempo que ficou meio bagunçado, talvez 
        # você consiga ajeitar isso com mais facilidade.

        self.t0 = time()
        
        if self.analysis_ID == 2:
            self.project.mesh.enable_fluid_mass_adding_effect(reset=True)
            self.solve = self.project.get_structural_solve()
            self.modes = self.project.get_modes()
        elif self.analysis_ID == 4:
            self.solve = self.project.get_acoustic_solve()
            self.modes = self.project.get_modes()
        elif self.analysis_ID == 3:
            self.solve = self.project.get_acoustic_solve()
        elif self.analysis_ID in [5,6]:
            self.project.mesh.enable_fluid_mass_adding_effect()
            self.solve = self.project.get_acoustic_solve()
            self.modes = self.project.get_modes()
            self.damping = self.project.get_damping()
        else:
            self.project.mesh.enable_fluid_mass_adding_effect(reset=True)
            self.solve = self.project.get_structural_solve()
            self.modes = self.project.get_modes()
            self.damping = self.project.get_damping()

        self.project.time_to_preprocess_model = time() - self.t0

    def logTransversalSectionSolving(self):
        # troca o texto da janelinha de texto
        text = 'Solving transversal section.'
        self.label_message.setText(text)
    
    def solveProblem(self):
        # Aqui ele chama a resolução do problema de verdade 

        if self.analysis_ID == 2:
            solution = RunAnalysisInput(self.solve, self.analysis_ID, self.analysis_type_label, [], self.modes, [], self.project)
            if solution.solution_structural is None:
                return
            self.project.set_structural_solution(solution.solution_structural)
            self.project.set_structural_natural_frequencies(solution.natural_frequencies_structural.tolist())

        elif self.analysis_ID == 4:
            solution = RunAnalysisInput(self.solve, self.analysis_ID, self.analysis_type_label, [], self.modes, [], self.project)
            if solution.solution_acoustic is None:
                return
            self.project.set_acoustic_solution(solution.solution_acoustic)
            self.project.set_acoustic_natural_frequencies(solution.natural_frequencies_acoustic.tolist())
        
        elif self.analysis_ID == 3:
            solution = RunAnalysisInput(self.solve, self.analysis_ID, self.analysis_type_label, self.frequencies, [], [], self.project)
            if solution.solution_acoustic is None:
                return
            self.project.set_acoustic_solution(solution.solution_acoustic)
        elif self.analysis_ID in [5,6]:
            solution = RunAnalysisInput(self.solve, self.analysis_ID, self.analysis_type_label, self.frequencies, self.modes, self.damping, self.project)
            self.solve = solution.solve
            self.dict_reactions_at_constrained_dofs = solution.dict_reactions_at_constrained_dofs
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = solution.dict_reactions_at_springs, solution.dict_reactions_at_dampers
            self.project.set_structural_solution(solution.solution_structural)
        else:
            solution = RunAnalysisInput(self.solve, self.analysis_ID, self.analysis_type_label, self.frequencies, self.modes, self.damping, self.project)
            if solution.solution_structural is None:
                return
            self.solve = solution.solve
            self.dict_reactions_at_constrained_dofs = solution.dict_reactions_at_constrained_dofs
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = solution.dict_reactions_at_springs, solution.dict_reactions_at_dampers
            self.project.set_structural_solution(solution.solution_structural)
        
        self.project.time_to_postprocess = time() - (self.t0 + self.project.time_to_solve_model + self.project.time_to_preprocess_model)
        self.project.total_time = time() - self.t0
    
    def logProblemSolving(self):
        # troca o texto da janelinha de texto de novo
        text = 'Solving the problem.'
        self.label_message.setText(text)
        
    def config_title_font(self):
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setFamily("Arial")
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color:black")

    def config_message_font(self):
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setFamily("Arial")
        self.label_message.setFont(font)
        self.label_message.setStyleSheet("color:blue")

    def logTimes(self):
        text = "Solution finished!\n\n"
        text += "Time to load/create the project: {} [s]\n".format(round(self.project.time_to_load_or_create_project, 6))
        text += "Time to process cross-sections: {} [s]\n".format(round(self.project.time_to_process_cross_sections, 6))
        text += "Time elapsed in pre-processing: {} [s]\n".format(round(self.project.time_to_preprocess_model, 6))
        text += "Time to solve the model: {} [s]\n".format(round(self.project.time_to_solve_model, 6))
        text += "Time elapsed in post-processing: {} [s]\n\n".format(round(self.project.time_to_postprocess, 6))
        text += "Total time elapsed: {} [s]\n\n\n".format(round(self.project.total_time, 6))

        text += "Press ESC to continue..."
        self.label_message.setText(text)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()