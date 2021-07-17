import time
import connector
from objects import *


class Matrix:

    def __init__(self, weight, height):
        self.__generation = 0
        self.__turns = 0
        self.__food = set()
        self.__venom = set()
        self.__walls = set()
        self.__cells = set()
        self.__dead_cells = []
        self.__weight = weight
        self.__height = height
        self.__matrix = []
        for i in range(weight + 1):
            self.__matrix.append([])
            for j in range(height + 1):
                self.__matrix[i].append(0)

        self.__objects_dict = {'F': self.__food, 'v': self.__venom, 'W': self.__walls, 'C': self.__cells}

        self.__con = connector.Connector()

    def get_sym(self, x, y):
        return self.__matrix[x][y]

    def cords_is_empty(self, x, y):

        if self.__matrix[x][y] == 0:
            return 1

        return 0

    def append_object(self, object):
        self.__objects_dict[str(object)].add(object)

    def generate_objects(self, generate_cells=False):

        food_array, venom_array, cells_array = arrays_of_random_cords()

        for i in range(food_number):
            Food(self, *food_array[i])

        for i in range(venom_number):
            Venom(self, *venom_array[i])

        if generate_cells is True:
            for i in range(cells_number):
                cell = Cell(self, *cells_array[i])
                cell.set_genotype(0, start_genotype)
                self.__cells.add(Cell(self, *cells_array[i]))

    def load_data(self):

        data = self.__con.get_data()

        self.__generation = data['generation']

        # TODO упростить
        map(lambda object_data: Food(*object_data), data['objects']['food'])
        map(lambda object_data: Venom(*object_data), data['objects']['venom'])
        map(lambda object_data: Wall(*object_data), data['objects']['walls'])
        map(lambda object_data: Cell(*object_data), data['objects']['cells'])

    def update_visualisation(self):

        w.update_idletasks()
        w.update()

        time.sleep(1)
