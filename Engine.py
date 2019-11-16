from Enums import *


class Engine:
    def __init__(self, starvation_sequencer, action_sequencer, doomsday_sequencer, game_map):
        self.game_map = game_map
        self.turn_counter = 0
        self.player = Player.BLUE
        self.action_sequencer = action_sequencer
        self.action_sequencer.player = self.player
        self.doomsday_sequencer = doomsday_sequencer
        self.doomsday_sequencer.player = self.player     # Poate ca e inutila
        self.starvation_sequencer = starvation_sequencer
        self.starvation_sequencer.player = self.player


    def run(self):
        turn_counter = 0
        while True:
            # print(self.game_map)
            # Chemarea unui obiect de tip "callable". De fapt, e chemata metoda self.starvation_sequencer.__call__()
            if turn_counter > 1:
                self.game_map.refresh_unresolved_hexes()
                if self.game_map.unresolved_hexes_exist():
                    if not self.starvation_sequencer(self.player):
                        break
            # Chemarea unui obiect de tip "callable". De fapt, e chemata metoda self.action_sequencer.__call__()
            if not self.action_sequencer(self.player):
                break
            # Chemarea unui obiect de tip "callable". De fapt, e chemata metoda self.doomsday_sequencer.__call__()
            if not self.doomsday_sequencer(self.player):
                break
            turn_counter += 1
            self.switch_players()


    def switch_players(self):
        if self.player == Player.BLUE:
            self.player = Player.RED
        else:
            self.player = Player.BLUE
        self.action_sequencer.player = self.player
        self.doomsday_sequencer.player = self.player     # Poate ca e inutila
        self.starvation_sequencer.player = self.player
