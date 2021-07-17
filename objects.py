import random as r
from func import *


class Object:

    def __init__(self, matrix, x, y, color, sym):
        self.__x = x
        self.__y = y
        self.__color = color
        self.__sym = sym
        self.__matrix = matrix

        matrix.append_object(self)

        c.create_polygon((10 + x * 30, 10 + y * 30), (40 + x * 30, 10 + y * 30), (40 + x * 30, 40 + y * 30),
                         (10 + x * 30, 40 + y * 30), fill=self.__color, outline='black')

    def __del__(self):
        c.create_polygon((10 + self.__x * 30, 10 + self.__y * 30), (40 + self.__x * 30, 10 + self.__y * 30),
                         (40 + self.__x * 30, 40 + self.__y * 30),
                         (10 + self.__x * 30, 40 + self.__y * 30), fill=self.__color, outline='black')

    def __repr__(self):
        return self.__sym

    def get_cords(self):
        return self.__x, self.__y


class Food(Object):

    def __init__(self, matrix, x, y):
        super().__init__(matrix, x, y, 'green', 'F')


class Venom(Object):

    def __init__(self, matrix, x, y):
        super().__init__(matrix, x, y, 'red', 'V')


class Wall(Object):

    def __init__(self, matrix, x, y):
        super().__init__(matrix, x, y, 'grey', 'W')


#TODO починить
class Cell(Object):

    def __init__(self, matrix, x, y, health=10, turns=0, direction=random.randint(0, 7), pointer=0, genotype=[]):

        super().__init__(matrix, x, y, 'blue', 'C')
        self.__health = health
        self.__turns = turns
        self.__direction = direction
        self.__p = pointer
        self.__genotype = genotype
        self.__reactions = {0: 5, 'F': 4, 'V': 1, 'W': 4, 'C': 3}

        self.__move_list = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        self.__directions_list = [-1, 0, 1, 2, 3, 4, 5, 6]

        if self.__genotype is False:
            for i in range(64):
                self.__genotype.append(random.randint(0, 63))

        matrix.append_object(self)

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

        # TODO переписать

        descendants = []
        for i in range(a):

            f = True
            x, y = 0, 0
            while f:
                x, y = r.randint(1, weight - 2), r.randint(1, height - 2)
                if self.__matrix.cords_is_empty(x, y):
                    f = False

            cell = Cell(self.__matrix, x, y)
            cell.set_genotype(0, self.get_genotype())

            if i == 0:
                cell.__mutate()

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

        reaction = self.__reactions[self.__matrix.get_sym(x, y)]
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
            return 1

        return 0
