# Open Source Software for Pulsation Analysis of Pipelines (OpenPulse)

*v1.0: Pipe only system (no cylinders or vessels considered)*

OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. It allows to import the geometry of the pipe system (lines in IGES), insert materials properties, set sections, and import pressure/acceleration/force loads (from measurements or theory). OpenPulse performs an acoustic harmonic response analysis of the respective 1D acoustic domain using the Finite Element Transfer Method (FETM). The resulting pressure field is applied as a distributed load over the respective structural piping system, modeled with the Timoshenko beam theory and the Finite Element Method (FEM), in order to run a structural harmonic response analysis. In addition to simply boundary conditions as constraints on displacements, OpenPulse allows to insert lumped springs, masses and dampers along the domain.

After defining the FEM mesh for the model, you can plot the piping system geometry and run simulations such as modal analysis and harmonic analysis. It is possible to plot deformed shapes, frequency plots of acoustical and structural responses, stress fields and local stresses of desired sections.

You can try it out now by running the tutorial on binder.

## Documentation

Access the Theory Reference for [Acoustic Gas Pulsation](https://www.overleaf.com/read/yxkdxvtpzgwd), [Structural Vibration Module](https://www.overleaf.com/read/qknbtmvyfxyn) and [Assembly Technique](https://www.overleaf.com/read/kzbbgbvpjjqc).

## Questions
If you have any questions you can open a new issue with the tag 'question'.

## Requirements

    Python v. 3.7 
    scipy
    matplotlib
    numpy
    PyQt5
    vtk
    

## Installing

    pip install -r requirements.txt
    
## Authors
    Olavo M. Silva,
    Diego M. Tuozzo, 
    Lucas V. Q. Kulakauskas,
    Jacson G. Vargas,
    Andre F. Fernandes,
    José L. Souza,
    Ana P. Rocha.

## Running the examples

**

## Built With

**

## License

**
