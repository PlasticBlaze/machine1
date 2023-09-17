# This was my initial openCV portion I wrote and was just using an iphone image to test the contour finding and
# stuff so I might have to redo some of it because now I'm using the depth camera


import pyrealsense2 as rs
import numpy as np
import cv2
import json
import time
import math
import serial

# Sets threshold for min & max divot size to fix (units: Pixels)
minDivot = 125
# Sets resized pixel count for x and y axis
pX = int(848)
pY = int(480)
# Determines center point of captured image to reference the divot coordinates off of.
# Using resized image pixel count (x, y), find center

# Global constants
PROJECT_PATH = "/home/plasticblaze/projects/machine1"


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' These are parameters to update once the final design is established                 '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def decodestr(inputstr):
    inputstr = inputstr.decode("utf-8")
    inputstr = inputstr.replace("\n","")
    inputstr = inputstr.replace("\r", "")
    inputstr = inputstr.replace("'b","")
    return inputstr


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
#config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
# Start streaming
cfg = pipeline.start(config)
device = cfg.get_device()

json = json.load(open(f"{PROJECT_PATH}/tests/json_stringTesting.json",
            encoding="utf-8",
        )
    )
json_string= str(json).replace("'", '\"')
advanced_mode = rs.rs400_advanced_mode(device)
advanced_mode.load_json(json_string)

try:
    start = time.time()
    while time.time() - start < 20:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        #color_frame = frames.get_color_frame()

        # Convert images to numpy arrays
        colorizer = rs.colorizer()
        #colorizer.set_option(rs.option.histogram_equalization_enabled, 1)
        colorizer.set_option(rs.option.visual_preset, 3)
        colorizer.set_option(rs.option.color_scheme, 2)
        colorizer.set_option(rs.option.min_distance, 0.365)
        colorizer.set_option(rs.option.max_distance, 0.385)
        depth_image = np.asanyarray(colorizer.colorize(depth_frame).get_data())
        #color_image = np.asanyarray(color_frame.get_data())
        cv2.imwrite('/home/plasticblaze/Pictures/frame1.jpg', depth_image)


        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', depth_image)
        #cv2.imshow('color', color_image)
        cv2.waitKey(1)

        blur = cv2.blur(depth_image, (6, 6))
        rblur = cv2.resize(blur, (424, 240))

        # Statistics based approach
        mean = np.mean(blur, axis=(0, 1))
        std = np.std(blur, axis=(0, 1))
        mask = (np.abs(blur - mean) / std >= 4.5).any(axis=2)
        mask_u8 = (255 * mask).astype(np.uint8)
        rmask_u8 = cv2.resize(mask_u8, (pX, pY))

        # Creates physical coordinate conversion factor from pixels to mm. Assuming 3 ft x 4 ft is image area.
        # Convert image to mm scale. = 914.4 mm x 1219.2 mm. Now cm scale
        PtoCM_Scale = 75 / pX
        #print(PtoCM_Scale)

        # Find contours using statistics, creates image to show contours.
        '''contours, _ = cv2.findContours(rmask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        canvas = cv2.cvtColor(rmask_u8, cv2.COLOR_GRAY2BGR)
        rcanvas = cv2.resize(canvas, (pX, pY))

        frameCentroidX = int(pX / 2)
        frameCentroidY = int(pY / 2)
        frameCentroid = (frameCentroidX, frameCentroidY)
        print("frameCentroid: ", frameCentroid)

        # For any contours found in the mask, draw bounding rectangle and find center of contour.
        # Divot area parameter filters out divots too small or too large.

        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        rectArea = w * h
        divotArea = np.int0(rectArea)
        #print("divotarea: ", divotArea)
        if np.any(divotArea > minDivot):
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
        textX = "x: " + str(cX)
        textY = "y: " + str(cY)
        cv2.putText(rcanvas, textX, (cX - -20, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
        cv2.putText(rcanvas, textY, (cX - -20, cY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)

        # Calculating the distance from center of contour to center of frame for both x and y directions.
        # These calculations will control the movement to the divot for amendment.

        if np.any(cX > frameCentroidX):
            xDistance = (cX - frameCentroidX)
            xDistanceCM = (xDistance * PtoCM_Scale)
            xDistanceCM = round(xDistanceCM, 2)
            print("x Distance from Center in CM:", xDistanceCM)
        else:
            xDistance = (cX - frameCentroidX)
            xDistanceCM = (xDistance * PtoCM_Scale)
            xDistanceCM = round(xDistanceCM, 2)
            print("x Distance from Center in CM:", xDistanceCM)

        if np.any(cY > frameCentroidY):
            yDistance = (cY - frameCentroidY)
            yDistanceCM = ((yDistance * PtoCM_Scale) * -1)
            yDistanceCM = round(yDistanceCM, 2)
            print("y Distance from Center in CM:", yDistanceCM)
        else:
            yDistance = (cY - frameCentroidY)
            yDistanceCM = ((yDistance * PtoCM_Scale) * -1)
            yDistanceCM = round(yDistanceCM, 2)
            print("y Distance from Center in CM:", yDistanceCM)

        cv2.drawMarker(rcanvas, frameCentroid, (255, 255, 255), cv2.MARKER_CROSS, 10, 1)
        #rmask_u8 = cv2.resize(mask_u8, (pX, pY))
        cv2.imshow("Canvas", rcanvas)'''
        cv2.imshow("Big Mask", rmask_u8)
        cv2.imshow("Blur", rblur)
        '''
        '''''''''''''''''''''''''''''''''''''''''''''''
        'Diameter of wheel is 97mm currently          '
        '1026 pulses is 1 stepper rotation             '
        '''''''''''''''''''''''''''''''''''''''''''''''
        wheelDiameter = 97
        wheelCircumference = (wheelDiameter * math.pi)
        wheelCircumference = round(wheelCircumference, 5)
        rotationParam = (wheelCircumference / 1000)
        print(rotationParam)

        XpulseCalc = (xDistanceCM / rotationParam)
        XpulseCalc = round(XpulseCalc)
        YpulseCalc = (yDistanceCM / rotationParam)
        YpulseCalc = round(YpulseCalc)
        print("Number of pulses in x direction:", XpulseCalc)
        print("Number of pulses in y direction:", YpulseCalc)

        YpulseCalc = str(YpulseCalc)
        YpulseCalc = str("YMOV:" + YpulseCalc + ":0")
        YpulseEncode = YpulseCalc.encode()
        print(YpulseEncode)

        XpulseCalc = str(XpulseCalc)
        XpulseCalc = str("XMOV:" + XpulseCalc + ":0")
        XpulseEncode = XpulseCalc.encode()
        print(XpulseEncode)

        '''''''''''''''''''''''''''''''''''''''''''''''''''
        ' Beginning Data Transmission                     '
        '''''''''''''''''''''''''''''''''''''''''''''''''''

        #serial1 = serial.Serial('/dev/ttyACM0', 115200)
        #time.sleep(2)
        #serial1.flush()

        #serial1.write(YpulseEncode)
        #while True:
            #AReply = decodestr(serial1.readline())
            #print(AReply)
            #if AReply == "Done":
                #break

        #serial1.write(XpulseEncode)
        #while True:
            #AReply = decodestr(serial1.readline())
            #print(AReply)
            #if AReply == "Done":
                #break

'''
finally:
    # Stop streaming
    pipeline.stop()
