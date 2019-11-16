from Enums import Doomsday, Command, OutputType
from Execs import *
from State import State


class ActionReset(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            # Termina jocul
            return OutputType.SURRENDER, None, None
        elif cmd == Command.MILITARIZE:
            # do all the militarize stuff
            if self.machine.validate_militarize(data):
                return OutputType.COMMAND, MilitarizeExec(self.game_map, self.machine, data), None
            else:
                logging.warning('Command ignored!')
        elif self.machine.validate_single_action_command(data):
            if cmd == Command.MARCH:
                return OutputType.COMMAND, MarchExec(self.game_map, self.machine, data), None
            if cmd == Command.THREATEN:
                return OutputType.COMMAND, ThreatenExec(self.game_map, self.machine, data), None
            if cmd == Command.PRESSGANG:
                return OutputType.COMMAND, PressgangExec(self.game_map, self.machine, data), None
            if cmd == Command.TRANSPORT:
                return OutputType.COMMAND, TransportExec(self.game_map, self.machine, data), None
            if cmd == Command.ATTACK:
                return OutputType.COMMAND, AttackExec(self.game_map, self.machine, data), None
            if cmd == Command.PASS:
                return OutputType.COMMAND, PassExec(self.game_map, self.machine, data), None
        else:
            return OutputType.IGNORED, None, None


class ActionActing(State):
    def __call__(self, cmd, data):
        if cmd == Command.SURRENDER:
            return OutputType.SURRENDER, None, None
        elif self.machine.validate_single_action_command(data):
            if cmd == Command.MARCH:
                return OutputType.COMMAND, MarchExec(self.game_map, self.machine, data), None
            if cmd == Command.THREATEN:
                return OutputType.COMMAND, ThreatenExec(self.game_map, self.machine, data), None
            if cmd == Command.PRESSGANG:
                return OutputType.COMMAND, PressgangExec(self.game_map, self.machine, data), None
            if cmd == Command.TRANSPORT:
                return OutputType.COMMAND, TransportExec(self.game_map, self.machine, data), None
            if cmd == Command.ATTACK:
                return OutputType.COMMAND, AttackExec(self.game_map, self.machine, data), None
            if cmd == Command.PASS:
                return OutputType.COMMAND, PassExec(self.game_map, self.machine, data), None
        else:
            return OutputType.IGNORED, None, None