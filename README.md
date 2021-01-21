# machine1

I have written quite a bit of random code for the serial communicaiton between the Pi and Arduino and honestly just really confused now. 

This is the process in which I want to run the program... I can work on the other portions of it after this part is figured out. I'm stumped.

1. Arduino sends "Comm's Ready" at the beginning to alert the Pi the serial is working. Once Pi receives "Comm's Ready", proceed with the image processing portion of the program. I believe I called it 'openCV()' in the python code.

2. Once openCV() is complete it should serially send an encoded message to the arduino called 'YpulseEncode', this is the number of steps my stepper motor needs to do in order to align the divot in the center of the camera screen. 

3. Once the stepper has completed that move I want it to serially send a confirmation called yMovementComplete. This tells the Pi to now send the 'XpulseEncode' value. Once again send the 'xMovementComplete' signal back to the Pi to let it know it has finished that move.

There is probably a better flow/ easier flow to write but that's just how I was thinking. (Sending both pulseEncode values at once but performing one then the other?). There is a lot of random code in there that I have been trying out so some stuff is in there and not even being used. 
