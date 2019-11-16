from Enums import Doomsday, Command, OutputType
from Execs import DResolveExec, KillHex1Exec, KillHex2Exec, AddCivExec
from State import State


# Comportamentul masinii cand e in starea RESET
class DoomsdayReset(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            # Termina jocul
            return OutputType.SURRENDER, None, None
        if cmd == Command.DRESOLVE:
            if self.machine.validate_dresolve_choice(data):
                # self.machine.set_state(Doomsday.KILLHEX1)
                # Comanda care se va executa in urma tranzitiei din RESET in FLEE e descrisa de obiectul FleeExec
                return OutputType.COMMAND, DResolveExec(self.game_map, self.machine, data), None
            else:
                return OutputType.ERROR, None, "Invalid cmd"
        else:
            return OutputType.IGNORED, None, None

class KillHex1(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            return OutputType.SURRENDER, None, None
        if self.machine.validate_killhex1(data):
            # self.machine.set_state(Doomsday.KILLHEX2)
            return OutputType.COMMAND, KillHex1Exec(self.game_map, self.machine, data), None
        else:
            return OutputType.ERROR, None, "Invalid hex"

class KillHex2(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            return OutputType.SURRENDER, None, None
        if self.machine.validate_killhex2(data):
            # self.machine.set_state(Doomsday.ADDCIV)
            return OutputType.COMMAND, KillHex2Exec(self.game_map, self.machine, data), None
        else:
            return OutputType.ERROR, None, "Invalid hex"


# Comportamentul masinii cand e in starea DIE
class AddCiv(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            return OutputType.SURRENDER, None, None
        if self.machine.validate_addciv(data):
            # self.machine.set_state(Doomsday.RESET)
            return OutputType.COMMAND, AddCivExec(self.game_map, self.machine, data), None
        else:
            return OutputType.ERROR, None, "Invalid hex"
