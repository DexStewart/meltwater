from copy import copy

import numpy as np

from Hex import *


class Map:
    doomsday_list = \
        [
            [[[5, 3], [5, 10]], [10, 10]],
            [[[4, 2], [3, 8]], [5, 10]],
            [[[3, 2], [7, 5]], [2, 2]],
            [[[1, 1], [6, 10]], [10, 9]],
            [[[5, 3], [2, 5]], [1, 1]],
            [[[5, 3], [10, 9]], [3, 8]],
            [[[3, 2], [10, 10]], [5, 10]],
            [[[1, 1], [10, 10]], [10, 8]],
            [[[3, 8], [8, 6]], [3, 3]],
            [[[7, 5], [10, 9]], [10, 8]],
            [[[7, 4], [6, 10]], [4, 9]],
            [[[6, 3], [3, 5]], [1, 1]],
            [[[3, 4], [8, 6]], [2, 2]],
            [[[3, 5], [10, 10]], [3, 2]],
            [[[7, 4], [2, 6]], [1, 1]],
            [[[6, 3], [7, 10]], [3, 8]],
            [[[3, 3], [9, 11]], [10, 9]],
            [[[2, 6], [9, 10]], [10, 8]],
            [[[10, 8], [8, 11]], [4, 9]],
            [[[6, 3], [3, 7]], [5, 10]],
            [[[4, 9], [8, 11]], [10, 10]],
            [[[2, 5], [9, 11]], [1, 1]],
            [[[5, 10], [10, 8]], [10, 10]],
            [[[3, 3], [9, 7]], [10, 9]],
            [[[5, 3], [7, 10]], [4, 9]],
            [[[3, 4], [4, 9]], [3, 8]],
            [[[7, 4], [3, 7]], [3, 2]],
            [[[4, 2], [9, 7]], [2, 2]],
        ]

    def __init__(self):
        self.count_red = 0
        self.count_blue = 0
        self.doomsday_stack = copy(Map.doomsday_list)
        # shuffle(self.doomsday_stack)
        self.doomsday_track = 0
        self.direct_ref_matrix = []
        self.unit_dict = {}             # this might need to be somewhere else
        self.unit_list = []             # 99% not necessary
        self.sc_dict = {}               # this might need to be somwhere else also
        self.sc_list = []               # 99% not necessary
        self.land_hex_list = []         # 99% yes necessary
        self.hexes_with_units = []      # *maybe* useful for alternate supply check. Otherwise garbage
        self.unresolved_hexes = []
        self.origin = Hex(self, 0, 0)

    def __repr__(self):        # exclusively prints hex capacity matrix. Also cheats.
        capacity_matrix = []
        for i in range(len(self.direct_ref_matrix)):
            capacity_matrix.append([])
            for j in range(len(self.direct_ref_matrix[i])):
                capacity_matrix[i].append(self.direct_ref_matrix[i][j].capacity)
        return str(np.matrix(capacity_matrix))

    def get_unit(self, i, j):
        tile = self.direct_ref_matrix[i][j]
        if tile.hex_type == HexType.OCEAN:
            return None
        else:
            owner = Player.GREY
            hex_type = tile.hex_type
            status = tile.status
            unit_data = [0, 0, 0, 0]
            unit_data[UnitDisplayType.STOCKPILE.value] = len(tile.cargo_sc)
            for unit in tile.cargo:
                if unit.owner == Player.GREY:
                    unit_data[UnitDisplayType.NEUTRAL_CIV.value] += 1
                else:
                    if unit.unit_type == UnitType.SOLDIER:
                        unit_data[UnitDisplayType.SOLDIER.value] += 1
                    else:
                        unit_data[UnitDisplayType.CIV.value] += 1
                    owner = unit.owner
            return unit_data, owner, hex_type, status

    def det_starvation_action(self, tile):
        if self.must_flee(tile):
            return Command.FLEE
        elif self.must_defect(tile):
            return Command.DEFECT
        else:
            return Command.DIE

    def must_flee(self, tile):
        adj_owners = {
            Player.BLUE: False,
            Player.RED: False,
            Player.GREY: False
        }
        for i in tile.adj.values():
            if i:
                if 0 < len(i.cargo) < i.capacity:
                    adj_owners[i.owner] = True
        for i in tile.cargo:
            if adj_owners[i.owner]:
                return True
        return False

    def must_defect(self, tile):
        adj_owners = {
            Player.BLUE: False,
            Player.RED: False,
            Player.GREY: False
        }
        flag = False
        for i in tile.adj.values():
            if 0 < len(i.cargo) < i.capacity:
                adj_owners[i.owner] = True
                flag = True
        for i in tile.cargo:
            if adj_owners[i.owner]:
                return False
        if flag:
            return True
        return False

    def must_die(self, tile):
        for i in tile.adj.values():
            if 0 < len(tile.cargo) < tile.capacity:
                return False
        return True

    def refresh_unresolved_hexes(self):
        self.unresolved_hexes = []
        for i in self.hexes_with_units:
            if i.capacity < len(i.cargo):
                self.unresolved_hexes.append(i)


    def unresolved_hexes_exist(self):
        self.refresh_unresolved_hexes()
        if len(self.unresolved_hexes) > 0:
            return True
        else:
            return False

    def encode_double(self, h):
        y = h.y_coord
        x = h.x_coord
        return [y*2 + 4 - x, x]

    def decode_double(self, h):
        return self.direct_ref_matrix[(h[0] + h[1] - 4)//2][h[1]]

    def encode_chess(self, h):
        if h.hex_type == HexType.OCEAN:
            # logging.warning('no chess notation for ocean')
            return
        y = h.y_coord
        x = h.x_coord
        hex_name = ''
        y += 2 - x // 2 - x % 2
        x += ord('a') - 1
        hex_name += chr(x)
        hex_name += str(y)
        return hex_name

    def decode_chess(self, hex_name):
        if hex_name == 'XX':
            return Hex(self, 0, 0, fake=True)
        x_code = hex_name[0]
        y_code = hex_name[1]
        x = (ord(x_code) - ord('A')) % 26 + 1
        y = ord(y_code) - ord('0')
        y = y - 2 + x // 2 + x % 2
        return self.direct_ref_matrix[y][x]

    def find_nearest_contaminated(self, origin_list, identifier=None):
        if not identifier:
            identifier = str(uuid.uuid4())  # generate unique query identifier to mark nodes
        neighbour_list = []
        success_list = []
        if isinstance(origin_list, Hex):
            origin_list = [origin_list]
        for i in origin_list:
            for j in i.adj.values():
                if not j.last_search_id == identifier and not j.hex_type == HexType.OCEAN:
                    neighbour_list.append(j)
                    j.last_search_id = identifier
            if i.status == Status.CONTAMINATED:
                success_list.append(i)
        if success_list:
            return success_list
        return self.find_nearest_contaminated(neighbour_list, identifier)

    @staticmethod
    def check_adjacent(hex1, hex2):
        x_diff = hex1.x_coord - hex2.x_coord
        y_diff = hex1.y_coord - hex2.y_coord
        if abs(x_diff) < 2 and abs(y_diff) < 2 and x_diff + y_diff != 0:
            return True
        else:
            return False


