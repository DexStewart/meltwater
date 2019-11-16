class TileHandler:
    def __init__(self, i, j, parent, display, id):
        self.i = i
        self.j = j
        self.parent = parent
        self.display = display
        self.id = id

    def __call__(self, event):
        self.display.set(str(self.i) + ',' + str(self.j))
        self.parent.itemconfig(self.id, text=self.display.get())

class UnitImageHandler:
    def __init__(self, i, j, k, parent, display, id):
        self.i = i
        self.j = j
        self.k = k
        self.parent = parent
        self.display = display
        self.id = id

    def __call__(self, event):
        self.display.set(str(self.i) + ',' + str(self.j)+ ',' + str(self.k))
        self.parent.itemconfig(self.id, text=self.display.get())

class CommandEndHandler:
    def __init__(self, controller):
        self.controller = controller
