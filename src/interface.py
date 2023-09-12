"""
Script to run the interface where the hole is selected
"""

from tkinter import Button, Tk

import numpy as np
import pandas as pd
from shapely.geometry.polygon import Polygon

PROJECT_PATH = "/home/plasticblaze/projects/machine1"


def HMI():
    """
    One time UI selection on start up where worker selects what hole they are on,
    based on button selection it will pull the csv file that contains the coordinates
    of each hole and store it as polygon.
    """
    root = Tk()
    root.title("Select Hole")

    def coordinate_file(x):
        #global polygon
        if x == 1:
            df_x = pd.read_csv(
                f"{PROJECT_PATH}/data/HCC1-1.csv",
                usecols=[0],
                header=0,
            )
            x_array = df_x.to_numpy()
            df_y = pd.read_csv(
                f"{PROJECT_PATH}/data/HCC1-1.csv",
                usecols=[1],
                header=0,
            )
            y_array = df_y.to_numpy()
            lats_long_array = np.column_stack((x_array, y_array))
            print(csv)
            return Polygon(lats_long_array)

        elif x == 2:
            csv = pd.read_csv(f"{PROJECT_PATH}/data/HCC1-1.csv", header=0)
            print(csv)

    # Defining buttons
    button_1 = Button(
        root,
        text=" 1 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(1),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_2 = Button(
        root,
        text=" 2 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(2),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_3 = Button(
        root,
        text=" 3 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(3),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_4 = Button(
        root,
        text=" 4 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(4),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_5 = Button(
        root,
        text=" 5 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(5),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_6 = Button(
        root,
        text=" 6 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(6),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_7 = Button(
        root,
        text=" 7 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(7),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_8 = Button(
        root,
        text=" 8 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(8),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_9 = Button(
        root,
        text=" 9 ",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(9),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_10 = Button(
        root,
        text="10",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(10),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_11 = Button(
        root,
        text="11",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(11),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_12 = Button(
        root,
        text="12",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(12),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_13 = Button(
        root,
        text="13",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(13),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_14 = Button(
        root,
        text="14",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(14),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_15 = Button(
        root,
        text="15",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(15),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_16 = Button(
        root,
        text="16",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(16),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_17 = Button(
        root,
        text="17",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(17),
        fg="#ffffff",
        bg="#355e3b",
    )
    button_18 = Button(
        root,
        text="18",
        padx=40,
        pady=40,
        command=lambda: coordinate_file(18),
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
