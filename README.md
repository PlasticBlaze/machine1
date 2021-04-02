# machine1

Project Flow -->
Turn device on, Hole Selection GUI, Run (routine) and then stop for image taking. Open realsense pipeline to (TakeImage) --> Take/ process image. Evaluate and send (xMove and yMove) pulse counts to arduino motor board. --> Move to respective locations in each axis, then send (xMoveComplete and yMoveComplete) (confirmation) back to Pi. --> Pi performs TakeImage again to see if the object is in the center of the image frame ***Not sure if Pi should determine this or if Arduino should determine this, but I want to set a threshold, ‘if more than (20 mm?) off in either axis perform movements again’*** If over threshold, send (xMoveRefinement) and (yMoveRefinement). --> Perform refinement movements if threshold reached, then add another movement command in arduino code to move to tool (Tool Offset), then (Fix divot), once complete perform (routine)


Variables -->
(Routine): All 4 stepper motors travel far enough to get a new image. For example, if the image frame is 3 feet in height, the pulse count will be enough to travel greater than 3 feet so that a new area is being inspected.

(TakeImage): Runs realsense capture and OpenCV portion. Might want to change this portion in the future. Will still send the same variables to Arduino.

(RefineImage): The movement refinement I talked about to confirm it’s at the correct location.

(xMoveRefinement and yMoveRefinement): Same as (xMove and yMove) but has a threshold. Maybe the threshold should also be set on the initial movements too so that if the divot is aligned on either of the axis, it won’t try to move. 

(Tool Offset): This is because the movements are intended to align the divot with the center of the image taken. The divot fixing tool obviously cannot be in the center of the image so I imagined it offset some distance that the bot will need to travel in order to actually align the divot and tool.

(FixDivot): This function will be driving the servo with tool attached.


Maybe the GPS coordinates should be checked after each (Routine) distance traveled because it will have just moved to a new location. and the Check() function can be called.
