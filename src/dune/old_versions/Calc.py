from tkinter import *
root = Tk()

e = Entry(root, width=50,  bg='lightblue')
e.grid(row=0, column=0, columnspan=3, padx=10, pady=20)

def button_click(number):
    # e.delete(0, END)
    current = e.get() # накопление чисел
    e.delete(0, END)
    e.insert(0, str(current)+ str(number)) # первое число - позиция на кт появляется число


x = 50
y = 20

x1 = 110
y1 = 20

button1 = Button(root, text = '1', padx=x, pady=y, command=lambda: button_click(1))
button2 = Button(root, text = '2', padx=x, pady=y, command=lambda: button_click(2))
button3 = Button(root, text = '3', padx=x, pady=y, command=lambda: button_click(3))
button4 = Button(root, text = '4', padx=x, pady=y, command=lambda: button_click(4))
button5 = Button(root, text= '5', padx=x, pady=y, command=lambda: button_click(5))
button6 = Button(root, text='6', padx=x, pady=y, command=lambda: button_click(6))
button7 = Button(root, text='7', padx=x, pady=y, command=lambda: button_click(7))
button8 = Button(root, text='8', padx=x, pady=y, command=lambda: button_click(8))
button9 = Button(root, text='9', padx=x, pady=y, command=lambda: button_click(9))
button_add = Button(root, text='+', padx=x, pady=y, command=lambda: button_click(10))
minus = Button(root, text='-', padx=x, pady=y, command=lambda: button_click(11))
button_clear = Button(root, text='C', padx=x, pady=y, command=lambda: button_click(12))
equal = Button(root, text='=', padx=x1, pady=y1, command=lambda: button_click(13))



button1.grid(row=3, column=0)
button2.grid(row=3, column=1)
button3.grid(row=3, column=2)
button4.grid(row=2, column=0)
button5.grid(row=2, column=1)
button6.grid(row=2, column=2)
button7.grid(row=1, column=0)
button8.grid(row=1, column=1)
button9.grid(row=1, column=2)
button_add.grid(row=4, column=0)
button_clear.grid(row=4, column=1)
minus.grid(row=4, column=2)
equal.grid(row=5, column=0, columnspan=2)

root.mainloop()