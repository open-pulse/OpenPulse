from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from opv.openPulse3DLines import OpenPulse3DLines

class OPVLayer(Qt.QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.plot = OpenPulse3DLines()
        self.plot.start()
        self.generic_init()

    def reset(self):
        self.removeWidget(self.vtkWidget)
        self.plot = OpenPulse3DLines()
        self.plot.start()
        self.generic_init()
        
    def generic_init(self):
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.plot.getRenderer())
        self.plot.getRenderer().ResetCamera()
        self.iren.Initialize()
        self.addWidget(self.vtkWidget)

    def change_line_plot(self, a,b):
        self.removeWidget(self.vtkWidget)
        self.plot = OpenPulse3DLines(a,b)
        self.plot.start()
        self.generic_init()