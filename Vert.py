import math


class Vert:

    def __init__(self):
        self.x_vertex = 0
        self.y_vertex = 0

    def length(self, x):
        return math.sqrt((self.x_vertex - x.x_vertex) ** 2 + (self.y_vertex - x.y_vertex) ** 2)