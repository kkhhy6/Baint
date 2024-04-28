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


class BrushSizeDialog(Toplevel):
    def __init__(self):
        # create window and set properties
        super().__init__(root)
        self.title("rozmiar pedzla")
        self.rowconfigure(0, weight=2)
        self.columnconfigure(0, weight=1)
        self.transient(root)
        self.grab_set()
        self.bind("<Escape>", self.close)

        self.current_value = DoubleVar(value=brush_size)
        self.max_value = 200
        self.create_widgets()

    def create_widgets(self):
        #create frames and separator
        top_frame = ttk.Frame(self)
        separator = ttk.Separator(self)
        bottom_frame = ttk.Frame(self)

        top_frame.grid(row=0, padx=10, pady=10, sticky="N")
        separator.grid(row=1, sticky="EW")
        bottom_frame.grid(row=2, sticky="S")


        #create widgets for top_frame
        self.slider = ttk.Scale(
            top_frame,
            from_ = 1,
            to = self.max_value,
            orient = "horizontal",
            length = 250,
            variable = self.current_value,
            command = self.set_slider_to_int
        )
        self.spinbox = ttk.Spinbox(
            top_frame,
            from_=1,
            to=self.max_value,
            textvariable=self.current_value,
            command=self.set_spinbox_to_int
        )
        self.slider.grid(column=0, row=0, padx=10, pady=10)
        self.spinbox.grid(column=1, row=0, padx=10, pady=10)


        #create widgets for bottom_frame
        cancel_button = ttk.Button(
            bottom_frame,
            text = "Anuluj",
            command = self.close
        )
        ok_button = ttk.Button(
            bottom_frame,
            text = "Ok",
            command=self.accept_new_size
        )
        cancel_button.grid(column=0, row=0, padx=10, pady=10)
        ok_button.grid(column=1, row=0, padx=10, pady=10)
        
    def close(self, event=None):
        self.destroy()
    
    def set_slider_to_int(self, num):
        if float(num).is_integer():
            pass
        else:
            new = int(float(num))
            self.slider.set(new)

    def set_spinbox_to_int(self):
        current = self.spinbox.get()
        current = float(current)
        if current.is_integer():
            pass
        else:
            new = int(current)
            self.spinbox.set(new)

    def accept_new_size(self):
        global brush_size
        brush_size = int(self.current_value.get())
        print(brush_size)
        self.close()

     
previous = (0,0)#creating variable "previous" to check last mouse location
def select(event): #funcion to draw indyvidual pixels
    global previous
    #widget = event.widget
    top_left = (event.x - brush_size/2, event.y - brush_size/2)
    bottom_right = (event.x + brush_size/2, event.y + brush_size/2)
    canvas.create_oval(*top_left, *bottom_right, outline=brush_color, fill=brush_color)
    # canvas.create_line(event.x, event.y, event.x + 1, event.y, width=brush_size)#creating line that actually is a dot
    previous = (event.x, event.y)
    print(brush_size)


def drag(event): #function to draw lines when dragging mouse
    global previous
    canvas.create_line(previous[0], previous[1], event.x, event.y, fill=brush_color, width=brush_size) #creating line (this time it is a line) when dragging mouse
    widget = event.widget
    previous = (event.x, event.y)#changng previous so it will be accurate next time
    print(brush_size)

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
        ["exit", root.destroy],
    ],
    "brush": [
        ["color", Choose_color],
        ["size", BrushSizeDialog],
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
