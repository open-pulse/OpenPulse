from pulse import app


class StructureOptions:
    def __init__(self) -> None:
        self.pipeline = app().project.pipeline

        self.structure_type = None
        self.add_function = None
        self.attach_function = None
    
    def xyz_callback(self):
        pass

    def attach_callback(self):
        pass

    def configure_structure(self):
        raise NotImplementedError(f"Method configure_structure not implemented on {self.__class__.__name__}")

    def update_permissions(self):
        pass