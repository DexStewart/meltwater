import math
from Enums import *

from Shape import Shape

class UnitImage(Shape):
    def __init__(self, hex_center, tile_size, k):
        # Calculeaza coordonatele coltului opus centrului hexagonului pentru patratul inscris
        opposite = hex_center + tile_size / 2 * ((math.sqrt(3) - 1) * complex(math.cos(1 / 3 * math.pi), math.sin(1 / 3 * math.pi)) - 1) * complex(math.cos(-k / 2 * math.pi), math.sin(-k / 2 * math.pi))
        self.center = (hex_center + opposite) / 2
        if k == UnitDisplayType.CIV.value:
            self.vertices = [opposite, complex(hex_center.real, opposite.imag), hex_center, complex(opposite.real, hex_center.imag)]
        elif k == UnitDisplayType.SOLDIER.value:
            self.vertices = [complex(hex_center.real, opposite.imag), opposite, complex(opposite.real, hex_center.imag), hex_center]
        elif k == UnitDisplayType.STOCKPILE.value:
            self.vertices = [hex_center, complex(opposite.real, hex_center.imag), opposite, complex(hex_center.real, opposite.imag)]
        elif k == UnitDisplayType.NEUTRAL_CIV.value:
            self.vertices = [complex(opposite.real, hex_center.imag), hex_center, complex(hex_center.real, opposite.imag), opposite]
        else:
            raise RuntimeError("Bad index in map build")
