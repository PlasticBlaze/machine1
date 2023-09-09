# Robot navigation & control

## Overview

This project involves controlling a robot's navigation and operation based on input from a RealSense camera and GPS data. The robot is intended to perform tasks within predefined boundaries and make decisions based on its location within those boundaries.

## Requirements

### Software

    - Python 3.x
    - Libraries: pyrealsense2, numpy, OpenCV (cv2), pandas, shapely, tkinter, serial, ublox_gps

### Hardware

    - Raspberry Pi Board
    - Ublox GPS Module
    - RealSense Camera

## Setup

0. Create a working directory

    ```bash
        mkdir projects
        cd projects
    ```

1. Clone the following repository:

    ```bash
        git clone https://github.com/PlasticBlaze/machine1.git
        cd machine1
    ```

2. Install the needed libraries
    
    ```bash
        sudo pip3 install -r requirements.txt
    ```

3. Install RealSense drivers
   [Raspberry Pi 4](https://github.com/datasith/Ai_Demos_RPi/wiki/Raspberry-Pi-4-and-Intel-RealSense-D435)
   [Issue](https://github.com/IntelRealSense/librealsense/issues/10033)

4. Run the script

    ```bash
        sudo python3 main.py
    ```

5. Configure the necessary hardware (connect the RealSense camera and the GPS device).

## Usage

### Program Flow

- HMI: The user selects a hole through an HMI interface. The selection is based on an array of coordinates stored in a CSV file. These coordinates define the boundary for the robot's current location.

- Loop: The program enters a loop.

- Travel Function (to be added later): Moves the robot to a new location that allows capturing a new image.

- getPoint: Retrieves the current location (GPS coordinates) and returns them for further processing.

- Check: Compares the current location against boundary coordinates. If the current location is outside the boundaries, the ReverseTravel function is executed.

- Routine:
  - Captures an image using a Realsense camera and processes it with OpenCV.
  - Identifies contours in the image and positions the robot over the target contour. 
  - Captures another image to confirm proper alignment with the contour.

- Tool Offset (commented out for now): A placeholder for adjusting robot movements to align the tool with the center of the image. This offset is applied to ensure accurate alignment of the tool with the identified contour.

- Fix Divot (commented out for now): A placeholder for a function that drives a servo with an attached tool for fixing the contour. This part will be implemented later.

### Functions

- HMI: The HMI interface consists of 18 buttons that allow the user to select a hole based on coordinates from a CSV file. The selected coordinates define the current boundary for the robot's location.

- Travel Function (to be added later): This function moves the robot's stepper motors to capture a new image. The movement is controlled by pulse counts, ensuring adequate coverage of the inspection area.

- Routine: Combines Realsense image capture and OpenCV processing. It captures images, identifies contours, positions the robot, and confirms alignment with another image.

- getPoint: Receives the current GPS location and provides the coordinate point for boundary checking.

- Check: Compares the current location with the boundary coordinates to ensure the robot stays within the defined area.

- xMoveRefinement and yMoveRefinement: These functions are similar to xMove and yMove but include a threshold. The threshold prevents unnecessary movements if the contour is already aligned along one axis. This refinement can be further developed later.

- Tool Offset: Reserved for adjusting robot movements to align the tool with the center of the image. It compensates for the offset between the tool and image center, improving accuracy.

- FixDivot: This function, when implemented, will control a servo with an attached tool for fixing contours. The servo-driven tool will perform the contour correction.

### Execution

Run the `./tests/compatibleWrong.py` function to start the process.

<!---
comments syntax

### machine1

I think the combinedWrong.py is the latest where I began putting everything together so I would work from that. 

From a program flow perspective, please break code into functions that make sense if needed. If the 'routine' function includes to much code, just break it into multiple functions if needed. I was building one part at a time so it might seem really confusing. Sorry about that.

***********************************************************
Program Flow 

HMI - Let user make selection for the hole

loop >

Travel function - Moves robot to new location

getPoint - gets current location

check - current location checked against boundary coordinates - if not, run ReverseTravel function

routine - takes image and finds contour to fix - currently this immediately sends step counts to arduino. Re-take image to confirm we centered the imager to the found contour, if not/ move again until it is.

tool offset - just leave this commented out for now in the overall program and I will add later

fix divot - fixes contour, just leave this commented out for now in the overall program and I will add later

< loop

***********************************************************



Functions 
(HMI): The current HMI is just 18 buttons right now, that should reference a csv file somewhere on the documents that contains an array of coordinates. The array of coordinates should be stored so that throughout the program running, it can be referenced as a boundary to the current location of the robot.

(Travel): I will add this later just leave it commented out please. I need a new function called travel that will move all 4 stepper motors far enough to get a new image. For example, if the image frame is 3 feet in height, the pulse count will be enough to travel greater than 3 feet so that a new area is being inspected. I can add the number of pulses later but it should be similar to the current comms() function. the serial write variables will just be fixed amounts. there might be multiple travel commands such as the routine one then an error handling one for when the current position is outside of the boundaries (ReverseTravel?)

(Routine): Runs realsense capture and OpenCV portion. After we take the first image and it finds a contour and moves the robot over top of it, I want it to take another image to confirm we centered the contour to the imager.

(getPoint): this function recieves current GPS location and needs to return the current coordinate point to be checked against the boundary

(check): checks current location

*(xMoveRefinement and yMoveRefinement): Same as (xMove and yMove) but has a threshold. Maybe the threshold should also be set on the initial movements too so that if the divot is aligned on either of the axis, it won’t try to move. ***We can work on this later***

*(Tool Offset): This is because the movements are intended to align the divot with the center of the image taken. The divot fixing tool obviously cannot be in the center of the image so I imagined it offset some distance that the bot will need to travel in order to actually align the divot and tool. ***We can work on this later***

*(FixDivot): This function will be driving the servo with tool attached. ***I can work on this later***

--->