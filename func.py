import random
import sqlite3
from vis import *

con = sqlite3.connect("db.db")
cur = con.cursor()

tables_dict = {0: 'food', 1: 'venom', 2: 'wall', 3: 'cell'}


def clear(matrix, x, y):
    c.create_polygon((10 + x * 30, 10 + y * 30), (40 + x * 30, 10 + y * 30), (40 + x * 30, 40 + y * 30),
                     (10 + x * 30, 40 + y * 30), fill='white', outline='black')
    matrix[x][y] = 0


def create_food(matrix, x, y):
    c.create_polygon((10 + x * 30, 10 + y * 30), (40 + x * 30, 10 + y * 30), (40 + x * 30, 40 + y * 30),
                     (10 + x * 30, 40 + y * 30), fill='green', outline='black')
    matrix[x][y] = 1


def create_venom(matrix, x, y):
    c.create_polygon((10 + x * 30, 10 + y * 30), (40 + x * 30, 10 + y * 30), (40 + x * 30, 40 + y * 30),
                     (10 + x * 30, 40 + y * 30), fill='red', outline='black')
    matrix[x][y] = 2


def create_wall(matrix, x, y):
    c.create_polygon((10 + x * 30, 10 + y * 30), (40 + x * 30, 10 + y * 30), (40 + x * 30, 40 + y * 30),
                     (10 + x * 30, 40 + y * 30), fill='black', outline='black')
    matrix[x][y] = 3


def draw_cell(x, y):
    c.create_polygon((10 + x * 30, 10 + y * 30), (40 + x * 30, 10 + y * 30), (40 + x * 30, 40 + y * 30),
                     (10 + x * 30, 40 + y * 30), fill='blue', outline='black')


funcs_dict = {0: create_food, 1: create_venom, 2: create_wall}


def arrays_of_random_cords():

    n = food_number + venom_number + cells_number

    array = []
    for i in range(n):
        array.append(random.randint(0, weight * height - 1))

    array.sort()
    for i in range(n - 1):
        if array[i + 1] <= array[i]:
            array[i + 1] = array[i] + 1

    d = array[-1] - weight * height + 1
    for i in range(n - 1, 1, -1):

        if array[i] > weight * height - 1:
            array[i] -= d

        if array[i - 1] >= array[i]:
            array[i - 1] = array[i] - 1

    d = max(weight, height)
    for i in range(n):
        array[i] = (array[i] % d, array[i] // d)

    food_array = []
    for i in range(food_number):
        x = random.randint(0, len(array) - 1)
        food_array.append(array[x])
        array.remove(array[x])

    venom_array = []
    for i in range(venom_number):
        x = random.randint(0, len(array) - 1)
        venom_array.append(array[x])
        array.remove(array[x])

    cells_array = []
    for i in range(cells_number):
        x = 0
        if len(array) > 1:
            x = random.randint(0, len(array) - 1)
        cells_array.append(array[x])
        array.remove(array[x])

    return food_array, venom_array, cells_array


def save(matrix, generation):

    objects_dict = {1: 'food', 2: 'venom', 3: 'wall'}

    cur.execute("INSERT INTO world_data(generation)"
                "VALUES({})".format(generation))

    cell_id = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if str(matrix[i][j]) == 'C':

                cell_id += 1
                cur.execute("INSERT INTO cell_objects(x, y, health, turns, direction, pointer)"
                            "VALUES({}, {}, {}, {}, {}, {})".format(*matrix[i][j].get_data()))

                cur.execute("CREATE TABLE genotype{}("
                            "ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
                            "gen INTEGER NOT NULL)".format(cell_id))

                genotype = matrix[i][j].get_genotype()

                for k in range(len(genotype)):
                    cur.execute("INSERT INTO genotype{}(gen) "
                                "VALUES({})".format(cell_id, genotype[k]))

            elif matrix[i][j] != 0:
                cur.execute("INSERT INTO {}_objects(x, y)"
                            "VALUES({}, {})".format(objects_dict[matrix[i][j]], i, j))

    con.commit()


def load(matrix):

    for i in range(3):
        cur.execute("SELECT * FROM {}_objects".format(tables_dict[i]))

        data = cur.fetchall()
        for j in range(len(data)):
            funcs_dict[i](matrix, *data[j])

    cur.execute("SELECT * FROM cell_objects")
    data = cur.fetchall()

    cur.execute("SELECT * FROM world_data")
    generation = cur.fetchone()

    genotypes = []
    for i in range(len(data)):
        cur.execute("SELECT * FROM genotype{}".format(i + 1))
        genotypes.extend(cur.fetchall())

    return generation, data, genotypes


def clear_db():
    cur.execute("SELECT * FROM cell_objects")
    cells = cur.fetchall()

    for i in range(len(cells)):
        cur.execute("DROP TABLE genotype{}".format(i + 1))

    for i in range(4):
        cur.execute("DELETE FROM {}_objects".format(tables_dict[i]))

    cur.execute("DELETE FROM world_data")

    con.commit()


def control():

    while True:

        if input() == 'stop':
            print('test')
            pass
