from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, mavutil

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('tcp:192.168.138.131:5760', wait_ready=True)

vehicle.gimbal.rotate(-45,13,5)


# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()