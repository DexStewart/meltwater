from tkinter import *
from tkinter import ttk
from Board import Board

class Display:
    def __init__(self, game_map, root):
        self.root = root
        self.game_map = game_map

        # Calculeaza factori de scalare pe x si y
        ref_width = 1536
        ref_height = 864
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_scale = screen_width / ref_width
        y_scale = screen_height / ref_height

        ## Calculeaza dimensiunile cadrului
        ref_frame_width = 1129
        ref_frame_height = 843
        frame_width = int(ref_frame_width * x_scale)
        frame_height = int(ref_frame_height * y_scale)

        # Calculeaza coordonatele originii hartii
        ref_x_origin = 355
        ref_y_origin = 278
        x_origin = ref_x_origin * x_scale
        y_origin = ref_y_origin * y_scale

        # Calculeaza dimensiunea hexagonului
        ref_tile_size = 53.4
        tile_size = ref_tile_size * x_scale

        # Defineste cadrul si geometria
        mainframe = ttk.Frame(root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Defineste "panza"
        can = Canvas(mainframe, width=frame_width, height=frame_height, bg="blue")
        can.pack()

        # Defineste harta
        self.board = Board(can, x_origin, y_origin, tile_size, self.game_map)

    def update(self, tiles):
        for t in tiles:
            self.board.set_tile_features(t[0], t[1])
