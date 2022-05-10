class Target:

    def __init__(self, x, y, weight):
        self.x_vertex = x
        self.y_vertex = y
        self.weight = weight
        self.color = (0, 255, 0)

    def taken(self):
        self.color = (255, 255, 255)

    def reload(self):
        self.color = (0, 255, 0)