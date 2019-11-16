from Enums import *
from StateMachine import StateMachine
from StarvationStates import *


class StarvationMachine(StateMachine):
    def __init__(self, game_map):
        # Initializeaza obiectele stari
        super().__init__(game_map)
        self.states[Starvation.RESET] = StarvationReset(self, game_map)
        self.states[Starvation.SRESOLVE] = SResolve(self, game_map)
        self.states[Starvation.SQUESTION] = SQuestion(self, game_map)
        # Celula pentru care se executa faza
        self.tile = None
        self.exp_command = None
        self.current_state = Starvation.RESET
        # Starea initiala a masinii e RESET
        # Comportamentul in starea initiala e implementat de functia reset
        # Functia reset nu e executata. E doar stocata, ca obiect, si va fi executata cand vine primul semnal

    def accept_message(self, cmd, data):
        # Toate starile au nevoie de adresa automatului pentru a defini starea urmatoare, care e stocata in membrul current_state al automatului
        # Din acest motiv, un argument (aici e primul, dar putea fi pe orice pozitie) cu care e chemata functia starii curente e adresa automatului
        # Functionare: dupa ce starea curenta a prelucrat comanda si a generat iesirile e inlocuita de starea urmatoare

        if cmd == Command.FLEE or cmd == Command.DEFECT or cmd == Command.DIE:
            data.source = self.tile
        return super().accept_message(cmd, data)

    def validate_sresolve(self, data):
        if data.target.capacity < len(data.target.cargo) and 0 < len(data.target.cargo):
            return True
        return False

    def validate_starvation_command(self, data):
        if data.cmd == 'DIE':
            if data.source.get_units_from_notation(data.units):
                return True
        elif data.cmd == 'FLEE':
            if data.source.get_units_from_notation(data.units):
                if data.target in data.source.adj.values():
                    return True
        elif data.cmd == 'DEFECT':
            if data.source.get_units_from_notation(data.units):
                if data.target in data.source.adj.values():
                    return True
        return False
