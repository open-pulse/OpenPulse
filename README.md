# OpenPulse: Open Source Software for Pulsation Analysis of Pipeline Systems

*v1.0*

OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. It allows to import the geometry of the pipe system (lines in IGES), insert materials properties, set sections, and import pressure/acceleration/force loads (from measurements or theory). OpenPulse performs an acoustic time harmonic response analysis of the respective 1D acoustic domain using the Finite Element Transfer Method (FETM). The resulting pressure field is applied as a distributed load over the respective structural piping system, modeled with the Timoshenko beam theory and the Finite Element Method (FEM), in order to run a structural time harmonic response analysis. In addition to simply boundary conditions as constraints on displacements, OpenPulse allows to insert lumped springs, masses and dampers along the domain.

After defining the FEM mesh for the model, you can plot the piping system geometry and run simulations such as modal analysis and harmonic analysis. It is possible to plot deformed shapes, frequency plots of acoustical and structural responses, stress fields and local stresses of desired sections.

You can try it out now by running the tutorial on binder.

## Installing

- **Install Python 3.7.7** ([download](https://www.python.org/downloads/release/python-377/)).

- **Install OpenPulse**.
Clone or download [OpenPulse](https://github.com/open-pulse/OpenPulse) files. In the case of download, unzip the received file and open a terminal in the main folder (an easy way to do this is to enter the folder, press shift and right click, then "Open PowerShell here"). So, enter the command: 
```
pip install -r requirements.txt
```

- **Run OpenPulse**.
In the same folder, enter the following command in the terminal:
```
python pulse.py
```

## Requirements

    Python v. 3.7.7 
    scipy
    matplotlib
    numpy
    PyQt5
    vtk
    
## Documentation

- Theory Reference for [1D Acoustics using FETM](https://www.overleaf.com/read/yxkdxvtpzgwd), [Structural Vibration of Timoshenko Beams using FEM](https://open-pulse.github.io/OpenPulse/doc/Theory_Structural.pdf), [Weak Fluid-Structure-Coupling FETM-FEM](https://), [Solution Types](https://) and [Matrix Assembly Technique using Python](https://open-pulse.github.io/OpenPulse/doc/Assembly.pdf).

- [User Guide for Structural Analysis (Portuguese)](https://open-pulse.github.io/OpenPulse/doc/TEMP_Structural_UserGuide.pdf).

- [User Guide for Acoustic Analysis](https://).

- [User Guide for Coupled Analysis](https://).

## Questions
If you have any questions you can open a new issue with the tag 'question'.

## Authors

The authors are members of MOPT - Multidisciplinary Optimization Group, from Federal University of Santa Catarina (Florianópolis, SC, Brazil).

    Olavo M. Silva,
    Jacson G. Vargas,
    Diego M. Tuozzo, 
    Lucas V. Q. Kulakauskas,
    Andre F. Fernandes,
    José L. Souza,
    Ana P. Rocha.

**
