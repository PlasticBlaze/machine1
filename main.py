"""
Main routine
"""
import json
import time
from math import pi
from tkinter import Button, Tk

import cv2
import numpy as np
import pandas as pd
import pyrealsense2 as rs
import serial
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from ublox_gps import UbloxGps

PROJECT_PATH = "/home/pi/machine"
PORT_SERIAL = "/dev/serial0"


def tool_ofset():
    """
    Further description in the future
    """
    print("tool_ofset processing")


def fix_divot():
    """
    Further description in the future
    """
    print("fix_divot processing")


def routine():
    """
    Takes image and finds contour to fix - currently this immediately sends step counts to arduino.
    Re-take image to confirm we centered the imager to the found contour,
    if not/ move again until it is.
    """
    # Sets threshold for min & max divot size to fix (units: Pixels)
    min_divot = 125
    # Sets resized pixel count for x and y axis
    p_x = int(848)
    p_y = int(480)
    # Determines center point of captured image to reference the divot coordinates off of.
    # Using resized image pixel count (x, y), find center
    # These parameters will be update once the final design is established

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

    # Start streaming
    cfg = pipeline.start(config)
    device = cfg.get_device()

    json_file = json.load(
        open(
            f"{PROJECT_PATH}/src/config/json_string_testing.json",
            encoding="utf-8",
        )
    )
    json_string = str(json_file).replace("'", '"')
    advanced_mode = rs.rs400_advanced_mode(device)
    advanced_mode.load_json(json_string)

    try:
        start = time.time()
        while time.time() - start < 20:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            # color_frame = frames.get_color_frame()

            # Convert images to numpy arrays
            colorizer = rs.colorizer()
            # colorizer.set_option(rs.option.histogram_equalization_enabled, 1)
            colorizer.set_option(rs.option.visual_preset, 3)
            colorizer.set_option(rs.option.color_scheme, 2)
            colorizer.set_option(rs.option.min_distance, 0.365)
            colorizer.set_option(rs.option.max_distance, 0.385)
            depth_image = np.asanyarray(colorizer.colorize(depth_frame).get_data())
            # color_image = np.asanyarray(color_frame.get_data())
            cv2.imwrite(f"{PROJECT_PATH}/data/images/frame1.jpg", depth_image)

            # Show images
            # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            # cv2.imshow('RealSense', depth_image)
            # cv2.imshow('color', color_image)
            cv2.waitKey(1)

            blur = cv2.blur(depth_image, (6, 6))
            rblur = cv2.resize(blur, (424, 240))

            # Statistics based approach
            mean = np.mean(blur, axis=(0, 1))
            std = np.std(blur, axis=(0, 1))
            mask = (np.abs(blur - mean) / std >= 4.5).any(axis=2)
            mask_u8 = (255 * mask).astype(np.uint8)
            rmask_u8 = cv2.resize(mask_u8, (p_x, p_y))

            # Creates physical coordinate conversion factor from pixels to mm. Assuming 3 ft x 4 ft is image area.
            # Convert image to mm scale. = 914.4 mm x 1219.2 mm. Now cm scale
            PtoCM_Scale = 75 / p_x
            print(PtoCM_Scale)

            # Find contours using statistics, creates image to show contours.
            contours, _ = cv2.findContours(
                rmask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
            )
            canvas = cv2.cvtColor(rmask_u8, cv2.COLOR_GRAY2BGR)
            rcanvas = cv2.resize(canvas, (p_x, p_y))

            frameCentroidX = int(p_x / 2)
            frameCentroidY = int(p_y / 2)
            frameCentroid = (frameCentroidX, frameCentroidY)
            print(f"frameCentroid: {frameCentroid}")

            # For any contours found in the mask, draw bounding rectangle and find center of contour.
            # Divot area parameter filters out divots too small or too large.

            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            rectArea = w * h
            divotArea = np.int0(rectArea)
            # print("divotarea: ", divotArea)
            if np.any(divotArea > min_divot):
                # Calculates centroid of each divot found that satisfies divot size parameters.
                M = cv2.moments(c)
                while M["m00"] == 0:
                    continue
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Prints results for each divot on canvas as well as result box later on.
                print("cX: ", cX)
                print("cY: ", cY)

            # Draws contours, bounding boxes, and a circle to notate the center of mass for the contour.
            cv2.drawContours(rcanvas, c, -1, (0, 255, 0), 1)
            cv2.rectangle(rcanvas, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.circle(rcanvas, (cX, cY), 2, (0, 0, 255), -1)
            # Shows contour centroids in pixel coordinates above contour.
            text_x = f"x: {str(cX)}"
            text_y = f"y: {str(cY)}"
            cv2.putText(
                rcanvas,
                text_x,
                (cX - -20, cY - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.3,
                (0, 255, 255),
                1,
            )
            cv2.putText(
                rcanvas,
                text_y,
                (cX - -20, cY - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.3,
                (0, 255, 255),
                1,
            )

            # Calculating the distance from center of contour to center of frame for both x and y directions.
            # These calculations will control the movement to the divot for amendment.

            if np.any(cX > frameCentroidX):
                x_dist = cX - frameCentroidX
                x_dist_cm = x_dist * PtoCM_Scale
                x_dist_cm = round(x_dist_cm, 2)
                print(f"x Distance from Center in CM: {x_dist_cm}")
            else:
                x_dist = cX - frameCentroidX
                x_dist_cm = x_dist * PtoCM_Scale
                x_dist_cm = round(x_dist_cm, 2)
                print(f"x Distance from Center in CM: {x_dist_cm}")

            if np.any(cY > frameCentroidY):
                y_dist = cY - frameCentroidY
                y_dist_cm = (y_dist * PtoCM_Scale) * -1
                y_dist_cm = round(y_dist_cm, 2)
                print(f"y Distance from Center in CM: {y_dist_cm}")
            else:
                y_dist = cY - frameCentroidY
                y_dist_cm = (y_dist * PtoCM_Scale) * -1
                y_dist_cm = round(y_dist_cm, 2)
                print(f"y Distance from Center in CM: {y_dist_cm}")

            cv2.drawMarker(
                rcanvas, frameCentroid, (255, 255, 255), cv2.MARKER_CROSS, 10, 1
            )
            # rmask_u8 = cv2.resize(mask_u8, (pX, pY))
            cv2.imshow(f"Canvas {rcanvas}")
            # cv2.imshow("Big Mask", rmask_u8)
            # cv2.imshow("Blur", rblur)

            # Diameter of wheel is 97mm currently
            # 1026 pulses is 1 stepper rotation

            wheel_diameter = 97
            wheel_circumference = wheel_diameter * pi
            wheel_circumference = round(wheel_circumference, 5)
            rotation_param = wheel_circumference / 1000
            print(rotation_param)

            x_pulse_calc = x_dist_cm / rotation_param
            x_pulse_calc = round(x_pulse_calc)
            y_pulse_calc = y_dist_cm / rotation_param
            y_pulse_calc = round(y_pulse_calc)
            print(f"Number of pulses in x direction: {x_pulse_calc}")
            print(f"Number of pulses in y direction: {y_pulse_calc}")

            y_pulse_calc = str(y_pulse_calc)
            y_pulse_calc = str("YMOV:" + y_pulse_calc + ":0")
            y_pulse_encode = y_pulse_calc.encode()
            print(y_pulse_encode)

            x_pulse_calc = str(x_pulse_calc)
            x_pulse_calc = str("XMOV:" + x_pulse_calc + ":0")
            x_pulse_encode = x_pulse_calc.encode()
            print(x_pulse_encode)

    finally:
        # Stop streaming
        pipeline.stop()


def getpoint():
    port = serial.Serial(PORT_SERIAL, baudrate=38400, timeout=1)
    gps = UbloxGps(port)

    max_time = 5
    start_time = time.time()

    data_lat_sum = []
    data_lon_sum = []

    try:
        print("Listening for UBX Messages")
        while (time.time() - start_time) < max_time:
            try:
                geo = gps.geo_coords()
                print("Longitude: ", geo.lon)
                print("Latitude: ", geo.lat)
                # print("Heading of Motion: ", geo.headMot)
                data_lat_sum.append(float(geo.lat))
                data_lon_sum.append(float(geo.lon))
            except (ValueError, IOError) as err:
                print(err)

    finally:
        port.close()
        avgLatCoord = sum(data_lat_sum) / len(data_lat_sum)
        avgLonCoord = sum(data_lon_sum) / len(data_lon_sum)
        print("Average Lat: ", avgLatCoord)
        print("Average Lon: ", avgLonCoord)
        point1 = Point("avgLatCoord", "avgLonCoord")
        return point1


def check(point1):
    """
    Function to check if the robot is still within the boundaries,
    if false, turn around and get back in
    if true, continue routine of fixing
    """
    # polygon = coordinateFile(x)
    print(polygon)
    # point = getPoint()
    print(point1)
    pos_check = polygon.contains(point1)
    print(pos_check)


def travel_robot():
    print("Traveling robot by controlling arduino")


def HMI():
    """
    One time UI selection on start up where worker selects what hole they are on,
    based on button selection it will pull the csv file that contains the coordinates
    of each hole and store it as polygon.
    """
    root = Tk()
    root.title("Select Hole")

    def coordinate_file(x):
        global polygon
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
            polygon = Polygon(lats_long_array)

            travel_robot()
            check(polygon)
            routine()

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


if __name__ == "__main__":
    HMI()