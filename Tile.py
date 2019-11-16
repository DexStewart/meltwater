import math
from Shape import Shape
from UnitImage import UnitImage
class Tile(Shape):
    def __init__(self, center, tile_size):
        self.center = center
        self.vertices = [self.center + tile_size / 2 * complex(math.cos(i / 3 * math.pi), math.sin(i / 3 * math.pi)) for i in range(6)]
        self.units = [UnitImage(center, tile_size, k) for k in range(4)]

    def get_unit(self, k):
        return self.units[k]

