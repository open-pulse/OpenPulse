<p align="center">
   <img src="https://open-pulse.github.io/OpenPulse/doc/OP_gamma.PNG?raw=true" alt="OpenPulse logo" width="600"/>

# OpenPulse: Open Source Software for Pulsation Analysis of Pipeline Systems

*v2.0 April 30th 2024 (now: v2.0.0a March 15th 2024)*

OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. It allows to create or/and import the geometry of the pipe system, insert materials properties, set standardized or customized sections, and import pressure/acceleration/force loads (from measurements or theory). OpenPulse performs an acoustic time-harmonic response analysis of the respective 1D acoustic domain using the Finite Element Transfer Matrix Method (FETM). The resulting pressure field is applied as a distributed load over the respective structural piping system, modeled with the Timoshenko beam theory and the Finite Element Method (FEM), in order to run a structural time-harmonic response analysis. In addition to simply boundary conditions as constraints on displacements, OpenPulse allows to insert lumped springs, masses and dampers along the domain.

After defining the FEM mesh for the model, you can plot the piping system geometry and run simulations such as modal analysis and harmonic analysis. It is possible to plot deformed shapes, frequency plots of acoustical and structural responses, stress fields and local stresses of desired sections.

*What's new?* 

- New geometry interface: now the user can draw geometry through an intuitive interface, following the conventions of popular piping software.
- Standardization of sections and materials, along with using various unit systems.
- Adjustments and validation of the reciprocating compressor model.
- Physics validation of several analysis after comparing with 3D FEM commercial softwares.
- New interface and visualization tools.
- Enhancements of project files management.
- Enhanced animation of results (real and imaginary parts, phase monitoring, etc).

## New geometry interface

<p align="">
   <img src="https://open-pulse.github.io/OpenPulse/doc/OPv2_A.PNG?raw=true" alt="OpenPulse logo" width="800"/>

## Enhanced FE/FETM modeling and representation

<p align="">
   <img src="https://open-pulse.github.io/OpenPulse/doc/OPv2_C.PNG?raw=true" alt="OpenPulse logo" width="800"/> 

## Dark theme

<p align="">
   <img src="https://open-pulse.github.io/OpenPulse/doc/OPv2_B.PNG?raw=true" alt="OpenPulse logo" width="800"/>

## Enhanced results visualisation

<p align="">
   <img src="https://open-pulse.github.io/OpenPulse/doc/OPv2.gif?raw=true" alt="OpenPulse logo" width="800"/>

## Installing through an executable

- Install OpenPulse for Windows and Linux downloading the executables [here](https://github.com/open-pulse/OpenPulse/releases).
 
## Installing through your Python IDE

- **Install Python 3.9.0 or later** ([download](https://www.python.org/downloads/release/python-390/)).

- **Install OpenPulse**.
Clone or download [OpenPulse](https://github.com/open-pulse/OpenPulse) files. In the case of download, unzip the received file and open a terminal in the main folder (preferably, **use PowerShell as administrator**). Start by installing the
poetry module using the command:
```
pip install poetry
```

then enter the following command to install all dependencies:

```
poetry install
```

Note: if some warning was logged repeat the command 'poetry install' before trying to run OpenPulse.


- **Run OpenPulse**.
In the same folder, enter the following command in the terminal:
```
poetry run python pulse
```
      
## Documentation
- You can read the API reference [here](https://open-pulse.readthedocs.io/en/latest/index.html).

- Theory Reference for [1D Acoustics](https://open-pulse.github.io/OpenPulse/doc/Acoustics.pdf), [Structural Vibration of Timoshenko Beams using FEM](https://open-pulse.github.io/OpenPulse/doc/Theory_Structural.pdf), [Weak Fluid-Structure-Coupling FETM-FEM](https://github.com/open-pulse/OpenPulse/blob/master/doc/OpenPulse___Report_D___Weak_Coupling.pdf), [Solution Types (May, 15th 21)](https://), [Matrix Assembly Technique using Python](https://open-pulse.github.io/OpenPulse/doc/Assembly.pdf) and [Stress Stiffening (Prestress)](https://github.com/open-pulse/OpenPulse/blob/master/doc/OpenPulse___Report_E___Prestress.pdf).

- Project page on [Researchgate](https://www.researchgate.net/project/Acoustically-Induced-Vibration-in-Pipeline-Systems).

## Article published: Mechanical Systems and Signal Processing - Volume 186, 1 March 2023

- [Time-harmonic analysis of acoustic pulsation in gas pipeline systems using the Finite Element Transfer Matrix Method: Theoretical aspects](https://doi.org/10.1016/j.ymssp.2022.109824).

## ISMA2020 - International Conference on Noise and Vibration Engineering

- [Presentation](https://www.youtube.com/watch?v=iarKDAei6fg&t).
- [Full Paper](https://github.com/open-pulse/OpenPulse/blob/master/doc/ISMA_2020_PRE.pdf).

## ASA Meeting 2020 - The 179th Meeting of the Acoustical Society of America

- [Effect of flow on the acoustic length correction factor of a Helmholtz resonator neck at high Strouhal number: a symmetric three-dimensional parametric study](https://asa.scitation.org/doi/10.1121/1.5147459). 

## FIA 2020/22 - 12o Congresso Iberoamericano de Acústica 

- [FIA2020/2022](https://fia2020.com.br/anais/index.php#topo).

## EEA Forum Acusticum 2023 - 10th Convention of the European Acoustics Association 

- [Vargas \& Silva, 2023](https://appfa2023.silsystem.solutions/).

## Next events 

- Internoise 2024, 25 - 29 August, Nantes, France.
- IIR conference on Compressors and Refrigerants 2024, 9 - 11 September, Bratislava, Slovakia.

## Questions
If you have any questions you can open a new issue with the tag 'question'.

## Authors

The authors are members of MOPT - Multidisciplinary Optimization Group, from Federal University of Santa Catarina (Florianópolis, SC, Brazil).

   - [Olavo M. Silva](https://www.linkedin.com/in/olavo-m-silva-5822a5151/) - Engineer;
   - [Jacson G. Vargas](https://www.linkedin.com/in/jacson-gil-vargas-a54b0768/) - Engineer;
   - [Andre F. Fernandes](https://www.linkedin.com/in/andrefpf/) - Computer Scientist; 
   - [Diego M. Tuozzo](https://www.linkedin.com/in/martintuozzo/) - Engineer (Former Member);
   - [Lucas V. Q. Kulakauskas](https://www.linkedin.com/in/lucas-kulakauskas-5a0314182/) - Engineer (Former Member);
   - [Ana P. Rocha](https://www.linkedin.com/in/ana-paula-da-rocha-55520a176/) - Engineer (Former Member);
   - [José L. Souza](https://www.linkedin.com/in/jos%C3%A9-luiz-de-souza-8669b5114/) - Computer Scientist (Former Member);
   - [Danilo Espindola](https://www.linkedin.com/in/danilo-espindola-7b47a626b/) - Interface with other softwares;
   - [Vitor Slongo](https://www.linkedin.com/in/vitor-slongo-45298a270/) - Mesh and Geometry Specialist;
   - [Gildean Almeida](https://www.linkedin.com/in/gildean-almeida-708862298/) - Validation;
   - [Fabrício Cruz](https://www.linkedin.com/in/fabricio-emanuel-cruz/) - Validation.

![alt text](https://open-pulse.github.io/OpenPulse/doc/MOPT.JPG?raw=true) 

**
