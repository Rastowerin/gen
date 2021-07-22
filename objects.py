import random

import func
from config import *
from vis import *


class Object:

    def __init__(self, matrix, x, y, color, sym, active=True):
        self._x = x
        self._y = y
        self._color = color
        self._sym = sym
        self._matrix = matrix

        if active:
            self.activate()

        c.create_polygon((10 + x * 30, 10 + y * 30), (40 + x * 30, 10 + y * 30), (40 + x * 30, 40 + y * 30),
                         (10 + x * 30, 40 + y * 30), fill=self._color, outline='black')

    def __del__(self):
        c.create_polygon((10 + self._x * 30, 10 + self._y * 30), (40 + self._x * 30, 10 + self._y * 30),
                         (40 + self._x * 30, 40 + self._y * 30),
                         (10 + self._x * 30, 40 + self._y * 30), fill='white', outline='black')

    def __repr__(self):
        return self._sym

    def activate(self):
        self._matrix.append_object(self)

    def get_cords(self):
        return self._x, self._y


class Food(Object):

    def __init__(self, matrix, x, y, active=True):
        super().__init__(matrix, x, y, 'green', 'F', active)


class Venom(Object):

    def __init__(self, matrix, x, y, active=True):
        super().__init__(matrix, x, y, 'red', 'V', active)


class Wall(Object):

    def __init__(self, matrix, x, y, active=True):
        super().__init__(matrix, x, y, 'grey', 'W', active)


class Cell(Object):

    def __init__(self, matrix, x, y, health=10, turns=0, direction=random.randint(0, 7), pointer=0, genotype=[], active=True):

        super().__init__(matrix, x, y, 'blue', 'C', active)
        self.__health = health
        self.__turns = turns
        self.__direction = direction
        self.__p = pointer
        self.__genotype = genotype
        self.__reactions = {'N': 5, 'F': 4, 'V': 1, 'W': 4, 'C': 3}

        self.__move_list = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        self.__directions_list = [-1, 0, 1, 2, 3, 4, 5, 6]

        if len(self.__genotype) < 64:
            for i in range(64):
                self.__genotype.append(random.randint(0, 63))

    def __mutate(self):
        x = random.randint(0, 3)
        while x > 0:
            self.__genotype[random.randint(0, 31)] = random.randint(0, 31)
            x -= 1

    def set_genotype(self, g, l=0, mutate=False):
        self.__genotype = self.__genotype[:l] + g + self.__genotype[l + len(g):]

        if mutate:
            self.__mutate()

    def get_genotype(self):
        return self.__genotype

    def replicate(self):

        array_of_random_cords = func.arrays_of_random_cords(weight, height, 1, selection)
        descendants = list(map(lambda data: Cell(self._matrix, *data, active=False), array_of_random_cords))
        descendants = list(map(lambda cell: cell.set_data(*self.get_data()), descendants))
        descendants = list(map(lambda cell: cell.set_genotype(self.get_genotype()), descendants[1:])) + \
                      descendants[0].set_genotype(self.get_genotype(), mutate=True)

        return descendants

    def set_data(self, health, turns, direction, pointer):
        self.__health, self.__turns, self.__direction, self.__p = health, turns, direction, pointer

    def get_data(self):
        return self.__health, self.__turns, self.__direction, self.__p

    def __die(self):
        self._matrix()._dead_cells += 1
        self._matrix.delete_object(self)

    def __eat(self, x, y):

        sym = self._matrix.get_sym(x, y)
        object = self._matrix.get_object(x, y)

        if sym == 'F':
            self._matrix.delete_object(object)
            self.__health += 10

        if sym == 'V':
            self._matrix.delete_object(object)
            self.__health -= 10

    def __go(self, num):

        new_direction = self.__direction + self.__directions_list[num]
        num = (num + self.__direction) % 8
        self.__direction = new_direction

        dx, dy = self.__move_list[num]
        x, y = (self._x + dx) % weight, (self._y + dy) % height

        sym = self._matrix.get_sym(x, y)

        self.__eat(x, y)

        if sym == 'W' or sym == 'C':
            return self.__reactions[sym]

        c.create_polygon((10 + self._x * 30, 10 + self._y * 30), (40 + self._x * 30, 10 + self._y * 30),
                         (40 + self._x * 30, 40 + self._y * 30),
                         (10 + self._x * 30, 40 + self._y * 30), fill='white', outline='black')

        self._x, self._y = x, y

        c.create_polygon((10 + self._x * 30, 10 + self._y * 30), (40 + self._x * 30, 10 + self._y * 30),
                         (40 + self._x * 30, 40 + self._y * 30),
                         (10 + self._x * 30, 40 + self._y * 30), fill='blue', outline='black')

        return self.__reactions[sym]

    def __catch(self, num):
        dx, dy = self.__move_list[num % 8]
        x, y = (self._x + dx) % weight, (self._y + dy) % height

        sym = self._matrix.get_sym(x, y)
        object = self._matrix.get_object(x, y)

        if sym == 'F':
            self.__eat(x, y)

        if sym == 'V':
            self._matrix.delete_object(object)
            Food(self._matrix, x, y)

        return self.__reactions[sym]

    def __look(self, num):
        dx, dy = self.__move_list[num % 8]
        x, y = (self._x + dx) % weight, (self._y + dy) % height

        return self.__reactions[self._matrix.get_sym(x, y)]

    def turn(self):

        self.__health -= 1
        if self.__health <= 0:
            self.__die()

        self.__turns += 1

        count = 0
        while count < 10:
            num = self.__genotype[self.__p]

            if num < 8:
                res = self.__go(num)
                self.__p = (self.__p + res) % 64
                break

            elif num < 16:
                res = self.__catch(num)
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

