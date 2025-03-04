import numpy as np
from molde.actors import CommonSymbolsActorFixedSize, CommonSymbolsActorVariableSize
from molde.colors import Color, color_names
from molde.utils.poly_data_utils import read_obj_file

from pulse import SYMBOLS_DIR, app

from ..polydata import (
    create_arrow_source,
    create_cone_source,
    create_double_arrow_source,
    create_double_cone_source,
)


class NodalSymbolsActor(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register_all_shapes()
        self.build()
        self.configure_appearance()

    def register_all_shapes(self):
        self.register_shape(
            "arrow",
            create_arrow_source(),
            scale=(2, 2, 2),
        )
        self.register_shape(
            "double_arrow",
            create_double_arrow_source(),
            scale=(1.8, 1.8, 1.8),
        )
        self.register_shape(
            "double_cone",
            create_double_cone_source(),
            scale=(0.5, 0.5, 0.5),
        )
        self.register_shape(
            "cone",
            create_cone_source(),
            scale=(0.5, 0.5, 0.5),
        )
        self.register_shape(
            "mass",
            read_obj_file(SYMBOLS_DIR / "structural/new_lumped_mass.obj"),
            rotation=(0, -90, 0),
            scale=(3.5, 3.5, 3.5),
        )
        self.register_shape(
            "spring",
            read_obj_file(SYMBOLS_DIR / "structural/lumped_spring.obj"),
        )
        self.register_shape(
            "damper",
            read_obj_file(SYMBOLS_DIR / "structural/lumped_damper.obj"),
            position=(-0.145, 0, 0),
            scale=(1.5, 1.5, 1.5),
        )

    def build(self):
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *_), data in nodal_properties.items():
            if property_name == "prescribed_dofs":
                self.add_prescribed_dof_symbol(
                    position=data["coords"],
                    displacements=data["values"][:3],
                    rotations=data["values"][3:],
                )

            elif property_name == "nodal_loads":
                self.add_nodal_load_symbol(
                    position=data["coords"],
                    displacements=data["values"][:3],
                    rotations=data["values"][3:],
                )

            elif property_name == "lumped_masses":
                self.add_lumped_mass_symbol(
                    position=data["coords"],
                    values=data["values"],
                )

            elif property_name == "lumped_stiffness":
                self.add_lumped_stiffness_symbol(
                    position=data["coords"],
                    displacements=data["values"][:3],
                    rotations=data["values"][3:],
                )

            elif property_name == "lumped_dampings":
                self.add_lumped_damping_symbol(
                    position=data["coords"],
                    displacements=data["values"][:3],
                    rotations=data["values"][3:],
                )

        return super().build()

    def add_prescribed_dof_symbol(
        self,
        position: tuple[float, float, float],
        displacements: tuple[bool, bool, bool],
        rotations: tuple[bool, bool, bool],
    ):
        self.add_symbol_by_axes(
            "cone",
            position,
            axes_mask=[(i is not None) for i in displacements],
            color=color_names.GREEN,
        )

        self.add_symbol_by_axes(
            "double_cone",
            position,
            axes_mask=[(i is not None) for i in rotations],
            color=color_names.BLUE,
            size=2,
        )

    def add_nodal_load_symbol(
        self,
        position: tuple[float, float, float],
        displacements: tuple[bool, bool, bool],
        rotations: tuple[bool, bool, bool],
    ):
        self.add_symbol_by_axes(
            "arrow",
            position,
            axes_mask=[(i is not None) for i in displacements],
            color=color_names.RED,
        )

        self.add_symbol_by_axes(
            "double_arrow",
            position,
            axes_mask=[(i is not None) for i in rotations],
            color=color_names.TEAL,
        )

    def add_lumped_mass_symbol(
        self,
        position: tuple[float, float, float],
        values: tuple[float, float, float],
    ):
        if any(i is not None for i in values):
            self.add_symbol(
                "mass",
                position,
                np.array([0, 1, 0]),
                color_names.BLUE,
            )

    def add_lumped_stiffness_symbol(
        self,
        position: tuple[float, float, float],
        displacements: tuple[float, float, float],
        rotations: tuple[float, float, float],
    ):
        mask = [(a is not None) or (b is not None) for a, b in zip(displacements, rotations)]
        self.add_symbol_by_axes(
            "spring",
            position,
            axes_mask=mask,
            color=color_names.ORANGE,
        )

    def add_lumped_damping_symbol(
        self,
        position: tuple[float, float, float],
        displacements: tuple[float, float, float],
        rotations: tuple[float, float, float],
    ):
        mask = [(a is not None) or (b is not None) for a, b in zip(displacements, rotations)]
        self.add_symbol_by_axes(
            "damper",
            position,
            axes_mask=mask,
            color=color_names.PINK,
        )

    def add_symbol_by_axes(
        self,
        shape_name: str,
        position,
        axes_mask: tuple[bool, bool, bool],
        color: Color,
        size: float = 1,
    ):
        axes = [
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([0, 0, 1]),
        ]

        for axis, mask in zip(axes, axes_mask):
            if mask:
                self.add_symbol(shape_name, position, axis, color, size)

    def configure_appearance(self):
        self.set_zbuffer_offsets(1, -66000)
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()
