from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import os
import csv

root = Tk(className="rock judging time !")


def load_scene(scene):
    match scene:
        case 0:
            frame_ts.tkraise()
        case 1:
            frame_rs.tkraise()


def load_image(img, width=500):
    image = Image.open("images\\" + img)

    ratio = width / image.width
    resized_img = image.resize((int(image.width * ratio), int(image.height * ratio)))
    #  print(resized_img.width, resized_img.height)

    return resized_img


# objects

frame_ts = ttk.Frame(root)
frame_rs = ttk.Frame(root, borderwidth=3)

# rs_tabs = ttk.Notebook(frame_rs)

images = [n for n in os.listdir("images")]
image_num = 0

current_rock = ImageTk.PhotoImage(load_image(images[0]))

ts_title = ttk.Label(frame_ts, text="Welcome, judge, to\n"
                                    "The Official Rock Judging GUI!",
                                    font=35, justify="center")
ts_btn = ttk.Button(frame_ts, text="Begin Judging", command=lambda: load_scene(1))

rs_title = ttk.Label(frame_rs, text="Look at this here Rock!!")
rs_rockpic = ttk.Label(frame_rs, image=current_rock)

# draw

ts_title.pack(padx=25, pady=12)
ts_btn.pack(padx=25, pady=13)

rs_title.grid(row=0, column=0, columnspan=2)
rs_rockpic.grid(row=1, column=0)

frame_ts.grid(row=0, column=0, sticky="nesw")
frame_rs.grid(row=0, column=0, sticky="nesw")

load_scene(0)

root.mainloop()
