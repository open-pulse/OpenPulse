*********
Acoustics
*********


Acoustic Element Types
======================

In this section, `MMs` and damping formulations are presented considering the cases of a stagnant and a moving fluid medium. The complex wavenumber and density expressions for a 1D hard-walled cylindrical waveguide element are presented. 

Stagnant fluid medium
---------------------

Consider a hard-walled straight uniform duct element with cross-section area :math:`S_f` as shown in :ref:`Figure <figDuct_element>`. Gas properties like mean density :math:`\rho_f` and speed of sound :math:`c_f` are assumed to be uniform inside the duct. The volume velocity and the pressure at the inlet of the element are denoted as :math:`q_1` and :math:`p_1`, while :math:`q_2` and :math:`p_2` denote the corresponding quantities at the outlet. :math:`Z_f= z_f/S_f = \rho_f c_f / S_f` represents the acoustic fluid impedance of the duct element (specific impedance :math:`z_f` divided by the duct element cross-sectional area :math:`S_f` [FundamentalsAcoustics]_).

.. _figDuct_element:

.. figure:: /figures/acoustics/duct_element.png
    :align: center

    Uniform duct element. Figure created by the author.


In a stagnant fluid medium, a `MM` is used to represent the wave propagation in a rigid walled cylindrical straight duct element as indicated in :ref:`Figure <figDuct_element>`. This elemental matrix is named :math:`\mathbf{K_{\text{A}}}^e` and is presented in the expanded form with :math:`p, q` nodal vectors as

.. math::
    :label: eq_mmm_element_expand

	\begin{bmatrix}
		- i \, \mathrm{cot}(k_c x)/Z_{f} & i / Z_{f} \, \mathrm{sin}(k_c x) \\
		i / Z_{f} \, \mathrm{sin}(k_c x) & -i \, \mathrm{cot}(k_c x) / Z_{f}
	\end{bmatrix}
	\begin{bmatrix}
		p_1 \\
		p_2
	\end{bmatrix}
	=
	\begin{bmatrix}
		q_1 \\
		q_2
	\end{bmatrix}, 

where the definitions of :math:`k_c` and :math:`Z_f` will change accordingly with each damping model seen in sections `proportional`_, `wide_duct`_ and `LRF_fluid_equivalent`_, and as a consequence, three different `MMs` (apart from the classical undamped wave propagation model) will be generated maintaining the same matrix structure as Eq. :math:numref:`eq_mmm_element_expand`.

The LRF-full damping model `LRF_full`_, has a different `MM` because how the viscothermal effect is represented differs from the other three presented models [PropagationSoundWaves]_. The expanded straight tube element matrix :math:`\mathbf{K_{\text{A}}}^e` with :math:`p, q` nodal vectors for this damping model is

.. math::
    :label: eq_mm_system_complete_damped_lrf_full

	\frac{i \, S \, \Gamma \, \langle \beta \rangle_r}{z_0 \, \mathrm{sinh}(\Gamma k_0 \, x)}
	\begin{bmatrix}
		-  \,  \cosh(\Gamma k_0 \, x)  & 1 \\
		1 & - \, \cosh(\Gamma k_0 \, x)
	\end{bmatrix}
	\begin{bmatrix}
		p_1 \\
		p_2
	\end{bmatrix}
	=
	\begin{bmatrix}
		q_1 \\
		q_2 
	\end{bmatrix}

To consider a damped wave propagation, different damping models are used to represent, through the complex wavenumber :math:`k_c`, the viscothermal effect in the acoustic boundary layer. To represent a viscothermal wave propagation, the complex wavenumber is not the unique associated parameter. The complex speed of sound :math:`c_c` and phase velocity :math:`c_{ph}` are directly related with :math:`k_c`. These velocities are computed as

.. math::
    :label: eq_c_c
    
	c_c = \frac{\omega}{k_c},

.. math::
    :label: eq_c_phase

    c_{\mathrm{ph}} = \frac{\omega}{\mathcal{R}(k_c)}


One of the most frequently used measures of the attenuation capability of a viscothermal damping model for a stagnant fluid is the attenuation coefficient :math:`\alpha_0`. This coefficient is obtained from the negative imaginary part of the complex wavenumber as

.. math::
    :label: eq_alpha0
    
	\alpha_0 = - \mathcal{I}(k_c).

Other parameters that represent a viscothermal wave propagation are the shear wavenumber :math:`s=r_i \sqrt{\omega / \nu}` (being :math:`\nu=\mu/\rho_{\mathrm{f}}` the kinematic viscosity, :math:`\mu` the dynamic viscosity and :math:`\rho_{\mathrm{f}}` the fluid density), which physically represents a ratio between inertial and viscous effects and the dimensionless Helmholtz number :math:`He = k r_i`. The inertial effect is represented by the ratio :math:`r_i` and the viscous effect by the kinematic viscosity :math:`\nu`. Most of the oil and gas pipe engineering applications fulfill the propagation conditions :math:`He\ll1` (plane wave propagation) and :math:`He/s \ll 1`, generally related with high :math:`s` values, (i.e. dominant inertial effects, :math:`r_i > \sqrt{\omega / \nu}`, in the acoustic wave propagation and/or plane wave propagation). In addition, varying the pulsation :math:`\omega` for a fixed fluid and duct radius, inertial or viscous effect can be dominant depending on the :math:`\omega` value. As defined here, `AIV` is not the exception and, in general, :math:`s` greater than unity is expected for most practical industry applications. Physically, it means that inertial effects start to become dominant rather than viscous effect. 

In engineering applications, sometimes it is useful to relate length scales of an acoustic model. A comparison between the thickness of the viscous or thermal boundary layer (:math:`\delta_v = \sqrt{2 \nu / \omega}` and :math:`\delta_t = \delta_v / \sqrt{Pr}` respectively, being :math:`Pr` the Prandtl number) with a physical dimension of the model (e.g., the tube inner radius :math:`r_i`) is a frequently used length scale, which makes possible to infer the importance of viscous and thermal effects in certain acoustic models. Larger :math:`s` values can be associated with :math:`\delta_v \ll r_i` and :math:`\delta_t \ll r_i` (regarding the concept of shear wavenumber previously mentioned).


.. _undamped:

Undamped
^^^^^^^^

The classical undamped model considers a purely real wavenumber and density, i.e.,

.. math::
	k_{\mathrm{c}} = k_0 = \frac{\omega}{c_0},

.. math::
	\rho_{\mathrm{c}} = \rho_0,

where :math:`k_0`, :math:`c_0` and :math:`\rho_0` are the undisturbed wavenumber, velocity and density of the fluid medium.


.. _proportional:

Proportional
^^^^^^^^^^^^

The classical proportional damping model can be basically interpreted as a viscous-attenuation fluid property. Its value is typically obtained from experimental data and can be expressed as a part of the real value of the complex wavenumber :math:`k_c`. Also, the proportional attenuation coefficient (referred to as the loss coefficient of the material) :math:`\eta` could be frequency-dependent, :math:`\eta(f)`, or frequency-independent, :math:`\eta`. For a rightward propagating plane wave (omitting time dependence) considering proportional damping, a complex wavenumber can be assumed as

.. math::
    :label: eq_complex_wavenumber_hysteretic

    k_c = k_1 + i k_2 = k_0(1 -i \eta),

where :math:`\eta` is dimensionless. The proportional complex density can be computed as

.. math:: 
    :label: eq_complex_density
    
    \rho_{c} = \rho_{0} (1-i \eta)^2.

The proportional damping model has no limitations on its application related with the :math:`He` or the :math:`s` for `AIV` problems.

.. _wide_duct:

Wide-duct
^^^^^^^^^

The Helmholtz-Kirchhoff wall-attenuation coefficient, also known as a wide-duct wall attenuation model, is intended to account separately viscous and thermal effects, which are then summed to obtain a total wall-attenuation in tubes with radius :math:`r_i` relatively large and :math:`\omega` relatively small. Under the assumption of small dissipation condition and plane-wave propagation (i.e.,  :math:`r < \lambda`, see [ElementsAcoustics]_ for more theoretical details), the Helmholtz-Kirchhoff (total) wall-attenuation coefficient can be included in the complex wavenumber as

.. math::
    :label: eq_complex_wavenumber_wideduct

	k_c = k_0 - i\frac{\sqrt{\omega \nu_{\mathrm{f}}} }{\sqrt{2}c_{0} r_{\mathrm{i}}} \left( 1 + \frac{\gamma-1}{\sqrt{Pr}} \right),

where :math:`\nu_{\mathrm{f}}` is the undisturbed fluid kinematic viscosity, and :math:`\gamma = C_p/C_v` is the ratio of specific heats. Then, the complex fluid density for the Helmholtz-Kirchoff damping is defined as

.. math::
	\rho_{c} = \rho_{0} \left( 1 - i \frac{ \sqrt{ \nu_{\mathrm{f}} } }{ \sqrt{2 \omega } \, c_{0} \,  r_{\mathrm{i}} } \left( 1 + \frac{\gamma-1}{\sqrt{Pr}} \right) \right)^{-2}.

The Helmholtz-Kirchoff damping may be accurate within the following assumptions [ElementsAcoustics]_:

.. math::
	r_{\mathrm{i}} \gg \sqrt{\frac{ 2 \nu_{\mathrm{f}} }{\omega}},

.. math::
	r_{\mathrm{i}} \gg \sqrt{\frac{ 2 \kappa_{\mathrm{f}} }{\omega}},

.. math::
	\frac{\omega \nu_{\mathrm{f}} }{ c_{\mathrm{f}}^2 } \ll 0.5,	


where :math:`\kappa_{\mathrm{f}}` is the undisturbed fluid thermal conductivity, :math:`c_{\mathrm{f}}` is the undisturbed sound speed of the fluid  and the symbol :math:`\gg` may be interpreted as "`at least one magnitude order greater`" (similarly, :math:`\ll`).

.. _LRF_fluid_equivalent:

LRF fluid equivalent
^^^^^^^^^^^^^^^^^^^^

The `LRF` model (named by Tijdeman [PropagationSoundWaves]_) describes viscothermal acoustics in uniform tubes and layers that have a cross-section smaller than the acoustic wavelength (inside the plane wave frequency range). Inside the low-frequency range, this model covers from very narrow tubes to large ducts where the boundary layer only represents a fraction of the duct size (wide tubes).

The approximate viscothermal solution obtained from solving the Eqs.3.10 in Chapter~3 in [ViscothermalAcoustics]_ derive into the solutions for the velocity, temperature and density. The Eq.~3.28 in Chapter 3 in [ViscothermalAcoustics]_ will allow us to calculate the `LRF-EF` complex wavenumber :math:`k_c` for cylindrical waveguides. With :math:`k_c`, the viscothermal effect can be introduced onto the fluid. In **OpenPulse**, the `LRF-EF` complex wavenumber :math:`k_c` is implemented as

.. math:: 
    :label: eq_complex_wavenumber_lrf_ef

	k_c= k_0 \, \sqrt{\frac{\Upsilon_t'}{\Upsilon_v} }, 

where :math:`\Upsilon_t'=\gamma - (\gamma - 1) \Upsilon_t` is the modified cross-sectional mean thermal field, in which :math:`\Upsilon_t` (the cross-sectional mean thermal field) and also :math:`\Upsilon_v` (the cross-sectional mean viscous field) are defined, for cylindrical waveguides, as

.. math::
	\Upsilon_t = -\frac{J_2(k_t r_\mathrm{i})}{J_0(k_t r_\mathrm{i})},

.. math::
	\Upsilon_v = -\frac{J_2(k_v r_\mathrm{i})}{J_0(k_v r_\mathrm{i})},

where :math:`J_0` and  :math:`J_2` are the Bessel function of the first kind and zeroth and second order, respectively, and :math:`k_v = \sqrt{ -i \omega \rho_0 / \mu } ` and :math:`k_t = \sqrt{ - i \omega \rho_0 C_p / \kappa}` the viscous and thermal wavenumber, respectively. Considering an harmonically varying pressure :math:`p`, the Eq. :math:numref:`eq_complex_wavenumber_lrf_ef` and defining the axial velocity on the form

.. math:: 
	u(x) = \frac{i \Upsilon_v \nabla p}{k_0 z_0},

the complex fluid impedance can be calculated using the impedance definition only retaining the rightward propagating pressure term (freely propagating plane wave)

.. math::
    :label: eq_zc_lrfef

	z_c = \frac{p(x,t)}{u(x,t)} = \frac{z_0}{\sqrt{\Upsilon_v \Upsilon_t'}}.

With Eq. :math:numref:`eq_complex_wavenumber_lrf_ef` and Eq. :math:numref:`eq_zc_lrfef`, the complex fluid density can be defined as

.. math::
	\rho_{c} = \frac{ z_c k_c }{ \omega  } = \frac{ \rho_{0} }{ \Upsilon_v  }.

The `LRF-EF` damping model may be accurate within the following assumptions

.. math::
	\frac{ k_{\text{t}} }{ k } \gg 1,

.. math::
	\frac{ k_{\text{v}} }{ k } \gg 1.	

Details about the `LRF-EF` model and expressions for the mean thermal and viscous field (:math:`\Upsilon_t` and :math:`\Upsilon_v`) as well as the viscous and thermal wavenumbers (:math:`k_v` and :math:`k_t`) for different fluid cross-section geometries can be found in pp.62 and 63 and Appendix A in [ViscothermalAcoustics]_ and also related papers.

.. _LRF_full:

LRF full
^^^^^^^^

In this subsection, another `LRF` model is presented, but not using the complex wavenumber as a way to introduce the viscothermal effects onto the bulk. The `LRF`-full model presented here uses the pressure, temperature, axial velocity and density field solutions from the `LRF` approximation for cylindrical waveguides. The denomination `full` is related to the fact that the pressure and the axial velocity `LRF` solution obtained by Tijdeman in [PropagationSoundWaves]_ were used to build the `MM` presented in Eq. :math:numref:`eq_mm_system_complete_damped_lrf_full`.

The model is obtained assuming no-slip and isothermal `BC`'s at the wall of the tube and also an axial symmetric velocity profile as `BC`, and imposing a harmonic pressure perturbation as

.. math::
    :label: eq_pressure_lrf_full

	p(x,t) = \frac{\rho_0 c_0^2  }{\gamma} ( A e^{\Gamma k_0 x } + B e^{- \Gamma k_0 x} ) e^{i \omega t},

where the following dimensionless numbers are the base of this model:

.. math::
	\Gamma = \sqrt{ J_0(i^{3/2} s)   / J_2(i^{3/2} s) } \sqrt{  \gamma / n },

.. math::
	s = r_i \sqrt{\omega / \nu},

.. math::
	\gamma_p = \Big[ 1 + ((\gamma-1)/\gamma) ( J_2(i^{3/2} \sigma s)   / J_0(i^{3/2} \sigma s)  )\Big]^{-1},

.. math::
	\sigma = \sqrt{\mu C_p / \kappa} = \sqrt{Pr},

where :math:`\Gamma` is the propagation constant, :math:`s` is the shear wave number (also referred as the Stokes number) and :math:`\gamma_p` is the politropic constant. Consequently, the solution for the axial velocity is (omitting time dependence)

.. math::
    :label: eq_velocity_lrf_full

	u(x) = \frac{i c_0 \Gamma}{\gamma} \beta ( A e^{\Gamma k_0 x } - B e^{- \Gamma k_0 x} ).

where 

.. math::
	\beta = 1 - \frac{J_0\left(i^{\frac{3}{2}} s \zeta\right)}{J_0\left(i^{\frac{3}{2}} s\right)},
	
and :math:`\zeta = r/r_i` is a dimensionless radial coordinate for the moving parameter :math:`r` and the fixed value of the inner tube radius :math:`r_i` (:math:`\eta = r/R` in Tijdeman's notation). 

As can be seen, the Eq. :math:numref:`eq_pressure_lrf_full` and Eq. :math:numref:`eq_velocity_lrf_full` are radial and axial dependent. Both `TMM` and `MMM` are based on 1D `TM` and `MM`. In this case, Eq. :math:numref:`eq_pressure_lrf_full` and Eq. :math:numref:`eq_velocity_lrf_full` need to be integrated over the cross-section to obtain the 1D `TM` and `MM`. This integration is based on the parameter :math:`\beta` and is executed as indicated in Eq. :math:numref:`eq_alpha_avrg`.

The propagation constant :math:`\Gamma = \mathcal{R}(\Gamma) + i \, \mathcal{I}(\Gamma)` is one of the dimensionless parameters used to describe a wave motion considering inertia, compressibility, viscosity, and thermal conductivity of a fluid in a cylindrical tube. The relation between :math:`\Gamma` and :math:`k_c` is presented as [NoiseReduction]_ [ModelingAcoustics]_

.. math::
	k_c = -i \Gamma k_0.

Moreover, the complex density is calculated utilizing Eq. :math:numref:`eq_complex_density`. Consequently,

.. math::
	\rho_c = \frac{z_c k_c}{\omega} = \frac{\rho_0}{\langle \beta \rangle_r},

where :math:`z_c = i z_0 / (\Gamma \langle \beta \rangle_r)` is the medium-specific impedance of a propagating plane wave when duct viscothermal effect is included and :math:`\langle \beta \rangle_r` is the average of :math:`\beta` over the tube cross section, defined as

.. math:: 
    :label: eq_alpha_avrg
    
	\langle \beta \rangle_r = \frac{1}{S_f} \int_{r} 2\pi r \beta(r) \text{d}r = 1 - \frac{2 J_1 \big( s \sigma (\sqrt{2}/2) (1 - i) \big) }{  (s \sigma (\sqrt{2}/2)  (1 - i) ) J_0 \big( s \sigma i^{3/2} \big)   }.

The LRF-full damping model may be accurate for the following shear wave number condition 

.. math::
	s \geq 4,

without limitations inside the plane wave frequency range (:math:`He= k r_{\text{i}} < 1.84118`). However, when :math:`1 < s < 4` the following limitations related with the Helmholtz number may be considered [PropagationSoundWaves]_

.. math:: 
	He \ll 1, 

.. math:: 
	\frac{He}{s} \ll 1.	



.. [ElementsAcoustics] Temkin, S. **Elements of Acoustics.** 1981. Wiley. ISBN: 9780471059905.

.. [FundamentalsAcoustics] Kinsler, L.E. and Frey, A.R. and Coppens, A.B. and Sanders, J.V. **Fundamentals of Acoustics.** 2000. Wiley. ISBN: 978-0-471-84789-2.

.. [PropagationSoundWaves] H. Tijdeman. **On the propagation of sound waves in cylindrical tubes.** 1975. Journal of Sound and Vibration. `doi.org/10.1016/S0022-460X(75)80206-9 <https://doi.org/10.1016/S0022-460X(75)80206-9>`_.

.. [ViscothermalAcoustics] W.R. Kampinga. **Viscothermal acoustics using finite elements - Analysis tools for engineers.** 2010. Netherlands. University of Twente. Ipskamp Printing. `doi.org/10.3990/1.9789036530507 <https://doi.org/10.3990/1.9789036530507>`_.

.. [NoiseReduction] Van der Eerden and Fredericus Joseph Marie. **Noise reduction with coupled prismatic tubes.** 2000. Universiteit Twente.

.. [ModelingAcoustics] Paulo H. Mareze and Eric Brandão and William D'A. Fonseca and Olavo M. Silva and Arcanjo Lenzi. **Modeling of acoustic porous material absorber using rigid multiple micro-ducts network: Validation of the proposed model.** 2019. Journal of Sound and Vibration. `doi.org/10.1016/j.jsv.2018.11.036 <https://doi.org/10.1016/j.jsv.2018.11.036>`_.


Moving fluid medium
-------------------

Undamped
^^^^^^^^

Howe model
^^^^^^^^^^

Peters model
^^^^^^^^^^^^

Boundary conditions
===================

Acoustic Pressure
-----------------

Volume Velocity
---------------

Specific Impedance
------------------

Radiation Impedance
-------------------

Anechoic
^^^^^^^^

Flanged
^^^^^^^

Unflanged
^^^^^^^^^

Perforated Plate
================

Impedance model
---------------

`ALC`
-----

Resistances
-----------

Nonlinear
^^^^^^^^^

Radiation
^^^^^^^^^

Bias flow
^^^^^^^^^

FETM implementation
-------------------

Meelling's impedance model
--------------------------

Common pipe section
-------------------

Length Correction
=================

Expansion
---------

Side branch
-----------

Loop
----

moving medium
-------------

Compressor Excitation
=====================



