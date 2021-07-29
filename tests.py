import matrix
import objects
import config

test_matrix = matrix.Matrix(3, 3)
test_matrix.set_start_genotype([])

while True:

    for i in range(3):
        for j in range(3):

            if i == 1 and j == 1:
                objects.Cell(test_matrix, i, j)

            else:
                objects.Venom(test_matrix, i, j)

    test_matrix.run_generation(generate=False)
