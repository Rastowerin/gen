import concurrent.futures
import time
import func
import connector
from objects import *


class Matrix:

    def __init__(self, weight, height):
        self.__generation = 0
        self.__summary_lifetime = 0
        self.__food = set()
        self.__venom = set()
        self.__walls = set()
        self.__cells = set()
        self.__dead_cells = 0
        self.__descendants_genotypes = []
        self.__weight = weight
        self.__height = height
        self.__matrix = []
        for i in range(weight + 1):
            self.__matrix.append([])
            for j in range(height + 1):
                self.__matrix[i].append('N')

        self.__objects_dict = {'F': self.__food, 'V': self.__venom, 'W': self.__walls, 'C': self.__cells}

        self.__con = connector.Connector()

    def swap_cords(self, x1, y1, x2, y2):
        self.__matrix[x1][y1], self.__matrix[x2][y2] = self.__matrix[x2][y2], self.__matrix[x1][y1]

    def get_all_objects(self):
        return self.__food.union(self.__venom.union(self.__walls.union(self.__cells)))

    def get_sym(self, x, y):
        return str(self.__matrix[x][y])

    def get_object(self, x, y):
        return self.__matrix[x][y]

    def get_average_lifetime(self):
        return self.__summary_lifetime // config.cells_number

    def delete_object(self, object):
        x, y = object.get_cords()
        self.__matrix[x][y] = 'N'
        self.__objects_dict[str(object)].remove(object)

    def cords_is_empty(self, x, y):
        if self.__matrix[x][y] == 'N':
            return 1
        return 0

    def append_object(self, object):
        x, y = object.get_cords()
        self.__matrix[x][y] = object
        self.__objects_dict[str(object)].add(object)
        object.vis()

    def get_dead_cells(self):
        return self.__dead_cells

    def append_dead_cell(self, turns_of_cell):
        self.__dead_cells += 1
        self.__summary_lifetime += turns_of_cell

    def append_descendants(self, array):
        self.__descendants_genotypes.extend(array)

    def __generate_objects(self):

        food_array, venom_array, walls_array, cells_array = \
            func.arrays_of_random_cords(config.weight, config.height, 4, config.food_number, config.venom_number,
            config.walls_number, config.cells_number)

        list(map(lambda object_data: Food(self, *object_data), food_array))
        list(map(lambda object_data: Venom(self, *object_data), venom_array))
        list(map(lambda object_data: Wall(self, *object_data), walls_array))
        list(map(lambda object_data: Cell(self, *object_data), cells_array))

    def __clear(self):
        list(map(self.delete_object, self.get_all_objects()))

    def clear_db(self):
        self.__con.clear_db()

    def set_start_genotype(self, genotype):
        for i in range(config.cells_number):
            self.__descendants_genotypes.append(genotype)

    def __turn(self):
        self.__turns += 1
        for cell in self.__cells.copy():
            cell.turn()

        # self.update_visualisation()

    def run_generation(self, generate=True):

        if generate:
            self.__generate_objects()

        self.__turns = 0
        self.__summary_lifetime = 0
        self.__generation += 1
        self.__dead_cells = 0

        ind = 0
        for cell in self.__cells:
            cell.set_genotype(self.__descendants_genotypes[ind])
            ind += 1
        self.__descendants_genotypes.clear()

        while len(self.__cells) > 0:
            self.__turn()

        self.__clear()

        if self.__generation % 1 == 0:
            print('generation ', self.__generation, '\n', 'average lifetime: ', self.get_average_lifetime(), '\n', sep='')

    def update_visualisation(self):

        w.update_idletasks()
        w.update()

        time.sleep(0.1)

    def __save(self):
        world_data = [self.__generation]
        objects = self.__food.union(self.__venom.union(self.__walls.union(self.__cells)))
        self.__con.load_data(world_data, objects)

    def load_data(self):

        data = self.__con.get_data()
        self.__generation = data['generation']

        # TODO упростить
        list(map(lambda object_data: Food(*object_data), data['objects']['food']))
        list(map(lambda object_data: Venom(*object_data), data['objects']['venom']))
        list(map(lambda object_data: Wall(*object_data), data['objects']['walls']))
        list(map(lambda object_data: Cell(*object_data), data['objects']['cells']))
