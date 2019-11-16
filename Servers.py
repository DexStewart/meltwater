from abc import ABC, abstractmethod
from Game import *
from Hex import *
from UnitManager import *


class Server(ABC):
    def __init__(self):
        self.player = None
        self.cmd = None

    @abstractmethod
    def execute(self, cmd):
        raise NotImplementedError


class StarvationServer(Server):
    def execute(self, exec_object):
        try:
            exec_object.do()
        except Exception as e:
            try:
                print(e)
                exec_object.undo()
                return False
            except:
                raise RuntimeError('undo failed')
        return True


class ActionServer(Server):
    def execute(self, exec_object):
        try:
            exec_object.do()
        except Exception as e:
            try:
                print(e)
                exec_object.undo()
                return False
            except:
                raise RuntimeError('undo failed')
        return True

# Fiind atat de particulara, poate ca nu trebuia derivata din Executive
class DoomsdayServer(Server):
    def execute(self, exec_object):
        try:
            exec_object.do()
        except Exception as e:
            try:
                print(e)
                exec_object.undo()
                return False
            except:
                raise RuntimeError('undo failed')
        return True
