# machine1

I have written quite a bit of random code for the serial communicaiton between the Pi and Arduino and honestly just really confused now. 

This is the process in which I want to run the program... I can work on the other portions of it after this part is figured out. I'm stumped.

1. Arduino sends "Comm's Ready" at the beginning to alert the Pi the serial is working. Once Pi receives "Comm's Ready", proceed with the image processing portion of the program. I believe I called it 'openCV()' in the python code.

2. Once openCV() is complete it should serially send an encoded message to the arduino called 'YpulseEncode', this is the number of steps my stepper motor needs to do in order to align the divot in the center of the camera screen. 

3. Once the stepper has completed that move I want it to serially send a confirmation called yMovementComplete. This tells the Pi to now send the 'XpulseEncode' value. Once again send the 'xMovementComplete' signal back to the Pi to let it know it has finished that move.

There is probably a better flow/ easier flow to write but that's just how I was thinking. (Sending both pulseEncode values at once but performing one then the other?). There is a lot of random code in there that I have been trying out so some stuff is in there and not even being used. 


I found an example of another project somebody has completed that seems to be doing a relatively similar process flow. I'm just having trouble following his program. I figured somebody that knows python would better be able to tell what hes doing for the communication aspect. https://github.com/pacogarcia3/hta0-horizontal-robot-arm

Here is another example (albeit has a lot of other pointless stuff going on). Mostly concerned with writing the portion that pertains to the serial communication and setting states from 0 to 1 in order to control the flow or timeline (handshaking) of the program between the two boards. https://github.com/ANM-P4F/ProductSortingSystem/blob/master/arduino/actuator/actuator.ino




Variables and other info. Link to images of the document below. Didn't know how else to post it. .txt of it is after.
https://imgur.com/a/u2bYR5P

***
Variables and Other Info.


Below is overall flow, items in parenthesis are variables/ commands to send to the Arduino code. Each variable is explained after. Red text is Pi actions, blue is Arduino actions.

Sorry if this is confusing. I think this is a good start for the flow. It’s what I could come up with off the top of my head. 


Project Flow -->
Turn device on, maybe press a button ***haven’t figured this part out, don’t know if you know how easy this would be*** to start both programs. Confirm communications is open and ready. --> Run (routine) and then stop for image taking. Command Pi to (TakeImage) --> Take/ process image. Evaluate and either send (bad area) command or send (xMove and yMove) pulse counts. --> Move to respective locations in each axis, then send (xMoveComplete and yMoveComplete) (confirmation) back to Pi. --> Pi performs (RefineImage) which will only do the color recognition part of the opencv. ***Not sure if Pi should determine this or if Arduino should determine this, but I want to set a threshold, ‘if more than 20 mm off in either axis perform movements again’*** If over threshold, send (xMoveRefinement) and (yMoveRefinement). --> Perform refinement movements if threshold reached, then add another movement command in arduino code to move to tool (Tool Offset), then (Fix divot), once complete perform (routine)


Variables -->
(Routine): All 4 stepper motors travel far enough to get a new image. For example, if the image is 3 feet in height, the pulse count will be enough to travel greater than 3 feet so that a new area is being inspected.

(TakeImage): Runs OpenCV portion. Might want to change this portion in the future. Will still send the same variables to Arduino.

(BadArea): My idea of how to keep it on the green and not wander off the area we’re intending on fixing. If it sees the fringe, (BadAreaLeft) or (BadAreaRight) will tell the Arduino to turn away from that direction and travel another (routine) distance. I’m going to attempt to figure this out on OpenCV.
(xMove and yMove): Can be separate or together, whatever is easier for the Arduino to take in and execute.

(RefineImage): The movement refinement I talked about to confirm it’s at the correct location.

(xMoveRefinement and yMoveRefinement): Same as (xMove and yMove) but has a threshold. Maybe the threshold should also be set on the initial movements too so that if the divot is aligned on either of the axis, it won’t try to move. 

(Tool Offset): This is because the movements are intended to align the divot with the center of the image taken. The divot fixing tool obviously cannot be in the center of the image so I imagined it offset some distance that the bot will need to travel in order to actually align the divot and tool.

(FixDivot): This function should be driving the ball screw stepper up and down to fix the divot.
