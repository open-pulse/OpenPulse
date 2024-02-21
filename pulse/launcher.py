import sys
import os
import platform
import vtk
from PyQt5 import Qt, QtCore, QtWidgets

from pulse.interface.application import Application

import matplotlib
matplotlib.use("Qt5Agg")


def main():
    """ OpenPulse main
        The main function starts the OpenPulse software.
        This will create the mainWindow and also pass the terminal arguments to it.

        # If are using Windows with HighDPI active, this'll set the scale to 100%
        # But the screen and text'll be blurry

        Example:
            To start the OpenPulse you must first install all requeriments and
            tip this command in the terminal:
            (Python3)

                $ python pulse.py

        Todo:
            Fix the HighDPI part to not blurry the screen. See more by searching "PyQt5 HighDPI".
    """
    
    # disables vtk terrible error handler
    # you may want to enable them while debugging something
    vtk.vtkObject.GlobalWarningDisplayOff() 

    if platform.system() == "Windows":
        sys.argv.append("--platform")
        sys.argv.append("windows:dpiawareness=0")

    app = Application(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
