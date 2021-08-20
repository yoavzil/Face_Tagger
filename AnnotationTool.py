import tkinter as tk
import atexit
from ImageHandler import *
from DataHandler import *
from PIL import Image, ImageTk


# Home assignment: implementing an annotation tool for tagging faces.

# The replace_img function replacing the current image displayed on the canvas with the next or previous image.
# Input: e - event, indicating which key has been pressed (<-/->).
# win - canvas, on this object all the components are drown.
# ih - ImageHandler, responsible for fetching the images from the file.
# DH - DataHandler, responsible for managing the data.

def replace_img(e, win, ih, DH):
    if e.keysym == "Left" or e.keysym == "Right":
        global img
        global imgtk
        # when pressing Right arrow the next image will be fetched
        # and when pressing Left arrow the previous image will be fetched.
        if e.keysym == "Right":
            img = ih.next()
        else:
            img = ih.prev()
        # transforming the image from a numpy array to an ImageTk format that can be displayed on the canvas.
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(img[0]))
        win.create_image(0, 30, anchor=tk.NW, image=imgtk)
        if len(DH.currentData) != 0:
            DH.flash_CurrentData()  # move the data of the current image to the general data
        if len(DH.currentRects) != 0:
            DH.clear_rects()  # clear all rectangles representations from the rectangles list.
        if img[1] in DH.get_data().keys():
            for rect in DH.get_data()[img[1]]:
                win.create_rectangle(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3] , width=4, outline='blue')

# THe first_location function is called when the user starts a new rectangle,
# it saves the first mouse location in order to draw later the rectangle.
# input: e - event, indicating the location of the mouse.
def first_location(e):
    global pos1
    pos1 = [e.x, e.y]


# The create_rect function draw a rectangle on the canvas from the first location point to the current location of the
# mouse. Input: e - event, indicating the location of the mouse. win - canvas, on this object all the components are
# drown.
def create_rect(e, win):
    if pos1[1] > 30:  # preventing the user from drawing a rectangle in the control panel.
        global rect
        win.delete(rect)  # deleting the previous rectangle.
        if e.y < 30:
            rect = win.create_rectangle(pos1[0], pos1[1], e.x, 32, width=4, outline='red')
        else:
            rect = win.create_rectangle(pos1[0], pos1[1], e.x, e.y, width=4, outline='red')


# THe finish_rect function draws a permanent rectangle when the use releases the mouse button.
# Input: e - event, indicating the location of the mouse.
# win - canvas, on this object all the components are drown.
# DH - DataHandler, responsible for managing the data.
def finish_rect(e, win, DH):
    if pos1[1] > 30:  # preventing the user from drawing a rectangle in the control panel.
        global rect
        global pos2
        global rects
        win.delete(rect)  # deleting the previous rectangle.
        if e.y < 30:
            pos2 = [e.x, 32]
        else:
            pos2 = [e.x, e.y]
        DH.add_key(img[1],
                   [pos1[0], pos1[1], pos2[0] - pos1[0], pos2[1] - pos1[1]])  # adding the image to the data as a key.
        DH.add_rect(win.create_rectangle(pos1[0], pos1[1], pos2[0], pos2[1], width=4,
                                         outline='blue'))  # adding the rectangle to the data as a value.


# The quit_save function saves the data in a pickle format and exit the program.
# Inputs: DH - DataHandler, responsible for managing the data.
def quit_save(e, DH):
    DH.flash_CurrentData()
    DH.data_to_pickle()
    exit(0)


# The save function saves the current image data in a pickle format.
# Inputs: DH - DataHandler, responsible for managing the data.
def save(e, DH):
    DH.current_data_to_pickle()


# THe remove_last_rect function remove the last rectangle that was drawn from the canvas and from the rectangle list.
# Input: win - canvas, on this object all the components are drown.
# DH - DataHandler, responsible for managing the data.
def remove_last_rect(e, win, DH):
    if DH.get_rects_size() > 0:
        win.delete(DH.last_rect())  # delete from canvas.
        DH.del_last_rect()  # delete from list.


# The get_path function return the path that the user entered.
# Input: path - Entry, the component that holds the user's path.
# Return: the user's path.
def get_path(path):
    return path.get()


# The start function is a callback function to the start button. responsible for presenting the first image
# and binding all the events to the main root so the functionality of the gui will begin with the first image.
# Input: win - canvas, on this object all the components are drown.
# ih - ImageHandler, responsible for fetching the images from the file.
# DH - DataHandler, responsible for managing the data.
# path - Entry, the component that holds the user's path.
# root - the main root.
def start(win, IH, DH, path, root):
    global img
    global imgtk
    IH.set_path(get_path(path))
    try:  # trying to read from the file.
        IH.init_list()
        img = IH.get_first_img(DH)

    except:
        return
    # transforming the image from a numpy array to an ImageTk format that can be displayed on the canvas.
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img[0]))
    win.create_image(0, 30, anchor=tk.NW, image=imgtk)
    if img[1] in DH.get_data().keys():
        for r in DH.get_data()[img[1]]:
            win.create_rectangle(r[0], r[1], r[0] + r[2], r[1] + r[3], width=4, outline='blue')
    # binding to the root all the events and their callback functions.
    root.bind("<KeyPress>", lambda event: replace_img(event, win, IH, DH))
    root.bind("<Button 1>", lambda event: first_location(event))
    root.bind("<B1-Motion>", lambda event: create_rect(event, win))
    root.bind("<ButtonRelease-1>", lambda event: finish_rect(event, win, DH))
    root.bind("<q>", lambda event: quit_save(event, DH))
    root.bind("<s>", lambda event: save(event, DH))
    root.bind("<d>", lambda event: remove_last_rect(event, win, DH))
    win.focus_set()  # moving the cursor from the entry box.


if __name__ == '__main__':
    # global vars
    img = 0
    imgtk = 0
    pos1 = 0
    pos2 = 0
    rect = 0

    ih = ImageHandler(500)
    DH = DataHandler()
    root = tk.Tk()
    root.title("Face Tagger")
    width = 500
    height = 530
    win = tk.Canvas(root, width=width, height=height)
    win.pack()
    txt = tk.Label(root, text="Enter Path: ")
    path = tk.Entry(root, width=50)
    txt.place(x=10, y=5)
    path.place(x=80, y=5)
    start_b = tk.Button(win, text="Start", command=lambda: start(win, ih, DH, path, root))
    start_b.place(x=400, y=5)
    atexit.register(DH.close_file)  # when exiting the program DH.close_file is called.

    root.mainloop()

