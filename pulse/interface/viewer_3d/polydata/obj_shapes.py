from pulse import SYMBOLS_DIR

from molde.utils.poly_data_utils import read_obj_file, transform_polydata


def create_new_lumped_mass():
    polydata = read_obj_file(SYMBOLS_DIR / "structural/new_lumped_mass.obj")

    return transform_polydata(
        polydata,
        rotation=(0, -90, 0),
        scale=(3.5, 3.5, 3.5),
    )

def create_lumped_spring():
    polydata = read_obj_file(SYMBOLS_DIR / "structural/lumped_spring.obj")

    return transform_polydata(
        polydata,
    )

def create_lumped_dumper():
    polydata = read_obj_file(SYMBOLS_DIR / "structural/lumped_damper.obj")

    return transform_polydata(
        polydata,
        position=(-0.145, 0, 0),
        scale=(1.5, 1.5, 1.5),
    )

def create_compressor_discharge():
    polydata = read_obj_file(SYMBOLS_DIR / "acoustic/compressor_discharge.obj")

    return transform_polydata(
        polydata,
        scale=(0.6, 0.6, 0.6),
    )

def create_compressor_suction():
    polydata = read_obj_file(SYMBOLS_DIR / "acoustic/compressor_discharge.obj")

    return transform_polydata(
        polydata,
        scale=(0.6, 0.6, 0.6),
    )

def create_pump_discharge():
    polydata = read_obj_file(SYMBOLS_DIR / "acoustic/pump_discharge.obj")

    return transform_polydata(
        polydata,
        scale=(0.6, 0.6, 0.6),
    )

def create_pump_suction():
    polydata = read_obj_file(SYMBOLS_DIR / "acoustic/pump_suction.obj")

    return transform_polydata(
        polydata,
        scale=(0.6, 0.6, 0.6),
    )
