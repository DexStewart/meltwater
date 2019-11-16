from Enums import *
from StateMachine import StateMachine
from ActionStates import *


class ActionMachine(StateMachine):
    def __init__(self, game_map):
        # Initializeaza obiectele stari
        super().__init__(game_map)
        self.states[Action.RESET] = ActionReset(self, game_map)
        self.states[Action.ACTING] = ActionActing(self, game_map)
        self.current_state = Action.RESET
        self.action_count = 0
        # Starea initiala a masinii e RESET
        # Comportamentul in starea initiala e implementat de functia reset
        # Functia reset nu e executata. E doar stocata, ca obiect, si va fi executata cand vine primul semnal

    def accept_message(self, cmd, data):
        # Toate starile au nevoie de adresa automatului pentru a defini starea urmatoare, care e stocata in membrul current_state al automatului
        # Din acest motiv, un argument (aici e primul, dar putea fi pe orice pozitie) cu care e chemata functia starii curente e adresa automatului
        # Functionare: dupa ce starea curenta a prelucrat comanda si a generat iesirile e inlocuita de starea urmatoare
        return super().accept_message(cmd, data)

    def increment_action_count(self):
        if self.action_count < 3:
            if self.action_count == 0:
                self.set_state(Action.ACTING)
            self.action_count += 1
        else:
            self.action_count = 0
            self.set_state(Action.RESET)

    def validate_single_action_command(self, data):
        if data.cmd == 'MARCH':
            foo = data.source.get_units_from_notation(data.units)
            if foo:
                civ_present = False
                for i in foo:
                    if i.unit_type is UnitType.CIV:
                        civ_present = True
                    if i.owner is not data.player:
                        return False
                    if civ_present and data.target.status is Status.DEAD:
                        return False
                if data.target in data.source.adj.values():
                    return True
        elif data.cmd == 'THREATEN':
            if data.target in data.source.adj.values():
                if data.target.get_unit_from_type(data.enemy, UnitType.CIV):
                    if not data.source.soldier_zoc[data.enemy]:
                        if data.source.stack_size[data.player] > data.target.stack_size[data.enemy]:
                            return True
        elif data.cmd == 'PRESSGANG':
            if (data.target in data.source.adj.values() or data.target is data.source) and (data.target2 in data.target.adj.values() or not data.target2):
                if data.target.get_unit_from_type(Player.GREY, UnitType.CIV):
                    if not data.source.soldier_zoc[data.enemy]:
                        if data.source.stack_size[data.player] > data.target.stack_size[Player.GREY]:
                            return True
        elif data.cmd == 'TRANSPORT':
            if data.target in data.source.adj.values():
                if data.target.owner is data.source.owner is data.player:
                    if data.source.cargo_sc:
                        return True
        elif data.cmd == 'ATTACK':
            if data.target in data.source.adj.values():
                if data.source.get_unit_from_type(data.player, UnitType.SOLDIER) and data.target.get_unit_from_type(data.enemy, UnitType.SOLDIER):
                    foo = self.game_map.find_nearest_contaminated(data.source)
                    empty_target_available = False
                    for i in foo:
                        if not len(i.cargo):
                            empty_target_available = True
                    if data.target2 in foo:
                        if not len(data.target2.cargo):
                            return True
                        if empty_target_available:
                            return False
                        return True
        elif data.cmd == 'PASS':
            return True
        return False

    def validate_militarize(self, data):
        if not data.target.get_unit_from_type(data.player, UnitType.CIV):
            return False
        if data.target.soldier_zoc[data.enemy]:
            return False
        if data.target2:
            if not data.target2.get_unit_from_type(data.player, UnitType.CIV):
                return False
            if data.target2.soldier_zoc[data.enemy]:
                return False
        return True
