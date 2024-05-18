from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from io import BytesIO
from os import path

try:
    from PIL import Image, ImageTk
except ImportError:
    print("pillow must be installed for open/save to work")


brush_color = "black"
brush_size = 10
current_image_path = None
old_image_path = None


def set_title():
    if current_image_path:
        root.title(f"{path.split(current_image_path)[1]} - BAINT")
    else:
        root.title("untitled - BAINT")

def get_current_image_path():
    if current_image_path == None:
        set_current_image_path(filedialog.asksaveasfilename())
    return current_image_path

def set_current_image_path(new):
    global current_image_path, old_image_path
    old_image_path = current_image_path
    current_image_path = new
    set_title()

def restore_image_path():
    global current_image_path
    current_image_path = old_image_path
    set_title()

def open_image():
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    canvas.config(width=photo.width(), height=photo.height())
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.image = photo
    set_current_image_path(file_path)


def save():
    print(current_image_path, old_image_path)
    ps = canvas.postscript(colormode='color')
    image = Image.open(BytesIO(ps.encode('utf-8')))
    try:
        image.save(get_current_image_path())
    except:
        restore_image_path()
        messagebox.showwarning(title="warning", message="wrong path")

def save_as():
    set_current_image_path(filedialog.asksaveasfilename())
    save()
    
def save_current():
    save(image_path=get_current_image_path())

def Choose_color():
    #asking user to choose color using deafult color choosing dialog window
    global brush_color
    brush_color = colorchooser.askcolor()[1]#getting color value, "[1]" gets only hex skipping rgb value

def New_image():
    canvas.delete("all")
    WSize = Toplevel()
    WSize.title("Set painting space size")
    WSize.transient(root)
    WSize.grab_set()
    
    HLabel = ttk.Label(WSize, text="Height")
    HLabel.grid(column=0,row=0,padx=10,pady=10)
    WLabel = ttk.Label(WSize, text="Width")
    WLabel.grid(column=0,row=1,padx=10,pady=10)
    
    MinHeight=1
    current_height= DoubleVar(value=MinHeight)
    height = ttk.Spinbox(
            WSize,
            from_=1,
            to_=1000000,
            textvariable=current_height,
            )
    height.grid(column=1, row=0, padx=10, pady=10)

    MinWidth=1
    current_width= DoubleVar(value=MinWidth)
    width = ttk.Spinbox(
            WSize,
            from_=1,
            to_=1000000,
            textvariable=current_width,
            )
    width.grid(column=1, row=1, padx=10, pady=10)
    
    def NewWindowSize():
        try:
            int_width = int(width.get())
            int_height = int(height.get())
        except ValueError:
            messagebox.showwarning(title="warning", message="wrong size")
            return
        canvas.config(width=int_width, height=int_height)
        WSize.destroy()
        
    ok_button = ttk.Button(
            WSize,
            text = "Ok",
            command=NewWindowSize)
    ok_button.grid(column=2, row=2, padx=10, pady=10)



class BrushSizeDialog(Toplevel):
    def __init__(self):
        # create window and set properties
        super().__init__(root)
        self.title("Brush size")
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
            text = "Cancel",
            command = self.close
        )
        ok_button = ttk.Button(
            bottom_frame,
            text = "Ok",
            command=self.accept_new_size
        )
        cancel_button.grid(column=0, row=0, padx=10, pady=10)
        ok_button.grid(column=1, row=0, padx=10, pady=10)
        
    def close(self, event=None):#closing window
        self.destroy()
    
    def set_slider_to_int(self, num):#user can change brush size using slider
        if float(num).is_integer():#checking is 'num' an int to avoid errors
            pass
        else:
            new = int(float(num))
            self.slider.set(new)

    def set_spinbox_to_int(self):
        current = self.spinbox.get()
        current = float(current)
        if current.is_integer():#checking is 'current' an int to avoid errors
            pass
        else:
            new = int(current)
            self.spinbox.set(new)

    def accept_new_size(self):
        global brush_size
        try:
            brush_size = int(self.current_value.get())
        except:
            messagebox.showwarning(title="warning", message="size must be a number")
            return
        self.close()

     
previous = (0,0)#creating variable "previous" to check last mouse location

def draw_circle(center):
    x = center[0]
    y = center[1]
    radius = brush_size / 2
    top_left = (x - radius, y - radius)
    bottom_right = (x + radius - 1, y + radius - 1)
    canvas.create_oval(*top_left, *bottom_right, outline=brush_color, fill=brush_color)



def select(event): #funcion to draw dots
    global previous
    #widget = event.widget 
    draw_circle((event.x, event.y))
    previous = (event.x, event.y)#changng previous so it will be accurate next time


def drag(event): #function to draw lines when dragging mouse
    global previous
    canvas.create_line(previous[0], previous[1], event.x, event.y, fill=brush_color, width=brush_size)
    draw_circle((event.x, event.y))
    #!Important, this feature is currently bugged, it isn't drawing how it is supposed to look like
    #possible fix(isn't tested) can be changing it from line to oval, this may make this function unnecesarry
    widget = event.widget
    previous = (event.x, event.y)#changng previous so it will be accurate next time

do_nothing = lambda: None

root = Tk()
root.minsize(400,500) # setting minimal windows size STC
set_title()
application = ttk.Frame(root, padding=10) # creating frame for root window
application.grid()#adding grid to frame created 2 lines ago


# Menubar setup
menubar = Menu(root)
root.config(menu=menubar)


menu_tree = {
    "file": [
        ["new", New_image],
        ["open", open_image],
        ["save_as", save_as],
        ["save", save],
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


canvas = Canvas(root, cursor="circle", width=300, height=300, bg="#ffffff")#creating canva to draw on, setting circle cursor to make drawing experience better
canvas.grid()#creating grid for canvas

# Bind mouse events to methods (could also be in the constructor)
canvas.bind("<Button-1>", select)

canvas.bind("<B1-Motion>", drag)

root.mainloop()
