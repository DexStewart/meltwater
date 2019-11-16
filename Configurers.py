from UnitManager import *
from Hex import *
from Enums import *

# Configuratorii sunt functii. Le "ascunzi", ordonat, intr-o clasa si le faci statice (adica n-au self)
class Configurers:
    map_source = \
        [
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN,
             HexType.OCEAN,
             HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.ICE, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN,
             HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.ICE, HexType.OCEAN, HexType.OCEAN, HexType.SNOW, HexType.SNOW,
             HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.SNOW, HexType.ICE, HexType.ICE, HexType.SNOW, HexType.SNOW,
             HexType.SNOW, HexType.SNOW, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.SNOW, HexType.SNOW, HexType.ICE, HexType.SNOW, HexType.SNOW,
             HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.SNOW,
             HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.SNOW, HexType.SNOW, HexType.ICE, HexType.SNOW,
             HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.ICE, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.SNOW, HexType.ICE, HexType.ICE,
             HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.ICE,
             HexType.ICE, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN,
             HexType.OCEAN,
             HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN,
             HexType.OCEAN,
             HexType.OCEAN, HexType.SNOW, HexType.SNOW, HexType.SNOW, HexType.OCEAN, HexType.OCEAN],
            [HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN,
             HexType.OCEAN,
             HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN, HexType.OCEAN],
        ]
    @staticmethod
    def default_configuration(game_map, display):
        unit_list = [[1, 1, UnitType.CIV, Player.BLUE],
                     [2, 2, UnitType.CIV, Player.BLUE],
                     [2, 5, UnitType.CIV, Player.BLUE],
                     [4, 6, UnitType.CIV, Player.BLUE],
                     [5, 6, UnitType.CIV, Player.BLUE],
                     [6, 7, UnitType.CIV, Player.BLUE],
                     [8, 7, UnitType.CIV, Player.BLUE],
                     [8, 8, UnitType.CIV, Player.BLUE],
                     [9, 8, UnitType.CIV, Player.BLUE],
                     [9, 8, UnitType.CIV, Player.BLUE],
                     [5, 6, UnitType.SOLDIER, Player.BLUE],
                     [8, 7, UnitType.SOLDIER, Player.BLUE],
                     [3, 6, UnitType.CIV, Player.RED],
                     [3, 7, UnitType.CIV, Player.RED],
                     [4, 7, UnitType.CIV, Player.RED],
                     [4, 8, UnitType.CIV, Player.RED],
                     [5, 10, UnitType.CIV, Player.RED],
                     [7, 8, UnitType.CIV, Player.RED],
                     [7, 9, UnitType.CIV, Player.RED],
                     [7, 10, UnitType.CIV, Player.RED],
                     [8, 9, UnitType.CIV, Player.RED],
                     [8, 10, UnitType.CIV, Player.RED],
                     [8, 11, UnitType.CIV, Player.RED],
                     [4, 8, UnitType.SOLDIER, Player.RED],
                     [8, 9, UnitType.SOLDIER, Player.RED],
                     [2, 5, UnitType.CIV, Player.GREY],
                     [2, 6, UnitType.CIV, Player.GREY],
                     [3, 5, UnitType.CIV, Player.GREY],
                     [3, 7, UnitType.CIV, Player.GREY],
                     [4, 9, UnitType.CIV, Player.GREY],
                     [5, 10, UnitType.CIV, Player.GREY],
                     [7, 10, UnitType.CIV, Player.GREY],
                     [7, 10, UnitType.CIV, Player.GREY],
                     [8, 7, UnitType.CIV, Player.GREY],
                     [9, 11, UnitType.CIV, Player.GREY],
                     [10, 10, UnitType.CIV, Player.GREY]]
        Configurers.assemble_grid(game_map)
        Configurers.add_map_terrain(game_map)
        Configurers.add_initial_units(game_map, unit_list)
        Configurers.initial_contaminate(game_map)

    @staticmethod
    def add_initial_units(game_map, unit_list):
        list(map(lambda w: UnitManager.add_unit_by_coordinates(game_map, w), unit_list))

    @staticmethod
    def initial_contaminate(game_map):
        for k in game_map.direct_ref_matrix:
            for i in k:
                if i.hex_type == HexType.OCEAN:
                    continue
                else:
                    for j in i.adj.values():
                        if j:
                            if j.hex_type == HexType.OCEAN:
                                i.status = Status.CONTAMINATED
                                i.capacity -= 1
                                # print('contaminated hex {} {}'.format(i.y_coord, i.x_coord))   # this was here to report where activated
                                break

    @staticmethod
    def assemble_grid(game_map):
        for i in range(len(Configurers.map_source) - 1):
            Configurers.add_row(game_map)
        for i in range(len(Configurers.map_source) - 1):
            Configurers.add_column(game_map)

    @staticmethod
    def add_column(game_map):  # finds the east edge, then runs south adding a new column with proper linkage
        runner = game_map.origin
        while runner.adj["ne"]:
            runner = runner.adj["ne"]
        else:
            runner.adj["ne"] = Hex(game_map, runner.x_coord + 1, runner.y_coord)
            runner.adj["ne"].adj["sw"] = runner
            while runner.adj["sd"]:
                runner = runner.adj["sd"]
                runner.adj["ne"] = Hex(game_map, runner.x_coord + 1, runner.y_coord)
                runner.adj["ne"].adj["sw"] = runner
                runner.adj["nd"].adj["se"] = runner.adj["ne"]
                runner.adj["ne"].adj["nw"] = runner.adj["nd"]
                runner.adj["ne"].adj["nd"] = runner.adj["nd"].adj["ne"]
                runner.adj["nd"].adj["ne"].adj["sd"] = runner.adj["ne"]

    @staticmethod
    def add_row(game_map):  # finds the south edge, then runs east adding a new column with proper linkage
        runner = game_map.origin
        while runner.adj["sd"]:
            runner = runner.adj["sd"]
        else:
            runner.adj["sd"] = Hex(game_map, runner.x_coord, runner.y_coord + 1)
            runner.adj["sd"].adj["nd"] = runner
            while runner.adj["ne"]:
                runner = runner.adj["ne"]
                runner.adj["sd"] = Hex(game_map, runner.x_coord, runner.y_coord + 1)
                runner.adj["sd"].adj["nd"] = runner
                runner.adj["sw"].adj["se"] = runner.adj["sd"]
                runner.adj["sd"].adj["nw"] = runner.adj["sw"]
                runner.adj["sd"].adj["sw"] = runner.adj["sw"].adj["sd"]
                runner.adj["sw"].adj["sd"].adj["ne"] = runner.adj["sd"]

    @staticmethod
    def add_map_terrain(game_map):
        list(map(lambda w: list(map(lambda y: Configurers.set_terrain(y, Configurers.map_source[y.y_coord][y.x_coord]), w)), game_map.direct_ref_matrix))

    @staticmethod
    def set_terrain(tile, terrain_value):
        if terrain_value != HexType.OCEAN:
            tile.game_map.land_hex_list.append(tile)
            tile.status = Status.CLEAN
            if terrain_value == HexType.SNOW:
                tile.hex_type = HexType.SNOW
                tile.capacity = 2
            if terrain_value == HexType.ICE:
                tile.hex_type = HexType.ICE
                tile.capacity = 3
                #        print('{} {} {}'.format(self.x_coord, self.y_coord, terrain_value))

    @staticmethod
    def recommended_configuration(game_map, display):
        pass

    @staticmethod
    def fully_open_configuration(game_map, display):
        pass
