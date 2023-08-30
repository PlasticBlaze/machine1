# A little back ground, I'm trying to make an automated ball mark repair robot for golf course greens.
# This portion is for location control of the robot. ie. how it knows to stay on the green. I determined vision might
# be too hard for that part as I want the robot to be able to be used at night time.

# This file works right now but it doesn't necessarily do what I want it to. There is probably a way better way of
# writing it as well, the problem is I'm learning everything as I go and it's taking me soooooo long.

from tkinter import *

import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

root = Tk()
root.title("Select Hole")


# This will be where, when called, the gps coordinates will be parsed and put into the shapely.geometry 'Point'
# for point in polygon from the GPS unit I have. I'm just using this test point for now
def getPoint():
    point1 = Point(-85.5911993, 38.2348362)
    return point1


# This will be a one time UI selection on start up where worker selects what hole they are on, based on button
# selection it will pull the csv file that contains the coordinates of each hole and store it as polygon.
def coordinateFile(x):
    global polygon
    if x == 1:
        csvX = pd.read_csv(
            "C:\\Users\\lysackb\\Documents\\Python Scripts\\HCC1-1.csv",
            usecols=[0],
            header=0,
        )
        numpX = csvX.to_numpy()
        csvY = pd.read_csv(
            "C:\\Users\\lysackb\\Documents\\Python Scripts\\HCC1-1.csv",
            usecols=[1],
            header=0,
        )
        numpY = csvY.to_numpy()
        lats_long_array = np.column_stack((numpX, numpY))
        polygon = Polygon(lats_long_array)
        Check(polygon)
    elif x == 2:
        csv = pd.read_csv(
            "C:\\Users\\lysackb\\Documents\\Python Scripts\\testfile.csv", header=0
        )
        print(csv)


# this is the function that I want to be called after getPoint is called at some point in the program
# to check and see if the robot is still within the boundaries, if false, turn around and get back in (maybe I'll
# add some distance calculations)/ if true, continue routine of fixing
def Check(polygon):
    # polygon = coordinateFile(x)
    print(polygon)
    point = getPoint()
    print(point)
    posCheck = polygon.contains(point)
    print(posCheck)


# Defining buttons
button_1 = Button(
    root,
    text=" 1 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(1),
    fg="#ffffff",
    bg="#355e3b",
)
button_2 = Button(
    root,
    text=" 2 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(2),
    fg="#ffffff",
    bg="#355e3b",
)
button_3 = Button(
    root,
    text=" 3 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(3),
    fg="#ffffff",
    bg="#355e3b",
)
button_4 = Button(
    root,
    text=" 4 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(4),
    fg="#ffffff",
    bg="#355e3b",
)
button_5 = Button(
    root,
    text=" 5 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(5),
    fg="#ffffff",
    bg="#355e3b",
)
button_6 = Button(
    root,
    text=" 6 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(6),
    fg="#ffffff",
    bg="#355e3b",
)
button_7 = Button(
    root,
    text=" 7 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(7),
    fg="#ffffff",
    bg="#355e3b",
)
button_8 = Button(
    root,
    text=" 8 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(8),
    fg="#ffffff",
    bg="#355e3b",
)
button_9 = Button(
    root,
    text=" 9 ",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(9),
    fg="#ffffff",
    bg="#355e3b",
)
button_10 = Button(
    root,
    text="10",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(10),
    fg="#ffffff",
    bg="#355e3b",
)
button_11 = Button(
    root,
    text="11",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(11),
    fg="#ffffff",
    bg="#355e3b",
)
button_12 = Button(
    root,
    text="12",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(12),
    fg="#ffffff",
    bg="#355e3b",
)
button_13 = Button(
    root,
    text="13",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(13),
    fg="#ffffff",
    bg="#355e3b",
)
button_14 = Button(
    root,
    text="14",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(14),
    fg="#ffffff",
    bg="#355e3b",
)
button_15 = Button(
    root,
    text="15",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(15),
    fg="#ffffff",
    bg="#355e3b",
)
button_16 = Button(
    root,
    text="16",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(16),
    fg="#ffffff",
    bg="#355e3b",
)
button_17 = Button(
    root,
    text="17",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(17),
    fg="#ffffff",
    bg="#355e3b",
)
button_18 = Button(
    root,
    text="18",
    padx=40,
    pady=40,
    command=lambda: coordinateFile(18),
    fg="#ffffff",
    bg="#355e3b",
)

# Placing buttons
button_1.grid(row=1, column=1)
button_2.grid(row=1, column=2)
button_3.grid(row=1, column=3)
button_4.grid(row=1, column=4)
button_5.grid(row=1, column=5)
button_6.grid(row=1, column=6)
button_7.grid(row=1, column=7)
button_8.grid(row=1, column=8)
button_9.grid(row=1, column=9)
button_10.grid(row=2, column=1)
button_11.grid(row=2, column=2)
button_12.grid(row=2, column=3)
button_13.grid(row=2, column=4)
button_14.grid(row=2, column=5)
button_15.grid(row=2, column=6)
button_16.grid(row=2, column=7)
button_17.grid(row=2, column=8)
button_18.grid(row=2, column=9)

root.mainloop()

getPoint()
coordinateFile()
Check(polygon)
