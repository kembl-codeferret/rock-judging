from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import os, csv

root = Tk(className="rock judging time !")


def load_scene(scene):
    match scene:
        case 0:
            frame_ts.tkraise()
        case 1:
            frame_rs.tkraise()


def set_image(cmd):
    pass



# objects

frame_ts = ttk.Frame(root)
frame_rs = ttk.Frame(root)

images = [n for n in os.listdir("images")]
current_img = Image.open("images\\" + images[0])
current_img = ImageTk.PhotoImage(current_img)

ts_title = ttk.Label(frame_ts, text="Welcome, judge, to\n"
                          "The Official Rock Judging GUI!", font=35)
ts_btn = ttk.Button(frame_ts, text="Begin Judging", command=lambda: load_scene(1))

rs_title = ttk.Label(frame_rs, text="This the rock screen ig")
rs_rockpic = ttk.Label(frame_rs, image=current_img)

# draw

ts_title.pack(padx=25, pady=12)
ts_btn.pack(padx=25, pady=13)

rs_title.pack(padx=10, pady=10)
rs_rockpic.pack(padx=10, pady=10)

frame_ts.grid(row=0, column=0, sticky="nesw")
frame_rs.grid(row=0, column=0, sticky="nesw")

load_scene(0)

root.mainloop()
