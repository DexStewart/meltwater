import logging
from Enums import Starvation, Command, OutputType
from Execs import SaveUniverseExec, SResolveExec, FleeExec, DefectExec, DieExec
from State import State


# Comportamentul masinii cand e in starea RESET
class StarvationReset(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            return OutputType.SURRENDER, None, None
        elif cmd == Command.SRESOLVE:
            if self.machine.validate_sresolve(data):
                return OutputType.COMMAND, SResolveExec(self.game_map, self.machine, data), None
            else:
                return OutputType.IGNORED, None, None
        else:
            return OutputType.IGNORED, None, None


class SResolve(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            # Termina jocul
            return OutputType.SURRENDER, None, None
        elif cmd == self.machine.exp_command:
            if self.machine.validate_starvation_command(data):
                if cmd == Command.FLEE:
                    return OutputType.COMMAND, FleeExec(self.game_map, self.machine, data), None
                if cmd == Command.DEFECT:
                    return OutputType.COMMAND, DefectExec(self.game_map, self.machine, data), None
                if cmd == Command.DIE:
                    return OutputType.COMMAND, DieExec(self.game_map, self.machine, data), None
            else:
                logging.warning('Command ignored!')
                return OutputType.IGNORED, None, None
        else:
            logging.warning('Command ignored!')
            return OutputType.IGNORED, None, None


class SQuestion(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            return OutputType.SURRENDER, None, None
        elif cmd == Command.SRESOLVE:
            if self.machine.validate_sresolve(data):
                return OutputType.COMMAND, SResolveExec(self.game_map, self.machine, data), None
            else:
                return OutputType.IGNORED, None, None
        else:
            return OutputType.IGNORED, None, None

