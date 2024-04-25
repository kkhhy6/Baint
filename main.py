from tkinter import *
from tkinter import  colorchooser
from tkinter import ttk
color = "black"
def Choose_color():
    #asking user to choose color using deafult color choosing dialog window
    global color
    color = colorchooser.askcolor()[1]#getting color value, "[1]" gets only hex skipping rgb value
    print(color) #debug log with hexadecimal value

previous = (0,0)#creating variable "previous" to check last mouse location

def select(event): #funcion to draw indyvidual pixels
    global previous
    widget = event.widget
    canvas.create_line(event.x, event.y, event.x + 1, event.y)#creating line that actually is a dot
    previous = (event.x, event.y)
def drag(event): #function to draw lines when dragging mouse
    global previous
    canvas.create_line(previous[0], previous[1], event.x + 1, event.y, fill=color) #creating line (this time it is a line) when dragging mouse
    widget = event.widget
    previous = (event.x, event.y)#changng previous so it will be accurate next time

root = Tk()
root.minsize(300,500) #setting minimal windows size STC
frm = ttk.Frame(root, padding=10)#creating frame for root window
root.title("BAINT")#setting window title
frm.grid()#adding grid to frame created 2 lines ago
ttk.Button(frm, text="Choose Color", command=Choose_color).grid(column=0, row=0)#added button to use function 'Choose_color', for more reference check function description

#!IMPORTANT, canvas use real pixels, only way to make pixel on bitmap bigger on screen is resizing photo, possible solution will be included in 'CanvasIssue.txt'(file not added yet, will be created soon)
canvas = Canvas(root, cursor="circle", widt=100, height=100)#creating canva to draw on, setting circle cursor to make drawing experience better
canvas.grid()#creating grid for canvas
#next line is made for debugging window size, keep commented if unnecessary
#line = canvas.create_line(0,0,100,100)

# Bind mouse events to methods (could also be in the constructor)
canvas.bind("<Button-1>", select)

canvas.bind("<B1-Motion>", drag)

root.mainloop()
