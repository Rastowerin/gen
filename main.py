import time
from objects import *

for i in range(20):
    for j in range(10):
        if i in (0, 19) or j in (0, 9):
            create_wall(i, j)

for i in range(4):

    f = True
    while f:
        x, y = r.randint(1, 18), r.randint(1, 8)
        if m[x][y] == 0:
            f = False

    Cell(x, y)

food_count = 0
venom_count = 0

count = 0
while True:

    count += 1
    print(count)

    food_count -= deleted_food
    venom_count -= deleted_venom
    deleted_food, deleted_venom = 0, 0

    while food_count <= 20:

        f = True
        while f:
            x, y = r.randint(1, 18), r.randint(1, 8)
            if m[x][y] == 0:
                f = False

        create_food(x, y)
        food_count += 1

    while venom_count <= 20:

        f = True
        while f:
            x, y = r.randint(1, 18), r.randint(1, 8)
            if m[x][y] == 0:
                f = False

        create_venom(x, y)
        venom_count += 1

    f = False
    while True:

        for cell in cells.copy():
            cell.turn()

            w.update_idletasks()
            w.update()

            time.sleep(0.1)

            if len(cells.difference(cells_to_del)) == 1:
                f = True
                break

        cells.difference_update(cells_to_del)
        cells_to_del.clear()

        if f:
            break

    for cell in cells.copy():
        cell.replicate(4)
        cell.delete()
