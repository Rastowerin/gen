import os, psutil
process = psutil.Process(os.getpid())

from threading import Thread
import matrix
import func
import config

# TODO прикрутить atexit

thread = Thread(target=func.control)
# thread.start()

matrix = matrix.Matrix(config.weight, config.height)
matrix.set_start_genotype(config.start_genotype)

# matrix.clear_db()

while True:
    matrix.run_generation()
