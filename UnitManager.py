import logging
import uuid
from Enums import *
from Hex import *


class UnitManager:

    @staticmethod
    def add_unit(game_map, unit_data):  # given single unit [tile, type, owner], adds to map
        tile = unit_data[0]
        unit_owner = unit_data[2]
        unit_id = str(uuid.uuid4())
        if (unit_owner == Player.GREY or unit_owner == tile.owner or tile.owner == Player.GREY) and tile.status != Status.DEAD:
            if unit_owner == Player.RED: game_map.count_red += 1
            if unit_owner == Player.BLUE: game_map.count_blue += 1
            unit = Unit(unit_data[1], unit_data[2], tile)
            game_map.unit_dict[unit_id] = unit
            if not tile.cargo:
                game_map.hexes_with_units.append(tile)
            tile.cargo.append(unit)
            if unit_owner != Player.GREY and tile.owner == Player.GREY:
                tile.owner = unit.owner
            game_map.unit_list.append(unit)
            if unit_data[1] == UnitType.SOLDIER:
                UnitManager.add_stockpile(game_map, tile)
                tile.stack_size[unit_owner] += 10
            else:
                tile.stack_size[unit_owner] += 1
            tile.determine_sc_bonus()
            # tile.update_self()
            return True
        else:
            logging.error('cannot add unit')
            return False

    @staticmethod
    def add_unit_by_coordinates(game_map, unit_data):  # given single unit [y coord, x coord, type, owner], adds to map
        tile = game_map.direct_ref_matrix[unit_data[0]][unit_data[1]]
        unit_owner = unit_data[3]
        unit_id = str(uuid.uuid4())
        if (unit_owner == Player.GREY or unit_owner == tile.owner or tile.owner == Player.GREY) and tile.status != Status.DEAD:
            if unit_owner == Player.RED: game_map.count_red += 1
            if unit_owner == Player.BLUE: game_map.count_blue += 1
            unit = Unit(unit_data[2], unit_data[3], tile)
            game_map.unit_dict[unit_id] = unit
            if not tile.cargo:
                game_map.hexes_with_units.append(tile)
            tile.cargo.append(unit)
            if unit_owner != Player.GREY and tile.owner == Player.GREY:
                tile.owner = unit.owner
            game_map.unit_list.append(unit)
            if unit_data[2] == UnitType.SOLDIER:
                UnitManager.add_stockpile(game_map, tile)
                tile.stack_size[unit_owner] += 10
                UnitManager.add_soldier_zoc(unit)
            else:
                tile.stack_size[unit_owner] += 1
            tile.determine_sc_bonus()
            return True
        else:
            logging.warning('error cannot add unit')
            return False

    @staticmethod
    def move_unit_out(game_map, unit):
        unit.tile.cargo.remove(unit)
        # unit.tile.update_self()
        if unit.unit_type == UnitType.SOLDIER:
            unit.tile.stack_size[unit.owner] -= 10
            UnitManager.remove_soldier_zoc(unit)
        else:
            unit.tile.stack_size[unit.owner] -= 1
        if not unit.tile.cargo:
            game_map.hexes_with_units.remove(unit.tile)
        if not unit.tile.stack_size[unit.owner] and unit.owner is not Player.GREY:
            unit.tile.owner = Player.GREY
            if unit.tile.sc_bonus_origin:
                unit.tile.sc_bonus_origin = []
                if unit.tile.cargo_sc:
                    for i in unit.tile.cargo_sc:
                        unit.tile.sc_bonus_origin.append(i)
                else:
                    unit.tile.sc_bonus = False
                    unit.tile.capacity -= 1

    @staticmethod
    def move_unit_in(game_map, unit, target):
        unit.tile = target
        if not target.cargo:
            game_map.hexes_with_units.append(target)
        target.cargo.append(unit)
        # unit.tile.update_self()
        flag = False
        if not unit.tile.stack_size[unit.owner] and unit.owner is not Player.GREY:
            flag = True
        if unit.unit_type == UnitType.SOLDIER:
            unit.tile.stack_size[unit.owner] += 10
            UnitManager.add_soldier_zoc(unit)
        else:
            unit.tile.stack_size[unit.owner] += 1
        if flag and unit.tile.status is not Status.DEAD:
            unit.tile.owner = unit.owner
            if unit.tile.cargo_sc:
                for i in unit.tile.cargo_sc:
                    UnitManager.add_sc_zoc(i)
                for i in unit.tile.adj.values():
                    if unit.tile.owner is i.owner:
                        for j in i.cargo_sc:
                            if not unit.tile.sc_bonus:
                                unit.tile.sc_bonus = True
                            unit.tile.sc_bonus_origin.append(j)

    @staticmethod
    def move_unit(game_map, unit, target):
        assert target in unit.tile.adj.values() and target.owner is not unit.enemy
        source = unit.tile
        UnitManager.move_unit_out(game_map, unit)
        UnitManager.move_unit_in(game_map, unit, target)
        source.determine_sc_bonus()
        target.determine_sc_bonus()

    @staticmethod
    def defect_unit(game_map, unit, target):
        source = unit.tile
        UnitManager.move_unit_out(game_map, unit)
        unit.owner = target.owner
        if unit.unit_type == UnitType.SOLDIER:
            unit.unit_type = UnitType.CIV
        UnitManager.move_unit_in(game_map, unit, target)
        source.determine_sc_bonus()
        target.determine_sc_bonus()

    @staticmethod
    def upgrade_civ(game_map, unit):
        logging.info('civ at {} being upgraded'.format(unit.tile))
        unit.unit_type = UnitType.SOLDIER
        UnitManager.add_soldier_zoc(unit)
        unit.tile.stack_size[unit.owner] += 9
        # unit.tile.update_self()

    @staticmethod
    def remove_unit(game_map, unit):
        logging.info('unit {} at {} being removed'.format(unit, unit.tile))
        if unit.unit_type == UnitType.SOLDIER:
            unit.tile.stack_size[unit.owner] -= 10
            UnitManager.remove_soldier_zoc(unit)
        else:
            unit.tile.stack_size[unit.owner] -= 1
        unit.tile.cargo.remove(unit)
        # unit.tile.update_self()
        if not unit.tile.stack_size[unit.owner]:
            unit.tile.determine_owner()
        if not unit.tile.cargo:
            game_map.hexes_with_units.remove(unit.tile)
        unit.tile.determine_sc_bonus()

    @staticmethod
    def add_stockpile(game_map, tile):
        kappa = Stockpile(tile)
        sc_id = str(uuid.uuid4())
        game_map.sc_dict[sc_id] = kappa
        tile.cargo_sc.append(kappa)
        game_map.sc_list.append(kappa)
        tile.determine_sc_bonus()

    @staticmethod
    def move_stockpile(source, target):
        assert target in source.adj.values() and target.owner == source.owner, "failed to move sc"
        stockpile = source.cargo_sc[0]
        UnitManager.remove_sc_zoc(stockpile)
        # UnitManager.remove_local(stockpile)
        source.cargo_sc.remove(stockpile)
        target.cargo_sc.append(stockpile)
        stockpile.tile = target
        # UnitManager.add_local(stockpile)
        UnitManager.add_sc_zoc(stockpile)
        source.determine_sc_bonus()
        target.determine_sc_bonus()
        # source.update_self()
        # target.update_self()
        logging.info('sc moved to {}'.format(stockpile.tile))
    
    # @staticmethod
    # def add_local(stockpile):
    #     if stockpile.tile.status != Status.DEAD:
    #         if not stockpile.tile.sc_bonus_origin:
    #             stockpile.tile.capacity += 1
    #         stockpile.tile.sc_bonus_origin.append(stockpile)
    #
    # @staticmethod
    # def remove_local(stockpile):                 # when called while tile is being made dead, must be called before DEAD designation. local influence will never be added in the first place to a dead tile
    #     if stockpile.tile.status != Status.DEAD:
    #         if stockpile in stockpile.tile.sc_bonus_origin:            # sanity check. Probably pointless
    #             stockpile.tile.capacity -= 1
    #             stockpile.tile.sc_bonus_origin.remove(stockpile)

    @staticmethod
    def add_soldier_zoc(soldier):
        for i in soldier.tile.adj.values():
            i.add_soldier_zoc_instance(soldier)

    @staticmethod
    def remove_soldier_zoc(soldier):
        for i in soldier.tile.adj.values():
            i.remove_soldier_zoc_instance(soldier)

    @staticmethod
    def add_sc_zoc(stockpile):
        if stockpile.tile.owner is not Player.GREY:      # ZOC only applies if SC is factional. This might be skipped if we're selective about calling the function. It's also a good sanity check tho
            for i in stockpile.tile.adj.values():
                i.add_sc_zoc_instance(stockpile)
        else:
            logging.warning('sc zoc addition does not apply')

    @staticmethod
    def remove_sc_zoc(stockpile):
        for i in stockpile.tile.adj.values():
            i.remove_sc_zoc_instance(stockpile)


class Unit:
    def __init__(self, unit_type, owner, tile):
        self.unit_type = unit_type
        self.owner = owner
        self.tile = tile
        self.game_map = self.tile.game_map
        if self.owner == Player.BLUE:
            self.enemy = Player.RED
        elif self.owner == Player.RED:
            self.enemy = Player.BLUE
        else:
            self.enemy = None

    def __repr__(self):
        return '{} {} {}'.format(self.owner.name, self.unit_type.name, self.tile)


class Stockpile:
    def __init__(self, tile):
        self.tile = tile
        self.game_map = self.tile.game_map
        self.owner = Player.GREY
        # UnitManager.add_local(self)
        UnitManager.add_sc_zoc(self)

    def __repr__(self):
        return 'stockpile at {}'.format(self.tile)