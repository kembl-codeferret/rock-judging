from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import os
import csv

# import gdown

root = Tk(className="rock judging time !")
with open("K24ROTY Submission Form.csv", newline='') as csvfile:
    rock_reader = csv.reader(csvfile)
    rock_lines = [n for n in rock_reader]


for line in range(len(rock_lines)):
    if line > 0:
        # gdown.download('uc'.join(rock_lines[line][4].split('open')), "images/" + rock_lines[line][4].split('=')[1])
        rock_lines[line][4] = rock_lines[line][4].split('=')[1]


def load_scene(scene):
    match scene:
        case 0:
            frame_ts.tkraise()
        case 1:
            frame_rs.tkraise()
        case 2:
            frame_es.tkraise()


def load_image(index, width=500):
    image = Image.open('images/' + rock_lines[index + 1][4] + ".jpg")

    ratio = width / image.width
    resized_img = image.resize((int(image.width * ratio), int(image.height * ratio)))
    #  print(resized_img.width, resized_img.height)

    return resized_img


def load_rock(index):
    global image_num, judging_data

    judging_data.append([rock_lines[image_num+1][1], rock_lines[image_num+1][2], rs_R1.get(), rs_R2.get(), rs_R3.get()])

    try:
        rs_description.config(text="Rock description:\n" + change_desc(index + 1))
        rs_story.config(text="Rock story:\n" + change_story(index + 1))

        new_img = ImageTk.PhotoImage(load_image(index + 1))
        rs_rockpic.config(image=new_img)
        rs_rockpic.image = new_img

        image_num += 1
    except IndexError:
        load_scene(2)


def change_image(index):
    return load_image(index)


def change_desc(index):
    return rock_lines[index + 1][2]


def change_story(index):
    return rock_lines[index + 1][3]


def final():
    global judge_name
    if len(es_entry.get()) > 1: judge_name = es_entry.get()
    root.destroy()


image_num = 0
current_rock = ImageTk.PhotoImage(load_image(image_num))

judge_name = "left blank, fuckign nerd"
judging_data = [
    ["contestant name", "rock id", "cool score", "color score", "story score"]
]

# objects

frame_ts = ttk.Frame(root)
frame_rs = ttk.Frame(root, borderwidth=3)
frame_es = ttk.Frame(root)

rs_scores = ttk.Frame(frame_rs)

desc_text = change_desc(image_num)
story_text = change_story(image_num)

ts_title = ttk.Label(frame_ts, text="Welcome, judge, to\n"
                                    "The Official Rock Judging GUI!",
                                    font=35, justify="center")
ts_btn = ttk.Button(frame_ts, text="Begin Judging", command=lambda: load_scene(1))

es_title = ttk.Label(frame_es, text="Thank you for judging!\nPlease enter your name here:", font=35, justify="center")
es_entry = ttk.Entry(frame_es)
es_btn = ttk.Button(frame_es, text="exit program", command=final)

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

es_title.pack(padx=25, pady=12)
es_entry.pack(padx=25)
es_btn.pack(padx=25, pady=13)

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
frame_es.grid(row=0, column=0, sticky="nesw")

load_scene(0)

root.mainloop()

with open("KRA24 Judging Form - " + judge_name + ".csv", 'w', newline='') as csvfile:
    rock_writer = csv.writer(csvfile)
    rock_writer.writerows(judging_data)
