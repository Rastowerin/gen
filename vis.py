from tkinter import *
from config import *

# TODO перейти на PyQt

w = Tk()
w.geometry('700x400')
c = Canvas(w, width=1920, height=1080)
c.pack()

for i in range(height + 1):
    c.create_line((10, 10 + i * 30), (10 + 30 * weight, 10 + i * 30))
for i in range(weight + 1):
    c.create_line((10 + i * 30, 10), (10 + i * 30, 10 + 30 * height))
