import uuid
from Enums import *
from UnitManager import Unit, UnitManager

class Hex:

    def __init__(self, game_map, x_coord, y_coord, fake=False):  # the default hex is ocean and dead
        self.display = None
        self.fake = fake
        self.game_map = game_map
        self.cargo = []
        self.cargo_sc = []
        self._owner = Player.GREY
        self._sc_bonus = False
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.hex_type = HexType.OCEAN
        self.status = Status.DEAD
        self.capacity = 0
        self.last_search_id = None  # to be used as flag during tree search
        self.adj = {
            "ne": None,
            "nd": None,
            "nw": None,
            "sw": None,
            "sd": None,
            "se": None
        }
        self.stack_size = {
            Player.BLUE: 0,
            Player.RED: 0,
            Player.GREY: 0
        }
        self.soldier_zoc = {
            Player.BLUE: False,
            Player.RED: False
        }
        self.soldier_zoc_origin = {
            Player.BLUE: [],
            Player.RED: []
        }
        self.sc_zoc = {
            Player.BLUE:False,
            Player.RED:False
        }
        self.sc_zoc_origin = {
            Player.BLUE: [],
            Player.RED: []
        }

        self.sc_bonus_origin = []

        if self.x_coord == 0:
            game_map.direct_ref_matrix.append([self])
        else:
            game_map.direct_ref_matrix[y_coord].append(self)
            # print('{} {}'.format(self.x_coord, self.y_coord))

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if self._owner is not Player.GREY and self.cargo_sc:
            for i in self.cargo_sc:
                for j in self.adj.values():
                    j.remove_sc_zoc_instance(i)
        self._owner = value
        if self._owner is not Player.GREY and self.cargo_sc:
            for i in self.cargo_sc:
                for j in self.adj.values():
                    j.add_sc_zoc_instance(i)

    @property
    def sc_bonus(self):
        return self._sc_bonus

    @sc_bonus.setter
    def sc_bonus(self, value):
        if self.sc_bonus:
            self.capacity -= 1
        if value:
            self.capacity += 1
        self._sc_bonus = value

    # def update_self(self):
    #     self.display.update([[self.y_coord, self.x_coord]])

    def determine_sc_bonus(self):   # to be called after any move or transport or death
        if self.status is Status.DEAD:
            self.sc_bonus = False
        elif self.cargo_sc:
            self.sc_bonus = True
        elif self.owner is not Player.GREY and self.sc_zoc[self.owner]:
            self.sc_bonus = True
        else:
            self.sc_bonus = False

    def __len__(self):
        if self.fake:
            return False
        else:
            return True

    def __repr__(self):
        x = '{} {}  '.format(self.y_coord, self.x_coord) + self.game_map.encode_chess(self)
        return x
        # return '{} {}'.format(self.y_coord, self.x_coord)

    def make_dead(self):
        self.status = Status.DEAD
        # self.update_self()
        self.capacity = -1
        for i in self.adj.values():
            if i.status == Status.CLEAN:
                i.status = Status.CONTAMINATED
                i.capacity -= 1
                # i.update_self()

    def add_soldier_zoc_instance(self, unit):
        if unit.tile not in self.adj.values():
            raise RuntimeError('failed to add Soldier ZOC instance; {} not adjacent to {}'.format(unit, self))
        if not self.soldier_zoc[unit.owner]:
            self.soldier_zoc[unit.owner] = True
        self.soldier_zoc_origin[unit.owner].append(unit)

    def remove_soldier_zoc_instance(self, unit):
        if unit.tile not in self.adj.values():
            raise RuntimeError('failed to remove Soldier ZOC instance; {} not adjacent to {}'.format(unit, self))
        self.soldier_zoc_origin[unit.owner].remove(unit)
        if not self.soldier_zoc_origin[unit.owner]:
            self.soldier_zoc[unit.owner] = False

    def add_sc_zoc_instance(self, sc):
        if sc.tile not in self.adj.values():
            raise RuntimeError('failed to add SC ZOC instance; {} not adjacent to {}'.format(sc, self))
        if not self.sc_zoc[sc.tile.owner]:
            self.sc_zoc[sc.tile.owner] = True
        self.sc_zoc_origin[sc.tile.owner].append(sc)
        self.determine_sc_bonus()

    def remove_sc_zoc_instance(self, sc):
        if sc.tile not in self.adj.values():
            raise RuntimeError('failed to remove SC ZOC instance; {} not adjacent to {}'.format(sc, self))
        self.sc_zoc_origin[sc.tile.owner].remove(sc)
        if not self.sc_zoc_origin[sc.tile.owner]:
            self.sc_zoc[sc.tile.owner] = False
        self.determine_sc_bonus()

    def get_unit_from_type(self, unit_owner, unit_type):
        for i in self.cargo:
            if i.unit_type == unit_type and i.owner == unit_owner:
                return i

    def get_units_from_notation(self, unit_set):
        if isinstance(unit_set, str):
            unit = unit_set
            if unit == 'sc':
                if self.cargo_sc:
                    return self.cargo_sc[0]
                else:
                    return False
            if unit[0] == 'r' or unit[0] == 'R':
                unit_owner = Player.RED
            elif unit[0] == 'b' or unit[0] == 'B':
                unit_owner = Player.BLUE
            elif unit[0] == 'g' or unit[0] == 'G':
                unit_owner = Player.GREY
            else:
                return False
            if unit[1] == 'c' or unit[1] == 'C':
                unit_type = UnitType.CIV
            elif unit[1] == 's' or unit[1] == 'S':
                unit_type = UnitType.SOLDIER
            else:
                return False
            for i in self.cargo:
                if i.unit_type == unit_type and i.owner == unit_owner:
                    return [i]
            return False
        else:
            assert isinstance(unit_set, list)
            unit_hits = []
            for unit in unit_set:
                assert isinstance(unit, str)
                hit_flag = False
                if unit[0] == 'r' or unit[0] == 'R':
                    unit_owner = Player.RED
                elif unit[0] == 'b' or unit[0] == 'B':
                    unit_owner = Player.BLUE
                elif unit[0] == 'g' or unit[0] == 'G':
                    unit_owner = Player.GREY
                else:
                    return False
                if unit[1] == 'c' or unit[1] == 'C':
                    unit_type = UnitType.CIV
                elif unit[1] == 's' or unit[1] == 'S':
                    unit_type = UnitType.SOLDIER
                else:
                    return False
                for i in self.cargo:
                    if i.unit_type == unit_type and i.owner == unit_owner and i not in unit_hits and not hit_flag:
                        unit_hits.append(i)
                        hit_flag = True
                if not hit_flag:
                    return False
            return unit_hits

    def determine_owner(self):
        old_owner = self.owner
        new_owner = None
        if self.stack_size[Player.BLUE]:
            new_owner = Player.BLUE
        elif self.stack_size[Player.RED]:
            new_owner = Player.RED
        else:
            new_owner = Player.GREY
        sc_temp_list = []
        if old_owner is not new_owner:
            for i in self.adj.values():
                for j in i.cargo_sc:
                    sc_temp_list.append(j)
                    UnitManager.remove_sc_zoc(j)
        self.owner = new_owner
        for i in sc_temp_list:
            UnitManager.add_sc_zoc(i)

    def determine_starvation_state(self):
        flee_flag = False
        defect_flag = False
        for i in self.cargo:
            for j in self.adj.values():
                if 0 < len(j.cargo) < j.capacity:
                    if j.stack_size[i.owner]:
                        flee_flag = True
                    else:
                        defect_flag = True
        if flee_flag:
            return ClockState.FLEE
        elif defect_flag:
            return ClockState.DEFECT
        else:
            return ClockState.DIE
