from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.processing.acoustic_solver import AcousticSolver
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.loading_screen import LoadingScreen
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.postprocessing.save_data import SaveData
from pulse.postprocessing.read_data import ReadData

from time import time, sleep
import logging

window_title_1 = "Error"
window_title_2 = "Warning"

class RunAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ui_path = UI_DIR / "messages/solution_log.ui"
        # uic.loadUi(ui_path, self)

        self.project = app().main_window.project

        # self._load_icons()
        # self._config_window()
        self._initialize()
        self._load_analysis_info()
        # self._define_qt_variables()
        # self._create_connections()
        # self._config_widgets()

        LoadingWindow(self.run_analysis)

        # LoadingScreen(title = 'Solution in progress', 
        #               message = 'Processing the cross-sections',  
        #               target = self.process_cross_sections, 
        #               project = self.project)
        
        # if self.project.preprocessor.stop_processing:
        #     self.project.preprocessor.stop_processing = False
        #     return

        # LoadingScreen(title = 'Solution in progress', 
        #               message = 'Preparing the model to solve', 
        #               target = self.preparing_mathematical_model_to_solve)

        # self.pre_non_linear_convergence_plot()

        # LoadingScreen(title = 'Solution in progress', 
        #               message = 'Solving the analysis',  
        #               target = self.process_analysis, 
        #               project = self.project)

        # self.post_non_linear_convergence_plot()  

        # if self.project.preprocessor.stop_processing:
        #     self.reset_all_results()
        #     self.project.preprocessor.stop_processing = False
        # else:

        #     LoadingScreen(title = 'Solution in progress', 
        #                   message = 'Post-processing the obtained results', 
        #                   target = self.post_process_results)
            
        #     # self.timer.start(200)
        #     # self.exec()
        #     self.check_warnings()
    
    def run_analysis(self):
        logging.info("Processing the cross-sections [1/4]")
        self.process_cross_sections()
        if self.project.preprocessor.stop_processing:
            self.project.preprocessor.stop_processing = False
            return

        logging.info("Preparing the model to solve [2/4]")
        self.preparing_mathematical_model_to_solve()
        self.pre_non_linear_convergence_plot()

        logging.info("Solving the analysis [3/4]")
        self.process_analysis()
        self.post_non_linear_convergence_plot()  

        if self.project.preprocessor.stop_processing:
            self.reset_all_results()
            self.project.preprocessor.stop_processing = False
        else:
            logging.info("Post-processing the obtained results [4/4]")
            self.post_process_results()
            self.check_warnings()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.solution_acoustic = None
        self.solution_structural = None
        self.convergence_dataLog = None
        self.natural_frequencies_acoustic = []
        self.natural_frequencies_structural = []
        self.complete = False
        self.solve = None

    def _define_qt_variables(self):

        # QFrame
        self.frame_message : QFrame
        self.frame_progress_bar : QFrame

        # QLabel
        self.label_title : QLabel
        self.label_message : QLabel

        # QProgressBar
        self.progress_bar_timer : QProgressBar

        # QTimer
        self.timer = QTimer()

    def _create_connections(self):
        self.timer.timeout.connect(self.update_progress_bar)
        pass

    def _config_widgets(self):
        self.label_message.setWordWrap(True)
        self.label_message.setMargin(16)
        # self.label_title.setStyleSheet("color: black; font: 75 12pt 'MS Shell Dlg 2'")
        # self.label_message.setStyleSheet("color: blue; font: 75 12pt 'MS Shell Dlg 2'")

    def update_progress_bar(self):
        self.timer.stop()
        t0 = time()
        dt = 0
        duration = 2
        while dt <= duration:
            sleep(0.1)
            dt = time() - t0
            value = int(100*(dt/duration))
            self.progress_bar_timer.setValue(value)
        self.close()

    def _load_analysis_info(self):
        self.analysis_id = self.project.analysis_ID
        self.analysis_type_label = self.project.analysis_type_label
        self.frequencies = self.project.frequencies
        self.modes = self.project.modes

    def pre_non_linear_convergence_plot(self):
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation

        if isinstance(self.solve, AcousticSolver):
            if self.analysis_id in [3,5,6]:
                if self.solve.non_linear:
                    fig = plt.figure(figsize=[8,6])
                    ax  = fig.add_subplot(1,1,1)
                    self.anime = FuncAnimation(fig, self.solve.graph_callback, fargs=(fig,ax), interval=2000)
                    self.anime._start()
                    plt.ion()
                    plt.show()

    def post_non_linear_convergence_plot(self):
        if isinstance(self.solve, AcousticSolver):
            if self.analysis_id in [3,5,6]:
                if self.solve.non_linear:
                    self.anime._stop()

    def process_cross_sections(self):
        t0 = time()
        self.complete = False
        self.project.process_cross_sections_mapping()
        self.project.time_to_process_cross_sections = time() - t0

    def preparing_mathematical_model_to_solve(self):

        t0 = time()
        if self.analysis_id in [0, 1, 3, 5, 6]:
            if self.frequencies is None:
                return
            if len(self.frequencies) == 0:
                return

        if self.project.preprocessor._process_beam_nodes_and_indexes():
            if self.analysis_id not in [0, 1, 2]:
                title = "INCORRECT ANALYSIS TYPE"
                message = "There are only BEAM_1 elements in the model, therefore, "
                message += "only structural analysis are allowable."
                info_text = [window_title_2, title, message]
                PrintMessageInput(info_text)
                return

        if self.analysis_id == 2:
            self.project.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.solve = self.project.get_structural_solve()

        elif self.analysis_id in [3, 4]:
            self.solve = self.project.get_acoustic_solve()

        elif self.analysis_id in [5, 6]:
            self.project.preprocessor.enable_fluid_mass_adding_effect()
            self.solve = self.project.get_acoustic_solve()
            
        else:
            self.project.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.solve = self.project.get_structural_solve()

        self.project.time_to_preprocess_model = time() - t0

    def process_analysis(self):
        
        t0 = time()

        if self.analysis_id == 0:
            self.solution_structural = self.solve.direct_method() # Structural Harmonic Analysis - Direct Method

        elif self.analysis_id == 1: # Structural Harmonic Analysis - Mode Superposition Method
            self.solution_structural = self.solve.mode_superposition(self.modes)

        elif self.analysis_id == 3: # Acoustic Harmonic Analysis - Direct Method
            self.solution_acoustic, self.convergence_dataLog = self.solve.direct_method()

        elif self.analysis_id == 5: # Coupled Harmonic Analysis - Direct Method
            
            t0_acoustic = time()
            self.solution_acoustic, self.convergence_dataLog = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.time_to_solve_acoustic_model = time() - t0_acoustic
            
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            
            t0_structural = time()
            self.solution_structural = self.solve.direct_method() #Coupled Harmonic Analysis - Direct Method
            self.project.time_to_solve_structural_model = time() - t0_structural
            
        elif self.analysis_id == 6: # Coupled Harmonic Analysis - Mode Superposition Method
            
            t0_acoustic = time()
            self.solution_acoustic, self.convergence_dataLog = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.time_to_solve_acoustic_model = time() - t0_acoustic
            
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            
            t0_structural = time()
            self.solution_structural = self.solve.mode_superposition(self.modes)
            self.project.time_to_solve_structural_model = time() - t0_structural
            
        elif self.analysis_id == 2: # Structural Modal Analysis
            self.natural_frequencies_structural, self.solution_structural = self.solve.modal_analysis(modes = self.modes, sigma=self.project.sigma)

        elif self.analysis_id == 4: # Acoustic Modal Analysis
            self.natural_frequencies_acoustic, self.solution_acoustic = self.solve.modal_analysis(modes = self.modes, sigma=self.project.sigma)
    
        elif self.analysis_id == 7: # Static Analysis
            self.solution_structural = self.solve.static_analysis()
        else:
            raise NotImplementedError("Not implemented analysis")

        self.project.time_to_solve_model = time() - t0

        if isinstance(self.solve, AcousticSolver):
            if self.analysis_id in [3, 5, 6]:
                if self.solve.non_linear:
                    sleep(2)

    def post_process_results(self): 

        t0 = time()
        self.project.set_perforated_plate_convergence_dataLog(self.convergence_dataLog)
        if self.analysis_id == 2:
            
            if self.solution_structural is None:
                return

            self.project.set_structural_solution(self.solution_structural)
            self.project.set_structural_natural_frequencies(self.natural_frequencies_structural.tolist())

        elif self.analysis_id == 4:
                    
            if self.solution_acoustic is None:
                return

            self.project.set_acoustic_solution(self.solution_acoustic)
            self.project.set_acoustic_natural_frequencies(self.natural_frequencies_acoustic.tolist())
        
        elif self.analysis_id == 3:

            if self.solution_acoustic is None:
                return

            self.project.set_acoustic_solution(self.solution_acoustic)
        
        elif self.analysis_id in [0, 1, 5, 6, 7]:
            
            if self.solution_structural is None:
                return

            self.project.set_structural_solve(self.solve)
            self.project.set_structural_solution(self.solution_structural)
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes()
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()
            self.project.set_structural_reactions([ self.dict_reactions_at_constrained_dofs,
                                                    self.dict_reactions_at_springs,
                                                    self.dict_reactions_at_dampers  ])

        # save = SaveData(self.project, file_name="results_data.hdf5")
        # read = ReadData(self.project, file_name="results_data.hdf5")

        self.project.time_to_postprocess = time() - t0
        _times =  [self.project.time_to_process_cross_sections, self.project.time_to_preprocess_model, self.project.time_to_solve_model, self.project.time_to_postprocess]
        self.project.total_time = sum(_times)
        # self.print_final_log()
        self.complete = True

    def reset_all_results(self):

        self.solution_structural = None
        self.solution_acoustic = None

        if self.analysis_id == 2:
            self.project.set_structural_solution(None)
            self.project.set_structural_natural_frequencies(None)
        elif self.analysis_id == 4: 
            self.project.set_acoustic_solution(None)
            self.project.set_acoustic_natural_frequencies(None)
        elif self.analysis_id == 3:
            self.project.set_acoustic_solution(None)
        elif self.analysis_id in [0, 1, 5, 6, 7]:
            self.project.set_acoustic_solution(None)
            self.project.set_structural_solution(None)
            self.project.set_structural_reactions([ {}, {}, {} ])

    def print_final_log(self):

        text = ""#"Solution finished!\n\n"
        # text += "Time to check all entries: {} [s]\n".format(round(self.project.time_to_checking_entries, 6))
        text += "Time to load/create the project: {} [s]\n".format(round(self.project.time_to_load_or_create_project, 4))
        text += "Time to process cross-sections: {} [s]\n".format(round(self.project.time_to_process_cross_sections, 4))
        text += "Time elapsed in pre-processing: {} [s]\n".format(round(self.project.time_to_preprocess_model, 4))
        if self.analysis_id in [5,6]:
            text += "Time to solve the acoustic model: {} [s]\n".format(round(self.project.time_to_solve_acoustic_model, 4))
            text += "Time to solve the structural model: {} [s]\n".format(round(self.project.time_to_solve_structural_model, 4))
        else:
            text += "Time to solve the model: {} [s]\n".format(round(self.project.time_to_solve_model, 4))
        text += "Time elapsed in post-processing: {} [s]\n\n".format(round(self.project.time_to_postprocess, 4))
        text += "Total time elapsed: {} [s]".format(round(self.project.total_time, 4))

        # text += "Press ESC to continue..."
        self.label_message.setText(text)
        self.adjustSize()

    def check_warnings(self):
        # WARNINGS REACHED DURING SOLUTION
        title = self.analysis_type_label
        message = ""
        if self.analysis_type_label == "Harmonic Analysis - Structural":
            if self.solve.flag_ModeSup_prescribed_NonNull_DOFs:
                message = self.solve.warning_ModeSup_prescribedDOFs
            if self.solve.flag_Clump and self.analysis_id==1:
                message = self.solve.warning_Clump[0]
        if self.analysis_type_label == "Modal Analysis - Structural":
            if self.solve.flag_Modal_prescribed_NonNull_DOFs:
                message = self.solve.warning_Modal_prescribedDOFs[0] 
        if message != "":
            PrintMessageInput([window_title_2, title, message])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.timer.stop()
            self.close()