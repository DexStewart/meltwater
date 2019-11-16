class Shape:
    def shape(self):
        coord = []
        for x in self.vertices:
            coord.append(int(x.real))
            coord.append(int(x.imag))
        return coord

    def center(self):
        return self.center

    def get_vertex(self, i):
        return self.vertices[i]

    def set_vertex(self, i, x):
        self.vertices[i] = x
