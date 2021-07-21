from threading import Thread
import matrix
import func
import config

thread = Thread(target=func.control)
# thread.start()

matrix = matrix.Matrix(config.weight, config.height)

#matrix.clear_db()

status = True
while status:

    status = matrix.run_generation()
