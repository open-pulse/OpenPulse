from dataclasses import dataclass, field, fields
from enum import IntEnum
from functools import wraps

from pulse import VERSION


class ImportType(IntEnum):
    CAD_FILE = 0
    BUILT_IN = 1


def ignore_extra_kwargs(cls):
    init_original = cls.__init__

    @wraps(init_original)
    def new_init(self, *args, **kwargs):
        field_names = {f.name for f in fields(self)}
        valid_fields = {k: v for k, v in kwargs.items() if k in field_names}
        init_original(self, *args, **valid_fields)

    cls.__init__ = new_init
    return cls


@ignore_extra_kwargs
@dataclass
class MesherSetup:
    element_size: float = 0.01
    geometry_tolerance: float = 1e-6
    length_unit: str = 'meter'

    def as_dict(self) -> dict:
        mesh_setup = {
            "length_unit" : self.length_unit,
            "element_size" : self.element_size,
            "geometry_tolerance" : self.geometry_tolerance,
            }

        return mesh_setup


@dataclass
class ProjectSetup:
    import_type: IntEnum = ImportType.BUILT_IN
    version: str = VERSION
    geometry_filename: str = ""
    geometry_path_source: str = ""
    geometry_path_internal: str = ""
    mesher_setup: MesherSetup = field(default_factory = MesherSetup)

    def as_dict(self) -> dict:

        data = {
            "version" : self.version,
            "import_type" : self.import_type,
            }
        
        if self.geometry_filename != "" and self.geometry_path_source != "":
            data.update({
                "geometry_filename" : self.geometry_filename,
                "geometry_path_source" : self.geometry_path_source,
                })

        data["mesher_setup"] = self.mesher_setup.as_dict()

        return data