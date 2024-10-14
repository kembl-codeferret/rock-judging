from tkinter import *
from tkinter import ttk
import os, csv

w = Tk(className="rock judging time !")

def scene2():
    pass

# objects

TS_Title = ttk.Label(text="Welcome, judge, to\nThe Official Rock Judging GUI!", font=35)
TS_Button = ttk.Button(text="Begin Judging", command=scene2)

# draw

TS_Title.pack(padx=25,pady=12)
TS_Button.pack(padx=25, pady=13)

w.mainloop()
