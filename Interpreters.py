from CommandObject import *
from Enums import *
from Hex import *

# Toate astea pot fi functii. In Python, si functiile sunt obiecte, asa ca sunt manipulate mai comod
class StarvationInterpreter:
    def __init__(self, game_map):
        self.game_map = game_map

    def __call__(self, cmd, player):
        cmd = cmd.split(" ")
        if cmd[0] == 'SRESOLVE':
            if len(cmd) != 2:
                return False, None, None
            return True, Command.SRESOLVE, CommandObject(cmd[0], target=self.game_map.decode_chess(cmd[1]), player=player)
        elif cmd[0] == 'FLEE':
            if len(cmd) != 3:
                return False, None, None
            return True, Command.FLEE, CommandObject(cmd[0], target=self.game_map.decode_chess(cmd[1]), units=cmd[2], player=player)
        elif cmd[0] == 'DEFECT':
            if len(cmd) != 3:
                return False, None, None
            return True, Command.DEFECT, CommandObject(cmd[0], target=self.game_map.decode_chess(cmd[1]), units=cmd[2], player=player)
        elif cmd[0] == 'DIE':
            if len(cmd) != 2:
                return False, None, None
            return True, Command.DIE, CommandObject(cmd[0], units=cmd[1], player=player)
        else:
            return False, None, None


class ActionInterpreter:
    def __init__(self, game_map):
        self.game_map = game_map

    def __call__(self, cmd, player):
        cmd = cmd.split(" ")
        if cmd[0] == 'MARCH':
            if len(cmd) < 4:
                return False, None
            return True, Command.MARCH, CommandObject(cmd[0], source=self.game_map.decode_chess(cmd[1]), target=self.game_map.decode_chess(cmd[2]), units=cmd[3:], player=player)
        elif cmd[0] == 'THREATEN':
            if len(cmd) != 4:
                return False, None
            return True, Command.THREATEN, CommandObject(cmd[0], source=self.game_map.decode_chess(cmd[1]), target=self.game_map.decode_chess(cmd[2]), target2=self.game_map.decode_chess(cmd[3]), player=player)
        elif cmd[0] == 'PRESSGANG':
            if len(cmd) != 4:
                return False, None
            return True, Command.PRESSGANG, CommandObject(cmd[0], source=self.game_map.decode_chess(cmd[1]), target=self.game_map.decode_chess(cmd[2]), target2=self.game_map.decode_chess(cmd[3]), player=player)
        elif cmd[0] == 'TRANSPORT':
            if len(cmd) != 3:
                return False, None
            return True, Command.TRANSPORT, CommandObject(cmd[0], source=self.game_map.decode_chess(cmd[1]), target=self.game_map.decode_chess(cmd[2]), player=player)
        elif cmd[0] == 'ATTACK':
            if len(cmd) != 4:
                return False, None
            return True, Command.ATTACK, CommandObject(cmd[0], source=self.game_map.decode_chess(cmd[1]), target=self.game_map.decode_chess(cmd[2]), target2=self.game_map.decode_chess(cmd[3]), player=player)
        elif cmd[0] == 'MILITARIZE':
            if len(cmd) != 3:
                return False, None
            return True, Command.MILITARIZE, CommandObject(cmd[0], target=self.game_map.decode_chess(cmd[1]), target2=self.game_map.decode_chess(cmd[2]), player=player)
        elif cmd[0] == 'PASS':
            if len(cmd) != 1:
                return False, None
            return True, Command.PASS, CommandObject(cmd[0], player=player)

        else:
            return False, None


class DoomsdayInterpreter:
    def __init__(self, game_map):
        self.game_map = game_map

    def __call__(self, cmd, player):
        cmd = cmd.split(" ")
        if cmd[0] == 'DRESOLVE':
            if len(cmd) != 2:
                return False, None
            return True, Command.DRESOLVE, CommandObject(cmd[0], target=self.game_map.decode_chess(cmd[1]), player=player)
        elif cmd[0] == 'KILLHEX':
            if len(cmd) != 2:
                return False, None
            return True, cmd[0], CommandObject(cmd[0], target=self.game_map.decode_chess(cmd[1]), player=player)
        elif cmd[0] == 'ADDCIV':
            if len(cmd) != 2:
                return False, None
            return True, cmd[0], CommandObject(cmd[0], target=self.game_map.decode_chess(cmd[1]), player=player)
        else:
            return False, None