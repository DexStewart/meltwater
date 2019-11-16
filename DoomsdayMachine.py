from Enums import *
from StateMachine import StateMachine
from DoomsdayStates import *


class DoomsdayMachine(StateMachine):
    def __init__(self, game_map):
        # Initializeaza obiectele stari
        super().__init__(game_map)

        self.states[Doomsday.RESET] = DoomsdayReset(self, game_map)
        self.states[Doomsday.KILLHEX1] = KillHex1(self, game_map)
        self.states[Doomsday.KILLHEX2] = KillHex2(self, game_map)
        self.states[Doomsday.ADDCIV] = AddCiv(self, game_map)
        # Celula pentru care se executa faza
        self.tile = None
        self.secondary_tile = None
        self.civ_tile = None
        self.current_state = Doomsday.RESET
        # Starea initiala a masinii e RESET
        # Comportamentul in starea initiala e implementat de functia reset
        # Functia reset nu e executata. E doar stocata, ca obiect, si va fi executata cand vine primul semnal

    def accept_message(self, cmd, data):
        # Toate starile au nevoie de adresa automatului pentru a defini starea urmatoare, care e stocata in membrul current_state al automatului
        # Din acest motiv, un argument (aici e primul, dar putea fi pe orice pozitie) cu care e chemata functia starii curente e adresa automatului
        # Functionare: dupa ce starea curenta a prelucrat comanda si a generat iesirile e inlocuita de starea urmatoare
        return super().accept_message(cmd, data)

    def validate_dresolve_choice(self, data):
        if [data.target.y_coord, data.target.x_coord] in self.game_map.doomsday_stack[self.game_map.doomsday_track][0]:
            return True
        return False

    def validate_killhex1(self, data):
        if data.target in self.game_map.find_nearest_contaminated(self.tile):
            return True
        return False

    def validate_killhex2(self, data):
        if data.target in self.game_map.find_nearest_contaminated(self.secondary_tile):
            return True
        return False

    def validate_addciv(self, data):
        if data.target in self.game_map.find_nearest_contaminated(self.civ_tile):
            return True
        return False