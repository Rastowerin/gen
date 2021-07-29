from threading import Thread
import matrix
import func
import config

matrix = matrix.Matrix(config.weight, config.height)
# matrix.set_start_genotype(config.start_genotype)

matrix.set_start_genotype(config.start_genotype)

while True:
    matrix.run_generation()
