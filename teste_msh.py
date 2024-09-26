import gmsh
import sys

import numpy as np

def create_curve():
    gmsh.initialize('', False)
    gmsh.option.setNumber("General.Terminal",0)
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.option.setNumber("Geometry.Tolerance", 1e-6)
    gmsh.option.setNumber("Geometry.ToleranceBoolean", 1e-3)

    start_coords = np.array([-9207.69, 16853.44, 2336.684], dtype=float)
    end_coords = np.array([-9113.244, 16600.31, 2606.684], dtype=float)
    # center_coords = np.array([-9113.30542677, 16600.47463083, 2336.68419489], dtype=float)
    center_coords = np.array([-9113.30542677, 16600.4746308,  2336.68419489], dtype=float)

    rad_1 = np.linalg.norm(start_coords - center_coords)
    rad_2 = np.linalg.norm(end_coords - center_coords)

    print(f"start_coords: {np.array(start_coords)}")
    print(f"end_coords: {np.array(end_coords)}")
    print(f"center_coords: {np.array(center_coords)}")

    print(f"start-to-center distance: {rad_1}")
    print(f"end-to-center distance: {rad_2}")

    start_point = gmsh.model.occ.addPoint(*start_coords)
    end_point = gmsh.model.occ.addPoint(*end_coords)
    center_point = gmsh.model.occ.addPoint(*center_coords)

    arc = gmsh.model.occ.addCircleArc(start_point, center_point, end_point)

    gmsh.model.occ.synchronize()

    if '-nopopup' not in sys.argv:
        gmsh.option.setNumber('General.FltkColorScheme', 1)
        gmsh.fltk.run()

create_curve()