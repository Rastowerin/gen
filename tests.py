import func
import os, psutil

sets = [100, 100, 4, 1000, 1000, 0, 64]

process = psutil.Process(os.getpid())

while True:
    a = process.memory_info().rss

    func.arrays_of_random_cords(*sets)

    b = process.memory_info().rss
    print(b - a)
