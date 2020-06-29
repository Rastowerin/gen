from config import *
from vis import *

deleted_food = 0
deleted_venom = 0


def clear(x, y):
    global deleted_food, deleted_venom
    c.create_polygon((50 + x * 30, 50 + y * 30), (80 + x * 30, 50 + y * 30), (80 + x * 30, 80 + y * 30),
                     (50 + x * 30, 80 + y * 30), fill='white', outline='black')
    if m[x][y] == 1:
        deleted_food += 1
    if m[x][y] == 2:
        deleted_venom += 1
    m[x][y] = 0


def create_food(x, y):
    c.create_polygon((50 + x * 30, 50 + y * 30), (80 + x * 30, 50 + y * 30), (80 + x * 30, 80 + y * 30),
                     (50 + x * 30, 80 + y * 30), fill='green', outline='black')
    m[x][y] = 1


def create_venom(x, y):
    c.create_polygon((50 + x * 30, 50 + y * 30), (80 + x * 30, 50 + y * 30), (80 + x * 30, 80 + y * 30),
                     (50 + x * 30, 80 + y * 30), fill='red', outline='black')
    m[x][y] = 2


def create_wall(x, y):
    c.create_polygon((50 + x * 30, 50 + y * 30), (80 + x * 30, 50 + y * 30), (80 + x * 30, 80 + y * 30),
                     (50 + x * 30, 80 + y * 30), fill='black', outline='black')
    m[x][y] = 3


def draw_cell(x, y):
    c.create_polygon((50 + x * 30, 50 + y * 30), (80 + x * 30, 50 + y * 30), (80 + x * 30, 80 + y * 30),
                     (50 + x * 30, 80 + y * 30), fill='blue', outline='black')
