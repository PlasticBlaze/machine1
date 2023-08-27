# machine1

I think the combinedWrong.py is the latest where I began putting everything together so I would work from that. 

From a program flow perspective, please break code into functions that make sense if needed. If the 'routine' function includes to much code, just break it into multiple functions if needed. I was building one part at a time so it might seem really confusing. Sorry about that.

***********************************************************
Program Flow -->

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



Functions -->
(HMI): The current HMI is just 18 buttons right now, that should reference a csv file somewhere on the documents that contains an array of coordinates. The array of coordinates should be stored so that throughout the program running, it can be referenced as a boundary to the current location of the robot.

(Travel): I will add this later just leave it commented out please. I need a new function called travel that will move all 4 stepper motors far enough to get a new image. For example, if the image frame is 3 feet in height, the pulse count will be enough to travel greater than 3 feet so that a new area is being inspected. I can add the number of pulses later but it should be similar to the current comms() function. the serial write variables will just be fixed amounts. there might be multiple travel commands such as the routine one then an error handling one for when the current position is outside of the boundaries (ReverseTravel?)

(Routine): Runs realsense capture and OpenCV portion. After we take the first image and it finds a contour and moves the robot over top of it, I want it to take another image to confirm we centered the contour to the imager.

(getPoint): this function recieves current GPS location and needs to return the current coordinate point to be checked against the boundary

(check): checks current location

*(xMoveRefinement and yMoveRefinement): Same as (xMove and yMove) but has a threshold. Maybe the threshold should also be set on the initial movements too so that if the divot is aligned on either of the axis, it won’t try to move. ***We can work on this later***

*(Tool Offset): This is because the movements are intended to align the divot with the center of the image taken. The divot fixing tool obviously cannot be in the center of the image so I imagined it offset some distance that the bot will need to travel in order to actually align the divot and tool. ***We can work on this later***

*(FixDivot): This function will be driving the servo with tool attached. ***I can work on this later***

