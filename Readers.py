from abc import ABC, abstractmethod
import threading
from Display import Display

#    result_available.set()

# Astea vor fi, probabil, clase, pentru ca vor fi mai complexe decat o simpla functie
class Reader(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError


# Cititor folosit cand vrei sa rejoci un joc inregistrat deja sau pentru test
class FileReader(Reader):
    def __init__(self):
        self.counter = -1
        f = open('commands.txt')
        self.cmd_list = f.read().splitlines()

    def read(self):
        self.counter += 1
        return True, self.cmd_list[self.counter]


class MemoryReader(Reader):
    def __init__(self):
        self.counter = 0
        self.cmd_list = ['XX',

                         'MARCH f4 g3 bc bs',
                         'THREATEN c3 g2 h2',
                         'PASS',
                         'PASS',
                         'DRESOLVE c5',
                         'KILLHEX c5',
                         'DRESOLVE j2',
                         'KILLHEX j2',
                         'ADDCIV j10'
                         'SRESOLVE j4']

    def read(self):
        self.counter += 1
        return self.cmd_list[self.counter]


class CommandLineReader(Reader):
    def read(self):
        # Preia comanda
        pass


class GUIReader(Reader):
    def __init__(self):
        self.result_available = threading.Event()

    def read(self):
        self.result_available.wait()
