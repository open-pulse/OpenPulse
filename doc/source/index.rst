#######################
OpenPulse Documentation
#######################

**Open Source Software for Pulsation Analysis of Pipeline Systems**

OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. It allows to import the geometry of the pipe system (lines in IGES), insert materials properties, set sections, and import pressure/acceleration/force loads (from measurements or theory). OpenPulse performs an acoustic time harmonic response analysis of the respective 1D acoustic domain using the Finite Element Transfer Method (FETM). The resulting pressure field is applied as a distributed load over the respective structural piping system, modeled with the Timoshenko beam theory and the Finite Element Method (FEM), in order to run a structural time harmonic response analysis. In addition to simply boundary conditions as constraints on displacements, OpenPulse allows to insert lumped springs, masses and dampers along the domain.

After defining the FEM mesh for the model, you can plot the piping system geometry and run simulations such as modal analysis and harmonic analysis. It is possible to plot deformed shapes, frequency plots of acoustical and structural responses, stress fields and local stresses of desired sections.

You can try it out now by running the tutorial on binder.

.. toctree::
   :caption: Installing
   :maxdepth: 2

   installing/installing

.. toctree::
   :caption: How-to Guides
   :maxdepth: 2

.. toctree::
   :maxdepth: 2
   :caption: Code Documentation

   api/preprocessing
   api/processing
