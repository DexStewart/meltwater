from Enums import Player

class CommandObject:
    def __init__(self, cmd=None, player=None, source=None, target=None, target2=None, units=None):
        self.cmd = cmd
        self.player = player
        if player == Player.BLUE:
            self.enemy = Player.RED
        else:
            self.enemy = Player.BLUE
        self.source = source
        self.target = target
        self.target2 = target2
        self.units = units

    def __call__(self):
        pass