import os
import atexit
import keyboard
# , psutil
# process = psutil.Process(os.getpid())

from threading import Thread
import matrix
import func
import config

# TODO прикрутить atexit

thread = Thread(target=func.control)
# thread.start()

matrix = matrix.Matrix(config.weight, config.height)
matrix.set_start_genotype(config.start_genotype)

matrix.load_data()

atexit.register(matrix.save)


while not keyboard.is_pressed('space'):
    matrix.run_generation()
