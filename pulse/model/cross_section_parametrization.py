import gmsh


def create_mesh_simple(points_coords):
    points = list()
    lines = [0 for i in range(len(points_coords))]

    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

    for coords in points_coords:
        points.append(gmsh.model.occ.addPoint(*coords))

    for index, point in enumerate(points):
        if point != points[-1]:
            lines[index] = gmsh.model.occ.addLine(points[index], points[index + 1])

        else:
            lines[index] = gmsh.model.occ.addLine(points[index], points[0])


    wire = gmsh.model.occ.addCurveLoop(lines)
    gmsh.model.occ.addSurfaceFilling(wire)

    gmsh.model.occ.synchronize()

    gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.3)    
    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()

def create_mesh_complex(points_coords_ext, points_coords_int):

    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

    points_ext = list()
    points_int = list()
    lines_ext = [0 for i in range(len(points_coords_ext))]
    lines_int = [0 for i in range(len(points_coords_int))]

    for coords in points_coords_ext:
        points_ext.append(gmsh.model.occ.addPoint(*coords))

    for coords in points_coords_int:
        points_int.append(gmsh.model.occ.addPoint(*coords))

    for index, point in enumerate(points_ext):
        if point != points_ext[-1]:
            lines_ext[index] = gmsh.model.occ.addLine(points_ext[index], points_ext[index + 1])
        
        else:
            lines_ext[index] = gmsh.model.occ.addLine(points_ext[index], points_ext[0])

    for index, point in enumerate(points_int):
        if point != points_int[-1]:
            lines_int[index] = gmsh.model.occ.addLine(points_int[index], points_int[index + 1])
        
        else:
            lines_int[index] = gmsh.model.occ.addLine(points_int[index], points_int[0])

    curve_loop_ext = gmsh.model.occ.addCurveLoop(lines_ext)
    curve_loop_int = gmsh.model.occ.addCurveLoop(lines_int)

    gmsh.model.occ.addPlaneSurface([curve_loop_ext, curve_loop_int])

    gmsh.model.occ.synchronize()

    gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.3)    
    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()


def i_beam(h, w1, w2, t1, t2, tw):

    points_coords = [
        [-w2/2, -h/2 + t2, 0],
        [-w2/2, -h/2, 0],
        [w2/2, -h/2, 0],
        [w2/2, -h/2 + t2, 0],
        [tw/2, -h/2 + t2, 0],
        [tw/2 ,h/2 - t1, 0],
        [w1/2, h/2 - t1, 0], 
        [w1/2, h/2, 0], 
        [-w1/2, h/2, 0],
        [-w1/2, h/2 - t1, 0],
        [-tw/2, h/2 - t1, 0],
        [-tw/2, -h/2 + t2, 0]
    ]

    create_mesh_simple(points_coords)

# i_beam(1.2, 0.7, 1, 0.2, 0.15, 0.3)
# # i_beam(1.5, 0.5, 0.8, 0.5, 0.3, 0.1)

def t_beam(w1, t1, h, tw):

    points_coords = [
        [-tw/2, -h/2, 0],
        [tw/2, -h/2, 0],
        [tw/2, h/2 - t1, 0],
        [w1/2, h/2 - t1, 0],
        [w1/2, h/2, 0],
        [-w1/2, h/2, 0],
        [-w1/2, h/2 - t1, 0],
        [-tw/2, h/2 - t1, 0],
    ]

    create_mesh_simple(points_coords)

# t_beam(0.5, 0.3, 1.5, 0.1)

def c_beam(h, t1, t2, w1, w2, tw):

    points_coords = [
        [0, 0, 0],
        [w2/2, 0, 0],
        [w2/2, t2, 0],
        [tw, t2, 0],
        [tw, h - t1, 0],
        [w1, h - t1, 0],
        [w1, h, 0],
        [0, h, 0]
    ]

    create_mesh_simple(points_coords)

# c_beam(1.5, 0.3, 0.3, 0.5, 0.5, 0.1)


def rectangular_beam(b, h, t):

    points_coords_ext = [
        [-b/2, -h/2, 0],
        [b/2, -h/2, 0],
        [b/2, h/2, 0],
        [-b/2, h/2, 0]
    ]

    points_coords_int = [
        [-b/2 + t, -h/2 + t, 0],
        [b/2 - t, -h/2 + t, 0],
        [b/2 - t, h/2 - t, 0],
        [-b/2 + t, h/2 - t, 0],
    ]

    create_mesh_complex(points_coords_ext, points_coords_int)

# rectangular_beam(1, 1, 0.1)

def circular_beam(d_out, t):

    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)


    circle_out = gmsh.model.occ.addCircle(0, 0, 0, d_out/2)
    circle_int = gmsh.model.occ.addCircle(0, 0, 0, d_out/2 - t)

    wire_out = gmsh.model.occ.addCurveLoop([circle_out])
    wire_int = gmsh.model.occ.addCurveLoop([circle_int])

    surface1 = gmsh.model.occ.addSurfaceFilling(wire_out)
    surface2 = gmsh.model.occ.addSurfaceFilling(wire_int)

    gmsh.model.occ.cut([(2, surface1)], [(2, surface2)])
    gmsh.model.occ.synchronize()

    gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.3)    
    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()

# circular_beam(1, 0.1)



