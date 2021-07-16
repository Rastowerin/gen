import random as r
from func import *


class Cell:

    def __init__(self, matrix, x, y):

        self.__p = 0
        self.__turns = 0
        self.__direction = random.randint(0, 7)
        self.__genotype = []
        self.__health = 10
        self.__reactions = {'0': 5, '1': 4, '2': 1, '3': 4, 'C': 3}

        self.__move_list = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        self.__directions_list = [-1, 0, 1, 2, 3, 4, 5, 6]

        for i in range(64):
            self.__genotype.append(random.randint(0, 63))

        self.__x = x
        self.__y = y
        self.matrix = matrix
        self.matrix[self.__x][self.__y] = self
        draw_cell(self.__x, self.__y)

    def __repr__(self):
        return 'C'

    def __die(self):
        clear(self.matrix, self.__x, self.__y)

    def __mutate(self):
        x = r.randint(0, 3)
        while x > 0:
            self.__genotype[r.randint(0, 31)] = r.randint(0, 31)
            x -= 1

    def set_genotype(self, l, g):
        self.__genotype = self.__genotype[:l] + g + self.__genotype[l + len(g):]

    def get_genotype(self):
        return self.__genotype

    def replicate(self, a):

        descendants = []
        for i in range(a):

            f = True
            while f:
                x, y = r.randint(1, weight - 2), r.randint(1, height - 2)
                if self.matrix[x][y] == 0:
                    f = False

            descendants.append(Cell(self.matrix, x, y))
            self.matrix[x][y].set_genotype(0, self.__genotype.copy())

            if i == 0:
                self.matrix[x][y].__mutate()

        return descendants

    def set_data(self, health, turns, direction, p):
        self.__health, self.__turns, self.__direction, self.__p = health, turns, direction, p

    def get_data(self):
        return self.__x, self.__y, self.__health, self.__turns, self.__direction, self.__p

    def __go(self, num):

        new_direction = self.__direction + self.__directions_list[num]
        num = (num + self.__direction) % 8
        self.__direction = new_direction

        dx, dy = self.__move_list[num]
        x, y = (self.__x + dx) % weight, (self.__y + dy) % height

        reaction = self.__reactions[str(self.matrix[x][y])]
        if self.matrix[x][y] != 2 and self.matrix[x][y] != 3 and str(self.matrix[x][y]) != 'C':

            if self.matrix[x][y] == 1:
                self.__health += 10

            clear(self.matrix, self.__x, self.__y)
            self.__x, self.__y = x, y
            self.matrix[self.__x][self.__y] = self
            draw_cell(self.__x, self.__y)

        if self.matrix[x][y] == 2:
            self.__health -= 10

        return reaction

    def __look(self, num):
        dx, dy = self.__move_list[num % 8]
        x, y = (self.__x + dx) % weight, (self.__y + dy) % height

        return self.__reactions[str(self.matrix[x][y])]

    def __eat(self, num):
        dx, dy = self.__move_list[num % 8]
        x, y = (self.__x + dx) % weight, (self.__y + dy) % height

        if self.matrix[x][y] == 1:
            clear(self.matrix, x, y)
            self.__health += 10

        if self.matrix[self.__x + dx][self.__y + dy] == 2:
            clear(self.matrix, self.__x + dx, self.__y + dy)
            create_food(self.matrix, self.__x + dx, self.__y + dy)

        return self.__reactions[str(self.matrix[x][y])]

    def turn(self):

        self.__health -= 1
        if self.__health <= 0:
            self.__die()
            return 1

        self.__turns += 1

        count = 0
        while count < 10:
            num = self.__genotype[self.__p]

            if num < 8:
                res = self.__go(num)
                self.__p = (self.__p + res) % 64
                break

            elif num < 16:
                res = self.__eat(num)
                self.__p = (self.__p + res) % 64
                break

            elif num < 24:
                res = self.__look(num)
                self.__p = (self.__p + res) % 64
                count += 1

            elif num < 64:
                self.__p = (self.__p + num) % 64
                count += 1

        if self.__health <= 0:
            self.__die()
            return 1

        return 0
