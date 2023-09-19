"""
Functions used to adjust parameters
"""
import serial
import time 

def tool_offset():
    """
    Further description in the future
    """
    print("tool_ofset processing")


def fix_divot():
    """
    Controls servo.
    """
    import serial
    import time
    
    # configure the serial connections (the parameters differs on the device you are connecting to)
    serial1 = serial.Serial('COM5', 115200)
    
    # SEND 'ALARM RESET'
    serial1.write(b':01050407FF00F0\r\n')
    time.sleep(.2)
    
    # SEND 'PIO SWITCHING OFF'
    serial1.write(b':010504270000CF\r\n')
    time.sleep(.2)
    
    # SEND 'PIO SWITCHING ON'
    serial1.write(b':01050427FF00D0\r\n')
    time.sleep(.2)
    
    # SEND 'SERVO OFF'
    serial1.write(b':010504030000F3\r\n')
    time.sleep(.2)
    
    # SEND 'SERVO ON'
    serial1.write(b':01050403FF00F4\r\n')
    time.sleep(.2)
    
    # SEND 'ALARM RESET'
    serial1.write(b':01050407FF00F0\r\n')
    time.sleep(.2)
    
    
    # Divot Loop
    
    # SEND 'POSITION 0'
    serial1.write(b':01069800000061\r\n')
    time.sleep(.5)
    
    # SEND 'POSITION 1'
    serial1.write(b':01069800000160\r\n')
    time.sleep(1)
    
    # SEND 'POSITION 2'
    serial1.write(b':0106980000025F\r\n')
    time.sleep(.5)
    
    # SEND 'POSITION 3'
    serial1.write(b':0106980000035E\r\n')
    time.sleep(.5)
    
    # REPEATED
    
    # SEND 'POSITION 2'
    serial1.write(b':0106980000025F\r\n')
    time.sleep(.5)
    
    # SEND 'POSITION 3'
    serial1.write(b':0106980000035E\r\n')
    time.sleep(.5)
    
    # SEND 'POSITION 4'
    #serial1.write(b':0106980000045D\r\n')
    #time.sleep(.5)
    
    
    # SEND 'POSITION 0'
    serial1.write(b':01069800000061\r\n')
    time.sleep(.5)
    
    # SEND 'POSITION 5'
    #serial1.write(b':0106980000055C\r\n')
    #time.sleep(.5)
    
    # SEND 'ALARM RESET'
    serial1.write(b':01050407FF00F0\r\n')
    time.sleep(.5)
    
    # SEND 'SERVO OFF'
    serial1.write(b':010504030000F3\r\n')
    time.sleep(.5)
    
    print("fix_divot processing")
