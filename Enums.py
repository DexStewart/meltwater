from enum import Enum, auto

class ClockState(Enum):
    STARTGAME = auto()
    SRESOLVE = auto()
    FLEE = auto()
    DEFECT = auto()
    DIE = auto()
    ACTION = auto()
    ACTION_3 = auto()
    ACTION_2 = auto()
    ACTION_1 = auto()
    POLLUTE = auto()
    DRESOLVE = auto()
    KILLHEX = auto()
    ADDCIV = auto()
    REVEAL = auto()

# Identificatori folositi la sfarsitul interpretarii semantice a mesajului pentru ca secventiatorul sa stie ce sa faca in continuare
class OutputType(Enum):
    ERROR = auto()          # Mesajul nu are sens
    DO_NOTHING = auto()     # Mesaj corect, dar nu e nici o comanda de executat (ex: urmeaza comenzile pentru o noua celula)
    IGNORED = auto()        # Bun pentru depanare sau pentru trimiterea comenzii la alt automat
    COMMAND = auto()        # Trebuie executata comanda data
    STARVATION_END = auto() # Iesire din faza Starvation
    SURRENDER = auto()      # Se termina jocul

RESET_CODE = 0

class Starvation(Enum):
    RESET = RESET_CODE
    SRESOLVE = auto()
    SQUESTION = auto()


class Doomsday(Enum):
    RESET = RESET_CODE
    KILLHEX1 = auto()
    KILLHEX2 = auto()
    ADDCIV = auto()


class Action(Enum):
    RESET = RESET_CODE
    ACTING = auto()


class UnitType(Enum):
    SOLDIER = auto()
    CIV = auto()
    STOCKPILE = auto()


class UnitDisplayType(Enum):
    CIV = 0
    SOLDIER = 1
    STOCKPILE = 2
    NEUTRAL_CIV = 3


class HexType(Enum):
    OCEAN = auto()
    SNOW = auto()
    ICE = auto()


class Player(Enum):
    RED = auto()
    BLUE = auto()
    GREY = auto()


class Status(Enum):
    CLEAN = auto()
    CONTAMINATED = auto()
    DEAD = auto()


class Command(Enum):
    REVEAL = auto()
    SURRENDER = auto()
    SEND = auto()
    AEND = auto()
    DEND = auto()
    FLEE = auto()
    SRESOLVE = auto()
    DEFECT = auto()
    DIE = auto()
    MARCH = auto()
    THREATEN = auto()
    PRESSGANG = auto()
    TRANSPORT = auto()
    ATTACK = auto()
    MILITARIZE = auto()
    DRESOLVE = auto()
    KILLHEX = auto()
    ADDCIV = auto()
    PASS = auto()


class MoveType(Enum):
    MARCH = auto()
    DEFECT = auto()
    TRANSPORT = auto()
