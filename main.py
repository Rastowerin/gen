from threading import Thread
from objects import *

#thread = Thread(target=control)
#thread.start()

cells = set()
dead_cells = []

matrix = []
for i in range(weight + 1):
    matrix.append([])
    for j in range(height + 1):
        matrix[i].append(0)

generation = 0

# TODO переписать
if load_data is True:
    generation, cells_data, genotypes = load(matrix)

    for i in range(len(cells_data)):
        cell = Cell(matrix, cells_data[i][0], cells_data[i][1])
        cell.set_data(*cells_data[i][3:])
        cell.set_genotype(0, list(genotypes[i]))

else:
    clear_db()

while True:

    food_array, venom_array, cells_array = arrays_of_random_cords()

    for i in range(food_number):
        create_food(matrix, *food_array[i])

    for i in range(venom_number):
        create_venom(matrix, *venom_array[i])

    if generation == 0:
        for i in range(cells_number):
            cell = Cell(matrix, *cells_array[i])
            cell.set_genotype(0, start_genotype)
            cells.add(Cell(matrix, *cells_array[i]))

    turn_count = 0

    while len(cells):

        turn_count += 1

        for cell in cells.copy():
            dead = cell.turn()

            if dead:
                cells.remove(cell)
                dead_cells.append(cell)

    dead_cells = dead_cells[::-1]
    for i in range(cells_number // selection):
        dead_cells[i].replicate(selection)
    dead_cells.clear()

    objects_to_del = food_array
    objects_to_del.extend(venom_array)

    for i in range(len(objects_to_del)):
        clear(matrix, *objects_to_del[i])

    generation += 1

    if generation % 1 == 0:
        print('generation: ', generation)
        print('total: ', turn_count, '\n')

    if generation == 100:
        clear_db()
        save(matrix, generation)
        break
