from random import *
from tkinter import *

window = Tk()
# colorchooser.askcolor()
# from tkinter import colorchooser

size = 600
root = Tk()
canvas = Canvas(root, width=size, height=size)
canvas.pack()
diapason = 0

while diapason < 5000:
    colors = choice(['aqua', 'blue', 'white'])
    x0 = randint(0, size)
    y0 = randint(0, size)
    d = randint(0, int(size / 6))
    canvas.create_oval(x0, y0, x0 + d, y0 + d, fill=colors)
    diapason += 1
    root.update()

# while diapason < 5000:
#    colors = choice(['aqua', 'blue', 'white'])
#    x0 = randint(0, size)
#    y0 = randint(0, size)
#    d = randint(0, int(size/6))
#    canvas.create_oval(x0, y0, x0 + d, y0 + d, fill=colors)
#    diapason += 1
#    root.update()
