<p align="center">
   <img src="https://open-pulse.github.io/OpenPulse/doc/OP_gamma.PNG?raw=true" alt="OpenPulse logo" width="600"/>

# OpenPulse: Open Source Software for Pulsation Analysis of Pipeline Systems

*v2.0.11 June 20th 2025*

OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. It allows to create or/and import the geometry of the pipe system, insert materials properties, set standardized or customized sections, and import pressure/acceleration/force loads (from measurements or theory). OpenPulse performs an acoustic time-harmonic response analysis of the respective 1D acoustic domain using the Finite Element Transfer Matrix Method (FETM). The resulting pressure field is applied as a distributed load over the respective structural piping system, modeled with the Timoshenko beam theory and the Finite Element Method (FEM), in order to run a structural time-harmonic response analysis. In addition to simply boundary conditions as constraints on displacements, OpenPulse allows to insert lumped springs, masses and dampers along the domain.

After defining the FEM mesh for the model, you can plot the piping system geometry and run simulations such as modal analysis and harmonic analysis. It is possible to plot deformed shapes, frequency plots of acoustical and structural responses, stress fields and local stresses of desired sections.

*What's new?*

- New geometry interface adjustments: the user can draw geometry following the conventions of popular piping software.
- Adjustments and validation of the reciprocating compressor model.
- New reciprocating pump model for applications with liquids such as oil, fuels, and water.
- New interface and visualization tools (enhanced symbols for boundary condition, excitation, etc).
- Project file management improvements: structural and acoustic results can now be saved and retrieved.
- Enhanced animation of results (real and imaginary parts, phase monitoring, etc).
- Beam theory validity check assistant.
- Adjustments and validation of the pulsation suppression device editor.

## New geometry interface

<p align="">
   <img src="https://github.com/open-pulse/OpenPulse/blob/olavosilva-patch-1/doc/geom_OP.gif" alt="OpenPulse logo" width="800"/>

## Enhanced FE/FETM modeling and representation

<p align="">
   <img src="https://github.com/open-pulse/OpenPulse/blob/v2.0/doc/NOP_FEM.png" alt="OpenPulse logo" width="800"/>

## Pulsation suppression device editor

<p align="">
   <img src="https://github.com/open-pulse/OpenPulse/blob/v2.0/doc/NOP_Filtros.png?raw=true" alt="OpenPulse logo" width="800"/>

## Enhanced results visualisation

<p align="">
   <img src="https://github.com/open-pulse/OpenPulse/blob/olavosilva-patch-1/doc/vib1.gif?raw=true" alt="OpenPulse logo" width="500" height="400"/>


   <img src="https://github.com/open-pulse/OpenPulse/blob/olavosilva-patch-1/doc/acous1.gif?raw=true" alt="OpenPulse logo" width="500" height="400"/>

## Installing through an executable

- Install OpenPulse for Windows and Linux downloading the executables [here](https://github.com/open-pulse/OpenPulse/releases).
      
## Documentation
- You can read the API reference [here](https://open-pulse.readthedocs.io/en/latest/index.html).

- Theory Reference for [1D Acoustics](https://open-pulse.github.io/OpenPulse/doc/Acoustics.pdf), [Structural Vibration of Timoshenko Beams using FEM](https://open-pulse.github.io/OpenPulse/doc/Theory_Structural.pdf), [Weak Fluid-Structure-Coupling FETM-FEM](https://github.com/open-pulse/OpenPulse/blob/master/doc/OpenPulse___Report_D___Weak_Coupling.pdf), [Solution Types (May, 15th 21)](https://), [Matrix Assembly Technique using Python](https://open-pulse.github.io/OpenPulse/doc/Assembly.pdf) and [Stress Stiffening (Prestress)](https://github.com/open-pulse/OpenPulse/blob/master/doc/OpenPulse___Report_E___Prestress.pdf).

- Project page on [Researchgate](https://www.researchgate.net/project/Acoustically-Induced-Vibration-in-Pipeline-Systems).

- [Português] Demonstração rápida: [MOPT YouTube](https://youtu.be/l8I8lAv6CSo).

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

## OpenSD 2025 - The 2nd Open-source Scientific Computing in Structural Dynamics Conference and Summer School

- [Silva et al, 2025](https://github.com/open-pulse/OpenPulse/blob/olavosilva-patch-1/doc/OpenSD_2025.pdf)

<p align="">
   <img src="https://github.com/open-pulse/OpenPulse/blob/olavosilva-patch-1/doc/OSD1.jpg?raw=true" alt="OpenPulse logo" width="200"/>  
   <img src="https://github.com/open-pulse/OpenPulse/blob/olavosilva-patch-1/doc/OSD2.jpg?raw=true" alt="OpenPulse logo" width="355"/>  

## Next events

- Internoise 2025, 24 - 27 August, São Paulo, Brazil.

## Questions
If you have any questions you can open a new issue with the label 'question'.

## Authors

The authors are members of MOPT - Multidisciplinary Optimization Group, from Federal University of Santa Catarina (Florianópolis, SC, Brazil).

   - [Olavo M. Silva](https://www.linkedin.com/in/olavo-m-silva-5822a5151/) - Engineer;
   - [Jacson G. Vargas](https://www.linkedin.com/in/jacson-gil-vargas-a54b0768/) - Engineer;
   - [Andre F. Fernandes](https://www.linkedin.com/in/andrefpf/) - Computer Scientist;
   - [Rodrigo Schwartz](https://www.linkedin.com/in/rodrigo-schwartz-249308244/) - Computer Scientist;
   - [Diego M. Tuozzo](https://www.linkedin.com/in/martintuozzo/) - Engineer (Former Member);
   - [Lucas V. Q. Kulakauskas](https://www.linkedin.com/in/lucas-kulakauskas-5a0314182/) - Engineer (Former Member);
   - [Ana P. Rocha](https://www.linkedin.com/in/ana-paula-da-rocha-55520a176/) - Engineer (Former Member);
   - [José L. Souza](https://www.linkedin.com/in/jos%C3%A9-luiz-de-souza-8669b5114/) - Computer Scientist (Former Member);
   - [Danilo Espindola](https://www.linkedin.com/in/danilo-espindola-7b47a626b/) - Interface with other softwares;
   - [Vitor Slongo](https://www.linkedin.com/in/vitor-slongo-45298a270/) - Mesh and Geometry Specialist;
   - [Gildean Almeida](https://www.linkedin.com/in/gildean-almeida-708862298/) - Validation;
   - [Fabrício Cruz](https://www.linkedin.com/in/fabricio-emanuel-cruz/) - Validation (Former Member);
   - [Gustavo C. Martins](https://www.linkedin.com/in/gustavo-martins/) - Engineer;
   - [Vinicius H. Ribeiro](linkedin.com/in/vinícius-henrique-ribeiro-385b67218) - Computer Scientist.

<p align="center">
   <img src="https://github.com/open-pulse/OpenPulse/blob/olavosilva-patch-1/doc/MOPT4.PNG?raw=true" alt="MOPT logo" width="1100"/>

**
