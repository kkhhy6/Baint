from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
brush_color = "black"
brush_size = 10


def Choose_color():
    #asking user to choose color using deafult color choosing dialog window
    global brush_color
    brush_color = colorchooser.askcolor()[1]#getting color value, "[1]" gets only hex skipping rgb value
    print(brush_color) #debug log with hexadecimal value


def Change_brush_width():
    global brush_size
    brush_size += 1

previous = (0,0)#creating variable "previous" to check last mouse location
def select(event): #funcion to draw indyvidual pixels
    global previous
    widget = event.widget
    top_left = (event.x - brush_size/2, event.y - brush_size/2)
    bottom_right = (event.x + brush_size/2, event.y + brush_size/2)
    canvas.create_oval(*top_left, *bottom_right, outline=brush_color, fill=brush_color)
    # canvas.create_line(event.x, event.y, event.x + 1, event.y, width=brush_size)#creating line that actually is a dot
    previous = (event.x, event.y)


def drag(event): #function to draw lines when dragging mouse
    global previous
    canvas.create_line(previous[0], previous[1], event.x, event.y, fill=brush_color, width=brush_size) #creating line (this time it is a line) when dragging mouse
    widget = event.widget
    previous = (event.x, event.y)#changng previous so it will be accurate next time

do_nothing = lambda: None

root = Tk()
root.minsize(400,500) # setting minimal windows size STC
root.title("BAINT") # setting window title

application = ttk.Frame(root, padding=10) # creating frame for root window
application.grid()#adding grid to frame created 2 lines ago


# Menubar setup
menubar = Menu(root)
root.config(menu=menubar)


menu_tree = {
    "file": [
        ["new", do_nothing],
        ["import", do_nothing],
        ["export", do_nothing],
        ["exit", do_nothing],
    ],
    "brush": [
        ["color", Choose_color],
        ["size", do_nothing],
    ],
}

for menu_name in menu_tree:
    new_menu = Menu(menubar)
    for item in menu_tree[menu_name]:
        new_menu.add_command(
            label=item[0],
            command=item[1]
        )
    menubar.add_cascade(
        label=menu_name,
        menu=new_menu
    )


#!IMPORTANT, canvas use real pixels, only way to make pixel on bitmap bigger on screen is resizing photo, possible solution will be included in 'CanvasIssue.txt'(file not added yet, will be created soon)
canvas = Canvas(root, cursor="circle", width=300, height=300, bg="#ffffff")#creating canva to draw on, setting circle cursor to make drawing experience better
canvas.grid()#creating grid for canvas
#next line is made for debugging window size, keep commented if unnecessary
#line = canvas.create_line(0,0,100,100)

# Bind mouse events to methods (could also be in the constructor)
canvas.bind("<Button-1>", select)

canvas.bind("<B1-Motion>", drag)

root.mainloop()
