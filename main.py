from tkinter import *
from tkinter import  colorchooser
from tkinter import ttk
color = None
def Choose_color():
    global color
    color = colorchooser.askcolor()
    print(color)
    #TODO check if tk gets whole color to paint or is just part of it needed

root = Tk()
frm = ttk.Frame(root, padding=10)
root.title("BAINT")
frm.grid()
ttk.Button(frm, text="Choose Color", command=Choose_color).grid(column=0, row=0)
root.mainloop()