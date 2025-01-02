from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import os
import csv

import gdown

root = Tk(className="rock judging time !")
with open("K24ROTY Submission Form.csv", newline='') as csvfile:
    rock_reader = csv.reader(csvfile)
    rock_lines = [n for n in rock_reader]

for line in range(len(rock_lines)):
    if line > 0:
        gdown.download('uc'.join(rock_lines[line][2].split('open')), "images/" + rock_lines[line][2].split('=')[1])
        rock_lines[line][2] = rock_lines[line][2].split('=')[1]


def load_scene(scene):
    match scene:
        case 0:
            frame_ts.tkraise()
        case 1:
            frame_rs.tkraise()


def load_image(index, width=500):
    image = Image.open('images/' + rock_lines[index + 1][2])

    ratio = width / image.width
    resized_img = image.resize((int(image.width * ratio), int(image.height * ratio)))
    #  print(resized_img.width, resized_img.height)

    return resized_img


def load_rock(index):
    rs_description.config(text=change_desc(index + 1))
    rs_story.config(text=change_story(index + 1))

    new_img = ImageTk.PhotoImage(load_image(index + 1))
    rs_rockpic.config(image=new_img)
    rs_rockpic.image = new_img
    # image_num += 1


def change_image(index):
    return load_image(index)

def change_desc(index):
    return rock_lines[index + 1][3]

def change_story(index):
    return rock_lines[index + 1][4]

# objects

frame_ts = ttk.Frame(root)
frame_rs = ttk.Frame(root, borderwidth=3)

rs_scores = ttk.Frame(frame_rs)

image_num = 0

current_rock = ImageTk.PhotoImage(load_image(image_num))

desc_text = change_desc(image_num)
story_text = change_story(image_num)

ts_title = ttk.Label(frame_ts, text="Welcome, judge, to\n"
                                    "The Official Rock Judging GUI!",
                                    font=35, justify="center")
ts_btn = ttk.Button(frame_ts, text="Begin Judging", command=lambda: load_scene(1))

rs_title = ttk.Label(frame_rs, text="Look at this here Rock!!")
rs_rockpic = ttk.Label(frame_rs, image=current_rock)

rs_R1 = ttk.Entry(rs_scores)
rs_R2 = ttk.Entry(rs_scores)
rs_R3 = ttk.Entry(rs_scores)
rs_submit = ttk.Button(rs_scores, text="Enter Scores", command=lambda: load_rock(image_num))

rs_description = ttk.Label(frame_rs, text="Rock description:\n" + desc_text, wraplength=500, justify="center")
rs_story = ttk.Label(frame_rs, text="Rock story:\n" + story_text, wraplength=500, justify="center")

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
