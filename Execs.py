import logging
from abc import ABC, abstractmethod
from Enums import *
from UnitManager import *


class Exec(ABC):
    def __init__(self, game_map, machine, cmd):
        self.game_map = game_map
        self.machine = machine
        self.cmd = cmd

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class SaveUniverseExec(Exec):
    def do(self):
        self.machine.tile = self.cmd.target
        self.machine.set_state(Starvation.RESET)

    def undo(self):
        pass

class RestoreUniverseExec(Exec):
    def do(self):
        pass

    def undo(self):
        pass

class SResolveExec(Exec):
    def do(self):
        logging.info('Sresolve focus set to {}'.format(self.cmd.target))
        self.machine.tile = self.cmd.target
        self.machine.exp_command = self.game_map.det_starvation_action(self.cmd.target)
        self.machine.set_state(Starvation.SRESOLVE)

    def undo(self):
        pass

class FleeExec(Exec):
    def do(self):
        unit = self.cmd.source.get_units_from_notation(self.cmd.units)[0]
        logging.info('{} FLEEING from {} to {}'.format(unit, unit.tile, self.cmd.target))
        UnitManager.move_unit(self.game_map, unit, self.cmd.target)
        if self.cmd.source.capacity < len(self.cmd.source.cargo):
            self.machine.set_state(Starvation.SRESOLVE)
            self.machine.exp_command = self.game_map.det_starvation_action(self.cmd.target)
        else:
            self.machine.exp_command = None
            self.game_map.unresolved_hexes.remove(self.cmd.source)
            if self.game_map.unresolved_hexes_exist():
                self.machine.set_state(Starvation.SQUESTION)
            else:
                self.machine.set_state(Starvation.RESET)

    def undo(self):
        pass

class DefectExec(Exec):
    def do(self):
        unit = self.cmd.source.get_units_from_notation(self.cmd.units)[0]
        logging.info('{} DEFECTING from {} to {}'.format(unit, unit.tile, self.cmd.target))
        UnitManager.defect_unit(self.game_map, self.cmd.source.get_units_from_notation(self.cmd.units)[0], self.cmd.target)
        if self.cmd.source.capacity < len(self.cmd.source.cargo):
            self.machine.set_state(Starvation.SRESOLVE)
            self.machine.exp_command = self.game_map.det_starvation_action(self.cmd.target)
        else:
            self.machine.exp_command = None
            self.game_map.unresolved_hexes.remove(self.cmd.source)
            if self.game_map.unresolved_hexes_exist():
                self.machine.set_state(Starvation.SQUESTION)
            else:
                self.machine.set_state(Starvation.RESET)
    def undo(self):
        pass

class DieExec(Exec):
    def do(self):
        unit = self.cmd.source.get_units_from_notation(self.cmd.units)[0]
        logging.info('{} DYING at location {}'.format(unit, unit.tile))
        UnitManager.remove_unit(self.game_map, unit)
        if self.cmd.source.capacity < len(self.cmd.source.cargo) and 0 < len(self.cmd.source.cargo):
            self.machine.set_state(Starvation.SRESOLVE)
            self.machine.exp_command = self.game_map.det_starvation_action(self.cmd.source)
        else:
            self.machine.exp_command = None
            self.game_map.unresolved_hexes.remove(self.cmd.source)
            if self.game_map.unresolved_hexes_exist():
                self.machine.set_state(Starvation.SQUESTION)
            else:
                self.machine.set_state(Starvation.RESET)

    def undo(self):
        pass


class DResolveExec(Exec):
    def do(self):
        logging.info('Dresolve focus set to {}'.format(self.cmd.target))
        self.machine.tile = self.cmd.target
        x = self.game_map.doomsday_stack[self.game_map.doomsday_track][0]
        x.remove([self.cmd.target.y_coord, self.cmd.target.x_coord])
        self.machine.secondary_tile = self.game_map.direct_ref_matrix[x[0][0]][x[0][1]]
        y = self.game_map.doomsday_stack[self.game_map.doomsday_track][1]
        self.machine.civ_tile = self.game_map.direct_ref_matrix[y[0]][y[1]]
        self.machine.set_state(Doomsday.KILLHEX1)
        self.game_map.doomsday_track += 1


    def undo(self):
        pass


class KillHex1Exec(Exec):
    def do(self):
        logging.info('hex {} being KILLED'.format(self.cmd.target))
        self.cmd.target.make_dead()
        self.machine.set_state(Doomsday.KILLHEX2)

    def undo(self):
        pass

class KillHex2Exec(Exec):
    def do(self):
        logging.info('hex {} being KILLED'.format(self.cmd.target))
        self.cmd.target.make_dead()
        self.machine.set_state(Doomsday.ADDCIV)

    def undo(self):
        pass

class AddCivExec(Exec):
    def do(self):
        logging.info('Civilian being ADDED to hex {}'.format(self.cmd.target))
        UnitManager.add_unit(self.game_map, [self.cmd.target, UnitType.CIV, Player.GREY])
        self.machine.set_state(Doomsday.RESET)
        self.machine.tile = None
        self.machine.secondary_tile = None
        self.machine.civ_tile = None

    def undo(self):
        pass


class MarchExec(Exec):
    def do(self):
        units = self.cmd.source.get_units_from_notation(self.cmd.units)
        for i in units:
            UnitManager.move_unit(self.game_map, i, self.cmd.target)
            logging.info('unit {} moved from {} to {}'.format(i, self.cmd.source, self.cmd.target))
        self.machine.increment_action_count()

    def undo(self):
        pass


class PressgangExec(Exec):
    def do(self):
        if self.cmd.target2:
            logging.info('stack at {} PRESSGANGED civ at {}, which moved to {}'.format(self.cmd.source, self.cmd.target, self.cmd.target2))
            UnitManager.defect_unit(self.game_map, self.cmd.target.get_unit_from_type(Player.GREY, UnitType.CIV), self.cmd.target2)
        else:
            logging.info('stack at {} PRESSGANGED civ at {}, and chose to not move it'.format(self.cmd.source, self.cmd.target))
            UnitManager.defect_unit(self.game_map, self.cmd.target.get_unit_from_type(Player.GREY, UnitType.CIV), self.cmd.target)
        self.machine.increment_action_count()

    def undo(self):
        pass


class ThreatenExec(Exec):
    def do(self):
        if self.cmd.target2:
            logging.info('stack at {} THREATENED civ at {}, which moved to {}'.format(self.cmd.source, self.cmd.target, self.cmd.target2))
            UnitManager.move_unit(self.game_map, self.cmd.target.get_unit_from_type(self.cmd.enemy, UnitType.CIV), self.cmd.target2)
        else:
            logging.info('stack at {} THREATENED civ at {}, which cannot flee and dies'.format(self.cmd.source, self.cmd.target))
            UnitManager.remove_unit(self.game_map,self.cmd.target.get_unit_from_type(self.cmd.enemy, UnitType.CIV))
        self.machine.increment_action_count()

    def undo(self):
        pass


class AttackExec(Exec):
    def do(self):
        logging.info('soldier at {} ATTACKED soldier at {}, hex {} polluted'.format(self.cmd.source, self.cmd.target, self.cmd.target2))
        UnitManager.remove_unit(self.game_map, self.cmd.source.get_unit_from_type(self.cmd.player, UnitType.SOLDIER))
        UnitManager.remove_unit(self.game_map, self.cmd.target.get_unit_from_type(self.cmd.enemy, UnitType.SOLDIER))
        self.cmd.target2.make_dead()
        self.machine.increment_action_count()

    def undo(self):
        pass


class TransportExec(Exec):
    def do(self):
        logging.info('stockpile TRANSPORTED from {} to {}'.format(self.cmd.source, self.cmd.target))
        UnitManager.move_stockpile(self.cmd.source, self.cmd.target)
        self.machine.increment_action_count()

    def undo(self):
        pass


class PassExec(Exec):
    def do(self):
        logging.info('player PASSED')
        self.machine.action_count = 0
        self.machine.set_state(Action.RESET)

    def undo(self):
        pass


class MilitarizeExec(Exec):
    def do(self):
        if self.cmd.target2:
            logging.info('player UPGRADED soldiers at {} and {}'.format(self.cmd.target, self.cmd.target2))
            UnitManager.upgrade_civ(self.game_map, self.cmd.target2.get_unit_from_type(self.cmd.player, UnitType.CIV))
            UnitManager.upgrade_civ(self.game_map, self.cmd.target.get_unit_from_type(self.cmd.player, UnitType.CIV))
        else:
            logging.info('player UPGRADED soldier at {}'.format(self.cmd.target))
            UnitManager.upgrade_civ(self.game_map, self.cmd.target.get_unit_from_type(self.cmd.player, UnitType.CIV))
        self.machine.set_state(Action.RESET)

    def undo(self):
        pass


