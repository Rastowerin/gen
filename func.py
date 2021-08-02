import random
import sqlite3
from vis import *

con = sqlite3.connect("db.db")
cur = con.cursor()

tables_dict = {0: 'food', 1: 'venom', 2: 'wall', 3: 'cell'}


def arrays_of_random_cords(width, height, n, *args):

    d = max(width, height)
    array_of_cords = range(width * height)
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


def average_array(array, k):

    sum, num = 0, 0
    result_array = []

    for i in range(min(len(array), k)):
        sum += array[i]
        num += 1

    for i in range(len(array)):

        if i - k > 0:
            sum -= array[i - k - 1]
            num -= 1

        if i + k < len(array):
            sum += array[i + k]
            num += 1

        result_array.append(sum // num)

    return result_array


def control():

    while True:
        if input() == 'stop':
            pass
