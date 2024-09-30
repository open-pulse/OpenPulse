from pulse import app


class StructureOptions:
    def __init__(self) -> None:
        self.pipeline = app().project.pipeline
        self.structure_type = None
    
    def xyz_callback(self):
        pass

    def attach_callback(self):
        pass

    def configure_structure(self):
        raise NotImplementedError(f"Method configure_structure not implemented on {self.__class__.__name__}")

    def configure_section_of_selected(self):
        if self.structure_type is None:
            return

        kwargs = self._get_kwargs()
        if kwargs is None:
            return

        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, self.structure_type):
                continue

            for k, v in kwargs.items():
                setattr(structure, k, v)

    def update_permissions(self):
        pass

    def _get_kwargs(self) -> dict:
        raise NotImplementedError(f"Method _get_kwargs not implemented on {self.__class__.__name__}")