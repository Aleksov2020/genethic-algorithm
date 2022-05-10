import math
import random


class Drone:

    def __init__(self, N):
        self.x_vertex = 255
        self.y_vertex = 255
        self.color = (255, 0, 0)
        self.length_route = 0
        self.F = 0
        self.weight = 0
        self.chromosome = [i for i in range(N)]
        random.shuffle(self.chromosome)

    def move(self, x, y):
        #dont stay on one point
        if (self.x_vertex - x) + (self.y_vertex - y) == 0:
            self.length_route += 100000
        else:
            self.length_route += math.sqrt((self.x_vertex - x) ** 2 + (self.y_vertex - y) ** 2)
            self.x_vertex = x
            self.y_vertex = y

    def mutation(self):
        random.shuffle(self.chromosome)