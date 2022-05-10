import random
import time
import pygame
import sys

import Target
import Base
import Drone
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QCheckBox,
                             QApplication, QLabel, QTableWidget, QTableWidgetItem)


POPULATION = 200
ver_population = 180
RANDOME_POPULATION = 50

min_length_route = 0
count_gen = 0

class GeneticAlgorithm(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # define table
        self.table = QTableWidget(self)
        self.table.setGeometry(20, 60, 317, 420)
        self.table.setColumnCount(3)
        self.table.setRowCount(1)

        self.table.setHorizontalHeaderLabels(["X coordinates", "Y coordinates", "Point weight"])

        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)

        # Button Start
        self.btns = QPushButton('Start', self)
        self.btns.move(20, 20)
        self.btns.clicked.connect(self.start)

        # Button Add
        self.btna = QPushButton('Add Point', self)
        self.btna.move(100, 20)
        self.btna.clicked.connect(self.add_row)

        # Button delete
        self.btna = QPushButton('Delete Point', self)
        self.btna.move(180, 20)
        self.btna.clicked.connect(self.del_row)

        # Button random
        self.btna = QPushButton('Random', self)
        self.btna.move(260, 20)
        self.btna.clicked.connect(self.random)

        # Resut
        self.rlab = QLabel("Result: ", self)
        self.rlab.move(400, 30)

        # Checkbox
        self.dlab = QLabel("View Process", self)
        self.dlab.move(500, 10)
        self.dop = QCheckBox(self)
        self.dop.setChecked(False)
        self.dop.move(600, 10)
        self.dop.stateChanged.connect(self.view_additional)

        # Additional Field
        self.dopf = QTextEdit(self)
        self.dopf.setGeometry(400, 60, 0, 0)

        self.res = QTextEdit(self)
        self.res.setGeometry(400, 60, 580, 420)
        self.res.setAlignment(QtCore.Qt.AlignCenter)

        self.setGeometry(500, 100, 1000, 500)
        self.setWindowTitle('GeneticAlgorithm')
        self.show()

    def view_additional(self, state):

        if state == False:
            self.res.setGeometry(400, 60, 580, 420)
            self.dopf.setGeometry(400, 60, 0, 0)
        else:
            self.res.setGeometry(400, 60, 580, 180)
            self.dopf.setGeometry(400, 270, 580, 210)

    def start(self):
        rows = self.table.rowCount()
        vertexes = []
        flag = False
        for row in range(rows):
            try:
                vertexes.append([
                    int(self.table.item(row, 0).text()),
                    int(self.table.item(row, 1).text()),
                    int(self.table.item(row, 2).text())
                ])
            except:
                flag = True

        if flag:
            result = "Проверьте правильность введенных данных! \nКоординаты точек должны быть целыми числами."
        else:
            print(1);
            result = self.GA(vertexes, rows)

        self.res.setText(result)

    def add_row(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)

    def del_row(self):
        rowPosition = self.table.rowCount() - 1
        self.table.removeRow(rowPosition)

    def random(self):
        for i in range(0, 7):
            self.table.setItem(i, 0, QTableWidgetItem(str(random.randint(0, 500))))
            self.table.setItem(i, 1, QTableWidgetItem(str(random.randint(0, 500))))
            self.table.setItem(i, 2, QTableWidgetItem(str(random.randint(1, 5))))

            self.add_row()

        self.table.setItem(7, 0, QTableWidgetItem(str(random.randint(0, 500))))
        self.table.setItem(7, 1, QTableWidgetItem(str(random.randint(0, 500))))
        self.table.setItem(7, 2, QTableWidgetItem(str(random.randint(1, 5))))

    def GA(self, vertexes, N):
        TARGET_NUM = N
        target_list = []
        checked = True

        for i in range(TARGET_NUM):
            a = Target.Target(int(vertexes[i][0]), int(vertexes[i][1]), int(vertexes[i][2]))
            target_list.append(a)

        base = Base.Base()

        drone_list = []
        for i in range(POPULATION):
            drone = Drone.Drone(N)
            drone_list.append(drone)

        # run process
        pygame.init()

        # Set up the drawing window
        screen = pygame.display.set_mode([500, 615])
        bg = pygame.image.load("C:/778.jpg")

        running = True
        step = 0
        gen = 0
        step_null = False
        while running:

            # INSIDE OF THE GAME LOOP
            screen.blit(bg, (0, 0))

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # drone go home
            #if step % 4 == 0:
                #new_x_vertex = base.x_vertex
                #new_y_vertex = base.y_vertex
                #drone_list[i].move(new_x_vertex, new_y_vertex)

            # check mass
            for i in range(0, N):
                if drone_list[i].weight > 5:
                    drone_list[i].length_route += 10000

            # null mass
            if step != 0:
                if drone_list[i].x_vertex == base.x_vertex and drone_list[i].y_vertex == base.y_vertex :
                    drone.weight = 0

            # Draw a solid black point. This is our base
            pygame.draw.circle(screen, base.color, (base.x_vertex, base.y_vertex), 10)

            # find tagrets
            for i in range(POPULATION):
                target_index = drone_list[i].chromosome[step]
                new_x_vertex = target_list[target_index].x_vertex
                new_y_vertex = target_list[target_index].y_vertex
                drone_list[i].move(new_x_vertex, new_y_vertex)
                target_list[target_index].taken()

            # new gen
            if step == TARGET_NUM - 1:
                step_null = True
                gen += 1
                step = 0
                min_ = 10000000
                sum_ = 0
                min_num = 0

                # find min route to print
                for i in range(POPULATION):
                    if drone_list[i].length_route < min_:
                        min_ = drone_list[i].length_route
                        min_num = i

                for i in range(TARGET_NUM):
                    target_list[i].reload()

                for i in range(TARGET_NUM):
                    pygame.draw.circle(
                        screen,
                        target_list[i].color,
                        (target_list[i].x_vertex, target_list[i].y_vertex),
                        5)

                    f1 = pygame.font.Font(None, 22)
                    text1 = f1.render(str(target_list[i].weight), 1, (0, 0, 0))

                    screen.blit(text1, (target_list[i].x_vertex + 5, target_list[i].y_vertex - 10))

                pygame.draw.line(screen, (0, 0, 0),
                                 (base.x_vertex,
                                  base.y_vertex),
                                 (target_list[drone_list[min_num].chromosome[0]].x_vertex,
                                  target_list[drone_list[min_num].chromosome[0]].y_vertex),
                                 2)
                for i in range(TARGET_NUM - 1):
                    if i % 3 == 0 and i != 0:
                        pygame.draw.line(screen, (0, 0, 0),
                                         (target_list[drone_list[min_num].chromosome[i]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i]].y_vertex),
                                         (base.x_vertex,
                                          base.y_vertex),
                                         2)
                        pygame.draw.line(screen, (0, 0, 0),
                                         (base.x_vertex,
                                          base.y_vertex),
                                         (target_list[drone_list[min_num].chromosome[i + 1]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i + 1]].y_vertex),
                                         2)
                    else:
                        pygame.draw.line(screen, (255, 0, 0),
                                         (target_list[drone_list[min_num].chromosome[i]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i]].y_vertex),
                                         (target_list[drone_list[min_num].chromosome[i + 1]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i + 1]].y_vertex),
                                         2)
                    pygame.display.flip()

                pygame.draw.line(screen, (0, 0, 0),
                                 (target_list[drone_list[min_num].chromosome[TARGET_NUM - 1]].x_vertex,
                                  target_list[drone_list[min_num].chromosome[TARGET_NUM - 1]].y_vertex),
                                 (base.x_vertex,
                                  base.y_vertex),
                                 2)
                pygame.display.flip()
                # time.sleep(3)
                # find sum of result F
                for i in range(POPULATION):
                    drone_list[i].F = 1 / drone_list[i].length_route * 100000
                    sum_ += drone_list[i].F

                list_ver = []
                for i in range(POPULATION):
                    list_ver.append(drone_list[i].F / sum_)

                roulette = [0]
                for i in range(1, POPULATION):
                    roulette.append(list_ver[i] + roulette[i - 1])

                new_drones = []
                a = Drone.Drone(N)
                a.chromosome = list(drone_list[min_num].chromosome)
                new_drones.append(a)
                # childs with roulette
                for i in range(1, POPULATION):
                    a = Drone.Drone(N)
                    child_ = random.random()
                    child_num = 0
                    for j in range(1, POPULATION):
                        if roulette[j] > child_:
                            child_num = j - 1
                            break
                    a.chromosome = list(drone_list[child_num].chromosome)
                    new_drones.append(a)

                drone_list = list(new_drones)

                # mutation
                for i in range(1, POPULATION - RANDOME_POPULATION):
                    if random.randint(1, 200) < ver_population:
                        a_v = random.randint(0, TARGET_NUM - 1)
                        b_v = random.randint(0, TARGET_NUM - 1)
                        temp = drone_list[i].chromosome[b_v]
                        drone_list[i].chromosome[b_v] = drone_list[i].chromosome[a_v]
                        drone_list[i].chromosome[a_v] = temp

                for i in range(POPULATION - RANDOME_POPULATION, POPULATION):
                    drone_list[i].mutation()

                # reload target_list
                for i in range(TARGET_NUM):
                    target_list[i].reload()

                global min_length_route
                global count_gen

                if gen > 2 and min_length_route != min_:
                    min_length_route = min_
                    count_gen = 0
                elif (gen > 2):
                    count_gen += 1

                if count_gen == 30:
                    time.sleep(5)
                    file = open("result.txt", "w")
                    result = "Итоговый маршрут состоит из следующих точек: \n"

                    for point in drone_list[i].chromosome:
                        result += str(point + 1) + " "

                    result += ". \nИтоговая длина минимального маршрута = " + str(min_length_route)

                    file.write(result)
                    time.sleep(30)
                    running = False
            if (count_gen != 0) and checked:
                checked = False
                prom_result = "Поколение = " + str(gen) + "\n" + "Лучший результат = " + str(min_) + "\n"
                print(prom_result)
                self.dopf.setText(prom_result)
            step += 1

            if step_null:
                step_null = False
                step = 0
                checked = True

        pygame.quit()

        return result




if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GeneticAlgorithm()
    sys.exit(app.exec_())

