### This script currently gets the coordinates from the GPS unit.
### I currently have it just running for 5 seconds and then averaging the values recieved to get an average position 
### incase the GPS signal is noisy. 

### I dont really intend on using the time aspect in the real code but just run this 
### script in the background and then the 'avgLatCoord' and 'avgLonCoord' to be saved as the 'Point' variable from the 
### other GPS script. Then that variable will be checked right before it does the routine movement.




import serial
import time
from ublox_gps import UbloxGps

port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
gps = UbloxGps(port)

#def run():
maxTime = 5
startTime = time.time()

dataLatSum = []
dataLonSum = []

try:
    print("Listening for UBX Messages")
    while (time.time() - startTime) < maxTime:
        try:
            geo = gps.geo_coords()
            print("Longitude: ", geo.lon)
            print("Latitude: ", geo.lat)
            #print("Heading of Motion: ", geo.headMot)
            dataLatSum.append(float(geo.lat))
            dataLonSum.append(float(geo.lon))
        except (ValueError, IOError) as err:
            print(err)

finally:
    port.close()
    avgLatCoord = (sum(dataLatSum) / len(dataLatSum))
    avgLonCoord = (sum(dataLonSum) / len(dataLonSum))
    print("Average Lat: ", avgLatCoord)
    print("Average Lon: ", avgLonCoord)
