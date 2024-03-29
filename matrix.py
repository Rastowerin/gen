import numpy as np
import matplotlib.pyplot as plt
import time
import func
import connector
from objects import *


class Matrix:

    def __init__(self, app, width, height):

        self.__app = app

        self.__generation = 0
        self.__summary_lifetime = 0
        self.__generation_is_active = False
        self.__food = set()
        self.__venom = set()
        self.__walls = set()
        self.__cells = set()
        self.__dead_cells = 0
        self.__descendants_genotypes = []
        self.__width = width
        self.__height = height
        self.__matrix = []
        for i in range(width + 1):
            self.__matrix.append([])
            for j in range(height + 1):
                self.__matrix[i].append('N')

        self.__average_lifetime_array = np.array([])

        self.__objects_dict = {'F': self.__food, 'V': self.__venom, 'W': self.__walls, 'C': self.__cells}

        self.set_start_genotype([])

        self.__con = connector.Connector()

    def change_cords(self, x1, y1, x2, y2):

        object = str(self.__matrix[x1][y1])
        self.__app.erase_object(x1, y1)
        self.__app.draw_object(x2, y2, object)
        self.__matrix[x1][y1], self.__matrix[x2][y2] = 'N', self.__matrix[x1][y1]

    def get_all_objects(self):
        return self.__food.union(self.__venom.union(self.__walls.union(self.__cells)))

    def get_sym(self, x, y):
        return str(self.__matrix[x][y])

    def get_object(self, x, y):
        return self.__matrix[x][y]

    def get_average_lifetime(self):
        return self.__summary_lifetime // user_settings.cells_number

    def delete_object(self, object):
        x, y = object.get_cords()
        self.__matrix[x][y] = 'N'
        self.__objects_dict[str(object)].remove(object)
        self.__app.erase_object(x, y)

    def cords_is_empty(self, x, y):
        if self.__matrix[x][y] == 'N':
            return 1
        return 0

    def append_object(self, object):
        x, y = object.get_cords()
        self.__matrix[x][y] = object
        self.__objects_dict[str(object)].add(object)
        object.vis()

    def draw_object(self, x, y, sym):
        self.__app.draw_object(x, y, sym)

    def get_dead_cells(self):
        return self.__dead_cells

    def append_dead_cell(self, turns_of_cell):
        self.__dead_cells += 1
        self.__summary_lifetime += turns_of_cell

    def append_descendants(self, array):
        self.__descendants_genotypes.extend(array)

    def __generate_objects(self):

        food_array, venom_array, walls_array, cells_array = \
            func.arrays_of_random_cords(user_settings.width, user_settings.height, 4, user_settings.food_number, user_settings.venom_number,
            user_settings.walls_number, user_settings.cells_number)

        list(map(lambda object_data: Food(self, *object_data), food_array))
        list(map(lambda object_data: Venom(self, *object_data), venom_array))
        list(map(lambda object_data: Wall(self, *object_data), walls_array))
        list(map(lambda object_data: Cell(self, *object_data), cells_array))

    def __clear(self):
        list(map(self.delete_object, self.get_all_objects()))

    def clear_db(self):
        self.__con.clear_db()

    def set_start_genotype(self, genotype):
        for i in range(user_settings.cells_number):
            self.__descendants_genotypes.append(genotype)

    def start_generation(self, generate=True):

        self.__generation_is_active = True

        if generate:
            self.__generate_objects()

        """if (self.__generation + 1) % 5 == 0:
            try:
                self.__con.load_data([self.__generation, self.__summary_lifetime], self.__cells)
            except Exception as e:
                print(e)"""

        self.__turns = 0
        self.__summary_lifetime = 0
        self.__generation += 1
        self.__dead_cells = 0

        ind = 0
        for cell in self.__cells:
            cell.set_genotype(self.__descendants_genotypes[ind])
            ind += 1

        self.__descendants_genotypes.clear()

    def __turn(self):
        self.__turns += 1
        for cell in self.__cells.copy():
            cell.turn()

        if len(self.__cells) == 0:
            self.__end_generation()

    def __end_generation(self):

        self.__generation_is_active = False

        self.__average_lifetime_array = np.append(self.__average_lifetime_array, self.get_average_lifetime())

        self.__clear()

        self.__app.print_generation_info(self.__generation, self.get_average_lifetime())

        array = func.average_array(self.__average_lifetime_array, user_settings.average_range)
        self.__app.set_plot(range(1, self.__generation + 1), array)

    def run(self):
        if self.__generation_is_active:
            self.__turn()
        else:
            self.start_generation()

    def save(self):
        objects = self.__food.union(self.__venom.union(self.__walls.union(self.__cells)))
        try:
            self.__con.load_data([self.__generation, self.__summary_lifetime], objects)
        except Exception as e:
            print(e)

    def load_data(self):

        data = self.__con.get_data()
        self.__generation = data['generation']

        # TODO упростить
        list(map(lambda object_data: Food(self, *object_data), data['objects']['food']))
        list(map(lambda object_data: Venom(self, *object_data), data['objects']['venom']))
        list(map(lambda object_data: Wall(self, *object_data), data['objects']['wall']))
        list(map(lambda object_data: Cell(self, *object_data), data['objects']['cell']))
