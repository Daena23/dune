from tkinter import *
import time

# создание объекта:
tk = Tk()
size = 500

# создание области рисования:
canvas = Canvas(tk, width=size, height=size)
# Canvas activation:
canvas.pack()

fish_obj = PhotoImage(file="fish.png")
fish_obj_up = PhotoImage(file="fish_up.png")

# координаты отображения картинки, anchor - с левого вернхего угла)

x1 = 200
y1 = 200
id_img = canvas.create_image(x1, y1, anchor=NW, image=fish_obj)
print(id_img)
canvas.create_line(x1, y1, 450, 450, dash=(4, 2))
canvas.create_rectangle(30, 30, 180, 120, outline="#fb0", fill="#fb0")
coordinates = []


# Перемещение по прямой
# for i in range(1, 100):
#     # ID, насколько сдвинуть на x и y
#     canvas.move(id_img, 2, 0)
#     tk.update()
#     time.sleep(0.02)

# for i in range(1, 100):
#     # ID, насколько сдвинуть на x и y
#     canvas.move(id_img, -2, 0)
#     tk.update()
#     time.sleep(0.02)

# (x;y)
#    -y
# -x  0  +x
#    +y
# обновит экран при каждом смещении объекта



def move_fish(event):
    global x1, y1
    if event.keysym == 'Up':
        canvas.move(id_img, 0, -4)
        y1 = y1 - 4
    elif event.keysym == 'Down':
        canvas.move(id_img, 0, 4)
        y1 = y1 + 4
    elif event.keysym == 'Left':
        canvas.move(id_img, -4, 0)
        x1 = x1 - 4
    elif event.keysym == 'Right':
        canvas.move(id_img, 4, 0)
        x1 = x1 + 4



canvas.bind_all("<KeyPress-Up>", move_fish)
canvas.bind_all("<KeyPress-Down>", move_fish)
canvas.bind_all("<KeyPress-Left>", move_fish)
canvas.bind_all("<KeyPress-Right>", move_fish)
# coordinates.append(x1, y1)
coordinates.append([x1, y1])
print(x1, y1)
tk.mainloop()




# canvas.create_rectangle(50,400,100,450)
#
# def rand_rect():
#     color_rect_1 = ["green","yellow","black","white","red","blue"]
#     color_rect = random.choice(color_rect_1)
#     x1 = random.randrange(400)
#     y1 = random.randrange(400)
#     x2 = random.randrange(400)
#     y2 = random.randrange(400)
#     canvas.create_rectangle(x1,y1,x2,y2, fill=color_rect)
#
# for i in range(0,100):
#     rand_rect()
# def move_fish(event):
#     if event.keysym == 'Up':
#         canvas.move(id_img, 0, -2)


# def round(x):
#     return

# while diapason < 5000:
#     colors = choice(['aqua', 'blue', 'white'])
#    x0 = randint(0, size)
#    y0 = randint(0, size)
#    d = randint(0, int(size/6))
#    canvas.create_oval(x0, y0, x0 + d, y0 + d, fill=colors)
#    root.update()

# while diapason < 5000:
#    colors = choice(['aqua', 'blue', 'white'])
#    x0 = randint(0, size)
#    y0 = randint(0, size)
#    d = randint(0, int(size/6))
#    canvas.create_oval(x0, y0, x0 + d, y0 + d, fill=colors)
#    diapason += 1
#    root.update()
