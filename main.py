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

rs_scores = ttk.Frame(frame_rs)

images = [n for n in os.listdir("images")]
image_num = 0

current_rock = ImageTk.PhotoImage(load_image(images[0]))

ts_title = ttk.Label(frame_ts, text="Welcome, judge, to\n"
                                    "The Official Rock Judging GUI!",
                                    font=35, justify="center")
ts_btn = ttk.Button(frame_ts, text="Begin Judging", command=lambda: load_scene(1))

rs_title = ttk.Label(frame_rs, text="Look at this here Rock!!")
rs_rockpic = ttk.Label(frame_rs, image=current_rock)

rs_R1 = ttk.Entry(rs_scores)
rs_R2 = ttk.Entry(rs_scores)
rs_R3 = ttk.Entry(rs_scores)
rs_submit = ttk.Button(rs_scores, text="Enter Scores")

rs_description = ttk.Label(frame_rs, text="description go here")
rs_story = ttk.Label(frame_rs, text="story go here")

# draw

ts_title.pack(padx=25, pady=12)
ts_btn.pack(padx=25, pady=13)

rs_title.grid(row=0, column=0, columnspan=2)
rs_rockpic.grid(row=1, column=0)

rs_scores.grid(row=1, column=1)
rs_R1.grid(row=0, column=0)
rs_R2.grid(row=0, column=1)
rs_R3.grid(row=0, column=2)
rs_submit.grid(row=1, column=0, columnspan=3)

rs_description.grid(row=2, column=0)
rs_story.grid(row=2, column=1)


frame_ts.grid(row=0, column=0, sticky="nesw")
frame_rs.grid(row=0, column=0, sticky="nesw")

load_scene(0)

root.mainloop()
