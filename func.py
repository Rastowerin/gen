import random
import sqlite3
from vis import *

con = sqlite3.connect("db.db")
cur = con.cursor()

tables_dict = {0: 'food', 1: 'venom', 2: 'wall', 3:     'cell'}


def arrays_of_random_cords(weight, height, n, *args):

    d = max(weight, height)
    array_of_cords = range(weight * height)
    array_of_cords = set(map(lambda x: (x % d, x // d), array_of_cords))

    ind = 0
    arrays = []
    while ind < n:

        array = set(random.sample(array_of_cords, args[ind]))
        array_of_cords = array_of_cords.difference(array)
        array = list(array)
        arrays.append(array)

        ind += 1

    return tuple(arrays)


def control():

    while True:
        if input() == 'stop':
            pass
