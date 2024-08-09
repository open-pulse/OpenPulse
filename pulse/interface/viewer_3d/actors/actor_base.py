from abc import ABC, abstractmethod

from vtkmodules.vtkRenderingCore import vtkActor


class ActorBase(ABC):
    def __init__(self):
        self._actor = vtkActor()
        super().__init__()

    @abstractmethod
    def source(self):
        pass

    @abstractmethod
    def filter(self):
        pass

    @abstractmethod
    def map(self):
        pass

    @abstractmethod
    def actor(self):
        pass

    def build(self):
        self.source()
        self.filter()
        self.map()
        self.actor()

    def getActor(self):
        return self._actor

    def setVisibility(self, cond):
        self._actor.SetVisibility(cond)
