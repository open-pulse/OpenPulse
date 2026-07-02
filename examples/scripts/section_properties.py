
from time import perf_counter

from sectionproperties.analysis import Section
from sectionproperties.pre.library import (
    cee_section,
    circular_hollow_section,
    circular_section,
    rectangular_hollow_section,
    tapered_flange_channel,
    tapered_flange_i_section,
)

# geom = tapered_flange_channel(
#     d=10,
#     b=3.5,
#     t_f=0.575,
#     t_w=0.475,
#     r_r=0.575,
#     r_f=0.4,
#     alpha=8,
#     n_r=16,
# )

# geom = tapered_flange_i_section(
#     d=10,
#     b=5.5,
#     t_f=0.575,
#     t_w=0.475,
#     r_r=0.575,
#     r_f=0.4,
#     alpha=8,
#     n_r=16,
# )

# geom = circular_section(d=50, n=64)
geom = circular_hollow_section(0.200, 0.010, 120)
# geom = rectangular_hollow_section(0.200, 0.200, 0.010, 0, 2, 0)
# geom = cee_section(0.200, 0.100, 0, 0.01, 0.0, 64)

# apply a section offset
geom = geom.shift_section(-0.1, -0.1)

geom.plot_geometry()
geom.create_mesh(mesh_sizes=[10e-5])

section = Section(geometry=geom)
section.display_mesh_info()
section.plot_mesh(materials=False)

t0 = perf_counter()
section.calculate_geometric_properties()
dt_A = perf_counter() - t0

t0 = perf_counter()
section.calculate_warping_properties()
dt_B = perf_counter() - t0

t0 = perf_counter()
section.calculate_plastic_properties()
dt_C = perf_counter() - t0

print(f"Time to calculate the geometric_properties: {dt_A : .8f} s")
print(f"Time to calculate the warping properties: {dt_B : .8f} s")
print(f"Time to calculate the plastic properties: {dt_C : .8f} s")
print()

# Obtém os valores calculados
a_sx, a_sy = section.get_as()
a_s11, a_s22 = section.get_as_p()
area_total = section.get_area()

print(f"Área Total da Seção: {area_total:.8e} mm²")
print(f"Área Cisalhante Efetiva (Eixo X) [A_sx]: {a_sx:.8e} mm²")
print(f"Área Cisalhante Efetiva (Eixo Y) [A_sy]: {a_sy:.8e} mm²")
print()

section.display_results()