from tkinter import *

w = Tk()
w.geometry('700x400')
c = Canvas(w, width=700, height=400)
c.pack()


for i in range(11):
    c.create_line((50, 50 + i * 30), (650, 50 + i * 30))
for i in range(21):
    c.create_line((50 + i * 30, 50), (50 + i * 30, 350))
