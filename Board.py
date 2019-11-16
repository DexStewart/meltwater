from tkinter import *
from Tile import *
from Handlers import *
from Enums import *
import math

class Board:
    bg_colours = {
        (HexType.SNOW, Status.CLEAN):"#ffffff",
        (HexType.SNOW, Status.CONTAMINATED):"#ffff00",
        (HexType.SNOW, Status.DEAD):"#444444",
        (HexType.ICE, Status.CLEAN):"#00ffff",
        (HexType.ICE, Status.CONTAMINATED):"#259fa8",
        (HexType.ICE, Status.DEAD):"#000000"}

    fg_colours = {Player.GREY:"#808080", Player.RED:"red", Player.BLUE:"blue"}

    def __init__(self, parent, x_origin, y_origin, tile_size, game_map):
        self.parent = parent
        self.tile_handler_map = {}
        self.unit_handler_map = {}
        self.game_map = game_map

        tile_text = StringVar(self.parent, 'None')
        tile_label = self.parent.create_text(150,150, font='Helvetica 20 bold', text=tile_text.get())
        unit_text = StringVar(self.parent, 'None')
        unit_label = self.parent.create_text(150,200, font='Helvetica 20 bold', text=tile_text.get())

        # Construieste imaginile hexagoanelor si unitatilor pe harta
        for i in range(12):
            for j in range(12):
                # Obtine informatia despre hexagon si unitatile din el
                data = game_map.get_unit(i, j)
                if data is not None:
                    # Calculeaza pozitia centrului hexagonului
                    tile_center = complex(x_origin, y_origin) + math.sqrt(3) / 2 * tile_size * (complex(0, i) + j*complex(math.cos(11 / 6 * math.pi), math.sin(11 / 6 * math.pi)))
                    # Creeaza obiectul pentru a calcula coordonatele colturilor hexagonului si campurilor pentru unitati
                    # Clasele Tile si UnitImage pot fi inlocuite prin functii sau formule scrise aici.
                    # Dupa construirea obiectelor in biblioteca nu mai sunt necesare
                    tile = Tile(tile_center, tile_size)
                    # Defineste hexagonul
                    tile_id = self.parent.create_polygon(tile.shape(), outline='blue', width=1)
                    # Adauga o inregistrare in dictionarul care leaga coordonatele de pe harta de identificatorii hexagoanelor
                    self.tile_handler_map[(i,j)] = tile_id
                    self.parent.tag_bind(tile_id, "<Button-1>", TileHandler(i, j, self.parent, tile_text, tile_label))
                    # Defineste unitatile
                    for k in range(4):
                        # Obtine coordonatele colturilor pentru a calcula dimensiunile campului de afisare
                        vertices = tile.get_unit(k).shape()
                        # Calculeaza latimea campului
                        field_width = abs(vertices[0] - vertices[4])
                        # Creeaza campul
                        unit_id = self.parent.create_text(vertices[0], vertices[1], font=("Monospaced Bold", field_width // 2), width=field_width, anchor=SW)
                        # Adauga o inregistrare in dictionarul care leaga coordonatele hartii de identificatorii imaginilor unitatilor
                        self.unit_handler_map[(i, j, k)] = unit_id
                        self.parent.tag_bind(unit_id, "<Button-1>", UnitImageHandler(i, j, k, self.parent, unit_text, unit_label))
                    # Afiseaza hexagonul si unitatile
                    self.set_tile_features(i, j)

    def set_tile_colour(self, i, j, colour):
        # Gaseste identificatorul
        id = self.tile_handler_map[(i,j)]
        # Coloreaza cu noua culoare
        self.parent.itemconfig(id, fill=colour)

    def set_unit_features(self, i, j, k, value, colour):
        # Gaseste identificatorul
        id = self.unit_handler_map[(i,j,k)]
        # Coloreaza cu noua culoare
        self.parent.itemconfig(id, fill=colour)
        # Scrie noul text
        self.parent.itemconfig(id, text=value)

    def set_tile_features(self, i, j):
        data = self.game_map.get_unit(i, j)
        values = data[0]
        tile_owner = data[1]
        tile_type = data[2]
        tile_status = data[3]
        # Defineste culoarea pentru hexagon
        self.set_tile_colour(i, j, Board.bg_colours[(tile_type, tile_status)])
        # Defineste valorile si culorile pentru unitati
        for k in range(4):
            if k == UnitDisplayType.CIV.value:
                foreground = Board.fg_colours[tile_owner]
            if k == UnitDisplayType.SOLDIER.value:
                foreground = Board.fg_colours[tile_owner]
            if k == UnitDisplayType.STOCKPILE.value:
                foreground = Board.fg_colours[Player.GREY]
            if k == UnitDisplayType.NEUTRAL_CIV.value:
                foreground = Board.fg_colours[Player.GREY]
            self.set_unit_features(i, j, k, str(values[k]), foreground)
