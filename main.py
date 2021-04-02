# This was my initial openCV portion I wrote and was just using an iphone image to test the contour finding and
# stuff so I might have to redo some of it because now I'm using the depth camera

import cv2
import numpy as np
import serial
import math
import time

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' These are parameters to update once the final design is established                 '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Sets threshold for min & max divot size to fix (units: Pixels)
minDivot = 135
# Sets resized pixel count for x and y axis
pX = int(512)
pY = int(768)
# Determines center point of captured image to reference the divot coordinates off of.
# Using resized image pixel count (x, y), find center


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' These are parameters to update once the final design is established                 '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def decodestr(inputstr):
    inputstr = inputstr.decode("utf-8")
    inputstr = inputstr.replace("\n","")
    inputstr = inputstr.replace("\r", "")
    inputstr = inputstr.replace("'b","")
    return inputstr

# Read in the image in YCrCb, also show default
img = cv2.imread('/home/pi/Downloads/divot2.jpeg', cv2.IMREAD_COLOR)
imgS = cv2.resize(img, (pX, pY))
aimg = cv2.imread('/home/pi/Downloads/divot2.jpeg', cv2.COLOR_BGR2YCrCb)

# Blur image to reduce noise and resize for viewing
blur = cv2.blur(aimg, (6, 6))
rblur = cv2.resize(blur, (384, 512))

# Statistics based approach
mean = np.mean(blur, axis=(0, 1))
std = np.std(blur, axis=(0, 1))
mask = (np.abs(blur - mean) / std >= 4.5).any(axis=2)
mask_u8 = (255 * mask).astype(np.uint8)
rmask_u8 = cv2.resize(mask_u8, (pX, pY))

# Creates physical coordinate conversion factor from pixels to mm. Assuming 3 ft x 4 ft is image area.
# Convert image to mm scale. = 914.4 mm x 1219.2 mm. Now cm scale
PtoCM_Scale = 91.44 / pX
print(PtoCM_Scale)

# Find contours using statistics, creates image to show contours.
contours, _ = cv2.findContours(rmask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
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

'''''''''''''''''''''''''''''''''''''''''''''''
'Diameter of wheel is 60mm currently          '
'200 pulses is 1 stepper rotation             '
'''''''''''''''''''''''''''''''''''''''''''''''
wheelDiameter = 60
wheelCircumference = ((wheelDiameter * math.pi) / 10)
wheelCircumference = round(wheelCircumference, 5)
rotationParam = (wheelCircumference / 200)
print(rotationParam)

XpulseCalc = (xDistanceCM / rotationParam)
XpulseCalc = round(XpulseCalc)
YpulseCalc = (yDistanceCM / rotationParam)
YpulseCalc = round(YpulseCalc)
print("Number of pulses in x direction:", XpulseCalc)
print("Number of pulses in y direction:", YpulseCalc)

YpulseCalc = str(YpulseCalc)
YpulseCalc = str("YMOV:" + YpulseCalc + ":0")
YpulseEncode = (YpulseCalc).encode()
print(YpulseEncode)

XpulseCalc = str(XpulseCalc)
XpulseCalc = str("XMOV:" + XpulseCalc + ":0")
XpulseEncode = (XpulseCalc).encode()
print(XpulseEncode)

'''''''''''''''''''''''''''''''''''''''''''''''''''
' Beginning Data Transmission                     '
'''''''''''''''''''''''''''''''''''''''''''''''''''

serial1 = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(3)
serial1.flush()

serial1.write(YpulseEncode)
while True:
    AReply = decodestr(serial1.readline())
    print(AReply)
    if AReply == "Done":
        break

serial1.write(XpulseEncode)
while True:
    AReply = decodestr(serial1.readline())
    print(AReply)
    if AReply == "Done":
        break
#msg = serial1.readline()
#print("Arduino Sent...")
#print(msg)

# Show each iteration of image.
cv2.drawMarker(rcanvas, frameCentroid, (255, 255, 255), cv2.MARKER_CROSS, 10, 1)
rmask_u8 = cv2.resize(mask_u8, (pX, pY))
cv2.imshow("Canvas", rcanvas)
cv2.imshow("Big Mask", rmask_u8)
cv2.imshow("Blur", rblur)
cv2.imshow("Natural", imgS)
cv2.waitKey(0)
cv2.destroyAllWindows()
